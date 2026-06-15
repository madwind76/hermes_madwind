---
title: head-dump — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, research, writeup, api, source-analysis, storage]
sources: [https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/head-dump/head-dump.md, https://medium.com/@rahmeez/picoctf-head-dump-writeup-2455761c362d, https://medium.owasp-cebu.org/head-dump-web-exploitation-3d378f5cfddb, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/]
confidence: high
---

# head-dump — picoCTF 2025 web writeup

> API 문서에서 진단 엔드포인트를 찾아 heap snapshot을 내려받고, 메모리 덤프 안에서 flag prefix를 검색하는 picoCTF 2025 Web Exploitation 입문 문제입니다.

## 1. 한 줄 요약
- 블로그형 사이트 안의 **API Documentation** 링크가 `/api-docs`로 이어집니다.
- Swagger UI에서 진단용 `/heapdump` 엔드포인트를 찾습니다.
- endpoint를 실행해 `.heapsnapshot` 파일을 다운로드한 뒤 `picoCTF{` 문자열을 검색합니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 문제명 | head-dump |
| 카테고리 | Web Exploitation |
| 점수 | 50 |
| 핵심 아이디어 | API documentation discovery, Swagger UI, heap dump inspection |
| 난이도 | easy / beginner |
| 관련 개념 | [[heap-dump-ctf-patterns]], [[api-security]], [[web-ctf-writeup-internal-service]] |

## 3. 공격면 정리
| Route / 위치 | Method | Auth | Input | Output | Notes |
|---|---|---|---|---|---|
| `/` | GET | No | 없음 | picoCTF News 블로그 | API Documentation 링크 탐색 |
| `/api-docs` | GET | No | 없음 | Swagger UI | API route 목록 노출 |
| `/heapdump` | GET 또는 Swagger 실행 | No | 없음 | `.heapsnapshot` 파일 | 서버 메모리 snapshot 다운로드 |
| heap snapshot 파일 | Local search | N/A | `picoCTF{` 검색 | flag 문자열 | 대용량 파일 직접 검색 |

## 4. 풀이 흐름
1. 문제 사이트를 열고 페이지 본문과 HTML source를 확인합니다.
2. `API Documentation`, `swagger UI`, `/api-docs` 같은 링크를 찾습니다.
3. `/api-docs`에 접속해 Swagger UI에 표시된 엔드포인트 목록을 봅니다.
4. `Diagnosing` 또는 유사 섹션에서 `/heapdump` 엔드포인트를 찾습니다.
5. Swagger UI의 **Try it out → Execute** 또는 직접 요청으로 heap snapshot 파일을 다운로드합니다.
6. 파일이 크므로 전체를 읽지 말고 flag prefix를 검색합니다.
7. `picoCTF{...}` 형식의 문자열을 확인합니다.

## 5. 재현용 명령 예시
아래 명령은 CTF 문제 인스턴스에서 내려받은 heap snapshot을 **로컬에서 분석하는 교육용 예시**입니다.

```bash
# 현재 디렉터리에 있는 heap snapshot 파일에서 picoCTF flag 형식을 검색합니다.
# 예상 출력: picoCTF{...} 형식의 문자열이 포함된 줄이 출력됩니다.
grep -E 'picoCTF\{[^}]+\}' heapdump-*.heapsnapshot
```

```bash
# 파일이 바이너리처럼 보이거나 줄이 길 때 strings로 사람이 읽을 수 있는 문자열만 추출한 뒤 검색합니다.
# 예상 출력: parsed.txt 안에서 picoCTF{...} 문자열이 발견됩니다.
strings heapdump-*.heapsnapshot > parsed.txt  # heap snapshot에서 출력 가능한 문자열만 추출합니다.
grep -E 'picoCTF\{[^}]+\}' parsed.txt       # 추출된 문자열에서 flag prefix를 검색합니다.
```

## 6. 핵심 학습 포인트
- **API 문서 자체가 공격면**입니다. `/api-docs`, `/swagger`, `/openapi.json`은 숨겨진 기능 발견에 도움을 줄 수 있습니다.
- **진단 엔드포인트는 민감합니다.** `/heapdump`는 원래 메모리 누수 분석용이지만, 외부에 열리면 secret·token·flag가 노출될 수 있습니다.
- **덤프 파일은 검색 우선**입니다. 대용량 파일을 눈으로 읽기보다 flag prefix나 키워드로 좁혀야 합니다.
- 문제명 `head-dump`는 `heapdump`와 연결되는 힌트로 볼 수 있습니다.

## 7. 방어 관점
- 운영 환경에서 Swagger UI와 OpenAPI 문서를 공개할지 별도 정책을 둡니다.
- `/heapdump`, `/debug`, `/diagnostics`, `/actuator/*` 같은 엔드포인트는 외부 인터넷에서 접근할 수 없게 합니다.
- 진단 기능이 꼭 필요하면 인증, 관리자 권한, 내부망 제한, 짧은 보관 기간을 적용합니다.
- memory dump 파일은 secret scanning과 보관 정책의 대상에 포함합니다.

## 8. 관련 위키 링크
- [[heap-dump-ctf-patterns]] — heap dump의 의미와 CTF 패턴
- [[api-security]] — API 보안 개요
- [[api-security-defense]] — Swagger/OpenAPI 운영 방어
- [[ssrf-core]] — 내부 진단 엔드포인트와 민감 정보 노출 예시
- [[signed-html-email-ctf-patterns]] — 이메일/HTML 렌더링 sink가 비밀값을 노출하는 비교 사례
- [[web-ctf-writeup-internal-service]] — 내부 서비스/진단 엔드포인트 계열 허브
- [[web-ctf-writeup-curation]] — Web CTF writeup 큐레이션
- [[web-ctf-writeup-topic-map]] — Web CTF 상위 지도

## 9. 참고 소스
- [snwau GitHub writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/head-dump/head-dump.md)
- [Rehema Said Medium writeup](https://medium.com/@rahmeez/picoctf-head-dump-writeup-2455761c362d)
- [OWASP Cebu Medium writeup](https://medium.owasp-cebu.org/head-dump-web-exploitation-3d378f5cfddb)
- [qz.sg picoCTF 2025 Web Exploitation writeups](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)

## 10. 다음 연결
- `Cookie Monster Secret Recipe`처럼 브라우저 저장소에서 flag를 찾는 문제와 비교하면 “클라이언트 저장소 vs 서버 메모리 덤프” 차이를 이해하기 좋습니다.
- `secure-email-service`와 비교하면 “서버 메모리 덤프 vs 브라우저 HTML sink”의 차이가 선명해집니다.
- `SSRF` 계열 문제와 함께 보면, 내부 진단 엔드포인트가 외부 입력으로 간접 노출되는 시나리오까지 확장할 수 있습니다.

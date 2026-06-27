---
title: URL-to-PDF SSRF — internal service writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, ssrf, internal-service, proxy]
sources: [https://github.com/muhashali/writeup-SSRF, https://github.com/jdonsec/allthingsssrf, https://github.com/orangetw/My-CTF-Web-Challenges]
confidence: medium
---

# URL-to-PDF SSRF — internal service writeup

> 외부 URL을 PDF로 렌더링하는 기능이 내부 서비스 접근으로 이어지는 SSRF 계열 writeup입니다.

## 참고 URL
- [muhashali/writeup-SSRF](https://github.com/muhashali/writeup-SSRF)
- [jdonsec/allthingsssrf](https://github.com/jdonsec/allthingsssrf)
- [orangetw/My-CTF-Web-Challenges](https://github.com/orangetw/My-CTF-Web-Challenges)


## 1. 한 줄 요약
- 사용자가 넣은 URL을 서버가 대신 fetch합니다.
- 내부 IP나 localhost 접근이 막혀 있지 않으면 민감한 내부 응답이 PDF로 되돌아옵니다.
- SSRF는 단독 취약점보다 다른 내부 서비스와 연결될 때 더 강해집니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 카테고리 | Web / SSRF |
| 핵심 아이디어 | URL fetch, loopback access, internal service exposure |
| 관련 개념 | [[ssrf-ctf-patterns]], [[ssrf-core]], [[ssrf-defense]] |
| 관련 survey | [[ssrf-internal-service-writeup-survey]] |

## 3. 관찰 포인트
1. 입력값이 외부 URL처럼 보이는지 확인합니다.
2. redirect, scheme, host 검증이 약한지 봅니다.
3. `127.0.0.1`, `localhost`, 사설 대역, 메타데이터 엔드포인트를 시도합니다.
4. 응답이 파일/PDF/preview로 돌아오는지 확인합니다.

## 4. 풀이 흐름
1. URL 입력 지점과 서버의 fetch 위치를 찾습니다.
2. 외부 URL로 정상 동작을 확인한 뒤 내부 대역으로 바꿔 봅니다.
3. 차단되면 redirect, scheme, 호스트별 우회 조건을 실험합니다.
4. 내부 서비스 응답이 렌더링 결과에 흘러나오면 flag를 수집합니다.

## 5. 방어 관점
- allowlist 기반으로 허용 대상을 제한합니다.
- 내부 대역과 메타데이터 주소를 별도로 차단합니다.
- redirect 체인을 무조건 신뢰하지 않습니다.
- 서버가 대신 요청하는 기능은 공격 표면으로 본 뒤 설계합니다.

## 6. 다음 연결
- [[ssrf-internal-service-writeup-survey]]
- [[ssrf-ctf-patterns]]
- [[proxy-mirror-final-writeup]]

---
title: GET aHEAD — picoCTF web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, http, method-manipulation, burp, head, get]
sources: [https://medium.com/@ahmednarmer1/ctf-day-13-2ad289797f14, https://medium.com/@Kamal_S/picoctf-web-exploitation-get-ahead-fb9fa30d8f3d, https://emilgallajov.medium.com/picoctf-get-ahead-writeup-10ace6190a03]
confidence: high
---

# GET aHEAD — picoCTF web writeup

> HTTP `GET` 요청을 `HEAD`로 바꾸면 응답 본문 대신 헤더 쪽에서 flag가 드러나는 picoCTF Web Exploitation 문제입니다.

## 1. 한 줄 요약
- 제목 자체가 힌트입니다.
- **`GET` → `HEAD`** 로 바꾸는 것이 핵심입니다.
- Burp Suite 같은 프록시 도구로 요청을 수정하면 flag를 얻을 수 있습니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 화면에는 색상 버튼만 보임 | UI만으로는 답이 안 보임 |
| 2 | 요청을 Burp로 캡처 | HTTP 메서드 수정이 가능함 |
| 3 | `GET aHEAD`라는 제목 확인 | `HEAD` 메서드가 핵심이라는 힌트 |
| 4 | 요청 메서드를 `HEAD`로 변경 | 서버 응답이 달라짐 |
| 5 | flag 확인 | 문제 해결 |

## 3. 분석 포인트
```bash
# HTTP 메서드를 GET에서 HEAD로 바꿔 테스트합니다.
# 예상 결과: 응답 본문 대신 헤더에서 flag가 드러날 수 있습니다.
# Burp Repeater에서 요청 메서드만 수정하면 됩니다.
```

## 4. 공격자 관점
1. 챌린지 URL을 열고 버튼 동작을 확인합니다.
2. Burp Suite로 요청을 캡처합니다.
3. 기본 `GET` 요청을 확인합니다.
4. 요청 메서드를 `HEAD`로 바꿉니다.
5. 응답에 flag가 포함되는지 확인합니다.

## 5. 방어자 관점
- 메서드별 응답 차이에 민감한 정보가 실리지 않도록 합니다.
- `HEAD` 요청에도 `GET`과 동일한 민감한 메타데이터가 노출되지 않게 합니다.
- HTTP 메서드 처리 로직을 일관되게 구현합니다.
- 테스트용 UI와 실제 데이터 노출을 분리합니다.

## 6. 같이 보면 좋은 페이지
- [[http-method-manipulation-ctf-patterns]]
- [[http]]
- [[burp-suite]]
- [[includes-final-writeup]]

## 7. 참고 소스
- [Ahmed Narmer — CTF Day(13): GET aHEAD](https://medium.com/@ahmednarmer1/ctf-day-13-2ad289797f14)
- [Kamal S — picoCTF Web Exploitation: GET aHEAD](https://medium.com/@Kamal_S/picoctf-web-exploitation-get-ahead-fb9fa30d8f3d)
- [Emil Gallajov — picoCTF: GET aHEAD writeup](https://emilgallajov.medium.com/picoctf-get-ahead-writeup-10ace6190a03)

---
title: login — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, client-side, source-inspection, base64, javascript, login]
sources: [https://medium.com/@ahmednarmer1/ctf-day-37-9587a06c6498, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/, https://hackmd.io/@fearnot/picoCTF_Web]
confidence: high
---

# login — picoCTF 2025 web writeup

> 로그인 폼 자체를 공격하는 문제가 아니라, **클라이언트 측 JavaScript 안에 Base64로 숨은 자격 증명**을 찾아 디코딩하는 picoCTF 2025 Web Exploitation 문제입니다.

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-37-9587a06c6498)
- [blog.qz.sg](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [hackmd.io](https://hackmd.io/@fearnot/picoCTF_Web)


## 1. 한 줄 요약
- UI는 평범한 로그인 폼처럼 보이지만, 실제 단서는 **page source와 JS 파일**에 있습니다.
- username/password가 **Base64 인코딩 문자열**로 숨겨져 있습니다.
- 핵심은 브루트포스가 아니라 **source inspection + decoding**입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 폼이 보임 | 일반적인 인증 문제처럼 보임 |
| 2 | HTML / JavaScript를 확인 | 클라이언트 측에 힌트가 있을 가능성 확인 |
| 3 | Base64 문자열 발견 | 자격 증명 또는 flag 조각이 숨겨짐 |
| 4 | 디코딩 | 실제 username/password 획득 |
| 5 | 로그인 성공 | flag 또는 다음 단계 접근 |

## 3. 대표 분석 예시
```bash
# Base64 문자열을 사람이 읽는 문자열로 복원합니다.
# 예상 결과: 숨겨진 username, password, 또는 flag 조각이 출력됩니다.
echo 'YWRtaW4=' | base64 -d
```

## 4. 공격자 관점
1. 로그인 폼을 보자마자 SQLi부터 시도하지 않고 source를 확인합니다.
2. JavaScript에서 `Base64`처럼 보이는 문자열을 찾습니다.
3. `admin`, `password`, `flag` 조각이 인코딩돼 있는지 확인합니다.
4. 디코딩한 값을 로그인에 사용합니다.
5. 필요하면 쿠키/세션 동작을 추가로 관찰합니다.

## 5. 방어자 관점
- 자격 증명이나 flag 조각을 HTML/JS에 넣지 않습니다.
- Base64는 보안이 아니라 인코딩입니다.
- 인증 로직은 반드시 서버에서 처리합니다.
- 소스맵, 주석, 테스트 문자열에 민감 정보를 남기지 않습니다.

## 6. 같이 보면 좋은 페이지
- [[client-side-secret-exposure-ctf-patterns]]
- [[source-inspection-minification-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[web-ctf-writeup-client-side]]

## 7. 참고 소스
- [Ahmed Narmer — picoCTF Web Exploitation: login](https://medium.com/@ahmednarmer1/ctf-day-37-9587a06c6498)
- [PicoCTF 2025 Web Exploitation Writeups](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [picoCTF Web writeup - HackMD](https://hackmd.io/@fearnot/picoCTF_Web)

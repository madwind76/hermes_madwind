---
title: IntroToBurp — picoCTF 2024 web writeup
created: 2026-06-13
updated: 2026-06-15
type: query
tags: [ctf, web, burp, parameter-tampering, picoctf]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/IntroToBurp.md, https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-introtoburp-ecbcfc60272e, https://medium.com/@Kamal_S/picoctf-web-exploitation-introtoburp-a2b50bf8e985, https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99]
confidence: high
---

# IntroToBurp — picoCTF 2024 web writeup

> `IntroToBurp`는 **Burp Suite로 요청 구조를 관찰한 뒤, OTP 파라미터를 완전히 제거해서 우회하는 picoCTF 2024 Web 문제**입니다. 값 자체를 맞히는 문제가 아니라, **서버가 필수 파라미터 존재 여부를 제대로 검증하는지**를 확인하는 것이 핵심입니다.

## 1. 한 줄 요약
- 등록 후 `/dashboard`의 OTP 제출 요청을 Burp Suite로 가로챕니다.
- OTP 값을 바꿔도 `Invalid OTP`가 반환됩니다.
- `otp` 값을 다른 값으로 바꾸는 것이 아니라, **`otp` 파라미터 자체를 삭제**해야 합니다.
- 빈 POST body로 재전송하면 flag가 반환됩니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 등록 폼은 아무 입력이나 받아들임 | 초기 입력 검증은 핵심이 아님 |
| 2 | 이후 OTP 페이지로 이동 | 2단계 인증 흐름처럼 보임 |
| 3 | `otp=123456` 등 임의 값 입력 | 단순 값 변경은 실패 |
| 4 | Burp Repeater에서 요청 구조를 수정 | 요청 변조가 핵심 |
| 5 | `otp` 파라미터를 제거한 뒤 전송 | 서버의 필수 필드 검증 누락 |
| 6 | flag 응답 획득 | 최종 성공 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 취약한가
이 문제는 OTP 숫자 자체의 강도보다, **서버가 `otp` 필드의 존재를 반드시 요구하지 않는 점**이 취약점입니다. 즉, 서버는 “잘못된 값”과 “아예 없는 값”을 다르게 다뤄야 하는데, 후자를 놓쳤습니다.

### 3.2 실전 확인 포인트
```bash
# Burp로 가로챈 요청에서 OTP 위치를 확인합니다.
# 예상 결과: POST body 또는 form data에 otp 파라미터가 보입니다.
# 예시: otp=0000
```

```bash
# Burp Repeater에서 다음 세 가지를 비교합니다.
# 1) otp 값을 다른 값으로 변경
# 2) otp를 빈 문자열로 변경
# 3) otp 파라미터 자체를 삭제
# 예상 결과: 3)에서만 flag가 반환됩니다.
```

## 4. 공격자 관점
1. 브라우저에서 등록 절차를 완료합니다.
2. OTP 제출 요청을 Burp Suite로 가로챕니다.
3. Repeater로 보내서 요청을 여러 방식으로 변형합니다.
4. `otp` 값만 바꾸는 시도는 모두 실패하는지 확인합니다.
5. `otp` 파라미터를 삭제한 뒤 재전송합니다.
6. flag 응답을 확인합니다.

## 5. 방어자 관점
- 필수 파라미터는 **존재 여부와 형식**을 모두 서버에서 검증해야 합니다.
- OTP는 세션과 강하게 바인딩해야 합니다.
- 프런트엔드에서만 검사하면 Burp 같은 도구로 쉽게 우회됩니다.
- 빈 요청이나 누락 필드에 대한 예외 처리를 명확히 해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[parameter-tampering-ctf-patterns]]
- [[burp-request-mutation]]
- [[burp-suite]]
- [[web-ctf-master-checklist]]
- [[web-ctf-writeup-auth-session]]

## 7. 참고 소스
- [noamgariani11 — IntroToBurp writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/IntroToBurp.md)
- [Bl4cky — picoCTF 2024 — Web Exploitation: IntroToBurp](https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-introtoburp-ecbcfc60272e)
- [Kamal S — picoCTF Web Exploitation: IntroToBurp](https://medium.com/@Kamal_S/picoctf-web-exploitation-introtoburp-a2b50bf8e985)
- [InfoSec Write-ups — picoCTF 2024 Web](https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99)

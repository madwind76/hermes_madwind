---
title: Cookies — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, cookies, parameter-tampering, enumeration, picoctf]
sources: [https://ctftime.org/writeup/27377, https://medium.com/@Kamal_S/picoctf-web-exploitation-cookies-c85d0df3f1d6, https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/Cookies.md]
confidence: high
---

# Cookies — picoCTF 2021 web writeup

> `Cookies`는 **서버가 쿠키 값 하나를 상태값처럼 사용하고, 그 값을 열거하면 숨은 응답이나 flag를 얻을 수 있는** picoCTF 2021 Web 문제입니다. 이 문제의 포인트는 복잡한 암호학이 아니라, **클라이언트가 보낸 쿠키를 서버가 그대로 신뢰하는지 확인하는 것**입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/27377)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-cookies-c85d0df3f1d6)
- [Original writeup](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/Cookies.md)


## 1. 한 줄 요약
- 입력값 `snickerdoodle`를 넣으면 쿠키 `name=0`이 설정됩니다.
- 쿠키 값 `name`을 0, 1, 2, ... 식으로 바꾸면 서버 응답이 달라집니다.
- 특정 값에서 flag가 드러납니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 임의 문자열은 invalid cookie로 거절됨 | 입력 검증이 있음 |
| 2 | `snickerdoodle`는 특별 처리됨 | 시작점이 되는 sentinel 값 |
| 3 | 쿠키 `name=0`이 설정됨 | 서버가 쿠키를 상태로 사용 |
| 4 | 쿠키 값을 1, 2, 3...로 바꿔봄 | 값 열거 가능 |
| 5 | 특정 숫자에서 응답이 달라짐 | flag 위치 발견 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 **쿠키는 클라이언트가 임의로 바꿀 수 있다**는 기본 원리를 보여줍니다. 서버가 쿠키 값을 권한/상태의 원천으로 사용하면, 공격자는 값만 바꿔서 다른 분기를 강제할 수 있습니다.

### 3.2 실전 확인 포인트
```bash
# 브라우저 개발자 도구나 Burp로 name 쿠키 값을 관찰합니다.
# 예상 결과: snickerdoodle 입력 후 name=0이 설정됩니다.
```

```bash
# name 값을 순차적으로 바꾸며 서버 응답 길이/내용을 비교합니다.
# 예상 결과: 특정 값에서 flag 또는 다른 응답이 나타납니다.
```

### 3.3 풀이 흐름
1. 페이지에 접속해 입력 폼을 확인합니다.
2. `snickerdoodle`를 넣어 쿠키를 설정합니다.
3. `name` 쿠키 값을 수동으로 바꿔봅니다.
4. Burp Intruder 또는 간단한 스크립트로 1~20 범위를 열거합니다.
5. 응답이 달라지는 값을 찾습니다.
6. 해당 응답에서 flag를 확인합니다.

## 4. 공격자 관점
- 복잡한 우회보다 **상태값 열거**가 핵심입니다.
- 쿠키 값이 서버 로직의 분기 키라면, 쿠키 조작만으로 우회가 가능합니다.
- 자동화 도구 없이도 수동으로 빠르게 확인할 수 있는 쉬운 문제입니다.

## 5. 방어자 관점
- 클라이언트 쿠키에 중요한 상태를 직접 넣지 않습니다.
- 서버는 쿠키 값이 변경 가능하다고 가정해야 합니다.
- 민감한 분기에는 서버 측 세션과 서명을 사용해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[cookie-client-storage-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[most-cookies-final-writeup]]
- [[power-cookie-final-writeup]]
- [[more-cookies-final-writeup]]

## 7. 참고 소스
- [CTFtime — Cookies](https://ctftime.org/writeup/27377)
- [Kamal S — picoCTF Web Exploitation: Cookies](https://medium.com/@Kamal_S/picoctf-web-exploitation-cookies-c85d0df3f1d6)
- [ZeroDayTea — Cookies writeup](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/Cookies.md)

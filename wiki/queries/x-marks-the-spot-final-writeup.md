---
title: X marks the spot — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, xpath, injection, login-bypass, picoctf]
sources: [https://picoctf2021.haydenhousen.com/web-exploitation/x-marks-the-spot, https://ctftime.org/writeup/27158, https://ctftime.org/writeup/27171, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/X%20marks%20the%20spot/script.py]
confidence: high
---

# X marks the spot — picoCTF 2021 web writeup

> `X marks the spot`는 **blind XPath injection**으로 로그인 검증을 우회하고, 응답 차이를 이용해 사용자 정보와 flag를 점차 복원하는 picoCTF 2021 Web 문제입니다. 핵심은 SQLi와 비슷해 보이지만, 실제로는 **XML/XPath 쿼리 문법**을 공격하는 점입니다.

## 1. 한 줄 요약
- 서버는 로그인 확인을 XML/XPath 질의로 처리합니다.
- 입력을 조합하면 조건식을 바꿔 로그인 검증을 우회할 수 있습니다.
- blind 형태라서 한 번에 flag가 나오지 않고, **응답 차이**를 통해 한 글자씩 추론합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 폼이 존재함 | 인증 우회 대상 |
| 2 | 일반 SQLi처럼 보이지만 동작이 다름 | XPath 가능성 |
| 3 | 응답이 참/거짓에 따라 달라짐 | blind oracle 가능 |
| 4 | `starts-with()` / `contains()` 같은 함수가 유용함 | 문자열 추측 가능 |
| 5 | 조건을 반복해 flag를 복원 | 자동화 스크립트가 잘 맞음 |

## 3. 핵심 분석
### 3.1 왜 XPath injection인가
XPath는 XML 문서에서 노드를 찾는 질의 언어입니다. 입력값이 XPath 식에 그대로 붙으면, 공격자가 `or 1=1` 비슷한 조건을 넣어 참 조건을 만들 수 있습니다.

### 3.2 실전 확인 포인트
```python
# XPath 주입의 형태를 이해하기 위한 예시입니다.
# 예상 결과: 조건식이 참이 되도록 바꾸면 인증 로직이 우회됩니다.
payload = "' or '1'='1"
print(payload)
```

```python
# blind 추측에서는 starts-with()와 contains()가 자주 쓰입니다.
# 예상 결과: 참/거짓 응답 차이로 문자열을 복원합니다.
expr = "starts-with(password, 'picoCTF{')"
print(expr)
```

### 3.3 풀이 흐름
1. 로그인 요청을 Burp Suite로 잡습니다.
2. 입력값이 XPath 식에 들어가는지 확인합니다.
3. 참/거짓에 따라 응답이 달라지는지 테스트합니다.
4. `starts-with()` 또는 `contains()`로 문자 단위를 추측합니다.
5. 자동화 스크립트로 username/password/flag를 복원합니다.

## 4. 공격자 관점
- XPath는 SQL과 유사하게 보이지만, 문자열 인코딩과 함수 사용법이 다릅니다.
- blind 방식이기 때문에 소량의 응답 차이를 자동화로 수집하는 것이 핵심입니다.
- 로그인 검사 로직이 XML에 의존하면, 백엔드 구조가 노출된 셈입니다.

## 5. 방어자 관점
- XPath 식을 문자열 결합으로 만들지 말고, 매개변수화 또는 안전한 API를 사용합니다.
- 입력값에 대한 allowlist 검증을 하되, 쿼리 구조 자체를 사용자 입력과 분리합니다.
- 인증 로직은 XML/XPath보다 명확한 서버측 세션 검증을 우선합니다.

## 6. 같이 보면 좋은 페이지
- [[xpath-injection-ctf-patterns]]
- [[web-ctf-writeup-parser-template]]
- [[xxe]]

## 7. 참고 소스
- [Hayden Housen — X marks the spot](https://picoctf2021.haydenhousen.com/web-exploitation/x-marks-the-spot)
- [CTFtime — X marks the spot](https://ctftime.org/writeup/27158)
- [CTFtime — X marks the spot](https://ctftime.org/writeup/27171)
- [HHousen — script.py](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/X%20marks%20the%20spot/script.py)

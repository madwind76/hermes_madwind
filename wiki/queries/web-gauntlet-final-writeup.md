---
title: Web Gauntlet — picoCTF 2020 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, sqlite, sqli, filter-bypass, picoctf]
sources: [https://github.com/onealmond/hacking-lab/blob/master/picoctf-2020/web-gauntlet/writeup.md, https://medium.com/@sobatistacyber/picoctf-writeup-web-gauntlet-7c3b8c7c7946, https://www.youtube.com/watch?v=ZQj5tSwaG0k]
confidence: high
---

# Web Gauntlet — picoCTF 2020 web writeup

> `Web Gauntlet`는 **SQLite 기반 로그인 폼에서 필터를 우회해 admin으로 로그인하는 picoCTF 2020 Web 문제**입니다. 핵심은 차단된 키워드와 연산자를 피하면서, SQLite의 문자열 결합과 주석 처리 규칙을 이용해 `admin` 조건을 깨는 것입니다.

## 참고 URL
- [Original writeup](https://github.com/onealmond/hacking-lab/blob/master/picoctf-2020/web-gauntlet/writeup.md)
- [medium.com](https://medium.com/@sobatistacyber/picoctf-writeup-web-gauntlet-7c3b8c7c7946)
- [www.youtube.com](https://www.youtube.com/watch?v=ZQj5tSwaG0k)


## 1. 한 줄 요약
- 여러 라운드의 로그인 필터를 통과해야 합니다.
- SQLite 특유의 문자열 결합(`||`)과 주석 처리(`--`)가 중요합니다.
- 일부 라운드에서는 null byte 같은 우회가 유용합니다.
- 최종 목표는 admin 계정으로 로그인하는 것입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 폼이 보임 | SQLi 가능성을 먼저 의심합니다 |
| 2 | 입력 필터가 특정 단어를 차단 | 일반적인 페이로드가 막힙니다 |
| 3 | SQLite 문법을 이용해 우회 | `||`, 주석, 짧은 payload 활용 |
| 4 | 라운드가 진행될수록 필터가 달라짐 | 각 라운드별로 페이로드를 조정해야 함 |
| 5 | admin 조건 충족 | flag 페이지 접근 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 단순 SQLi가 아니라, **필터가 어떻게 동작하는지 역으로 읽는 문제**입니다. 차단된 문자열을 직접 쓰지 않고도 SQLite 문법으로 같은 의미를 만들 수 있음을 보여줍니다.

### 3.2 자주 쓰는 우회 아이디어
```bash
# Round 1 계열의 기본 우회 예시입니다.
# 예상 결과: 필터가 특정 키워드를 막더라도 admin 조건을 우회할 실마리를 찾습니다.
```

```bash
# SQLite 문자열 결합과 주석을 조합합니다.
# 예상 결과: 입력이 admin' -- 또는 유사한 형태로 정리됩니다.
```

## 4. 공격자 관점
- 필터는 대개 문자열 단위로만 검사합니다.
- SQLite의 `||`는 문자열 결합이므로, 차단된 단어를 쪼개서 재조립할 수 있습니다.
- 주석 처리와 널 바이트는 서버 측 파서와 필터의 시차를 노릴 때 유용합니다.

## 5. 방어자 관점
- 문자열 필터보다 **파라미터 바인딩**이 중요합니다.
- SQLite 쿼리를 직접 붙여 쓰면 필터 우회가 매우 쉽게 생깁니다.
- 라운드별 다른 필터를 적용하더라도 근본 해결은 아닙니다.

## 재현 절차

1. 로그인 폼의 요청을 확인합니다.
```bash
# Burp Suite나 curl로 요청 파라미터와 필터 동작을 관찰합니다.
curl -i 'http://example.com/login'   # 예상: 로그인 페이지 HTML 또는 redirect 응답이 출력됩니다.
```
2. SQLite 문자열 결합과 주석을 이용한 우회 문자열을 실험합니다.
```bash
# 문자열을 쪼개고 주석을 붙여 admin 조건을 우회하는 예시입니다.
echo "ad'||'min' --"                # 예상: 필터가 막는 admin 문자열을 분해한 형태가 출력됩니다.
```
3. 라운드별 필터 차이를 비교하며 짧은 payload를 맞춥니다.
```python
# 각 라운드에서 허용되는 문자 집합을 기준으로 payload를 줄입니다.
payload = "ad'||'min"               # 예상: SQLite에서 admin 문자열로 이어집니다.
print(payload)
```

## 6. 같이 보면 좋은 페이지
- [[web-gauntlet-2-final-writeup]]
- [[web-gauntlet-3-final-writeup]]
- [[web-gauntlet-2-3-sqlite-survey]]
- [[picoctf-2020-web-survey]]
- [[sqlite-sqli-filter-bypass-ctf-patterns]]

## 7. 참고 소스
- [hacking-lab — picoctf-2020/web-gauntlet](https://github.com/onealmond/hacking-lab/blob/master/picoctf-2020/web-gauntlet/writeup.md)
- [Sobatista — PicoCTF Writeup Web Gauntlet](https://medium.com/@sobatistacyber/picoctf-writeup-web-gauntlet-7c3b8c7c7946)
- [YouTube — Bypassing SQL Filters (picoCTF Web Gauntlet)](https://www.youtube.com/watch?v=ZQj5tSwaG0k)

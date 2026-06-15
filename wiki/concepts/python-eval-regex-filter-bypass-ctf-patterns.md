---
title: Python eval regex filter bypass — picoCTF 패턴
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [ctf, web, python, eval, regex, injection, rce]
sources: [https://medium.com/@gbahenrijoel/picoctf-2025-web-3v-l-87fdd25094b4, https://medium.com/@mihasha/3v-l-write-up-picoctf-2025-d84e30c039cf, https://medium.com/@debasissadhu712/picoctf-3v-l-writeup-exploiting-python-eval-for-rce-bypassing-regex-ce85f1dc8c1e]
confidence: high
---

# Python eval regex filter bypass — picoCTF 패턴

## Step 1. 한 줄 정의
이 패턴은 **Python `eval()`에 들어가는 사용자 입력이 블랙리스트/정규식 필터로 제한되어 있을 때, `chr()`, `join()`, `__import__()` 같은 동적 구성으로 문자열을 재조립해 필터를 우회하는 문제 유형**입니다.

## Step 2. 비유
- **비유**: 검색창에 금지어를 직접 쓰면 막히지만, 글자를 하나씩 모아 문장을 만든 뒤 제출하면 검문을 통과하는 상황입니다.
- **이미지**: 계산기처럼 보이지만 실제로는 “입력된 문자열을 코드로 실행”하는 문입니다.
- **전문 설명**: `eval()`은 문자열을 Python 코드로 해석합니다. 그래서 문자열 필터가 있어도, 문자열을 실행 직전에 동적으로 만들어 버리면 차단 규칙을 우회할 수 있습니다.

## 핵심 흐름
```text
loan calculator / formula box -> eval() sink 확인 -> blacklist/regex 파악 -> 직접 문자열 입력 차단 확인 -> chr()/join()/__import__()로 재조립 -> /flag.txt 읽기 또는 RCE
```

## 공격자 관점
1. 소스 코드나 페이지 주석에서 필터 규칙을 확인합니다.
2. 직접 `open('/flag.txt')` 같은 페이로드가 막히는지 시험합니다.
3. 막히면 `chr(47)`, `''.join(...)`처럼 문자 단위 조립으로 전환합니다.
4. 파일 경로나 명령 문자열을 런타임에 만들고 `eval()` 결과를 활용합니다.
5. 경우에 따라 `__import__('subprocess')` 같은 동적 import로 RCE까지 이어갑니다.

## 방어자 관점
- `eval()`을 사용자 입력에 쓰지 않습니다.
- 계산이 목적이면 `ast.literal_eval()` 또는 안전한 파서를 사용합니다.
- 블랙리스트보다 allowlist를 적용합니다.
- `__import__`, `getattr`, `chr`, `join` 등 우회에 자주 쓰이는 primitive를 막는 것이 아니라, 애초에 코드 실행 경로를 제거합니다.
- 파일 접근은 허용 목록으로 제한합니다.

## 같이 보면 좋은 페이지
- [[3v-l-final-writeup]]
- [[eval]]
- [[web-ctf-writeup-parser-template]]
- [[command-injection]]
- [[python-eval-regex-filter-bypass-ctf-patterns]]를 참고한 후, `eval`이 아닌 안전한 계산기 설계를 생각해 보시면 좋습니다.

## 참고 소스
- [PICOCTF 2025–Web:3v@l — Gba](https://medium.com/@gbahenrijoel/picoctf-2025-web-3v-l-87fdd25094b4)
- [3v@l Write-up PicoCTF 2025 — mihasha](https://medium.com/@mihasha/3v-l-write-up-picoctf-2025-d84e30c039cf)
- [picoCTF 3v@l Writeup: Exploiting Python eval() for RCE — Debashish Sadhu](https://medium.com/@debasissadhu712/picoctf-3v-l-writeup-exploiting-python-eval-for-rce-bypassing-regex-ce85f1dc8c1e)

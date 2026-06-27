---
title: SSTI writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, ssti, template-injection, rce]
sources: [https://medium.com/@ahmednarmer1/ctf-day-12-df893a7035fe, https://medium.com/@mihasha/ssti2-write-up-picoctf-2025-5fc53e2320ba]
confidence: high
---

# SSTI writeup survey

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-12-df893a7035fe)
- [medium.com](https://medium.com/@mihasha/ssti2-write-up-picoctf-2025-5fc53e2320ba)


## 1. 목적
Jinja2 기반 SSTI writeup을 비교해, 기본 문법 증명 → 필터 우회 → RCE로 이어지는 계층을 정리합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| SSTI1 | Jinja2 basic injection | file read | `{{...}}`로 템플릿 문법이 실행되는지 확인하고 서버 파일을 읽습니다. |
| SSTI2 | Jinja2 filter bypass | sandbox escape | `attr()`·hex escape·`__getitem__`으로 필터를 우회해 명령을 실행합니다. |

## 3. 공통 관찰
1. SSTI는 `{{`나 `${`가 문자열 평가로 이어지는 순간 시작됩니다.
2. Jinja2는 `.`, `[]`, `|`, `attr()`을 모두 바꿔 쓸 수 있어 필터 우회가 까다롭습니다.
3. sandbox escape 경로는 `__class__.__mro__.__subclasses__()` 체인이 전형적입니다.

## 4. 관련 개념
- [[ssti]]
- [[ssti-core]]
- [[ssti-ctf-patterns]]
- [[web-ctf-writeup-family-hub]]
- [[ssti1-final-writeup]]
- [[ssti2-final-writeup]]

## 5. 다음 읽을 거리
- [[ssti1-final-writeup]]
- [[ssti2-final-writeup]]

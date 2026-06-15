---
title: Web CTF Writeup — 파서/템플릿/검증기 우회
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, research, writeup, parser, template, injection]
sources: [https://blog.hokyun.dev/posts/google-ctf-2024-quals-writeup/, https://github.com/ernw/ctf-writeups/blob/master/csaw2016/mfw/README.md, raw/articles/20260613_web-ctf-writeup-curated.md]
confidence: high
---

# Web CTF Writeup — 파서/템플릿/검증기 우회

> 입력값이 같은 문자열처럼 보여도, 서로 다른 파서에서 다르게 해석되는 지점을 모아둔 분류입니다.

## 1. 핵심 요약
- 이 분류는 **검증 로직과 실행 로직의 불일치**를 노립니다.
- 템플릿 엔진, Bash 파서, `assert()` 문자열, multipart 처리 차이 등이 핵심입니다.
- `ssti`, `command-injection`, `path-traversal`과 자주 이어집니다.

연결 개념: [[ssti]], [[jinja2-template-engine]], [[jinja2-filter-bypass]], [[command-injection]], [[path-traversal]], [[web-inspector-ctf-patterns]], [[xxe]], [[xpath-injection-ctf-patterns]]

## 2. 대표 writeup

| 문제 | 출처 | 핵심 아이디어 |
|------|------|---------------|
| `onlyecho` | Google CTF 2024 Quals | bash parser differential로 `echo` 제한 우회 |
| `grand prix heaven` | Google CTF 2024 Quals | multipart 처리와 template injection 결합 |
| `mfw` | CSAW CTF 2016 | `assert("strpos('$file', '..') === false")` 문자열 인젝션 |
| `SSTI2` | picoCTF 2025 | `attr()` + hex escape 기반 Jinja2 필터 우회 |
| `SSTI1` | picoCTF 2025 | Jinja2 SSTI 산술 평가 후 내부 객체 접근으로 flag 파일 읽기 |
| `X marks the spot` | picoCTF 2021 | blind XPath injection으로 로그인 우회 |
| `sappy` | Google CTF 2024 Quals | URL validation 및 parser 차이 |
| `SOAP` | picoCTF 2023 | XML/SOAP 기반 요청에 XXE 삽입 |

## 3. 자주 보이는 패턴
1. 검증은 정규식, 실행은 별도 파서가 담당함
2. `assert`, `eval`, 템플릿 렌더링이 문자열 기반임
3. multipart boundary나 header folding이 파서별로 다름
4. quoting/escaping이 한 단계만 적용됨
5. 불완전한 allowlist가 우회 가능함

## 4. 읽을 때 확인할 것
- 입력이 몇 번 파싱되는지
- 정규화 전에 검증하는지, 후에 검증하는지
- 문자열 조합 뒤에 다시 실행되는 함수가 있는지
- 다른 라이브러리/언어 런타임이 같은 입력을 다르게 읽는지

## 5. 방어 관점
- 검증과 실행 사이의 표현 형식을 고정합니다.
- 문자열 조합 후 실행하는 API를 피합니다.
- 하나의 파서가 아닌 여러 계층에서 동일 규칙을 적용합니다.
- 템플릿/쉘/SQL/헤더 주입 가능 지점을 별도로 리뷰합니다.

## 6. 추천 다음 읽기
- [[ssti]]
- [[command-injection]]
- [[path-traversal]]
- [[web-ctf-master-checklist]]

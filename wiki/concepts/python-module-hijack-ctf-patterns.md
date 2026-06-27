---
title: Python module hijack — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
sources: [queries/hijacking-final-writeup.md]
confidence: medium
tags: [ctf, pwn, python, module-hijack, import-abuse]
---

# Python module hijack — CTF patterns

> Python의 import 검색 경로를 악용해 악성 모듈을 먼저 로드시키는 패턴입니다.

## 참고 URL
- [Reference](queries/hijacking-final-writeup.md)

## 핵심 아이디어
- Python은 import 시 검색 순서를 따릅니다.
- 같은 이름의 모듈이 더 앞에 있으면 그 파일이 먼저 사용됩니다.
- 실행 환경이 공격자 제어 경로를 포함하면 코드 실행을 탈취할 수 있습니다.

## 자주 보이는 형태
- 현재 디렉터리의 `os.py`, `random.py` 같은 이름 충돌
- `PYTHONPATH` 오염
- import side effect를 이용한 코드 실행
- subprocess와 결합된 경로 우회

## picoCTF 예시
- [[hijacking-final-writeup]]

## 방어
- 절대경로 import 또는 신뢰된 패키지만 사용합니다.
- 배포 시 current directory를 import path에 포함하지 않습니다.
- 실행 전 경로를 정규화하고 제한합니다.

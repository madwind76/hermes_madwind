---
title: Tap into Hash — picoCTF 2025 reverse engineering writeup
created: 2026-06-16
updated: 2026-06-16
type: query
tags: [ctf, reverse-engineering, decode, encoding, encryption, picoctf]
sources: [https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Tap%20into%20Hash/Tap%20into%20Hash.md, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: medium
---

# Tap into Hash — picoCTF 2025 reverse engineering writeup

> 이 문제는 source file과 encrypted payload를 함께 보고, XOR/변환 루틴을 거꾸로 적용해 평문을 되살리는 문제입니다.

## 1. 핵심 요약
- `block_chain.py`가 주어진 입력을 여러 단계로 변형합니다.
- 최종 출력은 단순한 한 줄 XOR처럼 보이지만, 중간 구조를 먼저 복원해야 합니다.
- 디코딩 결과를 이어붙이면 flag를 얻을 수 있습니다.

연결 개념: [[reverse-engineering-ctf-patterns]], [[picoctf-2025-rec-survey]]

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 분류 | reverse engineering / decode |
| 핵심 요소 | source analysis, XOR, encrypted data |
| 목표 | 변환 루틴을 역추적해 plaintext 복원 |

## 3. 공격 흐름
1. `block_chain.py`의 데이터 변환 순서를 살핍니다.
2. 출력 길이와 XOR 단위를 맞춰봅니다.
3. 중간 변환을 먼저 재현한 뒤 최종 디코더를 작성합니다.
4. 복원된 바이트열에서 flag를 확인합니다.

## 4. 재현 절차
1. 소스 코드를 읽고 변환 순서를 확인합니다.
2. 암호문 블록을 분리한 뒤 역연산을 적용합니다.
3. 복호화 스크립트로 출력값을 확인합니다.

```bash
# 암호문을 복호화하는 스크립트를 실행합니다.
python3 block_chain_dec.py enc_flag

# 예상 결과: 복원된 바이트열과 flag 후보가 출력됩니다.
```

## 5. 같이 보면 좋은 페이지
- [[reverse-engineering-ctf-patterns]]
- [[quantum-scrambler-final-writeup]]
- [[picoctf-2025-rec-survey]]

## 6. 참고 소스
- [Tap into Hash — snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Reverse%20Engineering/Tap%20into%20Hash/Tap%20into%20Hash.md)

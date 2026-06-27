---
title: Quantum Scrambler — picoCTF 2025 reverse engineering writeup
created: 2026-06-16
updated: 2026-06-21
type: query
tags: [ctf, reverse-engineering, decode, encoding, encryption, picoctf]
sources: [https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Quantum%20Scrambler/Quantum%20Scrambler.md, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: high
---

# Quantum Scrambler — picoCTF 2025 reverse engineering writeup

> 이 문제는 중첩 리스트를 만드는 scramble 함수를 거꾸로 추적해서 flag를 복원하는 reverse engineering 문제입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Quantum%20Scrambler/Quantum%20Scrambler.md)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)


## 1. 핵심 요약
- 입력을 중첩 리스트 구조로 바꾸는 `scramble()`가 핵심입니다.
- 실제로는 리스트를 평탄화하고 재배열하는 규칙을 역으로 적용하면 됩니다.
- 출력 구조를 풀어보면 flag가 재조립됩니다.

연결 개념: [[reverse-engineering-ctf-patterns]], [[picoctf-2025-rec-survey]]

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 분류 | reverse engineering / decode |
| 핵심 요소 | nested list, transformation reversal |
| 목표 | scramble 로직을 역으로 적용해 평문 복원 |

## 3. 공격 흐름
1. `quantum_scrambler.py`의 `scramble(L)`를 읽습니다.
2. 리스트 append/pop 순서를 추적합니다.
3. 바뀐 구조를 역순으로 복원합니다.
4. 재조립된 문자열에서 flag를 확인합니다.

## 4. 재현 절차
1. 소스 코드의 변환 순서를 관찰합니다.
2. `pop`과 `append`가 만드는 구조 변화를 손으로 추적합니다.
3. 역변환 스크립트를 작성해 결과를 재생성합니다.

```bash
# 변환 규칙을 재현하는 스크립트를 실행합니다.
python3 decode_scramble.py

# 예상 결과: 원문 flag 문자열이 출력됩니다.
```

## 5. 같이 보면 좋은 페이지
- [[reverse-engineering-ctf-patterns]]
- [[wasm-reverse-engineering-ctf-patterns]]
- [[picoctf-2025-rec-survey]]

## 6. 참고 소스
- [Quantum Scrambler — snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Reverse%20Engineering/Quantum%20Scrambler/Quantum%20Scrambler.md)

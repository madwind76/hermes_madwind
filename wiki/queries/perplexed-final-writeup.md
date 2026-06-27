---
title: perplexed — picoCTF 2025 reverse engineering writeup
created: 2026-06-16
updated: 2026-06-21
type: query
tags: [ctf, reverse-engineering, brute-force, automation, picoctf]
sources: [https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/perplexed/perplexed.md, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: high
---

# perplexed — picoCTF 2025 reverse engineering writeup

> 이 문제는 Ghidra로 검증 조건을 읽고, 제한된 입력 길이를 바탕으로 brute force를 섞어 맞추는 reverse engineering 문제입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/perplexed/perplexed.md)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)


## 1. 핵심 요약
- `main()`은 문자열을 입력받아 `check()`에 넘깁니다.
- `check()`는 길이 조건과 내부 상태를 기반으로 여러 검증 단계를 수행합니다.
- 입력 길이가 고정되어 있으므로 조건을 해석한 뒤 자동화된 탐색이 효과적입니다.

연결 개념: [[reverse-engineering-ctf-patterns]], [[picoctf-2025-rec-survey]]

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 분류 | reverse engineering / brute force |
| 핵심 요소 | Ghidra, string check, state comparison |
| 목표 | 검증식에 맞는 입력을 복원 |

## 3. 공격 흐름
1. Ghidra로 `check()`의 조건 분기를 읽습니다.
2. 길이와 문자 검증 순서를 정리합니다.
3. 필요한 위치만 brute force로 탐색합니다.
4. 올바른 입력을 제출해 flag를 확인합니다.

## 4. 재현 절차
1. 바이너리를 Ghidra에 올리고 `check()`를 확인합니다.
2. 입력 길이와 조건을 메모합니다.
3. 자동화 스크립트로 후보를 돌려봅니다.

```bash
# 정적 분석 후, 좁은 입력 공간을 자동으로 탐색합니다.
python3 solve_perplexed.py

# 예상 결과: 조건을 만족하는 문자열이 출력됩니다.
```

## 5. 같이 보면 좋은 페이지
- [[reverse-engineering-ctf-patterns]]
- [[prng-seed-bruteforce-ctf-patterns]]
- [[picoctf-2025-rec-survey]]

## 6. 참고 소스
- [perplexed — snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Reverse%20Engineering/perplexed/perplexed.md)

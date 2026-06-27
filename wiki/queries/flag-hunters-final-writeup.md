---
title: Flag Hunters — picoCTF 2025 reverse engineering writeup
created: 2026-06-16
updated: 2026-06-21
type: query
tags: [ctf, reverse-engineering, source-analysis, automation, parser, picoctf]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/Reverse%20Engineering/Flag-Hunters.md, https://github.com/noamgariani11/picoCTF-2025-Writeup, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: high
---

# Flag Hunters — picoCTF 2025 reverse engineering writeup

> 이 문제는 노래 가사처럼 보이는 **Python source code**를 읽고, 세미콜론으로 분리되는 입력이 어떻게 `REFRAIN` / `RETURN` 분기로 흘러가는지 이해하는 reverse engineering 문제입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/Reverse%20Engineering/Flag-Hunters.md)
- [noamgariani11/picoCTF-2025-Writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)


## 1. 핵심 요약
- 소스 코드에 플래그가 들어 있는 `secret_intro`가 존재합니다.
- `reader()`는 현재 라인을 세미콜론(`;`) 기준으로 다시 해석합니다.
- 입력에 `RETURN 0`을 섞어 넣으면 숨은 프롤로그로 되돌아갈 수 있습니다.

연결 개념: [[reverse-engineering-ctf-patterns]], [[picoctf-2025-rec-survey]]

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 분류 | reverse engineering / source analysis |
| 핵심 요소 | Python script, semi-colon parsing, state jump |
| 입력 경로 | netcat |
| 목표 | 숨겨진 refrain / secret intro 출력 |

## 3. 공격 흐름
1. 원본 Python 소스를 내려받습니다.
2. `reader()`의 `split(';')` 동작을 확인합니다.
3. `CROWD:` 입력이 다음 토큰까지 그대로 이어진다는 점을 이용합니다.
4. `;RETURN 0` 형태로 제어 흐름을 되돌립니다.
5. 플래그가 포함된 숨은 intro를 출력합니다.

## 4. 재현 절차
1. 소스 파일을 내려받고 `reader()`의 분기 조건을 확인합니다.
2. 네트워크 연결 후 입력에 `;RETURN 0`을 포함시켜 다음 반복에서 탈출합니다.
3. 숨은 intro가 출력될 때 플래그를 확인합니다.

```bash
# 문제 소스를 받아서 로컬에서 흐름을 읽습니다.
wget https://challenge-files.picoctf.net/c_verbal_sleep/9f2b86c1e1068d492f783b106f4535aeb137b0c0e31e43351f8cb82a39456a84/lyric-reader.py

# 원격 서비스에 접속합니다.
nc verbal-sleep.picoctf.net 56688

# 입력 예시: 다음 반복에서 RETURN 0이 해석되도록 세미콜론을 포함합니다.
```

## 5. 같이 보면 좋은 페이지
- [[reverse-engineering-ctf-patterns]]
- [[prng-seed-bruteforce-ctf-patterns]]
- [[picoctf-2025-rec-survey]]

## 6. 참고 소스
- [Flag Hunters — noamgariani11/picoCTF-2025-Writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Reverse%20Engineering/Flag-Hunters.md)
- [picoCTF 2025 Writeup — noamgariani11](https://github.com/noamgariani11/picoCTF-2025-Writeup)

---
title: Google CTF Family Hub
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, google-ctf, ctf-challenge, writeup]
sources: [https://github.com/google/google-ctf]
confidence: high
---

# Google CTF — Family Hub

9개 연도 + 4개 트랙을 한 페이지에서 인덱싱. 각 survey 페이지는
연도 × 트랙 단위로 작성.

## 연도별 트랙

```
                2017  2018  2019  2020  2021  2022  2023  2024  2025
quals           ✓     ✓     ✓     ✓     ✓     ✓     ✓     ✓     ✓
finals          ✓     ✓     ✓     .     .     .     .     .     .
beginners       .     ✓     ✓     .     .     ✓     .     .     .
hackceler8      .     .     .     ✓     ✓     ✓     ✓     ✓     ✓
```

## 작성 상태

| 연도 | 트랙 | survey 페이지 | 챌린지 leaf |
|------|------|---------------|-------------|
| 2017 | quals | 미작성 | 0 |
| 2017 | finals | 미작성 | 0 |
| 2018~2023 | 모두 | 미작성 | 0 |
| **2024** | **quals** | **[[google-ctf-2024-quals-survey]]** | 1개 (시범: `crypto-blinders`) |
| 2024 | hackceler8 | 미작성 | 0 |
| 2025 | quals | 미작성 | 0 |
| 2025 | hackceler8 | 미작성 | 0 |

## 트랙별 특성

### quals (연례 메인)
- 누구나 참여 가능
- 35~40개 챌린지, 48시간
- 카테고리: crypto / pwn / rev / web / misc

### finals (2017~2019)
- 본선 오프라인 또는 온라인
- Attack-Defense 또는 jeopardy 형식

### beginners (2018~2019, 2022)
- 초보자 트랙, 쉬운 챌린지만
- 별도 점수 집계

### hackceler8 (2020~)
- 게임형 CTF (속도/탐험)
- 8시간짜리 미니 CTF 형식

## 카테고리별 챌린지 카운트 (2024 quals 기준)

| 카테고리 | 메인 | 봇 |
|----------|------|-----|
| crypto   | 6    | 0  |
| pwn      | 5    | 0  |
| reversing| 7    | 0  |
| web      | 5    | 5  |
| misc     | 7    | 0  |
| **합계** | **30**| **5** |

> 봇 챌린지는 web 메인 챌린지의 자동화 solver를 별도 트랙으로 분리한 것.

## 다음 작업 후보

| 우선순위 | 작업 |
|----------|------|
| 🟡 | 2024 quals leaf 작성 (나머지 29개 메인 챌린지) |
| 🟡 | 2023, 2025 quals survey 추가 |
| 🟢 | 2017~2022 quals survey 추가 (Contents API 한 번에 메타 추출) |
| 🟢 | hackceler8 챌린지 별도 survey (게임형이라 패턴 다름) |
| 🟢 | `nicolaisoeborg.github.io/ctf-writeups/2025/Google CTF 2025/` 등 외부 writeup 정리 |

## 참고 URL

- 공식 repo: <https://github.com/google/google-ctf>
- Contents API: <https://api.github.com/repos/google/google-ctf/contents/>
- raw metadata 예시: <https://raw.githubusercontent.com/google/google-ctf/main/2024/quals/crypto-otp/metadata.yaml>

## 관련 페이지

- [[google-ctf-topic-map]]
- [[google-ctf-quick-summary]]
- [[google-ctf-2024-quals-survey]]
- [[google-ctf-2024-crypto-blinders]]

---
title: Google CTF Quick Summary
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, google-ctf]
sources: [https://github.com/google/google-ctf]
confidence: high
---

# Google CTF — Quick Summary

한 페이지 요약. 자세한 분류는 [[google-ctf-topic-map]] 참조.

## 한 줄 요약

Google Security Team이 매년 운영하는 CTF. 2017년부터 진행. 모든 챌린지
코드와 flag가 GitHub (`google/google-ctf`)에 공개되어 있어 학습용으로 우수.

## 왜 중요한가

- **공식 writeup이 코드 형태로 제공됨** — PDF writeup이 아닌 실제
  챌린지 소스코드 + solver
- 9개 연도(2017~2025), 4개 트랙(quals, finals, beginners, hackceler8)
- 카테고리별로 다양한 primitive 패턴 커버 (crypto/pwn/rev/web/misc)
- 메이저 CTF 출제 트렌드 참고용

## 연도별 한 줄 평 (메타 정보만)

| 연도 | 트랙 | 챌린지 수 (qual, 추정) |
|------|------|------|
| 2017 | quals, finals | 미조사 |
| 2018 | + beginners | 미조사 |
| 2019 | + beginners | 미조사 |
| 2020 | + hackceler8 | 미조사 |
| 2021 | + hackceler8 | 미조사 |
| 2022 | + beginners, hackceler8 | 미조사 |
| 2023 | hackceler8, quals | 미조사 |
| **2024** | hackceler8, quals | **35개** (crypto 6, pwn 5, rev 7, web 5(+5 bot), misc 7) |
| 2025 | hackceler8, quals | 미조사 |

## 학습 추천 경로

1. **[[google-ctf-2024-quals-survey]]** — 가장 최근 본문 분석
2. 카테고리별 leaf 페이지 — 예: `crypto-blinders`, `pwn-knife`
3. 외부 writeup 보강 — `nicolaisoeborg.github.io/ctf-writeups/2025/Google CTF 2025/`

## 관련 페이지

- [[google-ctf-topic-map]]
- [[google-ctf-family-hub]]
- [[google-ctf-2024-quals-survey]]

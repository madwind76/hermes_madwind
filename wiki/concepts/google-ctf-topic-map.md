---
title: Google CTF Topic Map
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, google-ctf, ctf-challenge, writeup]
sources: [https://github.com/google/google-ctf]
confidence: high
---

# Google CTF — Topic Map

Google이 2017년부터 매년 운영하는 메이저 CTF 대회. 공식 GitHub 저장소
[`google/google-ctf`](https://github.com/google/google-ctf) 에 모든 연도
챌린지 코드·인프라가 공개되어 있다.

## 대회 운영 방식

| 항목 | 내용 |
|------|------|
| 운영 | Google Security Team |
| 시작 | 2017 |
| 형식 | Qualifiers (온라인) + Finals (온라인) + Hackceler8 (게임형) + Beginners (초보 트랙, 일부 연도) |
| 챌린지 공개 | 모든 대회 종료 후 GitHub repo에 코드 + flag + metadata 공개 |
| 카테고리 | crypto, pwn, reversing(rev), web, misc (+ 가끔 hw, net) |

## 연도별 디렉터리 구조 (Contents API 기준)

| 연도 | 하위 디렉터리 | 비고 |
|------|--------------|------|
| 2017 | finals, quals | 첫 대회, finals + quals만 |
| 2018 | beginners, finals, quals | beginners 트랙 시작 |
| 2019 | beginners, finals, quals |  |
| 2020 | hackceler8, quals | hackceler8 시작 |
| 2021 | hackceler8, quals |  |
| 2022 | beginners, hackceler8, quals |  |
| 2023 | hackceler8, quals |  |
| 2024 | hackceler8, quals | 가장 최근 본문 분석 대상 |
| 2025 | hackceler8, quals | 최신 |

## 챌린지 메타데이터 형식

각 챌린지 폴더에는 `metadata.yaml`이 있고 다음 필드가 있음 (2024 샘플):

```yaml
name: OTP                              # 사람이 읽는 이름
description: |+                        # 챌린지 설명 (multiline)
  I encrypted all my pictures using...
flag: CTF{I_THOUGHT_OTP_WAS_SECURE}    # flag 문자열 (공식)
category: crypto                       # crypto / pwn / rev / web / misc / hw / net
link: https://sappy-web.2024.ctf...    # web 챌린지인 경우 URL
```

## 이 위키에서의 정리 구조

```
google-ctf-topic-map (현재 페이지)
   │
   ├─ google-ctf-quick-summary        # 한 페이지 요약
   │
   ├─ google-ctf-family-hub           # 9개 연도 + 4개 트랙 통합 허브
   │     │
   │     ├─ google-ctf-2024-quals-survey
   │     │     ├─ google-ctf-2024-crypto-{blinders,desfunctional,...}
   │     │     ├─ google-ctf-2024-pwn-{knife,heat,...}
   │     │     ├─ google-ctf-2024-rev-{rustyschool,...}
   │     │     ├─ google-ctf-2024-web-{sappy,...}
   │     │     └─ google-ctf-2024-misc-{onlyecho,...}
   │     │
   │     ├─ google-ctf-2025-quals-survey
   │     └─ ... (2017~2023 survey)
   │
   └─ google-ctf-writeup-resources    # 외부 writeup 모음 (CTFtime, 블로그)
```

## 참고 URL

- 공식 repo: <https://github.com/google/google-ctf>
- README: <https://github.com/google/google-ctf/blob/main/README.md>
- 공지 시작: <https://security.googleblog.com/2017/06/announcing-google-capture-flag-2017.html>
- 2024 quals: <https://github.com/google/google-ctf/tree/main/2024/quals>

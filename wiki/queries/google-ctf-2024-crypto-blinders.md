---
title: Google CTF 2024 — crypto-blinders (Blinders) Writeup
created: 2026-06-26
updated: 2026-06-26
type: query
tags: [ctf, google-ctf, ctf-challenge, writeup, crypto]
sources: [https://github.com/google/google-ctf/tree/main/2024/quals/crypto-blinders]
confidence: medium
---

# Google CTF 2024 — crypto-blinders (Blinders)

> ⚠️ **시범 leaf 페이지**. 이 패턴으로 나머지 34개 챌린지를 확장 가능.

## 챌린지 정보 (공식 metadata)

| 필드 | 값 |
|------|----|
| 카테고리 | crypto |
| 이름 | Blinders |
| 슬러그 | `crypto-blinders` |
| flag | `CTF{pr1v4t3_s3t_m3mb3rsh1p_qu3r135_m3d4_m0r3_p0w3rfu1}` |
| 형식 | 오프라인 (attachments만 다운로드) |
| 설명 | If you are really efficient at guessing which number is missing from {0, 1, ..., 255}, I am more than happy to share you… |

## 문제 힌트 (description 전문)

> "If you are really efficient at guessing which number is missing from
> {0, 1, ..., 255}, I am more than happy to share you…"

`{0, 1, ..., 255}` = 256개 원소 집합. "어느 한 숫자가 빠진" 상태 = **private
set membership** 문제. 서버가 255개의 원소만 보여주고, 1개의 missing을
여러 번 query로 추측해야 함.

## 추정 primitive

- **Private Set Membership (PSM)**
  - 서버가 가진 비밀 집합 S (255개 원소, missing 1개)
  - 클라이언트가 임의 원소 x를 query → x ∈ S ? 1 bit 응답
  - 단, missing 원소를 알아내야 함
- 관련 primitive: `oblivious transfer`, `keyword PIR`, `Diffie-Hellman 가정 기반 PSM`
- 가능성 있는 flag 함의: `private set membership queries`

## 풀이 전략 (참고)

1. attachments 디렉터리에서 `chal.py` / `solve.py` / `server.py` 분석
2. PSM 프로토콜 분석 — membership oracle이 leak하는 정보량 계산
3. 256개 중 missing 1개 → log2(256) = **8 bit = 256 query**로 식별 가능
4. 각 query는 1 bit만 누설 → 평균 128 query로 충분 (이진 탐색)

## 다음 단계

- [ ] 공식 `challenge/` 디렉터리 코드 분석
- [ ] `solve.py` 실행 흐름 분석
- [ ] 외부 writeup (예: `nicolaisoeborg.github.io/ctf-writeups/2024/Google CTF 2024/`) 보강

## 참고 URL

- 공식 폴더: <https://github.com/google/google-ctf/tree/main/2024/quals/crypto-blinders>
- raw metadata: <https://raw.githubusercontent.com/google/google-ctf/main/2024/quals/crypto-blinders/metadata.yaml>
- 2024 quals survey: [[google-ctf-2024-quals-survey]]

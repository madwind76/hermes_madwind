---
title: Baby MD5 — ASIS CTF Finals 2020 writeup
created: 2026-06-20
updated: 2026-06-21
type: query
tags: [ctf, crypto, md5, hash-collision, brute-force, timing]
sources: [https://ctftime.org/writeup/25360, https://github.com/TalaatHarb/ctf-writeups/tree/main/asisctf2020/babymd5]
confidence: high
---

# Baby MD5 — ASIS CTF Finals 2020 writeup

> `Baby MD5`는 **부분 해시 충돌과 반복 해시 조건**을 섞어, MD5의 충돌 취약성을 단계적으로 보여주는 문제입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/25360)
- [Original writeup](https://github.com/TalaatHarb/ctf-writeups/tree/main/asisctf2020/babymd5)


## 1. 한 줄 요약
- PoW 구간은 특정 해시 끝자리를 맞추는 brute force입니다.
- 본문 구간은 반복 MD5 적용 후 동일 해시를 만드는 조건입니다.
- `dead` 같은 hex prefix를 활용해 반복 상태를 맞춥니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | PoW에서 hash suffix 맞추기 | 제한된 공간 brute force |
| 2 | 반복 MD5 조건 확인 | 단순 1회 해시가 아님 |
| 3 | 특정 prefix 문자열 사용 | 중간 상태를 유도 |
| 4 | 두 입력을 같은 최종 hash로 수렴 | collision 조건 만족 |
| 5 | flag 획득 | 문제 해결 |

## 3. 핵심 분석
이 문제는 해시 충돌의 현실성과, **반복 해시 구조가 공격자에게 예측 가능한 상태를 제공할 수 있다**는 점을 보여줍니다.

### 3.1 실전 메모
```python
# 부분 문자열 suffix brute force는 공간이 작으면 실제로 가능합니다.
# 반복 MD5 조건은 중간 결과를 다음 입력으로 재사용해 맞춥니다.
# 예상 결과: 동일한 최종 해시를 가진 두 입력이 나옵니다.
```

## 4. 공격자 관점
1. PoW에서 해시 일부를 맞추는 방식이 가능한지 확인합니다.
2. 반복 MD5 횟수와 prefix 제약을 정리합니다.
3. 중간 해시를 다음 입력으로 활용하는 구조를 만듭니다.
4. 해시 끝 상태가 같아지는 두 입력을 찾습니다.
5. 서버가 입력 검증을 해시 collision에 의존하는지 확인합니다.

## 5. 방어자 관점
- 부분 해시 비교는 위험합니다.
- 반복 해시는 설계에 따라 상태 재사용 공격을 허용할 수 있습니다.
- 민감 조건은 해시 문자열이 아니라 서버 측 검증/서명을 사용해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[crypto-writeup-family-hub]]
- [[md5-collision-upload-integrity-bypass-ctf-patterns]]
- [[it-is-my-birthday-final-writeup]]

## 7. 참고 소스
- [CTFtime — Baby MD5 writeup](https://ctftime.org/writeup/25360)
- [Original writeup referenced in CTFtime](https://github.com/TalaatHarb/ctf-writeups/tree/main/asisctf2020/babymd5)

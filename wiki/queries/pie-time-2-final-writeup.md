---
title: PIE TIME 2 — picoCTF 2025 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, format-string, pie, aslr, stack-leak, picoctf]
sources: [https://systemweakness.com/pie-time-2-picoctf-2025-ca481b91d209, https://hackmd.io/@sal/HJtUdR5n1e, https://medium.com/@anandrishav2228/picoctf-pie-time-2-walkthrough-af7d513c8484]
confidence: high
---

# PIE TIME 2 — picoCTF 2025 pwn writeup

> `PIE TIME 2`는 **`printf(buffer)` 형식 문자열 취약점을 이용해 코드/스택 주소를 누출한 뒤, PIE 베이스를 계산해서 `win()`으로 점프하는 picoCTF 2025 pwn 문제**입니다. 핵심은 **format string leak + PIE offset 계산**입니다.

## 1. 핵심 요약

- PIE TIME과 달리 `main()` 주소를 직접 보여주지 않습니다.
- 대신 `printf(buffer)`가 있어 **format string vulnerability**가 존재합니다.
- `%p` 같은 서식 지정자를 이용해 스택에서 코드 주소를 읽습니다.
- 누출한 주소와 `win()`의 오프셋을 계산해 최종 점프 주소를 만듭니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / format string / PIE-ASLR |
| 핵심 요소 | `printf(buffer)`, address leak, PIE base computation |
| 목표 | `win()`으로 제어 흐름 이동 |
| 난이도 | 중급 |

## 3. 취약점 위치

```c
void call_functions() {
  char buffer[64];
  printf("Enter your name:");
  fgets(buffer, 64, stdin);
  printf(buffer);  // format string vulnerability

  unsigned long val;
  printf(" enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);

  void (*foo)(void) = (void (*)())val;
  foo();
}
```

## 4. 공격 흐름

1. 입력란에 `%p` 계열 payload를 넣어 스택 값을 누출합니다.
2. 누출된 주소가 `main()` 또는 그 근처임을 확인합니다.
3. 로컬/정적 분석으로 구한 `main()`↔`win()` 오프셋을 적용합니다.
4. 계산된 `win()` 주소를 다음 프롬프트에 넣습니다.
5. 프로그램이 `win()`을 호출하면서 플래그를 출력합니다.

## 5. 대표 누출 패턴

```text
%19$p
%23$p
```

- 실제 위치는 빌드마다 다를 수 있습니다.
- 한 번 주소를 찾으면 PIE 베이스를 역산할 수 있습니다.

## 6. 왜 가능한가

PIE는 코드의 **절대 주소**만 바꾸고, 함수 간 **상대 오프셋**은 유지합니다. 따라서 코드 주소 하나만 새면, 나머지 함수 주소를 계산할 수 있습니다.

## 7. 방어 관점 메모

- `printf(user_input)`을 쓰지 않습니다.
- 형식 문자열은 반드시 고정 문자열로 사용합니다.
- PIE만으로는 충분하지 않으며, 입력 검증이 필수입니다.

## 8. `PIE TIME`과의 차이

- `PIE TIME`: `main()` 주소를 직접 보여줌
- `PIE TIME 2`: 직접 누출이 없고, **format string으로 주소를 먼저 새야 함**

## 9. 참고 자료

- [PIE TIME 2 — System Weakness](https://systemweakness.com/pie-time-2-picoctf-2025-ca481b91d209)
- [PicoCTF 2025 - Binary Exploitation Challenges Writeup - HackMD](https://hackmd.io/@sal/HJtUdR5n1e)
- [PicoCTF: PIE TIME 2 Walkthrough - Medium](https://medium.com/@anandrishav2228/picoctf-pie-time-2-walkthrough-af7d513c8484)
- [[format-string-ctf-patterns]]
- [[pie-aslr-function-offset-ctf-patterns]]

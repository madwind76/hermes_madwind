---
title: Horsetrack — picoCTF 2023 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, heap, tcache-poisoning, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, participant profile, Horsetrack writeups]
---

# Horsetrack — picoCTF 2023 pwn writeup

> `Horsetrack`은 **heap exploitation 문제**로, 외부 writeup들에서는 **tcache poisoning 계열**로 설명됩니다.

## 참고 URL
- [snwau/picoCTF-2023-Writeup](snwau/picoCTF-2023-Writeup)
- [participant profile](participant profile)
- [Horsetrack writeups](Horsetrack writeups)


## 요약
- 분류: pwn
- 핵심 primitive: heap exploitation / tcache poisoning
- 난이도 감각: 중상급
- 연결 개념: [[heap-tcache-poisoning-ctf-patterns]]

## 취약점 원인
말/오브젝트를 추가하고 삭제하는 과정에서 freed chunk가 다시 재사용되는 흐름을 노출하면, 공격자는 tcache freelist의 next 포인터를 오염시켜 원하는 주소를 반환받을 수 있습니다. 이 유형은 **UAF 또는 double-free 계열 힌트**가 있는지 먼저 보는 것이 중요합니다.

## 공격 흐름
1. horse 추가/삭제 시 힙 재할당 패턴을 확인합니다.
2. freed chunk의 재사용 타이밍을 관찰합니다.
3. tcache entry 또는 관련 함수 포인터를 원하는 값으로 바꿉니다.
4. 임의 주소 할당 또는 제어 흐름 탈취로 이어갑니다.

## 실전 포인트
- `tcache`는 같은 크기 chunk를 빠르게 재할당하므로 오염 효과가 안정적입니다.
- 힙 leak이 있으면 libc base 계산이 쉬워질 수 있습니다.
- 하나의 포인터만 바꿔도 함수 호출 경로를 바꿀 수 있는지 확인해야 합니다.

## 방어 관점
- UAF와 double-free를 막아야 합니다.
- 해제 후 포인터 무효화와 힙 무결성 검사가 필요합니다.
- 가능한 경우 safe-linking과 최신 glibc 보호를 유지합니다.

## 재현 절차
1. 추가/삭제 동작에서 freed chunk 재사용 흐름을 확인합니다.
2. tcache freelist 오염 가능 지점을 찾습니다.
3. 재할당 주소가 조작되는지 검증합니다.

```bash
# 힙 동작을 보기 위해 디버거로 실행합니다.
gdb -q ./horsetrack

# 필요하면 pwntools 스크립트로 반복 입력을 자동화합니다.
python3 solve.py
```

## 참고
- [snwau progress writeup](https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Binary%20Exploitation/Horsetrack/Horsetrack.md)
- [Horsetrack tcache poisoning writeup](https://medium.com/@arcvjs/horsetrack-picogym-writeup-tcache-poisoning-glibc-2-33-1e44c1624a4b)

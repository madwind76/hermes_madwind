---
title: reversing-xor — ForeverCTF crypto writeup
created: 2026-06-20
updated: 2026-06-21
type: query
tags: [ctf, crypto, xor, reverse-engineering, decode, encoding]
sources: [https://github.com/utisss/foreverctf-writeups/blob/master/reversing-xor.md]
confidence: medium
---

# reversing-xor — ForeverCTF crypto writeup

> `reversing-xor`는 **바이너리 안의 고정 XOR 키를 찾아 평문을 복원하는** 아주 전형적인 crypto/reversing 경계형 문제입니다.

## 참고 URL
- [Original writeup](https://github.com/utisss/foreverctf-writeups/blob/master/reversing-xor.md)


## 1. 한 줄 요약
- `xor eax, 0x41` 같은 고정 키가 루프에서 반복됩니다.
- 암호화된 바이너리를 통째로 XOR 해도 문자열이 복원됩니다.
- 핵심은 키 추출과 일괄 복호화입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | `gdb`로 main 확인 | 정적/동적 분석 시작 |
| 2 | 반복되는 XOR 명령 발견 | 고정 키 암호화 |
| 3 | 키가 `0x41`임을 확인 | 복호화 가능 |
| 4 | 전체 파일 XOR | 문자열 복원 |
| 5 | `strings`로 flag 확인 | 문제 해결 |

## 3. 핵심 분석
이 문제는 암호학적 복호화라기보다, **XOR 키가 고정되어 있는 아주 약한 변조**입니다. 고정 키 XOR는 복호화가 사실상 같은 연산이므로, 키만 찾으면 내용이 드러납니다.

### 3.1 실전 메모
```python
# 고정 XOR 키가 보이면, 같은 키로 전체 바이트를 다시 XOR합니다.
# 예상 결과: 바이너리 내부 문자열이 평문으로 복원됩니다.
```

## 4. 공격자 관점
1. 바이너리에서 XOR 연산과 반복 루프를 찾습니다.
2. 상수 키를 추출합니다.
3. 파일 전체를 같은 키로 XOR합니다.
4. `strings` 또는 유사 도구로 플래그를 찾습니다.

## 5. 방어자 관점
- 고정 키 XOR는 보안이 아닙니다.
- 바이너리에 평문 문자열이나 고정 키를 직접 두지 않습니다.
- 실제 보호가 필요하면 인증된 암호화를 사용해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[crypto-writeup-family-hub]]
- [[reverse-engineering-ctf-patterns]]
- [[cia]]

## 7. 참고 소스
- [foreverctf-writeups — reversing-xor](https://github.com/utisss/foreverctf-writeups/blob/master/reversing-xor.md)

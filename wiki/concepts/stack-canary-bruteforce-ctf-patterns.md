---
title: Stack canary brute force — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, pwn, stack-canary, brute-force, buffer-overflow, oracle, ret2win]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-3, https://qiita.com/housu_jp/items/f6b9e0dedf555f7288ce, https://cryptocat.me/blog/ctf/2022/pico/pwn/buffer_overflow_3/]
confidence: high
---

# Stack canary brute force — CTF patterns

## 참고 URL
- [picoctf2022.haydenhousen.com](https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-3)
- [qiita.com](https://qiita.com/housu_jp/items/f6b9e0dedf555f7288ce)
- [cryptocat.me](https://cryptocat.me/blog/ctf/2022/pico/pwn/buffer_overflow_3/)

## Step 1. 단어 풀이
- **Stack canary**: 리턴 주소 앞에 두는 보호값입니다.
- **Brute force**: 가능한 값을 하나씩 시험해 정답을 찾는 방법입니다.
- **Oracle**: 성공/실패를 알려주는 반응 채널입니다.

## 한 문장 정의
이 패턴은 **카나리 값이 직접 노출되지 않지만, 크래시 여부나 에러 메시지로 정답/오답을 구분할 수 있을 때 한 바이트씩 복원하는 문제 유형**입니다.

## 핵심 흐름
```text
input size control -> partial overwrite -> crash oracle -> byte recovery -> ret2win
```

## 전문 설명
이 유형은 다음 조건에서 자주 등장합니다.

1. 입력 길이를 조절할 수 있습니다.
2. 카나리가 고정되어 있습니다.
3. 카나리 검증 실패 시 프로그램 반응이 명확합니다.
4. 각 바이트를 독립적으로 시험해도 인스턴스가 유지됩니다.

## 공격자 관점
- 카나리 첫 바이트가 `\x00`인 경우가 많아, 이후 바이트만 맞춰도 됩니다.
- 실패 메시지나 종료 코드로 성공 여부를 판단합니다.
- 완성된 카나리 뒤에 saved EBP와 return address를 이어 붙입니다.

## 방어자 관점
- 실패 여부가 공격자에게 너무 명확하게 드러나면 안 됩니다.
- 에러 메시지와 타이밍 차이를 줄입니다.
- 카나리를 brute force하기 어려운 실행 모델을 고려합니다.

## 관련 writeup
- [[buffer-overflow-3-final-writeup]]

## 같이 보면 좋은 개념
- [[stack-leak-ret2win-ctf-patterns]]
- [[ret2win-64bit-stack-alignment-ctf-patterns]]
- [[function-pointer-overwrite-ctf-patterns]]

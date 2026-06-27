---
title: Race Condition — 보안 용어 해설과 Web CTF 패턴
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [security, glossary, web, ctf, race-condition, concurrency, timing]
sources: [https://medium.com/@ahmednarmer1/ctf-day-24-0e1e8a56b6f6, https://www.ztz0.com/writeups/2025/picoctf/web/pachinko/, https://owasp.org/www-community/attacks/Race_condition]
confidence: medium
---

# Race Condition — 보안 용어 해설과 Web CTF 패턴

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-24-0e1e8a56b6f6)
- [www.ztz0.com](https://www.ztz0.com/writeups/2025/picoctf/web/pachinko/)
- [owasp.org](https://owasp.org/www-community/attacks/Race_condition)

## Step 1. 단어 직역과 쉬운 비유

### 1) 단어 풀이
- **Race**: 여러 작업이 먼저 끝나려고 경쟁하는 상태입니다.
- **Condition**: 특정 조건이나 상태를 뜻합니다.
- **Race condition**: 여러 요청이나 스레드가 같은 자원에 거의 동시에 접근하면서, **순서에 따라 결과가 달라지는 상태**입니다.

### 2) 한 문장 정의
**Race condition**은 "같은 일을 두 번 하지 못하게 막아야 하는데, 두 요청이 동시에 들어와 둘 다 성공해버리는 문제"입니다.

### 3) 쉬운 비유
은행 잔고를 확인하고 돈을 보내는 과정이 있다고 하겠습니다. 두 사람이 거의 동시에 요청하면, 둘 다 "잔고 충분"이라고 보고 각각 송금해버릴 수 있습니다. 확인과 수정이 한 덩어리로 묶이지 않으면, 순서 싸움에서 이긴 쪽이 아닌 **둘 다 성공하는** 버그가 생깁니다.

## Step 2. 핵심 흐름 시각화

```text
request A -> check state -> wait -> update state
request B -> check state -> wait -> update state
```

검사와 상태 변경 사이에 빈틈이 있으면, 두 요청이 같은 초기 상태를 보고 동시에 통과할 수 있습니다.

## Step 3. 전문 설명

Race condition은 보통 다음 상황에서 발생합니다.

- 동일한 자원을 여러 요청이 공유합니다.
- 검사(check)와 변경(update)이 분리되어 있습니다.
- 잠금(lock)이나 원자성(atomicity)이 보장되지 않습니다.
- 실패/성공 응답이 시간 차이로 노출됩니다.

웹 CTF에서는 다음 형태로 자주 나타납니다.

1. 동시에 여러 요청을 보내야 하는 문제
2. 상태값이 아직 갱신되기 전에 다시 요청해야 하는 문제
3. 응답 길이, 코드, 타이밍 차이로 오라클이 생기는 문제
4. "revisit", "again", "history" 같은 힌트로 반복/순서 문제가 암시되는 경우

### 짧은 코드 예시
```python
# 요청 A와 요청 B가 동시에 들어오면 둘 다 balance를 통과할 수 있습니다.
if balance >= amount:
    send_money(amount)   # 상태 변경 전에 다른 요청이 끼어들 수 있습니다.
    balance -= amount
```

## 공격자 관점

1. 같은 엔드포인트를 짧은 간격으로 반복 호출해봅니다.
2. Burp Suite Intruder, Turbo Intruder, 간단한 병렬 스크립트를 사용합니다.
3. 성공/실패 응답이 달라지는지 확인합니다.
4. 상태 갱신 전에 들어가는 요청 조합을 찾습니다.

## 방어자 관점

1. 상태 변경 로직을 원자적으로 처리합니다.
2. 잠금, 트랜잭션, compare-and-swap 같은 동시성 제어를 사용합니다.
3. 중복 제출 방지 토큰을 둡니다.
4. 성공/실패 응답의 차이를 최소화합니다.
5. 초당 요청 수와 동시 요청 수를 제한합니다.

## Web CTF 패턴

`pachinko`처럼 UI는 단순하지만 실제로는 **동시 요청 타이밍**을 노리는 문제가 여기에 속합니다. 공개 writeup 중 일부는 Burp Intruder로 대량 반복 요청을 보내어 첫 번째 flag를 찾았고, 다른 자료는 race condition 관점으로 설명합니다. 이 차이는 대개 **flag 1 / flag 2**, 또는 **각기 다른 풀이 경로**를 반영한 것으로 볼 수 있습니다.

관련 writeup: [[pachinko-final-writeup]]

## 관련 위키 링크

- [[parameter-tampering-ctf-patterns]] — 값 변조와 비교되는 입력 조작 패턴
- [[burp-request-mutation]] — 요청 변형과 반복 테스트
- [[web-ctf-writeup-auth-session]] — 상태 전이와 요청 순서가 중요한 web CTF 허브
- [[pachinko-final-writeup]] — 이 패턴이 드러난 실전 writeup

## 참고 소스

- [CTF Day(24). picoCTF Web Exploitation: Pachinko](https://medium.com/@ahmednarmer1/ctf-day-24-0e1e8a56b6f6)
- [Pachinko - picoCTF 2025 Writeup | ztz0](https://www.ztz0.com/writeups/2025/picoctf/web/pachinko/)
- [OWASP Race Condition](https://owasp.org/www-community/attacks/Race_condition)

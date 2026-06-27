---
title: Browser history manipulation — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, web, browser-history, client-side, history-api]
sources: [https://ctftime.org/writeup/27367, https://picoctf2021.haydenhousen.com/web-exploitation/ancient-history]
confidence: high
---

# Browser history manipulation — CTF patterns

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/27367)
- [picoctf2021.haydenhousen.com](https://picoctf2021.haydenhousen.com/web-exploitation/ancient-history)

## 1. 정의
**Browser history manipulation**은 브라우저의 `history` 스택, `back/forward` 동작, `pushState/replaceState`를 이용해 이전 상태나 숨겨진 화면을 되찾는 패턴입니다. 서버 취약점이 아니라, 클라이언트 상태 관리가 안전하지 않을 때 발생합니다.

## 2. 왜 중요한가
- 현재 화면에 없던 정보가 이전 상태에 남을 수 있습니다.
- SPA/동적 페이지는 history와 DOM 상태가 분리될 수 있습니다.
- 사용자는 뒤로 가기만 해도 민감한 상태를 다시 볼 수 있습니다.

## 3. 공격 흐름
1. 페이지의 라우팅/상태 전환을 관찰합니다.
2. `history.length`와 `window.history.back()` 동작을 확인합니다.
3. 이전 상태에 민감정보가 남아 있는지 봅니다.
4. 여러 번 되돌아가며 숨은 화면을 찾습니다.

## 4. picoCTF 2021 `Ancient History`에서의 적용
이 문제는 페이지가 여러 상태를 DOM에 쌓아 두고, 브라우저 history를 통해 이전 상태로 돌아가면 flag가 있는 화면을 다시 볼 수 있게 구성되어 있습니다.

## 5. 같이 보면 좋은 페이지
- [[ancient-history-final-writeup]]
- [[web-ctf-writeup-client-side]]
- [[bookmarklet-execution-ctf-patterns]]

## 6. 방어 관점
- 민감정보를 이전 상태에 렌더링하지 않습니다.
- `pushState`로 상태를 쌓더라도 비밀값은 URL/DOM에 남기지 않습니다.
- 뒤로가기 시 복원될 수 있는 화면에 비밀을 두지 않습니다.

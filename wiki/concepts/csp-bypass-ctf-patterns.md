---
title: CSP bypass — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, xss, csp, client-side, browser]
sources: [https://www.justinsteven.com/posts/2024/04/02/picoctf-2024-elements-csp-bypass/, https://blog.jettchen.me/posts/elements/]
confidence: high
---

# CSP bypass — CTF patterns

## 1. 정의
**CSP bypass**는 Content Security Policy가 켜져 있어도, 정책이 허용하는 경로 또는 브라우저의 예외 동작을 이용해 스크립트 실행 결과를 밖으로 빼내는 패턴입니다. `XSS`가 있어도 CSP 때문에 바로 끝나지 않을 때 자주 등장합니다.

## 2. 쉬운 비유
보안 요원이 “문 밖으로 나가는 문은 하나만 사용하세요”라고 막아도, 공격자는 **예외 출입구**나 **우회 통로**를 찾아 빠져나갑니다. CSP bypass는 바로 이런 식으로, 제한된 문을 뚫는 것이 아니라 **정책이 생각하지 못한 통로를 이용**하는 문제입니다.

## 3. 자주 보이는 단서
| 단서 | 의미 |
|------|------|
| `Content-Security-Policy` 헤더가 매우 엄격함 | 일반 exfiltration 차단 |
| `unsafe-eval` 또는 특정 API만 허용됨 | 제한적 JS 실행 가능 |
| `navigate-to`, `worker-src`, `frame-ancestors`가 설정됨 | 브라우저 이동/프레임도 통제 대상 |
| server-side bot 또는 admin bot이 존재함 | 봇을 대상으로 우회 필요 |
| 네트워크는 막혔지만 브라우저 기능은 남아 있음 | 대체 채널 탐색 필요 |

## 4. 자주 쓰는 우회 유형
| 유형 | 설명 |
|------|------|
| Beacon 계열 | 브라우저의 비동기 전송 기능을 이용 |
| fetchLater / PendingBeacon | 일부 실험적 API로 CSP 우회 가능성 탐색 |
| Timing side-channel | 직접 전송 대신 응답 시간으로 정보 복원 |
| Same-origin sink | 허용된 origin 내에서 간접 저장 후 회수 |
| PostMessage chain | 프레임/창 사이 메시지로 간접 전달 |

## 5. 기본 풀이 루프
```text
1) CSP 헤더를 읽습니다.
2) 어떤 전송/실행 API가 허용되는지 찾습니다.
3) 직접 exfiltration이 막히면, 같은 origin 또는 timing side-channel을 찾습니다.
4) 봇/서버가 무엇을 신뢰하는지 확인합니다.
5) 가장 짧고 안정적인 우회 채널을 선택합니다.
```

## 6. 공격자 관점
1. XSS 자체보다 CSP가 막는 지점을 먼저 확인합니다.
2. 허용된 API를 활용해 우회합니다.
3. 봇의 실행 환경을 기준으로 가능한 채널을 고릅니다.
4. 직접 정보 전송이 어렵다면 간접 관측 방법으로 바꿉니다.

## 7. 방어자 관점
- CSP는 좋지만 `eval`과 실험적 API 허용은 위험합니다.
- 봇이 방문하는 페이지는 가능한 **격리된 origin**에서 서비스합니다.
- URL fragment, localStorage, postMessage 처리 시 입력 검증이 필요합니다.
- timing side-channel까지 고려하면 네트워크 차단만으로는 부족합니다.

## 8. 같이 보면 좋은 페이지
- [[elements-final-writeup]]
- [[web-ctf-writeup-client-side]]
- [[xss]]
- [[web-inspector-ctf-patterns]]

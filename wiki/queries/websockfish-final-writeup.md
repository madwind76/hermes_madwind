---
title: WebSockFish — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, websocket, research, writeup, request-manipulation, input-validation, client-side]
sources: [https://medium.com/@mihasha/websockfish-picoctf-2025-write-up-e7d4711ecfd3, https://medium.com/@ahmednarmer1/ctf-day-22-e303ac9df89b, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/, https://hackmd.io/HtXENiZJQG-w1EsEOZINpg]
confidence: high
---

# WebSockFish — picoCTF 2025 web writeup

> 체스 봇을 정상적으로 이기는 문제가 아니라, [[websocket|WebSocket]]으로 오가는 `[[eval|eval]]` 값을 [[tampering|조작]]해 서버가 클라이언트 제공 평가값을 신뢰하는지 확인하는 picoCTF 2025 Web Exploitation 문제입니다.

## 1. 한 줄 요약
- 문제명 `WebSockFish`는 **[[websocket|WebSocket]]**과 **Stockfish** 체스 엔진을 동시에 암시합니다.
- 실제 체스 게임에서 이겨도 flag가 나오지 않을 수 있습니다.
- 핵심은 [[websocket|WebSocket]] 메시지의 `[[eval|eval]]` 값을 극단적인 음수로 바꿔 fish가 항복하도록 만드는 것입니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 문제명 | WebSockFish |
| 카테고리 | Web Exploitation |
| 핵심 아이디어 | [[websocket|WebSocket]] traffic inspection, [[tampering|message tampering]], client-supplied [[eval|eval]] value |
| 난이도 | easy / beginner-intermediate |
| 관련 개념 | [[websocket-message-tampering-ctf-patterns]], [[parameter-tampering-ctf-patterns]], [[web-ctf-writeup-client-side]] |

## 3. 공격면 정리
| 위치 | 프로토콜/기능 | Auth | Input | Output | Notes |
|---|---|---|---|---|---|
| Chess UI | Browser UI | No | 체스 말 이동 | 봇 응답 | 정상 게임만으로는 flag 조건 미충족 가능 |
| HTML/JS source | Client-side code | No | `ws` / WebSocket URL 확인 | WebSocket 사용 단서 | 문제명과 동작으로 실시간 연결 추정 |
| WebSocket message | [[websocket|WebSocket]] | No | `eval` 값, 게임 상태 | fish 응답/항복 여부 | 핵심 변조 지점 |
| Proxy / DevTools | 분석 도구 | N/A | 메시지 수정·재전송 | 서버 반응 변화 | Burp Suite WebSockets history / Repeater 활용 가능 |

## 4. 풀이 흐름
1. 문제 페이지를 열고 체스판과 fish 봇의 대화형 동작을 확인합니다.
2. 문제명과 HTML source에서 WebSocket 사용 흔적(`ws`, `wss`)을 찾습니다.
3. 브라우저 개발자 도구 또는 Burp Suite로 WebSocket traffic을 관찰합니다.
4. 체스 말을 움직인 뒤 오가는 메시지에서 `eval` 값을 확인합니다.
5. 처음에는 작은 조작으로 서버 반응이 달라지는지 봅니다.
6. 서버가 `eval` 값을 신뢰하는 것으로 보이면 극단적인 음수 값을 전송합니다.
7. fish가 항복하거나 비정상적으로 불리하다고 판단하면서 flag가 노출됩니다.

## 5. 메시지 변조 예시
아래는 공개 writeup들에서 공통적으로 설명되는 흐름을 안전하게 일반화한 예시입니다.

```text
# 정상 또는 관찰된 평가값 예시입니다.
# 예상 결과: fish가 평범한 상태 평가 메시지를 반환합니다.
eval -13
```

```text
# 조작된 극단값 예시입니다.
# 예상 결과: 서버가 클라이언트 제공 eval 값을 신뢰하면 fish가 항복하거나 flag 조건이 트리거됩니다.
eval -130000000000
```

## 6. 핵심 학습 포인트

### 6.1 실전에서 먼저 확인할 것
- 메시지 안에 `eval` 같은 **판정용 필드**가 있는지 봅니다.
- 실제 체스 승패보다 **서버가 어떤 값을 신뢰하는지**를 먼저 확인합니다.
- WebSocket history에서 **클라이언트→서버 메시지**를 분리해 재전송할 수 있는지 봅니다.
- 음수/극단값/경계값을 넣었을 때 서버 반응이 바뀌는지 봅니다.

- **WebSocket 메시지도 입력값입니다.** [[http|HTTP]] form이나 JSON API처럼 검증해야 합니다.
- **클라이언트 제공 상태값을 믿으면 안 됩니다.** 체스 평가, 점수, 승패는 서버가 재계산해야 합니다.
- **정상 기능 성공과 flag 조건은 다를 수 있습니다.** Stockfish로 실제 게임을 이기는 것보다 메시지 신뢰 경계를 찾는 것이 핵심입니다.
- **프록시 도구는 HTTP뿐 아니라 WebSocket history도 확인해야 합니다.**

## 7. 방어 관점
- `eval` 같은 게임 판정 값은 서버에서 계산하고, 클라이언트 값은 참고하지 않습니다.
- WebSocket 메시지마다 type, schema, value range를 검증합니다.
- 비정상적으로 큰 수, 음수, 문자열/숫자 타입 혼동, 누락 필드를 거부합니다.
- WebSocket handshake에서 인증만 하고 끝내지 말고, 메시지 처리 시점에도 권한과 상태 전이를 검증합니다.
- WebSocket traffic을 로깅하고 rate limiting을 적용합니다.

## 8. 관련 위키 링크
- [[websocket-message-tampering-ctf-patterns]] — WebSocket 메시지 변조 개념과 방어
- [[websocket]] — WebSocket 프로토콜 자체
- [[http]] — WebSocket 핸드셰이크와 비교되는 요청/응답 프로토콜
- [[tampering]] — 클라이언트 제공 값 변조 개념
- [[eval]] — WebSockFish에서 조작 대상이 된 평가값
- [[parameter-tampering-ctf-patterns]] — 클라이언트 제공 값 변조 패턴
- [[web-ctf-writeup-client-side]] — 클라이언트 사이드/브라우저 상태 계열 허브
- [[web-ctf-writeup-auth-session]] — 서버가 클라이언트 제공 값을 신뢰하는 인증·세션 패턴과 비교
- [[web-ctf-writeup-curation]] — Web CTF writeup 큐레이션
- [[web-ctf-writeup-topic-map]] — Web CTF 상위 지도

## 9. 참고 소스
- [mihasha Medium writeup](https://medium.com/@mihasha/websockfish-picoctf-2025-write-up-e7d4711ecfd3)
- [Ahmed Narmer Medium writeup](https://medium.com/@ahmednarmer1/ctf-day-22-e303ac9df89b)
- [qz.sg picoCTF 2025 Web Exploitation writeups](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [HackMD picoCTF 2025 Write-Up](https://hackmd.io/HtXENiZJQG-w1EsEOZINpg)

## 10. 다음 연결
- `Cookie Monster Secret Recipe`와 비교하면 “클라이언트 저장소에 있는 값 읽기”와 “실시간 메시지 값을 변조하기”의 차이를 볼 수 있습니다.
- `IntroToBurp`와 함께 보면 Burp Suite에서 HTTP 요청뿐 아니라 WebSocket 메시지도 관찰·변조해야 한다는 점을 익히기 좋습니다.

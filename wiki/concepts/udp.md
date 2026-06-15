---
title: UDP — 보안 용어 해설
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [security, glossary, protocol, udp, network]
sources: [https://ko.wikipedia.org/wiki/%EC%82%AC%EC%9A%A9%EC%9E%90_%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C, https://ko.wikipedia.org/wiki/TCP/UDP%EC%9D%98_%ED%8F%AC%ED%8A%B8_%EB%AA%A9%EB%A1%9D]
confidence: high
---

# UDP (User Datagram Protocol)

## 1. 단어 직역 및 쉬운 비유

**UDP**는 **User Datagram Protocol**의 약자입니다.

- **User**: 사용자
- **Datagram**: 독립된 데이터 묶음
- **Protocol**: 통신 규칙

즉, **UDP는 연결을 미리 맺지 않고, 독립된 데이터그램을 빠르게 보내는 통신 규칙**입니다.

비유하면, **우편함에 편지를 그냥 넣는 방식**과 비슷합니다. 도착 확인을 길게 하지 않고 바로 보내기 때문에 빠르지만, 편지가 순서대로 도착하는지나 도착 자체를 보장하지는 않습니다.

## 2. 개념 시각화

![UDP 시각화: 클라이언트가 서버로 데이터그램을 바로 보내는 장면, 비연결형, 포트 번호, 체크섬, 순서 보장 없음, 재전송 없음, SYN/ACK 없음 - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9e2075/0I5haQ-2SrlAKJUzcvRHK_hvjRUbhG.png)

## 3. 전문 용어 설명

**UDP(User Datagram Protocol)**는 인터넷 프로토콜 스위트에서 사용되는 **전송 계층** 프로토콜입니다. TCP와 달리 **비연결형(connectionless)** 이며, 별도의 연결 수립 절차 없이 데이터를 전송합니다. UDP는 **포트 번호**를 통해 응용 프로그램을 구분하고, **체크섬**으로 기본적인 오류 검사를 수행합니다.

UDP는 **순서 보장**, **재전송**, **혼잡 제어**를 제공하지 않기 때문에 신뢰성보다는 지연 시간과 단순성을 중시하는 서비스에 적합합니다. 실시간 음성/영상, 게임, 스트리밍, DNS 질의처럼 빠른 응답이 중요한 환경에서 자주 사용됩니다. 반대로 손실이 허용되지 않는 데이터 전송에는 TCP가 더 적합합니다.

보안 관점에서는 UDP를 이용한 **UDP flood**, **DNS 증폭 공격** 같은 대량 트래픽 공격이 널리 알려져 있습니다. 또한 네트워크 서비스 설계 시 [[tcp]]와의 차이를 이해하고, [[vpn]]과 함께 사용할 때 경로와 성능 특성을 함께 고려해야 합니다.

### 참고
- 한국어 위키백과: https://ko.wikipedia.org/wiki/%EC%82%AC%EC%9A%A9%EC%9E%90_%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C
- 한국어 위키백과: https://ko.wikipedia.org/wiki/TCP/UDP%EC%9D%98_%ED%8F%AC%ED%8A%B8_%EB%AA%A9%EB%A1%9D
- 관련 링크: [[tcp]], [[vpn]], [[ddos]]

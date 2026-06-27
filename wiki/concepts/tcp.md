---
title: TCP (Transmission Control Protocol)
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [security, glossary, protocol, tcp, network]
sources: [https://ko.wikipedia.org/wiki/%EC%A0%84%EC%86%A1_%EC%A0%9C%EC%96%B4_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C, https://ko.wikipedia.org/wiki/%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%82%B9]
confidence: high
---

# TCP (Transmission Control Protocol)

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/%EC%A0%84%EC%86%A1_%EC%A0%9C%EC%96%B4_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%82%B9)

## 1. 단어 직역 및 쉬운 비유

**TCP**는 **Transmission Control Protocol**의 약자입니다.

- **Transmission**: 전달
- **Control**: 제어
- **Protocol**: 약속, 통신 규칙

즉, **TCP는 데이터를 안정적으로 전달하기 위한 통신 규칙**입니다.

비유하면, **전화 통화 전에 서로 “들리나요?”, “네, 들립니다”를 확인하고 나서 대화를 시작하는 방식**과 비슷합니다. 바로 말부터 하는 것이 아니라, 먼저 연결이 제대로 되었는지 확인한 뒤에 대화를 주고받습니다.

## 2. 개념 시각화

![TCP 3-way handshake 비유 시각화: 클라이언트, 서버, SYN, SYN-ACK, ACK, 연결 성립, 순서 보장, 재전송, 흐름 제어 - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9e1ff4/qeyPowwqPrBSTfCgbb9km_PKxroKI0.png)

## 3. 전문 용어 설명

**TCP(Transmission Control Protocol)**는 인터넷 프로토콜 스위트에서 사용되는 **전송 계층(transport layer)** 프로토콜입니다. 연결 지향적이며, 데이터 전달의 **순서 보장**, **오류 검출**, **재전송**, **흐름 제어**, **혼잡 제어**를 제공합니다.

연결 수립은 일반적으로 **3-way handshake**로 이루어집니다. 클라이언트가 **SYN**을 보내고, 서버가 **SYN-ACK**로 응답하며, 클라이언트가 **ACK**를 보내면 연결이 성립합니다. 이 과정은 양쪽이 통신 준비 상태를 확인하기 위한 절차입니다.

보안 관점에서는 TCP가 신뢰성 있는 전송을 제공하지만, **SYN flood**처럼 연결 수립 절차를 악용하는 공격의 대상이 되기도 합니다. 또한 애플리케이션 계층에서 동작하는 서비스와 함께 사용되므로, [[vpn]] 같은 암호화 터널링 기술이나 [[ddos]] 방어 체계와 함께 이해하는 것이 중요합니다. 네트워크 기본 구조를 이해할 때는 [[arp]] 같은 하위 계층 프로토콜과의 관계도 함께 보는 것이 좋습니다. UDP([[udp]])는 TCP와 달리 연결 수립 없이 데이터를 보내는 대표적 전송 계층 프로토콜이므로, 둘의 차이를 함께 보는 것이 좋습니다.

### 참고
- 한국어 위키백과: https://ko.wikipedia.org/wiki/%EC%A0%84%EC%86%A1_%EC%A0%9C%EC%96%B4_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C
- 한국어 위키백과: https://ko.wikipedia.org/wiki/%ED%95%B8%EB%93%9C%EC%85%B0%EC%9D%B4%ED%82%B9
- 관련 링크: [[vpn]], [[ddos]], [[arp]]

---
title: IPS — operational notes, blocking, and tuning
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [security, glossary, ips, ids, intrusion-prevention, network-security, inline, snort, suricata, ngfw, detection, response]
sources: [https://ko.wikipedia.org/wiki/침입_차단_시스템, https://ko.wikipedia.org/wiki/침입_탐지_시스템, https://ko.wikipedia.org/wiki/Snort_(소프트웨어), https://ko.wikipedia.org/wiki/방화벽_(네트워킹), https://ko.wikipedia.org/wiki/차세대_방화벽, https://ko.wikipedia.org/wiki/분산_서비스_거부_공격, https://ko.wikipedia.org/wiki/사이버_보안_관제_센터]
confidence: high
---

# IPS — operational notes, blocking, and tuning

## 요약
- IPS는 인라인 배치된 능동 방어 장비입니다.
- Drop/Reject/Reset/Shun/Quarantine 같은 차단 동작을 수행합니다.
- 운영에서는 오탐 관리와 fail-open/fail-close 정책이 핵심입니다.

## 차단 동작 유형
| 동작 | 설명 | 계층 |
|------|------|------|
| Drop | 패킷을 무시하고 폐기 | L3 |
| Reject | 폐기 + ICMP Unreachable 전송 | L3 |
| Reset | TCP RST 전송으로 연결 종료 | L4 |
| Shun | 특정 IP/포트를 일정 시간 차단 | L3-L4 |
| Quarantine | 감염 호스트를 격리 VLAN으로 이동 | L2-L3 |

## 탐지 및 차단 방식
| 방식 | 설명 | 장점 | 단점 |
|------|------|------|------|
| 시그니처 기반 차단 | 알려진 공격 패턴 매칭 후 드롭 | 빠름, 정확 | 변종/제로데이 미탐지 |
| 프로토콜 이상 탐지 | RFC 위반 행위 탐지 후 차단 | 프로토콜 공격 차단 | 커스텀 프로토콜 미지원 |
| 레이트 리미팅 | 초과 요청 제한 | DDoS/무차별 대입 차단 | 정상 대량 트래픽 제한 가능 |
| 평판 기반 차단 | 악성 IP 평판 DB 활용 | 사전 차단 | FP 가능, 피드 의존 |
| Geo-IP 차단 | 국가별 IP 블록 | 특정 지역 공격 차단 | VPN 우회 가능 |
| ML/AI 기반 차단 | 모델이 실시간 분류 후 차단 | 변종 탐지 가능 | 튜닝 난이도 높음 |

## 솔루션
| 솔루션 | 유형 | 특징 |
|--------|------|------|
| Snort (inline mode) | 오픈소스 NIPS | Snort 2.9+ inline, DAQ, NFQUEUE |
| Suricata (IPS mode) | 오픈소스 NIPS | 10Gbps+, AF_PACKET/NFQUEUE, Lua |
| Palo Alto Networks | 상용 NGFW | IPS 통합 차세대 방화벽 |
| Cisco Firepower/NGIPS | 상용 NIPS | Snort 기반, Talos 연동 |
| Fortinet FortiGate | 상용 UTM | IPS + 방화벽 + AV 통합 |
| Check Point IPS | 상용 NIPS | 휴리스틱 + 시그니처 + 행위 분석 |

## 운영 모범 사례
| 영역 | 권장 사항 |
|------|----------|
| 초기 배포 | 모니터 모드로 1-2주 운영 후 차단 활성화 |
| 오탐 관리 | Critical 1h / High 4h / Medium 24h SLA |
| 튜닝 | 예외 설정, 임계값 조정, 시그니처 커스터마이징 |
| 차단 정책 | 기본 차단보다 허용 목록 기반 권장 |
| HA 구성 | Active-Active 클러스터, 세션 동기화 |
| SIEM/SOAR | 차단 알림을 상관분석 및 자동 대응에 연계 |

## 출처
- [침입 차단 시스템](https://ko.wikipedia.org/wiki/침입_차단_시스템)
- [침입 탐지 시스템](https://ko.wikipedia.org/wiki/침입_탐지_시스템)
- [Snort](https://ko.wikipedia.org/wiki/Snort_(소프트웨어))
- [방화벽 (네트워킹)](https://ko.wikipedia.org/wiki/방화벽_(네트워킹))
- [차세대 방화벽](https://ko.wikipedia.org/wiki/차세대_방화벽)
- [분산 서비스 거부 공격](https://ko.wikipedia.org/wiki/분산_서비스_거부_공격)
- [사이버 보안 관제 센터](https://ko.wikipedia.org/wiki/사이버_보안_관제_센터)

## 관련 위키 링크
- [[ips]] — 상위 개념
- [[ids]] — 수동적 탐지 시스템
- [[vpn]] — 보호 대상 접근 경로
- [[rce]] — 차단해야 할 핵심 위협
- [[cia]] — 가용성 영향 관점

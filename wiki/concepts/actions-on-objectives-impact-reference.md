---
title: Actions on Objectives — impact mapping and reference notes
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [security, glossary, cyber-kill-chain, actions-on-objectives, data-exfiltration, ransomware, wiper, espionage, sabotage, impact, mitre-attck]
sources: [https://ko.wikipedia.org/wiki/사이버_킬_체인, https://ko.wikipedia.org/wiki/데이터_유출]
confidence: high
---

# Actions on Objectives — impact mapping and reference notes

## 요약
- 킬 체인의 마지막 단계에서 공격자가 실제 목적을 실행하는 구간입니다.
- 데이터 유출, 랜섬웨어, 와이퍼, 장기 첩보, 디페이스먼트, 금융 탈취, 리소스 하이재킹으로 나뉩니다.
- 방어는 DLP, 백업, IR, UEBA, SIEM/SOAR 연계를 중심으로 설계합니다.

## MITRE ATT&CK 매핑

| Tactic | Technique ID | Technique Name |
|--------|-------------|----------------|
| **Exfiltration** | **T1041** | Exfiltration Over Command and Control Channel |
| | **T1048** | Exfiltration Over Alternative Protocol |
| | **T1048.001** | Exfiltration Over Symmetric Encrypted Non-C2 Protocol |
| | **T1048.002** | Exfiltration Over Asymmetric Encrypted Non-C2 Protocol |
| | **T1048.003** | Exfiltration Over Unencrypted Non-C2 Protocol |
| | **T1567** | Exfiltration Over Web Service |
| | **T1567.001** | Exfiltration to Code Repository |
| | **T1567.002** | Exfiltration to Cloud Storage |
| | **T1567.003** | Exfiltration to Webhook |
| **Impact** | **T1485** | Data Destruction |
| | **T1486** | Data Encrypted for Impact (Ransomware) |
| | **T1489** | Service Stop |
| | **T1490** | Inhibit System Recovery |
| | **T1491** | Defacement |
| | **T1491.001** | Internal Defacement |
| | **T1491.002** | External Defacement |
| | **T1498** | Network Denial of Service |
| | **T1529** | System Shutdown/Reboot |
| | **T1531** | Account Access Removal |

## 방어 요약
| 대응 영역 | 구체적 방안 |
|----------|-------------|
| 데이터 유출 방지 (DLP) | 네트워크/엔드포인트/클라우드 DLP, 이메일 DLP |
| 랜섬웨어 대응 | 3-2-1 백업, 불변 백업, 행위 탐지, 허니파일 |
| 와이퍼/파괴 대응 | 부팅 가능 백업, TPM/Measured Boot, 외부 SIEM 전송 |
| APT 탐지 | UEBA, 수평 이동 탐지, 크리덴셜 덤프 탐지, 위협 헌팅 |
| 사고 대응 (IR) | 랜섬웨어/유출/와이퍼 플레이북, 포렌식 준비, 규제 신고 |

## 참고 문헌
- [사이버 킬 체인](https://ko.wikipedia.org/wiki/사이버_킬_체인)
- [데이터 유출](https://ko.wikipedia.org/wiki/데이터_유출)
- [랜섬웨어](https://ko.wikipedia.org/wiki/랜섬웨어)
- [와이퍼 (악성코드)](https://ko.wikipedia.org/wiki/와이퍼_(악성코드))
- [사이버 스파이활동](https://ko.wikipedia.org/wiki/사이버_스파이활동)

## 관련 위키 링크
- [[actions-on-objectives]] — 상위 개념
- [[real-world-breach-cases]] — 실제 침해 사례
- [[ips]] — 탐지/차단 계층과 연계되는 방어 관점

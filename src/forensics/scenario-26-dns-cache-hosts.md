---
title: 네트워크 캐시 속 가려진 조각 (DNS Cache & Hosts File Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, network, dns, dns-cache, hosts-file, spoofing]
confidence: high
---

# 네트워크 캐시 속 가려진 조각 (DNS Cache & Hosts File Analysis)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 호스트 이름 분석 우회 및 파싱 (DNS Cache 및 Local Hosts 파일 포렌식)

## 1. 배경 시나리오
사내 도메인인 `secure-auth-vault.local` 페이지 접속자가 가짜 피싱 사이트로 유도되어 패스워드가 탈취당하는 사건이 있었습니다. 보안 분석 팀은 용의자 PC가 로컬 이름 분석 단계를 조작한 것으로 판단하고, 호스트 설정 파일인 `hosts` 파일과 당시 메모리에 캐싱되어 동작하던 DNS 분석 캐시 덤프인 `dns_cache.txt` 파일을 수집했습니다. 공격자는 보안 탐지를 회피하기 위해 도메인의 TXT 레코드 필드 등에 비밀 키값을 숨겨 릴레이한 흔적이 있습니다. 이 두 파일을 분석하여 **로컬 조작에 악용된 타깃 도메인**과 **그 도메인의 DNS TXT 레코드에 남아 있는 플래그**를 찾아야 합니다.

## 2. 제공 파일
* `hosts` (용의자 PC의 로컬 호스트 매핑 설정 파일)
* `dns_cache.txt` (시스템 메모리에서 추출한 DNS 캐시 테이블 덤프 파일)

## 3. 문제 목표
OS의 도메인 주소 변환(Name Resolution) 우선순위(로컬 Hosts -> DNS Cache -> DNS Server)를 이해하고, 제공된 `hosts` 파일의 비정상 도메인 매핑 정보를 탐지한 뒤, `dns_cache.txt` 내에서 해당 도메인의 캐싱된 DNS 레코드 정보(특히 TXT 레코드)를 색인해 플래그를 복구합니다.

## 4. 의도한 풀이 흐름
1. **로컬 매핑 파일 분석 (hosts 검사)**:
   * 제공된 `hosts` 파일을 열어 비정상적인 IP와 도메인 매핑 내역을 확인합니다.
   * 일반적인 루프백(`127.0.0.1`) 설정 외에 다음과 같이 특정 도메인을 외부 C2 대역으로 포워딩한 조작 행을 찾아냅니다:
     `192.0.2.145 secure-auth-vault.local`
2. **DNS 캐시 테이블 대조 (dns_cache.txt 분석)**:
   * 조작 대상 도메인 `secure-auth-vault.local` 키워드를 사용해 `dns_cache.txt` 내의 캐시 목록을 검색합니다:
     ```bash
     grep -A 10 "secure-auth-vault.local" dns_cache.txt
     ```
   * 캐시 데이터 내에서 A 레코드(IP 주소) 외에 TXT 레코드(텍스트 메타데이터) 레코드가 캐싱되어 보존 중인지 점검합니다.
3. **TXT 레코드 데이터 추출**:
   * 조회 결과 다음 정보가 기록되어 있음을 식별합니다:
     ```text
     Record Name . . . . . : secure-auth-vault.local
     Record Type . . . . . : 16 (TXT)
     Time To Live  . . . . : 3600
     Data Length . . . . . : 32
     Section . . . . . . . : Answer
     TXT Record. . . . . . : picoCTF{dns_sp00f1ng_d3t3ct3d}
     ```
   * TXT 레코드 값에 들어 있는 최종 플래그 `picoCTF{dns_sp00f1ng_d3t3ct3d}`를 획득합니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{dns_sp00f1ng_d3t3ct3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 플래그 `picoCTF{dns_sp00f1ng_d3t3ct3d}`가 수록된 DNS TXT 레코드를 바인드(BIND) 또는 공용 DNS 서버에 임시 등록하거나 가상 DNS 네임서버에 설정합니다.
  2. Windows 환경에서 해당 도메인에 대한 DNS 질의를 강제로 수행하여 메모리에 캐시가 물리 로드되도록 합니다:
     `nslookup -type=txt secure-auth-vault.local`
  3. 로컬 호스트 주소 분석을 강제 변경하기 위해 `C:\Windows\System32\drivers\etc\hosts` 파일에 조작된 매핑(`192.0.2.145 secure-auth-vault.local`)을 등록합니다.
  4. 커맨드라인에서 DNS 캐시 덤프를 생성하여 텍스트로 저장합니다:
     `ipconfig /displaydns > dns_cache.txt`
  5. 최종 `hosts` 파일과 `dns_cache.txt` 파일을 배포 아티팩트로 패킹합니다.
* **출제 포인트**: 
  * 파밍(Pharming) 및 DNS 스푸핑 공격 대응 시 로컬 클라이언트에서 탐지할 수 있는 호스트 및 네트워크 메모리 아티팩트의 상관 분석 원리를 학습하게 합니다.

## 7. 트러블슈팅 및 힌트
* **Q. hosts 파일 변경 내용이 웹 브라우저에서 바로 적용되지 않는 이유는 무엇인가요?**
  * A. 모던 웹 브라우저(크롬, 파이어폭스 등)는 내부적으로 자체 DNS 캐시 테이블을 별도로 운용하므로, OS 수준의 `hosts` 파일을 고쳐도 수 초에서 수 분간 이전 주소로 리다이렉트될 수 있습니다. 이를 즉시 초기화하려면 브라우저 내부 관리자 메뉴(`chrome://net-internals/#dns`)에서 'Clear host cache'를 눌러 주어야 합니다.
* **Q. dns_cache.txt가 제공되지 않고 휘발된 경우 DNS 흔적은 어떻게 찾나요?**
  * A. DNS 질의 및 응답 패킷은 기본적으로 UDP 53 포트를 이용해 암호화되지 않은 채 흐르므로, 앞서 실습한 네트워크 PCAP 분석을 병행하여 로컬 게이트웨이 유출 패킷을 카빙해 내면 동일한 레코드를 원격 재구성할 수 있습니다.

## 8. 학습 포인트
* **도메인 분석 순서(Name Resolution Order)**: 운영체제 내에서 사람이 읽기 쉬운 주소를 IP로 변환하기 위해 거치는 논리적 캐싱 단계를 체계화합니다.
* **DNS TXT 레코드 분석**: 도메인 소유권 증명이나 보안 정책(SPF 등) 선언에 사용되는 TXT 레코드 필드를 악용하여 공격자가 데이터를 우회 통로로 반출하는 은닉 패턴을 분석합니다.

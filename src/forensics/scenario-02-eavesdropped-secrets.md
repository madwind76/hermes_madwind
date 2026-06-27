---
title: 조각난 패킷과 비밀 통신 (Eavesdropped Secrets)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, network, pcap, decryption]
confidence: high
---

# 조각난 패킷과 비밀 통신 (Eavesdropped Secrets)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: `Eavesdrop` (picoCTF 2022), `Trivial Flag Transfer Protocol` (picoCTF 2021)

## 1. 배경 시나리오
사내 위협 모니터링 시스템에서 외부 비인가 IP와의 비정상적인 데이터 전송 흐름을 탐지하고 해당 구간의 네트워크 패킷을 캡처한 `capture.pcapng` 파일을 확보했습니다. 예비 분석 결과, 공격자와 내부 조력자가 평문 프로토콜을 이용해 대화를 나누고 특정한 비밀 파일을 전송한 정황이 드러났습니다. 패킷에서 대화 내용과 파일을 추출해 기밀 데이터를 해독해야 합니다.

## 2. 제공 파일
* `capture.pcapng` (외부 통신 기록이 포함된 네트워크 패킷 캡처 파일)

## 3. 문제 목표
네트워크 스트림 분석을 통해 공격자 간의 평문 대화 로그를 복구하여 복호화 명령어와 비밀키를 알아낸 후, 전송된 암호화 파일을 카빙(Carving)하여 원래 파일로 복구합니다.

## 4. 의도한 풀이 흐름
1. **패킷 분석 도구 실행**: Wireshark 또는 `tshark` 명령어를 이용해 `capture.pcapng` 파일을 엽니다.
2. **TCP 스트림 추적**:
   * Wireshark의 `Follow TCP Stream` 기능을 활용해 대화가 오고 간 스트림을 탐색합니다.
   * 예: 대화 내용 중 공격자가 "I have encrypted the flag file. You can decrypt it using: `openssl enc -d -aes-256-cbc -pbkdf2 -in flag.enc -out flag.txt -k <password>`"와 같은 구체적인 복호화 힌트와 비밀키를 보낸 스트림을 식별합니다.
3. **파일 추출**:
   * 다른 TCP 스트림에서 이진 데이터(Raw Data) 형태로 전송된 암호화 파일(`flag.enc`)의 페이로드를 찾습니다.
   * Wireshark에서 해당 스트림의 포맷을 `Raw`로 변경하고 `Save as...` 기능을 이용해 파일(`flag.enc`)로 저장합니다.
4. **명령어 실행 및 복호화**:
   * 대화에서 식별한 OpenSSL 복호화 명령어를 실행합니다.
   * 예시 명령어: `openssl enc -d -aes-256-cbc -pbkdf2 -in flag.enc -out flag.txt -k supersecretpassword`
5. **결과 확인**: 복호화 완료된 `flag.txt` 파일을 열어 플래그를 획득합니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{pcap_eavesdropping_decrypted}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 파일 `flag.txt`를 생성합니다.
  2. OpenSSL을 활용하여 암호화합니다:
     `openssl enc -aes-256-cbc -pbkdf2 -in flag.txt -out flag.enc -k supersecretpassword`
  3. 로컬 가상 환경이나 컨테이너 간에 Netcat(`nc`) 또는 간단한 TCP 소켓 통신을 이용해 대화를 나누고 `flag.enc`를 전송하는 시나리오를 실행하며 `tcpdump` 또는 Wireshark로 패킷을 캡처합니다.
     * 포트 9001: 협상 대화 전송 (평문)
     * 포트 9002: `flag.enc` 바이너리 스트림 전송
  4. 캡처된 패킷에서 불필요한 패킷을 제거(필터링 후 다른 이름으로 저장)하여 크기를 줄인 `capture.pcapng`를 제작합니다.
* **출제 포인트**: 
  * Wireshark의 TCP 스트림 분석 숙련도와 네트워크 패킷 내 바이너리 데이터 추출 기법을 평가합니다.
  * 암호학 도구(OpenSSL CLI)의 기본 사용 방법을 실습하도록 유도합니다.

## 7. 트러블슈팅 및 힌트
* **Q. OpenSSL 복호화 시 'bad decrypt' 에러가 발생합니다.**
  * A. 대화 로그에 적힌 암호 알고리즘(예: `-aes-256-cbc` 등)이나 비밀번호 키워드가 정확히 매칭되는지 확인하십시오. 또한 최근 버전의 OpenSSL은 `-pbkdf2` 옵션을 필수로 요구하므로, 출제 당시 해당 옵션 유무를 대화 기록과 맞춰 보아야 합니다.
* **Q. Wireshark에서 파일을 저장했는데 헤더가 이상해 복호화가 안 됩니다.**
  * A. Wireshark의 Follow Stream 창에서 화면 표시 방식을 ASCII가 아닌 **Raw**로 설정했는지 확인하십시오. ASCII 상태로 저장하면 특수 바이트 문자들이 텍스트 인코딩 문제로 깨져 파일이 손상됩니다.

## 8. 학습 포인트
* **패킷 카빙 (Packet Carving)**: 네트워크 프로토콜 페이로드 영역에서 완전한 바이너리 파일을 재구성하는 원리를 습득합니다.
* **대칭키 암호화 분석**: 침해 사고 분석에서 획득한 암호 키와 툴체인(OpenSSL) 정보를 바탕으로 실제 증거 데이터를 복구하는 절차를 경험합니다.

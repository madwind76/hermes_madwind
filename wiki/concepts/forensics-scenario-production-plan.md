---
title: 초중급용 포렌식 문제 제작안 5선
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md, https://github.com/kisec/wiki/blob/main/concepts/forensics-beginner-intermediate-scenarios.md]
confidence: medium
---

# 초중급용 포렌식 문제 제작안 5선

## 목적
이 문서는 `forensics-beginner-intermediate-scenarios`의 5개 시나리오를 **실제 CTF 문제로 배포할 수 있는 수준**으로 정리한 제작안입니다.

## 공통 제작 원칙
- 파일은 1~3개 아티팩트로 제한합니다.
- 정답은 1차 힌트와 2차 힌트를 합치면 자연스럽게 보이게 만듭니다.
- 초급은 `메타데이터 / 문자열 / 단일 디코딩`, 초중급은 `아티팩트 2개 이상 결합`이 핵심입니다.
- 플래그 형식은 통일합니다: `picoCTF{...}`
- 참가자에게는 **문제 설명만** 제공하고, 제작자용 단서와 정답 규칙은 별도로 둡니다.

## 제작 체크리스트
- [ ] 샘플 파일만으로도 문제 의도가 드러나는가?
- [ ] 정답까지의 경로가 한 번에 너무 길지 않은가?
- [ ] 숨은 정보가 단일 도구로만 해결되지 않도록 균형을 맞췄는가?
- [ ] 과도한 brute force 없이 해결 가능한가?
- [ ] 플래그 생성 규칙이 테스트 가능한가?

---

## 1) 사내 메신저 유출 로그

### 제작 목표
Windows 이벤트 로그와 간단한 실행 흔적만으로 침입자 계정, 유출 파일명, 시각을 복원하게 합니다.

### 제공 파일
- `Security.evtx`
- `System.evtx`
- `Users.csv`
- `execution-notes.txt`

### 정답 생성 규칙
- 최종 플래그: `picoCTF{<username>_<filename>_<HHMM>}`
- 예시: `picoCTF{jlee_payroll.xlsx_0934}`
- `<HHMM>`는 마지막 수상 이벤트 시각의 24시간제 시각입니다.

### 파일 제작 방법
1. 정상 사용자 2명과 의심 사용자 1명을 준비합니다.
2. 로그인 성공/실패 이벤트를 8~12개만 남깁니다.
3. USB 연결 또는 파일 생성 이벤트를 1회 넣습니다.
4. `execution-notes.txt`에 파일명 일부와 메모 한 줄을 남깁니다.

### 검증 포인트
- 참가자가 이벤트 로그만 보고도 타임라인을 만들 수 있어야 합니다.
- 파일명과 계정명이 서로 교차 검증되도록 해야 합니다.

---

## 2) 잠긴 노트북의 비밀 메모

### 제작 목표
디스크 이미지, 메모리 덤프, 메모 파일을 조합해 복구 키 조각이나 비밀 문구를 찾게 합니다.

### 제공 파일
- `disk.dd`
- `memory.raw`
- `notes.txt`
- `recovery-hint.png`

### 정답 생성 규칙
- 최종 플래그: `picoCTF{<recovery_phrase>}`
- 예시: `picoCTF{stolen_keys_live_here}`
- `<recovery_phrase>`는 메모리 덤프의 문자열과 이미지 메타데이터를 합친 결과입니다.

### 파일 제작 방법
1. `memory.raw`에는 `strings`로 보이는 키워드를 2~3개 넣습니다.
2. `disk.dd`에는 실제 파일시스템 분석이 필요한 흔적만 남깁니다.
3. `recovery-hint.png`에는 메타데이터 또는 숨은 문자열 1개만 넣습니다.
4. `notes.txt`에 날짜/위치/별칭 중 하나를 넣어 단서를 보강합니다.

### 검증 포인트
- 디스크 자체를 해독하는 문제가 아니라 **흔적을 종합**하는 문제여야 합니다.
- 메모리와 이미지 중 최소 1개는 반드시 해석이 필요해야 합니다.

---

## 3) 스테가노 우편물

### 제작 목표
이미지 내부 메타데이터와 숨은 문자열을 결합해 짧은 암호문을 복원하게 합니다.

### 제공 파일
- `postcard.png`
- `caption.txt`
- `metadata.log`

### 정답 생성 규칙
- 최종 플래그: `picoCTF{<decoded_message>}`
- 예시: `picoCTF{meet_me_at_midnight}`
- `<decoded_message>`는 base64 또는 단순 치환으로 1회 디코딩되도록 구성합니다.

### 파일 제작 방법
1. 메타데이터에 힌트 문자열을 심습니다.
2. 이미지 본문에는 짧은 base64 또는 LSB 문자열을 넣습니다.
3. `caption.txt`는 디코딩 순서를 암시하는 짧은 문장으로 둡니다.
4. 한 번 더 복원할 수 있는 가짜 문자열을 하나 섞어 오답 유도를 만듭니다.

### 검증 포인트
- 메타데이터를 놓쳐도 image strings가 보조 단서가 되어야 합니다.
- 너무 긴 base64는 피하고, 초급자가 직접 손으로 풀 수 있는 수준으로 둡니다.

---

## 4) 깨진 패킷 속 단서

### 제작 목표
PCAP에서 흩어진 payload를 재조립하고, 디코딩한 뒤 최종 파일을 복원하게 합니다.

### 제공 파일
- `capture.pcapng`
- `flows.txt`
- `payload-map.csv`

### 정답 생성 규칙
- 최종 플래그: `picoCTF{<restored_payload>}`
- 예시: `picoCTF{packet_reassembly_is_fun}`
- `<restored_payload>`는 재조립된 파일의 내부 문자열입니다.

### 파일 제작 방법
1. 정답 payload를 2~4개 조각으로 나눕니다.
2. 조각의 순서를 packet 번호와 함께 숨겨 둡니다.
3. 정상 트래픽 1~2개를 섞어 잡음을 만듭니다.
4. `flows.txt`에 특정 스트림만 보게 하는 단서를 넣습니다.

### 검증 포인트
- 참가자가 stream follow로 재조립해야만 답이 보이게 해야 합니다.
- base64 조각이 너무 쉽게 정렬되지 않도록 약간의 순서 변형을 줍니다.

---

## 5) 엔디언이 뒤집힌 증거물

### 제작 목표
바이트 순서만 바로잡아 문자열을 읽게 만드는 아주 단순하지만 사고력 있는 문제로 만듭니다.

### 제공 파일
- `artifact.bin`
- `hex-dump.txt`
- `notes.txt`

### 정답 생성 규칙
- 최종 플래그: `picoCTF{<recovered_text>}`
- 예시: `picoCTF{endianness_matters}`
- `<recovered_text>`는 2바이트 또는 4바이트 단위 byte swap 결과입니다.

### 파일 제작 방법
1. 플래그 문자열을 먼저 정하고 hex로 변환합니다.
2. 2바이트 또는 4바이트 단위로 반전한 값을 `artifact.bin`에 넣습니다.
3. `hex-dump.txt`에는 일부만 정상 방향으로 보여 혼동을 줍니다.
4. `notes.txt`에 little-endian / big-endian 중 하나를 직접 언급하지 않고 암시합니다.

### 검증 포인트
- 압축/암호화가 아니라 **바이트 순서**가 핵심이어야 합니다.
- 초급자는 2바이트 단위, 초중급자는 혼합 단위로 확장할 수 있습니다.

---

## 배포 전 최종 점검
- [ ] 문제 설명이 지나치게 많은 배경지식을 요구하지 않는가?
- [ ] 정답 생성 규칙이 운영자 입장에서 재현 가능한가?
- [ ] 파일 수가 적당하고, 너무 긴 노가다를 요구하지 않는가?
- [ ] 참가자가 막혔을 때 다음 단서를 추적할 수 있는가?

## 관련 페이지
- [[forensics-beginner-intermediate-scenarios]]
- [[forensics-scenario-deployment-readme]]
- [[forensics-writeup-family-hub]]
- [[picoctf-2024-forensics-survey]]
- [[picoctf-2025-forensics-survey]]

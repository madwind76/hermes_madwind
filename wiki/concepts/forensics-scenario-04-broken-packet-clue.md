---
title: 깨진 패킷 속 단서
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md]
confidence: medium
---

# 깨진 패킷 속 단서

> 난이도: 초중급
> 소요 시간: 25~35분

## 배경
의심스러운 네트워크 통신이 캡처되었고, 데이터는 여러 패킷에 분산되어 전송되었습니다.

## 제공 파일
- `capture.pcapng`
- `flows.txt`
- `payload-map.csv`

## 문제 목표
패킷 안에 흩어진 문자열을 다시 이어 붙여 최종 파일의 내용을 확인합니다.

## 의도한 풀이 흐름
1. Wireshark 또는 tshark로 스트림을 분리합니다.
2. `flows.txt`로 중요한 스트림을 찾습니다.
3. HTTP 응답 또는 TCP stream에서 base64 조각을 모읍니다.
4. 필요한 순서대로 이어 붙여 디코딩합니다.
5. 복원된 파일에서 플래그를 찾습니다.

## 정답 규칙
- `picoCTF{<restored_payload>}`
- 예시: `picoCTF{packet_reassembly_is_fun}`

## 제작 포인트
- 스트림은 2~3개만 두고 정답 스트림은 하나로 제한합니다.
- base64를 너무 길게 만들지 말고 줄바꿈만 적당히 넣습니다.
- 복원 결과가 텍스트든 이미지든 최종 확인이 명확해야 합니다.

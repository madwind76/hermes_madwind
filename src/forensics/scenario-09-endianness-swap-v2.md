---
title: 깨진 조각 맞추기 (Endianness Swap v2)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, file-header, endianness, script, image-recovery]
confidence: high
---

# 깨진 조각 맞추기 (Endianness Swap v2)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: `endianness-v2` (picoCTF 2024)

## 1. 배경 시나리오
공격자가 기밀 플래그가 담긴 이미지 파일을 외부로 전송하기 직전, 보안 모니터링 시스템의 차단을 우회하기 위해 이미지 파일의 파일 바이트 순서(엔디언)를 뒤집어 난독화해 두었습니다. 이 파일 `scrambled_image`는 일반적인 방법으로는 손상된 파일로 분류되어 이미지 뷰어로 열리지 않습니다. 분석가는 파일의 구조를 분석해 바이트 순서를 정상적으로 재정렬하고 플래그가 적힌 원본 이미지를 복구해야 합니다.

## 2. 제공 파일
* `scrambled_image` (바이트 순서가 4바이트 단위로 뒤집힌 바이너리 파일)

## 3. 문제 목표
헥스 데이터 상에서 정상적인 이미지 시그니처가 특정 바이트 단위(DWORD, 4바이트)로 역순 배치(Byte Swapping)되어 있음을 탐지하고, 간단한 스크립트(Python 등) 또는 데이터 변환 도구(CyberChef)를 작성하여 정상적인 바이트 순서로 복원합니다.

## 4. 의도한 풀이 흐름
1. **바이너리 관찰**:
   * `xxd scrambled_image | head` 명령을 통해 파일 시작 부분을 헥스로 관찰합니다.
   * 첫 4바이트가 `E0 FF D8 FF` 등으로 나옵니다.
2. **시그니처 패턴 매칭**:
   * 일반 JPEG 이미지의 시작 매직 바이트가 `FF D8 FF E0` 임을 고려해 볼 때, 4바이트 단위로 바이트 순서가 정반대로 뒤집혀 저장(리틀 엔디언 구조화)되어 있음을 알아챕니다.
     (예: `FF D8 FF E0` -> `E0 FF D8 FF`, `JFIF` -> `FIFJ` 등)
3. **복구 스크립트 작성 (또는 도구 사용)**:
   * **Python 스크립트 작성**:
     ```python
     with open("scrambled_image", "rb") as f:
         data = f.read()
     
     # 4바이트 단위로 읽어 순서를 뒤집은 뒤 저장
     fixed_data = bytearray()
     for i in range(0, len(data), 4):
         chunk = data[i:i+4]
         fixed_data.extend(chunk[::-1]) # 역순 정렬
         
     with open("recovered.jpg", "wb") as f_out:
         f_out.write(fixed_data)
     ```
   * **CyberChef 활용**:
     * Input으로 `scrambled_image`를 로드합니다.
     * Recipe로 `Swap endianness`를 선택하고, Word Length를 `4`로 설정하여 변환된 결과를 확인하고 다운로드합니다.
4. **결과 검증**: 복구된 `recovered.jpg` 파일을 열어 내부에 적힌 텍스트 플래그를 읽습니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{bytes_swapped_successfully}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 플래그 이미지가 들어간 정상 JPEG 파일 `flag.jpg`를 준비합니다.
  2. 파이썬을 이용해 4바이트 단위로 순서를 거꾸로 연산한 난독화 파일을 생성합니다:
     ```python
     with open("flag.jpg", "rb") as f:
         orig = f.read()
     scrambled = bytearray()
     # 패딩을 위해 파일 크기가 4의 배수가 아닐 시 0x00 등으로 패딩 처리
     for i in range(0, len(orig), 4):
         chunk = orig[i:i+4]
         if len(chunk) < 4:
             chunk = chunk + b"\x00" * (4 - len(chunk))
         scrambled.extend(chunk[::-1])
     with open("scrambled_image", "wb") as f_out:
         f_out.write(scrambled)
     ```
* **출제 포인트**: 
  * 컴퓨터의 메모리 저장 방식(Big Endian vs Little Endian)의 하드웨어적 원리를 파일 포낸식 관점에서 복구 스크립트로 극복하는 개발력과 구조 이해도를 검증합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 복구 스크립트를 실행한 후 뷰어로 열었는데 여전히 일부가 깨지거나 열리지 않습니다.**
  * A. 이미지 파일 크기가 4바이트 단위로 완벽히 맞아떨어지지 않아 파일 끝부분(Trailer) 처리가 잘못되었을 수 있습니다. 슬라이싱 시 마지막 청크의 길이가 4바이트보다 작을 때의 패딩 처리를 점검하십시오.
* **Q. 엔디언이 2바이트(Word) 단위일 수도 있나요?**
  * A. 네, 문제 변형에 따라 2바이트(WORD) 단위 스왑일 수도 있으므로, 최초 헤더 분석 단계에서 `JFIF` 아스키 문자가 `F J I F` (2바이트씩 스왑) 인지, `F I F J` (4바이트씩 스왑) 인지 글자 배치를 통해 판단해야 합니다.

## 8. 학습 포인트
* **엔디언 변환(Endianness)**: 시스템 환경에 따른 Little-Endian과 Big-Endian의 바이트 정렬 특성을 학습합니다.
* **스크립트 기반 카빙**: GUI 도구의 한계를 넘어 대용량 이미지 손상 상황에서 파이썬 등 범용 언어 스크립트로 빠르게 바이너리를 필터링 및 복구하는 역량을 배양합니다.

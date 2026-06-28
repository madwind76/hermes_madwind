---
title: Volatility 3를 이용한 메모리 삽입 셸코드 카빙 및 어셈블 디코딩 (Memory Shellcode)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, shellcode, xor-decryption, assembly, capstone]
confidence: high
---

# Volatility 3를 이용한 메모리 삽입 셸코드 카빙 및 어셈블 디코딩 (Memory Shellcode)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 메모리 덤프 셸코드 역분석 및 디코딩 (Volatility Shellcode 복구)

## 1. 배경 시나리오
공격자가 정상 스레드 흐름에 원격 연결 통제용 셸코드(Shellcode)를 주입해 실행 중이던 침해 PC의 RAM 백업 이미지 분석을 진행했습니다. 분석관은 Volatility 3 `windows.malfind` 플러그인을 사용하여 의심되는 프로세스의 `PAGE_EXECUTE_READWRITE` 메모리 주소 섹터를 통째로 덤프하여 `injected_page.dmp` 파일을 카빙 격리했습니다. 공격자는 메모리 문자열 검출 솔루션의 시그니처 매칭을 피하기 위해, 셸코드의 데이터 영역에 보존하는 기밀 플래그 정보를 특정 단일 바이트 XOR 연산으로 암호화한 뒤 실행 시점에 실시간 복호화 루프(XOR Decryption Loop)를 돌려 풀도록 코딩해 두었습니다. 이 덤프 파일 내의 **셸코드 기계어 구문을 역어셈블(Disassemble)하고 XOR 해독 로직을 분석하여 플래그**를 구출하십시오.

## 2. 제공 파일
* `injected_page.dmp` (malfind 플러그인에 의해 복제 덤프된 인젝션 영역의 원시 기계어 셸코드 이진 파일)

## 3. 문제 목표
메모리에 주입되는 x86/x64 원시 셸코드(Raw Shellcode)의 구조적 특징과 런타임 자가 복호화(Self-Decryption) 메커니즘을 파악하고, 역어셈블러(Capstone, IDA, Ghidra 등) 또는 파이썬 스크립트를 통해 XOR 연산 키와 암호화된 바이트 시퀀스를 격리해 디코딩합니다.

## 4. 의도한 풀이 흐름
1. **바이너리 정적 리버싱**:
   * 제공된 `injected_page.dmp` 파일은 바이너리 파일이므로, `ndisasm` 또는 파이썬의 `capstone` 엔진 등을 활용해 32비트(또는 64비트) x86 기계어 코드로 어셈블 해독을 시도합니다:
     ```bash
     ndisasm -b 32 injected_page.dmp | head -n 20
     ```
2. **XOR 복호화 루프 코드 분석**:
   * 어셈블리 덤프 출력에서 다음과 같은 전형적인 XOR 자가 복호화 기계어 구문을 판독합니다:
     ```assembly
     00000000  31C0              xor eax,eax
     00000002  B923000000        mov ecx,0x23        ; 복호화할 바이트 길이: 35 바이트
     00000007  8D36              lea esi,[esi]       ; 암호화 데이터 시작 주소 오프셋
     00000009  803642            xor byte [esi],0x42 ; XOR Key: 0x42
     0000000C  46                inc esi
     0000000D  E2FA              loop 0x9            ; 루프 반복
     ```
   * 이 코드를 통해 셸코드가 특정 암호화 블록의 데이터를 단일 바이트 헥스 값 **`0x42`** 키로 XOR 연산하여 평문 문자열을 복구함을 파악합니다.
3. **암호화 데이터 영역 격리 및 복호화**:
   * 복호화 대상이 되는 35바이트 크기의 원시 헥스 바이트 스트림 영역을 파일 후반부에서 식별해 추출합니다:
     `32 2b 21 2d 01 16 04 39 31 2a 71 2e 2e 21 72 26 71 1d 3a 72 30 1d 2e 2d 2d 32 1d 26 27 21 2d 26 27 26 3f`
   * 파이썬 스크립트를 작성하여 이 바이트 배열을 단일 키 `0x42`와 일일이 XOR 연산 처리합니다:
     ```python
     enc_bytes = bytes.fromhex("32 2b 21 2d 01 16 04 39 31 2a 71 2e 2e 21 72 26 71 1d 3a 72 30 1d 2e 2d 2d 32 1d 26 27 21 2d 26 27 26 3f")
     flag = "".join(chr(b ^ 0x42) for b in enc_bytes)
     print(flag)
     ```
4. **플래그 도출**:
   * 스크립트 실행 결과 출력되는 원본 플래그 값을 획득합니다:
     `picoCTF{sh3llc0d3_x0r_loop_decoded}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sh3llc0d3_x0r_loop_decoded}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 플래그 문자열 `picoCTF{sh3llc0d3_x0r_loop_decoded}` (35글자)를 0x42 바이트로 XOR 변환하여 암호화된 바이트 시퀀스를 만듭니다.
  2. x86 어셈블리 언어로 암호화 데이터를 복호화(Loop Decrypt)하고 메모리에 스택으로 적재하는 셸코드 어셈블리 프로그램 소스(`payload.asm`)를 작성합니다.
  3. NASM 컴파일러를 기동해 raw 셸코드 바이너리인 `injected_page.dmp`로 컴파일합니다:
     `nasm -f bin payload.asm -o injected_page.dmp`
  4. 컴파일 완료된 덤프 파일 내에 XOR 복호화 로직과 암호 바이트들이 명확하게 실존하는지 ndisasm 교차 검수를 수행하여 배포 파일로 패키징합니다.
* **출제 포인트**: 
  * 메모리 포렌식 침해 감사 시, 단순 텍스트 `strings` 검색 필터링을 우회하여 난독화(Obfuscated Shellcode)된 상태로 숨겨져 가동되는 셸코드 내부의 기계어 연산 흐름을 역공학 역어셈블러 관점으로 진단하고, 암호 연산 로직을 환원해 원래 은닉 기밀을 색출하는 실전적 리버싱 역량을 교육합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 셸코드 바이너리의 32비트와 64비트 아키텍처는 어떻게 판별하나요?**
  * A. 디폴트 분석 시 32비트 x86 링커 규칙을 기본 대입해 보되, `ndisasm -b 32` 수행 결과 비정상적인 레지스터 참조나 끊어지는 기계어 지시자가 대량으로 뿜어진다면 `ndisasm -b 64` 옵션을 주어 64비트 모드로 교차 대조하십시오.
* **Q. Capstone 모듈이 설치되어 있지 않은 리눅스 터미널에서 빠르게 디코딩하는 팁이 있나요?**
  * A. CyberChef에 `XOR` 연산 모듈이 탑재되어 있습니다. 추출해 낸 16진수 바이트 시퀀스를 입력 데이터로 기입하고, 레시피에 XOR 모듈을 로드한 뒤 Key에 `42` (Hex 또는 UTF-8 상수) 값을 인가하면 즉각 디코딩 평문을 획득할 수 있습니다.

## 8. 학습 포인트
* **메모리 덤프 카빙 및 셸코드 리버싱**: Volatility dump에 따른 로데이터에서 유효 기계어 영역(Shellcode Payload)을 격리하는 기술을 파악합니다.
* **자가 복호화 메커니즘 분석**: 시그니처 감시망 우회를 시도하는 XOR 복호화 루프의 연산 키 구조와 길이를 어셈블리 코드로 정적 판독하여 해독해 내는 전문 포렌식 리버싱 기법을 내재화합니다.

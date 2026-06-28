---
title: 파이썬 컴파일 바이너리 디컴파일 (Python Compiled pyc Decompilation)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, python, pyc, bytecode, decompilation, pycdc, dis]
confidence: high
---

# 파이썬 컴파일 바이너리 디컴파일 (Python Compiled pyc Decompilation)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: 파이썬 실행 바이너리 리버싱 및 분석 (Python Compiled .pyc 바이트코드 분석)

## 1. 배경 시나리오
사내 서버의 비인가 동작 스크립트 중, 소스코드는 소거되고 컴파일된 바이트코드 파일인 `backdoor.pyc`만 디렉터리에 잔재한 상태로 발견되었습니다. 공격자는 스크립트의 침투 흔적 및 주요 로직을 은닉하기 위해 일반 텍스트 버전(`.py`)은 파쇄하고 바이트코드 형태만 작동시켰습니다. 파이썬 가상 머신(VM)이 직접 구동하는 이 바이트코드 구조를 분석(디컴파일 및 역어셈블)하여 **내부에 하드코딩되어 있던 비밀 통신용 키값(플래그)**을 복원해 내야 합니다.

## 2. 제공 파일
* `backdoor.pyc` (파이썬 스크립트 소스가 컴파일된 raw 바이트코드 파일)

## 3. 문제 목표
파이썬 컴파일 바이너리(`.pyc`)의 내부 물리 구조(Magic Number, Metadata, Marshal.dumps로 직렬화된 Code Object 구조)를 이해하고, 바이트코드 디컴파일러(uncompyle6, pycdc 등) 및 파이썬 표준 라이브러리(`dis`)를 활용하여 원본 파이썬 코드를 안전하게 복구합니다.

## 4. 의도한 풀이 흐름
1. **파이썬 컴파일 버전 감지**:
   * 제공된 `backdoor.pyc` 파일의 선두 4바이트 매직 번호(Magic Number)를 확인해 소스가 컴파일된 원래 파이썬 인터프리터 버전을 가늠합니다 (예: `A3 0D 0D 0A` 등).
2. **바이트코드 디컴파일 (Decompilation)**:
   * **도구 활용**: 파이썬 역공학 도구인 `pycdc` (Decompyle++) 또는 `uncompyle6`을 사용하여 바이트코드를 파이썬 소스코드로 번역합니다.
     ```bash
     pycdc backdoor.pyc
     ```
   * 디컴파일러가 정상 복구한 파이썬 원본 평문 코드를 획득합니다:
     ```python
     # Source Generated with Decompyle++
     # File: backdoor.pyc (Python 3.10)
     
     import base64
     import urllib.request
     
     FLAG = "picoCTF{pyc_bytecode_decompiled_and_reversed}"
     # ... [이하 생략]
     ```
3. **수동 디스어셈블 교차 분석 (디컴파일 실패 시 우회)**:
   * 디컴파일러 패키지 버전 문제로 코드가 깨지는 경우, 파이썬 표준 내장 모듈인 `dis` (Disassembler)를 가동하여 원시 어셈블리 바이트 코드를 역어셈블 덤프합니다:
     ```bash
     python3 -m dis backdoor.pyc
     ```
   * 출력된 바이트코드 명령어 세트(LOAD_CONST, STORE_FAST 등) 목록에서 변수 초기화 영역(`LOAD_CONST` 지시자가 가리키는 상수 레지스트리 목록)을 대조하여 문자열을 역추적합니다.
4. **플래그 획득**:
   * 소스코드 내부에서 하드코딩된 변수 `FLAG` 값인 문자열을 추출합니다:
     `picoCTF{pyc_bytecode_decompiled_and_reversed}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{pyc_bytecode_decompiled_and_reversed}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 플래그 변수를 탑재한 파이썬 스크립트 `backdoor.py`를 작성합니다:
     ```python
     FLAG = "picoCTF{pyc_bytecode_decompiled_and_reversed}"
     print("Backup service is active...")
     ```
  2. 파이썬 표준 라이브러리 `py_compile`을 사용해 컴파일을 수행합니다:
     `python3 -m py_compile backdoor.py`
  3. 캐시 디렉터리(`__pycache__/`) 아래에 자동 생성된 `backdoor.cpython-310.pyc` 형식의 파일을 획득합니다.
  4. 획득한 파일의 이름을 `backdoor.pyc`로 치환하고, uncompyle6 / pycdc / python3 -m dis 등의 파이프라인 분석으로 플래그 추출이 확실하게 성립하는지 최종 테스트한 후 배포합니다.
* **출제 포인트**: 
  * 파이썬 스크립트 악성 행위를 분석할 때 직면하게 되는 이진 스크립트 바이트코드(Python Bytecode Forensics)의 명세를 해독하고, 정적 역컴파일 분석 절차를 활용해 원본 소스코드를 안전하게 환원하는 기초 기스크 엔지니어링 역량을 함양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. uncompyle6 실행 시 'Unsupported Python version' 에러가 발생하며 파싱이 중단됩니다.**
  * A. `uncompyle6`은 Python 3.8 대역 이하의 코드 해독에 특화되어 있습니다. 최신 파이썬 3.9/3.10/3.11 환경에서 빌드된 `.pyc` 파일은 AST 문법 파서의 변형으로 인해 디컴파일이 거부될 수 있습니다. 이 경우 C++로 개발되어 최신 컴파일 사양을 널리 지원하는 **pycdc** (Decompyle++) 유틸리티를 기동하거나, 파이썬 표준 `dis` 모듈 역어셈블 명령행으로 우회해 직접 바이트 상수를 색인해야 합니다.
* **Q. .pyc 파일의 헤더에 기록되는 데이터 필드 구성은 어떻게 되나요?**
  * A. 파이썬 3 기준 기본 헤더 레이아웃은 다음과 같습니다 (각 4바이트 씩 총 16바이트 고정 크기):
     * 오프셋 0~3: 매직 넘버 (파이썬 컴파일러 버전 식별)
     * 오프셋 4~7: 컴파일 옵션 비트 필드 (PEP 552)
     * 오프셋 8~11: 컴파일 당시의 원본 파일 최종 수정 타임스탬프 (Unix epoch time)
     * 오프셋 12~15: 원본 파일 크기 (File Size)

## 8. 학습 포인트
* **파이썬 가상 머신(Python VM) 컴파일 메커니즘**: 소스코드가 중간 언어인 바이트코드(`.pyc`)로 컴파일되어 마샬링(Marshaling) 기법으로 패킹 보존되는 직렬화 사양을 이해합니다.
* **바이트코드 디컴파일 및 역어셈블**: uncompyle6, pycdc 및 내장 `dis` 툴을 활용해, 바이너리화된 스크립트 코드에서 원본 연산 제어 흐름과 하드코딩 변수 목록을 발굴하는 정적 리버싱 절차를 습득합니다.

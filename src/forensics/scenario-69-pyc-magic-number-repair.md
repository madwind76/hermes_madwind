---
title: 파이썬 컴파일 바이너리 매직넘버 변조 복구 (Python pyc Magic Number Repair)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, file-format, python, pyc, magic-number, hex-editor, decompilation]
confidence: high
---

# 파이썬 컴파일 바이너리 매직넘버 변조 복구 (Python pyc Magic Number Repair)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 파이썬 컴파일 파일 헤더 복원 및 파싱 (Python pyc Magic Number 분석)

## 1. 배경 시나리오
보안 사고 분석 도중 피의자가 파이썬 소스 파일을 지우고 남겨놓은 컴파일된 실행 파일인 `corrupted.pyc` 파일을 확보했습니다. 하지만 이 파일을 분석하기 위해 디컴파일 도구(pycdc, uncompyle6 등)에 입력하면 "Unknown magic number" 또는 "Invalid file header" 오류를 발생시키며 소스 디컴파일 분석이 거부됩니다. 조사관은 피의자가 리버스 엔지니어링 및 악성 행위 정적 진단을 거부하도록 하기 위해 `.pyc` 파일의 최상단 4바이트인 **파이썬 컴파일 매직 넘버(Python Magic Number)**를 고의로 제로아웃(`00 00 00 00`) 훼손해 두었음을 간파했습니다. 이 파일이 **Python 3.10** 버전으로 컴파일되었음을 기반으로 매직 바이트를 교정하여 디컴파일을 성공시키고, **소스 내에 숨겨진 플래그**를 알아내십시오.

## 2. 제공 파일
* `corrupted.pyc` (파이썬 컴파일 매직 넘버 정보인 선두 4바이트가 고의로 오염되어 파싱이 거부되는 바이너리 파일)

## 3. 문제 목표
파이썬 컴파일 바이너리(`.pyc`)의 기본 파일 구조 명세와 파이썬 버전별 컴파일 매직 넘버 대조표 정책을 학습하고, 헥스 에디터 수동 패치 기법을 활용해 바이너리를 정상화하여 디컴파일 세션을 획득합니다.

## 4. 의도한 풀이 흐름
1. **바이너리 헤더 오류 식별**:
   * 제공된 `corrupted.pyc` 파일을 헥스 에디터로 열어 선두 4바이트 오프셋 영역을 확인합니다.
   * 첫 4바이트 값이 `00 00 00 00` (또는 `DE AD BE EF` 등 규격을 이탈한 임의의 바이트)으로 훼손되어 파일 형식 식별자가 상실된 상태임을 인지합니다.
2. **파이썬 3.10 매직 넘버 매핑 대조**:
   * 파이썬 버전별 컴파일러 매직 번호 명세를 대조하여, 대상 개발 버전인 **Python 3.10** 계열의 공식 지정 헥스 매직바이트를 조사합니다.
   * Python 3.10.x의 컴파일 매직 번호는 헥스 규격상 **`6F 0D 0D 0A`** 임을 획득합니다.
     * *참고: 파이썬 매직바이트 하단 2바이트는 항상 리눅스/윈도우 텍스트 줄바꿈 시그니처인 CR/LF (`\r\n` -> `0D 0A`)로 끝나도록 정규 설계되어 있습니다.*
3. **헥스 패칭 및 디컴파일 구동**:
   * 헥스 에디터 상에서 `corrupted.pyc` 파일의 시작 오프셋 0~3 위치에 훼손되어 적혀 있던 바이트를 `6F 0D 0D 0A` 로 덮어쓰기 수동 패치합니다.
   * 복구된 파일을 `repaired.pyc` 이름으로 보관합니다.
   * 디컴파일러 도구(`pycdc` 등)를 기동하여 소스코드를 역컴파일 복구해 냅니다:
     ```bash
     pycdc repaired.pyc
     ```
   * 복구된 소스코드 내용:
     ```python
     # Source Generated with Decompyle++
     # File: repaired.pyc (Python 3.10)
     
     FLAG = "picoCTF{pyc_m4g1c_numb3r_r3p41r_succ3ss}"
     ```
4. **플래그 도출**:
   * 디컴파일된 파이썬 코드의 하드코딩 변수 `FLAG` 값으로부터 플래그를 추출합니다:
     `picoCTF{pyc_m4g1c_numb3r_r3p41r_succ3ss}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{pyc_m4g1c_numb3r_r3p41r_succ3ss}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Python 3.10 환경 가상머신에서 플래그 변수 `FLAG = "picoCTF{pyc_m4g1c_numb3r_r3p41r_succ3ss}"`가 수록된 `payload.py`를 제작합니다.
  2. 파이썬 컴파일러를 기동해 `.pyc` 바이너리를 확보합니다:
     `python3.10 -m py_compile payload.py`
  3. 생성된 `.pyc` 파일의 선두 4바이트(이 버전의 경우 원래 `6f 0d 0d 0a`로 기표됨)를 HxD 등의 에디터를 통해 `00 00 00 00`으로 덮어씁니다.
  4. 가공 완료된 파일을 `corrupted.pyc` 명칭으로 배포합니다.
* **출제 포인트**: 
  * 리버스 엔지니어링이나 포렌식 분석을 교란하기 위해 바이너리 선두의 매직 코드(Magic Identifier)를 변조해 시그니처 감지를 회피하는 고전적 안티 포렌식 행위에 맞서, 내부 런타임 플랫폼 버전 특징을 바탕으로 헤더를 재구성 패치(Header Correction)하는 핵심 기술력을 주지시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. 파이썬 버전별 컴파일 매직 넘버는 어디서 편리하게 조회할 수 있나요?**
  * A. 파이썬 표준 라이브러리 소스 중 `import importlib.util; print(importlib.util.MAGIC_NUMBER.hex())` 명령을 수행하면 현재 구동 중인 파이썬 인터프리터의 4바이트 매직값을 즉각 출력해 줍니다. 대표적인 버전별 매직 정보는 다음과 같습니다:
    * Python 3.8.x: `a3 0d 0d 0a`
    * Python 3.9.x: `61 0d 0d 0a`
    * Python 3.10.x: `6f 0d 0d 0a`
    * Python 3.11.x: `a7 0d 0d 0a`
* **Q. 매직넘버가 틀린 상태로 Python VM에서 직접 python3 corrupted.pyc를 치면 어떻게 되나요?**
  * A. 파이썬 엔진은 바이트코드를 인터프리팅하기 전 선두 매직 번호 값을 읽고 자신의 런타임 버전과 불일치하면 즉각 `RuntimeError: Bad magic number in .pyc file` 에러를 터트리며 작동을 거부합니다.

## 8. 학습 포인트
* **파이썬 컴파일 헤더 규격**: `.pyc` 파일의 물리 배치 사양(Magic Number, Bitfield, Timestamp, Size) 및 버전별 빌드 매크로 상수를 이해합니다.
* **시그니처 회피 안티포렌식 극복**: 인위적으로 훼손된 바이너리 파일을 포맷 명세 및 가상머신 환경 매핑 대조를 통해 복원(Header Hex Patching)하는 정적 역공학 역량을 훈련합니다.

---
title: 파이썬 컴파일 바이너리 내 소스 코드 파일 경로 추출 (Python pyc Source File Path)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, file-format, python, pyc, code-object, source-path, strings, metadata]
confidence: high
---

# 파이썬 컴파일 바이너리 내 소스 코드 파일 경로 추출 (Python pyc Source File Path)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 파이썬 컴파일 바이너리 개발지 정보 규명 (Python .pyc Code Object Path 분석)

## 1. 배경 시나리오
사내 서버 침투에 가동되었던 악성 에이전트 스크립트인 `malicious_agent.pyc` 바이너리가 회수되었습니다. 공격자가 원본 파이썬 소스 코드 파일(`.py`)은 흔적을 남기지 않고 소거했으나, 파이썬 컴파일러는 `.pyc` 바이트코드를 직렬화 생성할 때 실행 시 에러 추적(Traceback) 리포팅 출력을 지원할 목적으로, **개발 당시 소스 코드가 위치했던 원래 호스트 시스템 내의 원본 소스 파일 절대 경로명(Source File Path)**을 코드 오브젝트(Code Object) 내부 속성 테이블에 평문 문자열로 그대로 구착 보존합니다. 수집한 `malicious_agent.pyc` 파일을 분석하여, **헤더 바디 내부 코드 오브젝트 메타데이터 필드에 기록된 공격자의 개발 소스 절대 경로명 속의 플래그**를 구출하십시오.

## 2. 제공 파일
* `malicious_agent.pyc` (파이썬 3 환경에서 컴파일 수립되어 잔재하던 바이트코드 바이너리 파일)

## 3. 문제 목표
파이썬 컴파일 `.pyc` 파일 내부의 코드 오브젝트(PyCodeObject) 직렬화 스펙을 이해하고, 정적 문자열 추출(`strings` 등) 및 헥스 뷰어 스캔을 통해 컴파일 당시 하드코딩 저장되는 원본 소스 경로 메타데이터를 식별해 냅니다.

## 4. 의도한 풀이 흐름
1. **바이너리 평문 데이터 스캔**:
   * 제공된 `malicious_agent.pyc` 파일의 내부 평문 텍스트 이력을 추출하기 위해 `strings` 명령어를 실행합니다:
     ```bash
     strings malicious_agent.pyc
     ```
   * 파이썬 코드 오브젝트가 사용하는 문자열 직렬화 테이블 내의 아스키 엔트리들이 가시화됩니다.
2. **개발지 절대 경로명 식별**:
   * 출력된 문자열 목록 중 개발 당시의 파일 경로를 명시하는 절대 경로 문자열을 탐색 및 식별합니다:
     `/home/suspect/workspace/picoCTF{pyc_c0d3_0bj_s0urc3_path_tr4c3d}/agent.py`
3. **최종 플래그 도출**:
   * 식별된 절대 경로 문자열 내부에 매핑 탑재되어 있던 최종 플래그 값을 획득합니다:
     `picoCTF{pyc_c0d3_0bj_s0urc3_path_tr4c3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{pyc_c0d3_0bj_s0urc3_path_tr4c3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 개발 환경에서 플래그 문자열이 상위 경로명에 수록된 디렉터리 경로를 생성합니다:
     `mkdir -p /home/suspect/workspace/picoCTF{pyc_c0d3_0bj_s0urc3_path_tr4c3d}`
  2. 해당 경로 하위로 이동하여 임의의 동작 파이썬 코드 `agent.py`를 작성합니다.
  3. 파이썬 3 컴파일러를 구동하여 pyc 바이트코드를 빌드합니다:
     `python3 -m py_compile /home/suspect/workspace/picoCTF{pyc_c0d3_0bj_s0urc3_path_tr4c3d}/agent.py`
     (이 빌드가 수립되면 컴파일 엔진이 바이트코드 마샬링 포맷 내부의 `co_filename` 속성 정보로 해당 절대 경로 문자열 `/home/suspect/.../agent.py`를 평문 아스키로 박제 적재합니다)
  4. 생성된 캐시 폴더 내의 `.pyc` 파일명을 `malicious_agent.pyc`로 변경하고 수검 아티팩트로 지정해 유포합니다.
* **출제 포인트**: 
  * 로컬 디스크 상의 원본 스크립트 소스코드가 완전히 지워지더라도, 배포된 컴파일 캐시 파일(`.pyc`)의 저수준 마샬링 데이터 블록(Python Code Object Metadata Forensics)에 박제되어 소거되지 않는 개발 호스트 절대 경로 메타데이터를 역색인해 유출 행위의 용의자 계정명 및 공격 개발 환경 증적을 특정하는 프로페셔널 포렌식 수사 흐름을 학습시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. 파이썬 디컴파일러(pycdc 등)를 실행해도 원본 소스 경로 정보가 출력되나요?**
  * A. 디컴파일러 도구들은 바이트코드를 해석해 파이썬 고수준 소스 코드로 복원해 주지만, `co_filename`과 같은 단순 헤더/메타데이터 테이블 필드 정보는 복원된 `.py` 소스 코드 텍스트 내부에는 직접 표기해 출력하지 않는 경우가 흔합니다. 따라서 이와 같은 호스트 파일 경로 정보를 추출할 때는 디컴파일에 앞서 바이너리에 strings 또는 헥스 스캔을 병행하여 파일 메타데이터 레코드를 단독 적출하는 것이 포렌식 원칙에 부합합니다.
* **Q. 파이썬의 marshal 모듈을 이용해 pyc 내의 co_filename 객체를 파이썬 코드로 직접 파싱해 볼 수 있나요?**
  * A. 네, 가능합니다. 파이썬 기본 제공 `marshal` 라이브러리를 연동하면 다음과 같이 코드로 해당 파일명을 추출할 수 있습니다:
     ```python
     import marshal
     # pyc의 헤더 16바이트를 스킵하고 마샬링된 코드 오브젝트 로드
     with open('malicious_agent.pyc', 'rb') as f:
         f.read(16) # 헤더 스킵
         code_obj = marshal.load(f)
     print(code_obj.co_filename) # 출력 결과 절대 경로
     ```

## 8. 학습 포인트
* **Python Code Object 직렬화 아키텍처**: pyc 바이트코드의 마샬 데이터(co_filename, co_names, co_consts) 저장 구조를 상세히 이해합니다.
* **개발지 흔적(Source Path) 역추적**: 지워진 원본 코드와 무관하게, 바이너리 메타데이터에 고착되어 잔재하는 절대 경로명을 카빙 추출하여 침해 행위 증적의 물리적 입증 단서를 획득하는 노하우를 갖춥니다.

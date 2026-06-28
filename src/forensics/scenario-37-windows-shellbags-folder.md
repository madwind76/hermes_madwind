---
title: 윈도우 바로가기 폴더 분석 (Shellbags Forensics)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, shellbags, usrclass, sbecmd]
confidence: high
---

# 윈도우 바로가기 폴더 분석 (Shellbags Forensics)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 사용자 폴더 접근 흔적 복원 (Windows Shellbags 레지스트리 분석)

## 1. 배경 시나리오
사내 중요 정보가 외장 저장장치(USB)로 유출된 정황이 있어 용의자의 PC를 이미징 분석하고 있습니다. 용의자는 외장 드라이브를 완전히 포맷하고 흔적을 지웠다고 주장하며 범행을 부인하고 있습니다. 하지만 윈도우 탐색기(Windows Explorer)는 사용자가 탐색기로 진입해 열람한 모든 폴더의 뷰 스타일, 아이콘 크기 정보 등을 관리하기 위해 **셸백(Shellbags)** 아티팩트를 보존합니다. 외장 메모리가 언마운트되거나 폴더가 삭제되어도 로컬 레지스트리에 저장된 폴더 접근 이력은 영구 보존됩니다. 용의자 계정의 레지스트리 하이브 파일 `UsrClass.dat`를 분석하여 **용의자가 외장 하드에서 접근했던 특정 플래그 명칭의 폴더 경로**를 복구해야 합니다.

## 2. 제공 파일
* `UsrClass.dat` (용의자 사용자 계정의 윈도우 사용자 레지스트리 하이브 파일)

## 3. 문제 목표
윈도우 셸백(Shellbags) 아티팩트의 기록 원리 및 저장 경로(`BagMRU` 및 `Bags` 키 구조)를 이해하고, 셸백 전용 파싱 도구(SBECmd 등)를 사용하여 용의자가 외장 매체상에서 조회했던 폴더 트리 히스토리를 재구성하여 플래그를 찾아냅니다.

## 4. 의도한 풀이 흐름
1. **셸백 아티팩트 정의 짚기**:
   * 셸백 정보는 사용자 레지스트리 하이브 파일인 `NTUSER.dat` 및 `UsrClass.dat` 내부의 아래 키에 트리 구조로 기록됩니다:
     * `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU`
     * `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags`
2. **레지스트리 하이브 파싱 (SBECmd 활용)**:
   * Eric Zimmerman의 셸백 명령행 분석기인 `SBECmd.exe`를 사용하여 제공된 `UsrClass.dat`를 파싱 및 CSV 형식으로 추출합니다:
     `SBECmd.exe -f UsrClass.dat --csv output_dir`
   * **GUI 도구 활용**: `ShellBags Explorer`를 구동하여 `UsrClass.dat`를 로드합니다.
3. **디렉터리 트리 분석**:
   * 로드된 폴더 목록 중 로컬 C 드라이브 외에 외장 매체 드라이브 문자(예: `D:\`, `E:\`, `F:\` 등)로 시작하는 경로 구조를 파악합니다.
   * 외장 디바이스 하위에 위치했던 폴더들의 명칭을 검토하던 중 다음과 같은 비정상적인 폴더 명칭을 찾아냅니다:
     `F:\project_documents\picoCTF{shellbags_k3eps_tr4ck_of_folders}`
4. **플래그 도출**:
   * 폴더명 자체에 수록되어 있는 플래그 문자열을 추출합니다:
     `picoCTF{shellbags_k3eps_tr4ck_of_folders}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{shellbags_k3eps_tr4ck_of_folders}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 테스트 환경에 외장 USB(볼륨 드라이브: `F:\`)를 마운트합니다.
  2. USB 안에 `project_documents` 폴더를 만들고, 그 하위에 `picoCTF{shellbags_k3eps_tr4ck_of_folders}`라는 폴더를 생성합니다.
  3. 윈도우 탐색기(explorer.exe)를 실행하여 새로 만든 `picoCTF{shellbags_k3eps_tr4ck_of_folders}` 폴더 내부까지 진입하여 화면을 띄운 뒤 윈도우 탐색기 창을 닫습니다. (이 시점에 셸백에 기록이 강제 업데이트됩니다)
  4. 시스템에서 로그아웃하거나 재부팅한 후, 해당 사용자 계정의 로컬 앱 데이터 경로(`C:\Users\<계정명>\AppData\Local\Microsoft\Windows\UsrClass.dat`) 파일을 복제합니다.
  5. 획득한 `UsrClass.dat` 파일을 분석 아티팩트로 지정하여 배포합니다.
* **출제 포인트**: 
  * 디바이스 포맷이나 안티 포렌식 툴 가동 등으로 물리 볼륨 흔적이 완전히 사라진 악조건에서, 호스트 OS(윈도우) 측의 셸백 레지스트리에 백업되어 잔재하는 사용자 행위 흔적(User Activity Artifacts)의 강력한 증거 복원력을 실증합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 일반 레지스트리 편집기(regedit)로 UsrClass.dat를 열 수 없나요?**
  * A. 현재 활성 상태가 아닌 백업 레지스트리 파일(`UsrClass.dat`)을 직접 분석하려면, 윈도우 `regedit` 상에서 임시 키를 만들고 '하이브 로드(Load Hive)' 기능을 이용해 로컬 영역에 임시 마운트시켜 분석해야 하므로 번거롭습니다. `Registry Explorer`나 `SBECmd`와 같은 독립 포렌식 파서 도구를 사용하는 것이 훨씬 빠르고 정확합니다.
* **Q. 셸백 정보에 기록된 폴더 생성 시간과 실제 디스크의 생성 시간이 다른 이유는 무엇인가요?**
  * A. 셸백 내부에 기록되는 시간 메타데이터는 윈도우 탐색기가 해당 폴더를 **최초로 렌더링(열람)한 시점**이므로, 디스크에 폴더가 물리 생성된 원래 시점과는 약간의 오차가 존재할 수 있습니다.

## 8. 학습 포인트
* **윈도우 셸백(Shellbags) 흔적**: 탐색기 폴더 뷰 제어 목적의 윈도우 내부 레지스트리 구조와 데이터 영속 원리를 이해합니다.
* **사용자 행위 포렌식**: 외장 디바이스의 마운트 유무를 넘어 실제 폴더 접속 및 경로 이동 이력을 저수준 바이너리 파싱으로 규명하는 절차를 체계화합니다.

---
title: 악성 바로가기 파일의 비밀 (Malicious LNK Link File Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, lnk, windows, shortcut, powershell, base64]
confidence: high
---

# 악성 바로가기 파일의 비밀 (Malicious LNK Link File Analysis)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 악성 문서 및 바로가기 포렌식 (Windows LNK Shortcut 메타데이터 분석)

## 1. 배경 시나리오
사내 경리 부서 직원이 협력사로부터 수신한 대금 결제 요청 이메일의 첨부 파일 `invoice.pdf.lnk`를 더블 클릭하여 실행한 뒤, 화면에 피싱 경고가 나타나며 PC가 악성코드에 감염되었습니다. 이 파일은 겉보기에는 PDF 아이콘을 사용해 정상 문서로 위장했으나, 실제로는 특정 악성 행위 코드를 숨겨 놓은 윈도우 바로가기(LNK) 파일로 확인되었습니다. 이 바로가기 파일이 실제 백그라운드에서 구동한 **악성 명령어 원본**을 추출하고 내부에 인코딩되어 숨겨진 플래그를 찾아야 합니다.

## 2. 제공 파일
* `invoice.pdf.lnk` (윈도우 단축키/바로가기 형식으로 위장된 LNK 파일)

## 3. 문제 목표
윈도우 LNK 바로가기 파일의 셸 링크 바이너리 명세 구조를 이해하고, LNK 메타데이터 분석 도구(LECmd, lnkparse 등) 또는 터미널 필터링 명령어를 사용하여 실제 호출 대상 경로(Target Path) 및 전달 인자(Arguments) 값을 읽어내어 Base64 인코딩 페이로드 뒤에 숨겨진 플래그 값을 획득합니다.

## 4. 의도한 풀이 흐름
1. **아티팩트 특성 진단**:
   * 리눅스 터미널에서 `file invoice.pdf.lnk` 명령을 수행하여 해당 파일이 단순 문서가 아닌 `MS Windows shortcut` 형식임을 검증합니다.
2. **LNK 파일 파싱**:
   * **Linux CLI 환경**: `lnkparse` 도구(파이썬 패키지) 또는 `strings` 유틸리티를 사용하여 텍스트 가독 영역을 검출합니다:
     ```bash
     lnkparse invoice.pdf.lnk
     ```
   * **Windows GUI/CLI 환경**: Eric Zimmerman의 `LECmd.exe` 유틸리티를 사용해 분석 보고서를 출력합니다:
     `LECmd.exe -f invoice.pdf.lnk --csv .`
3. **타깃 실행 속성 확인**:
   * 분석된 메타데이터 결과창에서 **Local Path** 또는 **Command Line Arguments** 속성을 조회합니다.
   * 공격자가 다음과 같은 우회 파워셸 명령어를 삽입해 두었음을 식별합니다:
     `powershell.exe -windowstyle hidden -noprofile -executionpolicy bypass -command "echo cGljb0NURntsbmtfZmlsZV9iYWNrZG9vcl9kZXRlY3RlZH0= | base64 -d"`
4. **Base64 페이로드 디코딩**:
   * 명령어의 매개변수 뒤편에 자리한 Base64 인코딩 문자열(`cGljb0NURntsbmtfZmlsZV9iYWNrZG9vcl9kZXRlY3RlZH0=`)을 확보합니다.
   * 디코딩 연산을 통해 플래그 문자열을 도출합니다:
     `picoCTF{lnk_file_backdoor_detected}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{lnk_file_backdoor_detected}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 윈도우 바탕화면에서 마우스 우클릭 -> `새로 만들기` -> `바로가기`를 선택합니다.
  2. 항목 위치 입력 창에 실행 대상 명령어 인자를 주입합니다:
     `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -windowstyle hidden -NoProfile -ExecutionPolicy Bypass -Command "echo cGljb0NURntsbmtfZmlsZV9iYWNrZG9vcl9kZXRlY3RlZH0= | base64 -d"`
  3. 생성된 바로가기 파일의 이름을 `invoice.pdf.lnk`로 변경합니다.
  4. 파일 속성에 들어가 아이콘 변경 버튼을 누르고, `shell32.dll` 또는 기타 라이브러리에서 PDF 모양의 아이콘을 선택하여 시각적 위장을 보강합니다.
  5. 완성된 LNK 파일을 압축하여 배포합니다.
* **출제 포인트**: 
  * 초기 침투 단계에서 가장 빈번하게 오용되는 LNK 기반 악성코드 전달 흔적(LNK Forensics) 조사 프로세스를 정형화하고, 윈도우 탐색기 창이 사용자에게 실제 속성을 숨겨주는 트릭을 간파하도록 지도합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 윈도우 환경에서 LNK 파일 명세가 보이지 않고 자꾸 윈도우 시스템 내부에서 단축키 링크 동작만 수행합니다.**
  * A. 윈도우 탐색기는 LNK 확장자를 가진 파일의 확장자 보기를 허용하지 않고 강제로 링크 대상을 직접 실행해 주려 합니다. 파일을 포렌식 분석하기 위해서는 헥스 에디터를 실행한 뒤 해당 편집기 창 내부로 바로가기 파일을 직접 드래그 앤 드롭하여 로드해야 우회 조사가 가능합니다.
* **Q. LNK 메타데이터에서 원본 실행 경로 외에 다른 중요한 조사 단서도 나오나요?**
  * A. 네, LNK 파일 내부에는 바로가기 파일이 최초 작성된 용의자 PC의 **네트워크 MAC 주소(LinkInfo)**, 볼륨 일련번호(Volume Serial Number), 원본 실행 시각 메타데이터가 바이너리 구조 내에 깊숙이 저장되어 있어 시스템 식별용 보조 증거로 매우 가치 있습니다.

## 8. 학습 포인트
* **LNK 단축 링크 구조**: 윈도우 바로가기(LNK) 파일 구조 명세와 셸 링크 바이너리 포맷(Shell Link Binary Format)의 메타데이터 블록 구성을 학습합니다.
* **난독화 우회 명령어 탐지**: 파워셸의 인코딩 명령 실행 매개변수(-EncodedCommand 또는 우회 인자)의 성격을 이해하고, 이를 정적 텍스트 카빙으로 분리해 복구해 내는 기본 침해 추적 기법을 훈련합니다.

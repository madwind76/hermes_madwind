---
title: 숨겨진 슬라이드의 비밀 (Behind the Slides)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, office, pptx, zip, base64]
confidence: high
---

# 숨겨진 슬라이드의 비밀 (Behind the Slides)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: `MacroHard WeakEdge` (picoCTF 2021)

## 1. 배경 시나리오
모 정보기술 업체의 영업 담당자가 경쟁사로 비공개 세미나 자료인 `presentation.pptx` 발표 자료를 공유한 의심 내역을 발견했습니다. 해당 프레젠테이션 파일을 파워포인트로 열어 보면 평범한 3장짜리 슬라이드 내용만 담겨 있고 특이점이 없습니다. 하지만 정보보호 팀은 공격자가 파워포인트 파일 포맷의 구조적 틈새를 이용하여 파일 깊숙이 중요 코드와 플래그 조각을 은닉해 두었을 것으로 추정하고 있습니다.

## 2. 제공 파일
* `presentation.pptx` (일반적인 MS PowerPoint 발표 자료 파일)

## 3. 문제 목표
OpenXML 오피스 파일 포맷(.pptx)의 물리적 구조가 ZIP 압축 포맷이라는 사실을 기반으로, 아카이브를 해제하여 내부 구조를 분석하고 숨겨져 있는 은닉 데이터(Base64 인코딩)를 추출 및 디코딩하여 플래그를 찾아냅니다.

## 4. 의도한 풀이 흐름
1. **오피스 포맷 이해**: MS 오피스 파일(docx, pptx, xlsx)은 실제 내부적으로 여러 XML 파일과 미디어 파일을 결합한 **ZIP 파일 포맷**임을 인지합니다.
2. **압축 해제**:
   * 리눅스 터미널에서 `unzip presentation.pptx -d pptx_content` 명령을 수행하여 파일의 디렉터리 구조를 확장합니다.
   * 윈도우 환경인 경우 확장자를 `.pptx`에서 `.zip`으로 변경한 뒤 압축 풀기 기능을 활용합니다.
3. **디렉터리 내부 탐색**:
   * 생성된 `pptx_content/` 폴더 내의 파일 구조를 살핍니다.
   * `ppt/slides/`, `ppt/slideLayouts/`, `ppt/media/` 등의 하위 경로를 조사합니다.
   * 특히, 원래 표준 프레젠테이션 구조에는 수록되지 않는 임의의 텍스트 파일(예: `ppt/slideMasters/hidden` 또는 `ppt/slides/_rels/hidden.txt`)이 삽입되어 있는지 확인합니다.
4. **Base64 디코딩**:
   * 은닉된 텍스트 파일의 내용을 읽어 들입니다. 공백이나 엔터 없이 인코딩된 문자열(예: `cGljb0NURntwcHR4X3N0cnVjdHVyZV9leHBsb3JlZH0=`)을 획득합니다.
   * 터미널 명령어 또는 CyberChef를 사용하여 디코딩합니다.
     `echo "cGljb0NURntwcHR4X3N0cnVjdHVyZV9leHBsb3JlZH0=" | base64 -d`
5. **결과 확인**: 복구된 원본 플래그 값을 획득합니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{pptx_structure_explored}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 아무 내용이나 채운 2~3슬라이드짜리 PowerPoint 파일 `temp.pptx`를 생성합니다.
  2. 리눅스 환경에서 `unzip temp.pptx -d ppt_temp`로 구조를 풀어냅니다.
  3. `ppt/slideMasters/` 혹은 하위 XML 관계 정의 폴더 안에 임의의 파일 `hidden`을 만들어 플래그의 Base64 인코딩 값을 저장합니다:
     `echo -n "picoCTF{pptx_structure_explored}" | base64 > ppt_temp/ppt/slideMasters/hidden`
  4. 수정된 내부 파일 목록 전체를 다시 zip으로 패킹합니다:
     `cd ppt_temp; zip -r ../presentation.pptx *`
  5. 윈도우 파워포인트로 최종 `presentation.pptx`가 깨짐 없이 정상적으로 파일 실행이 되는지 재검증합니다.
* **출제 포인트**: 
  * OpenXML 계열 파일의 숨겨진 물리적 구조를 탐색하는 포렌식 기본 분석 역량을 배양하고, 매크로 파일에 숨겨지는 악성 스크립트 카빙의 원리를 터득합니다.

## 7. 트러블슈팅 및 힌트
* **Q. zip으로 다시 압축했는데 파워포인트에서 "손상된 파일"이라며 파일이 열리지 않습니다.**
  * A. 압축 시 `ppt_temp/` 최상위 폴더 자체를 압축하면 경로 기준이 어긋나 에러가 납니다. 반드시 `ppt_temp/` 내부의 파일들이 있는 곳으로 이동한 후 `zip -r ../presentation.pptx *`와 같이 하위 경로 구조를 보존하여 압축을 실행하십시오.
* **Q. strings 명령어로 한 번에 base64 스트링을 찾을 순 없나요?**
  * A. `strings presentation.pptx | grep -E "[A-Za-z0-9+/]{30,}"` 과 같은 정규식을 돌려 시도할 수 있으나, 압축 컨테이너 파일 포맷 상 텍스트 조각들이 쪼개져 있어 보이지 않는 경우가 많아 압축을 풀어 확인하는 정공법이 가장 신뢰도 높습니다.

## 8. 학습 포인트
* **OpenXML 아카이브 분석**: 현대 오피스 문서 파일 구조가 ZIP 컨테이너 방식임을 파악하고, 그 내부에 비표준 파일(Out-of-band files)을 심어 데이터 유출 경로로 사용할 수 있는 취약점을 학습합니다.
* **이중 구조 분석**: 애플리케이션 수준의 뷰어가 렌더링에 필요한 필수 매핑 XML을 참조하여 화면을 구성하므로, 매핑에 정의되지 않은 은닉 정보는 파워포인트 화면에 뜨지 않는다는 구조적 정보 은닉 기법을 터득합니다.

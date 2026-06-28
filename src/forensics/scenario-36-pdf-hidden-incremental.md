---
title: 변조된 PDF 속의 숨겨진 스트림 (PDF Hidden Incremental Update)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, pdf, pdf-parser, incremental-update, revision, flatedecode]
confidence: high
---

# 변조된 PDF 속의 숨겨진 스트림 (PDF Hidden Incremental Update)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: PDF 원시 구조 복원 및 숨겨진 스트림 분석 (PDF 증분 업데이트 아티팩트 카빙)

## 1. 배경 시나리오
보안 컴플라이언스 감사 중 배포용 대외 보고서 `corporate_policy.pdf` 파일 내에서 중요 기밀 플래그가 고의로 편집되어 마스킹/삭제되었다는 첩보를 입수했습니다. PDF 리더 프로그램으로 열었을 때는 삭제 완료되어 정상 문구만 가독되나, PDF 명세의 독특한 기능인 **증분 업데이트(Incremental Update)** 정책으로 인해 파일 뒷부분에 추가 오브젝트만 덧붙여졌을 뿐, 앞단에 존재하던 과거 버전의 원본 본문 텍스트 오브젝트는 여전히 파일 내에 압축 보존되어 삭제되지 않은 채 방치되어 있었습니다. PDF의 내부 물리 오브젝트 이력을 추적하여 **이전 리비전에 숨겨져 있던 플래그**를 색인해야 합니다.

## 2. 제공 파일
* `corporate_policy.pdf` (증분 업데이트로 편집 이력이 지워지지 않은 채 보존된 PDF 문서 파일)

## 3. 문제 목표
PDF 문서의 증분 업데이트(xref 테이블 및 trailer 추가 구조) 메커니즘을 파악하고, 여러 차례 저장되어 존재하는 `%%EOF` 마커 경계를 기반으로 이전 리비전의 객체를 분리한 뒤, 압축 스트림(`FlateDecode`) 데이터를 파싱 및 복원하여 플래그를 카빙합니다.

## 4. 의도한 풀이 흐름
1. **증분 업데이트 횟수 진단**:
   * 제공된 `corporate_policy.pdf` 파일을 텍스트 뷰어로 열거나 셸에서 `%%EOF` 문자열의 개수를 카운트합니다:
     ```bash
     grep -a "%%EOF" corporate_policy.pdf
     ```
   * 일반적으로 PDF는 단 한 번 저장되었을 때 파일 맨 끝에 `%%EOF`가 단 한 번 기록됩니다. 본 파일에서는 2개 이상의 `%%EOF` 마커가 검출되어 여러 버전으로 덮어쓰기 저장(Incremental Update)되었음이 증명됩니다.
2. **구버전 오브젝트 식별 (pdf-parser 활용)**:
   * Didier Stevens의 `pdf-parser.py` 도구를 사용하여 PDF 파일의 내부 오브젝트 레이아웃을 파악합니다:
     `pdf-parser.py corporate_policy.pdf`
   * 각 오브젝트 중 내용 변경을 위해 상위 리비전에서 오버라이드되기 전, 하위 리비전 영역에만 존재하는 원시 텍스트 스트림 오브젝트(예: `Object 8`)를 탐색합니다.
3. **압축 해제 및 플래그 복구**:
   * `Object 8` 내부를 보면 `/Filter /FlateDecode` 메타데이터와 함께 본문 바이너리 스트림이 저장되어 있습니다.
   * `pdf-parser.py`의 필터 해제 옵션(`-f`)을 기입해 해당 개별 오브젝트 번호를 타깃으로 압축을 해제합니다:
     ```bash
     pdf-parser.py -o 8 -f corporate_policy.pdf
     ```
   * 해제된 텍스트 출력 결과 하단에서 이전 리비전에 존재했던 원본 텍스트 내에 감춰져 있던 플래그 문자열을 발견합니다:
     `picoCTF{pdf_incr3m3nt4l_upd4t3_rev1s1on}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{pdf_incr3m3nt4l_upd4t3_rev1s1on}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 텍스트 `picoCTF{pdf_incr3m3nt4l_upd4t3_rev1s1on}`를 본문에 명시한 간단한 PDF 파일을 임의의 도구(예: LibreOffice Writer 등)를 이용해 1차 저장합니다 (예: `step1.pdf`).
  2. PDF 편집기(예: Adobe Acrobat 또는 PDFescape 등)로 `step1.pdf` 파일을 엽니다.
  3. 플래그가 들어 있는 텍스트 상자를 삭제하거나 완전히 덮어쓰는 대체 일반 문장을 입력한 뒤, **"새 이름으로 저장"이 아닌 "저장(Save)" 버튼을 눌러 증분 저장**을 유도합니다.
  4. 저장 완료된 최종 파일 내부 구조를 헥스 에디터로 보아, 두 번째 `xref` 및 `%%EOF`가 이전 `%%EOF` 아래에 덧붙여진 구조인지 교차 확인한 후 배포합니다.
* **출제 포인트**: 
  * PDF 문서를 편집한 뒤 덮어쓰기 저장 시, 내부 구조상 파일 전체를 재작성하지 않고 새로운 변경 정보만 테일에 추가하는 증분 구조의 특성과 그로 인한 정보 유출 위협(Incremental Update Leaks) 분석 능력을 배양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. pdf-parser 도구가 설치되어 있지 않습니다.**
  * A. `pdf-parser.py`는 단일 파이썬 파일로 구성되어 있어 깃허브 등에서 내려받아 즉시 사용이 가능합니다. 이 도구가 없다면 파이썬의 표준 `zlib` 라이브러리를 활용해, 헥스 에디터 상에서 `stream`과 `endstream` 사이의 바이너리 바이트 블록만 잘라내어 `zlib.decompress(data, -15)` 함수를 직접 구동시키는 스크립트를 작성하여 복구할 수도 있습니다.
* **Q. 모든 PDF 편집본에서 구버전 데이터가 남게 되나요?**
  * A. 아닙니다. 편집 도구에서 "새 이름으로 저장(Save As)"을 수행하게 되면 PDF 엔진은 불필요한 구버전 오브젝트와 끊어진 참조들을 완전히 소거하고 최종 리비전 레이아웃으로 전체 바이트를 재구성하여 기록하므로 증분 이력이 모두 휘발됩니다.

## 8. 학습 포인트
* **PDF 문서 구조**: 카탈로그, 페이지 트리, 개별 리소스 객체들로 이루어진 개체 지향 문서 명세를 이해합니다.
* **증분 업데이트(Incremental Update) 포렌식**: 덮어쓰기 저장 이력에 남겨지는 가비지 오브젝트 역추적을 통해, 안티 포렌식 위협을 극복하고 과거 삭제된 텍스트 원형을 발굴하는 기술을 체계화합니다.

---
title: ext4 저널링 기반 삭제된 PDF 스트림 카빙 복구 (ext4 Journal PDF Carving)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, disk, ext4, journal, pdf-carving, file-recovery, binwalk, foremost]
confidence: high
---

# ext4 저널링 기반 삭제된 PDF 스트림 카빙 복구 (ext4 Journal PDF Carving)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 삭제된 PDF 문서 저널 물리 카빙 복구 (ext4 Journal PDF Carving)

## 1. 배경 시나리오
공격자가 기밀 설계도 자료가 기록된 PDF 문서 파일을 유출한 뒤, 흔적을 지우기 위해 리눅스 볼륨 내에서 해당 문서를 완전 삭제(`rm -f sensitive.pdf`)했습니다. 디바이스 파일시스템이 ext4 규격인 탓에 삭제 즉시 Inode의 블록 매핑 정보가 완전 초기화되어 복구 유틸리티로는 무의미한 상태입니다. 그러나 해당 볼륨은 데이터 트랜잭션을 실시간 직렬화해 디스크에 기록하는 **저널링(JBD2)** 기법이 활성화되어 있었으므로, 삭제되기 직전 쓰기 트랜잭션 도중 저널 영역으로 일시 백업되었던 원본 PDF 바이너리 블록들이 고스란히 남아 있을 확률이 높습니다. 적출한 저널링 디바이스 원시 이미지 `ext4_journal_pdf.bin`을 분석하여 **삭제된 PDF 문서를 물리 카빙으로 정상 구출해 내고 본문 속의 플래그**를 획득하십시오.

## 2. 제공 파일
* `ext4_journal_pdf.bin` (피해 시스템 ext4 파일시스템의 저널 데이터 블록 전체를 통째로 덤프한 이진 이미지 파일)

## 3. 문제 목표
리눅스 ext4 저널 디바이스(Inode 8) 트랜잭션 기록 블록 내에 파일 데이터 조각이 평문 이진 스트림으로 잔재하는 아키텍처 원리를 배웁니다. 더불어 PDF 파일 포맷 표준 규격(시작 지시자 `%PDF-` 및 최종 종단 마커 `%%EOF` 매직 코드 구조)을 이용하여 수동 카빙 및 무결성 복구 기법을 마스터합니다.

## 4. 의도한 풀이 흐름
1. **바이너리 매직 헤더 스캔**:
   * 제공된 `ext4_journal_pdf.bin` 파일에 PDF 포맷 조각이 실재하는지 확인하기 위해 파일 카빙 분석 도구인 `binwalk`를 가동하여 정적 시그니처 맵을 탐지합니다:
     ```bash
     binwalk ext4_journal_pdf.bin
     ```
   * 분석 결과, 바이너리 중간 특정 오프셋 대역에서 PDF 파일의 시작 매직 시그니처인 **`%PDF-`** (`25 50 44 46 2D`)가 감지됨을 인지합니다.
2. **PDF 문서 물리 카빙 (Carving)**:
   * **도구 활용**: `foremost` 또는 `binwalk` 자동 적출 옵션을 사용해 저널 바이너리 내부에서 PDF 파일을 파싱해 분리합니다:
     ```bash
     binwalk -e ext4_journal_pdf.bin
     ```
     또는
     ```bash
     foremost -t pdf -i ext4_journal_pdf.bin -o output_dir
     ```
   * **수동 카빙**: 헥스 에디터로 저널 이미지를 엽니다. `%PDF-` (오프셋 시작점)부터 PDF 파일의 유효 종단을 지정하는 매직 마커인 **`%%EOF`** (`25 25 45 4F 46`) 문자열이 나타나는 마지막 오프셋(및 바로 뒤 개행문자 바이트)까지를 드래그 선택하여 `sensitive_rebuilt.pdf` 파일로 저장합니다.
3. **PDF 본문 분석 및 플래그 획득**:
   * 복구된 `sensitive_rebuilt.pdf` 문서를 PDF 리더나 웹 브라우저를 통해 실행하여 화면 본문을 관찰합니다.
   * 또는 텍스트 적출 도구인 `pdftotext`를 이용하여 텍스트 레이어를 출력 추출합니다:
     ```bash
     pdftotext sensitive_rebuilt.pdf output.txt
     cat output.txt
     ```
   * 출력된 텍스트 페이지 본문 속에 숨겨져 있던 최종 플래그 문자열을 확보합니다:
     `picoCTF{ext4_journ4l_pdf_stream_carv3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{ext4_journ4l_pdf_stream_carv3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 텍스트 `picoCTF{ext4_journ4l_pdf_stream_carv3d}`를 담고 있는 표준 PDF 문서를 작성하여 `sensitive.pdf`로 내보냅니다.
  2. 테스트 ext4 파티션에 마운트하여 해당 `sensitive.pdf` 파일을 라이트 적재하고, 디스크 동기화(`sync`)를 통해 저널 트랜잭션 블록에 PDF 데이터 전체가 완벽히 로깅 수립되도록 보장합니다.
  3. 파일을 강제 삭제합니다: `rm -f sensitive.pdf; sync`
  4. `debugfs` 도구를 연동해 저널 영역(8번 Inode)의 물리 이미지 `ext4_journal_pdf.bin`을 바이너리로 추출합니다.
  5. 덤프된 저널 내부에서 `%PDF-` 헤더와 `%%EOF` 종단 마커 사이의 스트림 세그먼트가 물리적으로 온전하게 보존되어 PDF 렌더링에 성공하는지 검증을 마친 후 문제 파일로 유포합니다.
* **출제 포인트**: 
  * Inode 테이블 매핑 인덱스가 통째로 소멸되는 리눅스 안티 포렌식(Anti-Forensics) 삭제 행위 직면 시, 시스템 저널링 버퍼(JBD2 Inode 8 Data Block) 트랜잭션 영역을 정적 스캔하고, 파일 포맷 고유 매직 헤더 규칙을 매핑해 유실 데이터를 완벽하게 구출해 내는 고급 디스크 분석론을 검증합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 카빙한 PDF가 "손상된 파일" 에러를 내며 열리지 않습니다.**
  * A. PDF 사양은 xref(크로스 레퍼런스 테이블) 및 스트림 오프셋 구조에 극도로 민감합니다. 저널 영역에서 데이터를 수동 카빙할 때, 시작 시그니처 `%PDF-` 이전 영역에 불필요한 저널 메타데이터 바이트가 일부 포함되었거나, 파일 끝부분 `%%EOF` 마커 뒤의 바이트 정렬이 무너졌을 때 리더 에러가 발생합니다. 이 경우 파일의 시작을 정확히 `%PDF-`의 첫 바이트(`0x25`)로 고정하고, 끝을 `%%EOF` 마커 부근으로 정확히 재재단하여 패칭해야 합니다.
* **Q. pdftotext 도구가 에러를 냅니다. 다른 해독법이 있나요?**
  * A. PDF 렌더링 엔진 오프셋이 일부 깨졌을 경우에도, PDF 본문 스트림은 내부적으로 `FlateDecode` (zlib 디플레이트) 압축 방식으로 각 오브젝트 단위로 파편 보존됩니다. 따라서 `zlib` 스트림 헤더 시그니처(`78 9C` 등)를 기반으로 바이너리 내의 압축 데이터 영역들만 개별 추출하여 zlib 해제 명령(`python -c "import zlib; print(zlib.decompress(...))"`)을 순차 대입하면, 이미지 깨짐과 무관하게 내부 평문 텍스트 스트림만 가독성 있게 뜯어낼 수 있습니다.

## 8. 학습 포인트
* **PDF 포맷 아키텍처 스펙**: 파일 헤더, 바디 오브젝트 구조, xref 테이블, 및 최종 종단 마커(%%EOF)의 정렬 특성을 학습합니다.
* **저널링(Journaling) 기반 데이터 카빙**: ext4/ext3 파일시스템의 백그라운드 트랜잭션 링 버퍼 명세를 파헤쳐, 흔적 삭제 우회 기법의 한계를 극복하는 실전 복구 노하우를 갖춥니다.

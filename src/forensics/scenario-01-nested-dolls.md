---
title: 다층 포장 인형 (Nested Dolls)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, stego, image, archive]
confidence: high
---

# 다층 포장 인형 (Nested Dolls)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: `Matryoshka doll` (picoCTF 2021)

## 1. 배경 시나리오
사이버 수사대에서 기밀 유출 혐의를 받고 있는 용의자의 외장 드라이브를 분석하던 중, 바탕화면에서 평범한 인형 사진인 `mystery_doll.png`를 발견했습니다. 하지만 용의자의 웹 브라우저 검색 기록에는 "파일 숨기기", "바이너리 병합"과 같은 단어들이 발견되어, 이 이미지 내부에 기밀 플래그가 은밀히 숨겨져 있을 가능성이 제기되었습니다.

## 2. 제공 파일
* `mystery_doll.png` (약 2.4MB, 용의자 PC에서 회수된 PNG 이미지 파일)

## 3. 문제 목표
이미지 파일 내부에 결합되어 숨겨져 있는 다층 구조의 아카이브 파일을 순차적으로 추출하고 해제하여 최종 경로에 위치한 플래그 값을 획득합니다.

## 4. 의도한 풀이 흐름
1. **기본 분석**: `file` 명령어로 제공된 파일의 형식을 확인하고, `strings` 또는 `exiftool`을 활용해 메타데이터에 이상 징후가 있는지 점검합니다.
2. **파일 은닉 검사**: `binwalk mystery_doll.png` 명령을 실행하여 PNG 이미지 파일의 끝에 압축 파일(ZIP)이 병합되어 있는지 식별합니다.
3. **1차 추출**: `binwalk -e mystery_doll.png` 또는 `foremost mystery_doll.png` 명령을 이용해 숨겨진 ZIP 아카이브를 추출합니다.
4. **다단계 아카이브 해제**:
   * 추출된 ZIP 파일 내부에서 `base_doll.png`를 획득합니다.
   * `binwalk base_doll.png`로 내부에 또 다른 ZIP이 있음을 파악하고 다시 추출합니다.
   * 이 과정을 총 3~4회 반복하여 `inner_doll/secret/flag.txt` 경로까지 도달합니다.
5. **플래그 확인**: 최종 추출된 `flag.txt`를 열어 플래그를 확인합니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{n3st3d_d0lls_4re_fun}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 최종 플래그 파일 `flag.txt`를 작성합니다. (예: `picoCTF{n3st3d_d0lls_4re_fun}`)
  2. `flag.txt`를 포함하는 `secret` 디렉터리를 `inner_doll.zip`으로 압축합니다.
  3. 임의의 인형 이미지 `doll_level3.png`에 `cat doll_level3.png inner_doll.zip > doll_level3_combined.png` 형태로 바이너리를 병합합니다.
  4. 이 결합된 이미지를 다시 `mid_doll.zip`으로 압축하고, `doll_level2.png`와 병합합니다.
  5. 최종적으로 `mystery_doll.png`가 최상위 파일이 되도록 3~4회 중첩 구조를 만듭니다.
* **출제 포인트**: 
  * 파일 카빙(File Carving)의 개념을 이해하고, 리눅스 도구 `binwalk`의 자동 추출 기능(`-e`) 혹은 `foremost`를 실습할 수 있도록 난이도를 낮게 유지합니다.
  * 아카이브에 별도의 비밀번호를 설정하지 않아 도구 사용법만 알면 쉽게 풀 수 있게 유도합니다.

## 7. 트러블슈팅 및 힌트
* **Q. binwalk 추출이 작동하지 않거나 폴더가 비어 있습니다.**
  * A. 파이썬 의존성 문제로 인해 자동 추출이 실패할 수 있습니다. 이 경우 `dd` 명령어를 사용하여 시그니처 시작 오프셋을 지정해 수동으로 잘라내거나, `foremost` 도구를 대안으로 사용하십시오.
* **Q. 압축을 풀었는데 또 이미지가 나옵니다. 잘못 푼 건가요?**
  * A. 러시아 인형(마트료시카)처럼 이미지 안에 압축 파일, 그 압축 파일 안에 또 이미지가 연속적으로 들어 있는 구조가 의도되어 있습니다. 끝까지 분석해 보세요.

## 8. 학습 포인트
* **파일 시그니처(File Signature)**: 파일의 매직 바이트(Magic Bytes)를 확인하고 여러 파일이 하나로 병합되어 있을 때 이를 분리하는 원리를 배웁니다.
* **도구 활용**: 디지털 포렌식에서 정밀 분석 전 아티팩트를 자동 분류 및 추출해 주는 `binwalk` 및 `foremost` 도구의 기본 동작을 학습합니다.

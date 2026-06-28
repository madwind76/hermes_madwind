---
title: 변조된 오피스 문서 매크로 해독 (VBA Macro Deobfuscation)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, office, excel, vba, macro, oletools, xor]
confidence: high
---

# 변조된 오피스 문서 매크로 해독 (VBA Macro Deobfuscation)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 악성 오피스 매크로 탐지 및 디비깅 (Excel xlsm VBA 난독화 해제)

## 1. 배경 시나리오
사내 구매 팀 직원이 거래처로부터 청구서 내역서라며 전송받은 엑셀 매크로 문서 `invoice_details.xlsm` 파일을 열고 매크로 실행 경고창에서 "콘텐츠 사용"을 눌렀습니다. 직후 백그라운드에서 악성 페이로드가 구동되었습니다. 조사 팀은 해당 엑셀 파일을 격리 확보했습니다. 용의자는 이 문서 내부의 VBA(Visual Basic for Applications) 매크로 모듈에 원격 공격을 수행하는 다운로더 코드를 심고, 탐지를 방해하기 위해 코드를 조각조각 쪼개고 XOR 연산으로 난독화해 두었습니다. 매크로 코드를 분석해 **악성 파일이 내려받아진 C2 서버 주소 내에 은닉된 플래그**를 알아내야 합니다.

## 2. 제공 파일
* `invoice_details.xlsm` (악성 VBA 매크로가 수록되어 유포된 Excel 통합 문서 파일)

## 3. 문제 목표
오피스 OLE(Object Linking and Embedding) 구조 및 VBA 매크로 보존 규칙을 이해하고, 정적 분석 도구(`oletools` 패키지의 `olevba` 등)를 사용하여 엑셀 내부의 매크로 모듈 소스코드를 추출하고, 코드 내의 XOR 복호화 알고리즘을 분석해 은닉 데이터를 복원합니다.

## 4. 의도한 풀이 흐름
1. **매크로 코드 정적 추출 (oletools 활용)**:
   * 리눅스 터미널에서 `olevba` 도구를 사용하여 엑셀 파일 내에 삽입된 VBA 매크로를 추출하고 의심 요소를 정밀 스캔합니다:
     ```bash
     olevba invoice_details.xlsm
     ```
   * 분석 결과 출력물 최하단의 요약(Summary) 테이블에서 `AutoExec` 속성 및 실행 명령어 레지스트리 호출 경고 등을 확인합니다.
2. **VBA 소스코드 난독화 역공학**:
   * 추출된 VBA 코드 본문을 분석합니다.
   * 소스 내부에서 다음과 같은 XOR 복호화 함수와 인코딩된 바이트 배열을 식별합니다:
     ```vba
     Sub Document_Open()
         Dim encArray As Variant
         encArray = Array(120, 115, 111, 123, 119, 104, 98, ... [중략])
         Dim key As Integer
         key = 13
         Dim decoded As String
         For i = LBound(encArray) To UBound(encArray)
             decoded = decoded & Chr(encArray(i) Xor key)
         Next i
         ' ... [이후 특정 쉘 실행 코드가 존재함]
     End Sub
     ```
3. **바이트 배열 복호화 수행**:
   * 찾아낸 10진수 바이트 배열을 XOR 키 `13` (0x0D)을 사용하여 복호화합니다.
   * **Python 스크립트 작성**:
     ```python
     enc = [120, 115, 111, 123, 119, 104, 98, ...] # encArray 복사
     key = 13
     print("".join([chr(b ^ key) for b in enc]))
     ```
   * **CyberChef 활용**:
     * 바이트 배열 값을 헥스 또는 스페이스 구분 텍스트 형태로 변환하여 Input에 입력합니다.
     * `XOR` 레시피를 배치하고 Key 값을 `13` (HEX의 경우 `0d` 혹은 Decimal `13`)으로 설정해 해독합니다.
4. **최종 플래그 확보**:
   * 복구된 문자열(예: `http://malicious-c2.net/picoCTF{vba_m4cro_decrypted_successfully}`)에서 플래그를 추출합니다.
     (최종 플래그: `picoCTF{vba_m4cro_decrypted_successfully}`)

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{vba_m4cro_decrypted_successfully}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 플래그가 들어간 문자열(`http://malicious-c2.net/picoCTF{vba_m4cro_decrypted_successfully}`)의 각 글자 아스키코드 값에 대해 수치 연산(XOR 13)을 가하여 인코딩된 바이트 배열을 도출합니다.
  2. MS Excel을 실행하여 새 문서를 만들고, 개발 도구(`Alt+F11`)를 눌러 VBA 에디터를 엽니다.
  3. `ThisWorkbook` 혹은 새 모듈을 생성하여 위의 복호화 스크립트 시나리오 루프를 구현합니다. 이때 실제 원격 실행 명령어는 주석 처리하거나 정상 출력 명령어(`MsgBox`)로 대체해 모의 검증 편의성을 돕습니다.
  4. 문서를 저장할 때 **Excel 매크로 사용 통합 문서(*.xlsm)** 포맷으로 명시하여 저장 및 배포합니다.
* **출제 포인트**: 
  * 이메일 침투 벡터로 오랫동안 남용되는 오피스 문서형 악성코드의 물리 구조 분석 및 OLE 분석 도구 활용 능력을 측정하고, 스크립트 난독화를 역산 복구하는 알고리즘 이해도를 높입니다.

## 7. 트러블슈팅 및 힌트
* **Q. olevba 명령 실행 시 모듈이 암호화되어 있어 코드가 깨져 보입니다.**
  * A. 피의자가 VBA 프로젝트에 비밀번호를 걸어 코드가 락인된 상황일 수 있습니다. 이럴 때는 `oledump.py` 도구를 사용하여 OLE 구조의 개별 스트림(특히 `vbaProject.bin` 하위의 스트림들)을 바이트 단위로 디 컴파일하거나, Hex 에디터로 파일 내부의 `DPB` 문자열을 수정해 강제로 비밀번호 팝업을 우회 해제하는 트릭을 병행해야 합니다.
* **Q. 파이썬 복호화 연산 중 인덱스 범위를 벗어났다는 에러가 뜹니다.**
  * A. 복사해 온 10진수 바이트 배열에 줄바꿈이나 쉼표(,) 누락이 있는지, 유효한 정수형 배열인지 검사해 문자열 조립을 재시도하십시오.

## 8. 학습 포인트
* **OLE(Object Linking and Embedding) 파일 구조**: 구조화된 저장소(Structured Storage) 명세를 지닌 고전 오피스 포맷의 스트림 배치 정책을 학습합니다.
* **VBA 매크로 정적 분석**: `oletools` 프레임워크의 도구군을 다루어 복잡한 문서 파일에서 순수 악성 스크립트 위협 요소(Autorun 트리거 등)를 빠르게 필터링해 분석하는 절차를 습득합니다.

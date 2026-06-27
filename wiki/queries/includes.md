---
title: Includes — picoCTF 2022 web note
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, research, writeup, client-side, source-analysis, decode]
sources: [https://ctftime.org/writeup/32843, https://medium.com/@Kamal_S/picoctf-web-exploitation-includes-10228bf124c8, https://github.com/FlyN-Nick/picoGymWriteups/blob/main/Web%20Exploitation/Includes/Includes.md, https://github.com/noamgariani11/picoCTF-2022-Writeup, https://github.com/arvindshima/PicoCTF-2022]
confidence: high
---

# Includes — picoCTF 2022 web note

> 페이지 소스와 참조된 정적 파일을 열어보면 flag가 부분적으로 노출되는 picoCTF 2022 Web Exploitation 문제입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/32843)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-includes-10228bf124c8)
- [Original writeup](https://github.com/FlyN-Nick/picoGymWriteups/blob/main/Web%20Exploitation/Includes/Includes.md)
- [noamgariani11/picoCTF-2022-Writeup](https://github.com/noamgariani11/picoCTF-2022-Writeup)
- [arvindshima/PicoCTF-2022](https://github.com/arvindshima/PicoCTF-2022)


## 1. 요약
- 플랫폼: picoCTF 2022
- 문제명: Includes
- 분류: client-side / source inspection
- 핵심 아이디어: HTML source, `script.js`, `style.css`에 분산된 단서를 모두 확인합니다.
- 연결 개념: [[web-inspector-ctf-patterns]], [[base64-decoding-ctf-patterns]], [[web-ctf-writeup-client-side]]

## 2. 공격면
| Route / Resource | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| main page | GET | No | browser click | popup | 버튼 클릭이지만 서버 요청이 보이지 않을 수 있음 |
| page source | GET | No | view-source | HTML | external resource 링크를 확인합니다 |
| script.js | GET | No | direct open | partial flag | flag 조각이 들어있습니다 |
| style.css | GET | No | direct open | partial flag | flag 조각이 들어있습니다 |

## 3. 가설
- 팝업과 버튼은 겉모습일 뿐, 실질적인 단서는 **HTML source**에 있습니다.
- `script.js`와 `style.css`를 각각 열면 flag가 **분할**되어 있을 가능성이 높습니다.
- 서버 취약점보다 **클라이언트 자원 노출**이 핵심일 수 있습니다.

## 4. 관찰 기록
### 시도 1
- payload: 버튼 클릭
- 관찰: 팝업만 뜨고 Burp에 새 요청이 안 보일 수 있음
- 해석: 서버 상호작용보다 로컬 JS 처리 가능성

### 시도 2
- payload: view-source 확인
- 관찰: `greetings()` 함수와 `script.js`, `style.css` 참조 발견
- 해석: 외부 정적 파일에 단서가 존재

### 시도 3
- payload: `script.js`, `style.css` 직접 열기
- 관찰: flag 조각이 각 파일에 분산
- 해석: 두 파일을 합쳐 flag를 복원

## 5. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[web-ctf-writeup-client-side]]

## 6. 회고
- 가장 먼저 페이지 소스와 정적 자원을 확인하는 습관이 중요합니다.
- UI가 단순하더라도 외부 파일에 민감 정보가 숨어 있을 수 있습니다.
- 다음에 먼저 볼 것: view-source, script, style, hidden comments, partial secrets.

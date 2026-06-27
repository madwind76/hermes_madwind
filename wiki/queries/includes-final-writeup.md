---
title: Includes — picoCTF 2022 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, client-side, source-analysis, decode, base64]
sources: [https://ctftime.org/writeup/32843, https://medium.com/@Kamal_S/picoctf-web-exploitation-includes-10228bf124c8, https://github.com/FlyN-Nick/picoGymWriteups/blob/main/Web%20Exploitation/Includes/Includes.md, https://github.com/noamgariani11/picoCTF-2022-Writeup, https://github.com/arvindshima/PicoCTF-2022]
confidence: high
---

# Includes — picoCTF 2022 web writeup

> 페이지 소스와 참조된 정적 파일을 확인하면 flag가 부분적으로 노출되는 아주 전형적인 source-inspection 문제입니다. 공격 포인트는 서버가 아니라 **브라우저가 내려받는 정적 자원**에 있습니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/32843)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-includes-10228bf124c8)
- [Original writeup](https://github.com/FlyN-Nick/picoGymWriteups/blob/main/Web%20Exploitation/Includes/Includes.md)
- [noamgariani11/picoCTF-2022-Writeup](https://github.com/noamgariani11/picoCTF-2022-Writeup)
- [arvindshima/PicoCTF-2022](https://github.com/arvindshima/PicoCTF-2022)


## 1. 한 줄 요약

`Includes`는 사용자가 보는 UI가 아니라 `view-source`와 외부 리소스(`script.js`, `style.css`)에 flag 조각이 숨겨진 문제입니다. CTFtime와 공개 writeup들은 버튼 클릭 후 팝업만 보일 뿐, 핵심은 HTML source와 정적 파일을 직접 열어보는 것이라고 설명합니다.

## 2. 문제 메타데이터

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 카테고리 | Web Exploitation |
| 문제명 | Includes |
| 핵심 유형 | [[web-inspector-ctf-patterns]] |
| 보조 개념 | [[base64-decoding-ctf-patterns]] |
| 난이도 | Easy / 100 points로 공개 writeup들에서 언급 |
| 재사용 패턴 | source inspection → static asset discovery → 분할된 flag 조각 복원 |

## 3. 공격면

| 요소 | 관찰 |
|------|------|
| UI 버튼 | `Say hello` 클릭 시 팝업만 뜸 |
| 네트워크 | Burp history에 새 요청이 안 보일 수 있음 |
| HTML source | `greetings()` 함수와 정적 리소스 링크가 노출됨 |
| script.js | flag 일부가 포함됨 |
| style.css | flag 나머지 일부가 포함됨 |

## 4. 풀이 흐름

### 4.1 단서 확인

Medium writeup과 CTFtime writeup 모두 **page source를 확인하라**는 점을 강조합니다. 팝업이 뜨더라도 네트워크 요청이 없거나 별다른 서버 반응이 없다면, 먼저 HTML source와 외부 파일을 보는 것이 맞습니다.

### 4.2 소스와 정적 자원 열기

브라우저에서 `view-source:`를 통해 HTML을 열어보면 `greetings()` 함수와 함께 아래 파일들을 확인할 수 있습니다.

- `script.js`
- `style.css`

이 두 파일을 직접 열면 flag가 **반씩 나뉘어** 들어있습니다. 공개 writeup들은 이를 합치면 최종 flag가 완성된다고 설명합니다.

### 4.3 복원 포인트

이 문제는 base64처럼 복잡한 암호화보다는, **분산된 문자열을 찾고 합치는 작업**에 가깝습니다. 다만 CTF 노트 관점에서는 어떤 문자열이 base64처럼 보일 경우 `base64-decoding` 습관을 함께 떠올릴 수 있습니다.

## 5. 핵심 개념 분리

이 문제에서 재사용 가능한 개념은 다음과 같습니다.

- [[web-inspector-ctf-patterns]] — page source / devtools / static asset inspection
- [[base64-decoding-ctf-patterns]] — 문자열이 인코딩처럼 보일 때 빠르게 확인할 수 있는 보조 습관
- [[web-ctf-writeup-client-side]] — client-side 분류 허브

## 6. 방어 관점

1. HTML source, JS, CSS에 민감 정보를 넣지 않습니다.
2. 클라이언트 자원은 공개된다는 전제로 설계합니다.
3. 민감한 문자열은 서버에서 조건에 맞게 생성하더라도 클라이언트에 그대로 노출하지 않습니다.
4. 버튼 클릭이나 UI 요소만으로 보안이 지켜질 것이라고 가정하지 않습니다.

## 7. 동일 계열 문제 체크리스트

- [ ] view-source를 먼저 확인했는가?
- [ ] 외부 JS/CSS 파일을 열어보았는가?
- [ ] HTML 주석이나 숨겨진 함수가 있는가?
- [ ] 네트워크 요청이 보이지 않아도 클라이언트 자원이 더 있는가?
- [ ] 문자열이 분산되어 있거나 이어 붙여야 하는가?

## 8. 출처별 교차 확인

| 출처 | 확인한 내용 |
|------|-------------|
| CTFtime writeup 32843 | HTML source와 `script.js`/`style.css`에 flag 조각이 존재 |
| Kamal S Medium | `greetings()` 함수, 팝업, 정적 파일 직접 열기 흐름 |
| FlyN-Nick GitHub writeup | Includes의 공식적인 풀이 흐름과 flag 조각 분리 |
| noamgariani11 / arvindshima repos | picoCTF 2022 Web Exploitation 아카이브에 Includes 포함 |

## 9. 관련 페이지

- [[includes]] — 본 노트의 짧은 진행 메모/전단계 페이지
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-topic-map]]
- [[web-inspector-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[web-ctf-writeup-curation]]

---
title: HiddenDOM — noxCTF18 web writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, client-side, source-analysis, inspector, hidden-file]
sources: [https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md, https://github.com/xpinked/ctf-writeups, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md]
confidence: medium
---

# HiddenDOM — noxCTF18 web writeup

> 페이지 소스와 obfuscated JS를 읽고, 숨은 파라미터와 DOM 동작 규칙을 찾아내는 source-inspection 계열 writeup입니다.

## 참고 URL
- [Original writeup](https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md)
- [xpinked/ctf-writeups](https://github.com/xpinked/ctf-writeups)
- [Original writeup](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md)


## 1. 한 줄 요약
- 렌더링된 화면보다 **원본 HTML / JS source**가 더 중요합니다.
- `target`, `expression` 같은 파라미터가 DOM 동작을 바꾸는 핵심 입력점입니다.
- 난독화된 JS를 풀면 필터 규칙과 우회 가능한 입력이 드러납니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | noxCTF18 |
| 카테고리 | Web |
| 핵심 아이디어 | source inspection, JS deobfuscation, DOM behavior |
| 관련 개념 | [[source-inspection-minification-ctf-patterns]], [[web-inspector-ctf-patterns]], [[web-ctf-writeup-client-side]] |
| 관련 survey | [[source-inspection-hidden-file-writeup-survey]] |

## 3. 관찰 포인트
1. view-source와 DevTools Sources 탭을 먼저 봅니다.
2. 난독화된 변수명과 함수명을 정리합니다.
3. query parameter가 DOM 로직에 연결되는지 확인합니다.
4. hidden element, comment, script literal을 검색합니다.

## 4. 풀이 흐름
1. 페이지 소스를 열어 JS 파일을 찾습니다.
2. 난독화가 심하면 pretty print 후 흐름을 추적합니다.
3. `target`과 `expression`이 어떤 분기와 연결되는지 확인합니다.
4. filter regex를 찾아 우회 가능한 입력을 구성합니다.

## 5. 방어 관점
- 민감한 로직을 클라이언트 JS에만 두지 않습니다.
- DOM 기반 검증은 공격자가 쉽게 읽고 재현할 수 있습니다.
- hidden path와 parameter는 최소한의 정보만 드러내야 합니다.

## 6. 다음 연결
- [[source-inspection-hidden-file-writeup-survey]]
- [[source-inspection-minification-ctf-patterns]]
- [[web-recon-hidden-file-discovery-ctf-hub]]

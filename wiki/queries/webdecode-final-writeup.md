---
title: webdecode — final writeup sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, inspector, base64]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/WebDecode.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-webdecode-2fb5f668eae6, https://infosecwriteups.com/picoctf-2024-webdecode-3801d825f803]
confidence: medium
---

# WebDecode — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: picoCTF 2024
- 난이도: Easy
- 핵심 취약점: 소스 코드/HTML attribute에 숨겨진 인코딩 데이터 노출
- 관련 개념: [[web-inspector-ctf-patterns]], [[base64-decoding-ctf-patterns]], [[cyberchef]]

## 2. 풀이 흐름
1. Home / About / Contact를 모두 탐색합니다.
2. About 페이지에서 Inspector를 열어 HTML 소스를 확인합니다.
3. `notify_true` 같은 수상한 속성을 찾습니다.
4. 해당 값을 복사합니다.
5. Base64로 디코딩합니다.
6. flag를 확인합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| 페이지 탐색 | 안내 문구 존재 | 숨겨진 정보가 있을 가능성 |
| About 소스 | encoded attribute 발견 | HTML 속성에 데이터 숨김 |
| 디코딩 | flag 문자열 획득 | 인코딩된 정답 노출 |

## 4. 방어 관점
- 민감한 값은 HTML attribute에 숨기지 않아야 합니다.
- 클라이언트 소스는 공격자에게 공개된다고 가정해야 합니다.
- 단순 인코딩은 보안이 아닙니다.
- Inspector로 쉽게 찾히는 정보는 비밀로 취급하면 안 됩니다.

## 5. 회고
- 이 문제는 복잡한 공격보다 **기본 소스 분석 습관**을 점검하는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 화면 텍스트가 아닌 HTML 소스를 봤는가
  - [ ] 숨은 attribute를 찾았는가
  - [ ] 인코딩 유형을 판별했는가

## 6. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[cyberchef]]
- [[web-ctf-master-checklist]]

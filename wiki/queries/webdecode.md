---
title: webdecode — picoCTF 2024 web ctf note
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, inspector, base64]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/WebDecode.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-webdecode-2fb5f668eae6, https://infosecwriteups.com/picoctf-2024-webdecode-3801d825f803]
confidence: medium
---

# WebDecode

> 이 페이지는 **picoCTF 2024 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: picoCTF 2024
- 난이도: Easy
- 문제 유형: Web Exploitation
- 핵심 개념: [[web-inspector-ctf-patterns]], [[base64-decoding-ctf-patterns]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| / | GET | No | navigation links | hidden content hint | Home/About/Contact 구조 |
| /about | GET | No | page source / inspector | encoded attribute | `notify_true` 속성에 주목 |
| /contact | GET | No | page navigation | hint text | 추가 탐색 유도 |

## 3. 가설
- 가설 1: 페이지 본문보다 HTML 소스에 중요한 값이 숨겨져 있습니다.
- 가설 2: 숨은 값은 인코딩되어 있으며, Base64일 가능성이 높습니다.
- 가설 3: About 페이지의 특수 속성에서 flag 또는 그 일부가 노출됩니다.

## 4. 실험 기록
### 시도 1
- payload: Home/About/Contact 메뉴 탐색
- 관찰: About과 Contact에 탐색 힌트가 존재
- 해석: 페이지 소스 확인이 필요합니다.
- 다음 가설: Inspector로 HTML 속성 탐색

### 시도 2
- payload: About 페이지 소스 확인
- 관찰: `notify_true="..."` 형태의 값 발견
- 해석: 일반 텍스트가 아니라 인코딩된 데이터입니다.
- 다음 가설: Base64 decode 시도

### 시도 3
- payload: `notify_true` 값 Base64 디코딩
- 관찰: flag 형식 문자열 획득
- 해석: 숨은 attribute + 인코딩 조합이 핵심입니다.

## 5. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[cyberchef]]
- [[web-ctf-master-checklist]]

## 6. 회고
- 막힌 지점: 화면에 보이는 텍스트만 보면 flag가 보이지 않습니다.
- 우회 포인트: **소스 코드/Inspector**에서 숨은 속성을 찾아야 합니다.
- 다음에 먼저 볼 것: HTML attribute, 주석, 포함된 리소스, encoded string
- 재사용 체크리스트:
  - [ ] DevTools/Inspector로 소스 확인했는가
  - [ ] 숨은 attribute나 주석이 있는가
  - [ ] encoded string의 형식을 판별했는가
  - [ ] base64/hex/url encoding을 순서대로 시험했는가

---
title: Unminify
created: 2026-06-14
updated: 2026-06-16
type: query
tags: [ctf, web, research, writeup, source-analysis, minification]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Unminify.md, https://medium.com/@erichdryn/unminify-picoctf-writeup-d62cfd67b8f5, https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Unminify/Unminify.md, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md]
confidence: high
---

# Unminify

> 화면에는 보이지 않지만 **page source / DOM / curl 출력**에 플래그가 숨어 있는 picoCTF 2024 Web 문제입니다.

## 1. 요약
- 플랫폼: picoCTF 2024
- 문제명: Unminify
- 유형: Web Exploitation / source inspection
- 핵심 아이디어: HTML이 minified 되어 있어도 소스에는 플래그가 그대로 들어 있습니다.
- 연결 개념: [[web-inspector-ctf-patterns]], [[source-inspection-minification-ctf-patterns]], [[web-ctf-writeup-client-side]], [[webdecode]], [[bookmarklet-final-writeup]]

## 2. 공격면
| Route / Resource | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| `/` | GET | No | browser | minified HTML | 눈에 띄는 UI는 거의 없습니다 |
| page source | view-source / Ctrl+U | No | DOM inspection | HTML 원본 | `picoCTF{...}` 문자열이 숨어 있습니다 |
| CLI fetch | curl / wget | No | URL | HTML source | grep로 플래그 추출이 가능합니다 |

## 3. 가설
- 렌더링된 화면에는 정보가 없고, **HTML source** 에 플래그가 있을 가능성이 높습니다.
- minification은 줄바꿈/공백 제거일 뿐이므로, source를 보면 숨은 attribute나 comment를 찾을 수 있습니다.
- 브라우저 DevTools 또는 `curl` 로 페이지를 직접 읽으면 빠르게 확인할 수 있습니다.

## 4. 실험 기록
### 시도 1
- payload: `Ctrl+U` 또는 DevTools로 source 확인
- 관찰: source가 한 줄로 붙어 있습니다.
- 해석: minified HTML이므로 pretty print가 유용합니다.

### 시도 2
- payload: source에서 `picoCTF` 검색
- 관찰: `<p class="picoCTF{...}"></p>` 같은 형태의 문자열이 보일 수 있습니다.
- 해석: 플래그가 DOM attribute 또는 hidden element 안에 있습니다.

### 시도 3
- payload: curl + grep
- 관찰: 플래그 패턴이 바로 추출됩니다.
- 해석: 브라우저보다 CLI가 더 빠를 수 있습니다.

```bash
# 페이지 소스를 가져와 flag 패턴만 추출합니다.
# 예상 출력: picoCTF{...}

curl -s http://titan.picoctf.net:54777/ | grep -oE 'picoCTF\{[^}]+\}'  # source에서 flag만 뽑습니다.
```

## 5. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[source-inspection-minification-ctf-patterns]]
- [[web-ctf-writeup-client-side]]
- [[bookmarklet-final-writeup]]
- [[webdecode]]

## 6. 회고
- 렌더링 결과보다 source가 더 중요할 때가 많습니다.
- minification은 숨김이 아니라 압축에 가깝습니다.
- 앞으로는 source-inspection 계열 문제에서 `Ctrl+U`, DevTools pretty print, `curl` 을 먼저 떠올리면 됩니다.

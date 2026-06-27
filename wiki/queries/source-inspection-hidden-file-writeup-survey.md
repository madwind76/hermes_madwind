---
title: Source Inspection and Hidden File Writeup Survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, source-analysis, hidden-file, hidden-path, hidden-directory, survey, writeup, reconnaissance]
sources: [https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/blob/main/Web%20Exploitation/Search%20Source/SearchSource.md, https://medium.com/@erichdryn/secrets-picoctf-writeup-bcfa26143bb1, https://medium.com/@hasnain_abid/where-are-the-robots-picoctf-web-exploitation-writeup-82a121cfd935, https://medium.com/@ahmednarmer1/ctf-day-29-7f76f92d5fb5, https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md, https://github.com/fathallah17/GamingServer-TryHackMe-WriteUp, https://github.com/shockz-offsec/Mr.Robot-CTF-Walkthrough-2021]
confidence: high
---

# Source Inspection and Hidden File Writeup Survey

> 목적: **겉으로 보이는 UI 뒤에 숨은 정보**를 찾는 writeup을 비교합니다.
> 핵심 질문: “페이지 소스, 정적 자원, robots.txt, 또는 JS 내부 로직에 답이 있는가?”

## 참고 URL
- [Original writeup](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md)
- [Original writeup](https://github.com/noamgariani11/picoCTF-2022-Writeup/blob/main/Web%20Exploitation/Search%20Source/SearchSource.md)
- [medium.com](https://medium.com/@erichdryn/secrets-picoctf-writeup-bcfa26143bb1)
- [medium.com](https://medium.com/@hasnain_abid/where-are-the-robots-picoctf-web-exploitation-writeup-82a121cfd935)
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-29-7f76f92d5fb5)
- [Original writeup](https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md)
- [fathallah17/GamingServer-TryHackMe-WriteUp](https://github.com/fathallah17/GamingServer-TryHackMe-WriteUp)
- [shockz-offsec/Mr.Robot-CTF-Walkthrough-2021](https://github.com/shockz-offsec/Mr.Robot-CTF-Walkthrough-2021)


## 비교 대상

| Source | Primitive | Discovery surface | Takeaway |
| --- | --- | --- | --- |
| `Includes` | Hidden strings in HTML / CSS / JS | `view-source`, DevTools, static assets | 클라이언트 리소스는 그대로 노출됩니다. |
| `Unminify` | Minified HTML source | `view-source`, DevTools, `curl` | minification은 보안이 아닙니다. |
| `Search Source` | Static file inspection | `wget -m`, `grep -R`, CSS comments | 미러링 후 전체 검색이 매우 효과적입니다. |
| `Secrets` | Hidden directories | `view-source`, directory discovery, path guessing | 경로 추론과 디렉터리 추적이 핵심입니다. |
| `Where Are the Robots?` | `robots.txt` recon | `robots.txt`, direct path access | 공개 힌트 파일이 숨은 경로를 가리킵니다. |
| `Roboto Sans` | `robots.txt` recon | `robots.txt`, direct path access | robots.txt는 보안이 아니라 정찰 힌트입니다. |
| `HiddenDOM` | Obfuscated JS + hidden parameters | Source, JS deobfuscation, DOM behavior | 숨은 파라미터와 필터 규칙이 공격면입니다. |

## 공통 패턴

1. **보이는 HTML만 보면 끝이 아닙니다.**
   - source, DevTools, network, response headers를 같이 봐야 합니다.
2. **숨은 파일은 정찰의 첫 단서입니다.**
   - `robots.txt`, `.htaccess`, `.well-known`, `/secret`, `/uploads` 같은 경로를 확인합니다.
3. **JS 로직도 “숨은 소스”입니다.**
   - obfuscated JavaScript, DOM-based behavior, regex filter는 실제 공격 표면입니다.
4. **정적 자원도 비밀 저장소가 될 수 있습니다.**
   - `style.css`, `script.js`, comments, hidden attributes를 항상 확인합니다.

## writeup별 메모

### 1) Includes
- `view-source`와 정적 파일에 flag 조각이 있습니다.
- 연습 포인트: source inspection, asset enumeration, 문자열 조각 복원

### 2) Unminify
- minified HTML 안에 flag가 그대로 들어 있습니다.
- 연습 포인트: source inspection, hidden element, browser devtools

### 3) Search Source
- 사이트를 로컬 미러링한 뒤 `grep`으로 flag를 찾는 방식이 잘 통합니다.
- 연습 포인트: recursive mirroring, bulk search, CSS comment 탐색

### 4) Secrets
- `secret/hidden/superhidden` 같은 경로를 따라갑니다.
- 연습 포인트: directory guessing, trailing slash, path progression

### 5) Where Are the Robots? / Roboto Sans
- `robots.txt`의 Disallow 경로가 실제 숨은 페이지로 이어집니다.
- 연습 포인트: `robots.txt` recon, path enumeration, direct access

### 6) HiddenDOM
- obfuscated JS가 숨은 파라미터와 DOM 규칙을 감춥니다.
- 연습 포인트: JS deobfuscation, regex bypass, DOM behavior analysis

## 관련 개념

- [[web-recon-hidden-file-discovery-ctf-hub]]
- [[source-inspection-minification-ctf-patterns]]
- [[web-inspector-ctf-patterns]]
- [[hidden-directory-discovery-ctf-patterns]]
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-auth-session]]
- [[includes-final-writeup]]
- [[unminify-final-writeup]]
- [[search-source-final-writeup]]
- [[secrets-final-writeup]]
- [[where-are-the-robots-final-writeup]]
- [[roboto-sans-final-writeup]]
- [[hidden-dom-final-writeup]]

## 다음 읽을 거리

- [[includes-final-writeup]]
- [[unminify-final-writeup]]
- [[search-source-final-writeup]]
- [[secrets-final-writeup]]
- [[where-are-the-robots-final-writeup]]
- [[roboto-sans-final-writeup]]
- [[hidden-dom-final-writeup]]

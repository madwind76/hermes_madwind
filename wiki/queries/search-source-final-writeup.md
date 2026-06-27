---
title: Search Source — picoCTF 2022 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, source-inspection, minification, mirror, picoctf]
sources: [https://zarrarkolachi.medium.com/search-source-picoctf-2022-55897300f239, https://github.com/noamgariani11/picoCTF-2022-Writeup/blob/main/Web%20Exploitation/Search%20Source/SearchSource.md, https://hhyleung.github.io/writeups/picoctf-2022-web/, https://docs.abbasmj.com/ctf-writeups/picoctf-2022]
confidence: high
---

# Search Source — picoCTF 2022 web writeup

> `Search Source`는 **렌더링된 화면이 아니라 소스 파일을 직접 뒤져야 하는 picoCTF 2022 Web 문제**입니다. 플래그는 본문이 아니라 `style.css` 같은 정적 파일에 숨어 있고, 로컬 미러링 후 `grep`으로 찾는 방식도 잘 통합니다.

## 참고 URL
- [zarrarkolachi.medium.com](https://zarrarkolachi.medium.com/search-source-picoctf-2022-55897300f239)
- [Original writeup](https://github.com/noamgariani11/picoCTF-2022-Writeup/blob/main/Web%20Exploitation/Search%20Source/SearchSource.md)
- [hhyleung.github.io](https://hhyleung.github.io/writeups/picoctf-2022-web/)
- [docs.abbasmj.com](https://docs.abbasmj.com/ctf-writeups/picoctf-2022)


## 1. 한 줄 요약
- 화면에는 flag가 보이지 않습니다.
- `view-source:` 또는 DevTools로 HTML/CSS/JS를 확인해야 합니다.
- 플래그는 `style.css`에 숨겨진 형태로 발견됩니다.
- 사이트를 `wget -m`으로 미러링한 뒤 `grep -R`로 찾는 것도 가능합니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 메인 화면에는 아무 정보가 없음 | source inspection 필요 |
| 2 | title / hint가 source를 보라고 암시 | CSS/JS 탐색 후보 |
| 3 | `style.css`에서 flag comment 발견 | 정적 리소스가 핵심 |
| 4 | `wget`으로 전체 미러 후 `grep` 가능 | 로컬 분석 루트 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 유형은 Web CTF에서 매우 자주 나오는 기본기입니다. 화면만 보면 아무것도 없어 보여도, **HTML 원문과 연결된 정적 파일은 브라우저가 그대로 받아서 해석**합니다. 따라서 플래그는 종종 `<!-- comment -->`나 CSS 주석, JS 문자열로 숨어 있습니다.

### 3.2 대표 풀이 흐름
```bash
# 사이트 원본을 로컬에 재귀적으로 미러링합니다.
# 예상 결과: HTML/CSS/JS 파일이 현재 디렉터리에 다운로드됩니다.
wget -r -np -k http://saturn.picoctf.net:61941/
```

```bash
# 다운로드한 파일 전체에서 picoCTF 문자열을 찾습니다.
# 예상 결과: style.css 또는 다른 정적 파일의 주석에서 flag가 나옵니다.
grep -R "picoCTF" .
```

```bash
# 필요한 경우 결과를 더 보기 좋게 정리합니다.
# 예상 결과: flag 문자열만 추려서 확인할 수 있습니다.
grep -R "picoCTF" . | cut -d ' ' -f3
```

## 4. 공격자 관점
1. 페이지 소스와 정적 파일 링크를 확인합니다.
2. `style.css`, `script.js`, image metadata 같은 리소스를 열어봅니다.
3. `picoCTF`, `flag`, `comment`, `hidden` 키워드로 검색합니다.
4. 파일이 많으면 사이트를 미러링하고 로컬에서 일괄 검색합니다.

## 5. 방어자 관점
- 정적 파일 주석에 민감 정보를 남기지 않습니다.
- 배포 전에 `grep -R "picoCTF"` 같은 간단한 검사를 자동화합니다.
- source map, debug comment, unused asset에 비밀을 넣지 않습니다.
- 클라이언트에 노출되는 모든 리소스는 공격자도 볼 수 있다고 가정합니다.

## 6. 같이 보면 좋은 페이지
- [[source-inspection-minification-ctf-patterns]]
- [[web-inspector-ctf-patterns]]
- [[web-recon-hidden-file-discovery-ctf-hub]]
- [[roboto-sans-final-writeup]]
- [[includes-final-writeup]]

## 7. 참고 소스
- [Zarar Ahmed — Search Source picoCTF 2022](https://zarrarkolachi.medium.com/search-source-picoctf-2022-55897300f239)
- [noamgariani11 — Search Source](https://github.com/noamgariani11/picoCTF-2022-Writeup/blob/main/Web%20Exploitation/Search%20Source/SearchSource.md)
- [Hannah’s Archive — picoCTF 2022 - Web Exploitation](https://hhyleung.github.io/writeups/picoctf-2022-web/)
- [Docs — PicoCTF 2022 | Web Exploit Writeups](https://docs.abbasmj.com/ctf-writeups/picoctf-2022)

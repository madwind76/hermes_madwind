---
title: Unminify — picoCTF 2024 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, source-analysis, minification, client-side]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Unminify.md, https://medium.com/@erichdryn/unminify-picoctf-writeup-d62cfd67b8f5, https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Unminify/Unminify.md, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md]
confidence: high
---

# Unminify — picoCTF 2024 web writeup

> **보이는 화면이 아니라 HTML source에 플래그가 박혀 있는** 아주 전형적인 source-inspection 문제입니다.

## 참고 URL
- [Original writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Unminify.md)
- [medium.com](https://medium.com/@erichdryn/unminify-picoctf-writeup-d62cfd67b8f5)
- [Original writeup](https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Unminify/Unminify.md)
- [Original writeup](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md)


## 1. 한 줄 요약

`Unminify`는 페이지가 minified되어 읽기 어려워 보이지만, 실제로는 HTML 소스에 `picoCTF{...}` 형태의 문자열이 숨어 있습니다. 공개 writeup들은 공통적으로 **view-source / DevTools / curl** 중 하나로 source를 읽고 플래그를 추출합니다.

## 2. 문제 메타데이터

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2024 |
| 카테고리 | Web Exploitation |
| 문제명 | Unminify |
| 핵심 유형 | [[web-inspector-ctf-patterns]] |
| 보조 개념 | [[web-ctf-writeup-client-side]], [[webdecode]], [[bookmarklet-final-writeup]] |
| 재사용 패턴 | view-source → hidden DOM → flag extraction |
| 난이도 | Easy |

## 3. 공격면

| 요소 | 관찰 |
|------|------|
| 렌더링된 페이지 | 거의 정보가 없거나 평범하게 보임 |
| HTML source | 한 줄로 minified 되어 있음 |
| DevTools | pretty print로 읽기 쉽게 정리 가능 |
| CLI | `curl` + `grep` 로 바로 검색 가능 |

## 4. 풀이 흐름

### 4.1 페이지 소스 확인

먼저 브라우저에서 `Ctrl+U` 또는 DevTools의 Elements / Sources 탭을 확인합니다. source가 한 줄로 붙어 있어도 내용 자체는 그대로 남아 있습니다.

```bash
# 브라우저 source inspection을 보조하는 CLI 예시입니다.
# 예상 출력: HTML source 내 picoCTF{...}

curl -s http://titan.picoctf.net:54777/ | grep -oE 'picoCTF\{[^}]+\}'  # flag 패턴만 추출합니다.
```

### 4.2 flag 위치 찾기

공개 writeup들은 `picoCTF` 문자열을 검색하면 `<p class="picoCTF{...}"></p>` 같은 hidden element를 찾을 수 있다고 설명합니다. 렌더링된 텍스트가 아니라 **attribute 값**에 들어 있을 수 있습니다.

### 4.3 추출

source에서 flag가 확인되면 그대로 복사하면 됩니다. 어떤 writeup은 grep 한 줄로 끝내기도 하고, 어떤 writeup은 DevTools에서 pretty print 후 수동으로 찾습니다.

## 5. 핵심 포인트

1. **minification은 난독화가 아닙니다.**
2. 플래그는 렌더링이 아니라 **source**에 있습니다.
3. `Ctrl+U`, DevTools pretty print, `curl` 은 source-inspection 문제의 기본 도구입니다.
4. 이런 유형은 `webdecode` 류와 같이 **클라이언트 사이드 탐색**으로 분류하는 것이 맞습니다.
5. 개념 페이지로는 [[source-inspection-minification-ctf-patterns]]를 같이 보면 재사용하기 좋습니다.

## 6. 방어 관점

1. 클라이언트에 노출한 HTML/주석/속성은 공격자에게 이미 보인 것으로 봐야 합니다.
2. 민감한 값은 source에 두지 않습니다.
3. 단순 minification은 보안 통제가 아닙니다.

## 7. 같은 계열에서 확인할 것

- [ ] `Ctrl+U` 또는 view-source를 확인했는가?
- [ ] DevTools pretty print로 source를 읽기 쉽게 만들었는가?
- [ ] HTML comment, attribute, hidden tag를 검색했는가?
- [ ] `curl` / `grep` 으로 패턴 추출이 가능한가?
- [ ] 이 문제를 client-side/source-inspection 허브에 연결했는가?

## 8. 출처별 교차 확인

| 출처 | 확인한 내용 |
|------|-------------|
| noamgariani11 GitHub | source에 숨은 flag, `curl`/`grep` 예시 |
| Eric H Medium | DevTools로 source/DOM 확인 후 hidden comment 발견 |
| snwau GitHub | flag가 class attribute/hidden element에 포함 |
| Cajac GitHub | `Ctrl+U`, view-source, pretty print, curl extraction |

## 9. 관련 페이지

- [[unminify]]
- [[web-ctf-writeup-client-side]]
- [[web-inspector-ctf-patterns]]
- [[source-inspection-minification-ctf-patterns]]
- [[webdecode]]
- [[bookmarklet-final-writeup]]

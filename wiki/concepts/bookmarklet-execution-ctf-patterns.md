---
title: Bookmarklet execution — picoCTF pattern
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, web, client-side, javascript, source-inspection, research]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Bookmarklet.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-bookmarklet-9e7d72c97f96, https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c, https://dev.to/davidonlinearchive/bookmarklet-picoctf-24-web-12hn, https://medium.com/@rachael_muga/picoctf-bookmarklet-web-exploitation-3cff31a6c1dc, https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-bookmarklet-506a480fd17f, https://qiita.com/colza_/items/ad51902cf9abc999b227]
confidence: high
---

# Bookmarklet execution — picoCTF pattern

## 참고 URL
- [Original source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Bookmarklet.md)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-bookmarklet-9e7d72c97f96)
- [medium.com](https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c)
- [dev.to](https://dev.to/davidonlinearchive/bookmarklet-picoctf-24-web-12hn)
- [medium.com](https://medium.com/@rachael_muga/picoctf-bookmarklet-web-exploitation-3cff31a6c1dc)
- [medium.com](https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-bookmarklet-506a480fd17f)
- [qiita.com](https://qiita.com/colza_/items/ad51902cf9abc999b227)

## 1. 한 줄 정의
이 패턴은 **페이지가 제공한 JavaScript를 북마크릿(bookmarklet) 또는 브라우저 콘솔에 넣어, 현재 페이지 맥락에서 바로 실행하게 만드는 Web CTF 유형**입니다.

## 2. 비유
- **비유**: 리모컨의 숨은 버튼을 누르면 TV 메뉴가 열리는 것처럼, 북마크 하나가 웹페이지 안에서 JavaScript를 바로 실행합니다.
- **흐름**: 사용자는 그냥 "북마크"를 누른다고 생각하지만, 브라우저는 실제로 `javascript:` 코드를 실행합니다.
- **핵심**: 겉보기에는 단순한 편의 기능이지만, CTF에서는 이 경로가 플래그 출력 또는 숨은 로직 재현의 통로가 됩니다.

## 3. 기술 설명
bookmarklet은 일반 URL 대신 `javascript:` 스킴을 사용하는 북마크입니다. 브라우저는 해당 문자열을 주소로 이동시키는 대신 현재 탭의 DOM과 JavaScript 실행 컨텍스트에서 코드를 수행합니다. picoCTF의 `Bookmarklet` 문제는 이 동작을 이용해 사용자가 제공된 코드를 콘솔이나 북마크로 실행하고, 결과로 flag를 얻도록 설계됩니다.

## 4. 전형적인 풀이 흐름
```text
challenge page -> provided JavaScript 확인 -> 북마크 또는 Console에 코드 입력 -> 현재 페이지 맥락에서 실행 -> alert / output에서 flag 확인
```

## 5. 공격자 관점
1. 페이지에 적힌 JavaScript를 그대로 복사합니다.
2. 브라우저 Console 또는 북마크 URL로 실행합니다.
3. 코드가 페이지 안의 숨은 값, 난독화 문자열, 디코딩 로직을 복원하는지 봅니다.
4. 출력된 `alert` 또는 DOM 갱신 결과에서 flag를 확인합니다.

## 6. 방어자 관점
- 사용자에게 임의 JavaScript 실행을 유도하는 흐름은 신뢰 경계를 흐리게 만듭니다.
- 민감한 값은 클라이언트 스크립트나 북마크릿 형태로 배포하지 않습니다.
- 브라우저 맥락에서 실행되는 코드는 DOM, 쿠키, 세션에 직접 접근할 수 있음을 전제로 설계해야 합니다.

## 7. 같이 보면 좋은 페이지
- [[bookmarklet-final-writeup]]
- [[web-ctf-writeup-client-side]]
- [[client-side-secret-exposure-ctf-patterns]]
- [[webdecode-final-writeup]]
- [[web-ctf-writeup-topic-map]]
- [[picoctf-web-survey]]

## 8. 참고 소스
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Bookmarklet.md)
- [Kamal S — Bookmarklet](https://medium.com/@Kamal_S/picoctf-web-exploitation-bookmarklet-9e7d72c97f96)
- [DEV Community — Bookmarklet](https://dev.to/davidonlinearchive/bookmarklet-picoctf-24-web-12hn)
- [Rachael Muga — Local Authority](https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c)

---
title: Bookmarklet — picoCTF 2024 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, client-side, research]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Bookmarklet.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-bookmarklet-9e7d72c97f96, https://dev.to/davidonlinearchive/bookmarklet-picoctf-24-web-12hn, https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Bookmarklet.md, https://medium.com/@rachael_muga/picoctf-bookmarklet-web-exploitation-3cff31a6c1dc, https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-bookmarklet-506a480fd17f, https://medium.com/@viscidCTF/picoctf-2024-bookmarklet-502c08e5659a, https://medium.com/@ahmednarmer1/ctf-day-4-76c165186a3a, https://qiita.com/colza_/items/ad51902cf9abc999b227, https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99, https://infosecwriteups.com/%EF%B8%8F-picoctf-2024-bookmarklet-web-exploitation-challenge-834b3ce821e2, https://www.linkedin.com/pulse/picoctf-introduction-bookmarklet-sreedeep-cv-7vluc, https://www.youtube.com/watch?v=9UF6OVORbuY, https://www.youtube.com/watch?v=vGH76PEFtaQ, https://hackmd.io/@urchinsec/rJgMIgJRT, https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/]
confidence: high
---

# Bookmarklet — picoCTF 2024 web writeup

> 브라우저 북마클릿(bookmarklet)을 직접 실행해 페이지가 숨긴 JavaScript를 재현하는 picoCTF Web Exploitation 문제입니다.
> 이 문제는 `javascript:` 스킴을 이용해 **현재 페이지 맥락에서 JavaScript를 실행**하는 흐름을 이해하는 것이 핵심입니다.

## 참고 URL
- [Original writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Bookmarklet.md)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-bookmarklet-9e7d72c97f96)
- [dev.to](https://dev.to/davidonlinearchive/bookmarklet-picoctf-24-web-12hn)
- [medium.com](https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c)
- [Original writeup](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Bookmarklet.md)
- [medium.com](https://medium.com/@rachael_muga/picoctf-bookmarklet-web-exploitation-3cff31a6c1dc)
- [medium.com](https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-bookmarklet-506a480fd17f)
- [medium.com](https://medium.com/@viscidCTF/picoctf-2024-bookmarklet-502c08e5659a)
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-4-76c165186a3a)
- [qiita.com](https://qiita.com/colza_/items/ad51902cf9abc999b227)
- [infosecwriteups.com](https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99)
- [infosecwriteups.com](https://infosecwriteups.com/%EF%B8%8F-picoctf-2024-bookmarklet-web-exploitation-challenge-834b3ce821e2)
- [www.linkedin.com](https://www.linkedin.com/pulse/picoctf-introduction-bookmarklet-sreedeep-cv-7vluc)
- [www.youtube.com](https://www.youtube.com/watch?v=9UF6OVORbuY)
- [www.youtube.com](https://www.youtube.com/watch?v=vGH76PEFtaQ)
- [hackmd.io](https://hackmd.io/@urchinsec/rJgMIgJRT)
- [blog.qz.sg](https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/)


## 1. 한 줄 요약
- 사용자가 페이지에 표시된 JavaScript를 **북마크에 저장한 뒤 실행**하면, 브라우저가 플래그를 포함한 동작을 수행합니다.
- 핵심은 서버 취약점이 아니라 **클라이언트 측 스크립트 실행 방식**을 이해하는 것입니다.
- 난이도는 낮지만, 브라우저 도구와 자바스크립트 실행 흐름을 익히기 좋습니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2024 |
| 유형 | Web Exploitation |
| 핵심 아이디어 | bookmarklet, browser JavaScript execution |
| 실전 포인트 | 브라우저 콘솔/북마크 편집/JS 실행 |

## 3. 풀이 흐름
1. 문제 페이지를 열어 표시된 JavaScript 또는 안내 문구를 확인합니다.
2. 페이지가 제공한 코드를 브라우저의 **북마크 URL**로 저장합니다.
3. 저장한 북마크를 실행하면 페이지 맥락에서 JavaScript가 동작합니다.
4. 실행 결과로 팝업 또는 출력값이 나타나며, 여기서 플래그를 얻습니다.

## 4. 왜 이 문제가 중요한가
- **bookmarklet**은 브라우저 기능이지만, 실전에서는 우회적인 스크립트 실행 경로가 됩니다.
- 웹 CTF에서는 이 방식이 `XSS`, `DOM 조작`, `client-side state` 이해로 이어집니다.
- 단순히 "자바스크립트를 실행했다"가 아니라, **어떤 맥락에서 스크립트가 실행되는지**를 읽는 훈련에 좋습니다.

## 5. 방어 관점
- 북마크릿 자체가 취약점은 아니지만, 사용자에게 임의 JavaScript 실행을 유도하는 흐름은 위험합니다.
- 민감 정보는 클라이언트 스크립트에 두지 않아야 합니다.
- 브라우저 맥락에서 실행되는 코드가 인증 정보/DOM/API를 직접 만질 수 있다는 점을 항상 의식해야 합니다.

## 6. 관련 위키 링크
- [[web-ctf-writeup-client-side]] — 클라이언트 사이드 Web CTF 분류 허브
- [[web-ctf-writeup-curation]] — Web CTF writeup 큐레이션 허브
- [[web-ctf-writeup-topic-map]] — Web CTF 상위 지도
- [[webdecode]] — picoCTF 2024의 또 다른 클라이언트 사이드 계열 문제
- [[bookmarklet-execution-ctf-patterns]] — 북마크릿 실행 패턴 개념 페이지
- [[web-ctf-master-checklist]] — Web CTF 공통 점검 목록

## 7. 참고 소스
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Bookmarklet.md)
- [Kamal S — Medium](https://medium.com/@Kamal_S/picoctf-web-exploitation-bookmarklet-9e7d72c97f96)
- [DEV Community](https://dev.to/davidonlinearchive/bookmarklet-picoctf-24-web-12hn)
- [Rachael Muga — Local Authority](https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c)
- [Cajac GitHub writeup](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Bookmarklet.md)
- [Rachael Muga — Bookmarklet](https://medium.com/@rachael_muga/picoctf-bookmarklet-web-exploitation-3cff31a6c1dc)
- [Bl4cky — Bookmarklet](https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-bookmarklet-506a480fd17f)
- [viscidCTF — Bookmarklet](https://medium.com/@viscidCTF/picoctf-2024-bookmarklet-502c08e5659a)
- [Ahmed Narmer — CTF Day(4)](https://medium.com/@ahmednarmer1/ctf-day-4-76c165186a3a)
- [Qiita — Bookmarklet](https://qiita.com/colza_/items/ad51902cf9abc999b227)
- [InfoSecWriteups — picoCTF 2024 Web](https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99)
- [InfoSecWriteups — Bookmarklet challenge](https://infosecwriteups.com/%EF%B8%8F-picoctf-2024-bookmarklet-web-exploitation-challenge-834b3ce821e2)
- [LinkedIn — PicoCTF an Introduction to Bookmarklet](https://www.linkedin.com/pulse/picoctf-introduction-bookmarklet-sreedeep-cv-7vluc)
- [YouTube — picoGym Exercise: Bookmarklet](https://www.youtube.com/watch?v=9UF6OVORbuY)
- [YouTube — Bookmarklet Pico CTF 2024 Walkthrough](https://www.youtube.com/watch?v=vGH76PEFtaQ)
- [HackMD — picoCTF 2024 writeup](https://hackmd.io/@urchinsec/rJgMIgJRT)
- [QZ.sg picoCTF 2024 web writeups](https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/)

## 8. 다음 연결
- `IntroToBurp`처럼 브라우저 도구를 활용하는 문제와 함께 보면 좋습니다.
- `WebDecode`처럼 사용자 입력이 브라우저에서 해석되는 흐름과 비교하면 학습 효과가 큽니다.
- `[[bookmarklet-execution-ctf-patterns]]`를 함께 보면 bookmarklet이 왜 클라이언트 사이드 패턴인지 정리됩니다.

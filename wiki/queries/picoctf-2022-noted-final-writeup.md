---
title: noted — picoCTF 2022 web exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, web-exploitation, xss, browser]
sources: [https://picoctf2022.haydenhousen.com/web-exploitation/noted.md, https://github.com/sambrow/ctf-writeups-2021/tree/master/perfect-blue-ctf/TBDXSS]
confidence: medium
---

# noted — picoCTF 2022 web exploitation writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/web-exploitation/noted.md)
- [Perfect Blue CTF 2021 TBDXSS writeup](https://github.com/sambrow/ctf-writeups-2021/tree/master/perfect-blue-ctf/TBDXSS)

## 핵심 요약
`Fastify + EJS + SQLite + Puppeteer` 조합의 노트 서비스에서 **stored XSS**를 활용하는 문제입니다.
`notes.ejs`의 비이스케이프 출력이 취약점의 출발점이며, `report` 기능으로 띄운 headless Chrome의 동일 출처 DOM 접근과 `window.open(..., "pico")` 동작을 이용해 노트 내용을 외부로 전송합니다.

## 풀이 메모
1. 노트 본문에 `<script>`를 넣어 저장형 XSS가 가능한지 확인합니다.
2. 보고 기능이 여는 headless Chrome 환경과 same-origin DOM 접근을 이용해 `pico` 윈도우의 내용을 읽습니다.
3. 읽은 내용을 webhook.site 같은 외부 수신기로 보내 플래그를 획득합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-web-exploitation-survey]]
- [[picoctf-2022-web-exploitation-family-hub]]
- [[picoctf-2022-topic-map]]

---
title: picoCTF 2020 web survey
created: 2026-06-16
updated: 2026-06-16
type: query
tags: [ctf, web, survey, picoctf, picoctf2020, sqlite, sqli]
sources: [queries/web-gauntlet-final-writeup.md, https://github.com/onealmond/hacking-lab/blob/master/picoctf-2020/web-gauntlet/writeup.md, https://medium.com/@sobatistacyber/picoctf-writeup-web-gauntlet-7c3b8c7c7946]
confidence: high
---

# picoCTF 2020 web survey

> picoCTF 2020 Web Exploitation에서 위키에 정리된 문제를 한눈에 보는 요약 페이지입니다.
> 현재 위키에는 **1/1 문제**가 정리되어 있습니다.
> 상위 허브: [[picoctf-web-survey]] · [[picoctf-2025-web-exploitation-survey]] · [[picoctf-pwn-survey]]

## 문제 목록

| # | 문제 | 상태 | 핵심 primitive | 연결 문서 |
|---|---|---|---|---|
| 1 | Web Gauntlet | solved | SQLite SQLi / filter bypass | [[web-gauntlet-final-writeup]] |

## 문제 해석

### 1) SQLite 필터 우회 계열
- `Web Gauntlet`

이 문제는 SQLite 기반 로그인 쿼리에서 필터를 우회해 `admin` 조건을 만족시키는 유형입니다. 문자열 결합, 주석 처리, 짧은 payload 압축이 핵심입니다.

## 같이 보면 좋은 페이지
- [[web-gauntlet-final-writeup]]
- [[web-gauntlet-2-3-sqlite-survey]]
- [[sqlite-sqli-filter-bypass-ctf-patterns]]
- [[sql-injection]]

## 참고 소스
- [hacking-lab — picoctf-2020/web-gauntlet](https://github.com/onealmond/hacking-lab/blob/master/picoctf-2020/web-gauntlet/writeup.md)
- [Sobatista — PicoCTF Writeup Web Gauntlet](https://medium.com/@sobatistacyber/picoctf-writeup-web-gauntlet-7c3b8c7c7946)
- [YouTube — Bypassing SQL Filters (picoCTF Web Gauntlet)](https://www.youtube.com/watch?v=ZQj5tSwaG0k)

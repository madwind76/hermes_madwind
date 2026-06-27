---
title: JWT auth bypass writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, jwt, token-forgery, auth, broken-auth, login]
sources: [https://raw.githubusercontent.com/team0se7en/CTF-Writeups/master/csictf2020/web/ccc/README.md, https://gist.github.com/JMdoubleU/705819866852690d34e34aee2074a65c, https://brandon-t-elliott.github.io/ctf-challenge-writeup-picoctf-jauth, https://www.probablynotimportant.com/posts/2021-08-17-picoctf2021-jauth, https://github.com/faisalmemon/picoCTF-JAuth-writeup]
confidence: high
---

# JWT auth bypass writeup survey

## 참고 URL
- [raw source](https://raw.githubusercontent.com/team0se7en/CTF-Writeups/master/csictf2020/web/ccc/README.md)
- [Gist](https://gist.github.com/JMdoubleU/705819866852690d34e34aee2074a65c)
- [brandon-t-elliott.github.io](https://brandon-t-elliott.github.io/ctf-challenge-writeup-picoctf-jauth)
- [www.probablynotimportant.com](https://www.probablynotimportant.com/posts/2021-08-17-picoctf2021-jauth)
- [faisalmemon/picoCTF-JAuth-writeup](https://github.com/faisalmemon/picoCTF-JAuth-writeup)


## 1. 목적
JWT secret 노출과 토큰 위조가 어떻게 admin 권한 획득으로 이어지는지 여러 writeup을 비교합니다.

## 2. 비교 대상

| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| ccc | JWT secret exposure | LFI / file read | `.env`에서 secret을 읽어 admin 토큰을 위조합니다. |
| h1-702 | JWT auth bypass | file read / path enumeration | JWT와 RPC 흐름을 분석해 유효한 토큰과 숨은 데이터를 연결합니다. |
| JAuth | weak JWT secret fallback | source inspection | fallback secret이 약해 관리자 토큰을 다시 서명할 수 있습니다. |

## 3. 공통 관찰
1. JWT는 **서명 비밀키**가 노출되면 무력화됩니다.
2. 파일 읽기 취약점은 종종 인증 계층 전체를 붕괴시킵니다.
3. admin 여부가 토큰 클레임 하나로 결정되면, 토큰 위조가 곧 권한 상승입니다.
4. fallback secret이나 하드코딩 키는 소스 공개 환경에서 특히 위험합니다.

## 4. 관련 개념
- [[jwt-secret-exposure-ctf-patterns]]
- [[broken-auth]]
- [[web-ctf-writeup-family-hub]]
- [[ccc-jwt-final-writeup]]
- [[h1-702-jwt-final-writeup]]
- [[jauth-final-writeup]]

## 5. 다음 읽을 거리
- [[ccc-jwt-final-writeup]]
- [[h1-702-jwt-final-writeup]]
- [[jauth-final-writeup]]

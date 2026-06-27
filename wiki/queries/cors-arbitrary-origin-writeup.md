---
title: CORS Arbitrary Origin Trust writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, cors, cross-origin, same-origin-policy, writeup]
sources: [https://medium.com/@vulnmachines/cross-origin-resource-sharing-write-up-vulnmachines-d09a522a295b, https://medium.com/bugbountywriteup/exploiting-cors-misconfigurations-ffb538698600]
confidence: high
---

# CORS Arbitrary Origin Trust writeup

> 서버가 들어오는 `Origin`을 그대로 신뢰하거나, 너무 느슨한 화이트리스트로 허용해서 민감 응답을 읽게 되는 CORS 실습입니다.

## 참고 URL
- [medium.com](https://medium.com/@vulnmachines/cross-origin-resource-sharing-write-up-vulnmachines-d09a522a295b)
- [medium.com](https://medium.com/bugbountywriteup/exploiting-cors-misconfigurations-ffb538698600)


## 1. 한 줄 요약
- `Access-Control-Allow-Origin`이 `Origin`을 그대로 반사하거나 `*`로 열려 있으면, 공격자 사이트가 피해자 브라우저의 응답을 읽을 수 있습니다.
- Vulnmachines 실습의 `Arbitrary Origin Trust`는 이 패턴을 직접 보여줍니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|---|---|---|
| 1 | 페이지 소스/로그인 흐름에서 lab entry 발견 | CORS 챌린지 진입점 |
| 2 | 응답 헤더가 `Access-Control-Allow-Origin`을 포함 | 브라우저가 cross-origin 읽기를 허용할 가능성 |
| 3 | `Origin`을 바꾸면 허용 값이 반영됨 | arbitrary origin trust |
| 4 | 자격증명 포함 요청이 성공 | 민감 데이터 읽기 가능 |

## 3. 핵심 포인트
```http
# 예상 동작: Origin이 허용되면 응답을 브라우저 JS가 읽을 수 있습니다.
Origin: https://attacker.example
```

## 4. 연결 개념
- [[cors-misconfig-core]]
- [[cors-misconfig-defense]]
- [[cors-misconfig]]
- [[web-ctf-writeup-family-hub]]

## 5. 참고 소스
- [Vulnmachines CORS write-up](https://medium.com/@vulnmachines/cross-origin-resource-sharing-write-up-vulnmachines-d09a522a295b)
- [Nol White Hat — Exploiting CORS misconfigurations](https://medium.com/bugbountywriteup/exploiting-cors-misconfigurations-ffb538698600)

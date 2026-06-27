---
title: CORS writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [web, survey, cors, cross-origin, same-origin-policy, writeup]
sources: [https://medium.com/@vulnmachines/cross-origin-resource-sharing-write-up-vulnmachines-d09a522a295b, https://medium.com/bugbountywriteup/exploiting-cors-misconfigurations-ffb538698600, https://medium.com/@boogsta/cors-misconfiguration-pii-leak-2765ff5b7115, https://ehxb.medium.com/ehxb-cors-sop-tryhackme-write-up-97e1b141efa9]
confidence: high
---

# CORS writeup survey

## 참고 URL
- [medium.com](https://medium.com/@vulnmachines/cross-origin-resource-sharing-write-up-vulnmachines-d09a522a295b)
- [medium.com](https://medium.com/bugbountywriteup/exploiting-cors-misconfigurations-ffb538698600)
- [medium.com](https://medium.com/@boogsta/cors-misconfiguration-pii-leak-2765ff5b7115)
- [ehxb.medium.com](https://ehxb.medium.com/ehxb-cors-sop-tryhackme-write-up-97e1b141efa9)


## 1. 목적
CORS는 단순 설정 실수처럼 보이지만, 실제로는 인증 응답을 읽게 만드는 데이터 유출 경로가 됩니다. 이 survey는 `arbitrary origin`, `regex bypass`, `null origin`, `credentialed read`를 함께 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| CORS Arbitrary Origin Trust | arbitrary origin trust | credentialed read | 입력한 Origin을 그대로 믿어 응답을 읽게 됩니다. |
| CORS PII Leak | origin reflection | withCredentials | 공격자 origin으로 반사되어 개인정보가 새어 나갑니다. |

## 3. 공통 관찰
1. CORS는 서버가 아닌 브라우저가 지키는 정책을 느슨하게 만드는 장치입니다.
2. `Access-Control-Allow-Origin`과 `Access-Control-Allow-Credentials` 조합이 핵심입니다.
3. 정규식 화이트리스트는 앵커 부족, suffix 매칭, `null` origin 허용 때문에 쉽게 무너질 수 있습니다.

## 4. 관련 개념
- [[cors-misconfig-core]]
- [[cors-misconfig-defense]]
- [[cors-misconfig]]
- [[web-ctf-writeup-family-hub]]
- [[cors-arbitrary-origin-writeup]]
- [[cors-pii-leak-writeup]]

## 5. 다음 읽을 거리
- [[cors-arbitrary-origin-writeup]]
- [[cors-pii-leak-writeup]]

---
title: CORS PII Leak writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [web, cors, cross-origin, same-origin-policy, writeup]
sources: [https://medium.com/@boogsta/cors-misconfiguration-pii-leak-2765ff5b7115, https://ehxb.medium.com/ehxb-cors-sop-tryhackme-write-up-97e1b141efa9]
confidence: high
---

# CORS PII Leak writeup

> `Origin` 반사, 느슨한 정규식 검사, `null` origin 허용 같은 실수로 인해 인증된 사용자 데이터가 새는 사례를 모아둔 leaf입니다.

## 참고 URL
- [medium.com](https://medium.com/@boogsta/cors-misconfiguration-pii-leak-2765ff5b7115)
- [ehxb.medium.com](https://ehxb.medium.com/ehxb-cors-sop-tryhackme-write-up-97e1b141efa9)


## 1. 한 줄 요약
- `Access-Control-Allow-Origin`이 공격자 origin으로 반사되면, 브라우저가 인증 응답을 읽을 수 있습니다.
- `null` origin 또는 약한 정규식은 추가 우회 포인트가 됩니다.

## 2. 문제 흐름
| 사례 | 관찰 | 의미 |
|---|---|---|
| PII leak | `Origin: https://test.com`이 반사됨 | credentialed cross-origin read 가능 |
| Regex bypass | `#vulnmachines.lab` 같은 값이 통과 | 느슨한 regex whitelist 우회 |
| Null origin | `Origin: null` 허용 | file://, sandbox iframe 계열 우회 가능 |

## 3. 핵심 포인트
```html
<!-- 예상 동작: withCredentials=true 요청이 CORS 허용 시 응답을 읽습니다. -->
<script>
  // 실제 공격 코드가 아니라 CORS 동작 확인용 예시입니다.
  xhr.withCredentials = true;
</script>
```

## 4. 연결 개념
- [[cors-misconfig-core]]
- [[cors-misconfig-defense]]
- [[cors-misconfig]]
- [[web-ctf-writeup-family-hub]]

## 5. 참고 소스
- [Boogsta — CORS Misconfiguration -> PII Leak](https://medium.com/@boogsta/cors-misconfiguration-pii-leak-2765ff5b7115)
- [Ehxb — CORS & SOP TryHackMe WriteUp](https://ehxb.medium.com/ehxb-cors-sop-tryhackme-write-up-97e1b141efa9)

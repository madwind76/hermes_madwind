---
title: findme — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, reconnaissance, burp, traffic-inspection, base64, post-auth]
sources: [https://medium.com/@ahmednarmer1/ctf-day-25-2c8a7a50e903, https://medium.com/@Kamal_S/picoctf-web-exploitation-findme-a471621624b3, https://medium.com/@f4b1o22/picoctf-2023-findme-write-up-41c8e20dcdde]
confidence: high
---

# findme — picoCTF 2025 web writeup

> 로그인 이후 발생하는 추가 요청을 Burp로 잡아내고, `id` 파라미터의 Base64 값을 디코딩해서 flag를 찾는 picoCTF Web Exploitation 문제입니다.

## 1. 한 줄 요약
- UI만 보면 단서가 거의 없습니다.
- 핵심은 **로그인 이후의 추가 요청**입니다.
- `flag` 요청의 `id` 값이 **Base64**로 숨겨져 있습니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | username/password만 제공됨 | source보다 트래픽이 중요할 수 있음 |
| 2 | 로그인 후 `/home` 이동 | 추가 요청이 발생할 수 있음 |
| 3 | Burp에서 `flag` 요청 2개 발견 | 숨은 백엔드 동작 존재 |
| 4 | `id` 파라미터 확인 | 값이 Base64처럼 보임 |
| 5 | Base64 디코딩 | flag 문자열 획득 |

## 3. 분석 포인트
```bash
# Base64로 인코딩된 id 값을 복원합니다.
# 예상 결과: 사람이 읽을 수 있는 flag 조각 또는 전체 flag가 출력됩니다.
echo 'cGljb0NURnt...}' | base64 -d
```

## 4. 공격자 관점
1. 로그인 전후 요청 차이를 확인합니다.
2. 숨은 요청이 있는지 Burp Proxy History를 봅니다.
3. `/home` 진입 후 추가 요청 이름과 파라미터를 확인합니다.
4. `id` 값이 Base64라면 디코딩합니다.
5. 응답에 flag가 바로 나오는지 확인합니다.

## 5. 방어자 관점
- 로그인 후 요청에도 최소 권한을 적용합니다.
- 숨은 엔드포인트에 민감 데이터를 그대로 보내지 않습니다.
- 파라미터 인코딩은 보안 통제가 아닙니다.
- 트래픽에 나오는 모든 값은 공격자에게 보인다고 가정합니다.

## 6. 같이 보면 좋은 페이지
- [[post-auth-hidden-request-recon-ctf-patterns]]
- [[reconnaissance]]
- [[base64-decoding-ctf-patterns]]
- [[client-side-secret-exposure-ctf-patterns]]

## 7. 참고 소스
- [Ahmed Narmer — picoCTF Web Exploitation: findme](https://medium.com/@ahmednarmer1/ctf-day-25-2c8a7a50e903)
- [Kamal S — picoCTF Web Exploitation: findme](https://medium.com/@Kamal_S/picoctf-web-exploitation-findme-a471621624b3)
- [F4b1o22 — picoCTF 2023 findme write-up](https://medium.com/@f4b1o22/picoctf-2023-findme-write-up-41c8e20dcdde)

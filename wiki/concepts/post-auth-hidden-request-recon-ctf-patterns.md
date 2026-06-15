---
title: Post-auth hidden request reconnaissance — picoCTF pattern
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [ctf, web, reconnaissance, burp, traffic-inspection, hidden-request, base64]
sources: [https://medium.com/@ahmednarmer1/ctf-day-25-2c8a7a50e903, https://medium.com/@Kamal_S/picoctf-web-exploitation-findme-a471621624b3]
confidence: high
---

# Post-auth hidden request reconnaissance — picoCTF pattern

## Step 1. 한 줄 정의
이 패턴은 **로그인 후에만 발생하는 추가 요청, 숨은 엔드포인트, 또는 Base64로 인코딩된 파라미터를 Burp 같은 프록시로 찾아내는 Web CTF 유형**입니다.

## Step 2. 비유
- **비유**: 문을 열고 들어간 뒤에야 보이는 뒷문과 쪽지를 찾는 것과 같습니다.
- **이미지**: 화면에는 검색창만 있지만, 실제 답은 네트워크 트래픽에 숨어 있습니다.
- **전문 설명**: 프론트엔드 UI만 보면 단서가 없을 수 있으므로, 로그인 전후 요청 차이와 추가 API 호출을 비교해야 합니다. 숨은 요청의 파라미터가 Base64일 수도 있으므로 인코딩 습관도 함께 적용합니다.

## 핵심 흐름
```text
login -> /home 확인 -> Burp Proxy로 요청 캡처 -> 추가 요청 / flag 엔드포인트 발견 -> 파라미터 분석 -> Base64 decode -> flag 획득
```

## 공격자 관점
1. 로그인 전후의 요청 수를 비교합니다.
2. 화면에 보이지 않는 추가 요청이 있는지 확인합니다.
3. `flag`, `search`, `api` 같은 힌트성 경로를 찾습니다.
4. 파라미터 값이 Base64처럼 보이면 먼저 디코딩합니다.
5. 응답 본문뿐 아니라 상태 코드와 리다이렉트도 같이 봅니다.

## 방어자 관점
- 민감 데이터가 숨은 요청에 실리지 않도록 설계합니다.
- 클라이언트가 볼 수 있는 모든 요청을 공개 정보로 간주합니다.
- 로그인 후 추가 요청에는 접근 제어와 출력 최소화를 적용합니다.
- Base64처럼 단순 인코딩으로 민감 정보를 숨기지 않습니다.

## 같이 보면 좋은 페이지
- [[reconnaissance]]
- [[base64-decoding-ctf-patterns]]
- [[client-side-secret-exposure-ctf-patterns]]
- [[findme-final-writeup]]

## 참고 소스
- [Ahmed Narmer — picoCTF Web Exploitation: findme](https://medium.com/@ahmednarmer1/ctf-day-25-2c8a7a50e903)
- [Kamal S — picoCTF Web Exploitation: findme](https://medium.com/@Kamal_S/picoctf-web-exploitation-findme-a471621624b3)

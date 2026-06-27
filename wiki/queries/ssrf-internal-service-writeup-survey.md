---
title: SSRF Internal Service Writeup Survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, ssrf, internal-service, survey, writeup]
sources: [https://github.com/ilhambagas/Bithug, https://github.com/muhashali/writeup-SSRF, https://github.com/jdonsec/allthingsssrf, https://github.com/orangetw/My-CTF-Web-Challenges]
confidence: medium
---

# SSRF Internal Service Writeup Survey

> 목적: **서버가 내부로 대신 요청을 보내는 구조**를 비교합니다.
> 핵심 질문: “외부에서 막힌 대상을 서버 내부 관점으로 우회할 수 있는가?”

## 참고 URL
- [ilhambagas/Bithug](https://github.com/ilhambagas/Bithug)
- [muhashali/writeup-SSRF](https://github.com/muhashali/writeup-SSRF)
- [jdonsec/allthingsssrf](https://github.com/jdonsec/allthingsssrf)
- [orangetw/My-CTF-Web-Challenges](https://github.com/orangetw/My-CTF-Web-Challenges)


## 비교 대상

| Source | Primitive | Internal target | Result |
| --- | --- | --- | --- |
| `Bithug` | Git webhook SSRF + template injection | localhost repo/admin path | collaborator 권한 획득 후 숨은 repo를 복제합니다. |
| `writeup-SSRF` | URL-to-PDF SSRF | `127.0.0.1:9732` | 내부 서비스 응답이 PDF로 흘러나오며 flag가 드러납니다. |
| `AllThingsSSRF` | Curated SSRF resource hub | many CTF/real-world targets | CTF writeup, talk, lab, and bypass 기법을 한 곳에 모읍니다. |
| `My-CTF-Web-Challenges` | Challenge repo with SSRF idea notes | local NFS/RPC, SSRF-to-RCE chain | SSRF가 다른 프로토콜과 결합될 때의 확장성을 보여줍니다. |
| `H1-2006` | Redirect / internal-service chaining | app, software, staff subdomain | redirect가 사실상 SSRF 브리지 역할을 하며, 로그/토큰 노출과 결합됩니다. |
| `RTFM` | Avatar SSRF + API version mismatch | `/api/v1/secrets` | URL allowlist 부재와 버전 간 인증 불일치가 함께 드러납니다. |

## 공통 패턴

1. **입력값이 외부 URL처럼 보여도 서버가 fetch를 수행합니다.**
   - 이미지 변환, PDF 렌더링, webhook, preview 기능을 특히 의심합니다.
2. **내부 서비스는 루프백/사설 대역에 숨어 있습니다.**
   - `127.0.0.1`, `169.254.169.254`, `10.0.0.0/8` 같은 대상이 자주 나옵니다.
3. **SSRF는 종종 다른 primitive의 시작점입니다.**
   - Git webhook, template injection, local file read, NFS/RPC, admin bot chaining과 연결됩니다.

## writeup별 메모

### 1) Bithug
- Git webhook과 template injection을 결합한 고급 SSRF 체인입니다.
- 핵심은 **localhost로 보내는 요청이 privileged action으로 이어지는지**입니다.
- 연습 포인트:
  - webhook routing 이해
  - 내부 Git repo 접근 경로 추적
  - collaborator/admin 권한 전환

### 2) writeup-SSRF
- URL-to-PDF converter가 외부 입력을 검증하지 않아서 내부 서비스에 접근합니다.
- 결과가 문서/PDF로 되돌아오므로 **정보 유출형 SSRF**를 이해하기 좋습니다.
- 연습 포인트:
  - allowlist/denylist 우회 시나리오
  - loopback 접근
  - 내부 포트 노출 확인

### 3) AllThingsSSRF
- 단일 writeup이 아니라 **SSRF 학습 허브**입니다.
- real-world report, CTF writeup, labs, tool, talk가 한 곳에 모여 있어 재사용성이 높습니다.
- 연습 포인트:
  - CTF만 보지 말고 실제 보고서까지 같이 보기
  - bypass 및 chaining 기법을 따로 정리하기

### 4) My-CTF-Web-Challenges
- `Metamon Verse`처럼 SSRF가 NFS/RPC와 결합되어 RCE로 이어지는 구조를 볼 수 있습니다.
- SSRF는 결국 **내부 요청을 시작할 수 있는 권한**이므로, 다음 단계 프로토콜이 중요합니다.
- 연습 포인트:
  - `gopher://` 같은 비표준 스킴
  - 내부 RPC 프로토콜 이해
  - SSRF → SSTI → RCE 체인 설계

### 5) H1-2006
- redirect와 서브도메인 구조가 내부 서비스 접근 경로를 넓힙니다.
- 로그 노출과 2FA 우회가 결합되며 SSRF가 인증 체인으로 확장됩니다.
- 연습 포인트:
  - open redirect와 SSRF의 경계
  - 내부 서비스 주소 추정
  - 민감 로그 식별

### 6) RTFM
- `avatar` 필드가 외부 URL을 받아 내부 secret endpoint로 fetch합니다.
- API 버전 간 인증 불일치가 SSRF의 파급을 키웁니다.
- 연습 포인트:
  - URL allowlist 검증
  - versioned API 권한 일관성
  - token/session 재사용 방지

## 관련 개념

- `[[ssrf]]`
- `[[ssrf-ctf-patterns]]`
- `[[ssrf-core]]`
- `[[ssrf-defense]]`
- `[[redis-ssrf-command-injection-ctf-patterns]]`
- `[[webrtc-turn-proxying-ctf-patterns]]`
- `[[signed-html-email-ctf-patterns]]`
- `[[path-traversal]]`

## 다음 읽을 거리

- `[[web-ctf-writeup-family-hub]]`
- `[[h1-2006-final-writeup]]`
- `[[rtfm-final-writeup]]`
- `[[url-to-pdf-ssrf-final-writeup]]`
- `[[ssrf-ctf-template]]`
- `[[proxy-mirror-final-writeup]]`
- `[[web-ctf-writeup-internal-service]]`
- `[[bithug-final-writeup]]`

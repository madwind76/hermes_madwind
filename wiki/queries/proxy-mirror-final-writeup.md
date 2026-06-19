---
title: Proxy Mirror — Web SSRF Sample
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, ssrf]
sources: []
confidence: medium
---

# Proxy Mirror — Web SSRF Sample

> **상태**: 샘플 기획서 + 구현 초안
> **분류**: Web CTF
> **핵심 주제**: [[ssrf]], [[ssrf-core]], [[ssrf-defense]], [[ssrf-ctf-patterns]]

## 1. 문제 개요
- 문제명: Proxy Mirror
- 난이도: 중급
- 예상 풀이 시간: 25~45분
- 출제 의도: 서버가 대신 요청하는 기능의 위험성을 체감시키고, URL 정규화·리다이렉트·내부 네트워크 접근의 관계를 익히게 합니다.

## 2. 플레이어가 보는 설명
서버가 대신 URL 내용을 미리 확인해 주는 기능이 있습니다. 입력값을 잘 살펴보고, 서버가 실제로 어떤 대상을 요청하는지 확인해 보세요.

## 3. 의도한 풀이 흐름
1. `/preview?url=...` 기능을 발견합니다.
2. 외부 URL은 정상적으로 불러와지는 것을 확인합니다.
3. `localhost` 문자열 차단만으로는 내부 접근이 막히지 않는다는 점을 확인합니다.
4. 내부 서비스로 향하는 URL 또는 리다이렉트 체인을 사용합니다.
5. 내부 서비스의 `/flag` 응답에서 플래그를 획득합니다.

## 4. 핵심 취약점 메모
- SSRF는 서버를 “요청 대행기”처럼 쓰는 취약점입니다.
- 문자열 기반 차단만 두면 `localhost` 외 내부 호스트, 리다이렉트, 정규화 우회에 취약해집니다.
- 방어는 정규화된 hostname/IP 기준으로 검증하고, redirect 최종 목적지도 재검증해야 합니다.

## 5. 샘플 환경 구성
### 서비스 구성
- `web`: 참가자가 접속하는 미리보기 서비스
- `internal-api`: 내부 전용 플래그 서비스
- `redirector`: 리다이렉트 우회 학습용 보조 서비스

### 네트워크
- 외부 노출: `127.0.0.1:8080`
- 내부 서비스: Docker `internal: true` 네트워크 전용

### Docker Compose 요약
```yaml
# web은 로컬 루프백에만 바인딩합니다.
# internal-api와 redirector는 내부 네트워크에서만 접근 가능합니다.
services:
  web:
    ports:
      - "127.0.0.1:8080:8000"
  internal-api:
    environment:
      - FLAG=CTF{ssrf_internal_service_flag_example}
  redirector:
    # /?to=... 로 최종 목적지를 바꾸는 리다이렉트 보조 서비스
```

## 6. 참가자용 힌트 3단계
- 힌트 1: 서버가 사용자를 대신해 요청을 보내는 기능이 있는지 확인해 보세요.
- 힌트 2: `localhost`만 막는다고 내부 주소 전체를 막을 수는 없습니다.
- 힌트 3: 리다이렉트가 포함되면, 처음 넣은 URL과 최종 요청 대상이 달라질 수 있습니다.

## 7. 운영자 체크 포인트
- 내부 서비스가 외부에서 직접 접근 불가한가
- 리다이렉트 최종 목적지까지 검증하는가
- `file://`, `gopher://` 같은 비의도 스킴이 허용되지 않는가
- 에러 메시지가 내부 호스트명을 과도하게 노출하지 않는가

## 8. 보강 아이디어
- DNS 재해석 우회 방지
- IPv6 루프백 차단
- 사설 대역 차단
- 메타데이터 주소 차단
- allowlist/denylist 정규화 강화

## 9. 연결된 문서
- [[ssrf]]
- [[ssrf-core]]
- [[ssrf-defense]]
- [[ssrf-ctf-template]]
- [[ssrf-ctf-patterns]]

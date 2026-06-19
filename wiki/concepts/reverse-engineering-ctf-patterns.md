---
title: Reverse engineering — CTF patterns
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [ctf, rev, reverse-engineering, automation, windows, wasm, prng, brute-force]
sources: [https://github.com/snwau/picoCTF-2025-Writeup, https://github.com/noamgariani11/picoCTF-2025-Writeup, concepts/custom-cpu-reverse-engineering-ctf-patterns.md, concepts/wasm-reverse-engineering-ctf-patterns.md]
confidence: high
---

# Reverse engineering — CTF patterns

## 1. 정의
**Reverse engineering**은 실행 파일, 스크립트, WASM, 앱 동작을 거꾸로 추적해 내부 규칙과 검증 로직을 복원하는 CTF 패턴입니다.

## 2. 왜 중요한가
- 겉보기엔 웹/윈도우/스크립트 문제처럼 보여도 핵심은 실행 흐름 복원입니다.
- 입력 검증이 아니라 상태 전이, PRNG, 외부 API 호출, 메모리 맵이 본체인 경우가 많습니다.
- 정적인 코드 읽기와 동적 계측을 같이 써야 빠릅니다.

## 3. 대표 하위 패턴
- [[windows-api-instrumentation-ctf-patterns]] — Windows API / Frida / 동적 계측
- [[prng-seed-bruteforce-ctf-patterns]] — 시간 기반 PRNG / 토큰 브루트포스
- [[custom-cpu-reverse-engineering-ctf-patterns]] — 커스텀 CPU / VM 역공학
- [[wasm-reverse-engineering-ctf-patterns]] — WebAssembly 역공학

## 4. 전형적 흐름
1. 정적 분석으로 진입점과 핵심 분기 조건을 찾습니다.
2. 실행 시점이 중요하면 계측 도구로 함수 호출과 반환값을 확인합니다.
3. PRNG, 해시, 암호화, 변환 루틴을 로컬에 재현합니다.
4. 작은 입력 공간은 brute force, 큰 입력 공간은 상태 복원을 우선합니다.

## 5. 같이 보면 좋은 페이지
- [[picoctf-2025-rec-survey]]
- [[windows-api-instrumentation-ctf-patterns]]
- [[prng-seed-bruteforce-ctf-patterns]]
- [[custom-cpu-reverse-engineering-ctf-patterns]]
- [[wasm-reverse-engineering-ctf-patterns]]

## 6. 방어 관점
- 비밀 검증은 클라이언트에 두지 않습니다.
- 동적 계측에 의존하는 로직은 서버측 최종 검증으로 보완합니다.
- 난수는 시간 seed에만 의존하지 않도록 합니다.

---
title: WASM reverse engineering — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, web, wasm, reverse-engineering, javascript, decompilation]
sources: [https://ctftime.org/writeup/27181, https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-3, https://ctftime.org/writeup/27505]
confidence: high
---

# WASM reverse engineering — CTF patterns

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/27181)
- [picoctf2021.haydenhousen.com](https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-3)
- [CTFtime writeup](https://ctftime.org/writeup/27505)

## 1. 정의
**WASM reverse engineering**은 브라우저가 불러온 WebAssembly 모듈을 디컴파일/디스어셈블해서 내부 함수, 상수 배열, 변환 로직을 복원하는 CTF 패턴입니다.

## 2. 왜 중요한가
- Web 문제처럼 보이지만 실제로는 바이너리 리버싱입니다.
- JS 난독화보다 WASM 내부가 핵심인 경우가 많습니다.
- XOR, lookup table, side-channel 같은 로직이 숨겨지는 경우가 많습니다.

## 3. 대표 도구
1. `wabt` / `wasm-decompile`
2. `wasm2wat`
3. Chrome DevTools Network/Sources
4. Burp Suite로 WASM 리소스 캡처
5. 간단한 Python 스크립트로 key array 역연산

## 4. 전형적 분석 흐름
1. JS가 로드하는 `.wasm` 파일을 찾습니다.
2. 디컴파일로 함수 이름과 메모리 구조를 확인합니다.
3. 입력 변환 함수와 상수 배열을 찾습니다.
4. 변환을 역으로 적용해 flag 후보를 복원합니다.
5. 필요하면 로컬에서 같은 로직을 재현합니다.

## 5. 같이 보면 좋은 페이지
- [[some-assembly-required-4-final-writeup]]
- [[some-assembly-required-3-final-writeup]]
- [[some-assembly-required-2-final-writeup]]
- [[custom-cpu-reverse-engineering-ctf-patterns]]

## 6. 방어 관점
- 클라이언트에 비밀 로직을 두지 않습니다.
- 검증과 최종 판정은 서버에서 수행합니다.
- 하드코딩 key, 단순 XOR, 고정 lookup table은 쉽게 복원됩니다.

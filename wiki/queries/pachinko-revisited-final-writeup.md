---
title: Pachinko Revisited — picoCTF 2025 pwn/rev writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, pwn, rev, reverse-engineering, wasm, custom-cpu]
sources: [https://unvariant.pages.dev/writeups/picoctf-2025/pwn-pachinko-revisited/, https://github.com/snwau/picoCTF-2025-Writeup, https://corgi.rip/posts/secure-email-service/]
confidence: medium
---

# Pachinko Revisited — picoCTF 2025 pwn/rev writeup

> `Pachinko`의 후속 문제이지만, 분류는 **Web**이 아니라 **pwn/rev**에 가깝습니다. 커스텀 CPU / WASM / 메모리 맵을 역공학해 `nand_checker.bin`의 실행 경로를 바꾸는 문제로 정리하는 것이 맞습니다.

## 1. 핵심 요약

- 이 문제는 **웹 요청 변조**가 아니라 **바이너리와 실행 모델을 역추적하는 문제**입니다.
- 주어진 환경은 커스텀 CPU 또는 VM처럼 동작하며, WASM 기반 `process` 루틴과 프로그램 바이너리를 함께 분석해야 합니다.
- 핵심 목표는 **프로그램 상태 또는 명령어 스트림을 바꿔 `flag_magic` 경로를 실행하는 것**입니다.

연결 개념: [[custom-cpu-reverse-engineering-ctf-patterns]], [[web-ctf-writeup-topic-map]], [[pachinko-final-writeup]]

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / reverse engineering |
| 핵심 요소 | WASM, custom CPU, state map, program overwrite |
| 주요 바이너리 | `nand_checker.bin`, `flag.bin` |
| 최종 목표 | `flag_magic` 경로 실행 |

## 3. 공격 흐름

1. 서버 JS와 WASM 바이너리에서 입력 포트와 상태 맵을 찾습니다.
2. `process` 루틴을 분석해 레지스터/메모리/포트 의미를 복원합니다.
3. 읽기 전용처럼 보이는 상태와 실제 쓰기 가능한 상태를 구분합니다.
4. `nand_checker.bin`의 검사 로직을 로컬에서 재현하거나 수동으로 추적합니다.
5. 프로그램 메모리나 실행 상태를 조작해 숨은 플래그 분기로 보냅니다.

## 4. 기술 포인트

- **WASM**: 일반 웹앱의 프론트엔드 코드가 아니라, 가상 CPU의 실행 엔진입니다.
- **state map**: 입력/출력/제어 비트가 메모리 오프셋으로 노출됩니다.
- **instruction recovery**: `load_imm`, `load`, `store`, `jmp_if_0`, `nand`, `halt` 같은 동작을 역추적합니다.
- **shared memory abuse**: 프로그램과 데이터가 같은 실행 맥락을 공유하면, 검사 로직 자체를 바꾸는 접근이 가능합니다.

## 5. 방어자 관점

1. 가상 CPU와 사용자 입력을 직접 연결하지 않습니다.
2. 프로그램 영역과 데이터 영역을 분리합니다.
3. 디버그 심볼과 개발용 플래그를 배포판에서 제거합니다.
4. 비정상적인 self-modifying code를 차단합니다.

## 6. 왜 Web이 아닌가

- `Pachinko`는 입력 JSON을 변조하는 문제로 볼 수 있었지만,
- `Pachinko Revisited`는 **실행 모델과 바이너리 의미 복원**이 중심입니다.
- 따라서 Web writeup 묶음에서는 분리하고, **pwn/rev 보조 항목**으로 다루는 편이 맞습니다.

## 7. 같이 보면 좋은 페이지

- [[custom-cpu-reverse-engineering-ctf-patterns]] — 커스텀 CPU / VM 역공학 패턴
- [[pachinko-final-writeup]] — 1차 문제의 요청 변조/상태 관찰 버전
- [[web-ctf-writeup-topic-map]] — Web CTF와의 경계 확인
- [[web-ctf-writeup-curation]] — 큐레이션 기준 참고

## 8. 참고 소스

- [Pachinko Revisited — Unvariant](https://unvariant.pages.dev/writeups/picoctf-2025/pwn-pachinko-revisited/)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)

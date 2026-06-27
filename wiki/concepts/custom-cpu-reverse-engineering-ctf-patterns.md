---
title: custom CPU reverse engineering — picoCTF 패턴
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [ctf, pwn, rev, wasm, reverse-engineering, cpu]
sources: [https://unvariant.pages.dev/writeups/picoctf-2025/pwn-pachinko-revisited/, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: medium
---

# custom CPU reverse engineering — picoCTF 패턴

## 참고 URL
- [unvariant.pages.dev](https://unvariant.pages.dev/writeups/picoctf-2025/pwn-pachinko-revisited/)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)

## Step 1. 단어 풀이
- **Custom CPU**: 일반적인 x86/ARM이 아니라, 문제를 위해 따로 설계된 작은 명령 집합입니다.
- **Reverse engineering**: 실행 중인 동작이나 바이너리를 거꾸로 분석해 내부 규칙을 알아내는 작업입니다.
- **WASM**: 웹에서 실행되는 저수준 바이트코드입니다. CTF에서는 VM/에뮬레이터처럼 쓰이기도 합니다.

## 한 문장 정의
이 패턴은 **커스텀 CPU나 VM이 주어졌을 때, 명령어와 메모리 맵을 역추적한 뒤 입력/상태를 조작해 숨겨진 분기나 플래그 경로를 여는 문제 유형**입니다.

## 핵심 흐름
```text
binary / wasm -> instruction set recovery -> memory map recovery -> local emulator -> state overwrite / control-flow redirection -> hidden flag path
```

## 전문 설명
이 유형의 CTF는 보통 다음 순서로 풀립니다.

1. 바이너리나 WASM에서 `process`, `step`, `execute` 같은 핵심 루프를 찾습니다.
2. 레지스터, 플래그, 메모리 오프셋, 포트 매핑을 정리합니다.
3. 입력이 어디에 저장되고, 어느 상태가 읽기 전용인지 구분합니다.
4. 로컬에서 에뮬레이션하거나 디버깅하면서 명령어 의미를 맞춥니다.
5. 프로그램 자체를 덮어쓰거나, 상태 비트를 조작해 비밀 분기를 강제로 실행합니다.

## 공격자 관점
- 단순 패턴 매칭보다 상태 전이표를 먼저 만듭니다.
- 읽기 전용으로 보이는 상태를 찾으면, 그것이 실제 공격면인지 확인합니다.
- 프로그램 메모리와 데이터 메모리가 분리되지 않았는지 봅니다.
- `flag_magic`, `halt`, `write_enable` 같은 신호가 있으면 우선 확인합니다.

## 방어자 관점
- 커스텀 VM을 외부 입력에 직접 연결하지 않습니다.
- 상태와 프로그램 영역을 분리하고, 쓰기 가능한 범위를 제한합니다.
- 비정상적 프로그램 변경을 검증합니다.
- 에뮬레이터/인터프리터는 디버그용 심볼을 배포판에 포함하지 않습니다.

## Web CTF와의 차이
- Web은 입력 검증, 세션, 브라우저 sink가 핵심입니다.
- 이 패턴은 **명령어 의미 복원과 상태 조작**이 핵심입니다.
- 겉보기엔 퍼즐 같아도 실제론 pwn/rev 문제인 경우가 많습니다.

## 관련 위키 링크
- [[pachinko-revisited-final-writeup]]
- [[web-ctf-writeup-topic-map]]
- [[web-ctf-writeup-curation]]
- [[web-ctf-master-checklist]]

## 참고 소스
- [Pachinko Revisited — Unvariant](https://unvariant.pages.dev/writeups/picoctf-2025/pwn-pachinko-revisited/)
- [picoCTF 2025 Writeup Repository — snwau](https://github.com/snwau/picoCTF-2025-Writeup)

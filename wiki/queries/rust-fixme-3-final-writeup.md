---
title: Rust fixme 3 — picoCTF 2025 general skills writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2025, general-skills, rust, unsafe, writeup]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/Rust-fixme-3.md]
confidence: high
---

# Rust fixme 3 — picoCTF 2025 general skills writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/Rust-fixme-3.md)

## 핵심 요약
- Rust에서 `unsafe` 블록이 필요한 위치를 찾아 감싸는 문제입니다.
- 컴파일 에러 메시지와 주석을 보고 수정 지점을 찾는 유형입니다.

## 풀이 메모
1. unsafe 함수 호출 부분을 찾습니다.
2. 주석에 맞춰 22번, 34번 줄의 `unsafe` 블록을 복원합니다.
3. `cargo run`으로 다시 빌드합니다.
4. 프로그램이 정상 실행되면 플래그를 확인합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2025-general-skills-survey]]
- [[picoctf-2025-general-skills-family-hub]]

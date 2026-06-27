---
title: Rust fixme 1 — picoCTF 2025 general skills writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2025, general-skills, rust, syntax, writeup]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/Rust-fixme-1.md]
confidence: high
---

# Rust fixme 1 — picoCTF 2025 general skills writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/Rust-fixme-1.md)

## 핵심 요약
- Rust 문법 오류를 고쳐서 프로그램이 정상 실행되게 만드는 문제입니다.
- 핵심은 컴파일 에러를 순서대로 고치고 `cargo run`으로 확인하는 것입니다.
- Rust 문법과 출력 포맷 수정이 포인트입니다.

## 풀이 메모
1. 5번째 줄에 세미콜론을 추가합니다.
2. `ret`를 `return`으로 바꿉니다.
3. `:?`를 `{}`로 바꿉니다.
4. `cargo run`으로 빌드를 다시 실행해 플래그를 확인합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2025-general-skills-survey]]
- [[picoctf-2025-general-skills-family-hub]]

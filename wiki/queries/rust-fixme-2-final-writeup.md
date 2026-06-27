---
title: Rust fixme 2 — picoCTF 2025 general skills writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2025, general-skills, rust, borrow-checker, writeup]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/Rust-fixme-2.md]
confidence: high
---

# Rust fixme 2 — picoCTF 2025 general skills writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/Rust-fixme-2.md)

## 핵심 요약
- Rust의 소유권/가변 참조/패턴 매칭 오류를 고치는 문제입니다.
- `cargo run`으로 컴파일 에러를 반복 확인하면서 수정합니다.

## 풀이 메모
1. 함수 인자를 `borrowed_string: &mut String`으로 맞춥니다.
2. `XORCryptor::new(&key)` 결과를 `if let Ok(xrc) = res`로 받습니다.
3. `let mut party_foul = ...`로 바꾸고 `decrypt(encrypted_buffer, &mut party_foul);`처럼 전달합니다.
4. 다시 `cargo run`을 실행해 플래그를 확인합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2025-general-skills-survey]]
- [[picoctf-2025-general-skills-family-hub]]

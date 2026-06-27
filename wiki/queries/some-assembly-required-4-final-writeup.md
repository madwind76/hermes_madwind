---
title: Some Assembly Required 4 — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, javascript, wasm, reverse-engineering, picoctf]
sources: [https://ctftime.org/task/15358, https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-4, https://github.com/nornorhub/some_assembly_required_4, https://www.youtube.com/watch?v=EsnzsnIN0YI]
confidence: high
---

# Some Assembly Required 4 — picoCTF 2021 web writeup

> `Some Assembly Required 4`는 **WebAssembly(WASM) 모듈의 변환 루틴을 되돌리고, 브루트포스/오라클 형태로 flag를 복원하는 picoCTF 2021 Web 문제**입니다. 전작보다 더 직접적으로 `wasmtime`/`WABT`를 사용해 내부 변환을 재현하는 흐름이 핵심입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/task/15358)
- [picoctf2021.haydenhousen.com](https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-4)
- [nornorhub/some_assembly_required_4](https://github.com/nornorhub/some_assembly_required_4)
- [www.youtube.com](https://www.youtube.com/watch?v=EsnzsnIN0YI)


## 1. 한 줄 요약
- 페이지는 JS와 WASM 모듈을 로드합니다.
- 변환 루틴은 WASM 내부에 있습니다.
- C-like WASM 코드를 분석해 역함수를 만듭니다.
- 필요한 경우 brute force를 통해 flag를 복원합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | JS가 WASM을 불러옴 | 실제 로직이 브라우저 리소스에 숨어 있음 |
| 2 | WASM 안에 encryption routine이 존재 | 입력/출력 관계를 분석해야 함 |
| 3 | 디컴파일 결과가 C 유사 코드로 보임 | 로직 재구성이 쉬워짐 |
| 4 | 일부 구간은 brute force 가능 | side-channel 또는 오라클처럼 활용 가능 |
| 5 | 역연산 스크립트를 작성 | flag 획득 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 단순한 웹 페이지가 아니라, **WASM 변환 루틴을 로컬에서 재현해 역으로 푸는 문제**입니다. 브라우저에서 보이는 UI보다, 모듈이 수행하는 연산의 역함수를 만드는 것이 중요합니다.

### 3.2 실전 확인 포인트
```bash
# Burp로 JS와 WASM 요청을 확인합니다.
# 예상 결과: /index.html 외에 wasm 바이너리와 관련 JS 요청이 보입니다.
```

```bash
# WABT/wasmtime로 WASM 로직을 재현하거나 디컴파일합니다.
# 예상 결과: encryption routine과 key handling 로직이 드러납니다.
```

## 4. 공격자 관점
- WASM 내부의 연산은 브라우저에 있어도 숨겨진 게 아닙니다.
- 디컴파일 결과를 Python/JS로 옮겨 역연산하면 됩니다.
- brute force가 가능한 경우, 일부 상태만 맞추는 오라클처럼 사용할 수 있습니다.

## 5. 방어자 관점
- 클라이언트에 있는 WASM 로직은 비밀이 아닙니다.
- 검증과 최종 판정은 서버에서 수행해야 합니다.
- 변환 함수가 단순하면 key recovery가 매우 빠르게 가능합니다.

## 6. 같이 보면 좋은 페이지
- [[some-assembly-required-3-final-writeup]]
- [[wasm-reverse-engineering-ctf-patterns]]
- [[custom-cpu-reverse-engineering-ctf-patterns]]

## 7. 참고 소스
- [CTFtime — Some Assembly Required 4](https://ctftime.org/task/15358)
- [PicoCTF-2021 Writeup — Some Assembly Required 4](https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-4)
- [nornorhub — some_assembly_required_4](https://github.com/nornorhub/some_assembly_required_4)
- [YouTube — Some Assembly Required 4](https://www.youtube.com/watch?v=EsnzsnIN0YI)

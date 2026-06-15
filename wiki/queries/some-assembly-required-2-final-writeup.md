---
title: Some Assembly Required 2 — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, javascript, wasm, reverse-engineering, picoctf]
sources: [https://ctftime.org/writeup/27180, https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-2, https://medium.com/@abdullahimtiazyousafzai/some-assembly-required-2-picoctf-writeup-0e45b0bf2390]
confidence: high
---

# Some Assembly Required 2 — picoCTF 2021 web writeup

> `Some Assembly Required 2`는 **난독화된 JavaScript가 WebAssembly(WASM) 모듈을 로드하고, 입력을 XOR-8으로 변환한 뒤 비교하는 picoCTF 2021 Web 문제**입니다. 전작과 비슷하지만, 이번에는 **WASM 내부의 변환 로직과 암호화된 기대 문자열**을 되돌리는 것이 핵심입니다.

## 1. 한 줄 요약
- 페이지는 JS와 WASM 파일을 로드합니다.
- `copy_char`가 입력 바이트를 `8`로 XOR합니다.
- WASM 메모리의 숨은 문자열도 같은 방식으로 난독화되어 있습니다.
- 해당 문자열을 XOR-8로 다시 풀면 flag가 나옵니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 간단한 입력 폼이 보임 | UI는 단순합니다 |
| 2 | JS가 별도 WASM 리소스를 가져옴 | 실제 로직은 WASM에 있음 |
| 3 | 입력 글자가 `copy_char`로 전달됨 | 문자 단위 변환 발생 |
| 4 | `i32.xor`로 `8`과 XOR됨 | 핵심 오프셋/변환 |
| 5 | WASM 메모리의 상수 문자열을 확보 | 기대 flag 후보 |
| 6 | 같은 XOR-8을 역으로 적용 | flag 복원 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 Web 취약점이지만 실질적으로는 **웹 리소스 분석 + WASM 리버싱** 문제입니다. 문자열 하나만 보는 것이 아니라, **브라우저가 로드하는 JS와 WASM의 역할 분담**을 분리해서 봐야 합니다.

### 3.2 실전 확인 포인트
```bash
# Burp로 JS와 WASM 요청을 확인합니다.
# 예상 결과: /index.html 외에 obfuscated JS와 wasm 바이너리 요청이 보입니다.
```

```bash
# XOR-8 변환은 파이썬 한 줄로 되돌릴 수 있습니다.
# 예상 결과: 숨은 문자열이 picoCTF{...} 형태로 복원됩니다.
```

### 3.3 풀이 흐름
1. 페이지를 열고 네트워크 요청을 캡처합니다.
2. 난독화된 JS를 beautify합니다.
3. JS가 가져오는 WASM 파일을 찾습니다.
4. WASM을 디컴파일하거나 텍스트로 변환합니다.
5. `copy_char`와 비교 로직을 확인합니다.
6. 숨은 문자열에 XOR-8을 적용해 flag를 복원합니다.

## 4. 공격자 관점
- 표면의 입력 체크보다 **리소스와 바이트코드**를 먼저 봐야 합니다.
- `i32.xor` 상수는 매우 중요한 단서입니다.
- 같은 변환을 입력과 기대 문자열 모두에 적용하는 경우, 역연산만 알면 쉽게 풀립니다.

## 5. 방어자 관점
- 클라이언트 배포물에 검증 비밀을 두지 않습니다.
- 난독화된 JS/WASM은 가림막일 뿐이므로, 중요한 검증은 서버에서 수행해야 합니다.
- 디버깅용/실험용 엔드포인트는 배포 전에 제거해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[some-assembly-required-1-final-writeup]]
- [[webdecode-final-writeup]]
- [[source-inspection-minification-ctf-patterns]]
- [[custom-cpu-reverse-engineering-ctf-patterns]]
- [[web-ctf-writeup-curation]]

## 7. 참고 소스
- [CTFtime — Some Assembly Required 2](https://ctftime.org/writeup/27180)
- [PicoCTF-2021 Writeup — Some Assembly Required 2](https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-2)
- [0xSudo — Some Assembly Required 2 PicoCTF — Writeup](https://medium.com/@abdullahimtiazyousafzai/some-assembly-required-2-picoctf-writeup-0e45b0bf2390)

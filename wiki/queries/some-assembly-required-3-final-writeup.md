---
title: Some Assembly Required 3 — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, javascript, wasm, reverse-engineering, picoctf]
sources: [https://ctftime.org/writeup/27181, https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-3, https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Some_Assembly_Required_3.md]
confidence: high
---

# Some Assembly Required 3 — picoCTF 2021 web writeup

> `Some Assembly Required 3`는 **WebAssembly(WASM) 코드를 디컴파일해 XOR 기반 변환을 되돌리는 picoCTF 2021 Web 문제**입니다. 전작보다 한 단계 더 나아가, 브라우저가 불러온 WASM 내부 로직을 읽고 key array를 역으로 적용해야 합니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/27181)
- [picoctf2021.haydenhousen.com](https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-3)
- [Original writeup](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Some_Assembly_Required_3.md)


## 1. 한 줄 요약
- 페이지는 JS와 WASM 모듈을 로드합니다.
- 핵심 로직은 WASM 안에 있습니다.
- `copy` 함수가 입력값을 XOR 기반으로 변환합니다.
- 키 배열을 복원해 flag를 얻습니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 페이지 소스는 평범해 보임 | 실제 로직은 JS/WASM 뒤에 숨어 있음 |
| 2 | WASM 파일을 가져옴 | 디컴파일 필요 |
| 3 | `copy` 또는 유사 함수가 보임 | 값 변환 함수 식별 |
| 4 | key array가 하드코딩되어 있음 | XOR 복원 가능 |
| 5 | 변환을 역으로 적용 | flag 문자열 획득 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 단순히 "웹 페이지를 본다"가 아니라, **WASM을 별도의 바이너리처럼 다뤄야 하는 문제**입니다. JS 난독화보다 한 단계 더 깊게, 디컴파일과 제어 흐름 복원이 필요합니다.

### 3.2 실전 확인 포인트
```bash
# Burp로 JS와 WASM 요청을 확인합니다.
# 예상 결과: /index.html 외에 obfuscated JS와 wasm 바이너리 요청이 보입니다.
```

```bash
# wasm-decompile 또는 wabt 도구로 WebAssembly를 사람이 읽을 수 있게 변환합니다.
# 예상 결과: copy 함수와 key array가 드러납니다.
```

## 4. 공격자 관점
- WASM은 브라우저 안에 있어도 네이티브 바이너리처럼 분석할 수 있습니다.
- XOR 기반 변환은 key와 연산을 찾아내면 쉽게 역산됩니다.
- 보이는 UI보다 로드된 리소스와 내부 함수가 더 중요합니다.

## 5. 방어자 관점
- 클라이언트에 숨긴 WASM 로직은 비밀이 아닙니다.
- 검증은 서버에서 수행해야 합니다.
- 단순 XOR, 하드코딩 key array, 브라우저 측 비교만으로는 충분하지 않습니다.

## 6. 같이 보면 좋은 페이지
- [[some-assembly-required-2-final-writeup]]
- [[custom-cpu-reverse-engineering-ctf-patterns]]
- [[webdecode-final-writeup]]

## 7. 참고 소스
- [CTFtime — Some Assembly Required 3](https://ctftime.org/writeup/27181)
- [PicoCTF-2021 Writeup — Some Assembly Required 3](https://picoctf2021.haydenhousen.com/web-exploitation/some-assembly-required-3)
- [Dvd848 — Some Assembly Required 3](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Some_Assembly_Required_3.md)

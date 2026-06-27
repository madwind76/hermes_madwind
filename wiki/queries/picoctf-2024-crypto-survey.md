---
title: picoCTF 2024 crypto survey
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/README.md, https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main/Cryptography]
confidence: medium
---

# picoCTF 2024 crypto survey

> 결론부터 말씀드리면, **picoCTF 2024에는 Crypto 문제가 5개 확인됩니다.**
> 공개 writeup 저장소의 Cryptography 디렉터리와 README 기준으로 `interencdec`, `Custom encryption`, `C3`, `rsa_oracle`, `flag_printer`가 보입니다.

## 참고 URL
- [picoCTF 2024 Writeup README](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/README.md)
- [picoCTF 2024 Cryptography directory](https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main/Cryptography)

## 1. 확인 결과
| Challenge | 상태 | 한 줄 요약 | 비고 |
| --- | --- | --- | --- |
| interencdec | Solved | 다중 인코딩(Base64 + ROT/Caesar) | 공개 해설 존재 |
| Custom encryption | Solved | DH/멀티플라이/XOR 조합 복호화 | 공개 해설 존재 |
| C3 | Solved | lookup table 기반 cyclical cipher 역변환 | 공개 해설 존재 |
| rsa_oracle | Solved | RSA oracle chosen-plaintext attack | 공개 해설 존재 |
| flag_printer | Present | BMP/계수 복원형 문제로 보이는 공개 해설 페이지 존재 | repo writeup 파일은 비어 있음 |

## 2. 핵심 포인트
1. `interencdec`와 `C3`는 **인코딩/치환의 역변환**이 핵심입니다.
2. `Custom encryption`과 `rsa_oracle`은 **구현 취약점과 공격 오라클**이 핵심입니다.
3. `flag_printer`는 공개 솔루션 페이지는 확인되지만, 이 저장소의 `flag_printer.md`는 현재 비어 있습니다.
4. 따라서 4개는 상세 writeup, 1개는 존재 확인/문제 분류 노트로 정리하는 편이 가장 자연스럽습니다.

## 3. 공개 writeup 수집
| Challenge | 공개 writeup / 참고 | 메모 |
| --- | --- | --- |
| interencdec | [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-interencdec), [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/interencdec.md) | Base64 2중 디코딩 + Caesar/ROT13 |
| Custom encryption | [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-custom-encryption), [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/Custom-encryption.md) | DH + multiplication + XOR 계층 복호화 |
| C3 | [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-c3), [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/C3.md) | cyclical cipher / lookup table inverse |
| rsa_oracle | [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-rsa_oracle), [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/rsa_oracle.md) | chosen-plaintext oracle attack |
| flag_printer | [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-flag-printer), [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/flag_printer.md) | 공개 페이지는 있으나 repo writeup은 비어 있음 |

## 4. 다시 묶는 기준
- `interencdec` → **multi-encoding / ROT / Base64**
- `C3` → **custom substitution / cyclical cipher**
- `Custom encryption` → **custom crypto / reverse engineering**
- `rsa_oracle` → **RSA oracle / chosen-plaintext**
- `flag_printer` → **bitmap / coefficient reconstruction**

## 5. 묶음 페이지
- [[picoctf-2024-crypto-family-hub]]
- [[interencdec-final-writeup]]
- [[custom-encryption-final-writeup]]
- [[c3-final-writeup]]
- [[rsa-oracle-final-writeup]]
- [[flag-printer-final-writeup]]

## 6. 관련 페이지
- [[picoctf-2024-topic-map]]
- [[crypto-writeup-family-hub]]
- [[crypto-primitive-writeup-survey]]
- [[picoctf-web-survey]]

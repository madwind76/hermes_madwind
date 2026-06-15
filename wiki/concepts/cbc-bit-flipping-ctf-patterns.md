---
title: CBC bit flipping — Web CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, crypto, cbc, bit-flipping, malleability, cookies]
sources: [https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md, https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md, https://www.youtube.com/watch?v=i9KiOjeE-VY]
confidence: high
---

# CBC bit flipping — Web CTF patterns

## 1. 정의
**CBC bit flipping**은 CBC(Cipher Block Chaining) 모드의 말변성(malleability)을 이용해, 이전 ciphertext 블록의 비트를 바꿔 다음 블록의 평문 일부를 원하는 값으로 조작하는 패턴입니다. Web CTF에서는 암호화된 쿠키, 세션 토큰, role 문자열 조작에 자주 등장합니다.

## 2. 쉬운 비유
CBC는 여러 장의 종이를 겹쳐 복사하는 방식과 비슷합니다. 앞 장에 낙서를 하면 다음 장의 글자가 조금씩 틀어집니다. 공격자는 이 성질을 이용해, **앞 장을 살짝 비틀어 뒷 장의 특정 글자를 원하는 문자로 바꾸는** 식의 조작을 시도합니다.

## 3. 자주 보이는 단서
| 단서 | 의미 |
|------|------|
| 쿠키 값이 Base64처럼 보이지만 내용이 읽히지 않음 | 암호문일 가능성 |
| 설명에 `encrypt`, `secure`, `CBC` 같은 단어가 있음 | 암호화 방식 힌트 |
| 서버가 `admin`, `role`, `auth` 등 문자열 기반 분기를 가짐 | 평문 조작 표적 |
| 무결성 검증/MAC 언급이 없음 | 변조 가능성 |

## 4. 기본 풀이 루프
```text
1) 쿠키를 디코딩해 ciphertext를 얻습니다.
2) 블록 경계를 확인합니다.
3) 이전 블록의 bit를 하나씩 뒤집습니다.
4) 서버 응답이 달라지는지 관찰합니다.
5) 성공하면 해당 변조 지점을 기록합니다.
```

## 5. 공격자 관점
1. 암호문이 어느 블록으로 나뉘는지 확인합니다.
2. 목표 문자열이 들어 있을 것으로 예상되는 위치를 추측합니다.
3. 이전 블록의 대응 비트를 XOR로 뒤집습니다.
4. 변조된 쿠키를 재전송합니다.
5. admin 페이지나 flag 응답이 뜨는 지점을 찾습니다.

## 6. 방어자 관점
- 암호화만으로는 무결성이 보장되지 않습니다.
- 쿠키/토큰에는 반드시 서명 또는 AEAD를 사용합니다.
- 권한 값은 클라이언트에 두지 않고 서버에서 관리합니다.
- 변조된 ciphertext는 복호화 전에 거부해야 합니다.

## 7. 같이 보면 좋은 페이지
- [[more-cookies-final-writeup]]
- [[cookie-client-storage-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]

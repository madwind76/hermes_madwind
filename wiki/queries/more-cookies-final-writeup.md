---
title: More Cookies — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, cookies, crypto, cbc, bit-flipping, flask-session]
sources: [https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md, https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md, https://www.youtube.com/watch?v=i9KiOjeE-VY, https://ctftime.org/task/15305]
confidence: high
---

# More Cookies — picoCTF 2021 web writeup

> `More Cookies`는 **암호화된 쿠키가 있어도, CBC의 말변성(malleability)을 이용하면 내용 일부를 조작할 수 있다**는 점을 보여주는 문제입니다.

## 참고 URL
- [Original writeup](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md)
- [Original writeup](https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md)
- [www.youtube.com](https://www.youtube.com/watch?v=i9KiOjeE-VY)
- [CTFtime writeup](https://ctftime.org/task/15305)


## 1. 한 줄 요약
- 쿠키 이름은 `auth_name`입니다.
- 값은 Base64로 한 번 더 감싸져 있지만, 본질은 **암호문(ciphertext)** 입니다.
- 핵심은 **CBC bit flipping**으로 관리자 상태를 유도하는 것입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 문제 설명에 `Cookies can Be modified Client-side` | 쿠키 변조가 핵심임을 암시 |
| 2 | `encrypt them!` | 평문 쿠키가 아니라 암호화된 쿠키 사용 |
| 3 | `auth_name` 쿠키 발견 | 조작 대상 식별 |
| 4 | Base64 decode | 레이어 1 제거 |
| 5 | 다시 decode/검사해도 읽기 어려움 | 단순 인코딩이 아니라 암호화임을 확인 |
| 6 | CBC bit flipping 적용 | 평문 일부를 바꾸는 공격 |
| 7 | admin 상태 유도 | flag 획득 |

## 3. 핵심 분석
이 문제는 **암호화를 했다는 사실만으로 클라이언트 저장값이 안전해지지 않는다**는 점을 보여줍니다.

- `auth_name`은 사용자 상태를 담는 쿠키입니다.
- 단순히 암호화되어 있어도, 복호화 후 서버가 해석하는 문자열 구조가 예측 가능하면 공격이 가능합니다.
- CBC 모드에서는 이전 블록의 비트 조작이 다음 블록 평문에 영향을 줍니다.
- 따라서 공격자는 원하는 문자열(`admin` 등)에 맞춰 ciphertext를 비틀 수 있습니다.

### 대표 스크립트 아이디어
```python
# 쿠키를 base64로 디코딩한 뒤, CBC bit flipping을 시도합니다.
# 예상 결과: 특정 bit flip 조합에서 admin 상태가 유도되고 flag가 반환됩니다.
import base64
import requests

# 세션을 만든 뒤 auth_name 쿠키를 가져옵니다.
s = requests.Session()
s.get("http://mercury.picoctf.net:15614/")
cookie = s.cookies["auth_name"]

# Base64를 두 번 풀어 실제 ciphertext를 얻습니다.
raw = base64.b64decode(base64.b64decode(cookie))
```

## 4. 공격자 관점
1. 쿠키의 인코딩 레이어를 제거합니다.
2. 암호문 길이와 블록 경계를 확인합니다.
3. 한 비트씩 바꿔가며 서버 반응을 관찰합니다.
4. `admin` 또는 권한 분기 문자열이 바뀌는 지점을 찾습니다.
5. flag가 노출되는 응답을 찾습니다.

## 5. 방어자 관점
- 클라이언트 쿠키에 민감한 상태를 넣지 않습니다.
- 암호화만 하지 말고 **무결성 검증**까지 포함해야 합니다.
- 가능하면 서버 측 세션으로 상태를 관리합니다.
- 암호문을 조작해도 검증에서 걸러지도록 서명/MAC를 적용합니다.

## 6. 같이 보면 좋은 페이지
- [[cookie-client-storage-ctf-patterns]]
- [[cbc-bit-flipping-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[power-cookie-final-writeup]]

## 7. 참고 소스
- [HHousen — More Cookies README](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md)
- [apoirrier — MostCookies.md](https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md)
- [YouTube walkthrough](https://www.youtube.com/watch?v=i9KiOjeE-VY)
- [CTFtime task page](https://ctftime.org/task/15305)

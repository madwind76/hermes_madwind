---
title: Local Authority — picoCTF web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, client-side, javascript, source-inspection, login, secrets, curl]
sources: [https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c, https://medium.com/@rachael_muga/picoctf-local-authority-web-exploitation-4eb654fa9702, https://hackmd.io/@sunfrancis12/HJpCC9Sph]
confidence: high
---

# Local Authority — picoCTF web writeup

> 겉보기에는 평범한 로그인 문제지만, 실제 핵심은 **클라이언트 측 `secure.js`** 에 숨겨진 인증 로직과 하드코딩된 자격 증명입니다.
> DevTools로 JS를 열어보면 `checkPassword` 흐름과 관리자 해시를 바로 확인할 수 있습니다.

## 참고 URL
- [medium.com](https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c)
- [medium.com](https://medium.com/@rachael_muga/picoctf-local-authority-web-exploitation-4eb654fa9702)
- [hackmd.io](https://hackmd.io/@sunfrancis12/HJpCC9Sph)


## 1. 한 줄 요약
- UI는 평범한 로그인 폼처럼 보이지만, 실제 정답은 **`secure.js` / `login.php` 소스**에 있습니다.
- `window.username`, `window.password`, `checkPassword()` 같은 값이 **평문**으로 노출됩니다.
- 성공 후에는 숨은 admin hash를 POST로 보내는 구조라서, 핵심은 **source inspection + request replay** 입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 시도 실패 | 정상 인증이 아닌 로직 검사가 존재 |
| 2 | DevTools / View Source 확인 | 클라이언트 JS에 단서가 있을 가능성 |
| 3 | `secure.js` 발견 | 외부 스크립트에 인증 로직 포함 |
| 4 | 평문 자격 증명 / admin hash 확인 | 소스 유출로 우회 가능 |
| 5 | `admin.php`로 POST 재현 | flag 획득 |

## 3. 대표 분석 예시
```bash
# CTF 환경에서 admin 페이지로 필요한 hash 값을 직접 전송합니다.
# 예상 결과: 인증 성공 또는 flag가 포함된 응답이 반환됩니다.
curl -X POST http://<challenge-host>/admin.php \
  --data 'hash=2196812e91c29df34f5e217cfd639881'
```

## 4. 공격자 관점
1. 로그인 폼 입력 전에 HTML과 JS 링크를 확인합니다.
2. `secure.js`처럼 외부로 분리된 스크립트를 열어봅니다.
3. `checkPassword`, `window.username`, `window.password`를 찾습니다.
4. 로그인 성공 후 전송되는 `hash` 값을 확인합니다.
5. 필요하면 브라우저 대신 `curl`로 POST를 재현합니다.

## 5. 방어자 관점
- 인증 로직과 비밀값을 클라이언트 JS에 두지 않습니다.
- `secure.js`처럼 접근 가능한 정적 파일에 평문 자격 증명을 넣지 않습니다.
- 화면상으로 숨겼더라도 브라우저가 받는 이상 비밀이 아닙니다.
- 인증 성공 조건은 서버에서 검증해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[client-side-secret-exposure-ctf-patterns]]
- [[login-final-writeup]]
- [[source-inspection-minification-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]

## 7. 참고 소스
- [Robert Simpson — PicoCTF: Local Authority](https://medium.com/@rwsimpson99/picoctf-local-authority-9026cd92436c)
- [Rachael Muga — PicoCTF: Local Authority (Web Exploitation)](https://medium.com/@rachael_muga/picoctf-local-authority-web-exploitation-4eb654fa9702)
- [picoCTF Local Authority — HackMD](https://hackmd.io/@sunfrancis12/HJpCC9Sph)

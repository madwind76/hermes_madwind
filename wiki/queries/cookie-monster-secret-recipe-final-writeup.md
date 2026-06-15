---
title: Cookie Monster Secret Recipe — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, research, writeup, auth, session, encoding]
sources: [https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/Cookie%20Monster%20Secret%20Recipe/Cookie%20Monster%20Secret%20Recipe.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-cookie-monster-secret-recipe-4c1776da9251, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/]
confidence: high
---

# Cookie Monster Secret Recipe — picoCTF 2025 web writeup

> 브라우저 쿠키에 숨겨진 값을 찾아 `URL decode → Base64 decode` 순서로 복원하는 picoCTF 2025 Web Exploitation 입문 문제입니다.

## 1. 한 줄 요약
- 로그인 폼에 임의 값을 넣으면 실패 응답과 함께 **쿠키를 확인하라**는 힌트가 나옵니다.
- 브라우저 개발자 도구의 Cookies 저장소에서 `secret_recipe` 쿠키를 찾습니다.
- 쿠키 값은 URL 인코딩된 Base64 문자열이므로, URL decode 후 Base64 decode하면 flag 형식 문자열이 복원됩니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 카테고리 | Web Exploitation |
| 점수 | 50 |
| 핵심 아이디어 | cookie inspection, URL decoding, Base64 decoding |
| 난이도 | easy / beginner |
| 관련 개념 | [[cookie-client-storage-ctf-patterns]], [[base64-decoding-ctf-patterns]], [[web-ctf-writeup-auth-session]] |

## 3. 공격면 정리
| Route / 위치 | Method | Auth | Input | Output | Notes |
|---|---|---|---|---|---|
| `/` 또는 `index.html` | GET | No | 없음 | 로그인 폼 | 사용자명·비밀번호 입력 화면 |
| `login.php` | POST | No | username, password | Access Denied + 힌트 | “Me no need password. Me just need cookies!” |
| Browser Cookies | Client-side storage | No | `secret_recipe` cookie | 인코딩된 문자열 | URL 인코딩 + Base64 조합 |

## 4. 풀이 흐름
1. 문제 페이지를 열고 로그인 폼을 확인합니다.
2. 임의의 username/password를 제출합니다.
3. 실패 응답에서 다음 힌트를 확인합니다.
   - `Have you checked your cookies lately?`
   - `Me no need password. Me just need cookies!`
4. 브라우저 개발자 도구에서 `Storage` 또는 `Application` 탭의 `Cookies`를 엽니다.
5. `secret_recipe` 쿠키 값을 복사합니다.
6. `%3D` 같은 URL 인코딩 문자를 먼저 복원합니다.
7. 복원된 Base64 문자열을 디코딩해 flag 형식 문자열을 확인합니다.

## 5. 재현용 디코딩 예시
아래 명령은 **문제에서 얻은 쿠키 값을 로컬에서 디코딩하는 교육용 예시**입니다. 실제 값은 문제 인스턴스 또는 공개 writeup에 따라 다를 수 있습니다.

```bash
# URL 인코딩을 먼저 해제한 뒤 Base64를 디코딩합니다.
# 예상 출력: picoCTF{...} 형식의 문자열이 출력됩니다.
python3 - <<'PY'
from urllib.parse import unquote  # URL 인코딩 해제 함수입니다.
import base64                    # Base64 디코딩 모듈입니다.

cookie_value = "cGljb0NURnt...%3D%3D"  # 브라우저 쿠키에서 복사한 secret_recipe 값을 넣습니다.
url_decoded = unquote(cookie_value)     # %3D 같은 URL 인코딩 문자를 '=' 등으로 복원합니다.
plain = base64.b64decode(url_decoded).decode()  # Base64 문자열을 원문으로 복원합니다.
print(plain)  # 예상 출력: picoCTF{...}
PY
```

## 6. 핵심 학습 포인트
- **인코딩은 암호화가 아닙니다.** Base64는 숨김이 아니라 표현 변환입니다.
- 클라이언트 쿠키는 사용자가 읽을 수 있으므로, 민감 정보 저장 위치로 부적절합니다.
- 로그인 실패처럼 보이는 응답도 쿠키·헤더·스토리지 변화를 남길 수 있습니다.
- Web CTF에서는 HTML/응답 본문만 보지 말고 브라우저 저장소까지 확인해야 합니다.

## 7. 방어 관점
- flag, secret, role, user id 같은 민감 값은 클라이언트 쿠키에 직접 저장하지 않습니다.
- 쿠키에는 불투명한 세션 식별자만 저장하고, 실제 권한·비밀 값은 서버 측에서 조회합니다.
- 쿠키 기반 상태가 필요하면 서명·만료·서버 검증을 적용합니다.
- `HttpOnly`, `Secure`, `SameSite` 설정을 사용하되, 이 속성이 단순 인코딩된 비밀 노출을 해결한다고 오해하지 않아야 합니다.

## 8. 관련 위키 링크
- [[cookie-client-storage-ctf-patterns]] — 쿠키 저장소를 Web CTF 공격면으로 보는 패턴
- [[base64-decoding-ctf-patterns]] — Base64 판별·디코딩 체크리스트
- [[web-ctf-writeup-auth-session]] — 인증/세션/권한 문제 허브
- [[web-ctf-writeup-curation]] — Web CTF writeup 큐레이션
- [[web-ctf-writeup-topic-map]] — Web CTF 상위 지도
- [[intro-to-burp-final-writeup]] — 브라우저/프록시 도구 활용 입문 문제

## 9. 참고 소스
- [snwau GitHub writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/Cookie%20Monster%20Secret%20Recipe/Cookie%20Monster%20Secret%20Recipe.md)
- [Kamal S Medium writeup](https://medium.com/@Kamal_S/picoctf-web-exploitation-cookie-monster-secret-recipe-4c1776da9251)
- [qz.sg picoCTF 2025 Web Exploitation writeups](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)

## 10. 다음 연결
- `WebDecode`와 함께 보면 “브라우저에 이미 노출된 값을 인코딩 해제하는 문제” 계열을 비교할 수 있습니다.
- `IntroToBurp`와 함께 보면 프록시/브라우저 개발자 도구로 요청·저장소를 함께 보는 습관을 만들 수 있습니다.

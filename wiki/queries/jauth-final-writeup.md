---
title: JAuth — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, jwt, authentication, token-forgery, picoctf]
sources: [https://brandon-t-elliott.github.io/ctf-challenge-writeup-picoctf-jauth, https://www.probablynotimportant.com/posts/2021-08-17-picoctf2021-jauth, https://github.com/faisalmemon/picoCTF-JAuth-writeup, https://www.youtube.com/watch?v=VpsGAv5fwDQ]
confidence: high
---

# JAuth — picoCTF 2021 web writeup

> `JAuth`는 **JWT 시크릿이 너무 약해서 관리자 토큰을 위조할 수 있는 picoCTF 2021 Web 문제**입니다. 공개 writeup들은 공통적으로 소스 코드에서 시크릿 생성 로직을 확인하고, `1234` 같은 기본값을 이용해 관리자 권한 토큰을 다시 서명하는 흐름을 보여줍니다.

## 1. 한 줄 요약
- 로그인용 계정(`user:user`)으로 먼저 접속합니다.
- 요청 헤더의 `Authorization: Bearer ...` 또는 로컬 저장소 토큰을 확인합니다.
- 소스 코드에서 JWT 서명 키를 찾습니다.
- `SecretGenerator`가 약한 기본값을 반환하는 분기를 확인합니다.
- 관리자 권한 클레임으로 토큰을 재서명해 `admin` 기능에 접근합니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 제공된 일반 계정으로 로그인 가능 | 인증 자체는 통과 가능 |
| 2 | JWT/Bearer 토큰 사용 | 상태는 토큰에 저장됨 |
| 3 | 소스에서 JWT 서명 키 생성 로직 발견 | 시크릿 유출 후보 |
| 4 | fallback 키가 매우 약함 | 토큰 위조 가능 |
| 5 | role / email / userId 변경 가능 | 관리자 권한 상승 지점 |
| 6 | 새 토큰으로 보호된 페이지 접근 | flag 획득 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
JWT는 “서명된 정보”이기 때문에, 서명 키가 안전해야 합니다. 이 문제는 소스 코드가 공개된 상황에서 **서명 키가 하드코딩 fallback으로 노출**되어 있어, 공격자가 정상 토큰 구조를 유지한 채 권한 클레임만 바꿔 다시 서명할 수 있습니다.

### 3.2 소스 분석 포인트
```bash
# JWT 관련 소스 파일을 찾습니다.
# 예상 결과: JwtService.java, SecretGenerator.java, Role.java 등이 확인됩니다.
grep -R "jwt\|secret\|role\|admin" .
```

```bash
# 서명 키 생성 로직을 찾습니다.
# 예상 결과: fallback secret 또는 하드코딩 문자열이 보입니다.
grep -R "1234\|server_secret\|SECRET_KEY" .
```

### 3.3 토큰 위조 흐름
1. 토큰을 디코딩합니다.
2. `role`을 `Admin`으로 바꿉니다.
3. 필요하면 `userId`와 `email`도 맞춥니다.
4. 시크릿 `1234`로 다시 서명합니다.
5. 토큰을 `auth-token` 저장소 또는 요청 헤더에 넣습니다.
6. 관리자 전용 페이지를 새로고침합니다.

## 4. 공격자 관점
1. 소스에서 JWT 생성/검증 코드와 시크릿 생성 코드를 찾습니다.
2. fallback 비밀값이 있는지 확인합니다.
3. 현재 토큰의 payload를 분석합니다.
4. 관리자 권한에 필요한 클레임을 맞춥니다.
5. 토큰을 재서명하고 저장 위치를 교체합니다.
6. flag가 있는 보호 페이지를 확인합니다.

## 5. 방어자 관점
- JWT 시크릿을 소스에 넣지 않습니다.
- 약한 fallback secret을 두지 않습니다.
- 서버는 토큰의 서명뿐 아니라 클레임의 의미도 검증해야 합니다.
- 클라이언트 저장소에 있는 토큰은 신뢰하지 않습니다.
- 권한 상승이 가능한 민감 기능은 서버측 재검증을 반드시 추가합니다.

## 6. 같이 보면 좋은 페이지
- [[jwt-secret-exposure-ctf-patterns]]
- [[broken-auth]]
- [[broken-access-control-core]]
- [[api-security-core]]
- [[java-code-analysis-final-writeup]]

## 7. 참고 소스
- [Brandon Elliott — JAuth CTF writeup](https://brandon-t-elliott.github.io/ctf-challenge-writeup-picoctf-jauth)
- [Probably Not Important — picoCTF 2021 JAuth](https://www.probablynotimportant.com/posts/2021-08-17-picoctf2021-jauth)
- [faisalmemon — picoCTF-JAuth-writeup](https://github.com/faisalmemon/picoCTF-JAuth-writeup)
- [YouTube — picoGym (picoCTF) Exercise: JAuth](https://www.youtube.com/watch?v=VpsGAv5fwDQ)

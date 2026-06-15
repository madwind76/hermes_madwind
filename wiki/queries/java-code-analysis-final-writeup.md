---
title: Java Code Analysis!?! — picoCTF 2023 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, jwt, token-forgery, source-inspection, picoctf]
sources: [https://zarrarkolachi.medium.com/java-code-analysis-picoctf-2023-e4ab29d4743e, https://brandon-t-elliott.github.io/java-code-analysis, https://cseciitb.github.io/posts/PicoCTFJavaCodeAnalysis/, https://hackmd.io/@ancorn/HyGTfwQG6]
confidence: high
---

# Java Code Analysis!?! — picoCTF 2023 web writeup

> `Java Code Analysis!?!`는 **서버 소스 코드에서 JWT 서명 키를 찾아 관리자 토큰을 위조하는 picoCTF 2023 Web 문제**입니다. 로그인 자체보다, `JwtService.java`와 `SecretGenerator.java`를 읽어 **약한 시크릿 `1234`**를 찾아내는 것이 핵심입니다.

## 1. 한 줄 요약
- 로그인 후 응답/요청에 JWT가 사용됩니다.
- 소스 코드에서 `JwtService.java`와 `SecretGenerator.java`를 확인합니다.
- 기본 시크릿이 `1234`로 떨어지는 분기가 있습니다.
- `role=user` 토큰을 `role=Admin`으로 바꿔 재서명하면 flag book에 접근할 수 있습니다.
- `localStorage`의 `auth-token`과 payload를 교체하면 됩니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 후 bearer/JWT가 보임 | 토큰 기반 권한 제어 |
| 2 | 소스에 `JwtService.java`가 있음 | 서명 로직 후보 |
| 3 | `SecretGenerator.java`가 키 생성 | 시크릿 노출 후보 |
| 4 | 기본 키가 `1234`로 보임 | 토큰 위조 가능 |
| 5 | `role` / `userId` / `email` 클레임이 존재 | 관리자 권한 조작 지점 |
| 6 | 로컬 스토리지 토큰 교체 후 flag book 접근 | 최종 획득 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 취약한가
JWT는 **서명된 클레임**을 전달하는 용도라서, 서버가 시크릿을 제대로 보호하고 검증해야 합니다. 이 문제는 소스 코드가 공개된 상황에서 **약한 기본 시크릿**이 노출되어 있어, 공격자가 정상 토큰 형식을 유지한 채 payload만 바꿔 재서명할 수 있습니다.

### 3.2 소스 분석 포인트
```bash
# 소스에서 JWT 관련 파일을 찾습니다.
# 예상 결과: JwtService.java, SecretGenerator.java 같은 파일명이 출력됩니다.
grep -R "jwt" .
```

```bash
# 권한 관련 문자열을 찾습니다.
# 예상 결과: role, admin, userId, email 같은 클레임 힌트를 찾을 수 있습니다.
grep -R "admin\|role\|userId\|email" .
```

### 3.3 토큰 변조 흐름
1. 현재 bearer token을 확보합니다.
2. `jwt.io` 같은 도구로 payload를 확인합니다.
3. `role`을 `Admin`으로 바꿉니다.
4. 소스 분석으로 확인한 시크릿 `1234`로 재서명합니다.
5. `localStorage.auth-token`을 새 토큰으로 교체합니다.
6. 페이지를 새로고침해서 관리자 권한을 확인합니다.

## 4. 공격자 관점
1. 소스 코드에서 JWT 관련 클래스와 시크릿 생성 로직을 찾습니다.
2. 약한 기본값이나 fallback secret이 있는지 확인합니다.
3. 현재 토큰의 payload를 디코딩합니다.
4. 관리자용 클레임(`role=Admin`, 필요 시 `userId`, `email`)을 맞춥니다.
5. 새 토큰을 재서명하고 클라이언트 저장소에 넣습니다.
6. 권한이 바뀌면 flag book을 읽습니다.

## 5. 방어자 관점
- JWT 시크릿을 소스에 두지 않고 환경 변수나 비밀 관리 시스템으로 분리해야 합니다.
- 기본 fallback 값(`1234` 같은 값)은 절대 두지 않아야 합니다.
- `role` 같은 권한 클레임은 서버에서 재검증해야 합니다.
- 클라이언트 저장소의 토큰은 신뢰 경계 밖이라고 봐야 합니다.
- 가능하면 짧은 만료와 서버측 세션 검증을 병행해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[broken-auth]]
- [[broken-access-control-core]]
- [[api-security-core]]
- [[jwt-secret-exposure-ctf-patterns]]
- [[login-final-writeup]]

## 7. 참고 소스
- [Zarar Ahmed — Java Code Analysis picoCTF 2023](https://zarrarkolachi.medium.com/java-code-analysis-picoctf-2023-e4ab29d4743e)
- [Brandon Elliott — CTF Writeup: picoCTF 2023 - "Java Code Analysis!?!"](https://brandon-t-elliott.github.io/java-code-analysis)
- [CSeC IITB — PicoCTF - web JavaCodeAnalysis](https://cseciitb.github.io/posts/PicoCTFJavaCodeAnalysis/)
- [HackMD — picoCTF 2023 Java Code Analysis!?!](https://hackmd.io/@ancorn/HyGTfwQG6)

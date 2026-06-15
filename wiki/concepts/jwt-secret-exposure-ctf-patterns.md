---
title: JWT secret exposure / token forgery — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, jwt, token-forgery, source-inspection, authentication]
sources: [https://brandon-t-elliott.github.io/java-code-analysis, https://cseciitb.github.io/posts/PicoCTFJavaCodeAnalysis/, https://zarrarkolachi.medium.com/java-code-analysis-picoctf-2023-e4ab29d4743e]
confidence: high
---

# JWT secret exposure / token forgery — CTF patterns

## 1. 정의
**JWT secret exposure**는 서버가 JWT를 서명하는 비밀키를 소스 코드, 설정 파일, 디버그 출력, 하드코딩 fallback 등에서 노출해 버리는 패턴입니다. 공격자는 이 시크릿으로 토큰을 다시 서명해 관리자 권한이나 다른 클레임을 위조할 수 있습니다.

## 2. 쉬운 비유
입장권에 **도장 찍는 잉크 색**이 적혀 있는 셈입니다. 그 색을 알면 누구나 새 입장권을 똑같이 만들어 낼 수 있습니다. JWT에서는 그 잉크가 `secret key`이고, 도장이 바로 서명입니다.

## 3. 자주 보이는 단서
| 단서 | 의미 |
|------|------|
| `JwtService`, `TokenService`, `AuthService` | JWT 서명/검증 코드 후보 |
| `SecretGenerator`, `.env`, config 파일 | 시크릿 유출 지점 |
| `1234`, `changeme`, `default` 같은 fallback | 매우 약한 키 |
| `role`, `admin`, `scope`, `userId`, `email` 클레임 | 위조할 권한 필드 |
| `localStorage`, `Authorization: Bearer` | 클라이언트 측 토큰 교체 지점 |

## 4. 기본 풀이 루프
```text
1) JWT 관련 소스 파일을 찾습니다.
2) 시크릿이 하드코딩되었는지 확인합니다.
3) 현재 토큰 payload를 디코딩합니다.
4) 권한 클레임을 바꿉니다.
5) 동일 알고리즘/시크릿으로 다시 서명합니다.
6) 토큰 저장 위치(localStorage, cookie, header)를 바꿔 재요청합니다.
```

## 5. 공격자 관점
1. 소스 코드에서 JWT 생성과 검증 흐름을 찾습니다.
2. 시크릿이 노출되면 토큰 위조 가능성을 판단합니다.
3. payload의 권한 클레임을 관리자 수준으로 조정합니다.
4. 토큰을 재서명한 뒤 클라이언트 저장소를 교체합니다.
5. 보호된 기능에 접근되는지 확인합니다.

## 6. 방어자 관점
- JWT 시크릿은 코드 저장소에 두지 않습니다.
- fallback default secret을 두지 않습니다.
- 알고리즘과 클레임 검증을 서버에서 엄격히 수행합니다.
- 권한 결정은 토큰 하나에만 의존하지 않습니다.
- 시크릿 로테이션과 만료 정책을 운영합니다.

## 7. 같이 보면 좋은 페이지
- [[broken-auth]]
- [[broken-access-control-core]]
- [[api-security-core]]
- [[java-code-analysis-final-writeup]]

## 8. 참고 소스
- [Brandon Elliott — Java Code Analysis writeup](https://brandon-t-elliott.github.io/java-code-analysis)
- [CSeC IITB — PicoCTF Java Code Analysis](https://cseciitb.github.io/posts/PicoCTFJavaCodeAnalysis/)
- [Zarar Ahmed — Java Code Analysis picoCTF 2023](https://zarrarkolachi.medium.com/java-code-analysis-picoctf-2023-e4ab29d4743e)

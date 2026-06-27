---
title: BitHug — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, git, webhook, access-control, ssrf, picoctf]
sources: [https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Bithug/README.md, https://www.tjcsec.club/writeups/picoctf-2021-bithug/, https://larry.sh/post/picoctf-2021/]
confidence: high
---

# BitHug — picoCTF 2021 web writeup

> `BitHug`는 **Git 호스팅 서비스의 접근 제어와 웹훅 처리, 그리고 내부 요청 경계를 함께 건드리는 picoCTF 2021 Web 문제**입니다. 핵심은 저장소 접근 규칙을 이해하고, 내부에서만 관리자 취급이 되는 경로를 이용해 보호된 저장소의 `access.conf`를 수정하는 것입니다.

## 참고 URL
- [Original writeup](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Bithug/README.md)
- [www.tjcsec.club](https://www.tjcsec.club/writeups/picoctf-2021-bithug/)
- [larry.sh](https://larry.sh/post/picoctf-2021/)


## 1. 한 줄 요약
- 서비스는 Git 저장소를 웹으로 제공합니다.
- 저장소 접근은 `admin` 또는 `access.conf`의 허용 사용자에 의해 결정됩니다.
- `req.socket.remoteAddress === localhost`이면 관리자처럼 동작하는 분기가 있습니다.
- 웹훅 URL 검증과 템플릿 치환이 엮여 내부 경로를 호출할 수 있습니다.
- 최종적으로 보호된 저장소의 `README`에서 flag를 읽습니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | Git 호스팅 웹앱이 보임 | 저장소/브랜치/훅이 공격면 |
| 2 | 일반 사용자는 다른 저장소 접근이 제한됨 | 접근 제어 필요 |
| 3 | localhost에서 온 요청만 admin 처리 | 내부 요청 위장 여지 |
| 4 | 웹훅 URL 템플릿이 `{{...}}` 치환을 지원 | 우회 문자열 조립 가능 |
| 5 | `git-receive-pack` / `git-upload-pack` 엔드포인트가 열려 있음 | Git 프로토콜 경로가 핵심 |
| 6 | 보호 저장소의 README에서 flag 획득 | 최종 목표 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 단순한 웹 화면 조작이 아니라, **Git 내부 프로토콜과 웹훅 실행 경로를 이용해 저장소 권한을 우회**하는 유형입니다. 공격자는 웹 애플리케이션이 내부적으로 호출하는 흐름을 잘 관찰해야 합니다.

### 3.2 소스에서 확인할 포인트
```bash
# 저장소 접근과 웹훅 관련 코드를 찾는 예시입니다.
# 예상 결과: auth, webhooks, git-api 같은 파일이 확인됩니다.
grep -R "remoteAddress\|webhook\|git-receive-pack\|access.conf" .
```

```bash
# 웹훅과 Git 엔드포인트 목록을 확인하는 예시입니다.
# 예상 결과: login/register 이외에 git-upload-pack, git-receive-pack 경로가 보입니다.
grep -R "git-upload-pack\|git-receive-pack\|webhooks" .
```

### 3.3 익스플로잇 개요
1. 기본 사용자 계정으로 로그인합니다.
2. Git 저장소와 웹훅 관련 엔드포인트를 확인합니다.
3. 내부 요청처럼 보이도록 웹훅 대상 문자열을 구성합니다.
4. 웹훅이 `localhost` 또는 내부 관리 경로를 호출하도록 유도합니다.
5. 보호 저장소의 `refs/meta/config`에 `access.conf`를 기록합니다.
6. 최종적으로 보호 저장소의 README를 읽어 flag를 확인합니다.

## 4. 공격자 관점
1. 접근 제어 조건을 먼저 읽습니다.
2. admin 판정이 어디서 이루어지는지 확인합니다.
3. 웹훅 URL 검증에서 막히는 조건을 찾습니다.
4. 템플릿 치환으로 내부 경로를 재구성할 수 있는지 봅니다.
5. Git receive-pack / upload-pack으로 저장소 설정을 바꿀 수 있는지 확인합니다.
6. 최종적으로 flag가 있는 저장소에 접근합니다.

## 5. 방어자 관점
- 관리 권한을 `remoteAddress` 같은 네트워크 정보에만 의존하면 안 됩니다.
- 웹훅 URL 검증은 문자열 필터가 아니라 명시적 allowlist로 처리해야 합니다.
- 내부 요청과 외부 요청의 trust boundary를 분리해야 합니다.
- Git 프로토콜 엔드포인트는 저장소 권한과 별개로 엄격히 제한해야 합니다.
- `access.conf` 같은 설정 파일은 서버 내부에서만 변경되도록 해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[web-ctf-writeup-internal-service]]
- [[ssrf]]
- [[web-ctf-writeup-auth-session]]
- [[web-ctf-writeup-parser-template]]
- [[head-dump-final-writeup]]

## 7. 참고 소스
- [HHousen — Bithug README](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Bithug/README.md)
- [TJCSC — picoCTF 2021 - BitHug (web)](https://www.tjcsec.club/writeups/picoctf-2021-bithug/)
- [Larry Yuan — picoCTF 2021](https://larry.sh/post/picoctf-2021/)

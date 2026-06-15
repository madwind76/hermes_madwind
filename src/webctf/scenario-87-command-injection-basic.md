---
title: OS Command Injection (운영체제 명령어 주입) — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, command-injection, rce, os-command, easy]
confidence: high
---

# OS Command Injection (운영체제 명령어 주입) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Network Utility Tool (간이 네트워크 유틸리티 도구)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 애플리케이션이 운영체제 시스템 명령어를 내부적으로 가동할 때 입력값 정제가 부재하여 임의의 OS 명령어가 기동되는 **운영체제 명령어 주입 (OS Command Injection)** 취약점 문제입니다.
- 대상 웹 서비스는 원격 서버의 네트워크 도달 여부를 테스트할 수 있는 웹 핑(Ping) 진단 도구입니다. 사용자가 입력 필드에 IP 주소나 호스트 이름을 입력하면, 백엔드 서버는 내부 시스템 쉘을 기동해 `ping -c 3 [입력값]` 명령어를 실행하고 그 결과 텍스트를 웹 브라우저 화면에 그대로 돌려줍니다. 개발자는 사용자의 입력값에 대해 쉘 메타문자가 포함되어 있는지 검증하지 않았습니다. 공격자는 세미콜론(`;`)이나 파이프(`|`), 앰퍼샌드(`&`) 등의 쉘 제어 연산자를 결합 주입해 시스템 명령어를 연쇄 가동시킴으로써 서버 내부 통제권을 획득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Network Diagnostic Page (`/ping.php`)**:
  - `?host=...` GET/POST 파라미터를 접수함.
  - 서버 운영체제의 `ping` 명령어를 자동 완성하여 내부 쉘(Terminal/Bash) 환경에서 구동한 뒤 결과를 응답으로 서빙.
- **Flag 위치**:
  - 시스템 서버 내부 파일 시스템 경로 `/flag.txt`.

### 2.2 취약점 지점
1. **Unsanitized Execution of Shell Commands**:
  - 웹 로직 내부에서 시스템 명령어를 조립할 때 문자열 연산을 직접 결합합니다:
    `$cmd = "ping -c 3 " . $_GET['host'];`
  - 이후 쉘을 직접 구동하는 `shell_exec($cmd)` 계열 함수를 호출합니다.
  - 공격자가 `127.0.0.1; cat /flag.txt` 를 입력하면, 운영체제 쉘 인터프리터는 이를 두 개의 개별 명령어로 나누어 해석합니다.
    1) `ping -c 3 127.0.0.1` (정상 종료 후)
    2) `cat /flag.txt` (즉각 연쇄 구동)
  - 이로 인해 관리자가 의도치 않은 임의의 시스템 명령어 출력이 웹 브라우저로 반환됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/ping.php` | POST | 불필요 | `host` | Text / String | `shell_exec()`, `exec()`, `system()` 등 OS 명령어 실행부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 정상적인 진단 기능 관찰
1. 핑 진단 입력란에 로컬 루프백 IP인 `127.0.0.1`을 적고 전송해 봅니다.
2. 화면에 `PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data...` 와 같이 리눅스 핑 유틸리티의 실행 텍스트 결과물이 고스란히 렌더링되어 응답되는 것을 보고 내부 명령어가 실행 중임을 인지합니다.

### Step 2. 쉘 메타문자를 활용한 구문 결합 테스트
1. 명령어 분리 제어 문자인 세미콜론(`;`)과 단순 정보 출력 명령어인 `id`를 호스트 명과 병합해 제출합니다.
   - 입력값: `127.0.0.1; id`
2. 응답 메시지에 `uid=33(www-data) gid=33(www-data) groups=33(www-data)...` 형태의 웹 서비스 데몬 사용자 권한 ID 정보가 함께 뒤이어 인쇄되는지 확인합니다.
3. 이를 통해 입력 필터링이 배제된 OS Command Injection 상태임을 확신합니다.

### Step 3. 서버 내부 디렉터리 구조 및 파일 탐색
1. 현재 어떤 파일이 서버에 들어있는지 확인하기 위해 파일 목록 보기 명령어를 결합하여 날립니다.
   - 입력값: `127.0.0.1; ls -la /`
2. 최상위 루트 디렉터리에 `flag.txt` 라는 파일 객체가 포함되어 존재함을 확인합니다.

### Step 4. flag 획득
1. 파일 읽기 도구(`cat` 등)를 활용하여 플래그 파일을 여는 명령어로 페이로드를 최종 작성합니다.
   - 입력값: `127.0.0.1; cat /flag.txt`
2. 웹 화면에 출력되는 최종 결과 텍스트 영역에서 플래그(`FLAG{os_command_injection_basic_shell_hijacked}`)를 확인해 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- ping.php (취약한 명령어 주입 PHP 예시) -->
<!DOCTYPE html>
<html>
<head>
    <title>Network Admin Tool</title>
</head>
<body>
    <h1>원격 서버 Ping 진단 서비스</h1>
    <form method="POST" action="ping.php">
        <label>IP / Hostname:</label>
        <input type="text" name="host" placeholder="e.g. 8.8.8.8">
        <button type="submit">진단 시작</button>
    </form>

    <pre>
    <?php
    if (isset($_POST['host'])) {
        $host = $_POST['host'];

        // 취약점 지점: $host 값의 포맷을 사전에 검증(IP 형식 등 정규식 판별)하지 않으며, 
        // 쉘 메타문자 제거 함수(escapeshellarg 등)를 거치지 않고 직접 문자열에 결합하여 
        // 쉘 커맨드를 조립 및 구동시킴.
        $command = "ping -c 3 " . $host;
        
        // 쉘 명령어 가동 및 출력 데이터 전송
        $output = shell_exec($command);
        echo htmlspecialchars($output);
    }
    ?>
    </pre>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **입력값의 형식 검증 (Strict Input Validation)**:
   - 호스트 정보는 순수한 IP 주소 또는 정상적인 도메인 주소명만 입력될 수 있으므로 정규 표현식(Regular Expression)을 이용해 문자가 규칙에 적합한 형태인지를 확실히 화이트리스트 검사합니다.
     ```php
     // IPv4 주소 형식만 통과시키는 정규식 가동 예
     if (!filter_var($host, FILTER_VALIDATE_IP)) {
         die("Invalid IP Address format.");
     }
     ```
2. **쉘 인자 이스케이프 전처리 기능 적용**:
   - 시스템 쉘을 부득이하게 가동해야 하는 경우, 인자값이 쉘 메타문자로 인식되지 않도록 `escapeshellarg()` 같은 플랫폼 전용 이스케이프 내장 라이브러리를 씌워 인자를 홑따옴표로 감싸서 문자열 단일 객체로 격리 처리합니다.
     ```php
     // 인자값을 안전한 스트링으로 봉인
     $command = "ping -c 3 " . escapeshellarg($host);
     ```
3. **네이티브 API 및 대체 시스템 라이브러리 사용**:
   - 운영체제 시스템 쉘 인터프리터를 기동하는 방식을 지양하고, 웹 개발 언어의 표준 소켓 라이브러리(Socket Library)나 네트워크 핑 내장 함수/모듈 패키지를 이용해 소스코드를 재구성하여 인젝션의 발생 계기를 완전 박멸합니다.

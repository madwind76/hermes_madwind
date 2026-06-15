---
title: Directory Listing Exposure — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, directory-listing, information-disclosure, misconfiguration, easy]
confidence: high
---

# Directory Listing Exposure — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Archival Safe Box (간이 백업 보관소)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 서버의 잘못된 환경 설정으로 인해 특정 디렉터리 내부에 포함된 파일 목록이 브라우저 상에 일괄 리스팅 노출되는 **디렉터리 리스팅 노출 (Directory Listing Exposure / Directory Indexing)** 취약점 문제입니다.
- 대상 웹 서비스는 일반적인 포털 사이트 구조이나, 웹 루트 하위에 백업 데이터를 임시 보관하기 위해 개발자가 마련한 `/backups/` 폴더가 존재합니다. 웹 서버(Apache, Nginx 등) 환경 설정에서 디렉터리 목록 보기 옵션이 활성화된 상태로 운영되고 있으며, 해당 폴더 안에는 인덱스 파일(예: `index.html`, `index.php`)이 존재하지 않습니다. 공격자는 브라우저 주소창에 수동으로 `/backups/` 경로를 기입하고 엔터를 누르면 서버 내 보관된 모든 정적 백업 파일명과 크기가 트리 구조로 한눈에 출력되는 오설정을 발견합니다. 방치된 구버전 소스코드 압축파일이나 SQL 데이터베이스 덤프 본을 다운로드하여 기밀을 유출할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Web Server Config (Apache/Nginx)**:
  - Apache의 `Options Indexes` 속성이 설정 파일에 선언되어 있거나 Nginx의 `autoindex on;` 지시자가 활성화됨.
- **Backup Folder (`/backups/`)**:
  - 실제 웹 서비스에 가시적으로 하이퍼링크가 걸려있진 않으나 웹 루트 물리 경로 하단에 상주하는 정적 폴더.
- **Flag 위치**:
  - `/backups/` 경로를 통해 다운로드받을 수 있는 정적 백업 파일 내부(예: `db_dump.sql` 파일 내 데이터 인서트 구문 목록 중 플래그 데이터값).

### 2.2 취약점 지점
1. **Directory Indexing Enabled**:
  - 사용자가 디렉터리 주소를 요청했을 때, 기본 인덱스 파일이 없다면 폴더 내용을 웹 뷰러 형태로 렌더링하여 반환합니다.
  - 이로 인해 외부에 알려지지 않아야 하는 시스템 임시 스크립트, 소스 복사본, 설정 백업(`.env.bak`, `config.zip` 등)의 파일 이름이 그대로 수집당해 2차 공격의 빌미를 주게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/backups/` | GET | 불필요 | 없음 | 정적 디렉터리 | 웹 서버 디렉터리 인덱싱 기능 (Autoindex / Indexes) |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 웹 자산 경로 조사 및 추측
1. 대상 웹 서비스의 페이지 소스코드나 로봇 배제 표준 파일(`/robots.txt`) 등을 스캔하여 특수 경로가 존재하지 않는지 분석합니다.
2. 백업 파일이 저장되어 있을 법한 일반적인 디렉터리 이름 목록(예: `/backup/`, `/backups/`, `/src/`, `/uploads/`)을 웹 브라우저 주소창에 직접 무작위 대입 테스트해 봅니다.

### Step 2. 디렉터리 리스팅 노출 뷰 발견
1. `/backups/` 경로를 주입하여 접속을 확인합니다.
2. HTTP 403 Forbidden 에러나 404 Not Found가 뜨지 않고, 브라우저 화면에 `Index of /backups` 라는 텍스트 헤더와 함께 내부 정적 파일 목록들이 하이퍼링크 리스트로 줄지어 나열되는 것을 확인합니다.
3. 이를 통해 웹 서버 미설정 결함인 Directory Listing 취약점이 활성화되어 있음을 확인합니다.

### Step 3. 민감한 백업 파일 객체 탐색 및 다운로드
1. 나열되어 표시되는 파일 객체 목록 중에서 민감도가 높아 보이는 자산을 골라냅니다:
   - 파일 예시: `db_backup_final_2026.sql`, `source_code.zip`
2. 다운로드 링크를 마우스 클릭하여 로컬 분석용 파일로 저장합니다.

### Step 4. flag 획득
1. 덤프 내려받은 데이터베이스 덤프 파일(`db_backup_final_2026.sql`)의 내부 구조를 로컬 텍스트 에디터로 엽니다.
2. `INSERT INTO admin_settings ...` 또는 사용자 관리 테이블 관련 테이블 스키마 및 레코드 데이터 영역을 조사하여 내부에 보관된 텍스트 플래그(`FLAG{directory_listing_leak_sensitive_backup_file}`)를 확인하고 최종 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Web Server Config)

### Apache 취약 서버 설정 예시 (`httpd.conf` / `.htaccess`)
```apache
# /var/www/html/backups/.htaccess (또는 httpd.conf 내 설정)
<Directory "/var/www/html/backups">
    # 취약점 지점: 디렉터리 내 기본 인덱스 파일(index.html 등)이 없으면 
    # 폴더의 파일 구조 전체를 웹 화면에 출력해 주는 "Indexes" 옵션이 켜져 있음.
    Options +Indexes +FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

### Nginx 취약 서버 설정 예시 (`nginx.conf`)
```nginx
server {
    listen 80;
    server_name target.local;
    root /var/www/html;

    location /backups {
        # 취약점 지점: autoindex 옵션이 on으로 기재되어 있어 
        # backups 디렉터리에 대한 파일 리스팅 뷰를 자동으로 클라이언트에 서빙함.
        autoindex on;
        autoindex_exact_size on;
        autoindex_localtime on;
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **디렉터리 인덱싱 기능 전면 비활성화 (Options -Indexes / autoindex off)**:
   - 웹 서버 구성 파일 내에서 디렉터리 인덱스 리스팅 관련 설정을 차단하는 지시자로 업데이트합니다.
     - **Apache**: `Options -Indexes` 적용
     - **Nginx**: `autoindex off;` 적용
   - 이를 비활성화하면, 인덱스 파일이 존재하지 않는 디렉터리에 누군가 접근하더라도 파일 목록을 공개하는 대신 HTTP 403 Forbidden 오류 코드를 반환하며 조회를 강제 거부합니다.
2. **더미 인덱스 파일 (Dummy index.html) 기본 배치**:
   - 정적 자산을 저장하고 퍼블릭 조회를 분할 가동해야 하는 디렉터리 경로마다 빈 페이지 혹은 경고 문구가 작성된 `index.html` 파일을 선제적으로 배치하여, 브라우저가 자동 리스팅 렌더링 모드로 전환되지 않고 빈 화면만 수신하도록 보조 방어를 수행합니다.
3. **업로드 및 정적 백업 자산의 경로 격리 정책 수립**:
   - 내부 시스템 백업 아카이브나 `.env`, 소스코드 압축본 같은 기밀 데이터는 웹 브라우저를 통해 URL 접근이 직접 가능한 퍼블릭 웹 루트(`DocumentRoot`)의 바깥쪽 물리 디렉터리에 저장해 두어, 주소창 추측이나 인덱싱으로 인한 외부 노출 가능성을 완벽히 원천 차단합니다.

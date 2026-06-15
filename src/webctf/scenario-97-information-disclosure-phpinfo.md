---
title: Information Disclosure via phpinfo — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, information-disclosure, phpinfo, misconfiguration, easy]
confidence: high
---

# Information Disclosure via phpinfo (phpinfo를 통한 정보 노출) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Server Stats Checker (서버 상태 확인기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 개발 및 서버 점검 목적으로 작성된 디버깅 파일이 상용 운영 환경에 무방비하게 방치되어 시스템 기밀을 드러내는 **phpinfo 페이지 노출을 통한 서버 환경 정보 유출 (Information Disclosure via phpinfo)** 취약점 문제입니다.
- 대상 웹 서비스는 리눅스 아파치 서버와 PHP 환경에서 구축되어 정상 작동하고 있습니다. 하지만 인프라 설정 단계에서 엔지니어가 PHP 가동 여부 및 환경 변수 로드 상태를 체크하기 위해 웹 루트 하위에 `phpinfo()` 표준 시스템 상태 요약 함수를 구동시키는 `info.php` 파일을 임시 작성한 뒤, 정비가 끝난 뒤에도 삭제하지 않고 방치했습니다. 공격자는 일반적인 정찰(Reconnaissance) 과정에서 추측하기 쉬운 관리 스크립트 명칭을 무작위 조회하여 서버 내부 설정 및 웹 데몬 환경 변수 영역에 평문으로 등록되어 있는 플래그 정보를 유출해 낼 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Unremoved Diagnostics Script (`/info.php` 또는 `/phpinfo.php`)**:
  - 오직 `<?php phpinfo(); ?>` 한 줄만을 실행하는 정적 진단용 파일.
  - 전역 환경 변수(`.env` 또는 웹서버 설정 파일에 정의된 변수)를 로드하여 테이블로 가시화함.
- **Flag 위치**:
  - `phpinfo()` 상세 출력 항목 내의 'Environment' 혹은 'PHP Variables' 섹션 내부의 환경 변수 키(`FLAG` 또는 `SYSTEM_FLAG`).

### 2.2 취약점 지점
1. **Exposure of Diagnostic Configuration Interfaces**:
  - 내부 보안 감사 정책 결여로 인해 테스트 지향적 스크립트가 소거되지 않았습니다.
  - `phpinfo()`는 웹 서버 운영체제 종류, 커널 버전, 활성화된 익스텐션, 소스코드의 실제 서버 물리 경로(예: `/var/www/html/...`) 및 DB 접근 계정이 명시된 시스템 환경 변수 사전을 화면 상에 완전히 정제 없이 렌더링하므로 2차 공격(LFI, RCE 등)을 위한 완벽한 정찰 지도를 공격자에게 상납하는 꼴이 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/info.php` | GET | 불필요 | 없음 | 정적 요청 | `phpinfo()` 시스템 정보 출력 기능 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 웹 정찰 및 디렉터리 스캔
1. 대상 사이트의 정보 수집을 위해 보편적으로 남겨지는 진단용 파일 리스트명을 쿼리해 봅니다.
   - 대상 리스트: `/info.php`, `/phpinfo.php`, `/test.php`, `/status.php`
2. `/info.php` 경로로 접근 시 에러 페이지 대신 보라색/회색 톤의 거대한 PHP 상태 명세 HTML 테이블이 렌더링되어 반환됨을 확인합니다.

### Step 2. 서버 설정 속성 분석
1. 로드된 테이블 화면의 상단을 보며 서버의 구체적인 스펙을 파악합니다.
   - 운영체제: Linux x86_64
   - PHP 버전: 8.2.x
   - 웹 서버: Apache/2.4.x
   - 물리 웹 루트: `/var/www/html/`

### Step 3. 환경 변수 영역 돋보기 검색
1. 브라우저의 찾기 단축키(Ctrl + F)를 활성화하여 환경 변수 영역으로 포커스를 이동하기 위해 `Environment` 또는 `_SERVER` 키워드를 검색합니다.
2. 시스템 시작 시 주입되어 운영되던 백엔드 변수 테이블 영역을 정밀하게 조사합니다.

### Step 4. flag 획득
1. 변수 목록 내의 `FLAG` 혹은 `SYSTEM_FLAG` 이름의 엔트리를 식별합니다.
2. 값으로 할당되어 매칭되어 있는 문자열(`FLAG{phpinfo_server_environment_variables_leak}`)을 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- info.php (방치된 취약한 진단 PHP 예시) -->
<?php
// 취약점 지점: 설치 테스트 완료 후 웹 서버 물리 경로에서 삭제되어야 하는 
// phpinfo() 호출 파일이 그대로 존재하여, 누구나 인증 없이 접근해 
// 서버의 전체 환경 변수 데이터(OS 버전, PHP 상세 설정, 비밀 키값 등)를 볼 수 있게 됨.
phpinfo();
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **테스트/디버그 스크립트 강제 삭제 정책 가동**:
   - 운영 서버 배포 파이프라인 진행 시 검사 스크립트 파일(`.php` 확장자 외 임시 테스트 파일)을 검출해 자동 삭제하는 빌드 단계를 적용합니다.
   - 수동 검사 시 `phpinfo.php`, `test.php`, `db_test.php` 등 전형적인 진단 파일은 목적 달성 즉시 시스템 내부에서 완전 소거합니다.
2. **웹 서버 구성 파일 내 접근 권한 통제**:
   - 로컬 테스트 목적으로 부득이하게 진단 페이지를 유지해야 할 경우에는 외부 인터넷 사용자의 다이렉트 호출을 차단하고, 특정 관리자 IP 대역(예: `127.0.0.1` 또는 사내 서브넷 망)만 호출할 수 있도록 웹서버 구성 파일(`.htaccess` 또는 `nginx.conf`) 단에서 접근 통제(Access Control) 규칙을 수립합니다.
     ```apache
     # Apache 특정 IP 접근 허용 설정 예시
     <Files "info.php">
         Require ip 192.168.1.100
     </Files>
     ```
3. **특정 취약 함수 비활성화 (disable_functions)**:
   - PHP 설정 파일인 `php.ini`의 `disable_functions` 항목에 `phpinfo` 지시자를 추가로 명시하여 소스 상에서 무단 호출 시에도 아예 기동되지 않도록 컴파일러 수준에서 안전 조치를 단행합니다.
     ```ini
     # php.ini 내 특정 함수 기동 차단
     disable_functions = phpinfo, system, shell_exec, passthru
     ```

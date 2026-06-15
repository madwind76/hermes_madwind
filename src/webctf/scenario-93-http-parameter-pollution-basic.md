---
title: HTTP Parameter Pollution (HPP) Basic — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, hpp, parameter-pollution, bypass, easy]
confidence: high
---

# HTTP Parameter Pollution (HPP) Basic — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Parameter Filter Bypass (파라미터 필터 우회기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 서버 및 웹 애플리케이션 프레임워크 간에 다중 수신된 동일 매개변수를 처리하는 구문 분석(Parsing) 우선순위의 차이를 이용해 보안 필터링을 조작 우회하는 **HTTP 파라미터 오염 (HTTP Parameter Pollution - HPP)** 취약점 문제입니다.
- 대상 웹 서비스는 관리자 메뉴 접근을 통제하기 위해 유입되는 `username` 파라미터를 검사하여 `admin`이 감지되면 HTTP 403 Forbidden 상태 코드로 요청을 즉시 거부하는 단순한 프론트 방화벽/미들웨어 검증 구조를 운영합니다. 그러나 백엔드 본체는 동일한 키를 가진 다중 파라미터(예: `username=guest&username=admin`)가 들어올 때, 마지막에 전송된 파라미터 값을 최종 인자로 채택해 실행하는 특성을 갖습니다. 공격자는 이 파라미터 오염 기법을 활용하여 통제 시스템에는 무해한 값을 보여주고, 백엔드 내부 DB 쿼리 도메인에는 어드민 파라미터가 들어가도록 통과시켜 플래그를 탈취할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend Security Check Module**:
  - 유입되는 URL 쿼리 파라미터를 추출해 `username`에 `admin`이 완벽히 포함되는지 검사하여 요청을 드롭(Drop)시킴.
  - 이때 다중 파라미터에 대한 정밀 배열 분석이 결여되어, 파라미터 묶음의 최초 값만 스캔하고 통과시키는 허점이 존재.
- **Backend Application (`/admin_control.php`)**:
  - 실질적인 어드민 업무 페이지.
  - 보안 장치 통과 후, 백엔드 엔진(예: PHP의 `$_GET['username']`)은 중복 인자 중 최종 해석된 인자값만 참조하여 관리자 페이지를 로드함.
- **Flag 위치**:
  - `username=admin` 세션 자격으로 우회 도달한 관리자 관리 화면 본문.

### 2.2 취약점 지점
1. **Discrepancy in Multi-Parameter Parsing**:
  - 프론트엔드 검사 엔진과 백엔드 인터프리터 엔진 간의 파라미터 파싱 일관성이 깨져 있습니다.
  - 공격자가 `?username=guest&username=admin` 을 주입하면:
    - 프론트엔드 통제 필터는 첫 번째 변수쌍인 `username=guest` 값만 분석하여 안전하다고 판독하고 승인 처리합니다.
    - 백엔드 PHP 코드는 뒤쪽 변수쌍으로 오버라이드(Override) 처리된 `username=admin` 값을 최종 변수 데이터로 추출해 버립니다.
  - 이로 인해 보안 검문소의 인가 로직을 우회하여 보호 자산에 침투하게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/admin_control.php` | GET | 불필요 (필터 우회) | `username` | Text / String | 다중 동일 매개변수 중복 입력 처리부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 정상적 파라미터 전송 관찰 및 접근 거부 확인
1. 어드민 페이지에 일반적인 매개변수를 입력해 접속을 시도합니다.
   `/admin_control.php?username=guest`
2. "일반 유저 `guest`님 환영합니다" 라는 문구를 확인하며 핑거프린팅을 시작합니다.
3. 어드민 계정인 `admin`을 파라미터로 명시적으로 삽입해 봅니다.
   `/admin_control.php?username=admin`
4. 프론트엔드 보안 검증 엔진이 발동하여 `Access Denied: Admin username is blocked!` 에러 페이지(403)가 리턴되는 현상을 관찰합니다.

### Step 2. HPP 취약성 분석 및 테스트
1. 타겟 백엔드 엔진이 다중 파라미터를 어떻게 처리하는지 파싱 특성을 봅니다.
   `/admin_control.php?username=guest&username=test`
2. 응답 페이지에 출력되는 로그인 아이디명이 `test`로 변경되어 출력되는 것을 보고, 백엔드가 뒤에 위치한 중복 파라미터 값으로 변수명을 최종 덮어쓰고 있음을 포착합니다.

### Step 3. HPP 페이로드 조립 및 필터 우회
1. 보안 필터가 검사하는 첫 번째 자리에 `guest`를 두고, 백엔드가 취하는 뒤쪽에 차단 대상이었던 `admin`을 배치하여 공격용 쿼리 주소를 만듭니다.
   `/admin_control.php?username=guest&username=admin`
2. 웹서버로 리퀘스트를 날립니다.

### Step 4. flag 획득
1. 보안 체크 모듈은 최초 식별된 `username=guest`만 감지하여 블로킹 없이 통과 처리를 수행합니다.
2. 미들웨어를 넘어간 요청을 접수한 `/admin_control.php` 파일은 `$_GET['username']`을 호출하며 뒤의 값인 `admin`으로 값을 덮어써 관리자 페이지를 브라우저에 표시합니다.
3. 로드된 대시보드 관리창의 데이터 테이블에서 플래그(`FLAG{hpp_parameter_pollution_parsing_conflict_bypass}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- admin_control.php (취약한 HPP PHP 예시) -->
<?php
// 1. 프론트 검사 단계를 가정한 보안 검증 로직 시뮬레이션
$raw_query = $_SERVER['QUERY_STRING']; // 예: username=guest&username=admin

// 단순 문자열 파싱 혹은 앞부분 매치 검사 시도
// (많은 간이 방화벽이 첫 번째 매치된 값을 위주로 검증함)
$params = [];
parse_str($raw_query, $params);

// 취약점 지점: 쿼리 원시 문자열에서 단순히 첫 번째 출현한 username 값을 임의로 
// 잘라내 검사하거나, 다중 파라미터를 통째로 안전하게 배열화하여 전수 필터링하지 않음
if (isset($params['username'])) {
    $first_user = $params['username'];
    // 만약 파싱 로직의 불일치로 인해 앞쪽의 guest만 탐색하고 block 구문을 스킵하면 우회됨
    if (strpos($raw_query, 'username=admin') !== false && strpos($raw_query, 'username=guest') === false) {
        die("Access Denied: Admin username is blocked!");
    }
}

// 2. 실제 백엔드 애플리케이션 서비스 동작 단계
// PHP의 $_GET 슈퍼 글로벌 변수는 덮어쓰기 특성을 통해 중복된 키값 중 가장 마지막 인자를 반환함.
if (isset($_GET['username'])) {
    $final_user = $_GET['username'];
    
    echo "<h1>로그인 회원: " . htmlspecialchars($final_user) . "</h1>";
    
    if ($final_user === 'admin') {
        echo "<p><b>관리자 플래그:</b> FLAG{hpp_parameter_pollution_parsing_conflict_bypass}</p>";
    } else {
        echo "<p>일반 사용자 메뉴만 노출됩니다.</p>";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **파라미터 일관성 검증 및 입력값 배열 검사**:
   - 수신된 파라미터가 단일 문자열 값이어야 하는 로직이라면, 파라미터의 타입이 배열 형태로 전달되지 않았는지 엄격하게 확인하고 다중 값의 입력 자체를 사전에 드롭시킵니다.
     ```php
     // 중복 파라미터 입력 시 차단
     if (is_array($_GET['username'])) {
         die("Invalid request: Multiple parameters detected.");
     }
     ```
2. **동일 파라미터 파싱 규칙 표준화**:
   - 보안 검증 모듈(WAF/Proxy)과 실제 서비스 구동 백엔드 언어의 버전 및 프레임워크가 동일한 방식으로 HTTP Request를 파싱하여 값을 도출하게 구성을 통일합니다.
3. **명시적 라우팅 및 컨트롤러 명세 작성**:
   - 쿼리 스트링 파라미터에 비즈니스 인가 자격을 위임하여 처리하는 동적 파싱을 배제하고, 세션에 기반한 인증 처리를 핵심 권한 모델로 채용하여 매개변수 변조 공격이 비즈니스 자격에 절대 영향을 주지 않도록 격리 설계합니다.

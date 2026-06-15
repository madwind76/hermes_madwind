---
title: Cookie Poisoning to Local File Inclusion (LFI) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, lfi, cookie-poisoning, path-traversal, php, vulnerability]
confidence: high
---

# Cookie Poisoning to Local File Inclusion (LFI) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Custom Portal Theme Reader (포털 테마 리더)
- **난이도**: Medium
- **핵심 컨셉**: 브라우저 쿠키(Cookie) 데이터를 검증 없이 서버의 동적 로딩 경로에 할당할 때 발생하는 **쿠키 포이즈닝 기반 Local File Inclusion (LFI)** 취약점 문제입니다. 대상 애플리케이션은 사용자가 선택한 디자인 테마 및 다국어 로케일 정보(예: `dark`, `light`)를 클라이언트 브라우저의 쿠키 영역(`theme=dark`)에 기록하고 매 요청마다 참조합니다. 그러나 백엔드 웹 템플릿 처리 코드는 이 쿠키 설정값을 안전하다고 임의 맹신하여, 디렉터리 경로 검사나 파일명 정제 없이 파일 포함 제어문(`include` 또는 `require`)에 바인딩합니다. 공격자는 브라우저 쿠키 내의 테마 파라미터를 상위 경로 탐색 문자열(`../../../../etc/passwd`)로 교체 포이즈닝하여, 서버의 기밀 시스템 설정 파일을 화면에 출력시키거나 원격 코드 실행(RCE)으로 연결시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Theme Loader Endpoint (`/dashboard.php`)**:
  - 사용자가 대시보드에 접근할 때 브라우저가 전달한 `theme` 쿠키의 값을 기반으로 디자인 템플릿 php 파일을 서버 디렉터리에서 동적으로 인클루드하는 허브 페이지.
  - 리퀘스트 처리 코드:
    `$themeFile = "themes/" . $_COOKIE['theme'] . ".php";`
    `include($themeFile);`
- **Flag 위치**:
  - 시스템 로컬 파일 `/etc/flag.txt` 에 탑재되어 있으며 LFI 경로 변조를 통해 화면에 출력시켜야 합니다.

### 2.2 취약점 지점
1. **Implicit Trust in Cookie Values**:
   - 개발자는 URL 파라미터(`?theme=...`)와 달리 쿠키 값은 공격자가 직접 변조하기 어려울 것이라고 가정하여 어떠한 유효성 필터링도 기재하지 않았습니다.
2. **Directory Traversal using Slashes**:
   - `include` 지연 인클루드 파일 빌드 시 상위 폴더 경로 이동 기호(`../` 혹은 `..\\`)를 지우거나 치환하지 않아 임의의 파일 시스템 노드가 노출됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 상태 | 변조 대상 헤더 | 대상 취약 함수 | 목적 |
|------------|--------|-----------|----------------|----------------|------|
| `/dashboard.php` | GET / POST | 로그인 권한 | `Cookie: theme=[POISON]` | PHP `include` / `require` | `/etc/flag.txt` 시스템 파일 노출 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 쿠키 정보 관찰 및 타겟 함수 예측
1. 사용자는 로그인 후 생성된 브라우저 쿠키 셋을 관찰합니다.
   `Cookie: session=xxxxxx; theme=light`
2. 테마를 변경할 때마다 쿠키 값의 `theme` 속성이 동적으로 갱신되는 양상을 포착합니다.
3. 소스코드 흐름 혹은 에러 반환(예: `include(themes/light.php): failed to open stream`)을 통해 쿠키 값을 통해 동적 파일 로드가 일어남을 예측합니다.

### Step 2. Cookie Poisoning을 활용한 LFI 시도
1. 브라우저 개발자 도구의 Application/Storage 탭 혹은 프록시 도구를 사용하여 `theme` 쿠키의 값을 다음과 같이 변조합니다.
   `theme=../../../../etc/passwd%00`
   *(구버전 PHP의 경우 Null Byte `%00`를 끝부분에 도킹하여 뒤의 자동 확장자 `.php` 꼬리를 강제 절단할 수 있으며, 최신 PHP는 파일 경로에 널 바이트가 들어오면 에러가 날 수 있으므로 세션이나 다른 임시 파일 LFI 가젯을 결합함)*
2. 타겟 경로가 `/etc/flag.txt` 이므로, 뒤에 자동으로 달라붙는 `.php` 확장자가 걸림돌입니다. 만약 PHP 8.x 이상 등 최신 환경이라면 널바이트 우회가 막혔으므로, `/etc/flag` 처럼 확장자가 없는 자원을 포함시키기 위해 디렉터리 경로를 여러 번 중첩해 우회하거나(예: `/etc/flag.txt`에 대한 단순 참조 시도), 혹은 실제로 존재할 수 있는 다른 `.php` 시스템 스크립트를 겨냥합니다.
3. 플래그가 보관된 파일명이 `/etc/flag.txt` 인 상황에서, 템플릿에 `.php`가 자동 부착된다면 다음과 같은 트래버셜을 시도합니다:
   `Cookie: theme=../../../../etc/flag`
   *(서버 코드가 `include("themes/" . $_COOKIE['theme'] . ".txt");` 형태로 디자인 템플릿 파일을 로드하거나 `.php`가 붙는 구조)*
   - 최종 조립 경로: `themes/../../../../etc/flag.txt` (정확히 플래그 파일 매핑 완료)

### Step 3. 오염된 쿠키를 소지한 리퀘스트 발송
1. 오염된 `theme` 쿠키를 달고 `/dashboard.php`로 GET 요청을 보냅니다.
   - **전송 요청 헤더**:
     ```http
     GET /dashboard.php HTTP/1.1
     Host: portal.challenge.local
     Cookie: session=valid_session; theme=../../../../etc/flag
     Connection: close
     ```

### Step 4. flag 획득
1. 백엔드는 `include("themes/../../../../etc/flag.txt");` 구문을 실행하여 서버 로컬 `/etc/flag.txt` 파일 내용을 컴파일 및 렌더링 영역으로 로딩합니다.
2. 페이지 메인 레이아웃 본문 내에 출력된 플래그 문자열(`FLAG{cookie_poisoning_lfi_path_traversal}`)을 확인 및 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<?php
// dashboard.php (취약한 쿠키 로딩 LFI 예시)
session_start();

if (!isset($_SESSION['username'])) {
    die("로그인이 필요한 서비스입니다.");
}

// 기본 테마 지정
$theme = "light";

// 취약점 지점 1: 사용자의 브라우저 쿠키를 전적으로 신뢰하여 theme 값을 불러옴
// 공격자는 쿠키 편집기나 프록시를 통해 theme 값을 자유롭게 변조 가능
if (isset($_COOKIE['theme'])) {
    $theme = $_COOKIE['theme']; 
}

// 취약점 지점 2: 상위 경로 변조 문자열(../) 필터링 없이 
// include 문법에 경로 바인딩하여 실행시킴
// 만약 $theme 값으로 "../../../../etc/flag" 가 주입되면, /etc/flag.txt 파일 내용이 노출됨
$templatePath = "themes/" . $theme . ".txt";

include($templatePath); 

// 대시보드 본문 HTML 렌더링...
echo "<h3>어서오세요, " . htmlspecialchars($_SESSION['username']) . "님!</h3>";
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **엄격한 화이트리스트 검사 (Strict Whitelist Validation)**:
   - 동적으로 로드할 파일 테마 목록을 서버 단에 정적 배열로 매핑한 화이트리스트를 구축하고, 이 목록에 포함된 정확한 명칭이 아닌 입력값(쿠키)은 동작을 즉각 거절합니다.
     ```php
     $allowed_themes = array("light", "dark", "elegant");
     if (!in_array($theme, $allowed_themes)) {
         $theme = "light"; // 기본값 복귀 강제
     }
     ```
2. **파일명 정제 및 베이스네임 함수 강제 (Filename Sanitization)**:
   - `pathinfo` 또는 `basename()` 함수를 사용하여 디렉터리 경로 이동 문자열을 제거하고 오직 순수 파일명(Basename) 부분만 파싱하여 자원을 포함시키도록 규정합니다.
3. **쿠키 암호화 및 서명화 (Signed Cookies)**:
   - 클라이언트 측 쿠키 변조 행위를 물리적으로 차단하기 위해, 웹 서버 수준에서 세션에 탑재하거나 쿠키에 서명 및 암호화(예: Express의 `signedCookies` 사용) 처리를 수립하여 무단 변조된 쿠키 요청은 미들웨어 단에서 폐기합니다.

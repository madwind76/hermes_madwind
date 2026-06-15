---
title: Regular Expression Denial of Service (ReDoS) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, redos, regular-expression, denial-of-service, algorithmic-complexity, backtracking]
confidence: high
---

# Regular Expression Denial of Service (ReDoS) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Robust Input Sanitizer (견고한 입력 분석기)
- **난이도**: Medium
- **핵심 컨셉**: 입력 유효성 검증 규칙의 비효율적 설계로 인한 자원 소모성 장애를 공략하는 **정규 표현식 서비스 거부 공격(ReDoS)** 취약점 문제입니다. 서버는 외부 사용자의 회원가입 양식(예: 이메일, 복잡한 사용자 이름 규칙)에 대해 중첩 정규 표현식을 기입하여 유효성 판단을 수행합니다. 그러나 작성된 정규식 내부의 다중 그룹 수량자(`*`, `+`) 설정 결함으로 인해, 매칭이 불완전하게 어긋나는 특정 문자열을 입력받을 경우 백트래킹(Backtracking) 연산 횟수가 기하급수적으로 증가하게 됩니다. 공격자는 이를 통해 서버 CPU 연산을 마비시키고 웹 서버 서비스 거부(DoS)를 유도하여 기밀 에러 로그 출력이나 동시성 처리 한계치를 붕괴시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Signup**: 사용자명, 이메일 주소를 받아 회원가입을 요청하는 단일 인터페이스.
- **Backend Service (Node.js/Express or Python/Flask)**:
  - 입력 데이터 유효성 검사 모듈 구동.
  - 이메일 정적 스캔 정규식: `/^([a-zA-Z0-9]+)*@gmail.com$/` (중첩 루프 형태의 패턴)
  - 또는 임의 문자열 검증식: `/^([a-z]+)+$/` 등 백트래킹 취약 패턴 적용.
- **Flag 위치**:
  - ReDoS에 의해 싱글 스레드로 동작하는 Node.js 서버가 3초 이상 블로킹(Blocking) 상태에 빠진 뒤 에러를 리턴할 때, 에러 메모리 덤프나 로그 정보에 플래그가 반환되는 시나리오.

### 2.2 취약점 지점
1. **Catastrophic Backtracking in Regex Engine**:
   - 정규 표현식 파싱 엔진(NFA 구조)은 입력값이 조건식 매치에 실패할 때, 다른 분기점을 찾아 앞으로 돌아가 재검증하는 '백트래킹' 연산을 수행합니다.
   - 예: `(a+)+` 정규식에 `aaaa...aaaa!` (끝에 느낌표가 포함되어 최종 매칭 실패)를 전달하면, 엔진은 모든 가능한 `a`의 그룹 조합(\(2^N\) 가지)을 연산하려다 스레드가 먹통이 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/api/validate`| POST | 없음 | `{"username": "악성 문자열"}` | 검증 결과 또는 타임아웃 에러 | ReDoS 타겟 필드 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 취약한 정규 표현식 구조 탐색
사용자 검증 폼의 정규식 패턴을 소스 검토를 통해 확인하거나, 다중 입력 테스트를 통해 매치 연산 속도 저하를 포착합니다.
- *정규식 예시*: `^([a-z]+)+$`

### Step 2. 백트래킹 유발 페이로드 설계
최종적으로 매치가 **실패**해야 하며, 앞부분은 정규식 규칙에 완벽히 매치되지만 맨 마지막 한 자리가 어긋나는 대량의 중복 문자열을 만듭니다.
- **패턴**: `a` 문자 40개 + 맨 마지막 특수 기호 `!`
- **페이로드**: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!`

### Step 3. 공격 요청 및 서버 CPU 점유 관찰
공격자는 작성한 페이로드를 POST 요청 인자로 실어 서버로 전송하고 응답 지연을 측정합니다.
- *전송 요청 (curl)*:
  ```bash
  # a의 개수를 늘려가며 연산 시간이 기하급수적으로(초 단위) 늘어나는지 관찰합니다.
  curl -X POST http://sanitizer.local/api/validate \
       -H "Content-Type: application/json" \
       -d '{"username": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!"}'
  ```
- *결과*: 서버가 즉각 에러나 성공을 주지 못하고 커넥션 대기(Blocking) 상태로 5초 이상 멈추는 현상이 발생합니다.

### Step 4. flag 획득
서버는 이 정규식 비교 때문에 CPU 점유율이 100%로 치솟으며 싱글 스레드 이벤트 루프가 블로킹 상태에 처하게 됩니다. 이에 따라 게이트웨이나 백엔드 에러 스택 파서가 타임아웃 인터럽트 에러(`RangeError: Maximum call stack size exceeded` 또는 Gateway Timeout)를 리턴하며, 해당 디버그용 에러 메시지 꼬리 정보에 숨겨져 있던 플래그(`FLAG{algorithmic_redos_complexity_dos_bypass}`)가 유출되어 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (Express & ReDoS 취약 예시)
const express = require('express');
const app = express();

app.use(express.json());

// 취약한 중첩 정규 표현식 패턴 (ReDoS 취약)
// ([a-zA-Z0-9]+)* 뒤에 @가 매칭되어야 하지만, 
// 끝에 @가 없는 아주 긴 문자열을 넘겨주면 엄청난 양의 백트래킹 유발
const EMAIL_REGEX = /^([a-zA-Z0-9]+)*@gmail.com$/;

@app.post("/api/validate", (req, res) => {
    const inputEmail = req.body.email;
    
    if (!inputEmail) {
        return res.status(400).json({ error: "Missing email" });
    }
    
    // 취약점 지점: 정규식 테스트 실행
    // aaaa... (약 40바이트) 문자열 입력 시 CPU가 수 초간 동작을 완전히 멈춤
    const startTime = Date.now();
    const isValid = EMAIL_REGEX.test(inputEmail);
    const duration = Date.now() - startTime;
    
    if (duration > 3000) {
        // 3초 이상 지연 유발 성공 시 디버그 정보와 함께 플래그 노출
        return res.json({
            status: "timeout_alert",
            message: "Algorithmic Complexity Warning!",
            flag: "FLAG{algorithmic_redos_complexity_dos_bypass}",
            time_taken_ms: duration
        });
    }
    
    return res.json({ status: "checked", valid: isValid });
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **정규 표현식 중첩 수량자 제거 (Avoid Nested Quantifiers)**:
   - 정규식을 작성할 때 그룹 내부 수량자 뒤에 전역 수량자를 덧붙이는 형태(`(a+)+`, `(a*)*`, `(a|b+)*`)를 전면 배제합니다.
   - 단일 선형 그룹 매칭으로 단순화하여 작성합니다: `^[a-zA-Z0-9]+@gmail\.com$`
2. **정규식 연산 시간 제한 및 타임아웃 라이브러리 연동**:
   - 자바스크립트 기본 `RegExp` 대신, 연산에 타임아웃 제한(예: 100ms 초과 시 강제 예외 리턴)을 걸 수 있는 정규식 안전 모듈을 사용합니다.
3. **Regex Safe Engine 사용 (예: Google RE2)**:
   - NFA(Nondeterministic Finite Automaton) 기반이 아닌, 백트래킹을 유발하지 않고 선형 시간(\(O(N)\)) 복잡도를 완벽히 보장하는 DFA(Deterministic Finite Automaton) 구조의 RE2 엔진(`safe-regex` 등 라이브러리)을 컴파일러로 채택합니다.

---
title: eval — 보안 용어 해설
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [security, glossary, web, injection, xss, payload, input-validation]
sources: [https://ko.wikipedia.org/wiki/Eval, https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval]
confidence: high
---

# eval — 보안 용어 해설

## Step 1. 단어 직역과 쉬운 비유

### 1) 단어 풀이
- **eval**은 **evaluate**에서 온 이름으로, “평가하다”, “계산하다”, “해석하다”라는 뜻입니다.
- 프로그래밍에서는 문자열이나 코드 표현을 실제 코드처럼 해석하고 실행하는 함수 또는 기능을 가리킵니다.

### 2) 한 문장 정의
**eval**은 문자열로 들어온 코드를 실행 가능한 코드로 해석해 결과를 반환하는 기능이며, 신뢰할 수 없는 입력과 결합하면 코드 실행·XSS 같은 심각한 보안 위험이 됩니다.

### 3) 쉬운 비유
`eval`은 “메모지에 적힌 문장을 그냥 읽는 사람”이 아니라, 메모지에 적힌 일을 **실제로 실행하는 직원**입니다. 메모지에 “2+2 계산”이 적혀 있으면 계산해 주지만, 누군가 “금고 열기” 같은 위험한 명령을 적어 넣으면 그대로 실행하려 할 수 있습니다.

## Step 2. 시각화

> `image_generate` 도구는 PNG 형식을 반환하므로, 시각화 이미지는 PNG URL로 임베드합니다.

![eval 시각화 — 문자열 입력이 코드 실행기로 들어가 실행 결과 또는 보안 위험으로 이어지는 구조](https://v3b.fal.media/files/b/0a9e3a17/tzLllW4ozlkbu7z5qU00Z_KCyDOe9p.png)

그림은 문자열 입력이 `eval` 코드 실행기를 거쳐 결과 또는 XSS/코드 실행 위험으로 이어지는 흐름을 보여줍니다. 핵심은 문자열이 단순 데이터가 아니라 코드로 해석된다는 점입니다.

## Step 3. 전문 설명

한국어 위키백과는 `eval`을 일부 프로그래밍 언어에서 제공하는 함수로, 문자열을 입력받아 그 문자열을 expression으로 처리한 뒤 결과값을 반환하는 함수라고 설명합니다. 문서는 신뢰할 수 없는 장소에서 온 데이터에 `eval`을 사용할 때 특별히 주의해야 한다고 설명합니다.

MDN은 JavaScript `eval()`이 문자열로 표현된 JavaScript 코드를 평가하고 completion value를 반환한다고 설명합니다. 또한 `eval()`에 전달된 인자는 동적으로 파싱되어 JavaScript로 실행되므로 injection sink가 될 수 있고, XSS 공격 벡터가 될 수 있다고 경고합니다.

Web CTF에서는 `eval`이라는 단어가 두 가지로 등장할 수 있습니다. 첫째, JavaScript/Python/PHP의 실제 `eval()` 함수처럼 문자열 실행 취약점으로 등장합니다. 둘째, `WebSockFish`처럼 체스 평가값(evaluation score)의 필드명으로 등장할 수 있습니다. 후자는 코드 실행 함수가 아니라 점수 필드지만, 서버가 클라이언트 값을 신뢰하면 [[tampering]] 대상이 됩니다.

## 공격자 관점

- 실제 `eval()` 함수가 사용자 입력을 실행하는지 확인합니다.
- 필터가 있으면 문자열 결합, 인코딩, 객체 접근, template expression 같은 우회 가능성을 봅니다.
- 단, 실습 환경 밖에서 실제 시스템을 대상으로 코드 실행을 시도하지 않습니다.
- WebSockFish처럼 `eval`이 필드명일 때는 [[websocket-message-tampering-ctf-patterns]] 관점에서 값 신뢰 여부를 확인합니다.

## 방어자 관점

- 신뢰할 수 없는 입력을 `eval()`에 전달하지 않습니다.
- JavaScript에서는 JSON 데이터 처리에 `JSON.parse()`를 사용하고, 표현식 계산은 allowlist 기반 파서로 제한합니다.
- CSP Trusted Types, sandboxing, 권한 최소화, 입력 검증을 함께 적용합니다.
- 게임 점수나 판정값은 서버가 직접 계산하고, 클라이언트가 보낸 `eval` 필드를 신뢰하지 않습니다.

## 관련 용어 링크

- [[xss]] — JavaScript eval이 유발할 수 있는 대표 클라이언트 취약점
- [[command-injection]] — 문자열이 명령 실행으로 이어지는 유사 위험
- [[ssti]] — 템플릿 표현식 실행과 연결되는 코드 실행 패턴
- [[websocket-message-tampering-ctf-patterns]] — WebSockFish의 `eval` 필드 변조 사례
- [[tampering]] — 코드 실행 함수가 아닌 필드값 조작 맥락

## 후속 분리 후보

- `Trusted Types`
- `injection sink`
- `JSON.parse`
- `sandbox`

## 참고 소스

- [한국어 위키백과 — Eval](https://ko.wikipedia.org/wiki/Eval)
- [MDN — eval()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval)

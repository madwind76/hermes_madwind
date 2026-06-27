---
title: Agent/Tool Security (에이전트 보안) — CTF 문제 유형
created: 2026-06-13
updated: 2026-06-21
type: ctf-challenge
tags: [ai-ctf, ctf, agent-security, llm, ctf-challenge, supply-chain, rce]
sources: [raw/20260610_AI_CTF_challenge_types.md]
confidence: high
---

# Agent/Tool Security (에이전트 보안) — CTF 문제 유형

> 2025-2026년 급부상 분야. LangChain, MCP, A2A 프로토콜 등장으로 AI CTF의 주요 축으로 부상. 전체 AI CTF 문제의 **~19%**를 차지합니다.

## 참고 URL
- [Reference](raw/20260610_AI_CTF_challenge_types.md)

## 개요

Agent/Tool Security는 LLM이 외부 도구(함수, API, 데이터베이스, 코드 실행)를 호출할 때 발생하는 보안 취약점을 다룹니다. 단순한 프롬프트 인젝션을 넘어, LLM이 실제 시스템에 접근할 수 있는 **Agentic AI** 환경에서의 공격 벡터에 초점을 맞춥니다.

## 세부 유형

### B1. Tool/Function Injection (도구 인젝션)

- **개념**: LLM이 호출하는 함수/도구의 파라미터를 인젝션으로 조작
- **난이도**: ⭐⭐⭐⭐ (중고급)
- **출처**: `ai-prompt-ctf L7` (SQL + 파일 접근), `Machine_Learning_CTF/Dolos II`
- **기술**: SQL injection via LLM tool parameter, path traversal in file tools

### B2. A2A Agent Exploitation (에이전트간 공격)

- **개념**: Multi-Agent 시스템에서 에이전트 간 신뢰 관계 악용
- **난이도**: ⭐⭐⭐⭐⭐ (고급)
- **출처**: `Machine_Learning_CTF/Matrix`, `Machine_Learning_CTF/Rogue`
- **기술**: A2A 프로토콜 변조, Agent Capability 우회, Inter-Agent Trust 사칭

**소스코드 핵심 (Rogue challenge):**
```python
# Rogue challenge: Financial Assistant가 Research Agent에게 데이터 요청
# → Research Agent의 결과를 조작하여 부정 송금 유도
# A2A protocol의 AgentCard에 허위 capability 등록
```

### B3. MCP Supply Chain Attack (MCP 공급망 공격)

- **개념**: MCP(Model Context Protocol) 서버 변조로 AI 클라이언트 공격
- **난이도**: ⭐⭐⭐⭐⭐ (고급)
- **출처**: `Machine_Learning_CTF/Mirage`
- **기술**: MCP Server Signature Cloaking, 악성 tool 등록, supply chain injection

### B4. RCE via LLM Tools (LLM 도구 → RCE)

- **개념**: LLM이 실행하는 코드/도구를 통해 원격 코드 실행
- **난이도**: ⭐⭐⭐⭐ (중고급)
- **출처**: `Machine_Learning_CTF/Dolos`, `ai-prompt-ctf L9`
- **기술**: Python eval injection, shell command injection via LLM-generated code

## 공격 체인 예시

Agent/Tool Security 문제의 전형적인 공격 체인:

```text
1. LLM이 사용자 입력을 받아 tool 호출 결정
2. 사용자 입력이 tool 파라미터에 직접 매핑됨 (입력 검증 미흡)
3. 악성 파라미터가 tool을 통해 시스템 명령어/SQL 쿼리로 전달
4. flag 추출 또는 원격 코드 실행 달성
```

## 문제 출제 공식

```text
1. LLM + Tool 호출 시스템 구축 (예: 웹 검색, SQL 쿼리, 파일 읽기)
2. Tool 호출의 입력 검증 미흡
3. 참가자가 LLM을 통해 tool 파라미터 조작
```

## 대표 저장소

- [alexdevassy/Machine_Learning_CTF_Challenges](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges) (235⭐) — Dolos, Matrix, Rogue, Mirage 등 9개 문제
- [c-goosen/ai-prompt-ctf](https://github.com/c-goosen/ai-prompt-ctf) (33⭐) — L7~L9 Tool Injection

## OWASP LLM 매핑

| CTF 유형 | OWASP LLM (2025) |
|---------|------------------|
| Tool/Function Injection | LLM08: Tool Usage Control |
| RCE via LLM Tools | LLM08: Tool Usage Control |
| A2A Agent Exploitation | LLM08: Tool Usage Control |
| MCP Supply Chain | LLM05: Supply Chain |

---

관련 페이지: [[ai-ctf-overview]], [[prompt-injection-ctf]]

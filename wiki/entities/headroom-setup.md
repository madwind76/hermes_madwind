---
title: Headroom — 설치 및 아키텍처
created: 2026-06-10
updated: 2026-06-21
type: tool
tags: [tool, llm, ai-ml, optimization, proxy, mcp]
sources: [raw/20260610_Headroom_완전분석.md]
confidence: high
---
> [[headroom]]의 분할 페이지입니다.

# Headroom — 설치 및 아키텍처

# Headroom — LLM Context Compression Layer

> ⭐ 20,138 · Apache 2.0 · github.com/chopratejas/headroom
> 로컬 설치 완료: `headroom-ai v0.24.0` (Hermes venv)
> 공식문서: https://headroom-docs.vercel.app/docs

## 참고 URL
- [Internal raw source](raw/20260610_Headroom_완전분석.md)

## 개요

**Headroom은 LLM 애플리케이션을 위한 컨텍스트 최적화 레이어다.** AI 에이전트가 읽는 모든 것 (툴 출력, 로그, RAG 청크, 파일, 대화 기록) 을 LLM에 보내기 전에 압축하여 **동일한 답변 품질에 토큰을 60-95% 절약**한다.

아키텍처 흐름:

```
Agent / App → Headroom (CacheAligner → ContentRouter → CCR) → Compressed Prompt → LLM
```

- ContentRouter: SmartCrusher (JSON), CodeCompressor (AST), Kompress-base (text, HF)
- CCR (Reversible Compression): 압축해도 원본 보존, LLM이 필요시 `headroom_retrieve` 조회
- Cross-Agent Memory: 여러 에이전트(Claude, Codex, Gemini)가 공유 메모리 사용
- `headroom learn`: 실패 세션 분석 → `CLAUDE.md`/`AGENTS.md`에 교정사항 자동 작성

Headroom은 AI CTF 대비 측면에서도 중요하다. [[ai-ctf-overview|AI CTF 개요]]의 Agent/Tool Security 분야에서 MCP 기반 공급망 공격, 프록시 레이어 보안 등과 직접 연관된다. Headroom 자체가 MCP 서버로 동작할 수 있기 때문에, MCP 생태계의 공격 표면 분석에도 관련된다.

## 4가지 사용 모드

### 모드 A: Agent Wrap (1커맨드)

```bash
pip install "headroom-ai[all]"
headroom wrap claude    # Claude Code
headroom wrap codex     # Codex CLI
headroom wrap cursor    # Cursor
headroom wrap aider     # Aider
headroom wrap copilot   # GitHub Copilot CLI
```

**원리**: 환경변수(API URL 등)를 Headroom 프록시로 리다이렉트 → 모든 트래픽 자동 압축

### 모드 B: Proxy (코드 변경 0)

```bash
headroom proxy --port 8787
# ANTHROPIC_BASE_URL=http://localhost:8787
# OPENAI_BASE_URL=http://localhost:8787
```

LLM API 호출을 프록시가 가로채서 요청 본문 압축 후 원래 API로 전달.

### 모드 C: Library (인라인)

```python
from headroom import compress

messages = [
    {"role": "user", "content": "시스템 로그에서 에러를 찾아줘"},
    {"role": "tool",  "content": json.dumps(100개_로그_항목)},
]
result = compress(messages, model="gpt-4o")
# result.messages → 압축된 메시지를 LLM에 전송
```

TypeScript: `import { compress } from "headroom-ai"`

### 모드 D: Framework Integration

| 프레임워크 | 통합 방법 |
|-----------|----------|
| Anthropic/OpenAI SDK | `withHeadroom(new Anthropic())` |
| Vercel AI SDK | `wrapLanguageModel({ model, middleware: headroomMiddleware() })` |
| LiteLLM | `litellm.callbacks = [HeadroomCallback()]` |
| LangChain | `HeadroomChatModel(your_llm)` |
| Agno | `HeadroomAgnoModel(your_model)` |
| ASGI 앱 | `app.add_middleware(CompressionMiddleware)` |
| MCP 클라이언트 | `headroom mcp install` |


## 관련 위키 링크
- [[headroom]] — 인덱스
- LLM 컨텍스트 압축 프록시 계층
- 위키 운영 배경

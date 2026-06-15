---
title: Headroom — 성능 및 비교
created: 2026-06-10
updated: 2026-06-13
type: tool
tags: [tool, llm, ai-ml, optimization, proxy, mcp]
sources: [raw/20260610_Headroom_완전분석.md]
confidence: high
---
> [[headroom]]의 분할 페이지입니다.

# Headroom — 성능 및 비교

## 아키텍처

### 6가지 압축 알고리즘

| 알고리즘 | 대상 | 방식 | 압축률 |
|---------|------|------|--------|
| **SmartCrusher** | JSON 배열 (툴 출력) | 통계적 분석: 에러·이상값·경계만 보존 | 70-90% |
| **CodeCompressor** | 소스코드 | AST 기반: 시그니처 보존, body 압축 | 40-70% |
| **Kompress-base** | 일반 텍스트 | HuggingFace ModernBERT token classification | 30-50% |
| **Image Compression** | 이미지 | ML 라우터로 최적 resize/quality 선택 | 40-90% |
| **CacheAligner** | 프롬프트 접두사 | Anthropic/OpenAI KV 캐시 hit율 최적화 | 간접적 |
| **IntelligentContext** | 전체 컨텍스트 | 중요도 기반 점수화 + learned importance | 상황별 |

### CCR (Reversible Compression)

- 압축해도 **원본은 절대 삭제되지 않음**
- LLM이 필요하면 `headroom_retrieve` 툴로 원본 조회 가능
- 투명성 + 효율성 동시 확보

## 설치 방법

### 기본 설치

```bash
# Python (전체 설치)
pip install "headroom-ai[all]"

# TypeScript / Node
npm install headroom-ai

# Docker
docker pull ghcr.io/chopratejas/headroom:latest
```

### 선택적 extras

| extra | 포함 기능 |
|-------|----------|
| `[all]` | 전부 |
| `[proxy]` | 프록시 서버 |
| `[mcp]` | MCP 서버 도구 |
| `[ml]` | Kompress-base (HuggingFace 모델) |
| `[code]` | CodeCompressor (AST 압축) |
| `[memory]` | Cross-agent memory (Qdrant/Neo4j) |
| `[image]` | 이미지 압축 |
| `[langchain]` | LangChain 통합 |
| `[agno]` | Agno 통합 |
| `[evals]` | 벤치마크 실행 |

**요구사항**: Python 3.10+


## 관련 위키 링크
- [[headroom]] — 인덱스
- LLM 컨텍스트 압축 프록시 계층
- 위키 운영 배경

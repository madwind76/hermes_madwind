---
title: Headroom — 운영 및 모니터링
created: 2026-06-10
updated: 2026-06-13
type: tool
tags: [tool, llm, ai-ml, optimization, proxy, mcp]
sources: [raw/20260610_Headroom_완전분석.md]
confidence: high
---
> [[headroom]]의 분할 페이지입니다.

# Headroom — 운영 및 모니터링

## 성능 벤치마크

### 실제 워크로드 토큰 절약

| 워크로드 | Before | After | 절약 |
|---------|-------:|------:|:----:|
| 코드 검색 (100개 결과) | 17,765 | 1,408 | **92%** |
| SRE 장애 디버깅 | 65,694 | 5,118 | **92%** |
| GitHub 이슈 트라이지 | 54,174 | 14,761 | **73%** |
| 코드베이스 탐색 | 78,502 | 41,254 | **47%** |

### 정확도 유지 (벤치마크)

| 벤치마크 | 분류 | Baseline | Headroom | 차이 |
|---------|------|---------:|---------:|:---:|
| GSM8K | 수학 | 0.870 | 0.870 | **±0.000** |
| TruthfulQA | 사실 | 0.530 | 0.560 | **+0.030** |
| SQuAD v2 | QA | — | **97%** | 19% 압축 |
| BFCL | 도구 | — | **97%** | 32% 압축 |

### 컨텐츠 타입별 압축률

| 타입 | 압축 방식 | 일반적 절약 |
|------|----------|:----------:|
| JSON 배열 (툴 출력) | SmartCrusher | 70-90% |
| 소스코드 | CodeCompressor (AST) | 40-70% |
| 빌드/테스트 로그 | SmartCrusher + Kompress | 80-95% |
| 검색 결과 | IntelligentContext (순위화) | 60-80% |
| 일반 텍스트 | Kompress-base | 30-50% |
| Git diffs | CodeCompressor | 40-60% |
| 이미지 | ML 라우터 | 40-90% |

## 유사 도구 비교

| 도구 | 범위 | 배포 | 로컬 | 복원 가능 |
|------|------|------|:---:|:---------:|
| **Headroom** | 모든 컨텍스트 | Proxy · Library · MCP | ✅ | ✅ (CCR) |
| RTK | CLI 명령 출력 | CLI wrapper | ✅ | ❌ |
| lean-ctx | CLI 명령, MCP, 에디터 규칙 | CLI · MCP | ✅ | ❌ |
| Compresr / Token Co. | 텍스트 | Hosted API | ❌ | ❌ |
| OpenAI Compaction | 대화 기록 | Provider-native | ❌ | ❌ |

Headroom의 차별점: 모든 컨텐츠 타입, 모든 주요 프레임워크, 로컬 실행, 복원 가능 (CCR)

## 에이전트 호환성

| 에이전트 | `headroom wrap` | 비고 |
|---------|:--------------:|------|
| Claude Code | ✅ | `--memory` · `--code-graph` |
| Codex CLI | ✅ | Claude와 메모리 공유 |
| Cursor | ✅ | 설정 출력 — 한 번 붙여넣기 |
| Aider | ✅ | 프록시 실행 + 런칭 |
| Copilot CLI | ✅ | 프록시 실행 + 런칭 |
| OpenClaw | ✅ | ContextEngine 플러그인 설치 |

모든 OpenAI 호환 클라이언트는 `headroom proxy`로 사용 가능.

## 보안 고려사항

| 측면 | Headroom의 처리 |
|------|----------------|
| 데이터 프라이버시 | **로컬 실행**. 데이터가 내 머신을 벗어나지 않음 |
| 원본 보존 | CCR — 원본 데이터는 로컬에 보관, LLM이 필요시 retrieval |
| 암호화 | 프록시 모드에서 전송 데이터는 TLS 유지 |
| API 키 | Headroom이 API 키를 보거나 저장하지 않음 |

## 헬스 체크 & 모니터링

```bash
# 절약 통계 확인
headroom stats

# 성능 벤치마크 실행
python -m headroom.evals suite --tier 1

# 실시간 메트릭
curl http://localhost:8787/metrics
```

## 로컬 설치 상태

- **패키지**: `headroom-ai v0.24.0`
- **설치 경로**: `/home/kisec/.hermes/hermes-agent/venv/lib/python3.11/site-packages`
- **실행 파일**: `/home/kisec/.hermes/hermes-agent/venv/bin/headroom`
- **설치 시점**: Hermes Agent venv에 포함되어 사전 설치됨

```bash
# 로컬에서 사용 가능한 명령 확인
headroom --version   # headroom, version 0.24.0
# 사용 예:
# headroom wrap claude
# headroom proxy --port 8787
# headroom stats
```

## 관련 페이지

- [[ai-ctf-overview|AI CTF 개요]] — Agent/Tool Security 분야와 연결 (Headroom의 MCP 레이어가 CTF 공격 표면)
- [[agent-security-ctf|Agent/Tool Security CTF]] — MCP 공급망 공격, 에이전트 간 메모리 보안
- llm-context-proxy 관련 개념 — 컨텍스트 압축 프록시 아키텍처와 Headroom의 Proxy 모드

## 요약

```
Headroom = LLM 컨텍스트 압축 레이어

특징:
  ✅ 60-95% 토큰 절약 (같은 답변)
  ✅ 6가지 압축 알고리즘 (JSON, 코드, 텍스트, 이미지, 로그++)
  ✅ 4가지 사용 모드 (wrap / proxy / library / MCP)
  ✅ 로컬 실행 (데이터 내 머신)
  ✅ 복원 가능 (CCR — 원본 유지)
  ✅ 크로스 에이전트 메모리
  ✅ 실패 학습 (headroom learn)

설치: pip install "headroom-ai[all]"
시작: headroom wrap claude
문서: https://headroom-docs.vercel.app/docs
```

^[raw/20260610_Headroom_완전분석.md]
## 관련 위키 링크
- [[headroom]] — 인덱스
- LLM 컨텍스트 압축 프록시 계층
- 위키 운영 배경

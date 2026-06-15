---
title: AI CTF 개요 및 유형 분류
created: 2026-06-10
updated: 2026-06-10
type: concept
tags: [ai-ctf, ctf, prompt-injection, adversarial-ml, llm, ctf-challenge]
sources: [raw/20260610_AI_CTF_challenge_types.md]
confidence: high
---

# AI CTF 개요 및 유형 분류

> AI 보안 CTF(Capture The Flag) 문제의 전반적인 분류 체계와 통계를 정리합니다.
> 조사 대상: GitHub 공개 소스 CTF 문제 (⭐12 이상, 실제 소스코드 포함)

## 개요

AI CTF는 인공지능/머신러닝 시스템의 보안 취약점을 탐구하는 CTF 문제 유형입니다. 초기에는 ML 모델의 적대적 공격(Adversarial ML)이 주류였으나, 2023-2026년 LLM의 폭발적 성장과 함께 **프롬프트 인젝션(Prompt Injection)** 이 가장 흔한 유형으로 자리잡았습니다.

2025-2026년에는 **Agent/Tool Security** 분야가 급부상하며 (LangChain, MCP, A2A 프로토콜 등장), AI CTF의 범위가 LLM 보안 전반으로 확장되고 있습니다.

## AI CTF 문제 유형 분류 (8개 대분류)

AI CTF 문제는 아래 8개 대분류로 체계화됩니다. 자세한 내용은 각 카테고리 페이지를 참조하세요.

### 🅰 [[prompt-injection-ctf|Prompt Injection (프롬프트 인젝션)]]
AI CTF의 **가장 기본적이면서도 핵심 유형**으로 전체의 ~47%를 차지합니다.
- **세부 유형**: Direct Injection, Prompt Extraction, Goal Manipulation, Indirect Injection, Filter/Guardrail Bypass, Multi-modal Injection, Multi-turn Injection
- **난이도 범위**: ⭐ (초급) ~ ⭐⭐⭐⭐⭐ (고급)
- **대표 저장소**: `ai-goat`, `ai-prompt-ctf`, `TensorTrust`, `LLM-Security-CTF`

### 🅱 [[agent-security-ctf|Agent/Tool Security (에이전트 보안)]]
2025-2026년 급부상 분야로 ~19%를 차지합니다.
- **세부 유형**: Tool/Function Injection, A2A Agent Exploitation, MCP Supply Chain Attack, RCE via LLM Tools
- **난이도 범위**: ⭐⭐⭐⭐ ~ ⭐⭐⭐⭐⭐ (중고급~고급)
- **대표 저장소**: `Machine_Learning_CTF_Challenges` (Dolos, Matrix, Rogue, Mirage)

### 🅲 [[adversarial-ml-ctf|Model Inversion/Extraction (모델 역공학)]]
전통적인 ML 보안 CTF의 핵심, 고난도 유형으로 ~6%를 차지합니다.
- **세부 유형**: Model Inversion, Model Extraction, Membership Inference
- **난이도 범위**: ⭐⭐⭐⭐ ~ ⭐⭐⭐⭐⭐ (중고급~고급)
- **대표 저장소**: `Machine_Learning_CTF_Challenges` (Vault, Fourtune)

### 🅳 [[adversarial-ml-ctf|Adversarial ML (적대적 ML)]]
초기 AI CTF의 주류였으며 ~9%를 차지합니다.
- **세부 유형**: Evasion Attacks, Adversarial Examples
- **난이도 범위**: ⭐⭐⭐ ~ ⭐⭐⭐⭐ (중급~중고급)
- **대표 저장소**: `ai_for_the_win`, `adversarial_ml_ctf`

### 🅴 [[adversarial-ml-ctf|Data Poisoning / Training Data Poisoning (데이터 오염)]] — OWASP LLM03
중난도 유형으로 ~6%를 차지합니다. LLM 훈련 데이터에 백도어/악성 데이터를 주입하여 모델 출력을 조작합니다.
- **세부 유형**: Training-time Poisoning, Backdoor Detection, Trigger-based Manipulation
- **난이도 범위**: ⭐⭐⭐⭐ ~ ⭐⭐⭐⭐⭐ (중고급~고급)
- **대표 저장소**: `Machine_Learning_CTF_Challenges` (Heist), `ai_for_the_win` (Model Poisoning)
- **공개 CTF**: BackdoorLLM (트리거 기반 백도어 주입 챌린지)

### 🅵 Model Serialization / Supply Chain (직렬화·공급망 공격) — OWASP LLM04
AI 공급망 취약점을 활용한 공격으로 ~8%를 차지합니다. 악성 모델 파일, MCP 서버 변조 등을 포함합니다.
- **세부 유형**: Pickle Deserialization RCE, Weight Manipulation, MCP Supply Chain Attack, Malicious Plugin
- **난이도 범위**: ⭐⭐⭐ ~ ⭐⭐⭐⭐⭐ (중급~고급)
- **대표 저장소**: `Machine_Learning_CTF_Challenges` (Persuade, Mirage), `AtHackCTF` (AI Leaky ReLU)
- **공개 CTF**: Garak CTF (HF 데이터셋 공급망), LangChain Bad Plugin 시나리오

### 🅶 AI Application Logic / Sensitive Info Disclosure (애플리케이션 로직·민감정보 노출) — OWASP LLM06
실용적인 웹 보안 + LLM 결합 유형으로 ~7%를 차지합니다. LLM 출력을 통한 민감 정보 노출(훈련 데이터 추출, PII 유출)을 포함합니다.
- **세부 유형**: SSRF via LLM Output, SQLi via LLM Tools, Training Data Extraction, Prompt Extraction
- **난이도 범위**: ⭐⭐ ~ ⭐⭐⭐⭐ (초중급~중고급)
- **대표 저장소**: `ai-goat` (Challenge 2), `Machine_Learning_CTF_Challenges` (Dolos II), TensorTrust
- **공개 CTF**: Garak CTF (PII Leakage), LLM Memorization Extraction

### 🅷 AI Supply Chain / Overreliance (AI 공급망·과의존) — OWASP LLM09
가장 최신 분야로 ~3%를 차지합니다. AI 에이전트가 과도한 권한을 행사하거나 인간의 감독 없이 자율적으로 위험한 결정을 내리는 취약점을 포함합니다.
- **세부 유형**: Excessive Agency, Human-in-the-Loop Bypass, Goal Manipulation, MCP Supply Chain
- **난이도 범위**: ⭐⭐⭐⭐⭐ (고급)
- **대표 저장소**: `Machine_Learning_CTF_Challenges` (Mirage), `OWASP Agentic AI CTF FinBot`
- **공개 CTF**: OWASP FinBot (urgency bypass, CEO impersonation), Agent Overreach (자동 결제/이메일 전송)

## 전체 통계

### 유형별 문제 수

| 유형 | 문제 수 | 비율 | 평균 난이도 |
|------|--------|------|-----------|
|| 🅰 Prompt Injection | ~15 | 47% | 초~중급 | LLM01 |
|| 🅱 Agent/Tool Security | ~6 | 19% | 중~고급 | LLM08 |
|| 🅳 Adversarial ML | ~3 | 9% | 중~고급 | — |
|| 🅴 Data Poisoning (LLM03) | ~2 | 6% | 중~고급 | **LLM03** |
|| 🅵 Model Serialization/Supply Chain (LLM04) | ~3 | 8% | 중~고급 | **LLM04** |
|| 🅲 Model Inversion/Extraction | ~2 | 6% | 고급 | LLM10 |
|| 🅶 App Logic/Sensitive Info (LLM06) | ~3 | 7% | 초~중고급 | **LLM06** |
|| 🅷 Supply Chain/Overreliance (LLM09) | ~2 | 3% | 고급 | **LLM09** |
|| **TOTAL** | **~36+** | **100%** | — | **LLM01-10 전범위** |

### 기술 스택별 분포

- **OpenAI API (GPT-4 등)**: 높음 (프롬프트 인젝션)
- **Flask/FastAPI**: 높음 (Web wrapper)
- **Docker / Docker Compose**: 매우 높음 (거의 모든 문제)
- **TensorFlow/Keras**: 중간 (ML Security)
- **PyTorch**: 중간 (Serialization, Weight)
- **LangChain/LlamaIndex**: 중간 (Agent Security)
- **llama-cpp-python (로컬 LLM)**: 낮음
- **MCP / A2A Protocol**: 낮음 (최신 트렌드)
- **HuggingFace Transformers**: 낮음
- **Guardrails (Rebuff, Prompt-Guard)**: 낮음 (우회 문제)

### 난이도 분포

| 난이도 | 비율 | 주요 유형 |
|--------|------|---------|
| 초급 (⭐) | 25% | Direct Injection, SSRF |
| 중급 (⭐⭐⭐) | 35% | Filter Bypass, Goal Manipulation, SQLi |
| 고급 (⭐⭐⭐⭐⭐) | 40% | Model Inversion, A2A Exploit, MCP, Weight Manipulation |

## 참고 저장소 목록

### 가장 추천하는 저장소 (교육용)

| 저장소 | ⭐ | 추천 이유 | 문제 수 |
|--------|---|---------|--------|
| [dhammon/ai-goat](https://github.com/dhammon/ai-goat) | 344 | 가장 접근성 좋음. 로컬 실행, Docker 지원, 초보자 친화적 | 2 |
| [alexdevassy/Machine_Learning_CTF_Challenges](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges) | 235 | 가장 다양한 유형. 9개 문제로 AI 보안 전반 커버 | 9 |
| [c-goosen/ai-prompt-ctf](https://github.com/c-goosen/ai-prompt-ctf) | 33 | 단계별 학습 최적화. 11개 Level, BSIDES 검증 | 11 |
| [depalmar/ai_for_the_win](https://github.com/depalmar/ai_for_the_win) | 149 | 50+ 랩 + CTF. 종합 AI 보안 학습 | 4+ |
| [HumanCompatibleAI/tensor-trust](https://github.com/HumanCompatibleAI/tensor-trust) | 70 | PvP 게임화. 프롬프트 인젝션 심화 학습 | ∞ |

### 기타 저장소

- [c-goosen/ai-prompt-ctf](https://github.com/c-goosen/ai-prompt-ctf) (33⭐) — 11개 Level 단계별 학습
- [TrustAI-laboratory/LLM-Security-CTF](https://github.com/TrustAI-laboratory/LLM-Security-CTF) (17⭐) — LLM 프롬프트 인젝션
- [athack-ctf/AtHackCTF-2025-Challenges](https://github.com/athack-ctf/AtHackCTF-2025-Challenges) (14⭐) — 신경망 가중치 조작
- [AdityaBhatt3010/OWASP-Agentic-AI-CTF-FinBot](https://github.com/AdityaBhatt3010/OWASP-Agentic-AI-CTF-FinBot) (12⭐) — Agent Goal Manipulation
- [arturmiller/adversarial_ml_ctf](https://github.com/arturmiller/adversarial_ml_ctf) (6⭐) — Adversarial 이미지

### OWASP LLM & AI 매핑

| CTF 문제 유형 | OWASP LLM (2025) | OWASP ML | 공개 CTF 예시 |
|--------------|------------------|----------|-------------|
| Prompt Injection | LLM01: Prompt Injection | — | ai-goat Ch1, ai-prompt-ctf L0-L10 |
| Insecure Output Handling | LLM02: Insecure Output Handling | — | ai-goat Ch2 (SSRF) |
| **Training Data Poisoning** | **LLM03: Training Data Poisoning** | **ML02: Data Poisoning** | **ML_CTF/Heist**, ai_for_the_win/Model Poisoning |
| **Supply Chain Vulnerabilities** | **LLM04: Supply Chain Vulnerabilities** | **ML05: Supply Chain** | **ML_CTF/Mirage** (MCP supply chain), ML_CTF/Persuade (pickle RCE) |
| Model Serialization | — | ML06: Model Theft | ML_CTF/Persuade, AtHackCTF/AI Leaky ReLU |
| **Sensitive Information Disclosure** | **LLM06: Sensitive Information Disclosure** | — | **Garak CTF** (training data extraction), TensorTrust (prompt extraction) |
| Data Leakage | LLM07: Data Leakage | — | ai-goat Ch1, TensorTrust |
| Agent Tool Injection | LLM08: Tool Usage Control | — | ML_CTF/Dolos, ai-prompt-ctf L7 |
| **Overreliance / Excessive Agency** | **LLM09: Overreliance** | — | **OWASP Agentic AI CTF FinBot** (goal manipulation, urgency bypass) |
| Model Theft | LLM10: Model Theft | ML06: Model Theft | ML_CTF/Fourtune (model extraction) |

---

관련 페이지: [[prompt-injection-ctf]], [[agent-security-ctf]], [[adversarial-ml-ctf]]
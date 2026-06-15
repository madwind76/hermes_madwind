---
title: Adversarial ML / Model Inversion CTF 문제 유형 상세
created: 2026-06-10
updated: 2026-06-10
type: ctf-challenge
tags: [ai-ctf, ctf, adversarial-ml, model-inversion, data-poisoning, model-extraction, ctf-challenge, serialization]
sources: [raw/20260610_AI_CTF_challenge_types.md]
confidence: high
---

# Adversarial ML & Model Inversion — CTF 문제 유형

> 전통적인 ML 보안 CTF의 핵심에서 최신 AI 공급망 위협까지. 전체 AI CTF 문제의 **~27%**를 차지합니다 (🅲+🅳+🅴+🅵+🅷).

## 개요

이 페이지는 AI CTF 중 ML 모델 자체를 대상으로 하는 고난도 유형들을 다룹니다. 모델 역공학(Model Inversion/Extraction), 적대적 ML(Adversarial ML), 데이터 오염(Data Poisoning), 직렬화 공격(Model Serialization), 그리고 AI 공급망(Supply Chain)까지 포함합니다.

---

## 🅲 Model Inversion/Extraction (모델 역공학)

### C1. Model Inversion (모델 역변환)

- **개념**: 모델의 출력만으로 학습 데이터(민감 정보) 복원
- **난이도**: ⭐⭐⭐⭐⭐ (고급)
- **출처**: `Machine_Learning_CTF/Vault`
- **난이도 표기**: **Hard** (Machine_Learning_CTF 중 유일한 Hard)
- **기술**: TensorFlow 신경망에 접근제어 모델 구현 → Confidence score 기반 역변환

### C2. Model Extraction (모델 도난)

- **개념**: API 쿼리만으로 대상 모델의 복제본 생성
- **난이도**: ⭐⭐⭐⭐ (중고급)
- **출처**: `Machine_Learning_CTF/Fourtune`
- **기술**: Prediction query → model distillation → substitute model 구축 → 추가 공격

### C3. Membership Inference (멤버십 추론)

- **개념**: 특정 데이터가 모델 학습에 사용되었는지 추론
- **난이도**: ⭐⭐⭐⭐ (중고급)
- **출처**: 직접 CTF 예는 드물지만, SaTML CTF 및 MLSP CTF에서 출제

---

## 🅳 Adversarial ML (적대적 ML)

### D1. Evasion Attacks (회피 공격)

- **개념**: 미세한 입력 변조로 ML 분류기 오작동 유발
- **난이도**: ⭐⭐⭐ (중급)
- **출처**: `ai_for_the_win/Adversarial Samples`, `arturmiller/adversarial_ml_ctf`
- **기술**: Feature perturbation (FGSM), imperceptible noise injection

**소스코드 핵심:**
```python
# 악성코드 분류기를 회피하는 feature 변조
# 예: malware_probability가 50% 미만이면 정상으로 판정
# FGSM을 사용하여 특정 feature 조정
```

### D2. Adversarial Examples (적대적 예제)

- **개념**: 사람은 구분 못하지만 모델을 속이는 입력 생성
- **난이도**: ⭐⭐⭐⭐ (중고급)
- **기술**: PGD, CW attack, boundary attack

---

## 🅴 Data Poisoning/Backdoor (데이터 오염)

### E1. Training-time Poisoning (학습 오염)

- **개념**: 학습 데이터에 악성 샘플을 주입하여 모델 동작 조작
- **난이도**: ⭐⭐⭐⭐ (중고급)
- **출처**: `Machine_Learning_CTF/Heist`
- **기술**: Backdoor trigger insertion (예: 특정 패턴이 있는 입력에만 오작동)
- **특징**: TensorFlow + h5py로 poisoned model 배포

### E2. Backdoor Detection (백도어 탐지)

- **개념**: 주어진 모델에서 백도어 트리거 탐지
- **난이도**: ⭐⭐⭐⭐⭐ (고급)
- **출처**: `ai_for_the_win/Model Poisoning`
- **기술**: Training pipeline audit, trigger pattern analysis, STRIP 기법

---

## 🅵 Model Serialization Attacks (직렬화 공격)

AI 공급망에서 가장 현실적인 위협입니다.

### F1. Pickle Deserialization RCE

- **개념**: 악성 PyTorch/TensorFlow 모델 파일을 로드할 때 RCE
- **난이도**: ⭐⭐⭐ (중급)
- **출처**: `Machine_Learning_CTF/Persuade`
- **기술**: `__reduce__`를 이용한 pickle payload, `torch.load()` 악용

**소스코드 핵심:**
```python
# pickle.load()에서 실행되는 악성 __reduce__ 체인
class Exploit:
    def __reduce__(self):
        return (os.system, ('cat /flag.txt',))
```

### F2. Weight Manipulation (가중치 변조)

- **개념**: 모델 가중치(weights)를 직접 변조하여 출력 조작
- **난이도**: ⭐⭐⭐⭐⭐ (고급)
- **출처**: `AtHackCTF/AI Leaky ReLU`
- **기술**: 사용자 정의 activation function 해석, `.pth` 파일 내 flag 인코딩 방식 분석

**소스코드 핵심:**
```python
# 12개의 커스텀 activation 함수가 flag 문자를 인코딩
# 제출된 .pth weights가 모델을 통해 flag로 변환되는 파이프라인
```

---

## 🅶 AI Application Logic (애플리케이션 로직)

### G1. SSRF via LLM Output

- **개념**: LLM이 생성한 URL을 서버가 요청할 때 SSRF 발생
- **난이도**: ⭐⭐ (초중급)
- **출처**: `ai-goat Challenge 2`
- **기술**: LLM이 "http://localhost:8080/" 같은 URL을 생성하도록 유도 → 숨겨진 내부 서비스 접근

### G2. SQLi via LLM Tools

- **개념**: LLM의 SQL 툴 호출을 조작하여 SQL injection
- **난이도**: ⭐⭐⭐ (중급)
- **출처**: `Machine_Learning_CTF/Dolos II`
- **기술**: LLM → SQL Query 생성 → Injection 삽입

---

## 🅷 AI Supply Chain (AI 공급망)

가장 최신 분야로, 아직 CTF 문제는 드물지만 중요도가 빠르게 증가 중입니다.

- **MCP Supply Chain**: `Machine_Learning_CTF/Mirage` — [[agent-security-ctf]] B3 참조
- **Malicious npm model packages**: 최근 뉴스에서 Claude AI 유저 공격 (악성 npm 패키지)
- **HuggingFace Hub 악성 모델**: pickle 기반 RCE 가능 (현재까지 CTF 문제는 미확인)

---

## 문제 출제 공식 (ML 모델)

```text
1. 취약한 모델 (pickle, poisoned weights, exposed API) 배포
2. 참가자가 모델 파일 분석 / API 호출
3. 모델의 취약점을 통해 flag 추출
```

## 대표 저장소

- [alexdevassy/Machine_Learning_CTF_Challenges](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges) (235⭐) — Vault, Fourtune, Heist, Persuade
- [depalmar/ai_for_the_win](https://github.com/depalmar/ai_for_the_win) (149⭐) — Adversarial Samples, Model Poisoning
- [athack-ctf/AtHackCTF-2025-Challenges](https://github.com/athack-ctf/AtHackCTF-2025-Challenges) (14⭐) — AI Leaky ReLU
- [arturmiller/adversarial_ml_ctf](https://github.com/arturmiller/adversarial_ml_ctf) (6⭐) — Adversarial 이미지

## OWASP 매핑

| CTF 유형 | OWASP LLM (2025) | OWASP ML |
|---------|------------------|----------|
| Model Serialization | LLM05: Supply Chain | ML06: Model Theft |
| Adversarial ML | — | ML03: Evasion |
| Data Poisoning | — | ML02: Data Poisoning |
| Model Extraction | LLM10: Model Theft | ML06: Model Theft |

---

관련 페이지: [[ai-ctf-overview]], [[prompt-injection-ctf]], [[agent-security-ctf]]
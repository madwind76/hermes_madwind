---
title: CTF Writeup Ingestion Workflow
created: 2026-06-19
updated: 2026-06-21
type: concept
tags: [ctf, research, training, workflow, wiki]
sources: [queries/picoctf-web-survey.md, concepts/web-ctf-writeup-topic-map.md, concepts/ctf-challenge-dev-research.md]
confidence: high
---

# CTF Writeup Ingestion Workflow

> 공개 CTF writeup을 조사해서 **분류 → 추출 → 재사용 개념화 → 위키 저장**까지 이어가는 자기학습 파이프라인입니다.
> 목적은 단순 요약이 아니라, 새 writeup을 읽을수록 기존 지식망이 커지게 만드는 것입니다.

## 참고 URL
- [Reference](queries/picoctf-web-survey.md)
- [Reference](concepts/web-ctf-writeup-topic-map.md)
- [Reference](concepts/ctf-challenge-dev-research.md)

## 1. 왜 이 방식이 필요한가
CTF writeup을 많이 읽어도 그냥 문장만 쌓이면 재사용성이 낮습니다. 따라서 다음 순서를 고정합니다.

1. **문제의 실제 분류를 확정**합니다.
2. **입력점과 primitive**를 뽑습니다.
3. **여러 writeup을 비교**해서 공통 메커니즘을 찾습니다.
4. **개별 문제 페이지**와 **재사용 가능한 concept page**를 분리합니다.
5. **index.md / log.md**까지 갱신해서 다음 탐색 비용을 줄입니다.

## 2. 입력 소스 우선순위
### 1차 소스
- GitHub 공개 writeup 저장소
- CTFtime writeup
- 개인 블로그 writeup
- 대회 참가자 공개 노트

### 2차 소스
- 문제 원본 소스
- challenge docker / archive
- 공식 대회 안내문
- 벤더 문서나 기술 사양

### 선택 기준
- 같은 문제의 writeup이 **2개 이상** 있으면 비교합니다.
- 문제명이 비슷해도 **실제 공격면**이 다르면 별도 분류합니다.
- `-final-writeup`가 이미 있으면 새 문서를 만들기보다 기존 문서를 보강합니다.

## 3. 분류 규칙
문제를 볼 때는 제목보다 다음을 먼저 봅니다.

| 질문 | 확인할 것 |
|---|---|
| 입력점은 무엇인가요? | URL, 쿠키, 파일, 헤더, 바이너리, PRNG seed |
| primitive는 무엇인가요? | leak, overwrite, inject, bypass, tamper |
| 방어 장치는 무엇인가요? | PIE, canary, CSP, allowlist, auth, sandbox |
| 비의도 풀이가 쉬운가요? | 직접 노출, 디버그 정보, 과도한 권한 |
| 재사용 가능한가요? | 다른 문제에도 적용되는 메커니즘인가요? |

## 4. 위키 저장 기준
### query page
- 문제별 풀이를 짧게 정리합니다.
- 재현 절차와 관찰 포인트를 남깁니다.
- 한 문제에 대해 가장 먼저 저장하는 단위입니다.

### concept page
- 반복되는 메커니즘만 분리합니다.
- 예: [[ssrf-ctf-patterns]], [[sqlite-sqli-filter-bypass-ctf-patterns]], [[format-string-ctf-patterns]]
- 여러 문제에서 재사용할 수 있어야 합니다.

### survey page
- 연도별 / 대회별 / 트랙별 묶음을 만듭니다.
- “무엇을 먼저 읽어야 하는지” 안내하는 상위 허브 역할을 합니다.

## 5. 저장 플로우
1. 공개 writeup 후보를 모읍니다.
2. 기존 위키에 같은 문제/같은 패턴이 있는지 검색합니다.
3. 분류가 애매하면 survey와 topic map을 먼저 확인합니다.
4. 새로 필요한 경우에만 query 또는 concept를 생성합니다.
5. 관련 허브에 역링크를 추가합니다.
6. `index.md`와 `log.md`를 갱신합니다.
7. `wiki lint`로 검증합니다.

## 6. 자동화 포인트
이 파이프라인은 수동으로도 가능하지만, 다음은 자동화하기 좋습니다.

- RSS / GitHub search / CTFtime 검색 결과 수집
- 문제명 중복 제거
- 연도 / 카테고리별 후보 분류
- 기존 위키 링크 매칭
- 새 문서 초안 생성
- index/log 업데이트

## 7. 자기학습 관점에서의 이득
이 방식으로 저장하면 다음이 가능합니다.

- 같은 패턴을 다른 문제에 재사용합니다.
- 문제 분류 정확도가 올라갑니다.
- 비의도 풀이를 더 빨리 찾습니다.
- 힌트 설계와 난이도 조절이 쉬워집니다.
- 위키가 커질수록 검색 비용이 줄어듭니다.

## 8. 운영자용 추천 루틴
- 매주 새 writeup 후보를 3~5개 모읍니다.
- 각 후보를 `query` / `concept` / `survey`로 분류합니다.
- 공통 primitive가 2회 이상 보이면 concept page를 만듭니다.
- 새로 추가한 페이지는 반드시 `index.md` / `log.md`에 반영합니다.

## 9. 연결 문서
- [[web-ctf-writeup-curation]]
- [[web-ctf-writeup-topic-map]]
- [[ctf-challenge-dev-research]]
- [[picoctf-web-survey]]
- [[ssrf-ctf-patterns]]

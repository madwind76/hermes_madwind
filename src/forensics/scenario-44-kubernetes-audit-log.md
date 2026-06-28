---
title: 쿠버네티스 감사 로그 침투 추적 (Kubernetes API Audit Log Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, cloud, kubernetes, audit-log, api-server, jq]
confidence: high
---

# 쿠버네티스 감사 로그 침투 추적 (Kubernetes API Audit Log Analysis)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 클라우드/컨테이너 감사 흔적 추적 (Kubernetes API Audit Log 분석)

## 1. 배경 시나리오
사내 클라우드 인프라의 쿠버네티스(Kubernetes) 클러스터에서 특정 서비스 어카운트(Service Account)의 토큰이 유출되어, 비인가자가 클러스터 내부에 저장되어 있던 데이터베이스 패스워드 및 토큰 정보(`Secrets` 리소스)를 무단 조회(get/list)해 간 흔적이 식별되었습니다. 쿠버네티스 제어 평면(Control Plane)의 API 서버에 기록된 보안 감사 로그 파일인 `k8s_audit.json` 파일이 제공됩니다. 이 감사 로그를 조사하여 **토큰 유출로 비인가 접근된 기밀(Secret) 리소스명 내에 포함되어 있는 플래그 문자열**을 획득하십시오.

## 2. 제공 파일
* `k8s_audit.json` (쿠버네티스 API 서버 감사 로그 파일 - JSON Lines 포맷)

## 3. 문제 목표
클라우드 네이티브 환경의 핵심 아티팩트인 Kubernetes API 감사 로그 명세 구조(Event structure, requestURI, verb, user, objectRef)를 이해하고, JSON 파싱 도구(`jq` 또는 파이썬 스크립트) 및 터미널 명령어 조합을 활용해 공격 타깃이 된 특정 기밀 리소스명을 발굴합니다.

## 4. 의도한 풀이 흐름
1. **감사 로그 형식 진단**:
   * 제공된 `k8s_audit.json` 파일이 줄바꿈 단위로 완전한 JSON 구조체가 나열된 JSON Lines 포맷임을 인지합니다.
2. **Secrets 리소스 쿼리 행 필터링**:
   * 공격자가 탈취를 시도한 리소스 종류는 쿠버네티스의 `secrets`에 해당하며, 조회 행위이므로 API 동사(`verb`)는 `get` 또는 `list` 혹은 `watch` 일 것입니다.
   * `jq` 명령어를 가동하여 secrets 객체를 대상으로 조회한 이벤트 행들을 걸러냅니다:
     ```bash
     cat k8s_audit.json | jq 'select(.objectRef.resource=="secrets" and (.verb=="get" or .verb=="list"))'
     ```
   * 혹은 간단하게 `grep` 명령을 사용하여 빠른 패턴 검색을 수행합니다:
     ```bash
     grep '"resource":"secrets"' k8s_audit.json | grep '"verb":"get"'
     ```
3. **타깃 리소스명 식별**:
   * 필터링 출력 결과 내의 **objectRef** 노드 하부의 **name** 필드를 살펴봅니다.
   * 정상적인 토큰 조회 외에 아래와 같이 비정상적인 도메인 이름의 시크릿 오브젝트를 요청해 획득(Response Status: 200 OK)한 공격 이벤트를 발견합니다:
     ```json
     {
       "level": "RequestResponse",
       "verb": "get",
       "user": {"username": "system:serviceaccount:default:compromised-sa"},
       "sourceIPs": ["198.51.100.82"],
       "userAgent": "kubectl/v1.28.2 (linux/amd64)",
       "objectRef": {
         "resource": "secrets",
         "namespace": "default",
         "name": "picoctf-k8s-aud1t-log-tr4c3s-cl0ud"
       },
       "responseStatus": {"metadata": {}, "code": 200}
     }
     ```
4. **플래그 복구**:
   * 획득한 시크릿 명칭(`picoctf-k8s-aud1t-log-tr4c3s-cl0ud`)을 규격 플래그 포맷에 맞게 대시(-)를 언더스코어(_)로 변형하여 최종 플래그를 정립합니다:
     `picoCTF{k8s_aud1t_log_tr4c3s_cl0ud}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{k8s_aud1t_log_tr4c3s_cl0ud}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 로컬 쿠버네티스 테스트 베드(Minikube, Kind 등)에서 기밀 시크릿을 생성합니다:
     `kubectl create secret generic picoctf-k8s-aud1t-log-tr4c3s-cl0ud --from-literal=key=value`
  2. API 감사 정책 활성화를 위해 `/etc/kubernetes/manifests/kube-apiserver.yaml` 설정을 열어 `--audit-policy-file` 및 `--audit-log-path` 옵션을 부여합니다.
  3. 탈취된 모의 서비스 계정 토큰을 활용해 해당 시크릿을 API 호출합니다:
     `kubectl get secret picoctf-k8s-aud1t-log-tr4c3s-cl0ud`
  4. 감사 기록에 적재된 `/var/log/kubernetes/audit.log` 내에서 방금 요청한 JSON 로그 엔트리를 추출하고, 정상 쿠버네티스 백그라운드 서비스 계정 동작 로그 수십 줄을 덧붙여 `k8s_audit.json` 파일로 저장 및 배포합니다.
* **출제 포인트**: 
  * 클라우드 네이티브 아키텍처 및 쿠버네티스 보안 위협 추적 시, 시스템 셸/디스크 포렌식의 한계를 넘어 API 서비스 레벨의 원격 트래픽 흔적(Kubernetes Audit)을 규명하는 역량을 평가합니다.

## 7. 트러블슈팅 및 힌트
* **Q. k8s_audit.json 파일을 일반 텍스트 편집기나 메모장으로 열었더니 긴 한 줄로 나와서 가독이 불가능합니다.**
  * A. JSON Lines 포맷은 엔터(\n) 기호로 각 행의 JSON 데이터를 구별합니다. 메모장 대신 `jq` 유틸리티를 사용하여 `jq .` 와 같이 구문 정형화(Pretty print) 옵션을 주거나, VS Code 등의 편집기를 실행하여 포맷 정렬을 가하면 정상 가독할 수 있습니다.
* **Q. level 속성의 Metadata, Request, RequestResponse는 각각 어떤 차이가 있나요?**
  * A. 쿠버네티스 감사 로그의 기록 등급(Level) 설정에 따라 차이가 납니다:
    * `Metadata`: 요청한 사용자, IP, 리소스 종류 등 헤더 정보만 기록 (가장 가벼움)
    * `Request`: 메타데이터에 더해 클라이언트가 보낸 바디 데이터(Payload)까지 기록
    * `RequestResponse`: 요청 메타데이터/바디에 더해 API 서버가 되돌려준 결과 데이터(Response Body)까지 모두 수록하므로 분석 정보가 가장 상세히 보존됩니다.

## 8. 학습 포인트
* **쿠버네티스 감사 정책(K8s Audit Policy)**: 컨테이너 오케스트레이션 제어 평면의 API 게이트웨이 보안 모니터링 감사 작동 원리를 학습합니다.
* **JSON 데이터 정형 필터링**: 대량의 정적 정형 JSON 파일군에서 원하는 다차원 노드 매핑 조건(objectRef, verb 등)을 적용하여 고속 색인해 내는 `jq` 필터 식을 학습합니다.

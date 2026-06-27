---
title: 클라우드 활동 로그 (CloudTrail 시뮬레이션)
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, education, forensics, challenge-development, lab, cloud, aws, cloudtrail, iam, dfir]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html]
confidence: medium
---

# 클라우드 활동 로그 (CloudTrail 시뮬레이션)

> 난이도: 초중급
> 소요 시간: 25~35분

## 배경
사내 AWS 계정에서 평소와 다른 S3 버킷 접근이 감지되었습니다. 로그는 CloudTrail JSON 형식으로 1시간치만 남아 있고, 그 안에서 **IAM 자격증명 남용 의심 이벤트**를 찾아야 합니다. 참가자는 IAM 정책의 의미를 이해하고 JSON 이벤트의 상관관계를 분석해 **공격자 접근 키 ID, 시각, 대상 버킷** 트리오를 복원합니다.

## picoCTF·기존 시나리오 대비 차별점
- picoCTF 2024/2025 포렌식 트랙은 **클라우드 포렌식** 문제를 포함하지 않습니다.
- 기존 5개 시나리오도 모두 온프레미스 아티팩트 중심.
- 본 시나리오는 AWS CloudTrail JSON 로그를 직접 다뤄 **클라우드 IR**을 처음 접하는 참가자도 따라올 수 있게 단순화합니다.

## 제공 파일
- `cloudtrail-2026-05-12.json` — 1시간치 이벤트 (~120건)
- `iam-policy-attached.json` — 시점에 유효했던 IAM 정책 (관리자가 별도 보관 중)
- `bucket-inventory.md` — 회사 소유 S3 버킷 목록과 각 버킷의 접근 허용 범위
- `case-context.md` — 사건 개요 + 의심 시각(UTC 기준 03:40~04:05)

## 문제 목표
의심 시각대에 발생한 비정상 이벤트를 찾아내고, **공격자가 사용한 액세스 키 ID, 시각, 버킷 이름**을 플래그로 제출합니다.

## 의도한 풀이 흐름
1. `cloudtrail-2026-05-12.json`을 열어 각 이벤트의 `eventTime`, `eventName`, `sourceIPAddress`, `userIdentity`, `awsRegion`을 훑습니다.
2. `case-context.md`의 의심 시각대(`eventTime` 범위)로 후보 이벤트를 좁힙니다:
   ```bash
   jq '.Records[] | select(.eventTime >= "2026-05-12T03:40:00Z" and .eventTime <= "2026-05-12T04:05:00Z")' cloudtrail-2026-05-12.json
   ```
3. 후보 이벤트 중 `eventName`이 `GetObject`, `ListBucket`, `AssumeRole`, `CreateAccessKey`인 건을 분리합니다.
4. `userIdentity.accessKeyId`가 평소 사용 패턴(`iam-policy-attached.json`의 `Principal`/조건)과 다른 키인지 확인합니다.
5. `sourceIPAddress`가 회사 IP 대역(`iam-policy-attached.json`의 `aws:SourceIp` 조건)에 해당하지 않으면 의심도가 올라갑니다.
6. `bucket-inventory.md`를 보고 `eventSource`가 `s3.amazonaws.com`이며 `requestParameters.bucketName`이 **민감 데이터 버킷**과 일치하는지 확인합니다.
7. 최종 후보 1건으로 **accessKeyId + 시각(UTC HHMM) + 버킷명**을 플래그로 조립합니다.

## 정답 규칙
- `picoCTF{<accessKeyId>_<HHMM>_<bucketName>}`
- 예시: `picoCTF{AKIAIOSFODNN7EXAMPLE_0347_employee-secrets}`
- 시각은 UTC HHMM

## 출제자 노트
- 120건 중 의심 이벤트는 3~5건, 실제 공격 이벤트는 1건입니다.
- 정상 이벤트에 `AssumeRole`, `GetObject`가 섞여 있어 단순 필터링만으로는 답을 못 찾게 만듭니다.
- `aws:SourceIp` 조건을 만족하지 않는 이벤트가 **다른 액세스 키**로 로그인한 사례로 등장합니다.
- `bucket-inventory.md`에 **공개 의도된 버킷**(예: `company-public-assets`)과 **민감 버킷**(`employee-secrets`)을 분리해 표기하면, 참가자가 비교 판단할 수 있습니다.

## 트러블슈팅
| 증상 | 원인 | 해결 |
|---|---|---|
| `jq` 결과가 너무 많음 | 시각 범위 미설정 | `select` 조건을 UTC 기준으로 좁히기 |
| `userIdentity.type`이 `IAMUser`인지 `Root`인지 헷갈림 | 정책 해석 부족 | `iam-policy-attached.json`의 `Principal` 섹션 참고 |
| `aws:SourceIp` 조건 누락 | 정책에 조건 미기재 | 정책의 `Condition` 블록을 함께 표시 |
| 버킷 이름 후보가 여러 개 | 공개 버킷까지 후보로 잡힘 | `bucket-inventory.md`의 데이터 분류(공개/내부/민감) 확인 |

## 학습 포인트
- CloudTrail JSON의 **구조**와 각 필드의 의미를 이해합니다.
- `eventTime`, `userIdentity`, `requestParameters` 등 **다중 채널을 교차 검증**하는 IR 감각을 기릅니다.
- IAM 정책의 `Principal`, `Action`, `Resource`, `Condition` 4요소가 **포렌식 판단 기준**으로 어떻게 쓰이는지 학습합니다.
- 온프레미스 포렌식에서 클라우드 포렌식으로 시야를 확장하는 진입점 역할을 합니다.

## 관련 페이지
- [[forensics-writeup-family-hub]] — 포렌식 패턴 허브
- [[forensics-network-hub]] — 네트워크/로그 트래픽 허브
- [[forensics-scenario-01-messenger-leak-log]] — Windows 이벤트 로그 (온프레미스 입문, 대비 시나리오)

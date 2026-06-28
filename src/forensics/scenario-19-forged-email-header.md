---
title: 조작된 메일 헤더 (Forged Email Header)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, email, eml, email-header, spf, dkim]
confidence: high
---

# 조작된 메일 헤더 (Forged Email Header)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 피싱 메일 추적 및 이메일 헤더 분석 (RFC 5322 이메일 명세 연계)

## 1. 배경 시나리오
사내 임직원을 타깃으로 보안 담당자를 사칭한 피싱 이메일이 인입되었습니다. 보낸 사람의 겉보기 이메일 주소는 `security@google.com`으로 표기되어 있어 사용자가 속아 비밀번호를 탈취당했습니다. 보안 분석 팀은 피해자가 받은 피싱 이메일의 원시 데이터(Raw Source)를 추출한 `phishing_mail.eml` 파일을 확보했습니다. 이메일 헤더를 정밀 분석하여 **실제로 이 피싱 메일을 최초 발송한 서버의 IP 주소**와 **이메일 발신지 검증(SPF) 검사 결과**를 찾아 해킹의 실체를 밝혀야 합니다.

## 2. 제공 파일
* `phishing_mail.eml` (텍스트 포맷의 피싱 메일 소스 코드 원본 파일)

## 3. 문제 목표
이메일 헤더 명세(RFC 5322) 구조를 이해하고, 메일 전송 프로세스에서 MTA(Mail Transfer Agent)가 순차적으로 추가하는 `Received` 필드의 추적 방향(탑다운이 아닌 바텀업 분석)을 체득합니다. 또한, 발신 IP 차단 방어를 위한 이메일 보안 기술 규격인 **SPF(Sender Policy Framework)**의 분석 결과를 획득하여 플래그를 생성합니다.

## 4. 의도한 풀이 흐름
1. **이메일 원본 열기**:
   * 제공된 `phishing_mail.eml` 파일을 일반 텍스트 편집기(vi, notepad 등)나 이메일 리더로 엽니다.
2. **이메일 전송 경로 추적 (Received 헤더 분석)**:
   * 이메일 헤더에는 하나 이상의 `Received:` 헤더가 존재합니다.
   * 메일이 전송 과정을 거칠 때마다 수신 서버가 가장 상단에 `Received:` 필드를 추가하므로, **최초 발신지와 가장 가까운 서버 정보는 헤더 목록 중 가장 하단(Bottom-most)에 위치한 Received 필드**에 들어 있습니다.
   * 가장 아래의 `Received:` 필드를 확인합니다:
     ```text
     Received: from fake-smtp.attacker-server.net (unknown [198.51.100.75])
               by mx.google.com with ESMTPS ...
     ```
   * 최초 발송지의 실제 IP 주소인 `198.51.100.75`를 확보합니다.
3. **발신지 도메인 검증 결과(SPF) 확인**:
   * 헤더 필드 중 수신 서버가 수행한 도메인 보안 인증 결과를 기록하는 `Authentication-Results:` 필드를 검색합니다.
   * 아래와 같이 Google 메일 서버가 `google.com` 도메인과 발신 IP `198.51.100.75`를 대조하여 판정한 SPF 검사 결과를 찾아냅니다:
     ```text
     Authentication-Results: mx.google.com;
            spf=fail (google.com: domain of security@google.com does not designate 198.51.100.75 as permitted sender) ...
     ```
   * SPF 판정 결과가 `fail` 임을 식별합니다. (기타 판정값 예: `pass`, `softfail`, `neutral`, `none`)
4. **플래그 결합**:
   * 알아낸 **실제 발신 IP**와 **SPF 판정값**을 소문자로 매칭하여 플래그를 조합합니다:
     `picoCTF{198.51.100.75_spf-fail}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<actual_ip>_<spf_result>}`
* **예시**: `picoCTF{198.51.100.75_spf-fail}` (SPF 결과가 softfail인 경우 `spf-softfail` 형식으로 결합)

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 텍스트 에디터를 사용하여 표준 이메일 원문 파일(`.eml`)을 수동으로 작성하거나, 모의 침투 도구를 활용해 발송한 메일 소스를 덤프합니다.
  2. 헤더 블록에 다음 필드를 필히 구조화해 둡니다:
     * `From: Google Security <security@google.com>` (가짜 표시)
     * 다중 `Received:` 헤더를 배치하여 하단으로 내려갈수록 공격자의 메일 서버 릴레이 경로(IP: `198.51.100.75`)가 명시되도록 구성합니다.
     * `Authentication-Results:` 필드에 해당 IP가 `google.com` 서버가 공식 등록한 SPF 레코드 범위 외이므로 `spf=fail` 판정을 받았음을 텍스트로 기록합니다.
  3. 피싱 메일 내용 본문에는 악성 피싱 피드백 페이지 링크 등을 텍스트로 추가하여 현실성을 높인 뒤 `phishing_mail.eml`로 저장하여 배포합니다.
* **출제 포인트**: 
  * 일상적으로 인입되는 이메일 사칭 공격의 원리를 파악하고, 수신 경로 조사의 바텀업 분석 원칙과 SPF/DKIM 등의 메일 인증 메커니즘을 이메일 헤더 덤프를 통해 직접 점검해 보는 기회를 갖게 합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 이메일 헤더가 너무 복잡해서 한눈에 읽기 어렵습니다.**
  * A. 웹 서비스인 **MXToolbox Email Header Analyzer** 또는 **Messageheader (by Google)** 등의 메일 헤더 분석 도구에 EML의 헤더 부분만 복사 및 붙여넣기(Paste)하면, 수신 서버들의 라우팅 타임라인과 SPF/DKIM 점검 결과를 테이블 형태로 아주 깔끔하게 번역하여 보여줍니다.
* **Q. From 헤더와 Return-Path 헤더가 다릅니다. 발신 IP는 무엇을 기준으로 봐야 하나요?**
  * A. `From` 및 `Return-Path` 헤더 역시 이메일 클라이언트 수준에서 임의 조작이 가능한 문자열 영역에 불과합니다. 메일 전송 인프라(SMTP) 단에서 거쳐온 전송 경로는 오직 중첩 기록된 `Received:` 헤더와 인증 결과 수신 IP만 신뢰할 수 있습니다.

## 8. 학습 포인트
* **이메일 헤더 파싱**: 메일 시스템 간의 전송 릴레이 기록이 기록되는 `Received` 필드의 고유 특성과 데이터 흐름 방향성 분석 기법을 터득합니다.
* **발신지 도메인 인증**: 스팸 및 피싱 방어를 위한 보안 기술 규격인 SPF의 정의와 동작 원리를 이해하고 실제 메일 분석에 대조 적용하는 능력을 배양합니다.

---
title: DNS rebinding — CTF patterns
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [ctf, web, dns, rebinding, localhost]
sources: [https://blog.nella17.tw/p/hitcon-ctf-2021-writeups/, https://ctftime.org/task/18312, https://ctftime.org/writeup/31677, https://github.com/orangetw/My-CTF-Web-Challenges]
confidence: medium
---

# DNS Rebinding

## 정의
DNS rebinding은 같은 도메인이 시간이 지나며 다른 IP로 해석되도록 만들어 브라우저의 동일 출처 판단을 흔드는 기법입니다.

## 왜 중요한가
로컬호스트나 내부망에 직접 접근할 수 없는 웹 챌린지에서 우회 통로가 됩니다.

## 관찰 포인트
- Host 헤더 검증 여부
- 로컬 서비스 경로(`/flag`, `/admin`, `/debug`)
- 브라우저가 동일 출처로 보는지 여부
- iframe, popup, text fragment와의 조합

## 공격 패턴
1. 먼저 공격자 도메인으로 연결시킵니다.
2. 이후 DNS 응답을 내부 주소로 바꿉니다.
3. 브라우저가 같은 출처라고 믿는 상태에서 localhost에 접근합니다.
4. 민감한 페이지나 플래그 엔드포인트를 읽습니다.

## 방어 포인트
- Host 헤더를 엄격히 검증합니다.
- localhost / 0.0.0.0 바인딩 경로를 분리합니다.
- 내부용 서비스에 브라우저 기반 접근을 허용하지 않습니다.

## 관련 예시
- [[vulpixelize]]

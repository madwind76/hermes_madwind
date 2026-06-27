---
title: XSSI / File Exfiltration
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [ctf, web, xssi, file, exfiltration]
sources: [https://gist.github.com/terjanq/4cb40653760c1ba8c33ee06be098d508, https://ctftime.org/event/2718/tasks/, https://www.mozilla.org/en-US/security/advisories/mfsa2025-42/#CVE-2025-5263]
confidence: medium
---

# XSSI / File Exfiltration

## 참고 URL
- [terjanq/4cb40653760c1ba8c33ee06be098d508](https://gist.github.com/terjanq/4cb40653760c1ba8c33ee06be098d508)
- [CTFtime writeup](https://ctftime.org/event/2718/tasks/)
- [www.mozilla.org](https://www.mozilla.org/en-US/security/advisories/mfsa2025-42/#CVE-2025-5263)

## 정의
XSSI는 외부 스크립트 포함을 악용해 내부 데이터가 예상치 못한 형태로 노출되는 문제입니다.

## 왜 중요한가
Puppeteer, file://, error handler가 결합되면 브라우저 보안 경계가 흔들릴 수 있습니다.

## 관찰 포인트
- `file://` 로드 가능 여부
- 콘솔/에러 메시지의 원문 노출 여부
- IndexedDB / 로컬 저장소 경로
- charset / parser side effect

## 공격 패턴
1. 파일 또는 스크립트가 포함되는 경로를 찾습니다.
2. 에러 메시지나 파서 동작으로 데이터를 새어 나오게 합니다.
3. 브라우저 저장소를 이용해 페이로드를 재사용 가능한 형태로 저장합니다.
4. 관리자 봇이 그 경로를 방문하도록 유도합니다.

## 방어 포인트
- file:// 접근 권한과 same-origin 정책을 보수적으로 유지합니다.
- 에러 메시지에 민감한 데이터를 넣지 않습니다.
- 봇/자동화 브라우저의 보안 설정을 확인합니다.

## 관련 예시
- [[sourceless]]

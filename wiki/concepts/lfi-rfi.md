---
title: LFI/RFI (Local/Remote File Inclusion)
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [security, lfi, rfi, file-inclusion, path-traversal]
sources: [https://owasp.org/www-community/attacks/Path_Traversal]
confidence: high
---

# LFI/RFI (Local/Remote File Inclusion)

> 이 페이지는 LFI/RFI 전체의 **인덱스**입니다.
> 상세 설명은 [[lfi-rfi-core]]와 [[lfi-rfi-defense]]를 참고합니다.

## 참고 URL
- [owasp.org](https://owasp.org/www-community/attacks/Path_Traversal)

## 핵심 페이지
- [[lfi-rfi-core]] — 공격 원리와 확장
- [[lfi-rfi-defense]] — 방어 및 안전한 구현

## 빠른 개요
- LFI는 로컬 파일을 포함하는 기능을 악용합니다.
- RFI는 원격 위치의 콘텐츠를 포함하도록 유도합니다.
- 파일 포함 취약점은 종종 **경로 순회**와 결합해 **RCE**로 확장됩니다.

## 관련 위키 링크
- [[lfi-rfi-core]] — 핵심 메커니즘
- [[lfi-rfi-defense]] — 방어
- [[path-traversal]] — 경로 순회
- [[rce]] — 원격 코드 실행

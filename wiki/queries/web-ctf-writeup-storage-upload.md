---
title: Web CTF Writeup — 파일 업로드/스토리지/클라우드
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, research, writeup, file-upload, storage, cloud]
sources: [https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/, https://blog.arkark.dev/2023/12/28/seccon-finals, raw/articles/20260613_web-ctf-writeup-curated.md]
confidence: high
---

# Web CTF Writeup — 파일 업로드/스토리지/클라우드

> 업로드 검증, 객체 스토리지 권한, multipart 처리, 후속 처리 파이프라인을 다루는 분류입니다.

## 참고 URL
- [blog.hokyun.dev](https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/)
- [blog.arkark.dev](https://blog.arkark.dev/2023/12/28/seccon-finals)
- [raw/articles/20260613_web-ctf-writeup-curated.md](raw/articles/20260613_web-ctf-writeup-curated.md)


## 1. 핵심 요약
- 이 분류는 **업로드 자체**보다 **업로드 후 처리**에서 터지는 문제를 모읍니다.
- S3 버전 노출, multipart filename 조작, 후속 이미지/아카이브 처리 취약점이 대표적입니다.
- `file-upload`, `idor`, `ssrf`와 연결되기도 합니다.

연결 개념: [[file-upload]], [[idor]], [[ssrf]], [[broken-access-control]]

## 2. 대표 writeup

| 문제 | 출처 | 핵심 아이디어 |
|------|------|---------------|
| `bucketwars` | CSAW CTF 2024 Quals | S3 versioning 노출 + 숨은 정보 회수 |
| `charlies angels` | CSAW CTF 2024 Quals | multipart 파싱 결함 + 내부 백업 서버 악용 |
| `It is my Birthday` | picoCTF 2021 | MD5 collision으로 PDF 업로드 검증 우회 |
| `LemonMD` | SECCON 2023 Finals | islands architecture와 클라이언트/서버 분리 흐름 |

## 3. 자주 보이는 패턴
1. 업로드 파일명이 저장 경로와 결합됨
2. 버전 관리 객체가 삭제된 것처럼 보여도 남아 있음
3. 이미지/문서 후처리 도구가 별도 취약점을 포함함
4. 백업/미리보기/변환 서버가 내부에서 열려 있음
5. 업로드 결과가 공개 버킷이나 CDN으로 노출됨

## 4. 읽을 때 확인할 것
- 업로드 후 파일이 어떤 파이프라인을 타는지
- 확장자, MIME, 매직 바이트 검증이 일치하는지
- 버전/삭제/복구 객체가 공개되는지
- 업로드와 다운로드 경로의 권한이 일치하는지

## 5. 방어 관점
- 저장소 권한과 공개 읽기 범위를 분리합니다.
- 업로드 파일은 무조건 재인코딩하거나 안전한 뷰어로만 처리합니다.
- multipart 파서는 검증 전용으로만 쓰지 않습니다.
- 내부 백업/변환 서버는 외부에서 직접 접근되지 않게 합니다.

## 6. 추천 다음 읽기
- [[file-upload]]
- [[idor]]
- [[ssrf]]
- [[it-is-my-birthday-final-writeup]]
- [[trickster-final-writeup]]
- [[web-ctf-master-checklist]]

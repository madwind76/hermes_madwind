---
title: File Upload CTF Patterns
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [ctf, web, file-upload, research]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Trickster.md, https://medium.com/@niceselol/picoctf-2024-trickster-af90f7476e18, https://dev.to/yowise/trickster-picoctf-2024-1j5j, https://brandon-t-elliott.github.io/trickster]
confidence: medium
---

# File Upload CTF Patterns

## 정의
Web CTF에서 File Upload는 **업로드된 파일의 검증, 저장, 접근, 실행 흐름 중 약점을 찾는 문제 유형**입니다.

## CTF에서 자주 보이는 신호
- 프로필 이미지 업로드
- 첨부파일 업로드
- MIME/확장자 검사
- 업로드 후 미리보기 또는 다운로드 URL
- `robots.txt` / `instructions.txt` 같은 숨은 업로드 규칙 안내

## 실험 순서
1. 확장자 제한 확인
2. MIME 및 매직바이트 확인
3. 더블 확장자 / polyglot 가능성 확인
4. 저장 경로 확인
5. 실행 가능 여부 확인
6. 경로 순회 또는 웹셸 전환 가능성 확인

## 관찰 포인트
- 업로드 성공 메시지
- 저장 경로 예측 가능성
- 변환/재인코딩 여부
- 정적 파일 서빙 여부
- 파일명 substring 검사 여부 (`.png.php` 같은 우회 가능성)
- magic bytes만 확인하는지 여부

## 방어 포인트
- 서버측 매직바이트 검사
- 확장자 화이트리스트
- 실행 권한 분리
- 랜덤 파일명 사용
- 업로드 파일 웹 실행 금지
- 업로드 전 재인코딩 또는 안전한 뷰어 사용

## 연결 개념
- [[file-upload]]
- [[file-upload-core]]
- [[file-upload-defense]]
- [[path-traversal]]
- [[rce]]
- [[trickster-final-writeup]]
- [[n0s4n1ty-1-final-writeup]]

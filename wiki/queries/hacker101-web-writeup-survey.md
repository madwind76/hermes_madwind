---
title: Hacker101 CTF web writeup survey
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, survey, writeup, file-upload, path-traversal, sql-injection, csrf, idor, xss, tampering]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Photo%20Gallery/README.md, https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Tempimage/README.md, https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Ticketastic%3A%20Live%20Instance/README.md, https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md]
confidence: high
---

# Hacker101 CTF web writeup survey

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Photo%20Gallery/README.md)
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Tempimage/README.md)
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Ticketastic%3A%20Live%20Instance/README.md)
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md)


## 1. 목적
Hacker101 CTF에서 공개된 웹 writeup 4건을 비교해, 반복되는 공격면과 재사용 가능한 primitive를 정리한 survey입니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Photo Gallery | SQL injection | command injection | DB 값을 쉘 명령에 흘려보내 RCE로 이어집니다. |
| Tempimage | path traversal | unrestricted upload | 업로드 파일명을 조작해 경로를 탈출하고, PNG에 PHP를 섞어 RCE로 확장합니다. |
| Ticketastic: Live Instance | CSRF | SQL injection | 티켓 본문에 HTML이 그대로 렌더링되고, 티켓 조회 파라미터도 취약합니다. |
| Petshop Pro | hidden field tampering | IDOR / stored XSS | 가격·ID·상품명 조작이 서로 다른 취약점으로 이어집니다. |

## 3. 공통 관찰
1. **클라이언트가 보낸 값을 서버가 믿는 지점**이 여러 군데 존재합니다.
2. 파일 업로드, 식별자, hidden field, ticket body처럼 겉보기 단순 입력이 실제 공격면입니다.
3. 하나의 취약점으로 끝나지 않고, DB → 파일 → 쉘, HTML → CSRF, hidden field → IDOR처럼 체인이 이어집니다.

## 4. 관련 개념
- [[web-ctf-writeup-family-hub]]
- [[file-upload-ctf-patterns]]
- [[path-traversal-ctf-patterns]]
- [[sql-injection]]
- [[csrf]]
- [[idor-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]
- [[xss]]
- [[web-ctf-writeup-curation]]

## 5. 다음 읽을 거리
- [[photo-gallery-final-writeup]]
- [[tempimage-final-writeup]]
- [[ticketastic-live-instance-final-writeup]]
- [[petshop-pro-final-writeup]]

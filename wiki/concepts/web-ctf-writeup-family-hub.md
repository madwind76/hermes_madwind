---
title: Web CTF writeup family hub
created: 2026-06-19
updated: 2026-06-21
type: concept
tags: [ctf, web, research, writeup, survey, client-side, source-analysis, ssrf, auth, session]
sources: [https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/postbook/README.md, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md, https://github.com/ilhambagas/Bithug, https://github.com/jdonsec/allthingsssrf]
confidence: medium
---

# Web CTF writeup family hub

## 참고 URL
- [Original source](https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/postbook/README.md)
- [Original source](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Web_Exploitation/Unminify.md)
- [ilhambagas/Bithug](https://github.com/ilhambagas/Bithug)
- [jdonsec/allthingsssrf](https://github.com/jdonsec/allthingsssrf)

## 1. 목적
이 페이지는 이번 자동 수집에서 만든 survey들과 그에 대응하는 개념 허브를 한곳에 묶는 상위 진입점입니다.

## 2. 이번 묶음
- [[cookie-tampering-writeup-survey]] → [[cookie-client-storage-ctf-patterns]]
- [[source-inspection-hidden-file-writeup-survey]] → [[source-inspection-minification-ctf-patterns]], [[web-inspector-ctf-patterns]], [[hidden-directory-discovery-ctf-patterns]], [[web-recon-hidden-file-discovery-ctf-hub]]
- [[web-ctf-writeup-client-side]] → [[web-inspector-ctf-patterns]], [[source-inspection-minification-ctf-patterns]], [[csp-bypass-ctf-patterns]]
- [[ssrf-internal-service-writeup-survey]] → [[ssrf-ctf-patterns]]
- [[hacker101-web-writeup-survey]] → [[file-upload-ctf-patterns]], [[sql-injection]], [[csrf]], [[idor-ctf-patterns]]
- [[graphql-api-writeup-survey]] → [[api-security-defense]], [[broken-access-control-defense]]
- [[jwt-auth-bypass-writeup-survey]] → [[jwt-secret-exposure-ctf-patterns]], [[broken-auth]]
- [[file-upload-path-traversal-writeup-survey]] → [[file-upload-ctf-patterns]], [[path-traversal-ctf-patterns]]
- [[sql-injection-writeup-survey]] → [[sql-injection]], [[sqlite-sqli-filter-bypass-ctf-patterns]], [[sqlite-union-based-sqli-ctf-patterns]]
- [[idor-writeup-survey]] → [[idor-ctf-patterns]], [[broken-access-control-defense]]
- [[xss-writeup-survey]] → [[xss]], [[csp-bypass-ctf-patterns]], [[web-ctf-writeup-client-side]]
- [[command-injection-writeup-survey]] → [[command-injection]], [[command-injection-defense]], [[redis-ssrf-command-injection-ctf-patterns]]
- [[ssti-writeup-survey]] → [[ssti]], [[ssti-ctf-patterns]]
- [[deserialization-writeup-survey]] → [[web-ctf-writeup-auth-session]], [[php-object-injection-ctf-patterns]]
- [[lfi-path-traversal-writeup-survey]] → [[lfi-rfi]], [[lfi-rfi-core]]
- [[csrf-writeup-survey]] → [[csrf]], [[web-ctf-writeup-client-side]]
- [[nosql-injection-writeup-survey]] → [[nosql-injection-ctf-patterns]]
- [[race-condition-writeup-survey]] → [[race-condition-ctf-patterns]]
- [[xxe-writeup-survey]] → [[xxe]], [[xxe-core]]
- [[websocket-writeup-survey]] → [[websocket-message-tampering-ctf-patterns]], [[websocket]]
- [[open-redirect-writeup-survey]] → [[ssrf-ctf-patterns]], [[parameter-tampering-ctf-patterns]], [[broken-auth]]
- [[cors-writeup-survey]] → [[cors-misconfig-core]], [[cors-misconfig-defense]], [[cors-misconfig]]

## 3. 왜 이 허브가 필요한가
- survey는 서로 다른 공개 writeup을 비교합니다.
- concept는 여러 writeup에서 반복되는 primitive를 재사용 가능한 형태로 정리합니다.
- leaf query writeup은 개별 문제의 풀이 흐름과 재현 포인트를 기록합니다.

## 4. 연결 개념
- [[web-ctf-writeup-topic-map]]
- [[web-ctf-writeup-curation]]
- [[web-ctf-writeup-auth-session]]
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-internal-service]]

## 5. 다음 작업
- 새 survey가 생기면 이 허브에 먼저 연결합니다.
- 반복 primitive가 보이면 해당 concept를 우선 업데이트합니다.
- 개별 leaf writeup이 추가되면 survey와 상호 링크를 맞춥니다.

# Wiki Schema

## Domain
보안 취약점(CVE), 공격 기법, CTF 문제 유형, 보안 용어, 보안 도구 및 실습 환경에 대한 지식 베이스.

## Conventions
- 파일명: 소문자, 하이픈, 공백 금지 (예: `cve-2026-23111-nftables-uaf.md`)
- 모든 위키 페이지는 YAML frontmatter로 시작 (아래 참조)
- `[[wikilinks]]`를 사용하여 페이지 간 연결 (페이지당 최소 2개 아웃바운드 링크)
- 페이지 업데이트 시 `updated` 날짜 갱신
- 새 페이지는 반드시 `index.md`의 올바른 섹션에 등록
- 모든 작업은 `log.md`에 기록
- **출처 표기**: 3개 이상 출처를 종합한 페이지는 문단 끝에 `^[raw/articles/출처파일.md]` 마커 사용

## Frontmatter
```yaml
---
title: 페이지 제목
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: cve | concept | tool | technique | comparison | ctf-challenge | query
tags: [아래 분류에서 선택]
sources: [raw/articles/출처명.md]
confidence: high | medium | low
contested: true   # 모순되는 주장이 있을 때
---
```

### raw/ Frontmatter
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <본문의 SHA256>
---
```

## Tag Taxonomy
### 취약점/위협
- vulnerability, cve, zero-day, rce, lpe, dos, ddos, xss, memory-corruption, uaf, command-injection, path-traversal, file-upload, xxe, ssrf, ssti, csrf, idor, lfi, rfi, file-inclusion, broken-auth, broken-access-control, cors, misconfiguration, denial-of-service, remote-code-execution, directory-traversal, unrestricted-upload, shell-injection, os-command-injection, injection, external-entity, file-read, xml, xpath, template-injection, sandbox-escape, csrf-token, bypass
### 공격 기법
- adversarial-ml, prompt-injection, model-inversion, data-poisoning, model-extraction, phishing, supply-chain, social-engineering, spoofing, mitm, amplification, slowloris, syn-flood, shellcode, rop, exploit, payload, drive-by-download, ping-of-death, serialization, osint, recon, active-recon, passive-recon, cloud-metadata
### 대상/환경
- web, cloud, linux, windows, ai-ml, llm, network, kernel, endpoint, database, local, remote, server-side, php, horizontal, vertical, inline
### CTF
- ctf, ctf-challenge, ai-ctf, agent-security, education, research, challenge-development, lab
### 웹 CTF 세부 태그
- auth, base64, burp, client-side, coturn, csp, cyberchef, decode, dns, encoding, exfiltration, file, inspector, internal-service, localhost, parameter-tampering, parser, race-condition, rebinding, redis, request-manipulation, sandbox, source-analysis, storage, stun, template, turn, webrtc, writeup, xssi
### 보안 도구/솔루션
- tool, scanner, edr, waf, ids, ips, dlp, vpn, hids, nids, snort, suricata, zeek, ngfw, xdr, mdr, epp, antivirus, proxy, detection, response, mcp
### 보안 개념
- security, glossary, cia, triad, confidentiality, integrity, availability, authentication, authorization, access-control, encryption, tunneling, network-security, remote-access, intrusion-detection, intrusion-prevention, data-exfiltration, data-loss-prevention, insider-threat, compliance, api, api-security, impact, critical, mime-type, magic-bytes, webshell, botnet, mirai, cloudflare, nftables, optimization, privilege-escalation, horizontal-privilege-escalation, vertical-privilege-escalation, request-forgery, template-engine, research
### 사이버 킬 체인
- cyber-kill-chain, reconnaissance, weaponization, delivery, exploitation, installation, command-and-control, c2, c2-framework, beacon, implant, actions-on-objectives, persistence, backdoor, rootkit, bootkit, covert-channel
### 보안 표준/프레임워크
- iso27001, nist, gdpr, hipaa, owasp, mitre-attck, parkerian-hexad, drm
### 프로토콜
- protocol, arp, ipsec, tcp, udp, wireguard, layer2
### 메타
- tutorial, reference, training, real-world, breach, ransomware, apt, espionage, sabotage, wiper, malware, webshell
### 인증/접근제어
- mfa-bypass, brute-force, credential-stuffing, session, session-riding, sameorigin, same-origin-policy, cross-origin, rate-limiting, input-validation

규칙: 모든 태그는 이 분류에 있어야 함. 새 태그가 필요하면 여기에 먼저 추가한 후 사용.

### Wiki-curated tags
- accept-language, adjacency, adjacent-chunk, arbitrary-write, array-bounds, aslr, automation, bash, binary-exploitation, bit-flipping
- picoctf2024, picoctf2025
- browser, browser-history, buffer-overflow, cbc, cdecl, checklist, command-abuse, concurrency, control-flow-hijack, cookie
- cookies, cpu, crash, crypto, curl, custom-cpu, decompilation, deserialization, directory-discovery, dnt
- ds-store, email, endianness, enumeration, environment, environment-abuse, eval, executable-stack, execve, filter-bypass
- flask, flask-session, fmtstr, format-string, function-arguments, function-pointer, function-prologue, game-state, get, gets
- git, global-variable, got-overwrite, hash-collision, head, headers, heap, heap-layout, heap-overflow, hidden-directory
- hidden-file, hidden-path, hidden-request, history-api, htaccess, http, import-abuse, info-leak, int-0x80, integer-overflow
- intentional-crash, javascript, jwt, libc-leak, logic-bug, login, login-bypass, maintenance, malleability, md5
- memory-disclosure, method-manipulation, methods, mime, minification, mirror, mmap, module-hijack, mongodb, movement
- no-canary, nopie, nosql, nx, nx-bypass, object-injection, onepage, oob, operations, oracle
- out-of-bounds, parser-template, partial-overwrite, path-hijack, picoctf, picoctf2023, pie, post-auth, printf, prng
- pwn, python, rbash, referer, regex, register-control, restricted-shell, ret2reg, ret2win, return-address
- rev, reverse-engineering, robots-txt, safe_var, saved-return-address, secrets, segfault, session-forgery, setcontext, setuid
- shell, signal-handler, signing, sigsegv, smime, soap, source-inspection, sql-injection, sqli, sqlite
- stack-alignment, stack-canary, stack-layout, stack-leak, stack-overflow, strcpy, strstr, substring, survey, syscalls
- system-abuse, tampering, tcache, tcache-poisoning, timing, tls, token-forgery, top-chunk, traffic-inspection, type-juggling
- underflow, union-based-sqli, unserialize, upload-bypass, use-after-free, user-agent, validation, wasm, webhook, websocket
- wiki, win-function, workflow, x-forwarded-for, x64, x86

## Page Types

### CVE Pages (type: cve)
하나의 CVE에 대한 종합 분석. 포함할 내용:
- 취약점 요약 (CVSS, CWE, 영향 버전)
- 기술적 원인
- 공격 시나리오
- PoC 존재 여부 및 링크
- 패치 및 완화 방법
- 실습 환경 구성 정보
- 관련 CVE/개념으로 [[wikilinks]]

### Concept Pages (type: concept)
보안 개념/용어 설명. 포함할 내용:
- 정의 / 설명
- 공격자 관점과 방어자 관점
- 실제 사례
- 관련 개념으로 [[wikilinks]]

### Tool Pages (type: tool)
보안 도구/프레임워크. 포함할 내용:
- 개요 및 용도
- 설치 방법
- 주요 명령어/사용법
- 실습 예제
- 유사 도구와 비교

### CTF Challenge Pages (type: ctf-challenge)
CTF 문제 유형 및 출제 가이드. 포함할 내용:
- 문제 유형 분류
- 난이도, 소요시간
- 필요한 기술 스택
- 풀이 전략
- 참고 저장소

### Comparison Pages (type: comparison)
비교 분석. 포함할 내용:
- 비교 대상과 이유
- 비교 기준 (표 형식 선호)
- 결론 또는 종합
- 출처

### Query Pages (type: query)
위키에 질문한 결과 중 보관할 가치가 있는 답변.

## Page Thresholds
- **페이지 생성**: 엔티티/개념이 2개 이상 출처에 등장하거나 1개 출처의 핵심 주제일 때
- **기존 페이지 보강**: 출처가 이미 커버된 내용을 언급할 때
- **생성 금지**: 단순 언급, 사소한 세부사항, 도메인 외부 주제
- **분할**: 페이지 200줄 초과 시 하위 주제로 분할하고 상호 링크
- **아카이브**: 내용이 완전히 대체된 경우 `_archive/`로 이동, index에서 제거

## Update Policy
새 정보가 기존 내용과 충돌할 때:
1. 날짜 확인 — 최신 출처가 일반적으로 우선
2. 진정한 모순이면 두 입장을 날짜와 출처와 함께 기록
3. Frontmatter에 `contradictions: [페이지명]` 표기
4. 린트 리포트에서 사용자 검토 플래그

## Entity Pages
주요 엔티티(취약점, 도구, 조직)별 한 페이지.
- 개요 / 정의
- 주요 사실 및 날짜
- 관련 엔티티로 [[wikilinks]]
- 출처 참조
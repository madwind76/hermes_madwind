---
title: Heap Dump — 보안 용어 해설과 Web CTF 패턴
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [security, glossary, web, ctf, storage, data-exfiltration, api]
sources: [https://nodejs.org/learn/diagnostics/memory/using-heap-snapshot, https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots, https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/head-dump/head-dump.md, https://medium.com/@rahmeez/picoctf-head-dump-writeup-2455761c362d]
confidence: high
---

# Heap Dump — 보안 용어 해설과 Web CTF 패턴

## 참고 URL
- [nodejs.org](https://nodejs.org/learn/diagnostics/memory/using-heap-snapshot)
- [developer.chrome.com](https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots)
- [Original source](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/head-dump/head-dump.md)
- [medium.com](https://medium.com/@rahmeez/picoctf-head-dump-writeup-2455761c362d)

## Step 1. 단어 직역과 쉬운 비유

### 1) 단어 풀이
- **Heap**: 프로그램이 실행 중 동적으로 데이터를 저장하는 메모리 영역입니다.
- **Dump**: 내부 상태를 파일로 쏟아내어 저장한 결과물입니다.
- **Heap Dump / Heap Snapshot**: 실행 중인 프로그램의 heap 메모리에 어떤 객체와 값이 들어 있는지 특정 시점에 저장한 파일입니다.

### 2) 한 문장 정의
**Heap Dump**는 애플리케이션이 실행 중 들고 있던 객체·문자열·세션·환경값 같은 메모리 내용을 분석용 파일로 저장한 것입니다.

### 3) 쉬운 비유
Heap dump는 서버의 머릿속을 찍은 **순간 사진**과 같습니다. 평소에는 개발자가 “왜 메모리가 새지?”를 확인하려고 찍는 진단 사진입니다. 그런데 책상 위 사진에 비밀번호 쪽지, API key, CTF flag가 같이 찍혀 있으면 사진을 받은 사람이 그 비밀도 함께 볼 수 있습니다.

## Step 2. 시각화

> `image_generate` 도구는 PNG 형식을 반환하므로, 시각화 이미지는 PNG URL로 임베드합니다.

![Heap Dump 시각화 — 서버 메모리의 순간 사진과 비밀값 노출 위험](https://v3b.fal.media/files/b/0a9e36a2/LIztpHOdqiARRIENjrtXu_RTaYCbJ9.png)

이 그림은 `서버 메모리` 보관함에 객체·변수·세션·API 키·flag가 함께 들어 있고, `/heapdump` 같은 진단 엔드포인트가 이를 `힙 스냅샷 파일`로 저장하는 흐름을 보여줍니다. 정상 목적은 메모리 누수 분석이지만, 외부에 노출되면 비밀값 유출로 이어질 수 있습니다.

## Step 3. 전문 설명

Heap dump 또는 heap snapshot은 실행 중인 프로세스의 heap 메모리 상태를 기록한 진단 산출물입니다. Node.js 문서는 실행 중인 애플리케이션에서 heap snapshot을 생성하고 Chrome Developer Tools로 로드해 변수, 객체, retain size 등을 분석할 수 있다고 설명합니다. Chrome DevTools 문서도 JavaScript 객체와 관련 DOM 노드의 메모리 분포를 분석하기 위해 heap snapshot을 기록하는 기능을 제공합니다.

보안 관점에서 heap dump는 단순 로그보다 더 민감할 수 있습니다. 애플리케이션이 메모리에 올려 둔 문자열, 토큰, 세션 값, 환경 변수, flag, API key가 파일 내부에 그대로 남을 수 있기 때문입니다. 따라서 `/heapdump`, `/actuator/heapdump`, `/debug/heap`, `/diagnostics` 같은 진단 엔드포인트는 외부에 노출되면 안 되며, 운영 환경에서는 인증·권한·네트워크 제한·비활성화 정책이 필요합니다.

CTF에서는 heap dump가 “비밀이 메모리에 이미 올라와 있다”는 전제를 학습시키는 문제로 자주 등장합니다. 대표 흐름은 `API 문서 발견 → 진단 엔드포인트 확인 → heap snapshot 다운로드 → flag prefix 검색`입니다.

## 공격자 관점

1. 공개 페이지에서 `/api-docs`, `/swagger`, `/docs`, `/openapi.json` 같은 API 문서 경로를 찾습니다.
2. 문서에서 `heapdump`, `diagnostics`, `debug`, `snapshot` 같은 진단성 엔드포인트를 찾습니다.
3. 다운로드 가능한 `.heapsnapshot` 또는 텍스트 파일을 확보합니다.
4. CTF에서는 알려진 flag prefix인 `picoCTF{`를 검색합니다.

```bash
# 다운로드한 heap snapshot에서 picoCTF flag prefix를 검색합니다.
# 예상 출력: picoCTF{...} 형식의 문자열이 포함된 줄이 출력됩니다.
grep -E 'picoCTF\{[^}]+\}' heapdump-*.heapsnapshot
```

## 방어자 관점

- 운영 환경에서 heap dump 생성 엔드포인트를 공개하지 않습니다.
- 디버그·진단 라우트는 기본 비활성화하고, 필요한 경우 내부망·VPN·관리자 인증으로 제한합니다.
- heap snapshot 파일은 로그나 첨부 파일처럼 장기간 보관하지 않습니다.
- secret, token, key를 장기 문자열로 메모리에 유지하지 않도록 설계합니다.
- API 문서에는 운영 환경에서 호출 가능한 민감 엔드포인트가 노출되지 않도록 합니다.

## Web CTF 패턴

`picoCTF 2025 head-dump`에서는 `picoCTF News` 사이트 안의 API Documentation 링크가 `/api-docs`로 이어지고, Swagger UI에서 `/heapdump` 엔드포인트를 찾습니다. 이 엔드포인트가 생성한 heap snapshot을 내려받아 `grep picoCTF`로 검색하면 flag가 발견됩니다.

관련 writeup: [[head-dump-final-writeup]]

## 관련 위키 링크

- [[api-security]] — API 문서와 엔드포인트 노출 관리
- [[api-security-defense]] — Swagger/OpenAPI 운영 방어 관점
- [[ssrf-core]] — 내부 진단 엔드포인트 노출 예시와 비교
- [[web-ctf-master-checklist]] — Web CTF 공통 점검 목록
- [[web-ctf-writeup-internal-service]] — 내부 서비스/진단 엔드포인트 계열 writeup 허브

## 참고 소스

- [Node.js — Using Heap Snapshot](https://nodejs.org/learn/diagnostics/memory/using-heap-snapshot)
- [Chrome DevTools — Record heap snapshots](https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots)
- [snwau GitHub writeup — picoCTF head-dump](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/head-dump/head-dump.md)
- [Rehema Said Medium writeup — picoCTF head-dump](https://medium.com/@rahmeez/picoctf-head-dump-writeup-2455761c362d)

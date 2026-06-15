---
title: Hidden directory discovery — picoCTF pattern
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [ctf, web, directory-discovery, reconnaissance, path-traversal, source-inspection]
sources: [https://medium.com/@erichdryn/secrets-picoctf-writeup-bcfa26143bb1, https://medium.com/@moromerx/picoctf-secrets-web-exploitation-explained-3e8d41b40a2a, https://medium.com/@ahmednarmer1/ctf-day-26-4760e9b83079]
confidence: high
---

# Hidden directory discovery — picoCTF pattern

## Step 1. 한 줄 정의
이 패턴은 **페이지 소스, 개발자 도구, 디렉터리 구조, 그리고 URL 경로를 이용해 숨은 디렉터리와 페이지를 순차적으로 찾아가는 Web CTF 유형**입니다. 상위 허브는 [[web-recon-hidden-file-discovery-ctf-hub]]입니다.

## Step 2. 비유
- **비유**: 지도에 없는 골목을 간판과 문패를 따라 하나씩 찾아가는 느낌입니다.
- **이미지**: 브라우저가 보여주는 화면보다, 소스에 적힌 경로와 디렉터리명이 더 중요한 단서입니다.
- **전문 설명**: 정적 자원이나 HTML에서 `secret`, `hidden`, `superhidden` 같은 경로 단서를 찾고, trailing slash 유무까지 확인하며 서버의 디렉터리 처리 방식을 추적합니다.

## 핵심 흐름
```text
page/source inspection -> directory hint 발견 -> /secret/ 접근 -> /hidden/ 추적 -> /superhidden/ 도달 -> flag 획득
```

## 공격자 관점
1. Developer Tools의 Sources 탭을 확인합니다.
2. 디렉터리 이름이 보이면 URL로 직접 접근합니다.
3. `.../secret/`처럼 trailing slash 차이를 테스트합니다.
4. 다음 하위 디렉터리 이름을 계속 추적합니다.
5. robots.txt, hidden assets, directory listing 가능성도 같이 확인합니다.

## 방어자 관점
- 민감한 디렉터리 구조를 클라이언트에 노출하지 않습니다.
- 디렉터리 브라우징과 불필요한 경로 노출을 차단합니다.
- 소스와 정적 자원에 힌트성 문자열을 남기지 않습니다.
- 서버의 기본 문서와 접근 정책을 명확히 설정합니다.

## 같이 보면 좋은 페이지
- [[reconnaissance]]
- [[web-recon-hidden-file-discovery-ctf-hub]]
- [[web-recon-hidden-file-discovery-checklist]]
- [[web-recon-hidden-file-discovery-onepage]]
- [[path-traversal-core]]
- [[source-inspection-minification-ctf-patterns]]
- [[secrets-final-writeup]]

## 참고 소스
- [Eric H — Secrets — PicoCTF Writeup](https://medium.com/@erichdryn/secrets-picoctf-writeup-bcfa26143bb1)
- [MoRoMeR — picoCTF Secrets Explained](https://medium.com/@moromerx/picoctf-secrets-web-exploitation-explained-3e8d41b40a2a)
- [Ahmed Narmer — picoCTF Web Exploitation: Secrets](https://medium.com/@ahmednarmer1/ctf-day-26-4760e9b83079)

---
title: Secrets — picoCTF web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, reconnaissance, directory-traversal, source-inspection, hidden-directory]
sources: [https://medium.com/@erichdryn/secrets-picoctf-writeup-bcfa26143bb1, https://medium.com/@moromerx/picoctf-secrets-web-exploitation-explained-3e8d41b40a2a, https://medium.com/@ahmednarmer1/ctf-day-26-4760e9b83079]
confidence: high
---

# Secrets — picoCTF web writeup

> 페이지 소스와 디렉터리 힌트를 따라 `secret/hidden/superhidden` 경로를 찾아가며 flag를 얻는 picoCTF Web Exploitation 문제입니다.

## 1. 한 줄 요약
- 핵심은 **숨은 디렉터리 탐색**입니다.
- `secret/` → `hidden/` → `superhidden/` 순서로 추적합니다.
- `view-source`와 Developer Tools의 **Sources** 탭이 중요합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 문제 설명에 hidden pages 언급 | 디렉터리 탐색을 의심 |
| 2 | Sources 탭에서 `assets`/`secret` 단서 발견 | 경로 구조 노출 |
| 3 | `/secret/` 접근 | 올바른 경로 진입 |
| 4 | `hidden` 단서 발견 | 다음 단계 경로 획득 |
| 5 | `/secret/hidden/superhidden/` 접근 | flag 획득 |

## 3. 분석 포인트
```text
# trailing slash 유무에 따라 서버가 디렉터리로 볼지 파일로 볼지 달라질 수 있습니다.
# 예상 결과: /secret/ 에서 힌트 페이지, 이후 하위 디렉터리로 flag에 도달합니다.
```

## 4. 공격자 관점
1. HTML source와 Developer Tools를 확인합니다.
2. 디렉터리 이름이 보이면 직접 URL로 입력합니다.
3. trailing slash(`.../secret/`) 차이를 확인합니다.
4. 다음 하위 디렉터리를 계속 추적합니다.
5. 숨은 파일/페이지가 있으면 끝까지 들어가 봅니다.

## 5. 방어자 관점
- 클라이언트에 디렉터리 구조 힌트를 남기지 않습니다.
- 디렉터리 브라우징을 허용하지 않습니다.
- 불필요한 정적 자원 공개를 줄입니다.
- 경로 추론이 가능한 이름을 그대로 노출하지 않습니다.

## 6. 같이 보면 좋은 페이지
- [[hidden-directory-discovery-ctf-patterns]]
- [[reconnaissance]]
- [[path-traversal-core]]
- [[source-inspection-minification-ctf-patterns]]

## 7. 참고 소스
- [Eric H — Secrets — PicoCTF Writeup](https://medium.com/@erichdryn/secrets-picoctf-writeup-bcfa26143bb1)
- [MoRoMeR — picoCTF Secrets Explained](https://medium.com/@moromerx/picoctf-secrets-web-exploitation-explained-3e8d41b40a2a)
- [Ahmed Narmer — picoCTF Web Exploitation: Secrets](https://medium.com/@ahmednarmer1/ctf-day-26-4760e9b83079)

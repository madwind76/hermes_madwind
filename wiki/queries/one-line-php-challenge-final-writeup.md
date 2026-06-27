---
title: One Line PHP Challenge — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, research]
sources: [https://github.com/orangetw/My-CTF-Web-Challenges, https://blog.kaibro.tw/2018/10/24/HITCON-CTF-2018-Web/, https://hacktricks.wiki/en/pentesting-web/file-inclusion/via-php_session_upload_progress.html]
confidence: medium
---

# One Line PHP Challenge — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 참고 URL
- [orangetw/My-CTF-Web-Challenges](https://github.com/orangetw/My-CTF-Web-Challenges)
- [blog.kaibro.tw](https://blog.kaibro.tw/2018/10/24/HITCON-CTF-2018-Web/)
- [hacktricks.wiki](https://hacktricks.wiki/en/pentesting-web/file-inclusion/via-php_session_upload_progress.html)


## 1. 문제 요약
- 플랫폼: HITCON CTF 2018
- 점수 / 난이도: web challenge
- 핵심 취약점: PHP wrapper와 session.upload_progress를 결합해 file read에서 RCE로 이어지는 문제입니다.
- 관련 개념: [[lfi-rfi]], [[path-traversal-ctf-patterns]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. 업로드 처리와 file inclusion 지점을 찾습니다.
2. PHP wrapper를 이용해 로컬 파일을 읽습니다.
3. session.upload_progress 경로를 LFI 대상으로 삼습니다.
4. 결국 RCE 또는 flag read를 획득합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| wrapper | file scheme 대신 PHP wrapper가 핵심입니다. | 단순 path traversal보다 강력합니다. |
| session file | 임시 세션 파일이 포함 대상입니다. | 서버 내부 상태가 공격면이 됩니다. |
| 결과 | flag에 도달합니다. | PHP file inclusion 계열의 전형입니다. |

## 4. 방어 관점
- 사용자 입력으로 PHP wrapper를 직접 열지 않아야 합니다.
- 업로드 처리와 include 경로를 분리해야 합니다.
- session upload progress 같은 레거시 기능은 제한해야 합니다.

## 5. 회고
- 이 문제는 PHP wrapper와 session.upload_progress를 결합해 file read에서 RCE로 이어지는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[lfi-rfi]]
- [[path-traversal-ctf-patterns]]
- [[web-ctf-master-checklist]]

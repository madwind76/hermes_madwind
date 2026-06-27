---
title: BBS — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, research]
sources: [https://kt.gy/blog/2018/06/googlectf-2018-quals-web-bbs/, https://ctftime.org/writeup/10369, https://ctftime.org/writeup/10366]
confidence: medium
---

# BBS — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 참고 URL
- [kt.gy](https://kt.gy/blog/2018/06/googlectf-2018-quals-web-bbs/)
- [CTFtime writeup](https://ctftime.org/writeup/10369)
- [CTFtime writeup](https://ctftime.org/writeup/10366)


## 1. 문제 요약
- 플랫폼: Google CTF 2018 Quals
- 점수 / 난이도: 453 pts
- 핵심 취약점: avatar 업로드와 Range header, report 경로 우회를 결합한 XSS 풀이입니다.
- 관련 개념: [[web-inspector-ctf-patterns]], [[parameter-tampering-ctf-patterns]], [[xss]]

## 2. 풀이 흐름
1. 게시판 iframe 렌더링과 ajax 호출을 분석합니다.
2. avatar에 XSS가 살아남는지를 확인합니다.
3. Range header로 필요한 바이트만 가져옵니다.
4. report 경로를 우회해 admin에게 제출합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| iframe | p 파라미터가 ajax settings로 확장됩니다. | 단순 query보다 더 큰 제어권이 생깁니다. |
| avatar | 재인코딩된 PNG의 일부를 악용합니다. | 이미지 처리 파이프라인이 공격 지점입니다. |
| report | 경로 검사 우회가 가능합니다. | validation이 곧 보안은 아닙니다. |

## 4. 방어 관점
- 클라이언트에서 받은 경로를 직접 ajax 설정으로 쓰지 않아야 합니다.
- 이미지 업로드 후 다시 읽는 경로를 엄격히 분리해야 합니다.
- report 대상은 정규화 후 allowlist로 검증해야 합니다.

## 5. 회고
- 이 문제는 avatar 업로드와 Range header, report 경로 우회를 결합한 XSS 풀이입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]
- [[xss]]

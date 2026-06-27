---
title: Sourceless — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, research]
sources: [https://gist.github.com/terjanq/4cb40653760c1ba8c33ee06be098d508, https://ctftime.org/event/2718/tasks/, https://ctftime.org/team/23929/]
confidence: medium
---

# Sourceless — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 참고 URL
- [Gist](https://gist.github.com/terjanq/4cb40653760c1ba8c33ee06be098d508)
- [CTFtime writeup](https://ctftime.org/event/2718/tasks/)
- [CTFtime writeup](https://ctftime.org/team/23929/)


## 1. 문제 요약
- 플랫폼: Google CTF 2025
- 점수 / 난이도: 298 pts
- 핵심 취약점: Firefox Puppeteer 환경에서 file://와 XSSI 성질을 이용해 flag.txt를 읽는 문제입니다.
- 관련 개념: [[xssi-file-exfiltration-ctf-patterns]], [[web-ctf-master-checklist]], [[web-inspector-ctf-patterns]]

## 2. 풀이 흐름
1. bot의 URL 방문 동작과 file:// 정책을 확인합니다.
2. 에러 메시지 기반으로 flag 조각을 추출합니다.
3. IndexedDB에 페이로드를 저장합니다.
4. 저장된 file:// 경로를 bot이 방문하게 합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| file scheme | file:// 접근이 가능한 경로가 있습니다. | 로컬 파일이 곧 데이터 소스가 됩니다. |
| error side channel | 에러 메시지에 내용이 노출됩니다. | 파서/콘솔 차이가 유출 통로입니다. |
| 결과 | flag.txt 내용을 복원합니다. | XSSI와 로컬 파일 접근이 결합됩니다. |

## 4. 방어 관점
- 자동화 브라우저의 file-origin 정책을 엄격히 유지해야 합니다.
- 에러 메시지와 콘솔 로그에 민감 정보를 넣지 않아야 합니다.
- 브라우저 저장소에 페이로드를 장기 보관하지 않도록 해야 합니다.

## 5. 회고
- 이 문제는 Firefox Puppeteer 환경에서 file://와 XSSI 성질을 이용해 flag.txt를 읽는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[xssi-file-exfiltration-ctf-patterns]]
- [[web-ctf-master-checklist]]
- [[web-inspector-ctf-patterns]]

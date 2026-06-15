---
title: Where Are the Robots? — picoCTF web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, reconnaissance, robots-txt, hidden-path, source-inspection]
sources: [https://medium.com/@hasnain_abid/where-are-the-robots-picoctf-web-exploitation-writeup-82a121cfd935, https://medium.com/@Kamal_S/picoctf-web-exploitation-where-are-the-robots-399111c4dc8e, https://medium.com/@vanya.verma31/where-are-the-robots-856b904fdc5d]
confidence: high
---

# Where Are the Robots? — picoCTF web writeup

> `robots.txt`에 숨겨진 경로를 따라가며 flag를 찾는 picoCTF Web Exploitation 문제입니다.

## 1. 한 줄 요약
- 핵심은 **웹사이트의 공개 안내 파일인 `robots.txt`** 를 확인하는 것입니다.
- `robots.txt`에 적힌 경로를 직접 열면 flag가 있는 페이지에 도달할 수 있습니다.
- 복잡한 공격보다 **정찰(reconnaissance)** 이 중심입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 웹페이지에 눈에 띄는 기능이 거의 없음 | 숨은 단서 탐색 필요 |
| 2 | `/robots.txt` 접근 | 검색 엔진용 안내 파일 확인 |
| 3 | Disallow 된 경로 발견 | 숨겨진 페이지 후보 확보 |
| 4 | 해당 경로를 직접 열기 | flag 페이지 접근 |
| 5 | flag 확인 | 문제 해결 |

## 3. 분석 포인트
```text
# robots.txt는 보안 장치가 아니라 공개 힌트입니다.
# 예상 결과: Disallow 경로가 실제 숨은 페이지 경로로 이어집니다.
```

## 4. 공격자 관점
1. 메인 페이지의 기능을 확인합니다.
2. `/robots.txt`를 직접 요청합니다.
3. 숨겨진 디렉터리나 파일명을 기록합니다.
4. 해당 경로를 브라우저로 열어봅니다.
5. flag가 있는지 확인합니다.

## 5. 방어자 관점
- `robots.txt`에 민감한 경로를 두지 않습니다.
- 숨겨진 경로가 있어도 접근 통제를 별도로 적용합니다.
- 공개 파일만으로 내부 구조가 쉽게 추정되지 않도록 합니다.
- 민감 페이지는 인증 뒤에만 접근 가능하게 둡니다.

## 6. 같이 보면 좋은 페이지
- [[hidden-directory-discovery-ctf-patterns]]
- [[scavenger-hunt-final-writeup]]
- [[web-ctf-writeup-curation]]
- [[web-ctf-writeup-topic-map]]

## 7. 참고 소스
- [Hasnain Abid — Where Are the Robots?](https://medium.com/@hasnain_abid/where-are-the-robots-picoctf-web-exploitation-writeup-82a121cfd935)
- [Kamal S — picoCTF Web Exploitation: where are the robots](https://medium.com/@Kamal_S/picoctf-web-exploitation-where-are-the-robots-399111c4dc8e)
- [Vanya Verma — where are the robots](https://medium.com/@vanya.verma31/where-are-the-robots-856b904fdc5d)

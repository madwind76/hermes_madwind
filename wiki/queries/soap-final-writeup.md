---
title: SOAP — picoCTF 2023 XXE web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, xxe, xml, soap, burp, parser-template]
sources: [https://medium.com/@Kamal_S/picoctf-web-exploitation-soap-c68604ec3469, https://medium.com/@Cy_berJack/soap-picoctf-web-exploitation-challenge-3cf9d0f38fa5, https://siunam321.github.io/ctf/picoCTF-2023/Web-Exploitation/SOAP/, https://github.com/DanArmor/picoCTF-2023-writeup/blob/main/Web%20Exploitation/SOAP/SOAP.md]
confidence: high
---

# SOAP — picoCTF 2023 XXE web writeup

> `SOAP`는 이름만 보면 프로토콜 학습 문제처럼 보이지만, 실제로는 **XML을 잘못 파싱하는 Web API에서 `XXE`를 유도하는 문제**입니다.

## 1. 한 줄 요약
- 챌린지 설명은 ` /etc/passwd `를 읽으라고 힌트를 줍니다.
- 화면의 `Details` 버튼은 내부적으로 XML 기반 POST 요청을 보냅니다.
- 핵심은 **SOAP/XML 요청을 Burp Suite로 잡아 `XXE` 페이로드로 바꾸는 것**입니다.

## 2. 문제 구조
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 메인 화면에 카드 3개와 `Details` 버튼 | 사용자 입력이 숨겨져 있을 가능성 |
| 2 | 버튼 클릭 시 `/data`로 POST | 서버가 상세정보를 별도 요청으로 처리 |
| 3 | 요청 본문이 XML 형태 | XML 파서가 동작함 |
| 4 | JS가 form 데이터를 XML로 변환 | 클라이언트가 XML 요청을 만들어 보냄 |
| 5 | 외부 엔티티 삽입 | 서버 측 파일 읽기 가능성 |
| 6 | `/etc/passwd` 내용 노출 | 취약점 성공 |

## 3. 핵심 분석
이 문제는 **검증 로직과 XML 파서의 기대 형식이 맞지 않는 경우**에 발생하는 전형적인 `XXE` 패턴입니다.

- 프론트엔드 스크립트가 `ID`를 XML로 변환합니다.
- 서버는 그 XML을 안전하게 처리하지 않습니다.
- 공격자는 `DOCTYPE`와 외부 엔티티를 넣어 서버 파일을 읽을 수 있습니다.

### 대표 페이로드 예시
```xml
<!-- XML 파서가 외부 엔티티를 허용하는지 확인하는 XXE 예시입니다. -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>
  <ID>&xxe;</ID>
</data>
```

## 4. 공격자 관점
1. 사이트를 열고 `Details` 버튼 동작을 확인합니다.
2. `Burp Suite`로 요청을 가로챕니다.
3. `/data` 엔드포인트와 XML 본문 형식을 확인합니다.
4. 요청을 `Burp Repeater`로 보내 XML을 수정합니다.
5. `DOCTYPE`와 외부 엔티티를 삽입합니다.
6. 응답에서 `/etc/passwd` 또는 flag 노출을 확인합니다.

## 5. 방어자 관점
- XML 파서에서 외부 엔티티를 비활성화합니다.
- `DOCTYPE`를 허용하지 않습니다.
- 요청 형식을 서버에서 엄격하게 검증합니다.
- SOAP/XML 입력을 그대로 렌더링하거나 echo 하지 않습니다.
- 네트워크 아웃바운드를 제한해 Blind XXE 피해를 줄입니다.

## 6. 같이 보면 좋은 페이지
- [[xxe]]
- [[xxe-defense]]
- [[web-ctf-writeup-parser-template]]
- [[web-ctf-writeup-curation]]
- [[web-ctf-writeup-topic-map]]

## 7. 참고 소스
- [Kamal S — picoCTF Web Exploitation: SOAP](https://medium.com/@Kamal_S/picoctf-web-exploitation-soap-c68604ec3469)
- [Daemi Jack — SOAP picoCTF Web Exploitation challenge](https://medium.com/@Cy_berJack/soap-picoctf-web-exploitation-challenge-3cf9d0f38fa5)
- [siunam — SOAP | picoCTF 2023 Web Exploitation Summary](https://siunam321.github.io/ctf/picoCTF-2023/Web-Exploitation/SOAP/)
- [DanArmor — picoCTF-2023-writeup / SOAP](https://github.com/DanArmor/picoCTF-2023-writeup/blob/main/Web%20Exploitation/SOAP/SOAP.md)

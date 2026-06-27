---
title: Some Assembly Required 1 — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, javascript, wasm, source-inspection, burp, picoctf]
sources: [https://ctftime.org/writeup/26982, https://medium.com/@Kamal_S/picoctf-web-exploitation-some-assembly-required-1-194e459b73db, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Some%20Assembly%20Required%201/README.md]
confidence: high
---

# Some Assembly Required 1 — picoCTF 2021 web writeup

> `Some Assembly Required 1`는 **오브퓨스케이티드(난독화된) JavaScript가 숨은 리소스를 불러오고, 그 뒤 WebAssembly/WASM 페이로드에서 flag를 찾는 picoCTF 2021 Web 문제**입니다. 겉보기에는 폼 입력 문제처럼 보이지만, 실제 핵심은 **브라우저가 추가로 요청하는 리소스와 응답 내용을 추적하는 것**입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/26982)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-some-assembly-required-1-194e459b73db)
- [Original writeup](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Some%20Assembly%20Required%201/README.md)


## 1. 한 줄 요약
- 화면의 입력값은 거의 의미가 없습니다.
- Burp Suite의 Proxy history에서 숨은 리소스 요청을 찾습니다.
- JS가 추가로 요청하는 파일과 그 응답을 따라갑니다.
- 응답으로 내려오는 WASM/바이너리 문자열 안에서 flag를 찾습니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 간단한 입력 폼과 `Incorrect!` 응답이 보임 | 폼 값 자체는 핵심이 아님 |
| 2 | 브라우저 트래픽을 Burp로 보면 추가 요청이 보임 | 숨은 리소스가 공격면 |
| 3 | `G82XCw5CX3.js` 같은 JS 리소스가 확인됨 | 난독화된 실행 흐름 |
| 4 | JS가 `JIFxzHyW8W` 같은 별도 리소스를 요청함 | 실제 flag 경로 |
| 5 | 응답을 열면 WASM/바이너리 형태의 긴 문자열이 보임 | flag가 payload 안에 포함됨 |
| 6 | 문자열 끝부분에서 flag를 획득함 | 최종 성공 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 **표면상 웹 폼 문제처럼 보이지만, 실질적으로는 브라우저가 로드하는 숨은 리소스를 추적하는 문제**입니다. 난독화된 JS를 읽는 것보다, **네트워크 요청 목록을 먼저 보는 것**이 훨씬 빠릅니다.

### 3.2 실전 확인 포인트
```bash
# Burp Proxy history에서 추가 JS/리소스 요청을 확인합니다.
# 예상 결과: /G82XCw5CX3.js, /JIFxzHyW8W 같은 경로가 보입니다.
```

```bash
# 응답 본문에서 flag 문자열을 직접 검색합니다.
# 예상 결과: 긴 base64/WASM 문자열 끝부분에서 picoCTF{...}가 확인됩니다.
```

### 3.3 풀이 흐름
1. 브라우저에서 문제 페이지를 엽니다.
2. Burp Suite로 요청/응답을 캡처합니다.
3. 입력값을 바꿔도 모두 `Incorrect!`가 나오는지 확인합니다.
4. Proxy history에서 이상한 JS/WASM 경로를 찾습니다.
5. 해당 요청을 Repeater 또는 브라우저로 다시 열어 응답을 확인합니다.
6. 응답 끝부분에서 flag를 추출합니다.

## 4. 공격자 관점
- 입력 폼이 아니라 **리소스 체인**을 보아야 합니다.
- JS 파일만 보지 말고, 그 JS가 불러오는 다음 단계 파일도 확인해야 합니다.
- 길게 인코딩된 문자열은 종종 WASM/바이너리 또는 숨은 데이터입니다.

## 5. 방어자 관점
- 클라이언트에 노출되는 리소스에는 비밀을 두지 말아야 합니다.
- 난독화는 보안이 아니므로, 중요한 값은 서버에서 검증해야 합니다.
- 디버깅용 엔드포인트나 숨은 파일이 배포본에 남지 않도록 정리해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[web-inspector-ctf-patterns]]
- [[source-inspection-minification-ctf-patterns]]
- [[web-recon-hidden-file-discovery-ctf-hub]]
- [[webdecode-final-writeup]]
- [[unminify-final-writeup]]

## 7. 참고 소스
- [CTFtime — Some Assembly Required 1](https://ctftime.org/writeup/26982)
- [Kamal S — picoCTF Web Exploitation: Some Assembly Required 1](https://medium.com/@Kamal_S/picoctf-web-exploitation-some-assembly-required-1-194e459b73db)
- [HHousen — Some Assembly Required 1 README](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Some%20Assembly%20Required%201/README.md)

---
title: Ancient History — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, browser-history, client-side, history-api, picoctf]
sources: [https://ctftime.org/writeup/27367, https://picoctf2021.haydenhousen.com/web-exploitation/ancient-history, https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Ancient_History.md]
confidence: high
---

# Ancient History — picoCTF 2021 web writeup

> `Ancient History`는 **브라우저 history stack을 역이용해 숨겨진 flag 상태를 되찾는** picoCTF 2021 Web 문제입니다. 핵심은 페이지가 생성한 여러 상태 중 일부가 브라우저 history에 남아 있고, `window.history.back()` 같은 동작으로 이전 상태를 다시 볼 수 있다는 점입니다.

## 1. 한 줄 요약
- 페이지가 여러 상태를 DOM에 쌓습니다.
- 브라우저 history에서 이전 상태를 되돌아가면 flag가 포함된 화면을 다시 볼 수 있습니다.
- 서버 취약점보다 **클라이언트 상태 관리 실수**가 핵심입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 페이지에서 입력/탐색을 반복할수록 history가 쌓임 | 상태가 브라우저에 남음 |
| 2 | 최신 화면에는 flag가 직접 보이지 않음 | 현재 상태만 보면 놓침 |
| 3 | 뒤로 가기(back)로 이전 상태를 확인 | history stack이 공격면 |
| 4 | 특정 이전 상태에서 flag 획득 | 정보가 history에 남아 있었음 |

## 3. 핵심 분석
### 3.1 왜 이게 먹히는가
브라우저는 사용자가 방문한 상태를 history stack에 남깁니다. 웹앱이 상태 전환을 서버에서 재검증하지 않거나, 이전 화면에 민감정보를 남겨두면 history를 통해 다시 볼 수 있습니다.

### 3.2 실전 확인 포인트
```javascript
// 브라우저 history를 한 단계 뒤로 이동합니다.
// 예상 결과: 이전 DOM 상태가 다시 렌더링됩니다.
window.history.back();
```

```javascript
// 현재 history 길이를 확인합니다.
// 예상 결과: 여러 상태가 쌓였는지 확인할 수 있습니다.
console.log(window.history.length);
```

### 3.3 풀이 흐름
1. 페이지를 열고 상호작용을 진행합니다.
2. `window.history.back()` 또는 브라우저 뒤로가기 버튼을 사용합니다.
3. 이전 화면에서 flag 또는 flag 단서를 찾습니다.
4. 필요하면 history를 여러 번 되돌아가며 숨은 상태를 확인합니다.

## 4. 공격자 관점
- 개발자가 “현재 화면만 보이지 않으면 안전하다”고 착각하기 쉬운 유형입니다.
- JS 상태, route, DOM snapshot, browser cache/history가 모두 단서가 됩니다.
- XSS가 없어도 민감정보가 history에 남으면 누출될 수 있습니다.

## 5. 방어자 관점
- 민감한 상태를 history에 남기지 않습니다.
- `pushState`/`replaceState` 사용 시 노출 가능한 파라미터를 최소화합니다.
- 이전 화면에 flag나 비밀값을 렌더링하지 않습니다.

## 6. 같이 보면 좋은 페이지
- [[browser-history-manipulation-ctf-patterns]]
- [[web-ctf-writeup-client-side]]
- [[bookmarklet-final-writeup]]

## 7. 참고 소스
- [CTFtime — Ancient History](https://ctftime.org/writeup/27367)
- [Hayden Housen — Ancient History](https://picoctf2021.haydenhousen.com/web-exploitation/ancient-history)
- [Dvd848 — Ancient History](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Ancient_History.md)

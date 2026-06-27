---
title: Live Art — picoCTF 2022 web exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, web-exploitation]
sources: [https://github.com/zwade/live-art, https://raw.githubusercontent.com/zwade/live-art/master/problem.md, https://raw.githubusercontent.com/zwade/live-art/master/solution/writeup.md]
confidence: medium
---

# Live Art — picoCTF 2022 web exploitation writeup

## 참고 URL
- [zwade/live-art challenge repo](https://github.com/zwade/live-art)
- [problem.md](https://raw.githubusercontent.com/zwade/live-art/master/problem.md)
- [solution writeup](https://raw.githubusercontent.com/zwade/live-art/master/solution/writeup.md)

## 핵심 요약
이 문제는 React의 higher-order component 처리와 hook state가 같은 fiber에 묶인다는 점을 악용하는 웹 문제입니다.
화면 너비를 바꿔 `ErrorPage`와 `Viewer`가 서로 다른 hook 순서를 공유하게 만들면, `useHashParams`에서 읽은 사용자 제어 값이 `img` props로 전이됩니다.
그 결과 `is=img`, `src=...`, `onload=...` 조합으로 XSS를 유도해 플래그를 탈취할 수 있습니다.

## 풀이 메모
1. `drawing/index.tsx`에서 `getWrappedError()`와 `getWrappedViewer()`가 직접 함수 호출로 쓰이는 점을 확인합니다.
2. `useHashParams`의 `useState` 상태를 이용해 hash fragment 값을 컨트롤합니다.
3. iframe 안에서 좁은 폭으로 에러 페이지를 띄운 뒤, 폭을 넓혀 Viewer로 전환하면서 hook state teleportation을 유도합니다.
4. `is=img`와 이벤트 속성을 함께 주입해 브라우저에서 JS가 실행되도록 만듭니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-web-exploitation-survey]]
- [[picoctf-2022-web-exploitation-family-hub]]
- [[picoctf-2022-topic-map]]

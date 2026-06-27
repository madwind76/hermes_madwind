---
title: Pachinko — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, research, writeup, burp, parameter-tampering, race-condition]
sources: [https://medium.com/@divyanshurds.kumar/writeup-picoctf-2025-pachinko-2dcb85b3202f, https://medium.com/@kofikitiabi/pachinko-picoctf-2025-full-walkthrough-beginner-friendly-91f263c801d2, https://medium.com/@ahmednarmer1/ctf-day-24-0e1e8a56b6f6, https://medium.com/@debasissadhu712/how-i-solved-picoctf-2025-pachinko-web-exploitation-full-step-by-step-walkthrough-9f76f069c52f, https://hackmd.io/qE2e4hMiQ06HcBaWWWhkuw]
confidence: high
---

# Pachinko — picoCTF 2025 web writeup

> NAND 시뮬레이터 형태의 웹앱입니다. 공개 writeup들은 `Burp Intruder` 기반 fuzzing 경로와 `race condition` 경로를 함께 보여주며, 이 노트는 **첫 번째 flag용 요청 변조/fuzzing 경로**를 중심으로 정리합니다.

## 참고 URL
- [medium.com](https://medium.com/@divyanshurds.kumar/writeup-picoctf-2025-pachinko-2dcb85b3202f)
- [medium.com](https://medium.com/@kofikitiabi/pachinko-picoctf-2025-full-walkthrough-beginner-friendly-91f263c801d2)
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-24-0e1e8a56b6f6)
- [medium.com](https://medium.com/@debasissadhu712/how-i-solved-picoctf-2025-pachinko-web-exploitation-full-step-by-step-walkthrough-9f76f069c52f)
- [hackmd.io](https://hackmd.io/qE2e4hMiQ06HcBaWWWhkuw)


## 1. 핵심 요약

- 이 문제는 **UI 퍼즐처럼 보이지만 실제로는 요청 변조, fuzzing, 그리고 일부 풀이의 race condition 관점**이 핵심입니다.
- 서버 소스가 제공되지만, 복잡한 회로를 완전히 수동으로 풀기보다 **요청 형식과 응답 차이**를 관찰하는 편이 빠릅니다.
- Burp Suite의 **Intruder**로 `input1`, `input2`, `output` 값을 대량 탐색하면 성공 응답을 찾을 수 있습니다.

연결 개념: [[parameter-tampering-ctf-patterns]], [[race-condition-ctf-patterns]], [[web-ctf-writeup-auth-session]], [[burp-suite]]

## 2. 문제 흐름

| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 인터페이스는 NAND simulator처럼 보임 | 프론트엔드 퍼즐로 보이지만 실제 핵심은 백엔드 |
| 2 | 제출 시 `/check` 로 JSON POST 발생 | 서버가 JSON circuit 구조를 검증 |
| 3 | 요청 본문에 `input1`, `input2`, `output` 필드 존재 | 변조 가능한 파라미터가 생김 |
| 4 | Burp Intruder로 0~100 숫자를 fuzzing | valid combination 탐색 |
| 5 | 특정 요청에서 200 / 더 긴 응답 / flag JSON 발견 | 첫 번째 flag 획득 |

## 3. 대표 우회 방식

### 3.1 캡처된 요청 예시
```http
POST /check HTTP/1.1
# Burp로 가로챈 뒤 JSON body를 확인합니다.
Content-Type: application/json
```

```json
{
  "circuit": [
    {"input1": 5, "input2": 6, "output": 1},
    {"input1": 6, "input2": 7, "output": 2}
  ]
}
```

### 3.2 Intruder fuzzing 방식
```text
# Burp Intruder 예시 설정
# - Attack type: Sniper
# - Payload type: Numbers
# - Range: 0 to 100
# - Targets: input1, input2, output
```

### 3.3 성공 응답 예시
```json
{
  "status": "success",
  "flag": "picoCTF{p4ch1nk0_f146_0n3_e947b9d7}"
}
```

## 4. 공격자 관점

1. 먼저 UI보다 요청/응답을 봅니다.
2. JSON 구조를 찾은 뒤, 수정 가능한 필드를 분리합니다.
3. Burp Intruder 같은 도구로 작은 정수 범위를 빠르게 탐색합니다.
4. 성공 여부는 status code 뿐 아니라 response length도 함께 봅니다.

## 5. 방어자 관점

- 제출 요청의 구조를 서버에서 엄격하게 검증합니다.
- 단순 회로 검증 엔드포인트는 rate limit과 이상 탐지를 적용합니다.
- 반환 메시지 길이 차이로 오라클이 생기지 않도록 응답을 균일하게 설계합니다.
- 검증 실패와 성공의 상태 차이를 줄입니다.

## 6. 같이 보면 좋은 페이지

- [[parameter-tampering-ctf-patterns]] — 클라이언트 제공 값 변조 패턴
- [[burp-suite]] — 요청 가로채기와 Intruder 사용의 기본 도구
- [[web-ctf-writeup-auth-session]] — 사용자 입력/세션/권한 검증이 얽힌 Web CTF 허브
- 후속 문제 [[pachinko-revisited-final-writeup]] — pwn/rev 분류의 커스텀 CPU 역공학 노트

## 7. 참고 소스

- [Writeup: PicoCTF 2025 — Pachinko](https://medium.com/@divyanshurds.kumar/writeup-picoctf-2025-pachinko-2dcb85b3202f)
- [Pachinko — PicoCTF 2025 Full Walkthrough](https://medium.com/@kofikitiabi/pachinko-picoctf-2025-full-walkthrough-beginner-friendly-91f263c801d2)
- [CTF Day(24). picoCTF Web Exploitation: Pachinko](https://medium.com/@ahmednarmer1/ctf-day-24-0e1e8a56b6f6)
- [How I Solved PicoCTF 2025: Pachinko](https://medium.com/@debasissadhu712/how-i-solved-picoctf-2025-pachinko-web-exploitation-full-step-by-step-walkthrough-9f76f069c52f)
- [picoCTF 2025 Writeups - HackMD](https://hackmd.io/qE2e4hMiQ06HcBaWWWhkuw)

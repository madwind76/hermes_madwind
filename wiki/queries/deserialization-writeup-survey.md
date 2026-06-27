---
title: PHP deserialization writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, deserialization, unserialize, php, object-injection]
sources: [https://ctftime.org/writeup/27159, https://github.com/kevinjycui/picoCTF-2019-writeup]
confidence: high
---

# PHP deserialization writeup survey

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/27159)
- [kevinjycui/picoCTF-2019-writeup](https://github.com/kevinjycui/picoCTF-2019-writeup)


## 1. 목적
PHP `unserialize()` 취약점을 이용한 CTF writeup을 비교해, 객체 주입과 gadget chain 유형을 정리합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Super Serial | cookie-based unserialize | __toString() gadget | login 쿠키를 조작해 access_log 객체의 __toString()을 트리거합니다. |
| Cereal Hacker 1 | cookie-based unserialize | SQLi blended | serialized 객체 내부 값에 SQL injection을 섞어 인증을 우회합니다. |

## 3. 공통 관찰
1. `unserialize()`에 사용자 입력이 들어가면 객체 속성/타입을 공격자가 제어할 수 있습니다.
2. gadget chain은 `__toString()`, `__wakeup()`, `__destruct()` 등 매직 메서드가 핵심입니다.
3. base64 + urlencode 이중 인코딩이 자주 사용됩니다.

## 4. 관련 개념
- [[super-serial-final-writeup]]
- [[cereal-hacker-1-final-writeup]]
- [[web-ctf-writeup-auth-session]]
- [[web-ctf-writeup-family-hub]]

## 5. 다음 읽을 거리
- [[super-serial-final-writeup]]
- [[cereal-hacker-1-final-writeup]]

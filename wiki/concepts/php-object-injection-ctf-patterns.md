---
title: PHP object injection / unsafe deserialization — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, php, deserialization, object-injection, unserialize, cookie]
sources: [https://ctftime.org/writeup/27159, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Super%20Serial/README.md, https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Super_Serial.md]
confidence: high
---

# PHP object injection / unsafe deserialization — CTF patterns

## 1. 정의
**PHP object injection**은 신뢰할 수 없는 입력이 `unserialize()`에 들어가면서, 공격자가 임의의 PHP 객체를 주입하거나 객체의 속성을 바꿀 수 있는 취약점입니다. 보통 `__wakeup()`, `__destruct()`, `__toString()` 같은 magic method와 결합됩니다.

## 2. 왜 위험한가
- 객체 생성 자체가 공격자 제어 하에 놓일 수 있습니다.
- 작은 속성 값 하나로 파일 읽기, SSRF, RCE까지 이어질 수 있습니다.
- 쿠키, 세션, POST 바디에 숨어 있어 눈에 잘 띄지 않습니다.

## 3. 전형적인 흐름
1. `serialize()` / `unserialize()`가 보입니다.
2. 쿠키나 POST 값이 base64, URL encoding으로 한 번 더 감싸져 있습니다.
3. magic method가 있는 클래스가 존재합니다.
4. 예외 처리나 로그 출력이 객체를 문자열로 바꿉니다.
5. gadget chain을 맞추면 파일 읽기 또는 코드 실행으로 이어집니다.

## 4. picoCTF 2021 `Super Serial`에서의 적용
이 문제에서는 `login` 쿠키가 역직렬화되고, 예외 처리에서 객체가 문자열로 출력됩니다. 그 결과 `access_log::__toString()` → `read_log()` → `file_get_contents('../flag')` 체인이 성립합니다.

## 5. 방어 관점
- 사용자 입력에 `unserialize()`를 사용하지 않습니다.
- 허용 클래스 목록을 제한합니다.
- magic method에 파일/네트워크 동작을 넣지 않습니다.
- 예외 메시지에 객체를 포함하지 않습니다.

## 6. 같이 보면 좋은 페이지
- [[super-serial-final-writeup]]
- [[web-ctf-writeup-auth-session]]
- [[cookie-client-storage-ctf-patterns]]

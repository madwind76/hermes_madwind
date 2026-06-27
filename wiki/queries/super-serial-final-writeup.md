---
title: Super Serial — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, php, deserialization, cookie, object-injection, picoctf]
sources: [https://ctftime.org/writeup/27159, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Super%20Serial/README.md, https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Super_Serial.md]
confidence: high
---

# Super Serial — picoCTF 2021 web writeup

> `Super Serial`은 **PHP `unserialize()`가 들어간 로그인 쿠키를 조작해 객체 주입을 유도하고, `__toString()`을 통해 flag 파일을 읽는** picoCTF 2021 Web 문제입니다. 핵심은 **unsafe deserialization**과 **gadget chain**의 기초를 보는 데 있습니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/27159)
- [Original writeup](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Super%20Serial/README.md)
- [Original writeup](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Super_Serial.md)


## 1. 한 줄 요약
- `login` 쿠키는 `urlencode(base64_encode(serialize($perm_res)))` 형태입니다.
- 서버는 이 값을 `unserialize()`해서 권한 객체로 사용합니다.
- 예외 처리에서 객체를 문자열로 출력하는 순간, `__toString()`이 트리거됩니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | `index.phps`와 `cookie.phps`가 노출됨 | 소스 분석 가능 |
| 2 | `login` 쿠키가 `unserialize()`됨 | 객체 주입 가능성 |
| 3 | 예외 시 `$perm`이 문자열로 출력됨 | `__toString()` 트리거 |
| 4 | `access_log` 객체를 만들 수 있음 | `read_log()` 실행 유도 |
| 5 | `../flag`를 읽게 만들 수 있음 | flag 획득 |

## 3. 핵심 분석
### 3.1 취약 지점
```php
# login 쿠키를 역직렬화합니다.
# 예상 결과: 공격자가 임의의 PHP 객체를 주입할 수 있습니다.
$perm = unserialize(base64_decode(urldecode($_COOKIE["login"])));
```

```php
# 예외 처리에서 객체를 문자열로 붙입니다.
# 예상 결과: __toString()이 호출됩니다.
die("Deserialization error. ".$perm);
```

### 3.2 왜 flag가 새나가나
`access_log` 클래스는 `__toString()`에서 `read_log()`를 호출하고, `read_log()`는 내부의 `log_file` 경로를 그대로 `file_get_contents()`로 읽습니다. 즉, 객체의 `log_file`을 `../flag`로 바꾸면 예외 메시지에 flag가 포함됩니다.

## 4. 익스플로잇 절차
1. `index.phps`, `cookie.phps`, `authentication.phps`를 먼저 확인합니다.
2. `access_log` 객체의 직렬화 문자열을 만듭니다.
3. `log_file` 값을 `../flag`로 둡니다.
4. base64 후 URL 인코딩해 `login` 쿠키에 넣습니다.
5. `authentication.php` 요청 시 예외 메시지로 flag를 회수합니다.

```bash
# PHP serialized object를 쿠키로 전송하는 예시입니다.
# 예상 결과: Deserialization error 메시지 안에 flag가 포함됩니다.
curl -s 'http://example.local/authentication.php' \
  --cookie 'login=TzoxMDoiYWNjZXNzX2xvZyI6MTp7czo4OiJsb2dfZmlsZSI7czo3OiIuLi9mbGFnIjt9'
```

## 5. 공격자 관점
- `unserialize()`는 입력 검증보다 훨씬 위험합니다.
- 예외 메시지에 객체를 붙이는 습관은 정보 누출을 부릅니다.
- 작은 gadget 클래스 하나로도 파일 읽기까지 이어질 수 있습니다.

## 6. 방어자 관점
- 사용자 입력에 `unserialize()`를 쓰지 않습니다.
- 반드시 써야 한다면 허용 클래스 목록을 제한합니다.
- 예외 메시지에 객체 전체를 포함하지 않습니다.
- 세션/쿠키에는 서명 검증과 서버측 상태 저장을 사용합니다.

## 7. 같이 보면 좋은 페이지
- [[php-object-injection-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[cookie-client-storage-ctf-patterns]]

## 8. 참고 소스
- [CTFtime — Super Serial](https://ctftime.org/writeup/27159)
- [HHousen — Super Serial README](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Super%20Serial/README.md)
- [Dvd848 — Super Serial](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Super_Serial.md)

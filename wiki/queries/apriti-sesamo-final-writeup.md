---
title: Apriti sesamo — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, research, writeup, php, authentication]
sources: [https://medium.com/@mihasha/apriti-sesamo-picoctf-2025-write-up-7f3d4bfd6085, https://medium.com/@ahmednarmer1/ctf-day-23-595078e28d0f, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/, https://hackmd.io/@fearnot/picoCTF_Web]
confidence: high
---

# Apriti sesamo — picoCTF 2025 web writeup

> PHP 로그인 검증에서 백업 소스 노출과 `sha1()`의 배열 처리 차이를 이용해 `../flag.txt`를 읽는 문제입니다.

## 1. 핵심 요약

- 이 문제는 **숨겨진 백업 파일 노출**과 **PHP 타입 처리**를 동시에 봐야 합니다.
- 개발자 힌트대로 `~`를 붙여 백업 소스를 확인하면, 로그인 로직이 드러납니다.
- 핵심은 SHA-1 충돌이 아니라 `username[]` / `password[]` 같은 **배열 입력**으로 `sha1()`이 `null`을 반환하게 만드는 것입니다.

연결 개념: [[broken-auth]], [[web-ctf-writeup-auth-session]], [[parameter-tampering-ctf-patterns]], [[php-array-input-null-hash-ctf-patterns]]

## 2. 문제 흐름

| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 페이지에서 단순 입력은 실패 | 일반 인증 우회는 막혀 있음 |
| 2 | 페이지 소스/백업 파일을 확인하면 PHP 로직이 보임 | 숨겨진 구현이 핵심 단서 |
| 3 | `username` 과 `password` 를 직접 비교한 뒤 `sha1()` 비교를 수행 | 타입 차이가 공격면이 됨 |
| 4 | 배열 입력을 보내면 `sha1(array)`가 경고 후 `null` 반환 | `null === null` 우회 가능 |
| 5 | 최종적으로 `../flag.txt` 내용을 출력 | flag 획득 |

## 3. 대표 우회 방식

### 3.1 백업 파일 확인
```text
# 페이지 소스에서 백업 파일을 확인하는 발상 예시
/path/to/login.php~
```

### 3.2 배열 입력으로 타입 우회
```text
# PHP가 $_POST를 배열로 받도록 만드는 예시
username[]=123&password[]=456
```

### 3.3 핵심 비교 로직
```php
<?php
# sha1(array) 호출은 경고 후 null 반환 → null === null 이 되어 우회 가능
if (sha1($username) === sha1($password)) {
    echo file_get_contents("../flag.txt");
}
?>
```

## 4. 공격자 관점

1. 먼저 백업 파일이나 주석을 찾아 실제 로직을 확인합니다.
2. `==` 와 `===` 비교가 섞여 있는지 봅니다.
3. 문자열이 아니라 **배열**을 주입해 함수 반환값이 어떻게 변하는지 확인합니다.
4. 해시 충돌을 만들기보다 타입 변화를 노리면 훨씬 쉽습니다.

## 5. 방어자 관점

- `$_POST` 값의 타입을 명시적으로 검증합니다.
- 해시 비교 전에 `is_string()` 같은 타입 검사를 추가합니다.
- 백업 파일(`~`, `.bak`, `.old`) 노출을 막습니다.
- 인증 분기에서 `===`만 믿지 말고 입력 정규화와 검증을 함께 적용합니다.

## 6. 같이 보면 좋은 페이지

- [[broken-auth]] — 인증 체계 결함의 상위 개념
- [[web-ctf-writeup-auth-session]] — 인증/세션/권한 계열 Web CTF 허브
- [[parameter-tampering-ctf-patterns]] — 클라이언트 제공 값 조작 패턴

## 7. 참고 소스

- [Apriti sesamo PicoCTF 2025 Write-up](https://medium.com/@mihasha/apriti-sesamo-picoctf-2025-write-up-7f3d4bfd6085)
- [CTF Day(23). picoCTF Web Exploitation: Apriti sesamo](https://medium.com/@ahmednarmer1/ctf-day-23-595078e28d0f)
- [PicoCTF 2025 - Web Exploitation Writeups](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [picoCTF Web writeup - HackMD](https://hackmd.io/@fearnot/picoCTF_Web)

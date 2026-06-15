---
title: MD5 collision / upload integrity bypass — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, file-upload, md5, hash-collision, integrity]
sources: [https://www.mscs.dal.ca/~selinger/md5collision/, https://ctftime.org/writeup/26974, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/It%20is%20my%20Birthday/README.md]
confidence: high
---

# MD5 collision / upload integrity bypass — CTF patterns

## 1. 정의
**MD5 collision / upload integrity bypass**는 업로드된 두 파일이 서로 다르지만 같은 MD5 해시를 갖는 점을 이용해, 서버의 무결성 검사를 우회하는 패턴입니다. 파일 형식 검사와 해시 검사가 함께 있어도, 알고리즘 자체가 충돌에 약하면 공격자가 검증을 통과할 수 있습니다.

## 2. 왜 중요한가
- MD5는 충돌 저항성이 깨져 있습니다.
- 서버가 `같은 해시 = 같은 파일`이라고 가정하면 위험합니다.
- PDF, 이미지, 압축 파일 등에서 미리 만들어진 충돌 예제가 존재합니다.

## 3. 공격 흐름
1. 서버가 요구하는 파일 형식과 크기 제한을 확인합니다.
2. 같은 해시를 갖는 서로 다른 파일 쌍을 찾습니다.
3. MIME type 또는 확장자 검사를 만족하도록 파일명을 조정합니다.
4. 두 파일을 동시에 업로드합니다.
5. 서버가 `contents1 != contents2`와 `md5_file(...) == md5_file(...)` 같은 조건으로 잘못 판단하는지 확인합니다.

## 4. picoCTF 2021 `It is my Birthday`에서의 적용
이 문제는 두 개의 PDF를 업로드하게 하고, 두 파일이 **서로 달라야 하면서도 MD5는 같아야** 통과됩니다. 결국 사용자는 알려진 충돌 PDF 쌍을 이용해 PHP 검증을 우회하고 `highlight_file("index.php")`로 소스와 flag를 확인합니다.

## 5. 같이 보면 좋은 페이지
- [[it-is-my-birthday-final-writeup]]
- [[web-ctf-writeup-storage-upload]]
- [[file-upload]]

## 6. 방어 관점
- MD5 같은 충돌 취약 해시는 무결성 판단에 사용하지 않습니다.
- 업로드 검증은 해시만 보지 말고 **콘텐츠 재분석**과 **안전한 파서**를 함께 사용합니다.
- 파일 타입 검사는 MIME, 매직 바이트, 실제 파서 결과를 함께 봐야 합니다.

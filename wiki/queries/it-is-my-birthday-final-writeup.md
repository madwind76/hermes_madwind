---
title: It is my Birthday — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, md5, hash-collision, file-upload, integrity, picoctf]
sources: [https://ctftime.org/writeup/26974, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/It%20is%20my%20Birthday/README.md, https://github.com/corkami/collisions]
confidence: high
---

# It is my Birthday — picoCTF 2021 web writeup

> `It is my Birthday`는 **서로 다른 두 PDF 파일이 같은 MD5 해시를 갖도록 만든 뒤 업로드 검증을 통과하는** picoCTF 2021 Web 문제입니다. 핵심은 “같은 해시 = 같은 파일”이라는 잘못된 가정을 깨는 **MD5 collision**입니다.

## 1. 한 줄 요약
- 서버는 두 파일이 **다르면서도** MD5는 같아야 통과시킵니다.
- 파일 크기와 MIME type도 검사합니다.
- 알려진 collision PDF 쌍을 사용하면 조건을 만족할 수 있습니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 두 PDF를 업로드하는 폼이 있음 | 파일 업로드 문제 |
| 2 | 파일 크기 제한 존재 | 필터링 조건 존재 |
| 3 | MIME type이 `application/pdf`여야 함 | 확장자만으로는 부족 |
| 4 | 두 파일 내용이 달라야 함 | 단순 복사로는 실패 |
| 5 | MD5가 같아야 함 | collision이 핵심 |
| 6 | 조건 통과 시 소스와 flag 노출 | 우회 성공 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
MD5는 충돌 저항성이 깨져 있어, 공격자가 서로 다른 두 파일을 같은 해시로 만들 수 있습니다. 서버가 해시만 믿고 무결성을 판단하면 우회가 가능합니다.

### 3.2 실전 확인 포인트
```bash
# 알려진 MD5 collision PDF 쌍을 사용합니다.
# 예상 결과: 두 파일은 다르지만 md5sum 값이 같습니다.
```

```bash
# 업로드 전 MIME type과 크기 제한을 확인합니다.
# 예상 결과: 두 PDF가 모두 조건을 만족해야 합니다.
```

### 3.3 풀이 흐름
1. 문제 설명에서 두 PDF 업로드가 필요함을 확인합니다.
2. 알려진 collision PDF 예제를 준비합니다.
3. 파일명 또는 MIME type이 PDF로 인식되도록 맞춥니다.
4. 두 파일을 동시에 업로드합니다.
5. 서버가 조건을 만족하면 `index.php` 소스가 출력됩니다.
6. 소스 하단의 flag를 확인합니다.

## 4. 공격자 관점
- 해시 검사는 안전해 보이지만, **충돌 저항성이 없으면 인증용으로 부적절**합니다.
- PDF처럼 복잡한 포맷도 collision 예제가 존재하므로, “문서 파일이라 안전하다”는 가정은 위험합니다.
- 업로드 정책은 해시보다 실제 콘텐츠 검증과 안전한 파서 활용이 중요합니다.

## 5. 방어자 관점
- MD5를 무결성/인증 판단에 사용하지 않습니다.
- 파일 업로드는 파일 형식, 콘텐츠, 후처리 경로를 함께 검증합니다.
- 필요하면 강한 해시(SHA-256 이상)와 추가 메타데이터를 사용합니다.

## 6. 같이 보면 좋은 페이지
- [[md5-collision-upload-integrity-bypass-ctf-patterns]]
- [[web-ctf-writeup-storage-upload]]
- [[file-upload]]

## 7. 참고 소스
- [CTFtime — It is my birthday](https://ctftime.org/writeup/26974)
- [HHousen — It is my Birthday README](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/It%20is%20my%20Birthday/README.md)
- [corkami collisions](https://github.com/corkami/collisions)

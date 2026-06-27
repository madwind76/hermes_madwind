---
title: solfire — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn]
sources: [https://github.com/TheJDen/solfire2022, https://raw.githubusercontent.com/TheJDen/solfire2022/master/README.md, https://raw.githubusercontent.com/TheJDen/solfire2022/master/src/lib.rs]
confidence: low
---

# solfire — picoCTF 2022 pwn writeup

## 참고 URL
- [TheJDen/solfire2022](https://github.com/TheJDen/solfire2022)
- [README.md](https://raw.githubusercontent.com/TheJDen/solfire2022/master/README.md)
- [src/lib.rs](https://raw.githubusercontent.com/TheJDen/solfire2022/master/src/lib.rs)

## 핵심 요약
독립 공개 writeup는 아직 찾지 못했고, 현재 확인된 공개 자료는 challenge/source 저장소입니다.
이 저장소의 `src/lib.rs`는 Solana 프로그램 템플릿에 가까운 상태라서, 단독으로는 exploit 흐름을 재구성하기 어렵습니다.
따라서 이 페이지는 challenge 메타데이터와 공개 source 위치를 기록하는 보조 자료로 두는 것이 적절합니다.

## 풀이 메모
1. 독립 writeup를 추가로 검색합니다.
2. 공개 source가 있다면 실제 취약 코드와 solve chain을 분리해 정리합니다.
3. 실질적인 exploit 흐름이 확보되기 전까지는 `low` confidence를 유지합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]

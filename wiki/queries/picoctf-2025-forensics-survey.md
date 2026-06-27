---
title: picoCTF 2025 forensics survey
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/README.md, https://github.com/noamgariani11/picoCTF-2025-Writeup/tree/main/Forensics]
confidence: medium
---

# picoCTF 2025 forensics survey

> 결론부터 말씀드리면, **picoCTF 2025 Forensics 문제는 공개 writeup 기준 6개 확인됩니다.**
> 이번 정리는 도구/아티팩트 유형별로 다시 묶어서 보실 수 있게 만들었습니다.

## 참고 URL
- [picoCTF 2025 Writeup README](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/README.md)
- [picoCTF 2025 Forensics directory](https://github.com/noamgariani11/picoCTF-2025-Writeup/tree/main/Forensics)

## 1. 확인 결과
| Challenge | 분류 | 주요 아티팩트 | 비고 |
| --- | --- | --- | --- |
| Ph4nt0m 1ntrud3r | network forensics | PCAP | base64 세그먼트 재조립 |
| RED | steganography | PNG | zsteg + base64 |
| flags are stepic | steganography | PNG | stepic hidden image |
| Bitlocker-1 | disk forensics | BitLocker dd | bitlocker2john + hashcat |
| Event-Viewing | Windows forensics | EVTX | event ID 기반 로그 분석 |
| Bitlocker-2 | memory forensics | RAM dump | strings / volatility |

## 2. 재분류 기준
1. `Ph4nt0m 1ntrud3r`는 **네트워크 트래픽 분석** 문제입니다.
2. `RED`와 `flags are stepic`는 **이미지 은닉 데이터**를 찾는 문제입니다.
3. `Bitlocker-1`과 `Bitlocker-2`는 **디스크 복호화와 메모리 기반 복구**가 핵심입니다.
4. `Event-Viewing`은 **Windows 이벤트 로그**를 읽고 사건 순서를 복원하는 문제입니다.

## 3. 세부 카테고리
- [[forensics-network-hub]] → Ph4nt0m 1ntrud3r
- [[forensics-stego-hub]] → RED, flags are stepic
- [[forensics-disk-hub]] → Bitlocker-1, Bitlocker-2
- [[forensics-memory-hub]] → Bitlocker-2
- [[forensics-windows-hub]] → Event-Viewing

## 4. 세부 페이지
- [[ph4nt0m-1ntrud3r-final-writeup]]
- [[red-final-writeup]]
- [[flags-are-stepic-final-writeup]]
- [[bitlocker-1-final-writeup]]
- [[event-viewing-final-writeup]]
- [[bitlocker-2-final-writeup]]

## 5. 관련 페이지
- [[picoctf-2025-topic-map]]
- [[picoctf-2025-web-exploitation-survey]]
- [[picoctf-2025-crypto-survey]]
- [[picoctf-2025-forensics-family-hub]]

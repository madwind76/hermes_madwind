---
title: Some Assembly Required 3 — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%203/README.md]
confidence: medium
---

# Some Assembly Required 3 — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%203/README.md)

## 핵심 요약
<http://mercury.picoctf.net:60154/index.html>

## 풀이 메모
1. The new WebAssembly base64 string is as follows: AGFzbQEAAAABEwRgAABgAn9/AX9gAAF/YAJ/fwADBQQAAQIDBAUBcAEBAQUDAQACBjcJfwFBsIoEC38AQbAIC38AQasIC38AQYAIC38AQbAKC38AQYAIC38AQbCKBAt/AEEAC38AQQELB6cBDQZtZW1vcnkCABFfX3dhc21fY2FsbF9jdG9ycwAABnN0cmNtcAABCmNoZWNrX2ZsYWcAAgVpbnB1dAMBCWNvcHlfY2hhcgADA2tleQMCDF9fZHNvX2hhbmRsZQMDCl9fZGF0YV9lbmQDBA1fX2dsb2JhbF9iYXNlAwULX19oZWFwX2Jhc2UDBg1fX21lbW9yeV9iYXNlAwcMX190YWJsZV9iYXNlAwgK2QQEAgAL5wIBKn8jgICAgAAhAkEgIQMgAiADayEEIAQgADYCGCAEIAE2AhQgBCgCGCEFIAQgBTYCECAEKAIUIQYgBCAGNgIMAkADQCAEKAIQIQdBASEIIAcgCGohCSAEIAk2AhAgBy0AACEKIAQgCjoACyAEKAIMIQtBASEMIAsgDGohDSAEIA02AgwgCy0AACEOIAQgDjoACiAELQALIQ9B/wEhECAPIBBxIRECQCARDQAgBC0ACyESQf8BIRMgEiATcSEUIAQtAAohFUH/ASEWIBUgFnEhFyAUIBdrIRggBCAYNgIcDAILIAQtAAshGUH/ASEaIBkgGnEhGyAELQAKIRxB/wEhHSAcIB1xIR4gGyEfIB4hICAfICBGISFBASEiICEgInEhIyAjDQALIAQtAAshJEH/ASElICQgJXEhJiAELQAKISdB/wEhKCAnIChxISkgJiApayEqIAQgKjYCHAsgBCgCHCErICsPC0wBC39BACEAQbCIgIAAIQFBgIiAgAAhAiACIAEQgYCAgAAhAyADIQQgACEFIAQgBUchBkF/IQcgBiAHcyEIQQEhCSAIIAlxIQogCg8LnQEBEX8jgICAgAAhAkEQIQMgAiADayEEIAQgADYCDCAEIAE2AgggBCgCDCEFAkAgBUUNAEEEIQYgBCgCCCEHQQUhCCAHIAhvIQkgBiAJayEKIAotAKuIgIAAIQtBGCEMIAsgDHQhDSANIAx1IQ4gBCgCDCEPIA8gDnMhECAEIBA2AgwLIAQoAgwhESAEKAIIIRIgEiAROgCwiICAAA8LCz0CAEGACAsrnW6TyLK5QYufkIxixcOViDTIk5KIP8GSx9s/yJ7HiTHGxcmLNsbGwJAAAABBqwgLBfGn8Aft
2. Let's decompile it by first converting it to wasm using write_wasm.py in ../Some Assembly Required 2 and then using wasm-decompile. The decompiled c-like code is in wasm-decompile-output.c.
3. We can decompile the compiled wasm to actual c code using wasm2c, which is also included in WebAssembly/wabt. wasm2c (Documentation) creates harder to read long c code that will actually run while wasm-decompile (Documentation) creates easier to read c-style pseudocode.
4. We can use git diff or diffchecker.com to compare the new wasm with the wasm from the previous challenge. We see the addition of a new variable, called key, and some changes at the end of the copy_char.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]

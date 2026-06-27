---
title: Some Assembly Required 2 — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%202/README.md]
confidence: medium
---

# Some Assembly Required 2 — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%202/README.md)

## 핵심 요약
<http://mercury.picoctf.net:53929/index.html>

## 풀이 메모
1. The website is identical to "Some Assembly Required 1", except a slightly different bas64 wasm string is downloaded: AGFzbQEAAAABEwRgAABgAn9/AX9gAAF/YAJ/fwADBQQAAQIDBAUBcAEBAQUDAQACBjEIfwFBsIoEC38AQbAIC38AQYAIC38AQbAKC38AQYAIC38AQbCKBAt/AEEAC38AQQELB6EBDAZtZW1vcnkCABFfX3dhc21fY2FsbF9jdG9ycwAABnN0cmNtcAABCmNoZWNrX2ZsYWcAAgVpbnB1dAMBCWNvcHlfY2hhcgADDF9fZHNvX2hhbmRsZQMCCl9fZGF0YV9lbmQDAw1fX2dsb2JhbF9iYXNlAwQLX19oZWFwX2Jhc2UDBQ1fX21lbW9yeV9iYXNlAwYMX190YWJsZV9iYXNlAwcKogQEAgAL5wIBKn8jgICAgAAhAkEgIQMgAiADayEEIAQgADYCGCAEIAE2AhQgBCgCGCEFIAQgBTYCECAEKAIUIQYgBCAGNgIMAkADQCAEKAIQIQdBASEIIAcgCGohCSAEIAk2AhAgBy0AACEKIAQgCjoACyAEKAIMIQtBASEMIAsgDGohDSAEIA02AgwgCy0AACEOIAQgDjoACiAELQALIQ9B/wEhECAPIBBxIRECQCARDQAgBC0ACyESQf8BIRMgEiATcSEUIAQtAAohFUH/ASEWIBUgFnEhFyAUIBdrIRggBCAYNgIcDAILIAQtAAshGUH/ASEaIBkgGnEhGyAELQAKIRxB/wEhHSAcIB1xIR4gGyEfIB4hICAfICBGISFBASEiICEgInEhIyAjDQALIAQtAAshJEH/ASElICQgJXEhJiAELQAKISdB/wEhKCAnIChxISkgJiApayEqIAQgKjYCHAsgBCgCHCErICsPC0wBC39BACEAQbCIgIAAIQFBgIiAgAAhAiACIAEQgYCAgAAhAyADIQQgACEFIAQgBUchBkF/IQcgBiAHcyEIQQEhCSAIIAlxIQogCg8LZwEJfyOAgICAACECQRAhAyACIANrIQQgBCAANgIMIAQgATYCCCAEKAIMIQUCQCAFRQ0AIAQoAgwhBkEIIQcgBiAHcyEIIAQgCDYCDAsgBCgCDCEJIAQoAgghCiAKIAk6ALCIgIAADwsLMgEAQYAICyt4YWtnS1xOcz5uO2psOTA7OTptam45bTwwbjk6OjA6Ojg4MTwwMD8+dQAA
2. Using write_wasm.py I converted this string to an actual wasm file. I then decompiled it using wasm-decompile from WebAssembly/wabt. The output can be found in wasm-decompile-output.c (note that this is not c code, it is c-like). When compared with the decompiled wasm code for the previous challenge, only these lines are new/changed:
3. I copied the variable content xakgK\Ns>n;jl90;9:mjn9m<0n9::0::881<00?>u (which can be seen from the decoded base64 text) into CyberChef&input=eGFrZ0tcTnM%2BbjtqbDkwOzk6bWpuOW08MG45OjowOjo4ODE8MDA/PnU). I used the magic block to search for picoCTF and sure enough it found the flag. Apparently, the decoding is an xor with 8.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]

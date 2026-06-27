---
title: Some Assembly Required 1 — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%201/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Some%20Assembly%20Required%201/README.md]
confidence: medium
---

# Some Assembly Required 1 — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%201/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Some%20Assembly%20Required%201/README.md)

## 핵심 요약
<http://mercury.picoctf.net:26318/index.html>

## 풀이 메모
1. The website loads an obfuscated javascript file. I spent a lot of time analyzing this file and realized that it performs an HTTP request and downloads the following string: AGFzbQEAAAABEwRgAABgAn9/AX9gAAF/YAJ/fwADBQQAAQIDBAUBcAEBAQUDAQACBjEIfwFBsIoEC38AQbAIC38AQYAIC38AQbAKC38AQYAIC38AQbCKBAt/AEEAC38AQQELB6EBDAZtZW1vcnkCABFfX3dhc21fY2FsbF9jdG9ycwAABnN0cmNtcAABCmNoZWNrX2ZsYWcAAgVpbnB1dAMBCWNvcHlfY2hhcgADDF9fZHNvX2hhbmRsZQMCCl9fZGF0YV9lbmQDAw1fX2dsb2JhbF9iYXNlAwQLX19oZWFwX2Jhc2UDBQ1fX21lbW9yeV9iYXNlAwYMX190YWJsZV9iYXNlAwcK+gMEAgAL5wIBKn8jgICAgAAhAkEgIQMgAiADayEEIAQgADYCGCAEIAE2AhQgBCgCGCEFIAQgBTYCECAEKAIUIQYgBCAGNgIMAkADQCAEKAIQIQdBASEIIAcgCGohCSAEIAk2AhAgBy0AACEKIAQgCjoACyAEKAIMIQtBASEMIAsgDGohDSAEIA02AgwgCy0AACEOIAQgDjoACiAELQALIQ9B/wEhECAPIBBxIRECQCARDQAgBC0ACyESQf8BIRMgEiATcSEUIAQtAAohFUH/ASEWIBUgFnEhFyAUIBdrIRggBCAYNgIcDAILIAQtAAshGUH/ASEaIBkgGnEhGyAELQAKIRxB/wEhHSAcIB1xIR4gGyEfIB4hICAfICBGISFBASEiICEgInEhIyAjDQALIAQtAAshJEH/ASElICQgJXEhJiAELQAKISdB/wEhKCAnIChxISkgJiApayEqIAQgKjYCHAsgBCgCHCErICsPC0wBC39BACEAQbCIgIAAIQFBgIiAgAAhAiACIAEQgYCAgAAhAyADIQQgACEFIAQgBUchBkF/IQcgBiAHcyEIQQEhCSAIIAlxIQogCg8LPwEFfyOAgICAACECQRAhAyACIANrIQQgBCAANgIMIAQgATYCCCAEKAIMIQUgBCgCCCEGIAYgBToAsIiAgAAPCwsyAQBBgAgLK3BpY29DVEZ7ODg1NzQ2MmY5ZTMwZmFhZTRkMDM3ZTVlMjVmZWUxY2V9AAA=.
2. Decoding this string from base64 shows the flag at the end. This string is compiled WebAssembly. I researched decompiling WebAssembly, which can be done with wasm-decompile in WebAssembly/wabt. I also reversed a lot of the JavaScript unnecessarily. This might come in handy for the next challenge in this series.
3. The compiled wasm file can be found at compiled.wasm. This was created using write_wasm.py from ../Some Assembly Required 2.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]

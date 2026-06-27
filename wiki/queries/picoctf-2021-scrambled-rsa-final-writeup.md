---
title: Scrambled: RSA — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Scrambled%3A%20RSA/README.md]
confidence: medium
---

# Scrambled: RSA — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Scrambled%3A%20RSA/README.md)

## 핵심 요약
Hmmm I wonder if you have learned your lesson... Let's see if you understand RSA and how the encryption works. Connect with `nc mercury.picoctf.net 4572`.

## 풀이 메모
1. Connecting to the service outputs some ciphertext, the public modulus, and the exponent:
2. In textbook RSA, a 1 should encrypt to 1. But, when we try encrypting a 1 we get 13589787814203979735997344432080802832776008984701751529073256623683835560426019268055662727723878817162581242623884397426411415725347741008962849580645219519573984615300484601979495080932024787662131004577978449903745252490885056468740446181188019506761784393355054186218263954234491000582090477859332982836.
3. Encrypting some input (aaa) multiple times produces different outputs, which means the algorithm is not deterministic. Strangely, encrypting a multiple times produces the same output. Essentially, the number of possible encrypted outputs is equal to the length of the input text. For example, there is only one character in 1 so there is only one ciphertext while there are three characters in aaa and thus three valid ciphertexts exist.
4. Encrypting aa produces 1358978781420397973599734443208080283277600898470175152907325662368383556042601926805566272772387881716258124262388439742641141572534774100896284958064521951957398461530048460197949508093202478766213100457797844990374525249088505646874044618118801950676178439335505418621826395423449100058209047785933298283673561024996000428515785201807310147438746525988645885310370799314417341170352572980373936820027773998706009446119059121725998847299152732140652261734547503673358211949690790453350635511909487532110430283112659904909965978120113482426195268318329751292020654211499572883335268473019408057847129211754745164317, which is 616 characters long. Let's use E to denote the encryption function and E1(m) to denote the first ciphertext of message m. The E1('a') from before is 308 characters long. This is exactly double which indicates that the encryption algorithm uses some kind of concatenation. Reconnecting and sending a and aa again does not produce ciphertexts where the length is exactly double, but the length of E1('aa') is always close to double that of E1('a').

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]

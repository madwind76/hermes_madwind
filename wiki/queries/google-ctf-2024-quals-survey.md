---
title: Google CTF 2024 — Qualifiers Survey
created: 2026-06-26
updated: 2026-06-26
type: query
tags: [ctf, google-ctf, ctf-challenge, writeup]
sources: [https://github.com/google/google-ctf/tree/main/2024/quals]
confidence: high
---

# Google CTF 2024 — Qualifiers Survey

`google/google-ctf` 공식 repo의 `2024/quals` 디렉터리에 공개된
**35개 챌린지** (메인 30 + 봇 5) 전체 인덱스. 모든 챌린지의
flag와 설명은 공식 `metadata.yaml` 기반.

## 통계

| 카테고리 | 메인 | 봇 |
|----------|------|-----|
| crypto   | 6    | 0  |
| pwn      | 5    | 0  |
| reversing| 7    | 0  |
| web      | 5    | 5  |
| misc     | 7    | 0  |
| **합계** | **30**| **5** |

## crypto (6)

- **Blinders** — [[google-ctf-2024-crypto-blinders]]. flag: `CTF{pr1v4t3_s3t_m3mb3rsh1p_qu3r135_m3d4_m0r3_p0w3rfu1}`. _If you are really efficient at guessing which number is missing from {0, 1, ..., 255}…_
- **desfunctional** — flag: `CTF{y0u_m4y_NOT_g3t_th3_k3y_but_y0u_m4y_NOT_g3t_th3_c1ph3rt3xt_as_w3ll}`. _A newbie friend of mine was trying to implement a secure server for DES encryption…_
- **IDEA** — flag: `CTF{we_have_no_idea_on_related_key_attacks}`. _We have a new idea about a cipher which we think may provide pretty good privacy So bruce for impact as we may patent…_
- **McEliece** — flag: `CTF{1f_0nly_th3r3_w45_50m3_c0d3_1nd1st1ngu15h4bl3_fr0m_r4nd0mn355_70c2decd2dd58446e825}`. _Mceliece cryptosystem was developed in 1978 and has resisted cryptanalysis so far. Lets make allies…_
- **OTP** — flag: `CTF{I_THOUGHT_OTP_WAS_SECURE}`. _I encrypted all my pictures using this fancy cipher. Unfortunately I lost my key, can you help me recover my data?_
- **ZKPOK** — flag: `CTF{wh0_w1l1_b3_us1n9_md5_f0r_h4sh1n9_1n_2024}`. _If you know the flag... you know the flag!_

## pwn (5)

- **Encrypted runner** — flag: `CTF{hmac_w0uld_h4ve_b33n_bett3r}`. _You won't be able to run anything but ls, echo or date, hahahaha!_
- **fasterbox** — flag: `CTF{expl0i1_glob4l_kernel_limi15}`. _fastbox wasn't good enough, so we built fasterbox._
- **heat** — flag: `CTF{mfw_the_sand_is_out_of_the_box}`. _IT'S BOILIN_
- **knife** — flag: `CTF{nonc4nonical_3ncod1ngs_g00d_for_stego_g00d_for_pwn}`. _We made a utility for converting between various encodings. We're afraid it might leak oth…_
- **Unicornel** — flag: `CTF{i_bet_you_hate_assembly_now}`. _I wrote this super cool emulator Above all the others, I'm quite sure it is greater Ther…_

## reversing (7)

- **Arcade** — flag: `CTF{h@cK1ng_r3tr0_gAm32_F0r_fuN}`. _We found a dusty cartridge from an old arcade machine, how can we play it?_
- **Bomberman** — flag: `CTF{NowWriteACPUInIt3727-5479}`. _CTFs are all work and no fun? Time for a quick gaming break :)_
- **IEEE** — flag: `CTF{5ign3d_z3r0_NaNs_and_infiniti3s_rock_but_den0rmal5_4re_meh}`. _I tried reversing it, but no matter what I put, it seems to result in the same thing..._
- **ilovecrackmes** — flag: `CTF{4r17hm371c_w17h0u7_d3ryp7i0n_f7w}`. _We may have created an unbreakable crackme. Seriously, it based on modern public key crypt…_
- **NotObfuscated** — flag: `CTF{I_pr0mize_its_jUsT_mAtriCeS}`. _True story: I had planned on learning to write LLVM passes and use them for obfuscation fo…_
- **Rusty School** — flag: `CTF{I_4m_1nd33d_rUs7y_I_f0rg0t_h0w_t0_d3z1gN_g00d_crYpt0_alg0z}`. _My school asked me to create a new encryption algorithm. ...But I haven't done any crypto…_
- **x86perm** — flag: `CTF{l0oks_l1k3_x86p3rm_pr07ector_i5_n0t_5ecur3}`. _I found this old text adventure in his archives, but the serial key got lost long time ago…_

## web (5)

- **Game Arcade** — [↗](https://game-arcade-web.2024.ctfcompetition.com). flag: `CTF{Bugs_Bugs_Where?_Everywhere!208c92890560773b2fa5b69f69d1a435}`. _Hello Arcane Worrier! Are you ready, to break. the ARCADE. GAME. Note: The challenge does…_
- **Grand Prix Heaven** — [↗](https://grandprixheaven-web.2024.ctfcompetition.com). flag: `CTF{Car_go_FAST_hEART_Go_FASTER!!!}`. _I LOVE F1 ♡ DO YOU LOVE RACING TOO?_
- **in-the-shadows** — [↗](https://in-the-shadows-web.2024.ctfcompetition.com). flag: `CTF{itisquitechallengingtowriteacsssanitizer}`. _Within this digital haunt, your touch may craft an HTML missive, a fleeting connection bet…_
- **Postviewer v3** — [↗](https://postviewer3-web.2024.ctfcompetition.com). flag: `CTF{iframes_are_pretty_dtough!fe050f75c9306d9da3469e131ba9f967}`. _New year new postviewer._
- **sappy** — [↗](https://sappy-web.2024.ctfcompetition.com). flag: `CTF{parsing_urls_is_always_super_tricky}`. _I am a beginner programmer and I share what I learnt about JavaScript with the world! Note: Flag is in the cookie_

## misc (7)

- **auxin2** — flag: `CTF{Sorry__n0_Music_thi5_t1m3}`. _It's only 208 bytes this time, how bad could it really be? Note: The flag is in 'flag'. Th…_
- **Hx8 Teaser 1** — flag: `CTF{1:H4rd_t0_gET_thr0ugh_th3_l3veLs?_sk1LL_Issu3}`. _Hackceler8 2023 was so much fun we added some modifications to the [original game](https:…_
- **Hx8 Teaser 2** — flag: `CTF{2:D1d_yOU_kN0w:Mew's_fUlL_n4mE_I5_BaRth0L0mEW}`. _Hackceler8 2023 was so much fun we added some modifications to the [original game](https:…_
- **hwsim** — flag: `CTF{H4rdwar3_acc3ler4ted_backd00rs_are_7he_w0rst}`. _You are the hardware supplier for G.U.G.L. Can you sneak past the formal verification?_
- **OnlyEcho** — flag: `CTF{LiesDamnedLiesAndBashParsingDifferentials}`. _I like echo because my friends told me it's safe. I made a shell that only allows you to r…_
- **PyStorage** — flag: `CTF{UNIv3rsa1_neWLine_1sNT_S@Fe!?}`. _Just a key-value pair storage in python, how hard can it be?_
- **PyCalc** — flag: `CTF{Ca$4_f0r_d3_C4cH3_Ha5hC1a5h}`. _A safe Python calculator in a non-bypassable sandbox._

## web-bot (5, 메인 web 챌린지의 자동 풀이 봇 트랙)

- **Game Arcade Bot** — metadata.yaml 없음 (flag 미공개)
- **Grand Prix Heaven Bot** — metadata.yaml 없음
- **in-the-shadows Bot** — metadata.yaml 없음
- **Postviewer v3 Bot** — metadata.yaml 없음
- **sappy Bot** — metadata.yaml 없음

> 봇 챌린지는 `metadata.yaml`이 비어있어 flag 미공개 (공식 repo 기준).

## 카테고리 패턴 메모

| 카테고리 | 관찰된 primitive |
|----------|-----------------|
| crypto | 멤버십 테스트, DES 구현 결함, IDEA related-key, McEliece 코드 distinguisher, OTP reuse, ZKP 해시 충돌 |
| pwn | 명령어 화이트리스트 우회, sandbox+kernel limit, sandbox escape, 인코딩 변환기를 통한 leak, Unicorn emulator |
| rev | 옛날 게임 cartridge, 게임 CPU 직접 구현, IEEE-754 NaN/denormal, RSA 기반 crackme, LLVM 패스 (실제 안 씀), Rust crypto 구현 결함, x86 인스트럭션 권한 비트 |
| web | JS sandbox escape, F1 게임 템포 조작, CSS sanitizer 우회, iframe sandbox, URL 파싱 결함 |
| misc | 208-byte ELF/PE, Hackceler8 미니 게임, HW formal verification 우회, bash echo parsing, Python pickle/storage, Python eval sandbox |

## 참고 URL

- 2024 quals 폴더: <https://github.com/google/google-ctf/tree/main/2024/quals>
- raw metadata 예시: <https://raw.githubusercontent.com/google/google-ctf/main/2024/quals/crypto-blinders/metadata.yaml>
- 2024 README: <https://github.com/google/google-ctf/blob/main/2024/README.md>

## 관련 페이지

- [[google-ctf-topic-map]]
- [[google-ctf-quick-summary]]
- [[google-ctf-family-hub]]
- [[google-ctf-2024-crypto-blinders]] (시범 leaf 페이지)

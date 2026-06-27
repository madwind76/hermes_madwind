---
title: Ready Gladiator 2 — picoCTF 2023 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, reverse-engineering]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Reverse%20Engineering/Ready%20Gladiator%202/ReadyGladiator2.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Reverse%20Engineering/Ready%20Gladiator%202]
confidence: medium
---

# Ready Gladiator 2 — picoCTF 2023 reverse engineering writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Reverse%20Engineering/Ready%20Gladiator%202/ReadyGladiator2.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Reverse%20Engineering/Ready%20Gladiator%202)

## 핵심 요약
Can you make a CoreWars warrior that wins every single round? Your opponent is the Imp. The source is available here. If you wanted to pit the Imp against himself, you could download the Imp and connect to the CoreWar...

## 풀이 메모
1. I used this [website](https://corewar.co.uk/) for refrence in trying different warriors. More specifically the [strategy](https://corewar.co.uk/strategy.htm) guide. The Binary Launch Imp was very close to getting 100, in one attempt I was able to get 97 but not quite 100. Since it was so close I tried running a script that tried it 1000 times but it didn't get to 100.
2. Then I went on to try other startegies and eventually came across the [bomber](https://corewar.co.uk/bomber.htm) strategy. The first 3 weren't very good (around 50/60 wins) but the fourth one [Herem/Scimitar](https://corewar.co.uk/heremscimitar.htm) was the one that gave 100 wins instanly no need to try mutliple times.

## 같이 보면 좋은 페이지
- [[picoctf-2023-reverse-engineering-survey]]
- [[picoctf-2023-reverse-engineering-family-hub]]
- [[picoctf-2023-topic-map]]

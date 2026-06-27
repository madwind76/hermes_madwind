---
title: Bithug — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Bithug/README.md]
confidence: medium
---

# Bithug — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Bithug/README.md)

## 핵심 요약
Code management software is way too bloated. Try our new lightweight solution, BitHug. Source: distribution.tgz

## 풀이 메모
1. This web application is using Express.js for the backend and React for the frontend. The package manager is Yarn and Webpack is used to bundle assets. NPM scripts are used to run the various build and serve processes. The entire project can easily be run in a docker container thanks to the included Dockerfile. Essentially, this challenge makes use of the standard set of tools used to build a full-stack application. It is likely a hard challenge due to the number of programs that one must understand to complete it. The goal of the challenge is to get access to the repository at /_/<username>.git because the flag is in the readme file of that repo.
2. The actual website itself is a simple Git server with functionality similar to that of GitHub (the challenge name is "GitHub" with the first and last letters switched). Users can create an account, create a git repository, and then push changes. Additionally, webhooks are supported so a user can post data to an external server on every commit. There is also a feature to give other users access to your repository by editing the access.conf file on the refs/meta/config commit of the repo.
3. Looking at the backend code we see following files:
4. auth-api.ts: Handles authentication from a user-token cookie or authorization header. Alternatively, if the incoming connection is happening over localhost, the user kind attribute is automatically set to admin.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]

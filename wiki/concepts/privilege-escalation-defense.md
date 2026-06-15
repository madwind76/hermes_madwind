---
title: Privilege Escalation — 방어
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, privilege-escalation, local, remote, vertical, horizontal, linux, windows, kernel, exploit]
sources: [https://ko.wikipedia.org/wiki/권한_상승, https://ko.wikipedia.org/wiki/커널_취약점]
confidence: high
---
> [[privilege-escalation]]의 후반부입니다.

## Step 3: 전문 용어 설명 (위키백과/MITRE/업계 표준 기반)
### 권한 상승 후 포스트 익스플로잇 (Post-Exploitation)

| 단계 | 활동 | 도구/기법 |
|------|------|----------|
| **자격증명 수집** | LSASS 덤프, SAM/NTDS.dit, 키체인, 섀도 파일 | Mimikatz, sekurlsa, gsecdump, gsecdump, laZagne |
| **지속성 확보** | 백도어, 예약 작업, 서비스, WMI, 레지스트리, SSH 키 | `schtasks`, `sc create`, `reg add`, `authorized_keys` |
| **수평 이동 (Lateral Movement)** | Pass-the-Hash, Pass-the-Ticket, RDP, SSH, PsExec, WMI, WinRM | `psexec`, `wmiexec`, `smbexec`, `ssh`, `xfreerdp` |
| **데이터 수집/유출** | 파일 탐색, DB 덤프, 이메일, 클라우드 스토리지 | `rclone`, `aws s3`, `scp`, `tar` + `exfil` |
| **증거 은닉** | 로그 삭제, 타임스톰핑, 아티팩트 제거 | `wevtutil cl`, `auditpol`, `timestomp`, `sdelete` |
| **C2 채널 구축** | 리버스 쉘, 바인드 쉘, DNS/HTTP/HTTPS/DNS 터널링 | Cobalt Strike, Sliver, Meterpreter, 맞춤형 임플란트 |

### 권한 상승 탐지 및 방어

| 방어 계층 | 기법 | 구현 예시 |
|----------|------|-----------|
| **OS 강화** | **커널/OS 패치 최신 유지**, 불필요한 서비스 비활성화 | 자동 패치 관리 (WSUS, yum-cron, unattended-upgrades) |
| **최소 권한 원칙** | **관리자 권한 최소 사용**, 일반 계정으로 일상 업무 | 표준 사용자 계정, UAC 최고 단계, `sudo` 감사 |
| **SUID/SGID 최소화** | 불필요한 SUID 바이너리 제거, `find / -perm -4000 -type f` 감사 | `chmod u-s /usr/bin/unnecessary_binary` |
| **Sudo 강화** | `NOPASSWD` 금지, 구체적 명령만 허용, `requiretty`, 로깅 | `Defaults logfile="/var/log/sudo.log"` |
| **커널 보호** | `kernel.yama.ptrace_scope=1`, `kernel.kptr_restrict=2`, `kernel.dmesg_restrict=1` | `/etc/sysctl.d/99-hardening.conf` |
| **AppArmor/SELinux** | 강제 접근 제어(MAC)로 프로세스 격리 | `enforcing` 모드, 커스텀 프로파일 |
| **Windows 강화** | UAC 최고, LSASS 보호(`RunAsPPL`), Credential Guard, LAPS | `reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v RunAsPPL /t REG_DWORD /d 1` |
| **자격증명 보호** | LSASS 보호(PPL), `CredGuard`, `RestrictDelegation`, 패스워드 정책 | `reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v LsaPplConfig /t REG_DWORD /d 1` |
| **모니터링/탐지** | **EDR/EDR**, Sysmon(Event ID 4688, 4672, 4673, 4698, 4704, 4720, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 4734, 4735, 4736, 4737, 4738, 4739, 4739, 4740, 4741, 4742, 4743, 4744, 4745, 4746, 4747, 4748, 4749, 4750, 4751, 4752, 4754, 4755, 4756, 4757, 4758, 4759, 4760, 4756, 4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4766, 4766, 4767, 4768, 4769, 4770, 4771, 4772, 4773, 4774, 4775, 4776, 4777, 4778, 4779, 4780, 4781, 4782, 4783, 4784, 4785, 4786, 4787, 4788, 4789, 4790, 4791, 4792, 4793, 4794, 4794, 4795, 4796, 4797, 4798, 4799, 4800, 4801, 4802, 4803, 4804, 4805, 4806, 4807, 4808, 4809, 4810, 4811, 4812, 4813, 4814, 4815, 4816, 4817, 4818, 4819, 4819, 4820, 4821, 4822, 4823, 4824, 4825, 4826, 4827, 4828, 4829, 4830, 4831, 4832, 4833, 4834, 4835, 4836, 4837, 4838, 4839, 4840, 4841, 4842, 4843, 4844, 4845, 4846, 4847, 4848, 4849, 4850, 4851, 4852, 4853, 4854, 4855, 4856, 4857, 4858, 4859, 4860, 4861, 4862, 4863, 4864, 4865, 4866, 4867, 4869, 4870, 4871, 4872, 4873, 4874, 4875, 4876, 4877, 4878, 4878, 4879, 4880, 4881, 4882, 4883, 4884, 4885, 4886, 4887, 4888, 4889, 4890, 4891, 4891, 4892, 4893, 4894, 4895, 4896, 4897, 4898, 4899, 4900, 4901, 4902, 4903, 4904, 4905, 4906, 4906, 4907, 4908, 4909, 4910, 4911, 4912, 4913, 4914, 4915, 4916, 4917, 4918, 4918, 4919, 4920, 4921, 4922, 4923, 4924, 4924, 4925, 4926, 4927, 4928, 4929, 4930, 4931, 4931, 4932, 4933, 4934, 4935, 4936, 4937, 4939 | Sysmon, Windows Event Log, Auditd, Falco, Wazuh, OSSEC |
| **파일 무결성** | 중요 바이너리/설정 파일 해시 모니터링 | AIDE, Tripwire, Samhain, Wazuh FIM |
| **최소 권한/제로 트러스트** | JIT(Just-in-Time) 관리자 접근, PAM, PIM | Azure PIM, CyberArk, BeyondTrust, HashiCorp Vault |

### 주요 권한 상승 사고 사례

| 사고 | 연도 | 기법 | 피해 |
|------|------|------|------|
| **Stuxnet** | 2010 | 제로데이 4개 + 권한 상승 (LNK, 프린트 스풀러) | 이란 핵시설 원심분리기 파괴 |
| **WannaCry** | 2017 | EternalBlue (SMBv1 RCE) + DoublePulsar (커널 권한 상승) | 전 세계 20만+ 시스템 감염 |
| **NotPetya** | 2017 | EternalBlue + Mimikatz(자격증명 탈취) + PsExec/WMIC 수평 이동 | 전 세계 100억 달러+ 피해 |
| **PrintNightmare** | 2021 | CVE-2021-34527 (프린트 스풀러 RCE → SYSTEM) | 전 세계 윈도우 서버 긴급 패치 |
| **ZeroLogon** | 2020 | CVE-2020-1472 (Netlogon) → 도메인 컨트롤러 완전 장악 | 다수 조직 도메인 컨트롤러 장악 |
| **Log4Shell** | 2021 | CVE-2021-44228 (Log4j JNDI) → RCE + 권한 상승 | 전 세계 광범위 영향 |
| **Dirty Pipe** | 2022 | CVE-2022-0847 (Linux 커널) → 루트 권한 상승 | 리눅스 서버 광범위 영향 |
| **PwnKit (pkexec)** | 2021 | CVE-2021-4034 (polkit pkexec) → 로컬 루트 권한 상승 | 주요 리눅스 배포판 전체 영향 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **MITRE ATT&CK TA0004** | Privilege Escalation 전술/기법 매트릭스 |
| **MITRE ATT&CK T1068** | Exploitation for Privilege Escalation |
| **CWE-269** | Improper Privilege Management |
| **CWE-250** | Execution with Unnecessary Privileges |
| **NIST SP 800-53 AC-6** | Least Privilege |
| **NIST SP 800-53 AC-5** | Separation of Duties |
| **Microsoft Privilege Escalation Guide** | 윈도우 권한 상승 완전 가이드 |
| **Linux Privilege Escalation (GTFOBins/HackTricks)** | 리눅스 권한 상승 치트시트 |

---


## 관련 위키 링크
- [[cve-2026-23111-nftables-uaf]] — CVE-2026-23111 (Linux nf_tables UAF LPE) — 최신 커널 권한 상승 취약점

- [[broken-access-control]] — Broken Access Control (권한 상승의 전제 조건)
- [[idor]] — IDOR (수평 권한 상승의 대표 사례)
- [[command-injection]] — Command Injection (RCE → 권한 상승 체인)
- [[file-upload]] — File Upload (웹쉘 업로드 → 권한 상승)
- [[exploitation]] — 익스플로잇 (취약점 익스플로잇으로 권한 상승)
- [[real-world-breach-cases]] — 실제 침해 사례 (WannaCry, NotPetya, PrintNightmare 등)
- [[rce]] — RCE (원격 코드 실행 → 권한 상승 체인)

---

## 참고 문헌

- 한국어 위키백과: [권한 상승](https://ko.wikipedia.org/wiki/권한_상승)
- MITRE ATT&CK: [Privilege Escalation (TA0004)](https://attack.mitre.org/tactics/TA0004/)
- GTFOBins: [Linux Privilege Escalation](https://gtfobins.github.io/)
- HackTricks: [Linux/Windows Privilege Escalation](https://book.hacktricks.xyz/)
- Microsoft: [Privilege Escalation in Windows](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-privilege-escalation)
- Linux Kernel Exploits: <https://www.kernel.org/doc/html/latest/admin-guide/kernel-hacking.html>
## 관련 위키 링크
- [[privilege-escalation]] — 인덱스 페이지
- [[privilege-escalation-core]] — 분할 페이지
- [[rce]]

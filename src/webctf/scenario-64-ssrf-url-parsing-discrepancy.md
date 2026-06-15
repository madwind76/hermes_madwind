---
title: SSRF via URL Parsing Discrepancy — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssrf, url-parsing, parser-discrepancy, bypass, rfc3986]
confidence: high
---

# SSRF via URL Parsing Discrepancy — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: URL Link Archiver (웹 링크 수집 및 아카이브)
- **난이도**: High
- **핵심 컨셉**: 동일한 URL 문자열 규격을 두고 이종 라이브러리/프로그래밍 언어의 내장 파서가 각자 다르게 해석하는 허점을 공략하는 **URL 파서 일관성 결여(Parser Discrepancy) 기반 SSRF** 우회 취약점 문제입니다. 대상 애플리케이션은 사용자가 입력한 웹페이지 주소를 방문해 스냅샷을 만들어 줍니다. 내부적인 보안 통제를 위해, 입력받은 주소 도메인이 신뢰할 수 있는 도메인 리스트(`*.safedomain.local`)에 속하는지 파이썬의 `urllib.parse` 함수로 선제 유효성 검사를 수행합니다. 하지만 유효성 검사 통과 후 실제 아웃바운드 HTTP 요청을 날리는 도구는 `cURL` 바이너리를 쉘 명령어로 기동하여 실행합니다. 공격자는 특정 구분 문자(`@`, `#`, `;`) 처리에 관한 두 파서의 상이한 매핑 패턴을 이용해 검증 시에는 안전한 도메인으로 파싱되지만 실제 요청은 내부망 루프백(`127.0.0.1`)으로 흘러가게 만들어 내부 데이터를 유출합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Snapshot Generator API (`/api/snapshot`)**:
  - 사용자로부터 URL 파라미터(`?url=...`)를 수신.
  - **검증 단**: 파이썬의 `urllib.parse.urlparse`를 이용해 `netloc`이 `*.safedomain.local` 도메인이 맞는지 검사하여 화이트리스트 필터링 수행.
  - **수행 단**: `curl -s [USER_URL]` 형태로 쉘 커맨드 또는 cURL 연동 모듈을 호출해 원격 데이터를 다운로드 후 반환.
- **Flag 위치**:
  - 오직 내부 사설 대역에서만 접근할 수 있는 내부 관리자 페이지 `http://127.0.0.1:8000/admin/flag`에 탑재되어 있습니다.

### 2.2 취약점 지점
1. **Discrepancy in Authority/UserInfo Parsing (RFC3986 해석 비대칭성)**:
   - URL 규격 중 `http://[UserInfo]@[Authority]/` 에서 `@` 기호는 사용자 인증 정보와 타겟 호스트를 분리하는 경계입니다.
   - 만약 URL 중간에 백슬래시(`/`)나 다른 기호가 엮여 있을 때:
     - **Python `urllib`**: `@` 문자 위치 분석 시 뒤의 문자나 슬래시를 우선하여 `@` 앞을 Host로 잘못 매핑하거나 특정 도메인을 Authority로 잘못 인식하게 유도할 수 있습니다.
     - **`cURL`**: 표준 RFC 명세에 따라 뒤쪽의 오리지널 호스트로 해석해 실 통신을 시도합니다.
     - 예: `http://127.0.0.1:8000#@safedomain.local` 또는 `http://safedomain.local:80@127.0.0.1:8000/`

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 우회 대상 필터 | 목표 |
|------------|--------|------|----------|----------------|------|
| `/api/snapshot` | GET | 불필요 | `url` | `urllib` 기반 `*.safedomain.local` 매칭 검사 | `curl` 호출 시 `127.0.0.1:8000` 강제 조회 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. URL 검증 및 통신 라이브러리 쌍 파악
1. 정상적인 safe 도메인인 `http://safedomain.local/`을 전송하여 스냅샷이 반환되는 것을 관찰합니다.
2. 외부 임의 IP 주소를 입력하면 `"Access Denied: Only safedomain.local is allowed"` 에러 응답을 획득합니다.
3. 에러 로그나 API 동작 양상 상, 검증 시에는 Python 계열의 파서가 동작하고 수집 백그라운드는 cURL 바이너리 등이 활용되고 있음을 유추합니다.

### Step 2. 파서 간 Authority 매칭 Discrepancy 페이로드 합성
두 파서의 파싱 우선순위 불일치를 유도할 특수 문자들의 조합을 테스트합니다.
- **테스트 케이스**:
  `http://safedomain.local@127.0.0.1:8000/admin/flag`
  - Python `urllib`: Host를 `safedomain.local`로 오인하여 통과.
  - cURL: `@` 뒤의 실제 호스트인 `127.0.0.1:8000`으로 접속 시도.
- **백슬래시(`/`) 결합 우회 패턴**:
  `http://safedomain.local:80@127.0.0.1:8000/admin/flag`
  서버가 보다 철저히 `safe.com`이 호스트 이름 문자열의 끝부분에 위치하는지 검사하는 경우(`endswith`), 백슬래시와 유저 정보를 결합한 특수 주소 규격을 사용합니다:
  `http://127.0.0.1:8000/admin/flag#@safedomain.local`
  - Python `urllib`는 `#` 이후를 프래그먼트로 무시하지 않고 끝의 `@safedomain.local` 부분 때문에 호스트를 `safedomain.local`로 매칭 판독합니다.
  - cURL은 `#` 기호를 표준 프래그먼트로 처리하여 무시하고, 앞의 `127.0.0.1:8000`을 타겟 호스트로 삼아 연결합니다.

### Step 3. 우회 요청 전송
1. 공격자는 합성 완료한 URL 페이로드를 전달합니다.
   - **요청 쿼리**:
     `/api/snapshot?url=http://127.0.0.1:8000/admin/flag%23@safedomain.local`
2. 파이썬 백엔드 검증 필터는 호스트 값을 `safedomain.local`로 디코딩하여 검증에 성공한 것으로 판정하고 허용합니다.

### Step 4. flag 획득
1. 백엔드는 검증을 넘긴 `url` 문자열 그대로 시스템 cURL 명령 인자로 할당하여 명령을 처리합니다.
   `curl -s "http://127.0.0.1:8000/admin/flag#@safedomain.local"`
2. cURL은 프래그먼트인 `#@safedomain.local` 부분을 잘라내고 사설 대역의 로컬 서버 `127.0.0.1:8000/admin/flag`로 실 통신을 수행하여 응답 데이터를 가져옵니다.
3. 공격자는 웹 화면에 스냅샷 결과물로 노출된 로컬 페이지 응답 속에서 플래그(`FLAG{url_parser_discrepancy_urllib_vs_curl_ssrf}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py (취약한 파서 연동 Flask 백엔드 서버 예시)
import subprocess
from urllib.parse import urlparse
from flask import Flask, request, jsonify

app = Flask(__name__)

# 화이트리스트 도메인
ALLOWED_DOMAIN = "safedomain.local"

def verify_url(url):
    try:
        # 취약점 지점 1: urllib.parse.urlparse를 사용하여 호스트명 검증
        # 특정 특수문자(#, @)가 섞여 있을 때 호스트 파싱 결과가 실제 HTTP 클라이언트와 불일치함
        parsed = urlparse(url)
        hostname = parsed.hostname
        
        if hostname and (hostname == ALLOWED_DOMAIN or hostname.endswith("." + ALLOWED_DOMAIN)):
            return True
        return False
    except Exception:
        return False

@app.route('/api/snapshot', methods=['GET'])
def get_snapshot():
    target_url = request.args.get('url', '')

    if not verify_url(target_url):
        return jsonify({"status": "error", "message": "Access Denied: Untrusted domain"}), 403

    # 취약점 지점 2: 검증에 통과한 URL 문자열 날것 그대로 cURL 바이너리 인자로 할당하여 요청 수행
    # cURL은 urllib와 다른 독자적인 URL 파서를 사용하여 실 접속 대상 IP를 127.0.0.1로 해석함
    cmd = ["curl", "-s", target_url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return jsonify({"status": "success", "content": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **동일 파서 일원화 (Use Identical Parser)**:
   - 유효성 검사 시점과 실제 데이터 수집 시점에 동작하는 URL 파서 라이브러리를 완전 동일한 모듈(예: Python `requests` 패키지 내부에서 파싱과 HTTP 송신을 동시에 처리)로 일치시켜 파서 간 해석 격차를 근원적으로 제거합니다.
2. **사설 IP 대역 아웃바운드 엄격 차단 (IP-Level Firewall Restrictions)**:
   - 도메인 검증에만 의존하지 않고, URL 확인 후 내부 DNS 질의(Resolve)를 통해 추출된 IP 주소가 사설/루프백 대역(`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/12`)에 해당하는 경우 즉각 커넥션을 끊도록 소켓 레이어에서 방어합니다.
3. **엄격한 문자열 필터링**:
   - 도메인 검증 전, URL 내부에 표준 구조 외에 오해를 일으킬 수 있는 백슬래시(`\`), 샤프(`#`), 골뱅이(`@`), 세미콜론(`;`) 같은 제어 기호가 포함되어 있는지 확인하고 기각합니다.

---
title: CORS Misconfiguration — 방어
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, web, cors, misconfiguration, same-origin-policy, cross-origin, owasp, api-security]
sources: [https://ko.wikipedia.org/wiki/교차_출처_리소스_공유, https://ko.wikipedia.org/wiki/동일_출처_정책, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---
> [[cors-misconfig]]의 후반부입니다.

# CORS Misconfiguration — 방어

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/교차_출처_리소스_공유)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/동일_출처_정책)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/OWASP)

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### 안전한 CORS 구현 패턴

```python
# Python (Flask/FastAPI) - 안전한 CORS 미들웨어 예시
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

# ✅ 안전한 설정: 구체적 출처만 허용, Credentials 신중히
ALLOWED_ORIGINS = [
    'https://app.example.com',
    'https://admin.example.com',
    'https://partner.example.com'
]

CORS(app, 
     origins=ALLOWED_ORIGINS,
     supports_credentials=True,  # Credentials 허용 시 Origin 구체적 필수
     allow_headers=['Authorization', 'Content-Type', 'X-CSRF-Token'],
     methods=['GET', 'POST', 'PUT', 'DELETE'],
     max_age=600  # 10분 캐시
)

# ✅ 동적 Origin 검증 (서브도메인 와일드카드 구현 시)
@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin and is_allowed_origin(origin):  # 화이트리스트/정규식 검증
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Vary'] = 'Origin'  # 캐시 키에 Origin 포함
    return response

def is_allowed_origin(origin: str) -> bool:
    """정확한 매칭 또는 안전한 서브도메인 검증"""
    if origin in ALLOWED_ORIGINS:
        return True
    # 서브도메인 허용 시: 정확한 접미사 매칭 + 공개 접미사 리스트 확인
    # 예: origin.endswith('.example.com') AND public_suffix_list 검증
    return False
```

```javascript
// Node.js (Express) - 안전한 CORS 설정
const cors = require('cors');

const corsOptions = {
  origin: function (origin, callback) {
    // origin이 undefined면 같은 출처 요청 → 허용
    if (!origin) return callback(null, true);
    
    const allowed = [
      'https://app.example.com',
      'https://admin.example.com'
    ];
    
    if (allowed.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,  // 쿠키/인증 헤더 허용 시 origin 구체적 필수
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Authorization', 'Content-Type', 'X-CSRF-Token'],
  maxAge: 600
};

app.use(cors(corsOptions));
```

### CORS 관련 보안 테스트 도구

| 도구 | 용도 |
|------|------|
| **curl** | `curl -H "Origin: https://evil.com" -H "Access-Control-Request-Method: PUT" -X OPTIONS https://api.example.com/resource` |
| **Postman/Insomnia** | Preflight 요청 자동 생성, 헤더 검증 |
| **Burp Suite** | CORS 스캐너, Origin 조작 반복기 |
| **CORS Misconfiguration Scanner** | 자동화된 CORS 취약점 스캔 |
| **browser-devtools** | Network 탭 → CORS 헤더 확인, Preflight 확인 |
| **cors-scanner** | 자동화된 CORS 설정 오류 스캔 |

### 주요 CORS Misconfiguration 사고 사례

| 사고 | 연도 | 설정 오류 | 피해 |
|------|------|-----------|------|
| **Facebook** | 2015 | `Access-Control-Allow-Origin: *` + `Allow-Credentials: true` | 사용자 데이터 유출 가능성 |
| ** 여러 API 제공업체** | 지속적 | Origin 검증 없이 요청 Origin 그대로 반영 | 사용자 데이터/토큰 유출 |
| **서브도메인 탈취 + CORS** | 지속적 | `*.example.com` 허용 + 서브도메인 탈취 | 전체 API 권한 탈취 |
| **Null Origin 허용** | 2018~ | `Allow-Origin: null` 허용 | 로컬 HTML/샌드박스에서 인증된 API 접근 |

### CORS vs CSRF vs XSS 비교

| 구분 | **CORS Misconfig** | **CSRF** | **XSS** |
|------|-------------------|----------|---------|
| **핵심 원인** | SOP 예외(CORS) 설정 오류 | 인증된 요청 위조 (Origin 검증 안 함) | 스크립트 주입 (출력 이스케이프 실패) |
| **공격 주체** | 악의적 사이트 (`evil.com`) | 악의적 사이트 (`evil.com`) | 공격자 스크립트 (피해자 브라우저에서 실행) |
| **브라우저 동작** | CORS 헤더 보고 **응답 읽기 허용** | 쿠키 자동 포함 요청 **전송만** (응답 못 읽음) | 악성 스크립트 **실행** (DOM 접근, 쿠키 탈취) |
| **응답 읽기** | **가능** (CORS 헤더 허용 시) | **불가능** (SOP 차단) | **가능** (같은 출처 컨텍스트) |
| **Credencials** | `Allow-Credentials: true` 필수 | 쿠키 자동 포함 | 쿠키 접근 가능 (`document.cookie`) |
| **방어 핵심** | Origin 화이트리스트, Credentials 신중 | CSRF 토큰, SameSite 쿠키, Origin/Referer 검증 | 출력 이스케이프, CSP, HttpOnly 쿠키 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **MDN CORS** | CORS 동작 원리, 헤더 상세 설명 |
| **OWASP CORS** | CORS 설정 오류 공격/방어 가이드 |
| **W3C CORS Spec** | CORS 표준 명세 |
| **RFC 6454** | 동일 출처 정책(SOP) 정의 |
| **CWE-942** | Overly Permissive Cross-domain Whitelist |

---


## 관련 위키 링크

- [[csrf]] — CSRF (CORS 설정 오류로 CSRF 방어 무력화 가능)
- [[xss]] — XSS (CORS 헤더로 민감 헤더 유출 시 XSS 결합)
- [[ssti]] — SSTI (CORS로 템플릿 엔진 API 접근)
- [[api-security]] — API 보안 (CORS는 API 보안의 핵심)
- [[real-world-breach-cases]] — 실제 침해 사례 (Facebook, API 제공업체 등 사례)
- [[exploitation]] — 익스플로잇 (CORS 설정 오류 → 인증된 API 탈취)

---

## 참고 문헌

- 한국어 위키백과: [교차 출처 리소스 공유](https://ko.wikipedia.org/wiki/교차_출처_리소스_공유)
- MDN Web Docs: [CORS (Cross-Origin Resource Sharing)](https://developer.mozilla.org/ko/docs/Web/HTTP/CORS)
- OWASP: [CORS Misconfiguration](https://owasp.org/www-community/attacks/CORS_Misconfiguration)
- PortSwigger: [CORS (Cross-Origin Resource Sharing)](https://portswigger.net/web-security/cors)
- W3C: [Cross-Origin Resource Sharing (CORS)](https://www.w3.org/TR/cors/)
## 관련 위키 링크
- [[cors-misconfig]] — 인덱스 페이지
- [[cors-misconfig-core]] — 분할 페이지
- [[rce]]

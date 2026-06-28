---
title: 컨테이너 내부의 비밀 레이어 (Docker Layer Secrets)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, docker, container, layer, tar]
confidence: high
---

# 컨테이너 내부의 비밀 레이어 (Docker Layer Secrets)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 컨테이너 보안 및 침해 사고 조사 (Docker 레이어 복구 실무)

## 1. 배경 시나리오
사내 클라우드 인프라에 배포되었던 웹 서비스 컨테이너의 베이스 이미지가 노출되는 사고가 있었습니다. 개발자는 빌드 과정 도중 실수로 관리자 API 키가 들어 있는 `key.txt` 파일을 이미지 내부에 복사(`COPY`)했다가, 뒤늦게 이를 인지하고 다음 빌드 스크립트 명령어에서 해당 파일을 삭제(`RUN rm /app/key.txt`)한 뒤 배포했다고 설명했습니다. 그러나 공격자는 공개된 도커 이미지 파일 `app_image.tar`에서 삭제되었다는 기밀 데이터를 완벽하게 복원하여 무단 접속 권한을 획득했습니다. 도커 레이어 구조를 분석해 누출된 플래그를 찾아야 합니다.

## 2. 제공 파일
* `app_image.tar` (`docker save` 명령어로 내보낸 도커 웹 애플리케이션 이미지 아카이브 파일, 약 80MB)

## 3. 문제 목표
도커 유니온 파일시스템(UnionFS)의 쓰기 시 복사(Copy-on-Write) 및 레이어 이미지 적층 동작 방식을 파악하고, 내보낸 이미지 타르볼 내부의 개별 레이어 아카이브 파일들을 순차적으로 역추적하여 최종 배포본에서 가려진(삭제된) 이전 시점의 원본 파일을 복구합니다.

## 4. 의도한 풀이 흐름
1. **아카이브 압축 해제**:
   * 제공된 도커 이미지 아카이브 파일을 디렉터리를 생성하여 압축 해제합니다.
     `mkdir extracted_image && tar -xf app_image.tar -C extracted_image`
2. **도커 이미지 메타데이터 분석**:
   * `manifest.json` 파일을 열어 어떤 레이어들(Layers)이 순서대로 적층되어 이미지 형상을 이루는지 확인합니다.
   * 예: 메타데이터에 등록된 레이어 해시값 목록(`d140b923.../layer.tar` 등)의 연결 구조를 파악합니다.
3. **레이어별 파일 검색**:
   * 각 레이어 디렉터리 내부에 존재하는 물리 파일 시스템 아카이브인 `layer.tar` 파일 목록을 훑습니다.
   * `find`와 `tar` 명령어를 조합하여 삭제된 파일인 `key.txt`가 들어 있는 과거 레이어를 추적합니다:
     ```bash
     find extracted_image/ -name "layer.tar" | while read layer; do
         echo "Checking $layer..."
         tar -tf "$layer" | grep "key.txt"
     done
     ```
   * 검색 결과 특정 레이어 아카이브(예: `8f3d1b.../layer.tar`) 내부에 `app/key.txt` 파일이 여전히 압축 보존되어 존재함을 발견합니다.
     *(후속 레이어의 `layer.tar`에는 해당 파일이 화이트아웃(`.wh.key.txt`) 파일로 표기되어 뷰에서만 삭제 처리되었음을 보여줍니다)*
4. **기밀 파일 추출**:
   * 해당 타깃 레이어 파일에서 특정 파일만 지정해 압축을 해제합니다.
     `tar -xf extracted_image/8f3d1b.../layer.tar app/key.txt`
5. **플래그 확인**: 복구한 `app/key.txt` 내용을 읽어 기밀 플래그를 획득합니다.
   (최종 플래그: `picoCTF{docker_layers_are_immutable_history}`)

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{docker_layers_are_immutable_history}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 다음 예시 구조의 `Dockerfile`을 작성합니다:
     ```dockerfile
     FROM alpine:latest
     WORKDIR /app
     # 레이어 1: 기밀 파일 복사 (과거 흔적에 기록됨)
     COPY key.txt /app/key.txt
     # 레이어 2: 텍스트 삭제 및 컴파일 진행 (파일이 사용자 뷰에서 가려짐)
     RUN rm /app/key.txt && echo "Build Success" > build.log
     ```
  2. 플래그가 담긴 `key.txt`를 생성하고 도커 이미지를 빌드합니다:
     `docker build -t vulnerable-app:latest .`
  3. 빌드된 이미지를 tar 파일로 아카이브 저장합니다:
     `docker save vulnerable-app:latest -o app_image.tar`
  4. 생성된 `app_image.tar`를 배포 파일로 삼아 출제합니다.
* **출제 포인트**: 
  * 컨테이너 환경의 불변성(Immutability) 정책과 레이어 캐싱 원리를 포렌식 관점에서 분석하는 역량을 육성합니다. `RUN rm` 명령어는 데이터의 물리 삭제가 아니라 상위 레이어에 **화이트아웃(Whiteout)** 메타데이터를 추가해 마스킹 처리할 뿐이라는 취약성을 입증합니다.

## 7. 트러블슈팅 및 힌트
* **Q. manifest.json의 레이어 해시 디렉터리들이 너무 많아 헷갈립니다.**
  * A. 도커 이미지를 분석할 때 오픈소스 도구인 **Dive**(`dive <image_tag>`)를 활용하면 레이어별 파일 시스템 추가/수정/삭제 현황을 GUI 형태로 훨씬 직관적으로 파악하고 특정 파일을 역추적할 수 있습니다.
* **Q. 특정 레이어에서 .wh.key.txt 라는 이상한 파일이 보입니다.**
  * A. 접두사 `.wh.`가 붙은 파일은 도커의 화이트아웃(Whiteout) 지시자로, 이전 레이어에 실재하는 파일을 상위 레이어 뷰에서 '삭제' 처리했음을 명시해 주는 시스템 지시어입니다. 즉, 이 지시어가 속하지 않은 그 직전의 이전 레이어로 내려가면 원본 파일이 고스란히 남아 있습니다.

## 8. 학습 포인트
* **유니온 파일시스템(UnionFS) 구조**: 여러 개의 읽기 전용 레이어와 최상위 쓰기 가능 레이어가 겹쳐 단일 뷰를 형성하는 도커의 스토리지 드라이버 메커니즘을 심층 학습합니다.
* **클라우드 보안 코딩**: 개발/CI-CD 과정에서 민감한 설정 정보(API Key, DB 패스워드 등)를 Dockerfile 빌드 스크립트 내부에서 복사하거나 파라미터로 지정할 때 발생하는 흔적 누출 보안 위협을 실증적으로 파악합니다.

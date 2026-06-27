---
title: Firecrawl 셀프호스팅 셋업 및 Hermes 연동
tags: [firecrawl, self-host, docker, hermes, web-search, web-extract]
category: devops/infra
sources:
  - /home/kisec/.hermes/profiles/ctf/home/firecrawl/docker-compose.yaml
  - /home/kisec/.hermes/profiles/ctf/home/firecrawl/.env
  - /home/kisec/.hermes/profiles/ctf/skills/devops/firecrawl-selfhost.md
  - /home/kisec/.hermes/profiles/news/.env
  - /home/kisec/.hermes/profiles/news/config.yaml
  - /home/kisec/.hermes/profiles/ctf/hermes-agent/plugins/web/firecrawl/plugin.yaml
updated: 2026-06-27
---

# Firecrawl 셀프호스팅 셋업 및 Hermes 연동 가이드

Hermes의 `web_search` / `web_extract` 백엔드를 외부 SaaS 없이 자체 서버에서 운영하기 위한 end-to-end 문서.  
2026-06-27 기준 현재 시스템에 적용되어 있는 실제 구성(컨테이너 6개 가동, /v1/scrape 정상 응답 확인)을 기준으로 작성.

## 1. 한눈에 보기

| 항목 | 값 |
|---|---|
| 운영 디렉터리 | `/home/kisec/.hermes/profiles/ctf/home/firecrawl/` |
| Compose 프로젝트명 | `firecrawl` |
| API 엔드포인트 | `http://localhost:3002` |
| Hermes 설정 위치 | `news` 프로필 (`~/.hermes/profiles/news/.env`, `config.yaml`) |
| 공유 프로필 | `ctf` 프로필의 compose 스택을 news 프로필이 URL로 함께 사용 |
| 사용 플러그인 | `web-firecrawl`, `browser-firecrawl` |
| 가동 컨테이너 | api, playwright-service, redis, rabbitmq, nuq-postgres, foundationdb (foundationdb-init은 초기화 후 정상 종료) |

## 2. 디렉터리 구조

```
~/.hermes/profiles/ctf/home/firecrawl/
├── docker-compose.yaml   # 6개 서비스 정의 (api, playwright-service, redis, rabbitmq, nuq-postgres, foundationdb, foundationdb-init)
└── .env                  # Firecrawl 환경변수 (자격증명, DB 비번, 큐 키 등)

~/.hermes/profiles/news/
├── .env                  # FIRECRAWL_API_URL=http://localhost:3002 (API 키는 주석 처리)
└── config.yaml           # web.backend: firecrawl

~/.hermes/profiles/ctf/hermes-agent/plugins/
├── web/firecrawl/plugin.yaml       # Hermes web_search 백엔드
└── browser/firecrawl/              # Hermes 브라우저 백엔드
```

news 프로필은 compose 스택을 직접 소유하지 않고, ctf 프로필의 스택을 `http://localhost:3002`로 호출하는 **공유 소비자** 구조.

## 3. 시스템 요구사항

### 3.1 실측 리소스 (7.6GB RAM / 4 CPU 서버 기준)

| 컴포넌트 | 이미지 크기 | 실 메모리 사용 |
|---|---|---|
| `ghcr.io/firecrawl/firecrawl` (api) | 1.5GB | 2.7GB |
| `ghcr.io/firecrawl/playwright-service` | 2GB | ~1GB |
| `ghcr.io/firecrawl/nuq-postgres` | 640MB | ~300MB |
| `rabbitmq:3-management` | 400MB | ~200MB |
| `redis:alpine` | 155MB | ~50MB |
| `foundationdb/foundationdb:7.3.63` | 1.5GB | ~300MB |
| 합계 (idle) | 6GB+ | 5~6GB |

12GB 이상 권장. 7.6GB 환경에서는 다른 무거운 서비스와 동시 운영 금지.

### 3.2 compose가 강제하는 리소스 한도 (docker-compose.yaml 기준)

| 서비스 | cpus | mem_limit |
|---|---|---|
| api | 1.5 | 3G |
| playwright-service | 1.0 | 2G |

공식 compose는 api 8G + playwright 4G를 요구하므로, 저사양 환경에서는 위처럼 축소해야 함.

## 4. 셋업 절차

### 4.1 작업 디렉터리 준비

```bash
mkdir -p ~/.hermes/profiles/ctf/home/firecrawl
cd ~/.hermes/profiles/ctf/home/firecrawl
```

### 4.2 docker-compose.yaml 작성

공식 저장소에서 직접 빌드하지 않고 **prebuilt 이미지를 사용**하도록 변환. 빌드 시간 절약 + ARM/x86 호환성 확보.

핵심 내용:
- `services`: playwright-service, api, redis, rabbitmq, nuq-postgres, foundationdb, foundationdb-init
- `api`: `image: ghcr.io/firecrawl/firecrawl:latest`, `command: node dist/src/harness.js --start-docker`, RabbitMQ healthy 의존, fdb-cluster-file 볼륨 ro 마운트
- `nuq-postgres`: `command: [postgres, -c, cron.database_name=firecrawl]` — pg_cron 워커 DB를 firecrawl DB로 명시
- `foundationdb-init`: 1회성 DB 초기화 (`restart: "no"`), 정상 종료 시 Exited (1)
- `networks.backend` (bridge) 공유
- 볼륨: `fdb-data`, `fdb-cluster-file`

### 4.3 .env 작성 (Pitfall: heredoc 사용 필수)

`write_file`로 작성하면 `=== Required ENVS ===` 같은 마커가 마스킹되며 줄이 합쳐지는 함정이 있음. 반드시 `terminal` heredoc + 인용부호 사용.

```bash
cat > ~/.hermes/profiles/ctf/home/firecrawl/.env << 'ENVEOF'
NUM_WORKERS_PER_QUEUE=4
PORT=3002
HOST=0.0.0.0
REDIS_URL=redis://redis:6379
REDIS_RATE_LIMIT_URL=redis://redis:6379
PLAYWRIGHT_MICROSERVICE_URL=http://playwright-service:3000/scrape
USE_DB_AUTHENTICATION=false
POSTGRES_USER=postgres
POSTGRES_PASSWORD=localpgpass123
POSTGRES_DB=firecrawl
POSTGRES_HOST=nuq-postgres
POSTGRES_PORT=5432
MAX_CPU=0.8
MAX_RAM=0.8
CRAWL_CONCURRENT_REQUESTS=8
MAX_CONCURRENT_JOBS=4
BROWSER_POOL_SIZE=3
LOGGING_LEVEL=INFO
BULL_AUTH_KEY=localbullsecret123
ENVEOF
chmod 600 ~/.hermes/profiles/ctf/home/firecrawl/.env
```

### 4.4 기동

```bash
cd ~/.hermes/profiles/ctf/home/firecrawl
docker compose pull
docker compose up -d
sleep 60   # api + workers 완전 기동 대기
```

첫 부팅 시 RabbitMQ healthcheck 통과에 ~21초 걸리므로, start_period 60s 설정으로 대기. 그래도 실패하면 한 번 더 `docker compose up -d api`로 통과.

### 4.5 헬스체크

```bash
curl -s http://localhost:3002/v1/scrape \
  -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","formats":["markdown"]}' | jq .data.markdown
```

성공 시 `Example Domain` 마크다운이 반환되고 `"success":true` 응답. `/health` 엔드포인트는 404가 정상 (Firecrawl 설계).

## 5. 운영 중 만난 함정 (Pitfalls)

### P1. nuq-postgres 첫 부팅 pg_cron 실패
- 증상: 컨테이너 시작 후 `Exit (3)`, 로그 `can only create extension in database postgres / Jobs must be scheduled from the database configured in cron.database_name`
- 원인: nuq 초기화 SQL이 사용자 DB에 `CREATE EXTENSION pg_cron` 실행, pg_cron 워커는 기본 `postgres` DB에서만 동작
- 해결: compose의 nuq-postgres `command`에 `postgres -c cron.database_name=firecrawl` 추가

### P2. RabbitMQ healthcheck 시작 시간 부족
- 증상: 첫 `docker compose up` 시 api 컨테이너 생성 안 됨
- 해결: rabbitmq healthcheck의 `start_period: 60s`로 여유 두기, 또는 두 번째 `up -d api` 시도

### P3. USE_DB_AUTHENTICATION 빈 값 ZodError
- 증상: api 즉시 죽음, `expected one of "true"|"1"|"yes"|...`
- 해결: `.env`에서 반드시 `USE_DB_AUTHENTICATION=false` 명시

### P4. POSTGRES_PASSWORD 변경 후 인증 실패
- 증상: `password authentication failed for user "postgres"`
- 원인: nuq-postgres는 첫 부팅 시 POSTGRES_PASSWORD로 DB 초기화. 데이터 디렉터리에 박혀 변경 불가
- 해결: `docker compose down -v`로 볼륨까지 지우고 새로 시작

### P5. .env 작성 시 마스킹 함정
- 증상: `write_file`로 작성하면 일부 마커가 마스킹되며 줄이 합쳐짐
- 해결: terminal heredoc + 인용부호 사용

### P6. 메모리 한도
- 공식 compose는 api 8G + playwright 4G 요구. 저사양 환경에서는 compose의 `cpus`/`mem_limit`를 위 표처럼 축소
- 그래도 idle 5~6GB. 동시 요청 시 OOM 위험 → `CRAWL_CONCURRENT_REQUESTS=8`, `BROWSER_POOL_SIZE=3` 보수적 운영

## 6. Hermes news 프로필 연동

### 6.1 .env 설정

파일: `~/.hermes/profiles/news/.env`

```bash
# Local self-hosted Firecrawl (ctf profile compose stack, shared)
FIRECRAWL_API_URL=http://localhost:3002
```

`FIRECRAWL_API_KEY`는 주석 처리 — 로컬 셀프호스팅이라 키 불필요.

### 6.2 config.yaml 설정

파일: `~/.hermes/profiles/news/config.yaml`

```yaml
web:
  backend: firecrawl
  search_backend: ''     # 비워두면 web_search가 자동으로 firecrawl 백엔드 사용
  extract_backend: ''    # 비워두면 web_extract가 자동으로 firecrawl 백엔드 사용
browser:
  ...
```

### 6.3 플러그인 자동 등록

`~/.hermes/profiles/ctf/hermes-agent/plugins/web/firecrawl/plugin.yaml`:

```yaml
name: web-firecrawl
version: 1.0.0
description: "Firecrawl web search + content extraction. Supports direct API and Nous-hosted tool-gateway routing for subscribers. Requires FIRECRAWL_API_KEY (or FIRECRAWL_API_URL for self-hosted)..."
provides_web_providers:
  - firecrawl
```

`browser-firecrawl` 플러그인과 함께 `web_search`, `web_extract`, `browser_*` 호출이 모두 로컬 Firecrawl로 라우팅됨.

### 6.4 검증

```bash
# 터미널에서 직접
curl -s http://localhost:3002/v1/scrape -X POST -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","formats":["markdown"]}'

# Hermes 세션에서
# web_search("최신 CVE-2026-23111"), web_extract(urls=["https://..."])
```

성공 시 응답 본문에 `success: true`와 markdown 본문 포함.

## 7. 운영 명령 모음

```bash
# 컨테이너 상태
cd ~/.hermes/profiles/ctf/home/firecrawl && docker compose ps

# API 로그
docker logs firecrawl-api-1 --tail 50

# 전체 재시작
docker compose restart

# 특정 서비스만 재시작
docker compose restart api

# 완전 초기화 (DB 볼륨 포함, 비밀번호 변경 시)
docker compose down -v && docker compose up -d

# 로그 드라이버는 이미 10MB x 3 파일로 로테이션 설정됨
docker logs --since 1h firecrawl-api-1
```

## 8. Search API (web_search 백엔드)

Firecrawl `/search`는 기본적으로 Google을 사용하지만 셀프호스팅에서는 Fire-engine 접근 불가로 차단될 수 있음. 대안:

1. **SearXNG 별도 운영**: `SEARXNG_ENDPOINT=http://localhost:8080` 환경변수 추가, SearXNG 컨테이너 별도 기동
2. **`web_search` 우회**: `terminal` + `curl`로 특정 사이트만 직접 크롤링
3. **`web_extract`만 사용**: `search_backend=''` 상태에서 URL 추출은 정상 작동

## 9. 현재 시스템 검증 결과

2026-06-27 점검 기준:

| 항목 | 결과 |
|---|---|
| `docker compose ps` | 6개 서비스 Up, foundationdb-init Exited (정상) |
| `:3002` 포트 | 0.0.0.0 LISTEN |
| `/v1/scrape` POST | HTTP 200, `success:true`, markdown 반환 |
| Hermes `web.backend` | `firecrawl` |
| `FIRECRAWL_API_URL` | `http://localhost:3002` |
| 플러그인 등록 | web-firecrawl, browser-firecrawl 모두 활성 |

## 10. 참고 자료

- 공식 저장소: https://github.com/firecrawl/firecrawl
- 공식 compose: https://raw.githubusercontent.com/firecrawl/firecrawl/main/docker-compose.yaml
- 내부 스킬: `~/.hermes/profiles/ctf/skills/devops/firecrawl-selfhost.md`
- 플러그인: `~/.hermes/profiles/ctf/hermes-agent/plugins/web/firecrawl/`
- 운영 compose: `~/.hermes/profiles/ctf/home/firecrawl/docker-compose.yaml`

## 11. 다음에 살펴볼 거리

- `/search` 차단 대비 SearXNG 컨테이너 추가
- foundationdb-init의 Exited (1)이 의도된 정상 종료인지 compose restart 정책 확인
- 디스크 사용량 누적 점검 (`docker system df`)

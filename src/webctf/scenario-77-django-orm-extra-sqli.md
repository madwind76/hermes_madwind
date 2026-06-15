---
title: Django ORM extra() SQL Injection — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, django, orm, extra-sqli, sql-injection, python, raw-sql]
confidence: high
---

# Django ORM extra() SQL Injection — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Django Query Helper (장고 쿼리 헬퍼 포털)
- **난이도**: Medium-High
- **핵심 컨셉**: 파이썬의 대표적인 안전한 웹 프레임워크인 **Django** 환경에서 제공하는 ORM 모델 사용 시, 특정 레거시 매핑 함수를 오용하여 발생하는 **Django ORM SQL 인젝션** 취약점 문제입니다. 개발진은 SQL Injection을 방어하기 위해 Django ORM을 사용하여 데이터베이스 질의를 수행해 왔습니다. 그러나 복잡한 서브쿼리 필터 및 사용자 정의 SELECT 칼럼 조작을 처리하는 과정에서, ORM 기본 인터페이스 대신 **`extra(select={...})`** 함수 혹은 `RawSQL` 모델을 변수 바인딩 없이 동적 문자열 결합 방식으로 연결해 작성했습니다. 공격자는 ORM 필터 내부로 전달되는 파라미터 값에 악성 SQL 구문을 주입해 ORM의 방어 통제를 완벽히 우회하고 데이터베이스 구조 전체를 유출시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Search Item View (`/api/items/search`)**:
  - 사용자가 기입한 정렬 기준(`sort_by`) 혹은 추가 메타데이터 정보 필터링 인자를 받아 Django ORM 쿼리셋을 가동하는 뷰(View).
- **Flag 위치**:
  - 데이터베이스 내 독립된 비공개 모델 테이블인 `auth_user` 또는 `flag_store` 테이블의 칼럼값.

### 2.2 취약점 지점
1. **Unsafe extra() Function Usage**:
   - Django의 `QuerySet.extra()` 함수는 개발자가 날것의 SQL 조각을 삽입할 수 있게 허용합니다.
   - 개발자는 `extra(select={'custom_field': "SELECT ... WHERE value = '%s'" % user_input})` 와 같이 문자열 서식 지정자(`%s` 또는 `.format()`)로 파라미터를 하드코딩해 결합했습니다.
   - ORM이 쿼리를 빌드할 때 이 부분은 바인딩되지 않은 Raw SQL 텍스트로 SQL 번역기에 삽입되어 주입 틈새가 열립니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 취약 ORM 지점 |
|------------|--------|------|----------|-------------|---------------|
| `/api/items/search` | GET | 불필요 | `custom_sort` / `meta_val` | Query Parameter | `QuerySet.extra()` 내 문자열 포맷팅 결합부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Django ORM 취약 API 탐색
1. 상품 조회 폼에 정규 문자열을 기입하고 데이터가 필터링/정렬되어 출력됨을 확인합니다.
2. 싱글 쿼테이션 `'` 문자 삽입 시 일반적인 데이터베이스 문법 예외 에러(예: `django.db.utils.ProgrammingError` 혹은 SQL Syntax Error)가 화면 또는 응답에 반환되는지 확인하여 ORM 내부에 Raw SQLi 요소가 상존함을 인지합니다.

### Step 2. extra() SELECT 구문 탈출 구조 분석
백엔드 소스코드 상의 쿼리셋 흐름이 다음과 같다고 가정합니다:
```python
queryset = Items.objects.filter(is_active=True).extra(
    select={'is_popular': "SELECT count(*) FROM user_clicks WHERE item_id = id AND click_type = '%s'" % user_val}
)
```
공격자는 `user_val` 입력칸에 싱글 쿼터를 삽입하여 내부 SELECT 절을 닫고 새로운 임의 쿼리를 수행하게 만듭니다.
- **주입할 공격 페이로드**:
  `test' UNION SELECT password FROM auth_user --`
- **조립되는 SQL 형상**:
  `SELECT (SELECT count(*) FROM user_clicks WHERE item_id = id AND click_type = 'test' UNION SELECT password FROM auth_user --') AS is_popular, ... FROM items WHERE is_active = True`

### Step 3. Blind SQL 인젝션 혹은 에러 메시지 덤프 가동
1. 컬럼 개수 불일치 에러 등으로 에러 기반 SQLi가 동작한다면 에러 스택 트레이스에서 직접 비밀 값을 읽어냅니다.
2. 만약 에러가 화면에 직접 나오지 않고 결과 참/거짓만 분별 가능한 상황이라면, Blind SQLi 쿼리(예: `CASE WHEN ... THEN ...`)를 주입하여 `flag_store` 테이블의 플래그 값을 덤프하는 익스플로잇 스크립트를 작성해 기동합니다.

### Step 4. flag 획득
1. Blind SQLi 덤프 자동화 요청을 전송하여 타겟 필드에 보관 중인 플래그 데이터를 한 바이트씩 복원합니다.
2. 복원을 완료하여 획득한 최종 플래그(`FLAG{django_orm_extra_unsafe_sql_concatenation}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Django View)

```python
# views.py (취약한 Django ORM extra() 연동 뷰 예시)
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Item

@require_GET
def search_items(request):
    meta_val = request.GET.get('meta_val', '')

    if not meta_val:
        return JsonResponse({"error": "meta_val is required"}, status=400)

    try:
        # 취약점 지점 1: extra() 함수의 select 파라미터 내부에 
        # 파라미터 바인딩을 쓰지 않고 문자열 포맷팅(%s)을 사용하여 SQL 조각을 완성함
        # 이로 인해 ORM 전체 쿼리 분석기에 공격자의 악성 SQLi 구문이 그대로 스며듬
        items = Item.objects.filter(status='active').extra(
            select={
                'custom_metadata': "SELECT val FROM item_metadata WHERE item_id = id AND meta_key = '%s'" % meta_val
            }
        )
        
        # 참고: 올바른 바인딩 사용법 -> select_params=[meta_val] 매개변수 분리 지정 필수
        
        results = []
        for item in items:
            results.append({
                "id": item.id,
                "name": item.name,
                "metadata": item.custom_metadata # SQLi 쿼리 결과 반환
            })
            
        return JsonResponse({"status": "success", "data": results})
    except Exception as e:
        # 취약점 지점 2: 상세한 DB 쿼리 컴파일 에러를 그대로 클라이언트에 노출
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **`select_params`를 이용한 파라미터 바인딩 강제**:
   - `extra()` 함수 내에 동적 변수가 할당되어야 하는 경우, 절대 문자열 포맷팅을 사용하지 않고 `select_params` 파라미터 배열을 별도로 분리 선언하여 SQL 컴파일 시 바인딩 처리가 안전하게 유도되도록 지정합니다.
     ```python
     # 안전한 extra() 적용법
     items = Item.objects.filter(status='active').extra(
         select={'custom_metadata': "SELECT val FROM item_metadata WHERE item_id = id AND meta_key = %s"},
         select_params=[meta_val]
     )
     ```
2. **`extra()` 함수 사용 배제 및 Annotate/Subquery 도입**:
   - Django 공식 도큐먼트에서도 `extra()` 함수는 장기적으로 폐기 예정(Deprecated)된 레거시 보안 위험 영역으로 명시하고 있습니다.
   - 복잡한 쿼리가 요구될 시 `annotate()`와 `Subquery`, `OuterRef` 등 안전한 Django 공식 빌트인 서브쿼리 표현식 API를 연동하여 개발할 것을 권장합니다.
     ```python
     # 현대적인 안전한 Django 서브쿼리 변환 예시
     from django.db.models import Subquery, OuterRef
     metadata_subquery = ItemMetadata.objects.filter(item_id=OuterRef('pk'), meta_key=meta_val).values('val')[:1]
     items = Item.objects.filter(status='active').annotate(custom_metadata=Subquery(metadata_subquery))
     ```

# Nova 데이터 생성기

Amazon QuickSight 데모를 위한 현실적인 스마트폰 제조사(Nova 브랜드) 데이터셋을 생성하는 Python 기반 시스템입니다. 판매, 고객 트랜잭션, 마케팅 캠페인, 소셜 미디어 포스트, 제품 리뷰 등 실제 비즈니스 시나리오를 시뮬레이션하는 정형 데이터(CSV)와 비정형 데이터(JSON)를 생성합니다.

## 개요

이 데이터 생성기는 Nova라는 가상의 스마트폰 제조사를 위한 7개 제품 라인의 종합적인 데이터셋을 생성합니다:
- **Nova Prime**: 플래그십 프리미엄 기기
- **Nova Flex Fold**: 폴더블 스마트폰
- **Nova Flex Flip**: 플립 스타일 폴더블 폰
- **Nova Plus**: 중급형 기기
- **Nova Lite**: 보급형 옵션
- **Nova Max**: 대화면 기기
- **Nova Mini**: 소형 스마트폰

생성되는 데이터는 24개월 기간을 포함하며 다음과 같은 현실적인 패턴을 반영합니다:
- 제품 라이프사이클 단계 (출시, 성장, 성숙, 쇠퇴)
- 계절적 트렌드 (연말 시즌, 신학기)
- 5개 글로벌 지역의 지역별 변동
- 다채널 판매 (온라인 및 오프라인)
- 고객 세그먼트 및 인구통계
- 마케팅 캠페인 성과
- 소셜 미디어 감성 분석
- 평점이 포함된 제품 리뷰

## 주요 기능

✅ **재현 가능**: 시드 기반 랜덤 생성으로 일관된 결과 보장  
✅ **현실적**: 실제 비즈니스 시나리오를 반영한 데이터 패턴  
✅ **설정 가능**: YAML 기반 설정으로 쉬운 커스터마이징  
✅ **검증됨**: 내장된 데이터 품질 검사 및 참조 무결성  
✅ **QuickSight 최적화**: AWS QuickSight 시각화에 최적화  
✅ **다중 포맷**: CSV(정형) 및 JSON(비정형) 데이터 생성

## 설치

### 사전 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)

### 설정

1. 이 저장소를 클론하거나 다운로드합니다

2. 프로젝트 디렉토리로 이동합니다:
```bash
cd nova-data-generator
```

3. 필요한 의존성을 설치합니다:
```bash
pip install -r requirements.txt
```

## 사용법

### 기본 사용법

기본 설정으로 모든 데이터셋을 생성합니다:

```bash
python main.py
```

이 명령은 `data/` 디렉토리에 6개의 데이터셋을 생성합니다:
- `dim_products.csv` - 제품 마스터 데이터
- `fact_daily_sales.csv` - 일별 판매 트랜잭션
- `fact_transactions.csv` - 고객 트랜잭션
- `fact_campaign_performance.csv` - 마케팅 캠페인 지표
- `social_media_posts.json` - 소셜 미디어 포스트
- `product_reviews.json` - 제품 리뷰

### 설정

`config/config.yaml` 파일을 편집하여 데이터 생성을 커스터마이징할 수 있습니다:

```yaml
# 재현성을 위한 랜덤 시드
random_seed: 42

# 데이터 생성 날짜 범위
date_range:
  start_date: "2022-01-01"
  end_date: "2024-01-31"

# 고객 설정
customers:
  total_count: 10000
  repeat_customer_rate: 0.30

# 리뷰 설정
reviews:
  min_per_product: 50
  max_per_product: 150
```

자세한 파라미터 설명은 [설정 가이드](#설정-가이드)를 참조하세요.

## 생성되는 데이터셋

### 1. 제품 마스터 (`dim_products.csv`)

모든 Nova 스마트폰 모델의 사양이 포함된 제품 카탈로그입니다.

**주요 필드**:
- `product_id`: 고유 식별자 (예: "PRIME-24")
- `product_name`: 전체 제품명
- `product_line`: 제품 카테고리 (Prime, Flex Fold 등)
- `price_usd`: 소매가
- `camera_mp`, `battery_mah`, `display_inch`: 기술 사양
- `launch_date`, `discontinue_date`: 제품 라이프사이클 날짜

**레코드 수**: 약 17개 제품

### 2. 일별 판매 (`fact_daily_sales.csv`)

제품, 지역, 채널별 일별 집계 판매 데이터입니다.

**주요 필드**:
- `date`: 판매 날짜 (YYYY-MM-DD)
- `product_id`: 제품 참조
- `region`: 지리적 지역 (북미, 유럽, 아시아 태평양 등)
- `channel`: 판매 채널 (Amazon, TechMart, Nova Direct 등)
- `units_sold`: 판매 수량
- `revenue_usd`: 총 매출
- `units_returned`, `return_rate`: 반품 지표

**레코드 수**: 약 180,000개 레코드 (24개월 × 제품 × 지역 × 채널)

### 3. 고객 트랜잭션 (`fact_transactions.csv`)

인구통계 정보가 포함된 개별 고객 구매 트랜잭션입니다.

**주요 필드**:
- `transaction_id`: 고유 트랜잭션 식별자
- `transaction_datetime`: 구매 타임스탬프 (ISO 8601 형식)
- `customer_id`: 고객 식별자
- `product_id`: 구매한 제품
- `price_paid`, `discount_amount`: 가격 세부정보
- `customer_segment`: 기술 애호가, 가격 민감형, 프리미엄 추구형, 일반 사용자
- `age_group`: 18-24, 25-34, 35-44, 45-54, 55+
- `income_level`: 낮음, 중간, 높음
- `is_repeat_customer`: 재구매 여부
- `previous_product_id`: 업그레이드 분석용

**레코드 수**: 약 54,000개 트랜잭션

### 4. 캠페인 성과 (`fact_campaign_performance.csv`)

여러 채널의 마케팅 캠페인 지표입니다.

**주요 필드**:
- `campaign_id`: 캠페인 식별자
- `campaign_name`: 캠페인 설명
- `start_date`, `end_date`: 캠페인 기간
- `product_id`: 홍보 제품
- `channel`: 소셜 미디어, 검색, 디스플레이, TV, 이메일, 인플루언서
- `budget_usd`: 캠페인 예산
- `impressions`, `clicks`, `conversions`: 성과 지표
- `ctr`: 클릭률
- `conversion_rate`: 전환율
- `roi`: 투자 수익률

**레코드 수**: 약 43개 캠페인

### 5. 소셜 미디어 포스트 (`social_media_posts.json`)

감성 분석이 포함된 소셜 미디어 콘텐츠입니다.

**주요 필드**:
- `post_id`: 고유 포스트 식별자
- `timestamp`: 포스트 생성 시간 (ISO 8601 형식)
- `platform`: Twitter, Instagram, Facebook
- `text`: 포스트 내용
- `product_mentioned`: 언급된 제품
- `sentiment`: positive, negative, neutral
- `sentiment_score`: -1.0 ~ 1.0
- `engagement`: {likes, comments, shares}

**레코드 수**: 약 5,500개 포스트

### 6. 제품 리뷰 (`product_reviews.json`)

상세한 피드백이 포함된 Amazon 스타일 제품 리뷰입니다.

**주요 필드**:
- `review_id`: 고유 리뷰 식별자
- `product_id`: 리뷰 대상 제품
- `review_datetime`: 리뷰 생성 시간 (ISO 8601 형식)
- `purchase_datetime`: 원래 구매 시간
- `verified_purchase`: 인증된 구매 여부 (80-90% true)
- `rating`: 1-5점
- `review_title`, `review_text`: 리뷰 내용
- `pros`, `cons`: 장단점 배열
- `helpful_votes`, `total_votes`: 커뮤니티 피드백
- `reviewer_profile`: 리뷰어 정보
- `variant`: 제품 변형 (색상, 저장용량)

**레코드 수**: 약 1,660개 리뷰

## 설정 가이드

### 핵심 파라미터

#### `random_seed`
- **타입**: 정수
- **기본값**: 42
- **설명**: 랜덤 숫자 생성을 위한 시드. 동일한 시드를 사용하면 동일한 데이터셋을 재생성할 수 있습니다.

#### `date_range`
- **start_date**: 데이터 생성 시작 날짜 (YYYY-MM-DD)
- **end_date**: 데이터 생성 종료 날짜 (YYYY-MM-DD)
- **기본값**: 2022-01-01 ~ 2024-01-31 (24개월)

### 제품 설정

#### `products.lines`
- **설명**: 생성할 제품 라인 목록
- **각 라인 포함 사항**:
  - `name`: 제품 라인 이름
  - `series_count`: 라인당 시리즈/모델 수 (2-3개)

### 고객 설정

#### `customers.total_count`
- **타입**: 정수
- **기본값**: 10000
- **설명**: 생성할 고유 고객의 총 수

#### `customers.repeat_customer_rate`
- **타입**: 실수 (0.0-1.0)
- **기본값**: 0.30
- **설명**: 재구매하는 고객의 비율

### 리뷰 설정

#### `reviews.min_per_product`
- **타입**: 정수
- **기본값**: 50
- **설명**: 제품당 최소 리뷰 수

#### `reviews.max_per_product`
- **타입**: 정수
- **기본값**: 150
- **설명**: 제품당 최대 리뷰 수

### 소셜 미디어 설정

#### `social_posts.posts_per_product_per_month`
- **타입**: 정수
- **기본값**: 50
- **설명**: 제품당 월평균 소셜 미디어 포스트 수

### 출력 설정

#### `output.data_dir`
- **타입**: 문자열
- **기본값**: "data"
- **설명**: 생성된 파일이 저장될 디렉토리

#### `output.csv_encoding`
- **타입**: 문자열
- **기본값**: "utf-8"
- **설명**: CSV 파일의 문자 인코딩

#### `output.json_indent`
- **타입**: 정수
- **기본값**: 2
- **설명**: JSON 파일의 들여쓰기 공백 수 (가독성용)

## 데이터 품질

생성기는 다음을 보장하는 내장 검증 기능을 포함합니다:

✓ **참조 무결성**: 모든 외래 키가 유효한 기본 키를 참조  
✓ **날짜 일관성**: 판매 날짜가 제품 출시일 이후  
✓ **현실적인 범위**: 모든 숫자 값이 예상 범위 내  
✓ **누락 데이터 없음**: 필수 필드에 null 값 없음  
✓ **적절한 형식**: 날짜는 ISO 8601 형식, 일관된 데이터 타입

## 출력 파일

생성기 실행 후 다음 파일들이 생성됩니다:

### 데이터 파일
- `data/dim_products.csv`
- `data/fact_daily_sales.csv`
- `data/fact_transactions.csv`
- `data/fact_campaign_performance.csv`
- `data/social_media_posts.json`
- `data/product_reviews.json`

### 메타데이터 파일
- `data/DATA_DICTIONARY.md` - 완전한 필드 설명
- `data/generation.log` - 생성 통계 및 타임스탬프

## 프로젝트 구조

```
nova-data-generator/
├── config/
│   └── config.yaml              # 설정 파일
├── generators/
│   ├── product_generator.py     # 제품 마스터 생성기
│   ├── sales_generator.py       # 일별 판매 생성기
│   ├── transaction_generator.py # 트랜잭션 생성기
│   ├── campaign_generator.py    # 캠페인 성과 생성기
│   ├── social_generator.py      # 소셜 미디어 포스트 생성기
│   └── review_generator.py      # 제품 리뷰 생성기
├── utils/
│   ├── date_utils.py           # 날짜 생성 유틸리티
│   ├── random_utils.py         # 랜덤 숫자 생성
│   ├── text_utils.py           # 텍스트 생성 템플릿
│   └── validation_utils.py     # 데이터 검증 함수
├── output/
│   ├── csv_writer.py           # CSV 파일 작성기
│   ├── json_writer.py          # JSON 파일 작성기
│   └── metadata_writer.py      # 메타데이터 생성
├── data/                        # 출력 디렉토리 (생성됨)
├── main.py                      # 메인 실행 스크립트
├── requirements.txt             # Python 의존성
└── README.md                    # 이 파일
```

## 활용 사례

### Amazon QuickSight
- CSV 파일을 데이터셋으로 가져오기
- product_id를 사용하여 테이블 간 관계 생성
- 판매 분석, 고객 세그먼트, 캠페인 ROI 대시보드 구축

### Amazon Q in QuickSight
- 판매 트렌드에 대한 자연어 질문
- 고객 인구통계 및 구매 패턴 쿼리
- 지역별 제품 성과 분석

### Amazon Q Business / Bedrock
- 의미 검색을 위한 JSON 파일(리뷰, 소셜 포스트) 인덱싱
- 고객 피드백에 대한 감성 분석 수행
- 비정형 텍스트 데이터에서 인사이트 생성

## 문제 해결

### 문제: "Module not found" 오류
**해결책**: 모든 의존성이 설치되었는지 확인:
```bash
pip install -r requirements.txt
```

### 문제: 파일 쓰기 시 권한 거부
**해결책**: `data/` 디렉토리가 존재하고 쓰기 가능한지 확인:
```bash
mkdir -p data
chmod 755 data
```

### 문제: 메모리 부족 오류
**해결책**: `config.yaml`에서 데이터 볼륨 감소:
- `customers.total_count` 감소
- `reviews.max_per_product` 감소
- `date_range` 단축

### 문제: 데이터가 예상 패턴과 일치하지 않음
**해결책**: `random_seed` 값을 확인하세요. 다른 시드는 다른 데이터 패턴을 생성합니다.

## 요구사항

정확한 버전은 `requirements.txt`를 참조하세요:
- pandas >= 2.1.4
- numpy >= 1.26.2
- faker >= 22.0.0
- pyyaml >= 6.0.1
- python-dateutil >= 2.8.2

## 라이선스

이것은 교육 및 데모 목적을 위한 데모 데이터 생성기입니다.

## 지원

문제나 질문이 있으면 자세한 필드 설명은 DATA_DICTIONARY.md 파일을 참조하세요.

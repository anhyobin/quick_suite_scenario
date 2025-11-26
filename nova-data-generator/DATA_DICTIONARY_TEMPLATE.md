# Nova 데이터 생성기 - 데이터 사전 템플릿

**생성일**: {generation_timestamp}  
**생성기 버전**: 1.0  
**설정 시드**: {random_seed}

---

## 개요

이 데이터 사전은 Nova 데이터 생성기가 생성하는 모든 데이터셋에 대한 종합적인 문서를 제공합니다. 각 데이터셋은 필드 정의, 데이터 타입, 샘플 값, 비즈니스 컨텍스트와 함께 설명됩니다.

## 목차

1. [제품 마스터 데이터](#1-제품-마스터-데이터)
2. [일별 판매 팩트](#2-일별-판매-팩트)
3. [고객 트랜잭션](#3-고객-트랜잭션)
4. [캠페인 성과](#4-캠페인-성과)
5. [소셜 미디어 포스트](#5-소셜-미디어-포스트)
6. [제품 리뷰](#6-제품-리뷰)
7. [데이터 관계](#7-데이터-관계)
8. [데이터 품질 참고사항](#8-데이터-품질-참고사항)

---

## 1. 제품 마스터 데이터

**파일**: `dim_products.csv`  
**형식**: CSV (UTF-8)  
**타입**: 차원 테이블  
**레코드 수**: {product_count}  
**기본 키**: `product_id`

### 설명
7개 제품 라인에 걸친 모든 Nova 스마트폰 모델의 사양 및 라이프사이클 정보를 포함하는 제품 카탈로그입니다.

### 필드

| 필드명 | 데이터 타입 | Null 가능 | 설명 | 샘플 값 |
|--------|------------|----------|------|---------|
| `product_id` | STRING | 아니오 | {LINE}-{YEAR} 형식의 고유 제품 식별자 | "PRIME-24", "FLEX-FOLD-23" |
| `product_name` | STRING | 아니오 | 전체 제품 마케팅 이름 | "Nova Prime 24", "Nova Flex Fold 23" |
| `product_line` | STRING | 아니오 | 제품 카테고리/라인 | "Prime", "Flex Fold", "Flex Flip", "Plus", "Lite", "Max", "Mini" |
| `series` | STRING | 아니오 | 제품 라인 내 시리즈 식별자 | "24", "23", "22" |
| `launch_date` | DATE | 아니오 | 제품 출시일 (YYYY-MM-DD) | "2023-03-15", "2024-01-10" |
| `discontinue_date` | DATE | 예 | 제품 단종일 (아직 활성이면 null) | "2025-06-30", null |
| `price_usd` | DECIMAL(10,2) | 아니오 | 미국 달러 소매가 | 999.00, 1299.99, 499.00 |
| `camera_mp` | INTEGER | 아니오 | 메가픽셀 단위 주 카메라 해상도 | 108, 50, 64, 200 |
| `battery_mah` | INTEGER | 아니오 | 밀리암페어시 단위 배터리 용량 | 5000, 4500, 3700 |
| `display_inch` | DECIMAL(3,1) | 아니오 | 인치 단위 디스플레이 크기 | 6.7, 7.6, 5.4 |
| `storage_gb` | INTEGER | 아니오 | 기가바이트 단위 내부 저장 용량 | 128, 256, 512, 1024 |
| `ram_gb` | INTEGER | 아니오 | 기가바이트 단위 RAM 용량 | 8, 12, 16 |
| `processor` | STRING | 아니오 | 프로세서 모델명 | "Snapdragon 8 Gen 2", "Exynos 2200" |
| `color_options` | STRING | 아니오 | 사용 가능한 색상 (쉼표로 구분) | "Black, White, Blue", "Phantom Black, Cream" |
| `weight_g` | INTEGER | 아니오 | 그램 단위 기기 무게 | 195, 263, 168 |

### 비즈니스 규칙
- 각 제품 라인은 2-3개의 시리즈/모델을 가집니다
- 출시일은 설정된 날짜 범위에 걸쳐 분산됩니다
- 프리미엄 라인 (Prime, Flex)은 더 높은 사양과 가격을 가집니다
- 보급형 라인 (Lite)은 더 낮은 사양과 가격을 가집니다


---

## 2. 일별 판매 팩트

**파일**: `fact_daily_sales.csv`  
**형식**: CSV (UTF-8)  
**타입**: 팩트 테이블  
**레코드 수**: {sales_count}  
**날짜 범위**: {sales_date_range}  
**외래 키**: `product_id` → `dim_products.product_id`

### 설명
제품, 지역, 판매 채널별 일별 집계 판매 데이터입니다. 품질 분석을 위한 반품 지표를 포함합니다.

### 필드

| 필드명 | 데이터 타입 | Null 가능 | 설명 | 샘플 값 |
|--------|------------|----------|------|---------|
| `date` | DATE | 아니오 | 판매 날짜 (YYYY-MM-DD) | "2023-06-15", "2024-01-20" |
| `product_id` | STRING | 아니오 | 제품 식별자 (FK) | "PRIME-24", "LITE-23" |
| `region` | STRING | 아니오 | 지리적 지역 | "North America", "Europe", "Asia Pacific", "Latin America", "Middle East" |
| `country` | STRING | 아니오 | 지역 내 특정 국가 | "United States", "Germany", "Japan" |
| `channel` | STRING | 아니오 | 판매 채널명 | "Amazon", "TechMart", "Nova Direct", "Nova Flagship Stores" |
| `channel_type` | STRING | 아니오 | 채널 카테고리 | "Online", "Offline" |
| `units_sold` | INTEGER | 아니오 | 판매된 수량 | 150, 1200, 45 |
| `revenue_usd` | DECIMAL(12,2) | 아니오 | 미국 달러 총 매출 | 149850.00, 599400.00 |
| `units_returned` | INTEGER | 아니오 | 반품된 수량 | 3, 48, 2 |
| `return_rate` | DECIMAL(5,4) | 아니오 | 반품률 (units_returned / units_sold) | 0.0200, 0.0400, 0.0150 |

### 비즈니스 규칙
- 판매는 제품 출시일 이후에만 발생합니다
- 반품률은 일반적으로 2-5% (프리미엄 제품은 더 낮음)
- 계절적 패턴: 11-12월 +25%, 8-9월 +15%
- 지역 분포: 북미 30%, 유럽 25%, 아시아태평양 35%, 중남미 7%, 중동 3%
- 채널 분할: 온라인 60%, 오프라인 40%

### 집계 참고사항
- 데이터는 일별 수준에서 사전 집계됩니다
- 하루의 여러 트랜잭션이 합산됩니다
- 시계열 분석 및 트렌드 시각화에 사용합니다


---

## 3. 고객 트랜잭션

**파일**: `fact_transactions.csv`  
**형식**: CSV (UTF-8)  
**타입**: 팩트 테이블  
**레코드 수**: {transaction_count}  
**외래 키**: `product_id` → `dim_products.product_id`, `previous_product_id` → `dim_products.product_id`

### 설명
인구통계 정보 및 구매 행동이 포함된 개별 고객 구매 트랜잭션입니다. 고객 세그먼트 및 업그레이드 패턴 분석을 가능하게 합니다.

### 필드

| 필드명 | 데이터 타입 | Null 가능 | 설명 | 샘플 값 |
|--------|------------|----------|------|---------|
| `transaction_id` | STRING | 아니오 | 고유 트랜잭션 식별자 | "TXN-20230615-001234" |
| `transaction_datetime` | DATETIME | 아니오 | 구매 타임스탬프 (ISO 8601: YYYY-MM-DDTHH:MM:SS) | "2023-06-15T14:23:45" |
| `customer_id` | STRING | 아니오 | 고객 식별자 | "CUST-00001234" |
| `product_id` | STRING | 아니오 | 구매한 제품 (FK) | "PRIME-24", "PLUS-23" |
| `price_paid` | DECIMAL(10,2) | 아니오 | 할인 후 실제 지불 가격 | 899.00, 1199.99, 449.00 |
| `discount_amount` | DECIMAL(10,2) | 아니오 | 적용된 총 할인 금액 | 100.00, 0.00, 50.00 |
| `channel` | STRING | 아니오 | 구매 채널 | "Amazon", "Nova Direct", "TechMart Stores" |
| `region` | STRING | 아니오 | 고객 지역 | "North America", "Europe", "Asia Pacific" |
| `country` | STRING | 아니오 | 고객 국가 | "United States", "United Kingdom", "Japan" |
| `customer_segment` | STRING | 아니오 | 고객 행동 세그먼트 | "Tech Enthusiast", "Budget Conscious", "Premium Seeker", "Casual User" |
| `age_group` | STRING | 아니오 | 고객 연령대 | "18-24", "25-34", "35-44", "45-54", "55+" |
| `income_level` | STRING | 아니오 | 고객 소득 구간 | "Low", "Medium", "High" |
| `is_repeat_customer` | BOOLEAN | 아니오 | 이전 구매 여부 | true, false |
| `previous_product_id` | STRING | 예 | 이전 소유 제품 (재구매 고객용) | "PRIME-23", "PLUS-22", null |

### 비즈니스 규칙
- 트랜잭션 시간은 현실적인 패턴을 위해 영업 시간(오전 9시 - 오후 9시) 내입니다
- 할인 범위: 0-30% (온라인에서 더 높음, 프로모션 기간 중)
- 30%의 고객이 재구매 고객입니다
- 고객 세그먼트는 제품 선호도를 가집니다:
  - 기술 애호가: Prime/Flex 제품
  - 가격 민감형: Lite/Plus 제품
  - 프리미엄 추구형: Prime/Max 제품
  - 일반 사용자: Plus/Lite 제품

### 분석 활용 사례
- 고객 생애 가치 계산
- 업그레이드 패턴 분석 (previous_product_id → product_id)
- 인구통계 세그먼트
- 세그먼트별 채널 선호도


---

## 4. 캠페인 성과

**파일**: `fact_campaign_performance.csv`  
**형식**: CSV (UTF-8)  
**타입**: 팩트 테이블  
**레코드 수**: {campaign_count}  
**외래 키**: `product_id` → `dim_products.product_id`

### 설명
여러 채널의 마케팅 캠페인 성과 지표입니다. 예산, 도달, 참여, ROI 계산을 포함합니다.

### 필드

| 필드명 | 데이터 타입 | Null 가능 | 설명 | 샘플 값 |
|--------|------------|----------|------|---------|
| `campaign_id` | STRING | 아니오 | 고유 캠페인 식별자 | "CAMP-PRIME24-001" |
| `campaign_name` | STRING | 아니오 | 캠페인 설명 | "Prime 24 출시 - 소셜", "Lite 23 연말 세일" |
| `start_date` | DATE | 아니오 | 캠페인 시작일 (YYYY-MM-DD) | "2023-03-01", "2023-11-15" |
| `end_date` | DATE | 아니오 | 캠페인 종료일 (YYYY-MM-DD) | "2023-03-31", "2023-12-31" |
| `product_id` | STRING | 아니오 | 홍보 제품 (FK) | "PRIME-24", "LITE-23" |
| `channel` | STRING | 아니오 | 마케팅 채널 | "Social Media", "Search", "Display", "TV", "Email", "Influencer" |
| `region` | STRING | 아니오 | 대상 지역 | "North America", "Europe", "Asia Pacific" |
| `budget_usd` | DECIMAL(12,2) | 아니오 | 미국 달러 캠페인 예산 | 50000.00, 250000.00 |
| `impressions` | INTEGER | 아니오 | 광고 노출 수 | 1500000, 25000000 |
| `clicks` | INTEGER | 아니오 | 클릭/참여 수 | 15000, 500000 |
| `ctr` | DECIMAL(6,4) | 아니오 | 클릭률 (clicks / impressions) | 0.0100, 0.0200 |
| `conversions` | INTEGER | 아니오 | 전환/구매 수 | 450, 25000 |
| `conversion_rate` | DECIMAL(6,4) | 아니오 | 전환율 (conversions / clicks) | 0.0300, 0.0500 |
| `revenue_usd` | DECIMAL(12,2) | 아니오 | 캠페인에 귀속된 매출 | 449550.00, 12499750.00 |
| `roi` | DECIMAL(8,4) | 아니오 | 투자 수익률 ((revenue - budget) / budget) | 7.9910, 48.9990 |

### 비즈니스 규칙
- 캠페인은 일반적으로 2-4주 동안 진행됩니다
- 출시 캠페인은 제품 출시 2주 전에 시작됩니다
- 채널 성과는 다양합니다:
  - 소셜 미디어: 높은 노출, 낮은 CTR (0.5-1.5%), 중간 전환 (2-4%)
  - 검색: 중간 노출, 높은 CTR (3-8%), 높은 전환 (5-10%)
  - 디스플레이: 매우 높은 노출, 낮은 CTR (0.3-0.8%), 낮은 전환 (1-2%)
  - 이메일: 낮은 노출, 높은 CTR (10-20%), 중간 전환 (3-6%)
  - 인플루언서: 중간 노출, 중간 CTR (2-5%), 높은 전환 (5-8%)

### 계산 지표
- CTR = clicks / impressions
- 전환율 = conversions / clicks
- ROI = (revenue_usd - budget_usd) / budget_usd


---

## 5. 소셜 미디어 포스트

**파일**: `social_media_posts.json`  
**형식**: JSON (UTF-8)  
**타입**: 비정형 데이터  
**레코드 수**: {social_count}

### 설명
감성 분석 및 참여 지표가 포함된 Nova 제품을 언급하는 소셜 미디어 포스트입니다. 브랜드 인식 및 트렌드 분석에 유용합니다.

### 스키마

```json
{
  "post_id": "string",
  "timestamp": "datetime (ISO 8601)",
  "platform": "string",
  "user_id": "string",
  "user_followers": "integer",
  "text": "string",
  "product_mentioned": "string (nullable)",
  "hashtags": ["string"],
  "sentiment": "string",
  "sentiment_score": "float",
  "engagement": {
    "likes": "integer",
    "comments": "integer",
    "shares": "integer"
  },
  "language": "string"
}
```

### 필드 설명

| 필드명 | 데이터 타입 | 설명 | 샘플 값 |
|--------|------------|------|---------|
| `post_id` | STRING | 고유 포스트 식별자 | "POST-TW-20230615-001234" |
| `timestamp` | DATETIME | 포스트 생성 시간 (ISO 8601) | "2023-06-15T14:23:45" |
| `platform` | STRING | 소셜 미디어 플랫폼 | "Twitter", "Instagram", "Facebook" |
| `user_id` | STRING | 사용자/계정 식별자 | "user_12345", "techreviewer99" |
| `user_followers` | INTEGER | 팔로워 수 | 1500, 50000, 250 |
| `text` | STRING | 포스트 내용 (100-500자) | "방금 Nova Prime 24를 받았어요! 카메라가 놀라워요..." |
| `product_mentioned` | STRING | 참조된 제품 (nullable) | "PRIME-24", "LITE-23", null |
| `hashtags` | ARRAY[STRING] | 사용된 해시태그 | ["#NovaPrime", "#Smartphone", "#TechReview"] |
| `sentiment` | STRING | 감성 분류 | "positive", "negative", "neutral" |
| `sentiment_score` | FLOAT | 감성 점수 (-1.0 ~ 1.0) | 0.85, -0.45, 0.10 |
| `engagement.likes` | INTEGER | 좋아요 수 | 150, 5000, 25 |
| `engagement.comments` | INTEGER | 댓글 수 | 12, 250, 3 |
| `engagement.shares` | INTEGER | 공유/리트윗 수 | 8, 150, 1 |
| `language` | STRING | 포스트 언어 코드 | "en", "es", "ja" |

### 비즈니스 규칙
- 감성 분포: 60% 긍정, 25% 중립, 15% 부정
- 제품 출시 후 포스트 빈도 증가
- 플랫폼 특성:
  - Twitter: 짧은 텍스트 (100-280자), 높은 빈도
  - Instagram: 이미지 중심, 많은 해시태그
  - Facebook: 긴 텍스트 (200-500자), 상세한 리뷰


---

## 6. 제품 리뷰

**파일**: `product_reviews.json`  
**형식**: JSON (UTF-8)  
**타입**: 비정형 데이터  
**레코드 수**: {review_count}

### 설명
평점, 상세한 피드백, 검증 상태가 포함된 Amazon 스타일 제품 리뷰입니다. 장단점 및 커뮤니티 투표를 포함합니다.

### 스키마

```json
{
  "review_id": "string",
  "product_id": "string",
  "customer_id": "string",
  "review_datetime": "datetime (ISO 8601)",
  "purchase_datetime": "datetime (ISO 8601)",
  "verified_purchase": "boolean",
  "rating": "integer",
  "review_title": "string",
  "review_text": "string",
  "pros": ["string"],
  "cons": ["string"],
  "helpful_votes": "integer",
  "total_votes": "integer",
  "reviewer_profile": {
    "name": "string",
    "total_reviews": "integer",
    "reviewer_rank": "integer"
  },
  "variant": "string"
}
```

### 필드 설명

| 필드명 | 데이터 타입 | 설명 | 샘플 값 |
|--------|------------|------|---------|
| `review_id` | STRING | 고유 리뷰 식별자 | "REV-20230625-001234" |
| `product_id` | STRING | 리뷰 대상 제품 | "PRIME-24", "PLUS-23" |
| `customer_id` | STRING | 리뷰 작성 고객 | "CUST-00001234" |
| `review_datetime` | DATETIME | 리뷰 생성 시간 (ISO 8601) | "2023-06-25T10:30:00" |
| `purchase_datetime` | DATETIME | 원래 구매 시간 (ISO 8601) | "2023-06-15T14:23:45" |
| `verified_purchase` | BOOLEAN | 구매 인증 여부 | true, false |
| `rating` | INTEGER | 별점 (1-5) | 5, 4, 3, 2, 1 |
| `review_title` | STRING | 리뷰 제목 (20-50자) | "놀라운 카메라 품질!", "배터리에 실망" |
| `review_text` | STRING | 리뷰 본문 (100-500자) | "이 폰을 2주 동안 사용했는데..." |
| `pros` | ARRAY[STRING] | 긍정적인 측면 | ["훌륭한 카메라", "빠른 프로세서", "아름다운 디스플레이"] |
| `cons` | ARRAY[STRING] | 부정적인 측면 | ["배터리 수명이 더 좋을 수 있음", "비쌈"] |
| `helpful_votes` | INTEGER | 도움이 됨 투표 수 | 45, 120, 5 |
| `total_votes` | INTEGER | 받은 총 투표 수 | 50, 135, 8 |
| `reviewer_profile.name` | STRING | 리뷰어 표시 이름 | "TechEnthusiast99", "JohnD" |
| `reviewer_profile.total_reviews` | INTEGER | 이 사용자의 총 리뷰 수 | 15, 3, 47 |
| `reviewer_profile.reviewer_rank` | INTEGER | 리뷰어 순위 | 1500, 50000, 250 |
| `variant` | STRING | 구매한 제품 변형 | "Phantom Black, 256GB", "White, 128GB" |

### 비즈니스 규칙
- 평점 분포: 5★ (40%), 4★ (30%), 3★ (15%), 2★ (10%), 1★ (5%)
- 80-90%의 리뷰가 인증된 구매입니다
- 리뷰 타이밍: 70%가 구매 후 7-30일 이내
- 높은 평점의 리뷰가 더 많은 도움이 됨 투표를 받습니다
- 각 제품은 50-150개의 리뷰를 가집니다


---

## 7. 데이터 관계

### 엔티티 관계 다이어그램

```
dim_products (제품 마스터)
    │
    ├──→ fact_daily_sales (일별 판매)
    │    └── 관계: product_id (1:N)
    │
    ├──→ fact_transactions (트랜잭션)
    │    ├── 관계: product_id (1:N)
    │    └── 관계: previous_product_id (1:N, nullable)
    │
    ├──→ fact_campaign_performance (캠페인)
    │    └── 관계: product_id (1:N)
    │
    ├──→ social_media_posts (소셜 포스트)
    │    └── 관계: product_mentioned (1:N, nullable)
    │
    └──→ product_reviews (리뷰)
         └── 관계: product_id (1:N)

fact_transactions
    └──→ product_reviews
         └── 관계: customer_id (1:N)
```

### 조인 예시

**제품별 판매**:
```sql
SELECT p.product_name, SUM(s.units_sold) as total_units
FROM dim_products p
JOIN fact_daily_sales s ON p.product_id = s.product_id
GROUP BY p.product_name
```

**고객 업그레이드 패턴**:
```sql
SELECT 
    p1.product_name as previous_product,
    p2.product_name as new_product,
    COUNT(*) as upgrade_count
FROM fact_transactions t
JOIN dim_products p1 ON t.previous_product_id = p1.product_id
JOIN dim_products p2 ON t.product_id = p2.product_id
WHERE t.is_repeat_customer = true
GROUP BY p1.product_name, p2.product_name
```

---

## 8. 데이터 품질 참고사항

### 적용된 검증 규칙

✓ **참조 무결성**: 모든 외래 키가 유효한 기본 키를 참조  
✓ **날짜 일관성**: 판매 날짜가 제품 출시일 이후  
✓ **현실적인 범위**: 모든 숫자 값이 예상 범위 내  
✓ **누락 데이터 없음**: 필수 필드에 null 값 없음  
✓ **적절한 형식**: 날짜는 ISO 8601 형식 사용  
✓ **계산 필드**: CTR, conversion_rate, ROI가 수학적으로 정확

### 알려진 제한사항

- 소셜 미디어 포스트와 리뷰는 템플릿 기반입니다 (실제 사용자 콘텐츠 아님)
- 고객 ID는 합성이며 실제 개인을 나타내지 않습니다
- 지리적 분포가 단순화되었습니다 (모든 국가가 표현되지 않음)
- 계절적 패턴이 일반화되었습니다 (지역별로 특화되지 않음)

### 데이터 신선도

- **생성일**: {generation_timestamp}
- **데이터 기간**: {date_range}
- **재현성**: 동일한 데이터를 재생성하려면 시드 {random_seed} 사용

---

## 부록: 열거 값

### 제품 라인
- Prime
- Flex Fold
- Flex Flip
- Plus
- Lite
- Max
- Mini

### 지역
- North America
- Europe
- Asia Pacific
- Latin America
- Middle East

### 판매 채널
**온라인**:
- Amazon
- TechMart
- MegaStore Online
- Nova Direct

**오프라인**:
- TechMart Stores
- MegaStore Retail
- CarrierShops
- Nova Flagship Stores

### 고객 세그먼트
- Tech Enthusiast (기술 애호가)
- Budget Conscious (가격 민감형)
- Premium Seeker (프리미엄 추구형)
- Casual User (일반 사용자)

### 연령대
- 18-24
- 25-34
- 35-44
- 45-54
- 55+

### 소득 수준
- Low (낮음)
- Medium (중간)
- High (높음)

### 마케팅 채널
- Social Media (소셜 미디어)
- Search (검색)
- Display (디스플레이)
- TV
- Email (이메일)
- Influencer (인플루언서)

### 소셜 미디어 플랫폼
- Twitter
- Instagram
- Facebook

### 감성 분류
- positive (긍정)
- negative (부정)
- neutral (중립)

---

**데이터 사전 끝**

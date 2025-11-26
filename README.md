# Amazon Quick Suite 데모 시나리오

Amazon Quick Suite 데모를 위한 현실적인 스마트폰 제조사(Nova 브랜드) 데이터셋 생성 시스템입니다.

## 📋 프로젝트 개요

이 프로젝트는 Amazon Quick Suite의 5가지 핵심 기능을 시연하기 위한 종합적인 데모 데이터셋을 생성합니다:

- **Amazon Quick Sight**: 대화형 데이터 시각화 및 비즈니스 인텔리전스
- **Amazon Quick Flows**: 지능형 워크플로우 자동화
- **Amazon Quick Automate**: 비즈니스 프로세스 자동화
- **Amazon Quick Index**: 데이터 검색 및 카탈로그화
- **Amazon Quick Research**: 포괄적인 데이터 분석 및 심층 리서치

## 🎯 주요 특징

✅ **현실적인 비즈니스 시나리오**: 실제 스마트폰 제조사의 24개월 운영 데이터  
✅ **다양한 데이터 타입**: 정형 데이터(CSV) + 비정형 데이터(JSON)  
✅ **9개 페르소나 시나리오**: 마케팅, 영업, 제품, 고객 분석, 브랜드, 품질, 재무, 데이터 과학, 경영진  
✅ **재현 가능**: 시드 기반 랜덤 생성으로 일관된 결과  
✅ **완전한 문서화**: 한글 README, 데이터 사전, 페르소나 시나리오

## 📊 생성되는 데이터셋

### 정형 데이터 (CSV)
1. **제품 마스터** (`dim_products.csv`) - 17개 제품의 사양 및 라이프사이클
2. **일별 판매** (`fact_daily_sales.csv`) - 180,000+ 레코드의 판매 트랜잭션
3. **고객 트랜잭션** (`fact_transactions.csv`) - 54,000+ 개별 구매 기록
4. **캠페인 성과** (`fact_campaign_performance.csv`) - 43개 마케팅 캠페인 지표

### 비정형 데이터 (JSON)
5. **소셜 미디어 포스트** (`social_media_posts.json`) - 5,500+ 감성 분석 포함
6. **제품 리뷰** (`product_reviews.json`) - 1,660+ Amazon 스타일 리뷰

## 🚀 빠른 시작

### 설치

```bash
cd nova-data-generator
pip install -r requirements.txt
```

### 데이터 생성

```bash
python main.py
```

생성된 데이터는 `data/` 디렉토리에 저장됩니다.

## 📖 문서

- **[README.md](nova-data-generator/README.md)** - 전체 프로젝트 문서 및 사용 가이드
- **[PERSONA_SCENARIOS.md](nova-data-generator/PERSONA_SCENARIOS.md)** - 9개 페르소나별 분석 시나리오
- **[DATA_DICTIONARY_TEMPLATE.md](nova-data-generator/DATA_DICTIONARY_TEMPLATE.md)** - 완전한 데이터 사전
- **[config.yaml](nova-data-generator/config/config.yaml)** - 설정 파라미터 상세 설명

## 👥 페르소나 시나리오

각 페르소나가 Quick Suite를 활용하여 수행하는 분석 업무:

1. **마케팅 매니저** - 캠페인 ROI 최적화
2. **영업 분석가** - 지역별 판매 트렌드 분석
3. **제품 매니저** - 제품 라이프사이클 및 포트폴리오 분석
4. **고객 인사이트 분석가** - 고객 세그먼트 및 행동 분석
5. **브랜드 매니저** - 소셜 미디어 감성 및 브랜드 인식 분석
6. **품질 관리 매니저** - 제품 리뷰 및 품질 이슈 분석
7. **재무 분석가** - 수익성 및 가격 전략 분석
8. **데이터 과학자** - 예측 모델링 및 고급 분석
9. **경영진** - 전사 대시보드 및 KPI 모니터링

자세한 내용은 [PERSONA_SCENARIOS.md](nova-data-generator/PERSONA_SCENARIOS.md)를 참조하세요.

## 🎨 Nova 제품 라인

- **Nova Prime** - 플래그십 프리미엄 기기 ($999-1299)
- **Nova Flex Fold** - 폴더블 스마트폰 ($1799-2199)
- **Nova Flex Flip** - 플립 스타일 폴더블 폰 ($999-1199)
- **Nova Plus** - 중급형 기기 ($599-799)
- **Nova Lite** - 보급형 옵션 ($299-499)
- **Nova Max** - 대화면 기기 ($899-1099)
- **Nova Mini** - 소형 스마트폰 ($699-899)

## 🔧 설정 커스터마이징

`config/config.yaml` 파일을 편집하여 데이터 생성을 커스터마이징할 수 있습니다:

```yaml
random_seed: 42                    # 재현성을 위한 시드
date_range:
  start_date: "2022-01-01"
  end_date: "2024-01-31"
customers:
  total_count: 10000               # 고객 수
  repeat_customer_rate: 0.30       # 재구매율
reviews:
  min_per_product: 50
  max_per_product: 150
```

## 📈 Quick Suite 활용 매트릭스

| 페르소나 | Quick Sight | Quick Index | Quick Research | Quick Flows | Quick Automate |
|---------|------------|-------------|----------------|-------------|----------------|
| 마케팅 매니저 | ✓✓✓ | - | - | ✓ | ✓✓ |
| 영업 분석가 | ✓✓✓ | - | - | ✓✓ | - |
| 브랜드 매니저 | ✓ | ✓✓✓ | ✓✓✓ | ✓✓ | - |
| 품질 관리 매니저 | ✓✓ | ✓✓✓ | ✓✓✓ | - | ✓✓ |
| 데이터 과학자 | ✓✓✓ | - | ✓✓ | - | - |
| 경영진 | ✓✓✓ | - | - | ✓ | - |

**범례**: ✓✓✓ 핵심 활용, ✓✓ 주요 활용, ✓ 보조 활용

## 🗂️ 프로젝트 구조

```
nova-data-generator/
├── config/
│   └── config.yaml              # 설정 파일
├── generators/                  # 데이터 생성기
│   ├── product_generator.py
│   ├── sales_generator.py
│   ├── transaction_generator.py
│   ├── campaign_generator.py
│   ├── social_generator.py
│   └── review_generator.py
├── utils/                       # 유틸리티 함수
├── output/                      # 출력 모듈
├── data/                        # 생성된 데이터 (gitignore)
├── main.py                      # 메인 실행 스크립트
├── requirements.txt             # Python 의존성
├── README.md                    # 프로젝트 문서
├── PERSONA_SCENARIOS.md         # 페르소나 시나리오
└── DATA_DICTIONARY_TEMPLATE.md  # 데이터 사전
```

## 💡 사용 예시

### Quick Sight 대시보드
```
- 채널별 ROI 비교 막대 차트
- 지역별 매출 트렌드 라인 차트
- 제품 라이프사이클 곡선
- 고객 세그먼트 분석
```

### Quick Index 검색
```
- "배터리 문제" 관련 리뷰 검색
- 부정적 감성 소셜 포스트 필터링
- 제품별 품질 이슈 키워드 추출
```

### Quick Research 심층 분석
```
- 5,500개 소셜 포스트 동시 분석
- 브랜드 인식 변화 추이 분석
- 제품 라인별 품질 이슈 비교
```

### Quick Automate 워크플로우
```
- ROI 목표 미달 시 자동 알림
- 주간 성과 리포트 자동 생성
- 부정적 리뷰 자동 분류 및 알림
```

## 🔍 데이터 품질

✓ **참조 무결성**: 모든 외래 키가 유효한 기본 키를 참조  
✓ **날짜 일관성**: 판매 날짜가 제품 출시일 이후  
✓ **현실적인 범위**: 모든 숫자 값이 예상 범위 내  
✓ **누락 데이터 없음**: 필수 필드에 null 값 없음  
✓ **적절한 형식**: 날짜는 ISO 8601 형식 사용

## 📦 요구사항

- Python 3.8 이상
- pandas >= 2.1.4
- numpy >= 1.26.2
- faker >= 22.0.0
- pyyaml >= 6.0.1
- python-dateutil >= 2.8.2

## 📝 라이선스

이것은 교육 및 데모 목적을 위한 데모 데이터 생성기입니다.

## 🤝 기여

이슈나 개선 제안은 GitHub Issues를 통해 제출해주세요.

## 📧 문의

프로젝트 관련 문의사항은 Issues를 통해 남겨주세요.

---

**Amazon Quick Suite**로 데이터 기반 의사결정을 시작하세요! 🚀

# Nova Data Generator - Data Dictionary

Generated: 2025-11-26 16:16:51

## Products

**File**: `dim_products.csv`

**Description**: Product master data with specifications

**Record Count**: 17

**Fields**:

- `product_id` (STRING): Unique product identifier
- `product_name` (STRING): Product name
- `product_line` (STRING): Product line (Prime, Flex, Plus, etc.)
- `price_usd` (DECIMAL): Product price in USD

## Daily Sales

**File**: `fact_daily_sales.csv`

**Description**: Daily sales transactions by product, region, and channel

**Record Count**: 179632

**Date Range**: 2022-02-24 to 2024-01-31

**Fields**:

- `date` (DATE): Sale date
- `product_id` (STRING): Product identifier
- `units_sold` (INTEGER): Number of units sold
- `revenue_usd` (DECIMAL): Revenue in USD

## Transactions

**File**: `fact_transactions.csv`

**Description**: Customer transaction details with segments and demographics

**Record Count**: 53890

**Fields**:

- `transaction_id` (STRING): Unique transaction identifier
- `customer_id` (STRING): Customer identifier
- `customer_segment` (STRING): Customer segment

## Campaigns

**File**: `fact_campaign_performance.csv`

**Description**: Marketing campaign performance metrics

**Record Count**: 43

**Fields**:

- `campaign_id` (STRING): Campaign identifier
- `channel` (STRING): Marketing channel
- `roi` (DECIMAL): Return on investment

## Social Media Posts

**File**: `social_media_posts.json`

**Description**: Social media posts with sentiment analysis

**Record Count**: 5525

**Fields**:

- `post_id` (STRING): Post identifier
- `sentiment` (STRING): Sentiment classification

## Product Reviews

**File**: `product_reviews.json`

**Description**: Amazon-style product reviews with ratings and feedback

**Record Count**: 1661

**Fields**:

- `review_id` (STRING): Review identifier
- `rating` (INTEGER): Rating (1-5)


"""
Nova Data Generator - Main execution script.
"""
import yaml
import logging
from datetime import datetime
import sys

from utils.random_utils import RandomGenerator
from generators.product_generator import ProductGenerator
from generators.sales_generator import SalesGenerator
from generators.transaction_generator import TransactionGenerator
from generators.campaign_generator import CampaignGenerator

from generators.social_generator import SocialGenerator
from generators.review_generator import ReviewGenerator
from output.csv_writer import write_csv
from output.json_writer import write_json
from output.metadata_writer import generate_data_dictionary, generate_log

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config/config.yaml') -> dict:
    """Load configuration from YAML file."""
    import os
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_config_path = os.path.join(script_dir, config_path)
    
    try:
        with open(full_config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"✓ Loaded configuration from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)


def main():
    """Main data generation pipeline."""
    print("="*60)
    print("Nova Data Generator")
    print("="*60)
    print()
    
    # Load configuration
    config = load_config()
    
    # Initialize random generator
    rng = RandomGenerator(seed=config['random_seed'])
    logger.info(f"✓ Initialized random generator with seed {config['random_seed']}")
    
    # Track generation log
    log_entries = []
    datasets_info = {}
    
    # 1. Generate Products
    logger.info("Step 1/6: Generating product master data...")
    product_gen = ProductGenerator(config, rng)
    products_df = product_gen.generate_products()
    write_csv(products_df, 'dim_products.csv', config['output']['data_dir'])
    
    log_entries.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': 'Products',
        'record_count': len(products_df),
        'status': 'SUCCESS'
    })
    
    datasets_info['Products'] = {
        'filename': 'dim_products.csv',
        'description': 'Product master data with specifications',
        'record_count': len(products_df),
        'fields': [
            {'name': 'product_id', 'type': 'STRING', 'description': 'Unique product identifier'},
            {'name': 'product_name', 'type': 'STRING', 'description': 'Product name'},
            {'name': 'product_line', 'type': 'STRING', 'description': 'Product line (Prime, Flex, Plus, etc.)'},
            {'name': 'price_usd', 'type': 'DECIMAL', 'description': 'Product price in USD'},
        ]
    }
    
    # 2. Generate Sales
    logger.info("Step 2/6: Generating daily sales data...")
    sales_gen = SalesGenerator(products_df, config, rng)
    sales_df = sales_gen.generate_daily_sales()
    write_csv(sales_df, 'fact_daily_sales.csv', config['output']['data_dir'])
    
    log_entries.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': 'Daily Sales',
        'record_count': len(sales_df),
        'date_range': f"{sales_df['date'].min()} to {sales_df['date'].max()}",
        'status': 'SUCCESS'
    })
    
    datasets_info['Daily Sales'] = {
        'filename': 'fact_daily_sales.csv',
        'description': 'Daily sales transactions by product, region, and channel',
        'record_count': len(sales_df),
        'date_range': f"{sales_df['date'].min()} to {sales_df['date'].max()}",
        'fields': [
            {'name': 'date', 'type': 'DATE', 'description': 'Sale date'},
            {'name': 'product_id', 'type': 'STRING', 'description': 'Product identifier'},
            {'name': 'units_sold', 'type': 'INTEGER', 'description': 'Number of units sold'},
            {'name': 'revenue_usd', 'type': 'DECIMAL', 'description': 'Revenue in USD'},
        ]
    }
    
    # 3. Generate Transactions
    logger.info("Step 3/6: Generating customer transactions...")
    transaction_gen = TransactionGenerator(products_df, sales_df, config, rng)
    transactions_df = transaction_gen.generate_transactions()
    write_csv(transactions_df, 'fact_transactions.csv', config['output']['data_dir'])
    
    log_entries.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': 'Transactions',
        'record_count': len(transactions_df),
        'status': 'SUCCESS'
    })
    
    datasets_info['Transactions'] = {
        'filename': 'fact_transactions.csv',
        'description': 'Customer transaction details with segments and demographics',
        'record_count': len(transactions_df),
        'fields': [
            {'name': 'transaction_id', 'type': 'STRING', 'description': 'Unique transaction identifier'},
            {'name': 'customer_id', 'type': 'STRING', 'description': 'Customer identifier'},
            {'name': 'customer_segment', 'type': 'STRING', 'description': 'Customer segment'},
        ]
    }
    
    # 4. Generate Campaigns
    logger.info("Step 4/6: Generating campaign performance data...")
    campaign_gen = CampaignGenerator(products_df, config, rng)
    campaigns_df = campaign_gen.generate_campaigns()
    write_csv(campaigns_df, 'fact_campaign_performance.csv', config['output']['data_dir'])
    
    log_entries.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': 'Campaigns',
        'record_count': len(campaigns_df),
        'status': 'SUCCESS'
    })
    
    datasets_info['Campaigns'] = {
        'filename': 'fact_campaign_performance.csv',
        'description': 'Marketing campaign performance metrics',
        'record_count': len(campaigns_df),
        'fields': [
            {'name': 'campaign_id', 'type': 'STRING', 'description': 'Campaign identifier'},
            {'name': 'channel', 'type': 'STRING', 'description': 'Marketing channel'},
            {'name': 'roi', 'type': 'DECIMAL', 'description': 'Return on investment'},
        ]
    }
    
    # 5. Generate Social Media Posts
    logger.info("Step 5/6: Generating social media posts...")
    social_gen = SocialGenerator(products_df, config, rng)
    social_posts = social_gen.generate_posts()
    write_json(social_posts, 'social_media_posts.json', config['output']['data_dir'])
    
    log_entries.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': 'Social Media Posts',
        'record_count': len(social_posts),
        'status': 'SUCCESS'
    })
    
    datasets_info['Social Media Posts'] = {
        'filename': 'social_media_posts.json',
        'description': 'Social media posts with sentiment analysis',
        'record_count': len(social_posts),
        'fields': [
            {'name': 'post_id', 'type': 'STRING', 'description': 'Post identifier'},
            {'name': 'sentiment', 'type': 'STRING', 'description': 'Sentiment classification'},
        ]
    }
    
    # 6. Generate Reviews
    logger.info("Step 6/6: Generating product reviews...")
    review_gen = ReviewGenerator(products_df, transactions_df, config, rng)
    reviews = review_gen.generate_reviews()
    write_json(reviews, 'product_reviews.json', config['output']['data_dir'])
    
    log_entries.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dataset': 'Product Reviews',
        'record_count': len(reviews),
        'status': 'SUCCESS'
    })
    
    datasets_info['Product Reviews'] = {
        'filename': 'product_reviews.json',
        'description': 'Amazon-style product reviews with ratings and feedback',
        'record_count': len(reviews),
        'fields': [
            {'name': 'review_id', 'type': 'STRING', 'description': 'Review identifier'},
            {'name': 'rating', 'type': 'INTEGER', 'description': 'Rating (1-5)'},
        ]
    }
    
    # Generate metadata
    logger.info("Generating metadata and documentation...")
    generate_data_dictionary(datasets_info, config['output']['data_dir'])
    generate_log(log_entries, config['output']['data_dir'])
    
    print()
    print("="*60)
    print("✓ Data generation completed successfully!")
    print("="*60)
    print(f"\nGenerated {len(datasets_info)} datasets:")
    for name, info in datasets_info.items():
        print(f"  - {name}: {info['record_count']} records")
    print(f"\nOutput directory: {config['output']['data_dir']}/")
    print()


if __name__ == '__main__':
    main()

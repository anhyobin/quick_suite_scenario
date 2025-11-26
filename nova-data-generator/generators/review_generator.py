"""
Amazon-style product reviews generator.
"""
from typing import Dict, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.random_utils import RandomGenerator
from utils.text_utils import generate_review_text, generate_pros_cons
from utils.date_utils import parse_date, add_days, format_date
import pandas as pd


class ReviewGenerator:
    """Generate Amazon-style product reviews."""
    
    RATING_DISTRIBUTION = {5: 0.40, 4: 0.30, 3: 0.15, 2: 0.10, 1: 0.05}
    
    def __init__(self, products_df: pd.DataFrame, transactions_df: pd.DataFrame, 
                 config: Dict, rng: RandomGenerator):
        self.products_df = products_df
        self.transactions_df = transactions_df
        self.config = config
        self.rng = rng
        self.reviews = []
    
    def generate_reviews(self) -> List[Dict]:
        """Generate product reviews."""
        review_id = 1
        
        for _, product in self.products_df.iterrows():
            # Get transactions for this product
            product_transactions = self.transactions_df[
                self.transactions_df['product_id'] == product['product_id']
            ]
            
            # Generate reviews (not all customers leave reviews)
            num_reviews = self.rng.randint(
                self.config['reviews']['min_per_product'],
                self.config['reviews']['max_per_product']
            )
            
            # Sample transactions
            if len(product_transactions) > 0:
                sampled_txns = product_transactions.sample(
                    n=min(num_reviews, len(product_transactions)),
                    random_state=self.rng.seed
                )
            else:
                continue
            
            for _, txn in sampled_txns.iterrows():
                # Select rating based on distribution
                rating = self.rng.weighted_choice(
                    list(self.RATING_DISTRIBUTION.keys()),
                    list(self.RATING_DISTRIBUTION.values())
                )
                
                # Review date (7-30 days after purchase)
                # Parse transaction_datetime (now includes time)
                if 'T' in txn['transaction_datetime']:
                    purchase_date = parse_date(txn['transaction_datetime'].split('T')[0])
                else:
                    purchase_date = parse_date(txn['transaction_datetime'])
                
                days_after = self.rng.randint(7, 30)
                review_date = add_days(purchase_date, days_after)
                
                # Add random time for review
                hour = self.rng.randint(0, 23)
                minute = self.rng.randint(0, 59)
                second = self.rng.randint(0, 59)
                review_date = review_date.replace(hour=hour, minute=minute, second=second)
                
                # Generate review text
                review_content = generate_review_text(rating, product['product_name'], self.rng)
                
                # Generate pros/cons
                pros_cons = generate_pros_cons(rating, self.rng)
                
                # Verified purchase (85%)
                verified_purchase = self.rng.random() < 0.85
                
                # Helpful votes (higher ratings get more votes)
                if rating >= 4:
                    total_votes = self.rng.randint(10, 100)
                    helpful_votes = int(total_votes * self.rng.uniform(0.7, 0.95))
                else:
                    total_votes = self.rng.randint(5, 50)
                    helpful_votes = int(total_votes * self.rng.uniform(0.5, 0.8))
                
                # Reviewer profile
                reviewer_profile = {
                    'total_reviews': self.rng.randint(1, 50),
                    'verified_purchases': self.rng.randint(1, 40)
                }
                
                # Variant (color and storage from product)
                colors = product['color_options'].split(',')
                variant = {
                    'color': self.rng.choice(colors),
                    'storage': f"{product['storage_gb']}GB"
                }
                
                review = {
                    'review_id': f'REV-{review_id:08d}',
                    'product_id': product['product_id'],
                    'customer_id': txn['customer_id'],
                    'review_datetime': review_date.strftime('%Y-%m-%dT%H:%M:%S'),
                    'purchase_datetime': txn['transaction_datetime'],
                    'verified_purchase': verified_purchase,
                    'rating': rating,
                    'review_title': review_content['title'],
                    'review_text': review_content['text'],
                    'pros': pros_cons['pros'],
                    'cons': pros_cons['cons'],
                    'helpful_votes': helpful_votes,
                    'total_votes': total_votes,
                    'reviewer_profile': reviewer_profile,
                    'variant': variant
                }
                
                self.reviews.append(review)
                review_id += 1
        
        return self.reviews

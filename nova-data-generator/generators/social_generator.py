"""
Social media posts generator.
"""
import json
from datetime import datetime
from typing import Dict, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.random_utils import RandomGenerator
from utils.text_utils import generate_social_post, generate_hashtags
from utils.date_utils import parse_date, add_days, format_date
import pandas as pd


class SocialGenerator:
    """Generate social media posts data."""
    
    PLATFORMS = ['Twitter', 'Instagram', 'Facebook']
    SENTIMENT_DISTRIBUTION = {'positive': 0.60, 'neutral': 0.25, 'negative': 0.15}
    
    def __init__(self, products_df: pd.DataFrame, config: Dict, rng: RandomGenerator):
        self.products_df = products_df
        self.config = config
        self.rng = rng
        self.posts = []
    
    def generate_posts(self) -> List[Dict]:
        """Generate social media posts."""
        post_id = 1
        
        for _, product in self.products_df.iterrows():
            launch_date = parse_date(product['launch_date'])
            
            # Generate posts for 6 months after launch
            for month in range(6):
                posts_this_month = self.config['social_posts']['posts_per_product_per_month']
                
                # More posts in first month
                if month == 0:
                    posts_this_month = int(posts_this_month * 1.5)
                
                for _ in range(posts_this_month):
                    # Random date in this month
                    days_offset = month * 30 + self.rng.randint(0, 29)
                    post_date = add_days(launch_date, days_offset)
                    
                    # Add random time (24 hours)
                    hour = self.rng.randint(0, 23)
                    minute = self.rng.randint(0, 59)
                    second = self.rng.randint(0, 59)
                    post_date = post_date.replace(hour=hour, minute=minute, second=second)
                    
                    # Select sentiment
                    sentiment = self.rng.weighted_choice(
                        list(self.SENTIMENT_DISTRIBUTION.keys()),
                        list(self.SENTIMENT_DISTRIBUTION.values())
                    )
                    
                    # Generate post text
                    text = generate_social_post(sentiment, product['product_name'], self.rng)
                    
                    # Generate hashtags
                    hashtags = generate_hashtags(product['product_line'], sentiment, self.rng)
                    
                    # Sentiment score
                    if sentiment == 'positive':
                        sentiment_score = self.rng.uniform(0.5, 1.0)
                    elif sentiment == 'negative':
                        sentiment_score = self.rng.uniform(-1.0, -0.5)
                    else:
                        sentiment_score = self.rng.uniform(-0.3, 0.3)
                    
                    # Engagement metrics
                    platform = self.rng.choice(self.PLATFORMS)
                    followers = self.rng.randint(100, 50000)
                    
                    if sentiment == 'positive':
                        likes = int(followers * self.rng.uniform(0.02, 0.10))
                        comments = int(likes * self.rng.uniform(0.05, 0.15))
                        shares = int(likes * self.rng.uniform(0.02, 0.08))
                    else:
                        likes = int(followers * self.rng.uniform(0.005, 0.03))
                        comments = int(likes * self.rng.uniform(0.10, 0.25))
                        shares = int(likes * self.rng.uniform(0.01, 0.05))
                    
                    post = {
                        'post_id': f'SM-{post_id:08d}',
                        'timestamp': post_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'platform': platform,
                        'user_id': f'user_{self.rng.randint(10000, 99999)}',
                        'user_followers': followers,
                        'text': text,
                        'product_mentioned': product['product_id'],
                        'hashtags': hashtags,
                        'sentiment': sentiment,
                        'sentiment_score': round(sentiment_score, 2),
                        'engagement': {
                            'likes': likes,
                            'comments': comments,
                            'shares': shares
                        },
                        'language': 'en'
                    }
                    
                    self.posts.append(post)
                    post_id += 1
        
        return self.posts

"""
Campaign performance data generator.
"""
import pandas as pd
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.random_utils import RandomGenerator
from utils.date_utils import parse_date, add_days, format_date


class CampaignGenerator:
    """Generate marketing campaign performance data."""
    
    CHANNELS = {
        'Social Media': {
            'impressions': (1000000, 5000000),
            'ctr': (0.005, 0.015),
            'conversion': (0.02, 0.04),
            'budget': (50000, 200000)
        },
        'Search': {
            'impressions': (100000, 500000),
            'ctr': (0.03, 0.08),
            'conversion': (0.05, 0.10),
            'budget': (30000, 150000)
        },
        'Display': {
            'impressions': (2000000, 10000000),
            'ctr': (0.003, 0.008),
            'conversion': (0.01, 0.02),
            'budget': (40000, 180000)
        },
        'TV': {
            'impressions': (10000000, 50000000),
            'ctr': (0, 0),  # Not measurable
            'conversion': (0, 0),  # Indirect
            'budget': (200000, 1000000)
        },
        'Email': {
            'impressions': (50000, 200000),
            'ctr': (0.10, 0.20),
            'conversion': (0.03, 0.06),
            'budget': (10000, 50000)
        },
        'Influencer': {
            'impressions': (500000, 2000000),
            'ctr': (0.02, 0.05),
            'conversion': (0.05, 0.08),
            'budget': (30000, 150000)
        }
    }
    
    REGIONS = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    
    def __init__(self, products_df: pd.DataFrame, config: Dict, rng: RandomGenerator):
        self.products_df = products_df
        self.config = config
        self.rng = rng
        self.campaigns = []
    
    def generate_campaigns(self) -> pd.DataFrame:
        """Generate campaign performance data."""
        campaign_id = 1
        
        for _, product in self.products_df.iterrows():
            launch_date = parse_date(product['launch_date'])
            
            # Generate 2-3 campaigns per product around launch
            num_campaigns = self.rng.randint(2, 3)
            
            for i in range(num_campaigns):
                # Campaign timing (before and after launch)
                days_offset = self.rng.randint(-30, 60)
                start_date = add_days(launch_date, days_offset)
                end_date = add_days(start_date, self.rng.randint(14, 45))
                
                # Select channel and region
                channel = self.rng.choice(list(self.CHANNELS.keys()))
                region = self.rng.choice(self.REGIONS)
                
                # Get channel specs
                specs = self.CHANNELS[channel]
                
                # Generate metrics
                budget = self.rng.randint(specs['budget'][0], specs['budget'][1])
                impressions = self.rng.randint(specs['impressions'][0], specs['impressions'][1])
                
                if specs['ctr'][1] > 0:
                    ctr = self.rng.uniform(specs['ctr'][0], specs['ctr'][1])
                    clicks = int(impressions * ctr)
                    
                    conversion_rate = self.rng.uniform(specs['conversion'][0], specs['conversion'][1])
                    conversions = int(clicks * conversion_rate)
                    
                    # Estimate revenue (conversions * product price)
                    revenue = conversions * product['price_usd']
                else:
                    ctr = 0
                    clicks = 0
                    conversion_rate = 0
                    conversions = 0
                    revenue = budget * self.rng.uniform(0.5, 1.5)  # Indirect effect
                
                # Calculate ROI
                roi = (revenue - budget) / budget if budget > 0 else 0
                
                campaign = {
                    'campaign_id': f'CMP-{campaign_id:05d}',
                    'campaign_name': f'{product["product_name"]} {channel} Campaign',
                    'start_date': format_date(start_date),
                    'end_date': format_date(end_date),
                    'product_id': product['product_id'],
                    'channel': channel,
                    'region': region,
                    'budget_usd': budget,
                    'impressions': impressions,
                    'clicks': clicks,
                    'ctr': round(ctr, 4),
                    'conversions': conversions,
                    'conversion_rate': round(conversion_rate, 4),
                    'revenue_usd': round(revenue, 2),
                    'roi': round(roi, 2)
                }
                
                self.campaigns.append(campaign)
                campaign_id += 1
        
        return pd.DataFrame(self.campaigns)

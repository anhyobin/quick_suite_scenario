"""
Sales fact data generator.
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.random_utils import RandomGenerator
from utils.date_utils import (
    generate_date_range, parse_date, get_days_between,
    is_holiday_season, is_back_to_school_season
)


class SalesGenerator:
    """Generate daily sales fact data."""
    
    # Regions and their weights
    REGIONS = {
        'North America': 0.30,
        'Europe': 0.25,
        'Asia Pacific': 0.35,
        'Latin America': 0.07,
        'Middle East': 0.03
    }
    
    # Countries by region
    COUNTRIES = {
        'North America': ['USA', 'Canada', 'Mexico'],
        'Europe': ['UK', 'Germany', 'France', 'Spain', 'Italy'],
        'Asia Pacific': ['Japan', 'South Korea', 'Australia', 'Singapore', 'India'],
        'Latin America': ['Brazil', 'Argentina', 'Chile'],
        'Middle East': ['UAE', 'Saudi Arabia', 'Qatar']
    }
    
    # Channels and their distribution
    CHANNELS = {
        'Amazon': {'type': 'Online', 'weight': 0.25},
        'TechMart': {'type': 'Online', 'weight': 0.15},
        'MegaStore Online': {'type': 'Online', 'weight': 0.12},
        'Nova Direct': {'type': 'Online', 'weight': 0.08},
        'TechMart Stores': {'type': 'Offline', 'weight': 0.15},
        'MegaStore Retail': {'type': 'Offline', 'weight': 0.12},
        'CarrierShops': {'type': 'Offline', 'weight': 0.08},
        'Nova Flagship Stores': {'type': 'Offline', 'weight': 0.05}
    }
    
    # Return rates by product line
    RETURN_RATES = {
        'Prime': (0.02, 0.03),
        'Flex Fold': (0.02, 0.03),
        'Flex Flip': (0.025, 0.035),
        'Plus': (0.03, 0.04),
        'Lite': (0.04, 0.05),
        'Max': (0.025, 0.035),
        'Mini': (0.03, 0.04)
    }
    
    def __init__(self, products_df: pd.DataFrame, config: Dict, rng: RandomGenerator):
        """
        Initialize sales generator.
        
        Args:
            products_df: Product master DataFrame
            config: Configuration dictionary
            rng: Random generator instance
        """
        self.products_df = products_df
        self.config = config
        self.rng = rng
        self.sales_data = []
    
    def generate_daily_sales(self) -> pd.DataFrame:
        """
        Generate daily sales data for all products.
        
        Returns:
            DataFrame with daily sales data
        """
        start_date = parse_date(self.config['date_range']['start_date'])
        end_date = parse_date(self.config['date_range']['end_date'])
        
        # Generate sales for each product
        for _, product in self.products_df.iterrows():
            self._generate_product_sales(product, start_date, end_date)
        
        df = pd.DataFrame(self.sales_data)
        return df

    
    def _generate_product_sales(self, product: pd.Series, start_date: datetime, end_date: datetime):
        """Generate sales data for a single product."""
        product_launch = parse_date(product['launch_date'])
        product_discontinue = parse_date(product['discontinue_date']) if pd.notna(product['discontinue_date']) else end_date
        
        # Only generate sales between launch and discontinue dates
        sales_start = max(product_launch, start_date)
        sales_end = min(product_discontinue, end_date)
        
        if sales_start >= sales_end:
            return
        
        # Generate date range
        dates = generate_date_range(sales_start.strftime('%Y-%m-%d'), sales_end.strftime('%Y-%m-%d'), freq='D')
        
        # Get return rate range for this product line
        return_rate_range = self.RETURN_RATES.get(product['product_line'], (0.03, 0.04))
        
        for date in dates:
            # Calculate lifecycle stage
            days_since_launch = get_days_between(product_launch, date)
            base_units = self._get_base_units_by_lifecycle(days_since_launch)
            
            # Apply seasonality
            seasonal_multiplier = self._get_seasonal_multiplier(date)
            base_units = int(base_units * seasonal_multiplier)
            
            # Generate sales for each region and channel
            for region, region_weight in self.REGIONS.items():
                # Select a country from this region
                country = self.rng.choice(self.COUNTRIES[region])
                
                for channel, channel_info in self.CHANNELS.items():
                    # Calculate units sold
                    units_sold = int(base_units * region_weight * channel_info['weight'])
                    
                    # Add some randomness
                    units_sold = max(0, int(units_sold * self.rng.uniform(0.8, 1.2)))
                    
                    if units_sold == 0:
                        continue
                    
                    # Calculate revenue
                    revenue_usd = units_sold * product['price_usd']
                    
                    # Calculate returns
                    return_rate = self.rng.uniform(return_rate_range[0], return_rate_range[1])
                    units_returned = int(units_sold * return_rate)
                    
                    sale_record = {
                        'date': date.strftime('%Y-%m-%d'),
                        'product_id': product['product_id'],
                        'region': region,
                        'country': country,
                        'channel': channel,
                        'channel_type': channel_info['type'],
                        'units_sold': units_sold,
                        'revenue_usd': round(revenue_usd, 2),
                        'units_returned': units_returned,
                        'return_rate': round(return_rate, 4)
                    }
                    
                    self.sales_data.append(sale_record)
    
    def _get_base_units_by_lifecycle(self, days_since_launch: int) -> int:
        """
        Get base daily units based on product lifecycle stage.
        
        Args:
            days_since_launch: Number of days since product launch
        
        Returns:
            Base daily units (reduced for demo purposes)
        """
        if days_since_launch < 90:  # 0-3 months: Introduction
            # Gradual increase from 5 to 20
            return int(5 + (days_since_launch / 90) * 15)
        elif days_since_launch < 365:  # 3-12 months: Growth
            # Increase from 20 to 100
            progress = (days_since_launch - 90) / 275
            return int(20 + progress * 80)
        elif days_since_launch < 730:  # 12-24 months: Maturity
            # Maintain high sales 80-120
            return self.rng.randint(80, 120)
        else:  # 24+ months: Decline
            # Gradual decrease from 60 to 30
            days_in_decline = days_since_launch - 730
            decline_factor = max(0.3, 1 - (days_in_decline / 365) * 0.5)
            return int(60 * decline_factor)
    
    def _get_seasonal_multiplier(self, date: datetime) -> float:
        """
        Get seasonal multiplier for sales.
        
        Args:
            date: Date to check
        
        Returns:
            Multiplier (1.0 = normal, >1.0 = increased sales)
        """
        if is_holiday_season(date):
            return 1.25  # +25% for holiday season
        elif is_back_to_school_season(date):
            return 1.15  # +15% for back-to-school
        elif date.month in [1, 2]:
            return 0.90  # -10% for post-holiday slowdown
        else:
            return 1.0

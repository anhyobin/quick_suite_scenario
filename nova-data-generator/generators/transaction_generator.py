"""
Transaction data generator.
"""
import pandas as pd
from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.random_utils import RandomGenerator


class TransactionGenerator:
    """Generate customer transaction data."""
    
    CUSTOMER_SEGMENTS = {
        'Tech Enthusiast': 0.25,
        'Budget Conscious': 0.30,
        'Premium Seeker': 0.20,
        'Casual User': 0.25
    }
    
    AGE_GROUPS = ['18-24', '25-34', '35-44', '45-54', '55+']
    INCOME_LEVELS = ['Low', 'Medium', 'High']
    
    # Segment preferences for product lines
    SEGMENT_PREFERENCES = {
        'Tech Enthusiast': ['Prime', 'Flex Fold', 'Flex Flip'],
        'Budget Conscious': ['Lite', 'Plus'],
        'Premium Seeker': ['Prime', 'Max', 'Flex Fold'],
        'Casual User': ['Plus', 'Lite', 'Mini']
    }
    
    def __init__(self, products_df: pd.DataFrame, sales_df: pd.DataFrame, 
                 config: Dict, rng: RandomGenerator):
        self.products_df = products_df
        self.sales_df = sales_df
        self.config = config
        self.rng = rng
        self.transactions = []
        self.customer_history = {}  # Track customer purchases
    
    def generate_transactions(self) -> pd.DataFrame:
        """Generate transaction data based on sales data."""
        # Sample transactions from sales (not every sale needs a detailed transaction)
        sampled_sales = self.sales_df.sample(frac=0.3, random_state=self.rng.seed)
        
        transaction_id = 1
        for _, sale in sampled_sales.iterrows():
            # Generate multiple transactions for this sale record
            num_transactions = max(1, int(sale['units_sold'] * 0.1))  # 10% of units
            
            for _ in range(num_transactions):
                customer_id = self._get_or_create_customer()
                product = self.products_df[self.products_df['product_id'] == sale['product_id']].iloc[0]
                
                # Determine if repeat customer
                is_repeat = customer_id in self.customer_history
                previous_product_id = self.customer_history.get(customer_id) if is_repeat else None
                
                # Calculate discount
                discount_pct = self._get_discount_rate(sale['channel'], sale['channel_type'])
                discount_amount = round(product['price_usd'] * discount_pct, 2)
                price_paid = round(product['price_usd'] - discount_amount, 2)
                
                # Get customer attributes
                segment = self._get_customer_segment(product['product_line'])
                age_group = self.rng.choice(self.AGE_GROUPS)
                income_level = self.rng.choice(self.INCOME_LEVELS)
                
                # Generate datetime with random hour (business hours 9-21)
                hour = self.rng.randint(9, 21)
                minute = self.rng.randint(0, 59)
                second = self.rng.randint(0, 59)
                transaction_datetime = f"{sale['date']}T{hour:02d}:{minute:02d}:{second:02d}"
                
                transaction = {
                    'transaction_id': f'TXN-{transaction_id:08d}',
                    'transaction_datetime': transaction_datetime,
                    'customer_id': customer_id,
                    'product_id': sale['product_id'],
                    'price_paid': price_paid,
                    'discount_amount': discount_amount,
                    'channel': sale['channel'],
                    'region': sale['region'],
                    'country': sale['country'],
                    'customer_segment': segment,
                    'age_group': age_group,
                    'income_level': income_level,
                    'is_repeat_customer': is_repeat,
                    'previous_product_id': previous_product_id if previous_product_id else ''
                }
                
                self.transactions.append(transaction)
                self.customer_history[customer_id] = sale['product_id']
                transaction_id += 1
        
        return pd.DataFrame(self.transactions)
    
    def _get_or_create_customer(self) -> str:
        """Get existing customer or create new one."""
        # 30% chance of repeat customer
        if self.customer_history and self.rng.random() < 0.30:
            return self.rng.choice(list(self.customer_history.keys()))
        else:
            return f'CUST-{self.rng.randint(100000, 999999)}'
    
    def _get_customer_segment(self, product_line: str) -> str:
        """Determine customer segment based on product line."""
        # Find segments that prefer this product line
        matching_segments = [seg for seg, prefs in self.SEGMENT_PREFERENCES.items() 
                           if product_line in prefs]
        
        if matching_segments:
            return self.rng.choice(matching_segments)
        else:
            return self.rng.weighted_choice(
                list(self.CUSTOMER_SEGMENTS.keys()),
                list(self.CUSTOMER_SEGMENTS.values())
            )
    
    def _get_discount_rate(self, channel: str, channel_type: str) -> float:
        """Calculate discount rate based on channel."""
        if channel_type == 'Online':
            base_discount = self.rng.uniform(0.10, 0.15)
        else:
            base_discount = self.rng.uniform(0.05, 0.10)
        
        # Random promotion periods
        if self.rng.random() < 0.15:  # 15% chance of promotion
            base_discount = min(0.30, base_discount + self.rng.uniform(0.10, 0.15))
        
        return base_discount

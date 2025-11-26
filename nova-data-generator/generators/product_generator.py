"""
Product master data generator.
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.random_utils import RandomGenerator
from utils.date_utils import format_date, parse_date, add_months


class ProductGenerator:
    """Generate product master data for Nova smartphone brand."""
    
    # Product line specifications
    PRODUCT_SPECS = {
        'Prime': {
            'price_range': (999, 1299),
            'camera_range': (108, 200),
            'battery_range': (5000, 5500),
            'display_range': (6.7, 6.9),
            'storage_options': [256, 512, 1024],
            'ram_options': [12, 16],
            'processors': ['Snapdragon 8 Gen 3', 'Exynos 2400'],
            'weight_range': (195, 210)
        },
        'Flex Fold': {
            'price_range': (1799, 2199),
            'camera_range': (50, 108),
            'battery_range': (4400, 4800),
            'display_range': (7.6, 8.0),
            'storage_options': [256, 512],
            'ram_options': [12, 16],
            'processors': ['Snapdragon 8 Gen 2', 'Snapdragon 8 Gen 3'],
            'weight_range': (250, 280)
        },
        'Flex Flip': {
            'price_range': (999, 1199),
            'camera_range': (12, 50),
            'battery_range': (3700, 4000),
            'display_range': (6.7, 6.7),
            'storage_options': [256, 512],
            'ram_options': [8, 12],
            'processors': ['Snapdragon 8+ Gen 1', 'Snapdragon 8 Gen 2'],
            'weight_range': (185, 195)
        },
        'Plus': {
            'price_range': (599, 799),
            'camera_range': (64, 108),
            'battery_range': (4500, 5000),
            'display_range': (6.5, 6.7),
            'storage_options': [128, 256],
            'ram_options': [6, 8],
            'processors': ['Snapdragon 778G', 'Snapdragon 7 Gen 1'],
            'weight_range': (180, 195)
        },
        'Lite': {
            'price_range': (299, 499),
            'camera_range': (48, 64),
            'battery_range': (4000, 4500),
            'display_range': (6.4, 6.6),
            'storage_options': [64, 128],
            'ram_options': [4, 6],
            'processors': ['Snapdragon 695', 'MediaTek Dimensity 700'],
            'weight_range': (175, 190)
        },
        'Max': {
            'price_range': (899, 1099),
            'camera_range': (108, 108),
            'battery_range': (5500, 6000),
            'display_range': (6.9, 7.2),
            'storage_options': [256, 512],
            'ram_options': [8, 12],
            'processors': ['Snapdragon 8 Gen 2', 'Snapdragon 8 Gen 3'],
            'weight_range': (220, 240)
        },
        'Mini': {
            'price_range': (699, 899),
            'camera_range': (50, 64),
            'battery_range': (3500, 4000),
            'display_range': (5.4, 5.8),
            'storage_options': [128, 256],
            'ram_options': [6, 8],
            'processors': ['Snapdragon 8 Gen 1', 'Snapdragon 8 Gen 2'],
            'weight_range': (160, 175)
        }
    }
    
    COLOR_OPTIONS = [
        'Midnight Black,Phantom Silver,Aurora Blue',
        'Cosmic Gray,Pearl White,Rose Gold',
        'Graphite,Silver,Gold',
        'Black,White,Blue,Green',
        'Phantom Black,Cream,Lavender'
    ]
    
    def __init__(self, config: Dict, rng: RandomGenerator):
        """
        Initialize product generator.
        
        Args:
            config: Configuration dictionary
            rng: Random generator instance
        """
        self.config = config
        self.rng = rng
        self.products = []
    
    def generate_products(self) -> pd.DataFrame:
        """
        Generate all product data.
        
        Returns:
            DataFrame with product master data
        """
        product_lines = self.config['products']['lines']
        start_date = parse_date(self.config['date_range']['start_date'])
        
        for line_config in product_lines:
            line_name = line_config['name']
            series_count = line_config['series_count']
            
            self._generate_product_line(line_name, series_count, start_date)
        
        df = pd.DataFrame(self.products)
        return df
    
    def _generate_product_line(self, line_name: str, series_count: int, start_date: datetime):
        """Generate products for a specific product line."""
        specs = self.PRODUCT_SPECS[line_name]
        
        # Generate series (e.g., 24, 23, 22 for years)
        current_year = 2024
        for i in range(series_count):
            year = current_year - i
            series = str(year % 100)  # 24, 23, 22
            
            # Generate launch date (spread across the year)
            month_offset = i * 6  # Space out launches
            launch_date = add_months(start_date, month_offset)
            
            # Generate product ID
            line_id = line_name.upper().replace(' ', '-')
            product_id = f"{line_id}-{series}"
            
            # Generate product name
            product_name = f"Nova {line_name} {series}"
            
            # Generate specs
            price = self.rng.randint(specs['price_range'][0], specs['price_range'][1])
            camera_mp = self.rng.randint(specs['camera_range'][0], specs['camera_range'][1])
            battery_mah = self.rng.randint(specs['battery_range'][0], specs['battery_range'][1])
            display_inch = round(self.rng.uniform(specs['display_range'][0], specs['display_range'][1]), 1)
            storage_gb = self.rng.choice(specs['storage_options'])
            ram_gb = self.rng.choice(specs['ram_options'])
            processor = self.rng.choice(specs['processors'])
            color_options = self.rng.choice(self.COLOR_OPTIONS)
            weight_g = self.rng.randint(specs['weight_range'][0], specs['weight_range'][1])
            
            # Discontinue date (24-36 months after launch, or None for recent products)
            if i >= series_count - 1:  # Most recent product
                discontinue_date = None
            else:
                months_to_discontinue = self.rng.randint(24, 36)
                discontinue_date = format_date(add_months(launch_date, months_to_discontinue))
            
            product = {
                'product_id': product_id,
                'product_name': product_name,
                'product_line': line_name,
                'series': series,
                'launch_date': format_date(launch_date),
                'discontinue_date': discontinue_date,
                'price_usd': price,
                'camera_mp': camera_mp,
                'battery_mah': battery_mah,
                'display_inch': display_inch,
                'storage_gb': storage_gb,
                'ram_gb': ram_gb,
                'processor': processor,
                'color_options': color_options,
                'weight_g': weight_g
            }
            
            self.products.append(product)

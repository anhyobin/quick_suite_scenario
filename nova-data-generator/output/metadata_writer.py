"""
Metadata and documentation writer.
"""
import os
from datetime import datetime
import pandas as pd


def generate_data_dictionary(datasets_info: dict, output_dir: str = 'data'):
    """
    Generate data dictionary README file.
    
    Args:
        datasets_info: Dictionary with dataset information
        output_dir: Output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'DATA_DICTIONARY.md')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Nova Data Generator - Data Dictionary\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for dataset_name, info in datasets_info.items():
            f.write(f"## {dataset_name}\n\n")
            f.write(f"**File**: `{info['filename']}`\n\n")
            f.write(f"**Description**: {info['description']}\n\n")
            f.write(f"**Record Count**: {info['record_count']}\n\n")
            
            if 'date_range' in info:
                f.write(f"**Date Range**: {info['date_range']}\n\n")
            
            f.write("**Fields**:\n\n")
            for field in info['fields']:
                f.write(f"- `{field['name']}` ({field['type']}): {field['description']}\n")
            
            f.write("\n")
    
    print(f"✓ Generated data dictionary: {filepath}")
    return filepath


def generate_log(log_entries: list, output_dir: str = 'data'):
    """
    Generate generation log file.
    
    Args:
        log_entries: List of log entry dictionaries
        output_dir: Output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'generation.log')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Nova Data Generator - Generation Log\n")
        f.write(f"{'='*60}\n\n")
        
        for entry in log_entries:
            f.write(f"[{entry['timestamp']}] {entry['dataset']}\n")
            f.write(f"  Records: {entry['record_count']}\n")
            if 'date_range' in entry:
                f.write(f"  Date Range: {entry['date_range']}\n")
            f.write(f"  Status: {entry['status']}\n\n")
    
    print(f"✓ Generated log file: {filepath}")
    return filepath

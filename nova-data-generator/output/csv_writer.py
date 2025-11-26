"""
CSV file writer.
"""
import pandas as pd
import os


def write_csv(df: pd.DataFrame, filename: str, output_dir: str = 'data', encoding: str = 'utf-8'):
    """
    Write DataFrame to CSV file.
    
    Args:
        df: DataFrame to write
        filename: Output filename
        output_dir: Output directory
        encoding: File encoding (default: utf-8)
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False, encoding=encoding)
    print(f"✓ Wrote {len(df)} records to {filepath}")
    return filepath

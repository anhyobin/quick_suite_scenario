"""
JSON file writer.
"""
import json
import os


def write_json(data: list, filename: str, output_dir: str = 'data', indent: int = 2, encoding: str = 'utf-8'):
    """
    Write list of dictionaries to JSON file.
    
    Args:
        data: List of dictionaries to write
        filename: Output filename
        output_dir: Output directory
        indent: JSON indentation (default: 2)
        encoding: File encoding (default: utf-8)
    """
    import numpy as np
    
    def convert_to_native(obj):
        """Convert numpy types to native Python types."""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(item) for item in obj]
        return obj
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # Convert data
    converted_data = convert_to_native(data)
    
    with open(filepath, 'w', encoding=encoding) as f:
        json.dump(converted_data, f, indent=indent, ensure_ascii=False)
    
    print(f"✓ Wrote {len(data)} records to {filepath}")
    return filepath

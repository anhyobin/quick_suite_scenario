"""
Data validation utilities.
"""
import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def validate_foreign_keys(df: pd.DataFrame, fk_column: str, 
                          reference_df: pd.DataFrame, pk_column: str) -> bool:
    """
    Validate that all foreign key values exist in reference table.
    
    Args:
        df: DataFrame with foreign key column
        fk_column: Name of foreign key column
        reference_df: Reference DataFrame with primary key
        pk_column: Name of primary key column
    
    Returns:
        True if all foreign keys are valid, False otherwise
    """
    fk_values = set(df[fk_column].dropna().unique())
    pk_values = set(reference_df[pk_column].unique())
    
    invalid_fks = fk_values - pk_values
    
    if invalid_fks:
        logger.warning(f"Found {len(invalid_fks)} invalid foreign key values in {fk_column}")
        logger.warning(f"Invalid values: {list(invalid_fks)[:10]}")  # Show first 10
        return False
    
    logger.info(f"Foreign key validation passed for {fk_column}")
    return True


def validate_date_range(df: pd.DataFrame, date_column: str, 
                        min_date: str = None, max_date: str = None) -> bool:
    """
    Validate that dates are within expected range.
    
    Args:
        df: DataFrame with date column
        date_column: Name of date column
        min_date: Minimum allowed date (optional)
        max_date: Maximum allowed date (optional)
    
    Returns:
        True if all dates are valid, False otherwise
    """
    df[date_column] = pd.to_datetime(df[date_column])
    
    if min_date:
        min_date = pd.to_datetime(min_date)
        invalid_count = (df[date_column] < min_date).sum()
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} dates before {min_date} in {date_column}")
            return False
    
    if max_date:
        max_date = pd.to_datetime(max_date)
        invalid_count = (df[date_column] > max_date).sum()
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} dates after {max_date} in {date_column}")
            return False
    
    logger.info(f"Date range validation passed for {date_column}")
    return True


def validate_numeric_range(df: pd.DataFrame, column: str, 
                           min_val: float = None, max_val: float = None) -> bool:
    """
    Validate that numeric values are within expected range.
    
    Args:
        df: DataFrame with numeric column
        column: Name of numeric column
        min_val: Minimum allowed value (optional)
        max_val: Maximum allowed value (optional)
    
    Returns:
        True if all values are valid, False otherwise
    """
    if min_val is not None:
        invalid_count = (df[column] < min_val).sum()
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} values below {min_val} in {column}")
            return False
    
    if max_val is not None:
        invalid_count = (df[column] > max_val).sum()
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} values above {max_val} in {column}")
            return False
    
    logger.info(f"Numeric range validation passed for {column}")
    return True


def validate_no_nulls(df: pd.DataFrame, columns: List[str]) -> bool:
    """
    Validate that specified columns have no NULL values.
    
    Args:
        df: DataFrame to validate
        columns: List of column names that should not have NULLs
    
    Returns:
        True if no NULLs found, False otherwise
    """
    for column in columns:
        null_count = df[column].isnull().sum()
        if null_count > 0:
            logger.warning(f"Found {null_count} NULL values in required column {column}")
            return False
    
    logger.info(f"NULL validation passed for columns: {columns}")
    return True


def validate_data_types(df: pd.DataFrame, type_map: Dict[str, str]) -> bool:
    """
    Validate that columns have expected data types.
    
    Args:
        df: DataFrame to validate
        type_map: Dictionary mapping column names to expected types
                 (e.g., {'price': 'float', 'quantity': 'int'})
    
    Returns:
        True if all types are correct, False otherwise
    """
    for column, expected_type in type_map.items():
        actual_type = str(df[column].dtype)
        
        # Check type compatibility
        if expected_type == 'int' and 'int' not in actual_type:
            logger.warning(f"Column {column} has type {actual_type}, expected int")
            return False
        elif expected_type == 'float' and 'float' not in actual_type:
            logger.warning(f"Column {column} has type {actual_type}, expected float")
            return False
        elif expected_type == 'str' and 'object' not in actual_type:
            logger.warning(f"Column {column} has type {actual_type}, expected string")
            return False
    
    logger.info("Data type validation passed")
    return True


def validate_distribution(df: pd.DataFrame, column: str, 
                         expected_distribution: Dict[Any, float], 
                         tolerance: float = 0.05) -> bool:
    """
    Validate that value distribution matches expected proportions.
    
    Args:
        df: DataFrame to validate
        column: Column name to check distribution
        expected_distribution: Dictionary mapping values to expected proportions
        tolerance: Allowed deviation from expected proportion (default 5%)
    
    Returns:
        True if distribution is within tolerance, False otherwise
    """
    actual_counts = df[column].value_counts(normalize=True)
    
    for value, expected_prop in expected_distribution.items():
        actual_prop = actual_counts.get(value, 0)
        diff = abs(actual_prop - expected_prop)
        
        if diff > tolerance:
            logger.warning(
                f"Distribution mismatch for {value} in {column}: "
                f"expected {expected_prop:.2%}, got {actual_prop:.2%}"
            )
            return False
    
    logger.info(f"Distribution validation passed for {column}")
    return True


def validate_record_count(df: pd.DataFrame, min_count: int = None, 
                         max_count: int = None) -> bool:
    """
    Validate that DataFrame has expected number of records.
    
    Args:
        df: DataFrame to validate
        min_count: Minimum expected record count (optional)
        max_count: Maximum expected record count (optional)
    
    Returns:
        True if record count is valid, False otherwise
    """
    actual_count = len(df)
    
    if min_count and actual_count < min_count:
        logger.warning(f"Record count {actual_count} is below minimum {min_count}")
        return False
    
    if max_count and actual_count > max_count:
        logger.warning(f"Record count {actual_count} exceeds maximum {max_count}")
        return False
    
    logger.info(f"Record count validation passed: {actual_count} records")
    return True

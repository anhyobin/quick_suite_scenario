"""
Date utility functions for data generation.
"""
from datetime import datetime, timedelta
from typing import List
import pandas as pd


def generate_date_range(start_date: str, end_date: str, freq: str = 'D') -> List[datetime]:
    """
    Generate a list of dates between start_date and end_date.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        freq: Frequency ('D' for daily, 'W' for weekly, 'M' for monthly)
    
    Returns:
        List of datetime objects
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
    return date_range.tolist()


def add_days(date: datetime, days: int) -> datetime:
    """Add days to a date."""
    return date + timedelta(days=days)


def add_months(date: datetime, months: int) -> datetime:
    """Add months to a date (approximate)."""
    return date + timedelta(days=months * 30)


def format_date(date: datetime, format_str: str = '%Y-%m-%d') -> str:
    """
    Format datetime object to string.
    
    Args:
        date: Datetime object
        format_str: Format string (default: YYYY-MM-DD)
    
    Returns:
        Formatted date string
    """
    return date.strftime(format_str)


def parse_date(date_str: str, format_str: str = '%Y-%m-%d') -> datetime:
    """
    Parse date string to datetime object.
    
    Args:
        date_str: Date string
        format_str: Format string (default: YYYY-MM-DD)
    
    Returns:
        Datetime object
    """
    return datetime.strptime(date_str, format_str)


def get_month_number(date: datetime) -> int:
    """Get month number (1-12) from datetime."""
    return date.month


def get_days_between(start_date: datetime, end_date: datetime) -> int:
    """Calculate number of days between two dates."""
    return (end_date - start_date).days


def is_holiday_season(date: datetime) -> bool:
    """Check if date is in holiday season (November-December)."""
    return date.month in [11, 12]


def is_back_to_school_season(date: datetime) -> bool:
    """Check if date is in back-to-school season (August-September)."""
    return date.month in [8, 9]

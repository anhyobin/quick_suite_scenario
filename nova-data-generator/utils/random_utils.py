"""
Random number generation utilities with seed support.
"""
import random
import numpy as np
from typing import List, Any


class RandomGenerator:
    """Random number generator with seed support for reproducibility."""
    
    def __init__(self, seed: int = 42):
        """
        Initialize random generator with seed.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
    
    def randint(self, min_val: int, max_val: int) -> int:
        """Generate random integer between min_val and max_val (inclusive)."""
        return random.randint(min_val, max_val)
    
    def uniform(self, min_val: float, max_val: float) -> float:
        """Generate random float between min_val and max_val."""
        return random.uniform(min_val, max_val)
    
    def normal(self, mean: float, std: float) -> float:
        """Generate random number from normal distribution."""
        return np.random.normal(mean, std)
    
    def choice(self, items: List[Any]) -> Any:
        """Randomly select one item from list."""
        return random.choice(items)
    
    def choices(self, items: List[Any], weights: List[float] = None, k: int = 1) -> List[Any]:
        """
        Randomly select k items from list with optional weights.
        
        Args:
            items: List of items to choose from
            weights: Optional list of weights for each item
            k: Number of items to select
        
        Returns:
            List of selected items
        """
        return random.choices(items, weights=weights, k=k)
    
    def sample(self, items: List[Any], k: int) -> List[Any]:
        """Randomly select k unique items from list."""
        return random.sample(items, k)
    
    def shuffle(self, items: List[Any]) -> List[Any]:
        """Shuffle list in place and return it."""
        random.shuffle(items)
        return items
    
    def random(self) -> float:
        """Generate random float between 0 and 1."""
        return random.random()
    
    def weighted_choice(self, items: List[Any], weights: List[float]) -> Any:
        """
        Select one item based on weights.
        
        Args:
            items: List of items
            weights: List of weights (must sum to 1.0 or will be normalized)
        
        Returns:
            Selected item
        """
        # Normalize weights
        total = sum(weights)
        normalized_weights = [w / total for w in weights]
        return np.random.choice(items, p=normalized_weights)
    
    def beta(self, alpha: float, beta: float) -> float:
        """Generate random number from beta distribution."""
        return np.random.beta(alpha, beta)
    
    def poisson(self, lam: float) -> int:
        """Generate random integer from Poisson distribution."""
        return np.random.poisson(lam)

"""
Text generation utilities for reviews and social media posts.
"""
from typing import List, Dict
import random


# Product features for mentions
FEATURES = {
    'camera': ['camera', 'photo quality', 'picture quality', 'camera system', 'zoom', 'night mode'],
    'battery': ['battery life', 'battery', 'charging', 'battery performance', 'all-day battery'],
    'display': ['display', 'screen', 'screen quality', 'brightness', 'colors', 'AMOLED'],
    'performance': ['performance', 'speed', 'processor', 'multitasking', 'gaming', 'smooth']
}

# Review templates
POSITIVE_REVIEW_TEMPLATES = [
    "Just got my {product}! The {feature} is amazing. Highly recommend!",
    "Loving my new {product}. The {feature} exceeded my expectations.",
    "Best phone I've owned. The {feature} is outstanding.",
    "Upgraded to {product} and couldn't be happier. {feature} is incredible.",
    "The {product} is fantastic. {feature} works perfectly.",
]

NEUTRAL_REVIEW_TEMPLATES = [
    "The {product} is decent. {feature} is okay but nothing special.",
    "Got the {product}. {feature} is average, meets basic needs.",
    "It's a solid phone. {feature} is acceptable for the price.",
    "{product} is fine. {feature} could be better but it works.",
]

NEGATIVE_REVIEW_TEMPLATES = [
    "Disappointed with {product}. The {feature} is not as advertised.",
    "Expected more from {product}. {feature} is underwhelming.",
    "Not happy with my {product}. {feature} has issues.",
    "The {product} fell short. {feature} needs improvement.",
]

# Social media templates
SOCIAL_POSITIVE_TEMPLATES = [
    "Just unboxed my {product}! 📱 The {feature} is 🔥 #Nova #smartphone",
    "Loving my new {product}! {feature} is next level 💯",
    "{product} camera is insane! 📸 Best photos ever #NovaPrime",
    "Switched to {product} and wow! {feature} is amazing ✨",
]

SOCIAL_NEGATIVE_TEMPLATES = [
    "Not impressed with {product} 😞 {feature} disappointing",
    "{product} {feature} not living up to the hype...",
    "Regretting my {product} purchase. {feature} issues 😤",
]

SOCIAL_NEUTRAL_TEMPLATES = [
    "Got the {product}. {feature} is decent 👍",
    "Using {product} for a week now. {feature} is okay",
    "{product} review: {feature} meets expectations",
]


def generate_review_text(rating: int, product_name: str, rng) -> Dict[str, str]:
    """
    Generate review title and text based on rating.
    
    Args:
        rating: Rating from 1-5
        product_name: Name of the product
        rng: Random generator instance
    
    Returns:
        Dictionary with 'title' and 'text' keys
    """
    # Select feature to mention
    feature_category = rng.choice(list(FEATURES.keys()))
    feature = rng.choice(FEATURES[feature_category])
    
    # Select template based on rating
    if rating >= 4:
        template = rng.choice(POSITIVE_REVIEW_TEMPLATES)
        title_templates = [
            "Excellent phone!",
            "Love it!",
            "Highly recommend",
            "Best purchase ever",
            "Amazing device"
        ]
    elif rating == 3:
        template = rng.choice(NEUTRAL_REVIEW_TEMPLATES)
        title_templates = [
            "It's okay",
            "Decent phone",
            "Average experience",
            "Meets expectations"
        ]
    else:
        template = rng.choice(NEGATIVE_REVIEW_TEMPLATES)
        title_templates = [
            "Disappointed",
            "Not worth it",
            "Expected better",
            "Has issues"
        ]
    
    title = rng.choice(title_templates)
    text = template.format(product=product_name, feature=feature)
    
    # Add more detail to text
    additional_comments = [
        f" The {feature} really stands out.",
        f" I use it daily and {feature} performs well.",
        f" Compared to my old phone, {feature} is much better.",
        f" The {feature} is exactly what I needed.",
        f" Overall, {feature} meets my needs."
    ]
    
    if rating >= 4:
        text += rng.choice(additional_comments)
    
    return {'title': title, 'text': text}


def generate_pros_cons(rating: int, rng) -> Dict[str, List[str]]:
    """
    Generate pros and cons lists based on rating.
    
    Args:
        rating: Rating from 1-5
        rng: Random generator instance
    
    Returns:
        Dictionary with 'pros' and 'cons' lists
    """
    all_pros = [
        "camera", "battery", "display", "performance", "design",
        "build quality", "fast charging", "storage", "5G connectivity"
    ]
    
    all_cons = [
        "price", "weight", "no headphone jack", "bloatware",
        "camera in low light", "battery drain", "heating issues"
    ]
    
    if rating >= 4:
        pros = rng.sample(all_pros, rng.randint(2, 4))
        cons = rng.sample(all_cons, rng.randint(0, 1))
    elif rating == 3:
        pros = rng.sample(all_pros, rng.randint(1, 2))
        cons = rng.sample(all_cons, rng.randint(1, 2))
    else:
        pros = rng.sample(all_pros, rng.randint(0, 1))
        cons = rng.sample(all_cons, rng.randint(2, 3))
    
    return {'pros': pros, 'cons': cons}


def generate_social_post(sentiment: str, product_name: str, rng) -> str:
    """
    Generate social media post text based on sentiment.
    
    Args:
        sentiment: 'positive', 'negative', or 'neutral'
        product_name: Name of the product
        rng: Random generator instance
    
    Returns:
        Social media post text
    """
    feature_category = rng.choice(list(FEATURES.keys()))
    feature = rng.choice(FEATURES[feature_category])
    
    if sentiment == 'positive':
        template = rng.choice(SOCIAL_POSITIVE_TEMPLATES)
    elif sentiment == 'negative':
        template = rng.choice(SOCIAL_NEGATIVE_TEMPLATES)
    else:
        template = rng.choice(SOCIAL_NEUTRAL_TEMPLATES)
    
    return template.format(product=product_name, feature=feature)


def generate_hashtags(product_line: str, sentiment: str, rng) -> List[str]:
    """
    Generate hashtags for social media post.
    
    Args:
        product_line: Product line name
        sentiment: 'positive', 'negative', or 'neutral'
        rng: Random generator instance
    
    Returns:
        List of hashtags
    """
    base_tags = [f"#Nova{product_line}", "#smartphone", "#tech"]
    
    if sentiment == 'positive':
        extra_tags = ["#love", "#amazing", "#recommended", "#bestphone"]
    elif sentiment == 'negative':
        extra_tags = ["#disappointed", "#notgood", "#issues"]
    else:
        extra_tags = ["#review", "#newphone", "#techreview"]
    
    selected_extra = rng.sample(extra_tags, rng.randint(1, 2))
    return base_tags + selected_extra

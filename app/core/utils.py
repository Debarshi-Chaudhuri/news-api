# app/core/utils.py
from typing import List
from app.core.constants import NEWS_KEYWORDS

def validate_keywords(tags: List[str]) -> List[str]:
    """
    Validate tags against the static keywords list.
    Returns only tags that are valid keywords.
    """
    if not tags:
        return []
    
    return [tag for tag in tags if tag.lower() in [k.lower() for k in NEWS_KEYWORDS]]

def suggest_keywords(text: str, max_suggestions: int = 5) -> List[str]:
    """
    Analyze text and suggest relevant keywords from our static list.
    This is a simple implementation that checks if keywords appear in the text.
    
    Args:
        text: The text to analyze
        max_suggestions: Maximum number of keyword suggestions to return
        
    Returns:
        List of suggested keywords
    """
    if not text:
        return []
    
    text = text.lower()
    suggestions = []
    
    for keyword in NEWS_KEYWORDS:
        if keyword.lower() in text:
            suggestions.append(keyword)
            if len(suggestions) >= max_suggestions:
                break
                
    return suggestions
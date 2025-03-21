# 1. Create a new file app/models/responses/__init__.py
# This makes the responses directory a proper Python package

# Empty init file
# app/models/responses/__init__.py

# 2. Create app/models/responses/news.py
# This will contain the NewsArticleResponse model

# app/models/responses/news.py
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl
import random

from app.models.news import NewsArticle
from app.core.constants import INDUSTRY_IMAGES

class NewsArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    summary: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    published_date: Optional[datetime] = None
    categories: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str] = None
    
    @classmethod
    def from_article(cls, article: NewsArticle, keywords: List[str]) -> 'NewsArticleResponse':
        """Convert a NewsArticle to a NewsArticleResponse with image_url"""
        # Create a dict from the article
        article_dict = article.dict() if hasattr(article, 'dict') else article.model_dump()
        
        # Select image URL based on categories
        image_url = cls._select_image_url(keywords)
        article_dict['image_url'] = image_url
        
        return cls(**article_dict)
    
    @staticmethod
    def _select_image_url(keywords: List[str]) -> Optional[str]:
        """
        Select an image URL based on the article's categories.
        
        Args:
            categories: List of article categories
            
        Returns:
            Image URL if a match is found, None otherwise
        """
        if not keywords:
            return None
        
        # Map keywords to their industry categories
        from app.core.constants import INDUSTRY_CATEGORIES
        
        # Find the industry category for each keyword
        matched_industries = []
        for keyword in keywords:
            for industry, industry_keywords in INDUSTRY_CATEGORIES.items():
                if keyword in industry_keywords:
                    matched_industries.append(industry)
                    break
            
        # Check if any category matches with the keys in INDUSTRY_IMAGES
        for keyword in matched_industries:
            if keyword in INDUSTRY_IMAGES:
                # Select a random image URL from the list
                images = INDUSTRY_IMAGES[keyword]
                if images:
                    return random.choice(images)
                    
        # No matching category found
        return None

# 3. Update the routes in app/api/routes.py
# Add the necessary import and update the route handlers

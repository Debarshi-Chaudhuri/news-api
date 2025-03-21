from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, validator
from app.core.constants import NEWS_KEYWORDS

class NewsArticleBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    published_date: Optional[datetime] = None
    categories: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    url: Optional[HttpUrl] = None
    
    @validator('tags')
    def validate_tags(cls, tags):
        """Validate that tags are in our predefined keywords list"""
        if tags:
            # Only keep tags that are in our keywords list
            return [tag for tag in tags if tag.lower() in [keyword.lower() for keyword in NEWS_KEYWORDS]]
        return []

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    published_date: Optional[datetime] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    url: Optional[HttpUrl] = None
    
    @validator('tags')
    def validate_tags(cls, tags):
        """Validate that tags are in our predefined keywords list"""
        if tags:
            # Only keep tags that are in our keywords list
            return [tag for tag in tags if tag.lower() in [keyword.lower() for keyword in NEWS_KEYWORDS]]
        return tags

class NewsArticle(NewsArticleBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # In Pydantic v2, orm_mode was renamed to from_attributes
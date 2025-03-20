from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

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

class NewsArticle(NewsArticleBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # In Pydantic v2, orm_mode was renamed to from_attributes
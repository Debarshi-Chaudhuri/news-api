from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import get_api_key
from app.models.news import NewsArticle, NewsArticleCreate, NewsArticleUpdate
from app.services.news_service import NewsService
from typing import List, Dict, Optional

app = FastAPI(
    title=settings.APP_NAME,
    description="A RESTful API for news articles using Elasticsearch",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/news/search", tags=["news"])
async def search_news(
    q: str = Query(description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page"),
    sort_by: str = Query("published_date", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    api_key: str = Depends(get_api_key)
):
    """
    Search for news articles matching the provided query.
    """
    result = await NewsService.search_news(q, page, limit, sort_by, sort_order)
    return result

@app.get("/api/news/{article_id}", response_model=NewsArticle, tags=["news"])
async def get_news(article_id: str, api_key: str = Depends(get_api_key)):
    """
    Get a specific news article by ID.
    """
    article = await NewsService.get_news_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.post("/api/news", response_model=NewsArticle, status_code=201, tags=["news"])
async def create_news(article: NewsArticleCreate, api_key: str = Depends(get_api_key)):
    """
    Create a new news article.
    """
    return await NewsService.create_news(article)

@app.put("/api/news/{article_id}", response_model=NewsArticle, tags=["news"])
async def update_news(article_id: str, article: NewsArticleUpdate, api_key: str = Depends(get_api_key)):
    """
    Update an existing news article.
    """
    updated_article = await NewsService.update_news(article_id, article)
    if not updated_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated_article

@app.delete("/api/news/{article_id}", tags=["news"])
async def delete_news(article_id: str, api_key: str = Depends(get_api_key)):
    """
    Delete a news article.
    """
    success = await NewsService.delete_news(article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"detail": "Article deleted successfully"}
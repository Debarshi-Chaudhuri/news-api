from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import get_api_key
from app.core.constants import NEWS_KEYWORDS
from app.core.utils import suggest_keywords
from app.models.news import NewsArticle, NewsArticleCreate, NewsArticleUpdate
from app.services.news_service import NewsService
from app.services.scraper_service import ScraperService
from app.core.background import create_background_task
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

@app.get("/api/keywords", tags=["keywords"])
async def get_keywords(api_key: str = Depends(get_api_key)):
    """
    Get the list of available keywords for news articles.
    """
    return {"keywords": NEWS_KEYWORDS}

@app.post("/api/keywords/suggest", tags=["keywords"])
async def suggest_article_keywords(
    data: dict = {"text": ""}, 
    max_suggestions: int = Query(5, ge=1, le=20, description="Maximum number of keyword suggestions"),
    api_key: str = Depends(get_api_key)
):
    """
    Suggest relevant keywords for article content.
    """
    text = data.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text content is required")
        
    suggestions = suggest_keywords(text, max_suggestions)
    return {"suggestions": suggestions}

@app.get("/api/news/search", tags=["news"])
async def search_news(
    q: str = Query(description="Search query"),
    keyword: Optional[str] = Query(None, description="Filter by keyword"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page"),
    sort_by: str = Query("published_date", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    api_key: str = Depends(get_api_key)
):
    """
    Search for news articles matching the provided query.
    Optionally filter by keyword from the static keywords list.
    """
    result = await NewsService.search_news(q, page, limit, sort_by, sort_order)
    
    # If keyword filter is provided, filter results after fetching from Elasticsearch
    if keyword and keyword in NEWS_KEYWORDS:
        # Post-process results to filter by keyword
        filtered_articles = [
            article for article in result["articles"] 
            if keyword.lower() in [tag.lower() for tag in article.tags]
        ]
        # Update the result with filtered articles
        result["total"] = len(filtered_articles)
        result["articles"] = filtered_articles
        
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

@app.post("/api/scraper/run", tags=["scraper"])
async def run_scraper(
    keywords: List[str] = Query(None, description="Optional list of keywords to scrape. If not provided, all keywords will be used."),
    api_key: str = Depends(get_api_key)
):
    """
    Manually trigger the news scraper to run.
    """
    if keywords:
        # Validate keywords against our list
        valid_keywords = [k for k in keywords if k.lower() in [keyword.lower() for keyword in NEWS_KEYWORDS]]
        
        if not valid_keywords:
            raise HTTPException(status_code=400, detail="No valid keywords provided")
        
        # Create a background task for each keyword
        tasks_created = 0
        for keyword in valid_keywords:
            create_background_task(ScraperService.scrape_and_store_articles(keyword))
            tasks_created += 1
        
        return {"message": f"Scraper started for {tasks_created} keywords: {valid_keywords}"}
    else:
        # Run for all keywords
        create_background_task(ScraperService.run_scraper_for_all_keywords())
        return {"message": f"Scraper started for all {len(NEWS_KEYWORDS)} keywords"}
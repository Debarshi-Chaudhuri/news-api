from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import get_api_key
from app.core.constants import INDUSTRY_CATEGORIES, NEWS_KEYWORDS
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
    industry: Optional[str] = Query(None, description="Filter by industry category"),
    india_focus: bool = Query(True, description="Ensure content is focused on India"),
    business_only: bool = Query(True, description="Only return business-related content"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page"),
    sort_by: str = Query("published_date", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    api_key: str = Depends(get_api_key)
):
    """
    Search for news articles matching the provided query.
    By default, focuses on Indian business news.
    Optionally filter by keyword or industry category.
    """
    # Ensure India focus if requested
    if india_focus:
        # Add "india" or "indian" to the query if not already present
        if "india" not in q.lower() and "indian" not in q.lower():
            q = f"{q} india"
    
    # Ensure business focus if requested
    if business_only:
        # Add "business" to the query if not already present
        if "business" not in q.lower() and "industry" not in q.lower():
            q = f"{q} business"
    
    # Perform the search
    result = await NewsService.search_news(q, page, limit, sort_by, sort_order)
    
    # Filter by keyword if provided
    if keyword and keyword in NEWS_KEYWORDS:
        filtered_articles = [
            article for article in result["articles"] 
            if keyword.lower() in [tag.lower() for tag in article.tags]
        ]
        result["total"] = len(filtered_articles)
        result["articles"] = filtered_articles
    
    # Filter by industry category if provided
    if industry and industry in INDUSTRY_CATEGORIES:
        # Get all keywords for this industry
        industry_keywords = INDUSTRY_CATEGORIES[industry]
        industry_keywords.append(industry)  # Include the industry name itself
        
        # Filter articles that have any of these keywords in their tags
        filtered_articles = []
        for article in result["articles"]:
            # Check if any tag matches any industry keyword
            if any(keyword.lower() in [tag.lower() for tag in article.tags] for keyword in industry_keywords):
                filtered_articles.append(article)
            # Also check categories
            elif industry in article.categories:
                filtered_articles.append(article)
        
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

@app.post("/api/scraper/industry", tags=["scraper"])
async def run_industry_scraper(
    category: Optional[str] = Query(None, description="Optional specific industry category to scrape. If not provided, all categories will be scraped."),
    max_articles_per_keyword: int = Query(2, ge=1, le=5, description="Maximum number of articles per keyword"),
    api_key: str = Depends(get_api_key)
):
    """
    Manually trigger the industry-specific news scraper to run.
    """
    from app.core.constants import INDUSTRY_CATEGORIES
    
    if category and category not in INDUSTRY_CATEGORIES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid industry category. Available categories: {list(INDUSTRY_CATEGORIES.keys())}"
        )
    
    # Create a background task for the scraper
    task = create_background_task(
        ScraperService.scrape_industry_specific_news(
            category=category,
            max_articles_per_keyword=max_articles_per_keyword
        )
    )
    
    if category:
        return {
            "message": f"Industry scraper started for category: {category}",
            "keywords": INDUSTRY_CATEGORIES[category],
            "max_articles_per_keyword": max_articles_per_keyword
        }
    else:
        return {
            "message": f"Industry scraper started for all {len(INDUSTRY_CATEGORIES)} categories",
            "categories": list(INDUSTRY_CATEGORIES.keys()),
            "max_articles_per_keyword": max_articles_per_keyword
        }

@app.get("/api/industries", tags=["industries"])
async def get_industry_categories(api_key: str = Depends(get_api_key)):
    """
    Get the list of industry categories and their keywords.
    """
    from app.core.constants import INDUSTRY_CATEGORIES
    return {"industries": INDUSTRY_CATEGORIES}

@app.get("/api/stats/india-business", tags=["stats"])
async def get_india_business_stats(
    timeframe: str = Query("month", description="Timeframe for stats: day, week, month, year"),
    api_key: str = Depends(get_api_key)
):
    """
    Get statistics about Indian business news articles in the system.
    """
    es = get_elasticsearch()
    
    # Calculate date range based on timeframe
    now = datetime.utcnow()
    date_ranges = {
        "day": now - timedelta(days=1),
        "week": now - timedelta(weeks=1),
        "month": now - timedelta(days=30),
        "year": now - timedelta(days=365)
    }
    
    from_date = date_ranges.get(timeframe, date_ranges["month"])
    
    # Build aggregation query
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "published_date": {
                                "gte": from_date.isoformat()
                            }
                        }
                    },
                    {
                        "bool": {
                            "should": [
                                # India-related content
                                {"match": {"content": "india indian"}},
                                {"match": {"title": "india indian"}},
                                {"term": {"categories": "India"}},
                                {"terms": {"tags": ["india", "indian"]}},
                                
                                # Business-related content
                                {"match": {"content": "business industry"}},
                                {"match": {"title": "business industry"}},
                                {"term": {"categories": "Business"}},
                                {"terms": {"tags": ["business", "industry"]}}
                            ],
                            "minimum_should_match": 2  # Must match at least one India AND one business criteria
                        }
                    }
                ]
            }
        },
        "size": 0,
        "aggs": {
            "categories": {
                "terms": {
                    "field": "categories",
                    "size": 20
                }
            },
            "tags": {
                "terms": {
                    "field": "tags",
                    "size": 30
                }
            },
            "sources": {
                "terms": {
                    "field": "source",
                    "size": 20
                }
            },
            "per_day": {
                "date_histogram": {
                    "field": "published_date",
                    "calendar_interval": "day"
                }
            }
        }
    }
    
    # Execute the query
    response = await es.search(
        index=settings.NEWS_INDEX,
        body=query
    )
    
    # Extract statistics
    total_articles = response["hits"]["total"]["value"]
    
    stats = {
        "total_articles": total_articles,
        "timeframe": timeframe,
        "from_date": from_date.isoformat(),
        "to_date": now.isoformat(),
        "top_categories": [
            {"name": bucket["key"], "count": bucket["doc_count"]}
            for bucket in response["aggregations"]["categories"]["buckets"]
        ],
        "top_tags": [
            {"name": bucket["key"], "count": bucket["doc_count"]}
            for bucket in response["aggregations"]["tags"]["buckets"]
        ],
        "top_sources": [
            {"name": bucket["key"], "count": bucket["doc_count"]}
            for bucket in response["aggregations"]["sources"]["buckets"]
        ],
        "articles_per_day": [
            {"date": bucket["key_as_string"], "count": bucket["doc_count"]}
            for bucket in response["aggregations"]["per_day"]["buckets"]
        ]
    }
    
    # Calculate average articles per day
    day_count = max(1, (now - from_date).days)
    stats["avg_articles_per_day"] = round(total_articles / day_count, 2)
    
    return stats
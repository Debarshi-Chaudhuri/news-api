from datetime import datetime
# Import using try/except to handle different elasticsearch versions
try:
    from elasticsearch import NotFoundError
except ImportError:
    # Fallback for different versions
    NotFoundError = Exception  # Generic fallback

from app.db.elasticsearch import get_elasticsearch
from app.core.config import settings
from app.models.news import NewsArticle, NewsArticleCreate, NewsArticleUpdate

class NewsRepository:
    @staticmethod
    async def search(query: str, page: int = 1, limit: int = 10, sort_by: str = "published_date", sort_order: str = "desc"):
        es = get_elasticsearch()
        
        # Calculate from based on page and limit
        from_idx = (page - 1) * limit
        
        # Build the search query
        search_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "content", "summary^2", "author", "source", "categories", "tags"]
                }
            },
            "sort": [
                {sort_by: {"order": sort_order}}
            ],
            "from": from_idx,
            "size": limit
        }
        
        # Execute the search
        response = await es.search(
            index=settings.NEWS_INDEX,
            body=search_query
        )
        
        # Process and return results
        total = response["hits"]["total"]["value"]
        hits = response["hits"]["hits"]
        
        articles = []
        for hit in hits:
            source = hit["_source"]
            article = NewsArticle(
                id=hit["_id"],
                title=source["title"],
                content=source["content"],
                summary=source.get("summary"),
                author=source.get("author"),
                source=source.get("source"),
                published_date=source.get("published_date"),
                categories=source.get("categories", []),
                tags=source.get("tags", []),
                url=source.get("url"),
                created_at=source.get("created_at"),
                updated_at=source.get("updated_at")
            )
            articles.append(article)
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "articles": articles
        }
    
    @staticmethod
    async def get_by_id(article_id: str):
        es = get_elasticsearch()
        
        try:
            response = await es.get(
                index=settings.NEWS_INDEX,
                id=article_id
            )
            
            source = response["_source"]
            return NewsArticle(
                id=response["_id"],
                title=source["title"],
                content=source["content"],
                summary=source.get("summary"),
                author=source.get("author"),
                source=source.get("source"),
                published_date=source.get("published_date"),
                categories=source.get("categories", []),
                tags=source.get("tags", []),
                url=source.get("url"),
                created_at=source.get("created_at"),
                updated_at=source.get("updated_at")
            )
        except NotFoundError:
            return None
    
    @staticmethod
    async def create(article: NewsArticleCreate):
        es = get_elasticsearch()
        
        now = datetime.utcnow().isoformat()
        article_dict = article.dict()
        article_dict["created_at"] = now
        article_dict["updated_at"] = now
        
        response = await es.index(
            index=settings.NEWS_INDEX,
            document=article_dict,
            refresh=True
        )
        
        return NewsArticle(
            id=response["_id"],
            **article_dict
        )
    
    @staticmethod
    async def update(article_id: str, article: NewsArticleUpdate):
        es = get_elasticsearch()
        
        # Get the existing article
        existing = await NewsRepository.get_by_id(article_id)
        if not existing:
            return None
        
        # Update fields from the update object
        update_data = article.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update in Elasticsearch
        await es.update(
            index=settings.NEWS_INDEX,
            id=article_id,
            doc=update_data,
            refresh=True
        )
        
        # Return the updated article
        return await NewsRepository.get_by_id(article_id)
    
    @staticmethod
    async def delete(article_id: str):
        es = get_elasticsearch()
        
        try:
            await es.delete(
                index=settings.NEWS_INDEX,
                id=article_id,
                refresh=True
            )
            return True
        except NotFoundError:
            return False
from app.db.repositories import NewsRepository
from app.models.news import NewsArticle, NewsArticleCreate, NewsArticleUpdate
from typing import Dict, List, Optional

class NewsService:
    @staticmethod
    async def search_news(
        query: str, 
        page: int = 1, 
        limit: int = 10,
        sort_by: str = "published_date",
        sort_order: str = "desc"
    ) -> Dict:
        return await NewsRepository.search(query, page, limit, sort_by, sort_order)
    
    @staticmethod
    async def get_news_by_id(article_id: str) -> Optional[NewsArticle]:
        return await NewsRepository.get_by_id(article_id)
    
    @staticmethod
    async def create_news(article: NewsArticleCreate) -> NewsArticle:
        return await NewsRepository.create(article)
    
    @staticmethod
    async def update_news(article_id: str, article: NewsArticleUpdate) -> Optional[NewsArticle]:
        return await NewsRepository.update(article_id, article)
    
    @staticmethod
    async def delete_news(article_id: str) -> bool:
        return await NewsRepository.delete(article_id)
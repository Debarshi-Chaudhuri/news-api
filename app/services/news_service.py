from app.db.repositories import NewsRepository
from app.models.news import NewsArticle, NewsArticleCreate, NewsArticleUpdate
from app.services.summarizer_service import SummarizerService
from app.core.config import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class NewsService:
    @staticmethod
    async def search_news(
        query: str, 
        keywords: list[str] = None,
        page: int = 1, 
        limit: int = 10,
        sort_by: str = "published_date",
        sort_order: str = "desc"
    ) -> Dict:
        return await NewsRepository.search(query, keywords,  page, limit, sort_by, sort_order)
    
    @staticmethod
    async def get_news_by_id(article_id: str) -> Optional[NewsArticle]:
        return await NewsRepository.get_by_id(article_id)
    
    @staticmethod
    async def create_news(article: NewsArticleCreate) -> NewsArticle:
        # Auto-generate summary if enabled and not already provided
        if settings.ENABLE_AUTO_SUMMARIZATION and not article.summary and article.content:
            try:
                summary = await SummarizerService.summarize_text(
                    article.content, 
                    max_length=settings.SUMMARY_MAX_LENGTH
                )
                if summary:
                    # Update the article with the generated summary
                    # Handle both Pydantic v1 and v2
                    try:
                        # Pydantic v2
                        article_dict = article.model_dump()
                        article_dict["summary"] = summary
                        article = NewsArticleCreate(**article_dict)
                    except AttributeError:
                        # Pydantic v1
                        article_dict = article.dict()
                        article_dict["summary"] = summary
                        article = NewsArticleCreate(**article_dict)
                    
                    logger.info(f"Auto-generated summary for article: {article.title}")
            except Exception as e:
                logger.error(f"Failed to auto-generate summary: {e}")
        
        return await NewsRepository.create(article)
    
    @staticmethod
    async def update_news(article_id: str, article: NewsArticleUpdate) -> Optional[NewsArticle]:
        # Auto-generate summary if enabled, content is updated, and summary not provided
        try:
            # Check if we need to update the summary
            update_summary = False
            
            # Handle both Pydantic v1 and v2
            try:
                # Pydantic v2
                article_dict = article.model_dump(exclude_unset=True)
            except AttributeError:
                # Pydantic v1
                article_dict = article.dict(exclude_unset=True)
            
            # If content is updated but summary is not, regenerate the summary
            if (settings.ENABLE_AUTO_SUMMARIZATION and 
                'content' in article_dict and 
                article_dict.get('content') and 
                'summary' not in article_dict):
                
                update_summary = True
                
            if update_summary:
                existing_article = await NewsRepository.get_by_id(article_id)
                if existing_article:
                    summary = await SummarizerService.summarize_text(
                        article_dict['content'],
                        max_length=settings.SUMMARY_MAX_LENGTH
                    )
                    if summary:
                        article_dict['summary'] = summary
                        
                        # Update the article object
                        try:
                            # Pydantic v2
                            article = NewsArticleUpdate(**article_dict)
                        except TypeError:
                            # Pydantic v1
                            article = NewsArticleUpdate.parse_obj(article_dict)
                        
                        logger.info(f"Auto-generated summary for updated article: {existing_article.title}")
        except Exception as e:
            logger.error(f"Failed to auto-generate summary during update: {e}")
        
        return await NewsRepository.update(article_id, article)
    
    @staticmethod
    async def delete_news(article_id: str) -> bool:
        return await NewsRepository.delete(article_id)
        
    @staticmethod
    async def summarize_article(article_id: str, max_length: int = None) -> Optional[str]:
        """
        Generate or regenerate a summary for an existing article.
        
        Args:
            article_id: The ID of the article to summarize
            max_length: Optional custom max length for the summary
            
        Returns:
            The generated summary or None if summarization failed
        """
        if not settings.CLAUDE_API_KEY:
            logger.warning("Claude API key is not set. Summarization is not available.")
            return None
            
        # Get the article
        article = await NewsRepository.get_by_id(article_id)
        if not article:
            logger.error(f"Article not found: {article_id}")
            return None
            
        # Set the max length
        if max_length is None:
            max_length = settings.SUMMARY_MAX_LENGTH
            
        # Generate the summary
        summary = await SummarizerService.summarize_text(article.content, max_length)
        if not summary:
            logger.error(f"Failed to generate summary for article: {article_id}")
            return None
            
        # Update the article with the new summary
        update = NewsArticleUpdate(summary=summary)
        updated_article = await NewsRepository.update(article_id, update)
        
        if updated_article:
            logger.info(f"Updated article with new summary: {article_id}")
            return summary
        else:
            logger.error(f"Failed to update article with new summary: {article_id}")
            return None
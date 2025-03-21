from datetime import datetime
import logging
from urllib.parse import urlparse, urlunparse
# Import using try/except to handle different elasticsearch versions
try:
    from elasticsearch import NotFoundError
except ImportError:
    # Fallback for different versions
    NotFoundError = Exception  # Generic fallback

from app.db.elasticsearch import get_elasticsearch
from app.core.config import settings
from app.models.news import NewsArticle, NewsArticleCreate, NewsArticleUpdate

logger = logging.getLogger(__name__)

class NewsRepository:
    @staticmethod
    def _normalize_url(url):
        """
        Normalize a URL by removing query parameters and fragments.
        
        Args:
            url: The URL to normalize
            
        Returns:
            Normalized URL without query parameters or fragments
        """
        if not url:
            return ""
            
        try:
            # Parse the URL
            parsed_url = urlparse(str(url))
            
            # Rebuild without query parameters and fragments
            normalized = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                '',  # params
                '',  # query
                ''   # fragment
            ))
            
            return normalized
        except Exception as e:
            logger.warning(f"Error normalizing URL '{url}': {e}")
            return str(url)
    
    @staticmethod
    async def find_by_normalized_url(url):
        """
        Find an article by its normalized URL.
        
        Args:
            url: The URL to search for (will be normalized)
            
        Returns:
            Article object if found, None otherwise
        """
        if not url:
            return None
            
        normalized_url = NewsRepository._normalize_url(url)
        if not normalized_url:
            return None
            
        es = get_elasticsearch()
        
        # Search for the normalized URL
        search_query = {
            "query": {
                "term": {
                    "normalized_url.keyword": normalized_url
                }
            }
        }
        
        try:
            response = await es.search(
                index=settings.NEWS_INDEX,
                body=search_query,
                size=1
            )
            
            hits = response.get("hits", {}).get("hits", [])
            if not hits:
                return None
                
            # Return the first matching article
            hit = hits[0]
            source = hit["_source"]
            
            return NewsArticle(
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
        except Exception as e:
            logger.error(f"Error searching for article by URL '{normalized_url}': {e}")
            return None
    
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
        
        try:
            now = datetime.utcnow().isoformat()
            
            # Handle Pydantic v2 vs v1 differences
            try:
                # Pydantic v2 way
                article_dict = article.model_dump(exclude_unset=True)
            except AttributeError:
                # Fallback to Pydantic v1 way
                article_dict = article.dict(exclude_unset=True)
            
            # Check for duplicate by URL if URL exists
            url = article_dict.get("url")
            existing_article = None
            
            if url:
                # Normalize the URL for deduplication
                normalized_url = NewsRepository._normalize_url(url)
                
                # Store the normalized URL in the document for future searches
                article_dict["normalized_url"] = normalized_url
                
                # Check if an article with this normalized URL already exists
                existing_article = await NewsRepository.find_by_normalized_url(url)
                
                if existing_article:
                    logger.info(f"Found duplicate article with URL: {normalized_url}")
                    
                    # Update the existing article instead of creating a new one
                    # Extract the ID of the existing article
                    article_id = existing_article.id
                    
                    # Keep the original created_at date
                    article_dict["created_at"] = existing_article.created_at
                    article_dict["updated_at"] = now
                    
                    # Merge tags from both articles to avoid losing information
                    if "tags" in article_dict and existing_article.tags:
                        combined_tags = list(set(article_dict["tags"] + existing_article.tags))
                        article_dict["tags"] = combined_tags
                    
                    # Update the existing article
                    await es.update(
                        index=settings.NEWS_INDEX,
                        id=article_id,
                        doc=article_dict,
                        refresh=True
                    )
                    
                    # Return the updated article
                    return await NewsRepository.get_by_id(article_id)
            
            # If no duplicate was found or no URL was provided, create a new article
            
            # Ensure dates are properly formatted as strings
            article_dict["created_at"] = now
            article_dict["updated_at"] = now
            
            # Handle potential JSON serialization issues with dates
            if "published_date" in article_dict and article_dict["published_date"] is not None:
                if isinstance(article_dict["published_date"], datetime):
                    article_dict["published_date"] = article_dict["published_date"].isoformat()
                elif not isinstance(article_dict["published_date"], str):
                    article_dict["published_date"] = str(article_dict["published_date"])
            
            # Make URL serializable (Pydantic HttpUrl might cause issues)
            if "url" in article_dict and article_dict["url"] is not None:
                article_dict["url"] = str(article_dict["url"])
            
            # Ensure all fields are properly serializable
            for key in list(article_dict.keys()):
                value = article_dict[key]
                if value is None:
                    continue  # None is JSON serializable
                elif isinstance(value, (list, dict)):
                    # Check nested items in lists
                    if isinstance(value, list):
                        article_dict[key] = [str(item) if not isinstance(item, (str, int, float, bool, type(None))) else item for item in value]
                elif not isinstance(value, (str, int, float, bool)):
                    # Convert other non-serializable types to string
                    article_dict[key] = str(value)
            
            # Log sanitized data for debugging
            logging.debug(f"Sanitized article data: {article_dict}")
            
            response = await es.index(
                index=settings.NEWS_INDEX,
                document=article_dict,
                refresh=True
            )
            
            return NewsArticle(
                id=response["_id"],
                **article_dict
            )
        except Exception as e:
            logging.error(f"Error creating article in Elasticsearch: {e}")
            logging.error(f"Article data: {article}")
            raise
    
    @staticmethod
    async def update(article_id: str, article: NewsArticleUpdate):
        es = get_elasticsearch()
        
        try:
            # Get the existing article
            existing = await NewsRepository.get_by_id(article_id)
            if not existing:
                return None
            
            # Handle Pydantic v2 vs v1 differences
            try:
                # Pydantic v2 way
                update_data = article.model_dump(exclude_unset=True)
            except AttributeError:
                # Fallback to Pydantic v1 way
                update_data = article.dict(exclude_unset=True)
            
            # Update the timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # If URL is being updated, update the normalized URL as well
            if "url" in update_data and update_data["url"] is not None:
                update_data["url"] = str(update_data["url"])
                update_data["normalized_url"] = NewsRepository._normalize_url(update_data["url"])
            
            # Handle other serialization issues similar to create method
            for key in list(update_data.keys()):
                value = update_data[key]
                if value is None:
                    continue
                elif isinstance(value, (list, dict)):
                    if isinstance(value, list):
                        update_data[key] = [str(item) if not isinstance(item, (str, int, float, bool, type(None))) else item for item in value]
                elif isinstance(value, datetime):
                    update_data[key] = value.isoformat()
                elif not isinstance(value, (str, int, float, bool)):
                    update_data[key] = str(value)
            
            # Update in Elasticsearch
            await es.update(
                index=settings.NEWS_INDEX,
                id=article_id,
                doc=update_data,
                refresh=True
            )
            
            # Return the updated article
            return await NewsRepository.get_by_id(article_id)
        except Exception as e:
            logging.error(f"Error updating article in Elasticsearch: {e}")
            raise
    
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
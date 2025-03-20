# Import the Elasticsearch client in a way that works with different versions
try:
    # For elasticsearch>=8.0.0
    from elasticsearch import AsyncElasticsearch
except ImportError:
    try:
        # For elasticsearch>=7.0.0
        from elasticsearch import Elasticsearch as AsyncElasticsearch
    except ImportError:
        # Fallback
        raise ImportError("Could not import Elasticsearch. Make sure it's installed: pip install elasticsearch")

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
es_client = None

def get_elasticsearch():
    return es_client

def init_elasticsearch():
    global es_client
    try:
        es_auth = {}
        if settings.ELASTICSEARCH_USERNAME and settings.ELASTICSEARCH_PASSWORD:
            es_auth = {
                "basic_auth": (settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD)
            }
        
        es_client = AsyncElasticsearch(
            settings.ELASTICSEARCH_URL,
            **es_auth
        )
        logger.info("Connected to Elasticsearch")
        
        # Create index if it doesn't exist
        import asyncio
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            # If we're not in an event loop, create one and run the coroutine
            asyncio.run(create_index_if_not_exists())
        else:
            # If we're already in an event loop, schedule the coroutine
            asyncio.create_task(create_index_if_not_exists())
        
        return es_client
    except Exception as e:
        logger.error(f"Error connecting to Elasticsearch: {e}")
        raise e

async def create_index_if_not_exists():
    if not await es_client.indices.exists(index=settings.NEWS_INDEX):
        # Define the mapping for the news articles
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "summary": {"type": "text"},
                    "author": {"type": "keyword"},
                    "source": {"type": "keyword"},
                    "published_date": {"type": "date"},
                    "categories": {"type": "keyword"},
                    "tags": {"type": "keyword"},
                    "url": {"type": "keyword"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            }
        }
        
        await es_client.indices.create(
            index=settings.NEWS_INDEX,
            body=mapping
        )
        logger.info(f"Created index: {settings.NEWS_INDEX}")
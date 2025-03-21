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
                    "title": {"type": "text", "analyzer": "business_india_analyzer"},
                    "content": {"type": "text", "analyzer": "business_india_analyzer"},
                    "summary": {"type": "text", "analyzer": "business_india_analyzer"},
                    "author": {"type": "keyword"},
                    "source": {"type": "keyword"},
                    "published_date": {"type": "date"},
                    "categories": {"type": "keyword"},
                    "tags": {"type": "keyword"},
                    "url": {"type": "keyword"},
                    "normalized_url": {
                        "type": "keyword",
                        "normalizer": "lowercase"  # Use lowercase normalizer for case-insensitive matching
                    },
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"},
                    # New fields for India and business relevance
                    "india_relevance": {"type": "float"},
                    "business_relevance": {"type": "float"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
                "analysis": {
                    "filter": {
                        "india_business_synonym_filter": {
                            "type": "synonym",
                            "synonyms": [
                                "india, indian, bharat, desi, hindustani",
                                "business, industry, commerce, trade, corporate, enterprise",
                                "msme, micro small medium enterprise, small business",
                                "startup, new business, venture",
                                "make in india, manufactured in india, indian manufacturing",
                                "digital india, digitalization india, india tech",
                                "gst, goods and services tax",
                                "rbi, reserve bank of india",
                                "sebi, securities and exchange board of india",
                                "economy, economic, financial, fiscal"
                            ]
                        },
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_stemmer": {
                            "type": "stemmer",
                            "language": "english"
                        }
                    },
                    "analyzer": {
                        "business_india_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "india_business_synonym_filter",
                                "english_stop",
                                "english_stemmer"
                            ]
                        }
                    },
                    "normalizer": {
                        "lowercase": {
                            "type": "custom",
                            "filter": ["lowercase"]
                        }
                    }
                }
            }
        }
        
        await es_client.indices.create(
            index=settings.NEWS_INDEX,
            body=mapping
        )
        logger.info(f"Created index: {settings.NEWS_INDEX}")
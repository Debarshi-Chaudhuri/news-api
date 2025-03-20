import pytest
import asyncio
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch
from app.api.routes import app
from fastapi.testclient import TestClient

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def es_client():
    # Use a test index instead of the production one
    settings.NEWS_INDEX = "test_news"
    
    # Initialize Elasticsearch
    es = init_elasticsearch()
    
    # Create the test index
    if not await es.indices.exists(index=settings.NEWS_INDEX):
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
            }
        }
        
        await es.indices.create(
            index=settings.NEWS_INDEX,
            body=mapping
        )
    
    yield es
    
    # Clean up the test index
    await es.indices.delete(index=settings.NEWS_INDEX)
    await es.close()
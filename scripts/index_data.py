import asyncio
import json
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch
from elasticsearch import AsyncElasticsearch

async def index_sample_data():
    # Initialize Elasticsearch
    es_client = init_elasticsearch()
    
    # Load sample data
    with open("data/sample_news.json", "r") as file:
        articles = json.load(file)
    
    print(f"Indexing {len(articles)} sample news articles...")
    
    # Index each article
    for article in articles:
        await es_client.index(
            index=settings.NEWS_INDEX,
            document=article,
            refresh=True
        )
    
    print("Sample data indexed successfully!")
    
    # Close Elasticsearch connection
    await es_client.close()

if __name__ == "__main__":
    asyncio.run(index_sample_data())
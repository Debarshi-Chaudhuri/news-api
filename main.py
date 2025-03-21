import uvicorn
import logging
from app.api.routes import app
from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch, create_index_if_not_exists
from app.core.nltk_init import download_nltk_resources

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Initialize Elasticsearch connection
    init_elasticsearch()
    
    # Create index if it doesn't exist
    await create_index_if_not_exists()
    
    # Download NLTK resources for NLP processing
    download_nltk_resources()
    
    # Note: Background news scraper is now moved to a separate service
    logger.info("API service started. News scraping is handled by the data-populator service.")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )
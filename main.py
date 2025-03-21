import uvicorn
import logging
from app.api.routes import app
from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch, create_index_if_not_exists
from app.core.nltk_init import download_nltk_resources
from app.core.background import create_background_task
from app.services.scraper_service import ScraperService
from app.db.dynamodb import init_dynamodb, create_user_subscriptions_table_if_not_exists
from app.services.event_service import EventService  # Import EventService

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Initialize Elasticsearch connection
    init_elasticsearch()
    init_dynamodb()
    
    # Create index if it doesn't exist
    await create_index_if_not_exists()
    await create_user_subscriptions_table_if_not_exists()
    
    # Download NLTK resources for NLP processing
    download_nltk_resources()
    
    # Initialize the EventService
    EventService.initialize()
    logger.info("EventService initialized")
    
    # Note: Background news scraper is now moved to a separate service
    logger.info("API service started. News scraping is handled by the data-populator service.")

@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown the EventService
    await EventService.shutdown()
    logger.info("EventService shutdown completed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )
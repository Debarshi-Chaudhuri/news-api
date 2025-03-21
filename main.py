import uvicorn
import logging
from app.api.routes import app
from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch, create_index_if_not_exists
from app.core.background import create_background_task
from app.services.scraper_service import ScraperService

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    init_elasticsearch()
    
    await create_index_if_not_exists()
    
    # Start the background news scraper task if enabled
    if settings.ENABLE_NEWS_SCRAPER:
        create_background_task(
            ScraperService.schedule_periodic_scraping(
                interval_minutes=settings.SCRAPER_INTERVAL_MINUTES
            )
        )
        logger.info(f"News scraper started with interval of {settings.SCRAPER_INTERVAL_MINUTES} minutes")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )
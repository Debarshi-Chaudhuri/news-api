#!/usr/bin/env python3
import asyncio
import logging
import os
import sys
from datetime import datetime

# Set environment variable to enable scraping regardless of the .env setting
os.environ["ENABLE_NEWS_SCRAPER"] = "True"

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging before any other imports
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to stdout instead of files to avoid permission issues
    ]
)

logger = logging.getLogger("data-populator")

# Now import application modules
from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch, create_index_if_not_exists
from app.core.nltk_init import download_nltk_resources
from app.services.scraper_service import ScraperService

async def main():
    try:
        logger.info("Starting data populator service")
        
        # Initialize Elasticsearch
        es_client = init_elasticsearch()
        logger.info("Elasticsearch client initialized")
        
        # Create index if it doesn't exist
        await create_index_if_not_exists()
        logger.info(f"Ensured Elasticsearch index '{settings.NEWS_INDEX}' exists")
        
        # Download NLTK resources for the scraper
        download_nltk_resources()
        logger.info("NLTK resources downloaded")
        
        # No sample data indexing - we'll directly scrape fresh data
        
        # Always run the scraper - ignore the ENABLE_NEWS_SCRAPER setting since this is specifically a scraper service
        logger.info("Running initial news scraping...")
        total_articles = await ScraperService.run_scraper_for_all_keywords()
        logger.info(f"Initial scraping complete. {total_articles} articles added.")
        
        # Start periodic scraping
        interval_minutes = settings.SCRAPER_INTERVAL_MINUTES
        logger.info(f"Starting periodic scraping every {interval_minutes} minutes")
        await ScraperService.schedule_periodic_scraping(interval_minutes)
    
    except Exception as e:
        logger.error(f"Error in data populator service: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Data populator service stopped by user")
    except Exception as e:
        logger.error(f"Unhandled exception in data populator: {e}", exc_info=True)
        sys.exit(1)
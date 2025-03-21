#!/usr/bin/env python
"""
Data Populator Service for News API

This script runs as a separate service to populate Elasticsearch with news articles.
It handles both initial data loading and periodic scraping of news articles.
"""

import asyncio
import logging
import os
import sys
import random
import time
from datetime import datetime

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.elasticsearch import init_elasticsearch, create_index_if_not_exists
from app.services.scraper_service import ScraperService
from app.services.news_service import NewsService
from app.models.news import NewsArticleCreate
from app.core.constants import NEWS_KEYWORDS, INDUSTRY_CATEGORIES
from app.core.config import settings
from app.core.nltk_init import download_nltk_resources

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('data_populator.log')
    ]
)

logger = logging.getLogger(__name__)

async def scrape_for_category(category, max_articles=3):
    """Scrape articles for a specific industry category."""
    logger.info(f"Scraping for category: {category}")
    
    # First scrape using the category name itself
    articles_stored = await ScraperService.scrape_and_store_articles(category)
    
    # Get keywords for this category
    keywords = INDUSTRY_CATEGORIES.get(category, [])
    
    # Scrape for each keyword, but limit to avoid overloading
    sample_keywords = random.sample(keywords, min(3, len(keywords)))
    
    for keyword in sample_keywords:
        logger.info(f"Scraping for keyword: {keyword} (Category: {category})")
        search_term = f"{keyword} {category}"
        
        await ScraperService.scrape_and_store_articles(
            search_term, 
            category=category,
            max_articles=max_articles
        )
        
        # Sleep between requests to avoid rate limiting
        await asyncio.sleep(random.uniform(3, 5))
    
    return True

async def run_periodic_scraping():
    """Run periodic scraping of news articles based on configured interval."""
    interval_minutes = int(os.getenv("SCRAPER_INTERVAL_MINUTES", "60"))
    
    while True:
        try:
            logger.info(f"Starting scheduled news scraping...")
            
            # Select random keywords to avoid scraping everything every time
            # This makes the service more efficient and avoids rate limiting
            sample_size = min(10, len(NEWS_KEYWORDS))
            keywords_to_scrape = random.sample(NEWS_KEYWORDS, sample_size)
            
            # Scrape for each selected keyword
            for keyword in keywords_to_scrape:
                logger.info(f"Scraping for keyword: {keyword}")
                await ScraperService.scrape_and_store_articles(keyword)
                # Sleep between requests to avoid rate limiting
                await asyncio.sleep(random.uniform(2, 4))
            
            # Select a few random industry categories to scrape
            categories = list(INDUSTRY_CATEGORIES.keys())
            sample_size = min(3, len(categories))
            categories_to_scrape = random.sample(categories, sample_size)
            
            # Scrape for each selected category
            for category in categories_to_scrape:
                await scrape_for_category(category)
                # Sleep between categories to avoid rate limiting
                await asyncio.sleep(random.uniform(5, 8))
            
            logger.info(f"Scheduled scraping completed successfully")
            
        except Exception as e:
            logger.error(f"Error in scheduled scraping: {e}")
        
        # Log next run time
        next_run = datetime.now().timestamp() + (interval_minutes * 60)
        next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Next scraping run scheduled at: {next_run_time} (in {interval_minutes} minutes)")
        
        # Sleep until next scheduled run
        await asyncio.sleep(interval_minutes * 60)

async def main():
    """Main entry point for the data populator service."""
    logger.info("Starting News API Data Populator Service")
    
    try:
        # Initialize Elasticsearch client
        init_elasticsearch()
        
        # Create index if it doesn't exist
        await create_index_if_not_exists()
        
        # Download NLTK resources for NLP processing
        download_nltk_resources()
        
        # Run an initial scraping
        logger.info("Running initial news scraping...")
        
        # Scrape for a few key terms to build initial dataset
        initial_keywords = ["india business", "indian industry", "make in india", 
                          "business news", "indian economy", "india manufacturing"]
        
        for keyword in initial_keywords:
            await ScraperService.scrape_and_store_articles(keyword)
            await asyncio.sleep(random.uniform(2, 4))  # Sleep to avoid rate limiting
        
        # Scrape for a few categories to build a well-rounded dataset
        initial_categories = ["Information Technology & Services", 
                            "Renewable Energy", "Fintech & Banking"]
        
        for category in initial_categories:
            await scrape_for_category(category)
            await asyncio.sleep(random.uniform(5, 8))
        
        # Start periodic scraping
        logger.info("Starting periodic scraping...")
        await run_periodic_scraping()
        
    except Exception as e:
        logger.error(f"Error in data populator service: {e}")
        # In a container environment, it's best to exit on critical errors
        # The container orchestration will restart the service
        sys.exit(1)

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
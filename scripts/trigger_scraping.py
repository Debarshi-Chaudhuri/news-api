#!/usr/bin/env python
"""
Trigger Script for Data Populator

This script can be used to manually trigger scraping for specific keywords
or industry categories. It's useful for debugging or ad-hoc data collection.
"""

import asyncio
import sys
import os
import argparse
import logging

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.elasticsearch import init_elasticsearch, create_index_if_not_exists
from app.services.scraper_service import ScraperService
from app.core.constants import NEWS_KEYWORDS, INDUSTRY_CATEGORIES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def run_scraper(keyword=None, category=None, all_keywords=False, all_categories=False):
    """Run the scraper with specified parameters."""
    # Initialize Elasticsearch
    init_elasticsearch()
    await create_index_if_not_exists()
    
    if all_keywords:
        logger.info(f"Scraping for all {len(NEWS_KEYWORDS)} keywords")
        await ScraperService.run_scraper_for_all_keywords()
        return
    
    if all_categories:
        logger.info(f"Scraping for all {len(INDUSTRY_CATEGORIES)} industry categories")
        await ScraperService.scrape_industry_specific_news()
        return
    
    if keyword:
        logger.info(f"Scraping for keyword: {keyword}")
        await ScraperService.scrape_and_store_articles(keyword)
    
    if category:
        if category not in INDUSTRY_CATEGORIES:
            logger.error(f"Invalid category: {category}")
            logger.info(f"Available categories: {list(INDUSTRY_CATEGORIES.keys())}")
            return
        
        logger.info(f"Scraping for category: {category}")
        await ScraperService.scrape_industry_specific_news(category=category)

async def main():
    parser = argparse.ArgumentParser(description='Trigger news scraping')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--keyword', '-k', type=str, help='Specific keyword to scrape')
    group.add_argument('--category', '-c', type=str, help='Specific industry category to scrape')
    group.add_argument('--all-keywords', '-ak', action='store_true', help='Scrape all keywords')
    group.add_argument('--all-categories', '-ac', action='store_true', help='Scrape all categories')
    group.add_argument('--list', '-l', action='store_true', help='List available keywords and categories')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available Keywords:")
        for keyword in NEWS_KEYWORDS:
            print(f"  - {keyword}")
        
        print("\nAvailable Categories:")
        for category, keywords in INDUSTRY_CATEGORIES.items():
            print(f"  - {category}")
        return
    
    await run_scraper(
        keyword=args.keyword,
        category=args.category,
        all_keywords=args.all_keywords,
        all_categories=args.all_categories
    )

if __name__ == '__main__':
    asyncio.run(main())
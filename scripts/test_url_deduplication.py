# scripts/test_url_deduplication.py
import asyncio
import json
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch
from app.db.repositories import NewsRepository
from app.models.news import NewsArticleCreate

async def test_url_deduplication():
    """
    Test the URL deduplication functionality by:
    1. Creating a test article
    2. Attempting to create another article with the same URL but with query parameters
    3. Checking that the second article is recognized as a duplicate
    """
    # Initialize Elasticsearch
    es_client = init_elasticsearch()
    
    # Test URLs - these should all deduplicate to the same normalized URL
    test_urls = [
        "https://example.com/article/123",
        "https://example.com/article/123?utm_source=twitter",
        "https://example.com/article/123#section1",
        "https://example.com/article/123/?ref=homepage",
        "HTTPS://EXAMPLE.COM/article/123"
    ]
    
    print("Testing URL normalization:")
    for url in test_urls:
        normalized = NewsRepository._normalize_url(url)
        print(f"  Original: {url}")
        print(f"  Normalized: {normalized}")
        print()
    
    # Create a base test article
    base_article = {
        "title": "Test Deduplication Article",
        "content": "This is a test article to check URL deduplication.",
        "summary": "Test summary",
        "author": "Test Author",
        "source": "Test Source",
        "url": test_urls[0],  # Use the first URL in our list
        "tags": ["test", "deduplication"]
    }
    
    print(f"Creating base article with URL: {test_urls[0]}")
    article_create = NewsArticleCreate(**base_article)
    base_created = await NewsRepository.create(article_create)
    print(f"  Base article created with ID: {base_created.id}")
    
    # Now try to create a duplicate article with a different URL (with query parameters)
    duplicate_article = base_article.copy()
    duplicate_article["title"] = "Duplicate Test Article"  # Change title to see if it updates
    duplicate_article["url"] = test_urls[1]  # URL with query parameters
    
    print(f"Creating article with duplicate normalized URL: {test_urls[1]}")
    duplicate_create = NewsArticleCreate(**duplicate_article)
    result = await NewsRepository.create(duplicate_create)
    
    # Check if it was recognized as a duplicate (same ID) or created as new
    if result.id == base_created.id:
        print("  SUCCESS: Duplicate detected and original article updated")
        print(f"  Updated title: {result.title}")
    else:
        print("  FAILURE: Duplicate not detected, new article created")
        print(f"  New article ID: {result.id}")
    
    # Try once more with a different URL variation
    another_duplicate = base_article.copy()
    another_duplicate["title"] = "Another Duplicate Test Article"
    another_duplicate["url"] = test_urls[3]  # Different URL variation
    
    print(f"Creating another article with duplicate normalized URL: {test_urls[3]}")
    another_create = NewsArticleCreate(**another_duplicate)
    another_result = await NewsRepository.create(another_create)
    
    if another_result.id == base_created.id:
        print("  SUCCESS: Another duplicate detected and original article updated")
        print(f"  Updated title: {another_result.title}")
    else:
        print("  FAILURE: Duplicate not detected, new article created")
        print(f"  New article ID: {another_result.id}")
    
    # Clean up: delete the test articles
    print("\nCleaning up test data...")
    success = await NewsRepository.delete(base_created.id)
    if success:
        print("  Test articles deleted")
    else:
        print("  Failed to delete test articles")
    
    # Close Elasticsearch connection
    await es_client.close()
    print("\nTest completed")

if __name__ == "__main__":
    asyncio.run(test_url_deduplication())
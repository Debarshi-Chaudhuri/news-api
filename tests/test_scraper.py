import pytest
from unittest.mock import patch, MagicMock
from app.services.scraper_service import ScraperService

@pytest.mark.asyncio
async def test_search_google_news():
    # Mock the aiohttp ClientSession
    with patch("app.services.scraper_service.aiohttp.ClientSession") as mock_session:
        # Setup the mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = MagicMock(return_value="""
            <html>
                <body>
                    <div class="SoaBEf">
                        <a href="/url?q=https://example.com/article1&sa=U">Article 1</a>
                    </div>
                    <div class="SoaBEf">
                        <a href="/url?q=https://example.com/article2&sa=U">Article 2</a>
                    </div>
                </body>
            </html>
        """)
        
        # Setup the context manager returns
        mock_session_instance = MagicMock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        
        # Call the function
        urls = await ScraperService.search_google_news("technology")
        
        # Verify results
        assert len(urls) == 2
        assert urls[0] == "https://example.com/article1"
        assert urls[1] == "https://example.com/article2"

@pytest.mark.asyncio
async def test_scrape_article():
    # Mock the newspaper Article
    with patch("app.services.scraper_service.Article") as mock_article_class:
        # Setup the mock article
        mock_article = MagicMock()
        mock_article_class.return_value = mock_article
        
        # Configure mock article properties
        mock_article.title = "Test Article"
        mock_article.text = "Test content"
        mock_article.summary = "Test summary"
        mock_article.authors = ["Test Author"]
        mock_article.source_url = "example.com"
        mock_article.publish_date = None
        mock_article.keywords = ["tech", "news"]
        
        # Call the function
        url = "https://example.com/article"
        article_data = await ScraperService.scrape_article(url)
        
        # Verify results
        assert article_data is not None
        assert article_data["title"] == "Test Article"
        assert article_data["content"] == "Test content"
        assert article_data["summary"] == "Test summary"
        assert article_data["author"] == "Test Author"
        assert article_data["tags"] == ["tech", "news"]
        assert article_data["url"] == url

@pytest.mark.asyncio
async def test_scrape_and_store_articles():
    # Mock dependent functions
    with patch("app.services.scraper_service.ScraperService.search_google_news") as mock_search, \
         patch("app.services.scraper_service.ScraperService.scrape_article") as mock_scrape, \
         patch("app.services.news_service.NewsService.create_news") as mock_create:
        
        # Configure mocks
        mock_search.return_value = ["https://example.com/article1", "https://example.com/article2"]
        
        article1 = {
            "title": "Article 1",
            "content": "Content 1",
            "tags": []
        }
        
        article2 = {
            "title": "Article 2",
            "content": "Content 2",
            "tags": ["business"]
        }
        
        mock_scrape.side_effect = [article1, article2]
        
        # Mock the NewsArticleCreate model
        with patch("app.services.scraper_service.NewsArticleCreate") as mock_model:
            mock_model.return_value = MagicMock()
            
            # Call the function
            result = await ScraperService.scrape_and_store_articles("business")
            
            # Verify results
            assert result == 2
            assert mock_search.call_count == 1
            assert mock_scrape.call_count == 2
            assert mock_create.call_count == 2
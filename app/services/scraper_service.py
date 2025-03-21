import aiohttp
import asyncio
import logging
import ssl
import certifi
from datetime import datetime
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import random
import time

from app.core.constants import NEWS_KEYWORDS
from app.core.config import settings
from app.models.news import NewsArticleCreate
from app.services.news_service import NewsService

logger = logging.getLogger(__name__)

class ScraperService:
    @staticmethod
    @staticmethod
    async def search_google_news(keyword: str, category: str = "business", country: str = "india") -> List[str]:
        """
        Search Google News for the given keyword and return article URLs.
        Always focuses on Indian business news.
        
        Args:
            keyword: The keyword to search for
            category: The news category to search in (defaults to business)
            country: The country to focus on (defaults to india)
            
        Returns:
            List of article URLs
        """
        # Ensure we always search for India and business
        if "india" not in country.lower():
            country = f"india {country}"
        
        if "business" not in category.lower():
            category = f"business {category}"
        
        # Google News search URL with India and business focus
        url = f"https://www.google.com/search?q={keyword}+{category}+{country}&tbm=nws"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            # Rest of the method remains the same...
            # Configure SSL context based on settings
            ssl_context = None
            if not settings.SCRAPER_VERIFY_SSL:
                logger.warning("SSL certificate verification is disabled. This is not recommended for production.")
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            else:
                # Use certifi's certificates
                ssl_context = ssl.create_default_context(cafile=certifi.where())

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, ssl=ssl_context) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch search results for {keyword}. Status: {response.status}")
                        return []
                    
                    html = await response.text()
            
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            
            # Find all news article links
            article_links = []
            
            # Google News search results typically have different class names
            # Try multiple selectors to increase chances of finding links
            selectors = [
                "div.SoaBEf", # Main result container
                "div.dbsr", # Another common result container
                "a.WlydOe", # Direct link selector
                "div.n0jPhd", # Title container that might contain links
                "g-card" # General card container
            ]
            
            for selector in selectors:
                results = soup.select(selector)
                if results:
                    for result in results:
                        # Try to find the link within the container
                        link_element = result.find("a")
                        if link_element and "href" in link_element.attrs:
                            href = link_element["href"]
                            if href.startswith("/url?q="):
                                # Extract the actual URL from Google's redirect
                                actual_url = href.split("/url?q=")[1].split("&sa=")[0]
                                article_links.append(actual_url)
                            elif href.startswith("http"):
                                article_links.append(href)
            
            # If we still don't have links, try a more generic approach
            if not article_links:
                for link in soup.find_all("a"):
                    href = link.get("href", "")
                    if "url?q=" in href and "google" not in href:
                        actual_url = href.split("url?q=")[1].split("&sa=")[0]
                        article_links.append(actual_url)
            
            # Return the top 5 unique links (increased from 2 to get more articles)
            unique_links = []
            for link in article_links:
                if link not in unique_links:
                    unique_links.append(link)
                    if len(unique_links) >= 5:
                        break
            
            return unique_links
        
        except Exception as e:
            logger.error(f"Error searching Google News for {keyword}: {e}")
            return []

    @staticmethod
    async def scrape_article(url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape article content from the given URL using newspaper3k.
        Modified to ensure India and business focus in categories and tags.
        
        Args:
            url: The URL of the article to scrape
            
        Returns:
            Dictionary with article data or None if scraping failed
        """
        try:
            # Configure newspaper3k with SSL settings
            if not settings.SCRAPER_VERIFY_SSL:
                # Disable SSL verification warnings for requests
                import requests
                from requests.packages.urllib3.exceptions import InsecureRequestWarning
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                
                # Use a non-verifying session with newspaper
                from newspaper import Article, Config
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                config.request_timeout = 10
                config.fetch_images = False
                
                # Create a custom session with SSL verification disabled
                session = requests.Session()
                session.verify = False
                
                # Use a custom adapter to mount to the session
                article = Article(url, config=config)
                
                # Monkey patch the session's get method to use our non-verifying session
                # This is a hack but necessary since newspaper3k doesn't expose the session directly
                original_get = requests.get
                try:
                    requests.get = session.get
                    article.download()
                finally:
                    # Restore the original get method
                    requests.get = original_get
            else:
                # Use default settings with verification
                from newspaper import Article
                article = Article(url)
                article.download()
                
            article.parse()
            
            # Try to extract additional metadata with NLP
            try:
                article.nlp()  # Extract keywords, summary
            except Exception as nlp_error:
                if "Resource punkt not found" in str(nlp_error) or "punkt_tab not found" in str(nlp_error):
                    logger.warning("NLTK resources missing. NLP processing will be skipped. Download with: nltk.download('punkt')")
                else:
                    logger.warning(f"Error during NLP processing: {nlp_error}. Continuing without NLP.")
            
            # Extract published date or use current date
            pub_date = article.publish_date if article.publish_date else datetime.utcnow()
            pub_date_str = pub_date.isoformat() if hasattr(pub_date, 'isoformat') else str(pub_date)
            
            # Extract source from URL
            source = None
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                source = domain.replace("www.", "")
            except Exception:
                source = article.source_url
            
            # Default categories to include Business and India
            categories = ["Business"]
            if "India" not in categories:
                categories.append("India")
                
            # Extract tags/keywords
            tags = []
            if hasattr(article, 'keywords') and article.keywords:
                tags = [str(k) for k in article.keywords[:5]]
                
            # Add India and Business tags if not already present
            if "india" not in [t.lower() for t in tags]:
                tags.append("india")
            if "business" not in [t.lower() for t in tags]:
                tags.append("business")
            
            # Create article data in our format
            article_data = {
                "title": str(article.title) if article.title else "Untitled Article",
                "content": str(article.text) if article.text else "No content available",
                "summary": str(article.summary) if hasattr(article, 'summary') and article.summary else None,
                "author": str(article.authors[0]) if article.authors and len(article.authors) > 0 else None,
                "source": str(source) if source else None,
                "published_date": pub_date_str,
                "categories": categories,
                "tags": tags,
                "url": str(url),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Validate required fields
            if not article_data["title"] or not article_data["content"]:
                logger.warning(f"Missing required fields for article from {url}")
                return None
            
            return article_data
        
        except Exception as e:
            logger.error(f"Error scraping article from {url}: {e}")
            return None
        
    @staticmethod
    async def scrape_and_store_articles(keyword: str) -> int:
        """
        Search for articles with the given keyword, scrape them and store in Elasticsearch.
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            Number of articles scraped and stored
        """
        # Search for articles
        urls = await ScraperService.search_google_news(keyword)
        
        if not urls:
            logger.warning(f"No URLs found for keyword: {keyword}")
            return 0
        
        articles_stored = 0
        
        # Scrape and store each article
        for url in urls:
            try:
                article_data = await ScraperService.scrape_article(url)
                
                if not article_data:
                    continue
                
                # Add our keyword to the tags
                if keyword.lower() not in [tag.lower() for tag in article_data["tags"]]:
                    article_data["tags"].append(keyword.lower())
                
                # Sanitize data to ensure it's JSON serializable
                ScraperService._sanitize_article_data(article_data)
                
                # Create article using the NewsService
                try:
                    article_create = NewsArticleCreate(**article_data)
                    await NewsService.create_news(article_create)
                    articles_stored += 1
                    logger.info(f"Article stored successfully: {article_data['title']}")
                except Exception as e:
                    logger.error(f"Error storing article: {e}")
                    logger.error(f"Article data that failed: {article_data}")
            except Exception as e:
                logger.error(f"Error processing article from {url}: {e}")
        
        return articles_stored
    
    @staticmethod
    def _sanitize_article_data(article_data: Dict[str, Any]) -> None:
        """
        Sanitize article data to ensure it's JSON serializable.
        
        Args:
            article_data: The article data to sanitize
        """
        # Ensure title and content are strings and not None
        article_data["title"] = str(article_data.get("title", "")) if article_data.get("title") else "Untitled Article"
        article_data["content"] = str(article_data.get("content", "")) if article_data.get("content") else "No content available"
        
        # Ensure summary is a string
        if article_data.get("summary") is None:
            article_data["summary"] = ""
        else:
            article_data["summary"] = str(article_data["summary"])
        
        # Ensure author is a string
        if article_data.get("author") is None:
            article_data["author"] = ""
        else:
            article_data["author"] = str(article_data["author"])
        
        # Ensure source is a string
        if article_data.get("source") is None:
            article_data["source"] = ""
        else:
            article_data["source"] = str(article_data["source"])
        
        # Ensure tags and categories are lists of strings
        if not isinstance(article_data.get("tags", []), list):
            article_data["tags"] = []
        else:
            article_data["tags"] = [str(tag) for tag in article_data["tags"]]
        
        if not isinstance(article_data.get("categories", []), list):
            article_data["categories"] = []
        else:
            article_data["categories"] = [str(cat) for cat in article_data["categories"]]
        
        # Handle URL
        if article_data.get("url") is None:
            article_data["url"] = ""
        else:
            article_data["url"] = str(article_data["url"])
    
    @staticmethod
    async def run_scraper_for_all_keywords() -> int:
        """
        Run the scraper for all keywords in the NEWS_KEYWORDS list.
        
        Returns:
            Total number of articles scraped and stored
        """
        total_articles = 0
        
        for keyword in NEWS_KEYWORDS:
            logger.info(f"Scraping articles for keyword: {keyword}")
            articles_stored = await ScraperService.scrape_and_store_articles(keyword)
            total_articles += articles_stored
            
            # Sleep between requests to avoid rate limiting
            await asyncio.sleep(random.uniform(3, 5))
        
        logger.info(f"Scraping complete. Total articles stored: {total_articles}")
        return total_articles
    
    @staticmethod
    async def schedule_periodic_scraping(interval_minutes: int = 60):
        """
        Schedule periodic scraping of news articles.
        
        Args:
            interval_minutes: Time interval between scraping runs in minutes
        """
        while True:
            try:
                logger.info(f"Starting scheduled news scraping...")
                await ScraperService.run_scraper_for_all_keywords()
            except Exception as e:
                logger.error(f"Error in scheduled scraping: {e}")
            
            # Sleep until next scheduled run
            logger.info(f"Sleeping for {interval_minutes} minutes until next scraping run")
            await asyncio.sleep(interval_minutes * 60)

    @staticmethod
    async def scrape_industry_specific_news(category: str = None, max_articles_per_keyword: int = 2):
        """
        Scrape news specific to industries defined in the INDUSTRY_CATEGORIES.
        
        Args:
            category: Optional specific industry category to scrape. If None, all categories are scraped.
            max_articles_per_keyword: Maximum number of articles to scrape per keyword
            
        Returns:
            Total number of articles scraped and stored
        """
        from app.core.constants import INDUSTRY_CATEGORIES
        
        total_articles = 0
        
        # If a specific category is provided, only scrape for that category
        if category:
            # Validate the category
            if category not in INDUSTRY_CATEGORIES:
                logger.error(f"Invalid industry category: {category}")
                return 0
                
            categories_to_scrape = {category: INDUSTRY_CATEGORIES[category]}
        else:
            # Scrape for all categories
            categories_to_scrape = INDUSTRY_CATEGORIES
        
        for category_name, keywords in categories_to_scrape.items():
            logger.info(f"Scraping for industry category: {category_name}")
            
            # First scrape using the category name itself
            logger.info(f"Searching for industry category: {category_name}")
            articles_stored = await ScraperService.scrape_and_store_articles(category_name)
            total_articles += articles_stored
            
            # Then scrape using each specific keyword for that category
            for keyword in keywords:
                logger.info(f"Searching for industry keyword: {keyword} (Category: {category_name})")
                
                # Combine the keyword with the category name for better results
                search_term = f"{keyword} {category_name}"
                
                articles_stored = await ScraperService.scrape_and_store_articles(
                    search_term, 
                    category=category_name, 
                    max_articles=max_articles_per_keyword
                )
                
                total_articles += articles_stored
                
                # Sleep between requests to avoid rate limiting
                await asyncio.sleep(random.uniform(3, 5))
            
            # Sleep a bit longer between categories
            await asyncio.sleep(random.uniform(5, 8))
        
        logger.info(f"Industry-specific scraping complete. Total articles stored: {total_articles}")
        return total_articles
    
    @staticmethod
    async def scrape_and_store_articles(
        keyword: str, 
        category: str = None,
        max_articles: int = 2
    ) -> int:
        """
        Search for articles with the given keyword, scrape them and store in Elasticsearch.
        
        Args:
            keyword: The keyword to search for
            category: Optional industry category to associate with the articles
            max_articles: Maximum number of articles to scrape and store
            
        Returns:
            Number of articles scraped and stored
        """
        # Search for articles
        urls = await ScraperService.search_google_news(keyword)
        
        if not urls:
            logger.warning(f"No URLs found for keyword: {keyword}")
            return 0
        
        articles_stored = 0
        
        # Limit the number of URLs to process
        urls = urls[:max_articles]
        
        # Scrape and store each article
        for url in urls:
            try:
                article_data = await ScraperService.scrape_article(url)
                
                if not article_data:
                    continue
                
                # Add our keyword to the tags
                if keyword.lower() not in [tag.lower() for tag in article_data["tags"]]:
                    article_data["tags"].append(keyword.lower())
                
                # If a category was provided, add it to the categories
                if category and category not in article_data["categories"]:
                    article_data["categories"].append(category)
                
                # Sanitize data to ensure it's JSON serializable
                ScraperService._sanitize_article_data(article_data)
                
                # Create article using the NewsService
                try:
                    article_create = NewsArticleCreate(**article_data)
                    await NewsService.create_news(article_create)
                    articles_stored += 1
                    logger.info(f"Article stored successfully: {article_data['title']}")
                except Exception as e:
                    logger.error(f"Error storing article: {e}")
                    logger.error(f"Article data that failed: {article_data}")
            except Exception as e:
                logger.error(f"Error processing article from {url}: {e}")
        
        return articles_stored
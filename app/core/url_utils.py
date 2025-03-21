# app/core/url_utils.py
import logging
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)

def normalize_url(url):
    """
    Normalize a URL by removing query parameters and fragments.
    
    Args:
        url: The URL to normalize
        
    Returns:
        Normalized URL without query parameters or fragments
    
    Example:
        >>> normalize_url("https://example.com/path?q=search&lang=en#section")
        'https://example.com/path'
    """
    if not url:
        return ""
        
    try:
        # Convert to string if needed
        url_str = str(url)
        
        # Parse the URL
        parsed_url = urlparse(url_str)
        
        # Rebuild without query parameters and fragments
        normalized = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            '',  # params
            '',  # query
            ''   # fragment
        ))
        
        # Remove trailing slash if present for more consistent matching
        if normalized.endswith('/') and len(normalized) > 1:
            normalized = normalized[:-1]
            
        # Convert to lowercase for case-insensitive matching
        normalized = normalized.lower()
        
        return normalized
    except Exception as e:
        logger.warning(f"Error normalizing URL '{url}': {e}")
        return str(url).lower()  # Fall back to lowercased string


def test_url_normalization(urls):
    """
    Test URL normalization on a list of URLs.
    Useful for debugging.
    
    Args:
        urls: List of URLs to test
        
    Returns:
        Dictionary mapping original URLs to their normalized versions
    """
    results = {}
    for url in urls:
        normalized = normalize_url(url)
        results[url] = normalized
        
    return results
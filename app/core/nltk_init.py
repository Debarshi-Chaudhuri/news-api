import nltk
import logging
import os
import ssl
from app.core.config import settings

logger = logging.getLogger(__name__)

# List of required NLTK resources for newspaper3k
REQUIRED_NLTK_RESOURCES = [
    'punkt',
    'maxent_treebank_pos_tagger',
    'averaged_perceptron_tagger',
    'maxent_ne_chunker',
    'words',
    'stopwords'
]

def download_nltk_resources():
    """
    Download required NLTK resources if they don't exist.
    This function should be called during application startup.
    """
    # Set NLTK data path to ensure permissions
    nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
    os.environ['NLTK_DATA'] = nltk_data_dir
    
    # Create the directory if it doesn't exist
    if not os.path.exists(nltk_data_dir):
        try:
            os.makedirs(nltk_data_dir)
            logger.info(f"Created NLTK data directory at {nltk_data_dir}")
        except Exception as e:
            logger.warning(f"Could not create NLTK data directory: {e}")
    
    # Handle SSL verification based on application settings
    if not settings.SCRAPER_VERIFY_SSL:
        logger.warning("SSL certificate verification is disabled for NLTK downloads. This is not recommended for production.")
        try:
            # Create unverified context
            ssl._create_default_https_context = ssl._create_unverified_context
        except AttributeError:
            logger.error("Failed to disable SSL verification for NLTK downloads")
    
    # Download each required resource
    for resource in REQUIRED_NLTK_RESOURCES:
        try:
            nltk.download(resource, quiet=True, download_dir=nltk_data_dir)
            logger.info(f"Downloaded NLTK resource: {resource}")
        except Exception as e:
            logger.error(f"Failed to download NLTK resource {resource}: {e}")
            logger.info("If you're experiencing SSL errors, try setting SCRAPER_VERIFY_SSL=False in your .env file.")
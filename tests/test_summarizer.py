import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
import json
from aiohttp import ClientResponse, ClientSession

from app.services.summarizer_service import SummarizerService
from app.core.config import settings
import logging

# Sample test data
SAMPLE_TEXT = """
The Global Climate Summit concluded today with participating nations reaching agreements on reducing carbon emissions and increasing renewable energy investments. The historic deal aims to limit global warming to 1.5 degrees Celsius above pre-industrial levels by 2050. Nations have committed to more aggressive carbon reduction targets, with developed countries pledging additional funding to help developing nations transition to cleaner energy sources. Environmental groups cautiously welcomed the agreement while emphasizing the need for concrete action and accountability mechanisms. Business leaders from major corporations also attended the summit, announcing private sector initiatives to support sustainable practices across global supply chains.
"""

logger = logging.getLogger(__name__)

# Direct API tests
class TestSummarizerService:
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.post')
    async def test_summarize_text_success(self, mock_post):
        
        # Call the method under test
        result = await SummarizerService.summarize_text(SAMPLE_TEXT, 200)
        
        logger.debug(f"Summarized text: {result}")

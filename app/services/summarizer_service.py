import aiohttp
import logging
import os
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class SummarizerService:
    """Service for summarizing content using Claude AI APIs."""
    
    @staticmethod
    async def summarize_text(text: str, max_length: int = 200) -> Optional[str]:
        """
        Summarize text using Claude API.
        
        Args:
            text: The text to summarize
            max_length: The maximum length of the summary in characters
            
        Returns:
            Summarized text or None if summarization failed
        """
        if not text:
            return None
            
        if not settings.CLAUDE_API_KEY:
            logger.warning("Claude API key is not set. Summarization is not available.")
            return None
            
        # Prepare the request to Claude API
        try:
            async with aiohttp.ClientSession() as session:
                api_url = settings.CLAUDE_API_URL
                
                # Create the prompt for Claude
                prompt = f"""Summarize the following text in about {max_length} characters:{text}Your summary should be concise but include the most important points."""
                
                # Prepare the request payload
                payload = {
                    "model": settings.CLAUDE_MODEL,
                    "max_tokens": max(500, max_length // 4),  # Ensure we have enough tokens for the response
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
                
                headers = {
                    "x-api-key": settings.CLAUDE_API_KEY,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"  # Use appropriate API version
                }
                
                # Make the API call
                async with session.post(api_url, json=payload, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Claude API request failed: {response.status} - {error_text}")
                        return None
                        
                    data = await response.json()
                    
                    # Extract the summary from the response
                    # Format depends on the Claude API version
                    if "content" in data and isinstance(data["content"], list):
                        # For newer Claude API format
                        for content_block in data["content"]:
                            if content_block.get("type") == "text":
                                # Remove the prefix that Claude often adds to summaries
                                summary_text = content_block.get("text", "").strip()
                                prefixes_to_remove = [
                                    "Here's a concise summary in about 150 characters:\n\n",
                                    "Here's a summary in about 150 characters:\n\n",
                                    "Here's a concise summary:\n\n",
                                    "Here's a summary:\n\n",
                                    "Summary:\n\n"
                                ]
                                
                                for prefix in prefixes_to_remove:
                                    if summary_text.startswith(prefix):
                                        summary_text = summary_text[len(prefix):].strip()
                                        break
                                
                                return summary_text

                    elif "completion" in data:
                        # For older Claude API format
                        return data["completion"].strip()
                        
                    # Fallback
                    logger.error(f"Unexpected Claude API response format: {data}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error summarizing text with Claude API: {e}")
            return None
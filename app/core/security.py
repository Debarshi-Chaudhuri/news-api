import secrets
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

# You can implement API key authentication here
# This is a simple example - for production, use a more secure approach

API_KEY_NAME = "X-API-Key"
API_KEY = secrets.token_urlsafe(32)  # Generate a random API key for development

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Depends(api_key_header)) -> Optional[str]:
    """Validate API key if it's provided."""
    # For development purposes, allow requests without API key
    # In production, uncomment the code below to require API key
    
    """
    if not api_key_header or api_key_header != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    """
    
    return api_key_header
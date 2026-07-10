from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.config import API_KEY

# Tell Fast API to look for header called "X-API-KEY"
api_key_header = APIKeyHeader(name="X-API-KEY")

async def get_api_key(api_key: str = Security(api_key_header)):
    '''
    Check if the provided API key in the "X-API-KEY" header is valid
    '''
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key or missing API Key",
        )
    
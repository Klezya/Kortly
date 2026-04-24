from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.database.core import SessionDep
from src.logging import logger
from .service import acortar_url
from .model import ShortenUrlRequest
from .exception import LinkGenerationError

router = APIRouter(tags=["links"])

@router.post("/shorten", status_code=status.HTTP_201_CREATED)
async def shorten_url(request: ShortenUrlRequest, session: SessionDep):
    try:
        short_code = acortar_url(request.url, session)
        return {"short_code": short_code,
                "original_url": request.url,
                "short_url": f"http://localhost:8000/{short_code}"}
    
    except LinkGenerationError:
        logger.error(f"Failed to generate a unique short code for URL: {request.url}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate a unique short code, please retry later.")
    
    except Exception as e:
        logger.critical(f"Error acortando la URL {request.url}, ERROR: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
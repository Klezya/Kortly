from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from src.database.core import SessionDep
from src.logging import logger
from .service import acortar_url, redirect_url
from .model import ShortenUrlRequest
from .exception import LinkGenerationError, LinkNotFoundError

router = APIRouter(tags=["links"])

@router.post("/shorten", status_code=status.HTTP_201_CREATED)
async def shorten_url(request: ShortenUrlRequest, session: SessionDep):
    try:
        short_code = acortar_url(request.url, session)
        return {"short_code": short_code,
                "original_url": request.url,
                "short_url": f"http://127.0.0.1:8000/{short_code}"}
    
    except LinkGenerationError:
        logger.warning(f"Failed to generate a unique short code for URL: {request.url}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate a unique short code, please retry later.")
    
    except Exception as e:
        logger.critical(f"Error acortando la URL {request.url}, ERROR: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{short_code}")
async def redirect(short_code: str, session: SessionDep):
    try:
        original_url = redirect_url(short_code, session)
        return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)
    
    except LinkNotFoundError:
        logger.warning(f"Short code no encontrado: {short_code}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found.")
    
    except Exception as e:
        logger.critical(f"Error redirigiendo el short code {short_code}, ERROR: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
from secrets import token_urlsafe
from sqlmodel import Session, select

from src.entities.links import Link
from src.logging import logger
from .exception import LinkGenerationError, LinkNotFoundError

MAX_INTENTOS = 5
LARGO_CODIGO = 8

def acortar_url(url: str, session: Session, large: int = LARGO_CODIGO) -> str:
    
    for _ in range(MAX_INTENTOS):
        url_code = token_urlsafe(large*2)[:large]

        db_statement = select(Link).where(Link.short_code == url_code)
        existing_link = session.exec(db_statement).first()
        if not existing_link:
            break
    else:
        logger.warning(f"No se pudo generar un código único después {MAX_INTENTOS} intentos, para la url: {url}")
        raise LinkGenerationError
    
    new_link = Link(
        original_url=url,
        short_code=url_code,
        owner_id=None
    )

    session.add(new_link)
    session.commit()
    session.refresh(new_link)

    return new_link.short_code

def redirect_url(short_code: str, session: Session) -> str:
    db_statement = select(Link).where(Link.short_code == short_code)
    link = session.exec(db_statement).first()
    if not link:
        logger.warning(f"Short code no encontrado: {short_code}")
        raise LinkNotFoundError
    
    link.visits += 1

    session.add(link)
    session.commit()

    return link.original_url
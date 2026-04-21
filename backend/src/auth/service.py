from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from uuid import UUID
import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

from src.entities.users import User
from src.auth.model import TokenData
from src.logging import logger
from src.settings import settings

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def autenticate_user(email: str, password: str, session: Session) -> User | None:
    statement = session.select(User).where(User.email == email)
    user: User | None = session.exec(statement).first()
    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Failed login attempt for email: {email}")
        return None
    return user

def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        "sub": email, 
        "user_id": str(user_id),
        "iss": settings.ISSUER,
        "exp": datetime.now(timezone.utc) + expires_delta,
        }
    
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, 
                             settings.SECRET_KEY, 
                             algorithms=[settings.ALGORITHM], 
                             issuer=settings.ISSUER)
        user_id: str = payload.get("user_id")
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except jwt.PyJWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None
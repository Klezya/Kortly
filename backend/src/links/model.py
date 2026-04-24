from sqlmodel import SQLModel
import uuid

class ShortenUrlRequest(SQLModel):
    url: str

class LinkToCreate(SQLModel):
    original_url: str
    short_code: str
    owner_id: uuid.UUID | None

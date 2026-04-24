from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid

class Link(SQLModel, table=True):
    __tablename__ = "links"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    original_url: str
    short_code: str = Field(unique=True, index=True)
    owner_id: uuid.UUID | None = Field(foreign_key="users.id")
    visits: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):   
    # Database settings
    DATABASE_URL: str

    # Debug
    DEBUG: bool = False

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    ISSUER: str = "Kortly"

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

settings = Settings()

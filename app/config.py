from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

class Settings(BaseSettings):
    # WhatsApp API settings
    whatsapp_api_url: str = "https://graph.facebook.com/v18.0"
    whatsapp_phone_number_id: str
    whatsapp_access_token: str
    
    # Database settings
    database_url: str = "postgresql://postgres:postgres@localhost:5432/whatsapp_db"
    
    # Application settings
    app_name: str = "TMBC WhatsApp Messaging API"
    debug: bool = True
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Database configuration
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency function that yields a database session and ensures it's closed
    after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
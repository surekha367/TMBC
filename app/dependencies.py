from fastapi import Depends
from sqlalchemy.orm import Session
from app.config import get_db,SessionLocal
from app.services.whatsapp_service import WhatsAppService

def get_db_session():
    """
    Dependency function to get database session
    """
    # return get_db
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_whatsapp_service():
    """
    Dependency function to get WhatsApp service instance
    """
    return  WhatsAppService()
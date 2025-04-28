from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
import phonenumbers
from app.utils import validate_phone_number
from app.exceptions import InvalidPhoneNumberException

class MessageRequest(BaseModel):
    """
    Request model for sending WhatsApp messages
    """
    phone_number: str = Field(..., description="Recipient's phone number with country code")
    
    @validator('phone_number')
    def validate_phone(cls, value):
        """Validate phone number format using phonenumbers library"""
        try:
            return validate_phone_number(value)
        except InvalidPhoneNumberException as e:
            raise ValueError(str(e))

class MessageResponse(BaseModel):
    """
    Response model for WhatsApp message API
    """
    success: bool
    message: str
    message_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class MessageLogSchema(BaseModel):
    """
    Schema for message log data
    """
    id: int
    phone_number: str
    message: str
    status: str
    created_at: datetime
    
    class Config:
        orm_mode = True
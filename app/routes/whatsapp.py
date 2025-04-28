from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db

from app.schemas import MessageRequest, MessageResponse, MessageLogSchema
from app.services.whatsapp_service import WhatsAppService
from app.dependencies import get_db_session, get_whatsapp_service
from app.exceptions import InvalidPhoneNumberException, WhatsAppAPIException
from app.models import MessageLog

router = APIRouter(
    prefix="/whatsapp",
    tags=["whatsapp"]
)

@router.get("/send_message", response_model=MessageResponse)
async def send_whatsapp_message(
    phone_number: str = Query(..., description="Recipient's phone number with country code"),
    db: Session = Depends(get_db),
    whatsapp_service: WhatsAppService = Depends(get_whatsapp_service)
):
    """
    Send a test message to the specified WhatsApp number
    
    - **phone_number**: The recipient's phone number with country code
    
    Returns the WhatsApp API response or an error message
    """
    # Create a message request with the phone number
    message_request = MessageRequest(phone_number=phone_number)
    
    try:
        # Send the message
        result = await whatsapp_service.send_message(db, message_request.phone_number)
        
        # Get the message ID from the response if available
        message_id = None
        if result and "messages" in result and len(result["messages"]) > 0:
            message_id = result["messages"][0].get("id")
            
        return MessageResponse(
            success=True,
            message=f"Message sent successfully to {message_request.phone_number}",
            message_id=message_id,
            details=result
        )
    
    except InvalidPhoneNumberException as e:
        # Re-raise to let FastAPI handle it
        raise e
    
    except WhatsAppAPIException as e:
        # Re-raise to let FastAPI handle it
        raise e
    
    except Exception as e:
        # Catch any other exceptions
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": f"Unexpected error: {str(e)}"}
        )

@router.post("/send_message", response_model=MessageResponse)
async def send_whatsapp_message_post(
    request: MessageRequest,
    db: Session = Depends(get_db_session),
    whatsapp_service: WhatsAppService = Depends(get_whatsapp_service)
):
    """
    Send a test message to the specified WhatsApp number (POST method)
    
    - **phone_number**: The recipient's phone number with country code
    
    Returns the WhatsApp API response or an error message
    """
    try:
        # Send the message
        result = await whatsapp_service.send_message(db, request.phone_number)
        
        # Get the message ID from the response if available
        message_id = None
        if result and "messages" in result and len(result["messages"]) > 0:
            message_id = result["messages"][0].get("id")
            
        return MessageResponse(
            success=True,
            message=f"Message sent successfully to {request.phone_number}",
            message_id=message_id,
            details=result
        )
    
    except InvalidPhoneNumberException as e:
        # Re-raise to let FastAPI handle it
        raise e
    
    except WhatsAppAPIException as e:
        # Re-raise to let FastAPI handle it
        raise e
    
    except Exception as e:
        # Catch any other exceptions
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": f"Unexpected error: {str(e)}"}
        )

@router.get("/logs", response_model=List[MessageLogSchema])
async def get_message_logs(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db_session)
):
    """
    Get recent WhatsApp message logs
    
    - **limit**: Maximum number of logs to retrieve (default: 10)
    - **skip**: Number of logs to skip (default: 0)
    
    Returns a list of message logs
    """
    logs = db.query(MessageLog).order_by(MessageLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs
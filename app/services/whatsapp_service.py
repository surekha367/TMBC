import httpx
import json
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.config import settings
from app.models import MessageLog
from app.exceptions import WhatsAppAPIException, ConfigurationException
from app.utils import dict_to_json_string

class WhatsAppService:
    """
    Service class for interacting with the WhatsApp Business API
    """
    def __init__(self):
        self.api_url = settings.whatsapp_api_url
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.access_token = settings.whatsapp_access_token
        
        # Validate configuration
        if not self.phone_number_id or not self.access_token:
            raise ConfigurationException(
                "WhatsApp API credentials not configured. Please set WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN."
            )
    
    async def send_message(self, db: Session, recipient_phone: str) -> Dict[str, Any]:
        """
        Send a text message via WhatsApp Business API
        
        Args:
            db: Database session
            recipient_phone: The recipient's phone number in E.164 format
            
        Returns:
            API response as dictionary
            
        Raises:
            WhatsAppAPIException: If there's an error in the API call
        """
        # Create message log entry with pending status
        message_log = MessageLog(
            phone_number=recipient_phone,
            message="Hello, this is a test message from our TMBC bot!",
            status="pending"
        )
        db.add(message_log)
        db.commit()
        db.refresh(message_log)
        
        # Prepare API call
        endpoint = f"{self.api_url}/{self.phone_number_id}/messages"
        
        # Prepare the message payload according to WhatsApp API requirements
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hello, this is a test message from our TMBC bot!"
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(endpoint, json=payload, headers=headers)
                
                # Check if request was successful
                if response.status_code != 200:
                    # Update message log with failure
                    message_log.status = "failed"
                    message_log.error_message = f"API Error: {response.status_code} - {response.text}"
                    db.commit()
                    
                    raise WhatsAppAPIException(
                        f"WhatsApp API error: {response.status_code} - {response.text}"
                    )
                
                # Process success response
                response_data = response.json()
                
                # Update message log with success
                message_log.status = "sent"
                message_log.response_data = dict_to_json_string(response_data)
                db.commit()
                
                return response_data
                
        except httpx.RequestError as e:
            # Update message log with failure
            message_log.status = "failed"
            message_log.error_message = f"Request Error: {str(e)}"
            db.commit()
            
            raise WhatsAppAPIException(f"Error sending WhatsApp message: {str(e)}")
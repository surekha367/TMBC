import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    """Mock database session for testing"""
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_whatsapp_service():
    """Mock WhatsApp service for testing"""
    with patch("app.routes.whatsapp.WhatsAppService") as mock:
        mock_instance = mock.return_value
        mock_instance.send_message.return_value = {
            "messaging_product": "whatsapp",
            "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
            "messages": [{"id": "wamid.test123"}]
        }
        yield mock_instance

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "documentation" in response.json()

@pytest.mark.asyncio
async def test_send_message_success(mock_db_session, mock_whatsapp_service):
    """Test successful message sending"""
    with patch("app.routes.whatsapp.get_db", return_value=mock_db_session):
        with patch("app.routes.whatsapp.get_whatsapp_service", return_value=mock_whatsapp_service):
            response = client.get("/api/v1/whatsapp/send_message?phone_number=+1234567890")
            
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "Message sent successfully" in response.json()["message"]
            assert response.json()["message_id"] == "wamid.test123"

@pytest.mark.asyncio
async def test_send_message_invalid_phone(mock_db_session, mock_whatsapp_service):
    """Test sending message with invalid phone number"""
    with patch("app.routes.whatsapp.get_db", return_value=mock_db_session):
        with patch("app.routes.whatsapp.get_whatsapp_service", return_value=mock_whatsapp_service):
            with patch("app.routes.whatsapp.MessageRequest") as mock_request:
                mock_request.return_value.phone_number = "invalid"
                mock_request.return_value.validate_phone_number.side_effect = ValueError("Invalid phone number")
                
                response = client.get("/api/v1/whatsapp/send_message?phone_number=invalid")
                
                assert response.status_code == 400
                assert response.json()["success"] is False
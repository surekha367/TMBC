import pytest
import httpx
from unittest.mock import patch, MagicMock
from app.services.whatsapp_service import WhatsAppService
from app.exceptions import WhatsAppAPIException, ConfigurationException

@pytest.fixture
def mock_settings():
    with patch("app.services.whatsapp_service.settings") as mock:
        mock.whatsapp_api_url = "https://test-api.com"
        mock.whatsapp_phone_number_id = "12345"
        mock.whatsapp_access_token = "test-token"
        yield mock

@pytest.fixture
def mock_httpx_client():
    with patch("httpx.AsyncClient") as mock:
        mock_instance = MagicMock()
        mock.return_value.__aenter__.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def whatsapp_service(mock_settings):
    return WhatsAppService()

@pytest.mark.asyncio
async def test_send_message_success(whatsapp_service, mock_httpx_client):
    """Test successful message sending"""
    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "messaging_product": "whatsapp",
        "contacts": [{"input": "+1234567890", "wa_id": "1234567890"}],
        "messages": [{"id": "wamid.test123"}]
    }
    mock_httpx_client.post.return_value = mock_response
    
    # Mock the database
    mock_db = MagicMock()
    
    # Call the method
    result = await whatsapp_service.send_message(mock_db, "+1234567890")
    
    # Assert results
    assert result["messaging_product"] == "whatsapp"
    assert "contacts" in result
    assert "messages" in result
    assert result["messages"][0]["id"] == "wamid.test123"
    
    # Verify database operations
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called()

@pytest.mark.asyncio
async def test_send_message_api_error(whatsapp_service, mock_httpx_client):
    """Test WhatsApp API error handling"""
    # Mock the error response
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_httpx_client.post.return_value = mock_response
    
    # Mock the database
    mock_db = MagicMock()
    
    # Call the method and expect exception
    with pytest.raises(WhatsAppAPIException) as exc_info:
        await whatsapp_service.send_message(mock_db, "+1234567890")
    
    assert "WhatsApp API error" in str(exc_info.value)
    
    # Verify database operations (status should be updated to failed)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called()

@pytest.mark.asyncio
async def test_send_message_network_error(whatsapp_service, mock_httpx_client):
    """Test network error handling"""
    # Mock the network error
    mock_httpx_client.post.side_effect = httpx.RequestError("Connection error", request=MagicMock())
    
    # Mock the database
    mock_db = MagicMock()
    
    # Call the method and expect exception
    with pytest.raises(WhatsAppAPIException) as exc_info:
        await whatsapp_service.send_message(mock_db, "+1234567890")
    
    assert "Error sending WhatsApp message" in str(exc_info.value)
    
    # Verify database operations (status should be updated to failed)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called()

def test_missing_configuration():
    """Test configuration validation"""
    # Mock settings with missing credentials
    with patch("app.services.whatsapp_service.settings") as mock_settings:
        mock_settings.whatsapp_api_url = "https://test-api.com"
        mock_settings.whatsapp_phone_number_id = ""  # Empty phone number ID
        mock_settings.whatsapp_access_token = "test-token"
        
        # Expect ConfigurationException
        with pytest.raises(ConfigurationException) as exc_info:
            WhatsAppService()
        
        assert "WhatsApp API credentials not configured" in str(exc_info.value)
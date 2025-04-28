# TMBC WhatsApp Messaging API

A FastAPI application that integrates with Meta's WhatsApp Business Manager API to send messages. This project is built as part of the technical challenge for The Madras Branding Company.

## Features

- 🚀 FastAPI endpoint to send WhatsApp messages
- ✅ GET and POST endpoints for flexibility
- 📱 Phone number validation and formatting
- 📊 Message logging to PostgreSQL database
- 🛡️ Comprehensive error handling and responses
- 📝 Complete API documentation with Swagger UI
- 🧪 Unit tests with pytest

## Tech Stack

- **Python 3.11+**: Modern Python features
- **FastAPI**: High-performance web framework
- **PostgreSQL**: Relational database for message logging
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and settings management
- **Httpx**: Asynchronous HTTP client
- **pytest**: Testing framework

## Project Structure

```
TMBC/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── exceptions.py        # Custom exceptions
│   ├── dependencies.py      # FastAPI dependencies
│   ├── utils.py             # Utility functions
│   ├── routes/              # API routes
│   │   ├── __init__.py
│   │   └── whatsapp.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── whatsapp_service.py
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_services.py
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore
├── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL
- WhatsApp Business API credentials (Phone Number ID and Access Token)

### Installation

#### Option 1: Local Development

1. Clone this repository:
   ```bash
   git clone https://github.com/surekha367/TMBC.git
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

6. Edit the `.env` file and add your WhatsApp Business API credentials and database settings.

7. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Running Tests

```bash
pytest
```

## API Usage

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

### Send a WhatsApp Message (GET)

```
GET /api/v1/whatsapp/send_message?phone_number=+1234567890
```

### Send a WhatsApp Message (POST)

```
POST /api/v1/whatsapp/send_message
Content-Type: application/json

{
  "phone_number": "+1234567890"
}
```

### Check Message Logs

```
GET /api/v1/whatsapp/logs?limit=10&skip=0
```

## Response Format

```json
{
  "success": true,
  "message": "Message sent successfully to +1234567890",
  "message_id": "wamid.abcdefghijklmnop",
  "details": {
    "messaging_product": "whatsapp",
    "contacts": [
      {
        "input": "+1234567890",
        "wa_id": "1234567890"
      }
    ],
    "messages": [
      {
        "id": "wamid.abcdefghijklmnop"
      }
    ]
  }
}
```

## WhatsApp Business API Setup

To use this API with the WhatsApp Business API:

1. Create a Meta for Developers account
2. Register an app in the Meta for Developers portal
3. Set up a WhatsApp Business account
4. Complete the WhatsApp Business API verification process
5. Get your Phone Number ID and Access Token

## Notes on Security

- In a production environment, limit CORS origins to specific domains
- Use a proper secrets management system for API credentials
- Implement rate limiting to prevent abuse
- Add authentication to protect the API endpoints

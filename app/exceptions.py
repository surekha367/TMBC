from fastapi import HTTPException, status

class WhatsAppAPIException(HTTPException):
    """
    Exception raised when there is an error with the WhatsApp API
    """
    def __init__(self, detail: str = "WhatsApp API error occurred"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail
        )

class InvalidPhoneNumberException(HTTPException):
    """
    Exception raised when phone number validation fails
    """
    def __init__(self, detail: str = "Invalid phone number format"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class ConfigurationException(HTTPException):
    """
    Exception raised when there's a configuration error
    """
    def __init__(self, detail: str = "API configuration error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class DatabaseException(HTTPException):
    """
    Exception raised when there's a database error
    """
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
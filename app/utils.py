import re
import json
import phonenumbers
from app.exceptions import InvalidPhoneNumberException

def validate_phone_number(phone_number: str) -> str:
    """
    Validates and formats the phone number to E.164 format
    
    Args:
        phone_number: Phone number to validate
        
    Returns:
        Formatted phone number string in E.164 format
        
    Raises:
        InvalidPhoneNumberException: If the phone number is invalid
    """
    # Remove any whitespace or special characters
    cleaned_number = re.sub(r'[\s\-\(\)]', '', phone_number)
    
    # If number doesn't start with +, assume it's missing country code and add +
    if not cleaned_number.startswith('+'):
        cleaned_number = '+' + cleaned_number
    
    try:
        # Parse phone number and check if it's valid
        parsed_number = phonenumbers.parse(cleaned_number)
        if not phonenumbers.is_valid_number(parsed_number):
            raise InvalidPhoneNumberException(f"Phone number {phone_number} is not valid")
        
        # Format to E.164 format for WhatsApp API
        formatted_number = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
        
        return formatted_number
    except phonenumbers.phonenumberutil.NumberParseException:
        raise InvalidPhoneNumberException(f"Could not parse phone number {phone_number}")

def dict_to_json_string(data: dict) -> str:
    """
    Convert dictionary to JSON string for database storage
    """
    if data is None:
        return None
    return json.dumps(data)

def json_string_to_dict(json_str: str) -> dict:
    """
    Convert JSON string from database to dictionary
    """
    if not json_str:
        return {}
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return {}
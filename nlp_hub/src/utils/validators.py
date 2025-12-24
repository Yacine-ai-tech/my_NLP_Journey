"""Input validators for NLP Hub."""

from typing import List
from .exceptions import ValidationError


SUPPORTED_LANGUAGES = ["en", "fr", "ha", "es", "de", "it", "pt"]
MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 10000


def validate_text(text: str, min_length: int = MIN_TEXT_LENGTH, max_length: int = MAX_TEXT_LENGTH) -> str:
    """
    Validate and clean text input.
    
    Args:
        text: Text to validate
        min_length: Minimum text length
        max_length: Maximum text length
    
    Returns:
        Cleaned text
    
    Raises:
        ValidationError: If text is invalid
    """
    if not isinstance(text, str):
        raise ValidationError("Text must be a string")
    
    text = text.strip()
    
    if len(text) < min_length:
        raise ValidationError(f"Text must be at least {min_length} character(s)")
    
    if len(text) > max_length:
        raise ValidationError(f"Text must not exceed {max_length} characters")
    
    return text


def validate_language_code(language_code: str, supported_languages: List[str] = None) -> str:
    """
    Validate language code.
    
    Args:
        language_code: Language code to validate
        supported_languages: List of supported language codes
    
    Returns:
        Validated language code
    
    Raises:
        ValidationError: If language code is invalid
    """
    if supported_languages is None:
        supported_languages = SUPPORTED_LANGUAGES
    
    language_code = language_code.lower().strip()
    
    if language_code not in supported_languages:
        raise ValidationError(
            f"Unsupported language: {language_code}. "
            f"Supported languages: {', '.join(supported_languages)}"
        )
    
    return language_code


def validate_confidence_score(score: float) -> float:
    """
    Validate confidence score is between 0 and 1.
    
    Args:
        score: Confidence score
    
    Returns:
        Validated score
    
    Raises:
        ValidationError: If score is invalid
    """
    if not isinstance(score, (int, float)):
        raise ValidationError("Confidence score must be a number")
    
    if not 0 <= score <= 1:
        raise ValidationError("Confidence score must be between 0 and 1")
    
    return float(score)


def validate_non_empty_list(items: list, item_name: str = "items") -> list:
    """
    Validate list is not empty.
    
    Args:
        items: List to validate
        item_name: Name of items for error message
    
    Returns:
        Validated list
    
    Raises:
        ValidationError: If list is empty
    """
    if not isinstance(items, list):
        raise ValidationError(f"{item_name} must be a list")
    
    if not items:
        raise ValidationError(f"{item_name} cannot be empty")
    
    return items

"""Preprocessing module for text cleaning and normalization."""

import re
from typing import List
from ..utils.logger import get_logger


logger = get_logger(__name__)


class TextPreprocessor:
    """Text preprocessing utilities."""
    
    @staticmethod
    def lowercase(text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()
    
    @staticmethod
    def remove_special_characters(text: str, keep_spaces: bool = True) -> str:
        """Remove special characters."""
        if keep_spaces:
            text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        else:
            text = re.sub(r"[^a-zA-Z0-9]", "", text)
        return text
    
    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """Remove extra whitespace."""
        return " ".join(text.split())
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        return re.sub(url_pattern, "", text)
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove email addresses."""
        email_pattern = r"\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
        return re.sub(email_pattern, "", text)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace."""
        return re.sub(r"\s+", " ", text).strip()
    
    @classmethod
    def preprocess(
        cls,
        text: str,
        lowercase: bool = True,
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_special_chars: bool = False,
        normalize_whitespace: bool = True,
    ) -> str:
        """
        Apply multiple preprocessing steps.
        
        Args:
            text: Text to preprocess
            lowercase: Convert to lowercase
            remove_urls: Remove URLs
            remove_emails: Remove email addresses
            remove_special_chars: Remove special characters
            normalize_whitespace: Normalize whitespace
        
        Returns:
            Preprocessed text
        """
        if lowercase:
            text = cls.lowercase(text)
        
        if remove_urls:
            text = cls.remove_urls(text)
        
        if remove_emails:
            text = cls.remove_emails(text)
        
        if remove_special_chars:
            text = cls.remove_special_characters(text)
        
        if normalize_whitespace:
            text = cls.normalize_whitespace(text)
        
        return text

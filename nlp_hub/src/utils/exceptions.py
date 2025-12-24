"""Custom exceptions for NLP Hub."""


class NLPHubException(Exception):
    """Base exception for NLP Hub."""
    pass


class ModelNotFoundError(NLPHubException):
    """Raised when a required model is not found."""
    pass


class ConfigurationError(NLPHubException):
    """Raised when configuration is invalid or missing."""
    pass


class ValidationError(NLPHubException):
    """Raised when input validation fails."""
    pass


class ProcessingError(NLPHubException):
    """Raised when text processing fails."""
    pass


class IntegrationError(NLPHubException):
    """Raised when external service integration fails."""
    pass


class RAGError(NLPHubException):
    """Raised when RAG operations fail."""
    pass


class TranslationError(NLPHubException):
    """Raised when translation operations fail."""
    pass


class SpeechError(NLPHubException):
    """Raised when speech processing fails."""
    pass


class LLMError(NLPHubException):
    """Raised when LLM operations fail."""
    pass


class ChatbotError(NLPHubException):
    """Raised when chatbot operations fail."""
    pass

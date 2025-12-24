"""
NLP Hub - Comprehensive NLP Pipeline
Main package for chatbot, intent recognition, entity extraction, RAG, speech, LLM, and translation.
"""

__version__ = "1.0.0"
__author__ = "NLP Hub Team"
__description__ = "Production-ready NLP Hub with multi-language support"

from .config.settings import settings
from .chatbot.manager import ChatbotManager
from .intent.classifier import IntentClassifier
from .entity.extractor import EntityExtractor
from .rag.retriever import RAGRetriever
from .speech.processor import SpeechProcessor
from .llm.manager import LLMManager
from .translation.translator import Translator

__all__ = [
    "settings",
    "ChatbotManager",
    "IntentClassifier",
    "EntityExtractor",
    "RAGRetriever",
    "SpeechProcessor",
    "LLMManager",
    "Translator",
]

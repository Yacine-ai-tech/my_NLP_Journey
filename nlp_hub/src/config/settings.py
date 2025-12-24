"""
Global configuration and settings for NLP Hub.
Supports environment-based configuration for development, staging, and production.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Database configuration."""
    type: str = "postgres"
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", 5432))
    username: str = os.getenv("DB_USER", "admin")
    password: str = os.getenv("DB_PASSWORD", "")
    database: str = os.getenv("DB_NAME", "nlp_hub")
    pool_size: int = 10
    max_overflow: int = 20


@dataclass
class LLMConfig:
    """LLM configuration."""
    provider: str = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, local
    model_name: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    api_key: str = os.getenv("LLM_API_KEY", "")
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    timeout: int = 30


@dataclass
class TranslationConfig:
    """Translation configuration."""
    models_path: str = os.getenv("TRANSLATION_MODELS_PATH", "models/translation")
    supported_languages: List[str] = field(default_factory=lambda: ["en", "fr", "ha"])
    default_source: str = "en"
    default_target: str = "fr"
    batch_size: int = 32
    use_gpu: bool = os.getenv("USE_GPU", "true").lower() == "true"


@dataclass
class RAGConfig:
    """RAG (Retrieval Augmented Generation) configuration."""
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    vector_db_type: str = os.getenv("VECTOR_DB", "faiss")  # faiss, pinecone, weaviate
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "data/embeddings/vectors")
    chunk_size: int = 256
    chunk_overlap: int = 50
    top_k: int = 5
    similarity_threshold: float = 0.5


@dataclass
class SpeechConfig:
    """Speech processing configuration."""
    provider: str = os.getenv("SPEECH_PROVIDER", "google")  # google, azure, local
    sample_rate: int = 16000
    chunk_duration_ms: int = 1024
    language: str = "en-US"
    max_duration: int = 300  # 5 minutes


@dataclass
class IntentConfig:
    """Intent classification configuration."""
    model_type: str = os.getenv("INTENT_MODEL", "transformer")  # transformer, bert, distilbert
    model_name: str = os.getenv("INTENT_MODEL_NAME", "distilbert-base-uncased")
    num_labels: int = 10
    confidence_threshold: float = 0.5
    batch_size: int = 32


@dataclass
class EntityConfig:
    """Entity extraction configuration."""
    model_type: str = os.getenv("ENTITY_MODEL", "transformer")  # transformer, spacy
    model_name: str = os.getenv("ENTITY_MODEL_NAME", "distilbert-base-uncased")
    entity_types: List[str] = field(default_factory=lambda: [
        "PERSON", "ORG", "GPE", "DATE", "TIME", "MONEY", "QUANTITY", "LOCATION"
    ])
    confidence_threshold: float = 0.5


@dataclass
class ChatbotConfig:
    """Chatbot configuration."""
    max_history: int = 10
    context_window: int = 5
    response_timeout: int = 30
    enable_logging: bool = True
    personality: str = "professional"  # professional, friendly, formal


@dataclass
class Settings:
    """Global application settings."""
    # Environment
    env: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Paths
    project_root: Path = Path(__file__).parent.parent.parent
    data_dir: Path = project_root / "data"
    models_dir: Path = project_root / "models"
    logs_dir: Path = project_root / "logs"
    
    # API
    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("API_PORT", 8000))
    api_workers: int = int(os.getenv("API_WORKERS", 4))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = "json"  # json or text
    
    # Feature flags
    enable_rag: bool = True
    enable_speech: bool = True
    enable_translation: bool = True
    enable_intent_recognition: bool = True
    enable_entity_extraction: bool = True
    
    # Sub-configurations
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    translation: TranslationConfig = field(default_factory=TranslationConfig)
    rag: RAGConfig = field(default_factory=RAGConfig)
    speech: SpeechConfig = field(default_factory=SpeechConfig)
    intent: IntentConfig = field(default_factory=IntentConfig)
    entity: EntityConfig = field(default_factory=EntityConfig)
    chatbot: ChatbotConfig = field(default_factory=ChatbotConfig)
    
    # Security
    cors_origins: List[str] = field(default_factory=lambda: ["http://localhost:3000"])
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    def __post_init__(self):
        """Create necessary directories."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

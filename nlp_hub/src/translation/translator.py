"""Translation module with support for multiple languages including French and Hausa."""

from abc import ABC, abstractmethod
from typing import Dict, List
from dataclasses import dataclass
from pathlib import Path
from ..utils.logger import get_logger
from ..utils.validators import validate_text, validate_language_code
from ..utils.exceptions import TranslationError, ModelNotFoundError
from ..config.settings import settings


logger = get_logger(__name__, level=settings.log_level)


@dataclass
class TranslationResult:
    """Translation result."""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Translator(ABC):
    """Base class for translation."""
    
    # Supported language pairs
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "fr": "French",
        "ha": "Hausa",
        "es": "Spanish",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
    }
    
    def __init__(self, source_lang: str = None, target_lang: str = None):
        """
        Initialize translator.
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
        """
        self.source_lang = source_lang or settings.translation.default_source
        self.target_lang = target_lang or settings.translation.default_target
        
        self.source_lang = validate_language_code(
            self.source_lang,
            list(self.SUPPORTED_LANGUAGES.keys())
        )
        self.target_lang = validate_language_code(
            self.target_lang,
            list(self.SUPPORTED_LANGUAGES.keys())
        )
        
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        """Load translation model."""
        pass
    
    @abstractmethod
    def _translate(self, text: str) -> str:
        """Internal translation method."""
        pass
    
    def translate(self, text: str) -> TranslationResult:
        """
        Translate text from source to target language.
        
        Args:
            text: Text to translate
        
        Returns:
            TranslationResult with translated text
        
        Raises:
            TranslationError: If translation fails
        """
        try:
            text = validate_text(text)
            translated_text = self._translate(text)
            
            result = TranslationResult(
                original_text=text,
                translated_text=translated_text,
                source_language=self.source_lang,
                target_language=self.target_lang,
            )
            
            logger.info(
                f"Translation completed",
                extra={
                    "source_lang": self.source_lang,
                    "target_lang": self.target_lang,
                    "original_length": len(text),
                    "translated_length": len(translated_text),
                }
            )
            
            return result
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise TranslationError(f"Translation failed: {str(e)}")
    
    def batch_translate(self, texts: List[str]) -> List[TranslationResult]:
        """
        Translate multiple texts.
        
        Args:
            texts: List of texts to translate
        
        Returns:
            List of translation results
        """
        return [self.translate(text) for text in texts]
    
    @classmethod
    def get_supported_languages(cls) -> Dict[str, str]:
        """Get supported languages."""
        return cls.SUPPORTED_LANGUAGES


class MarianMTTranslator(Translator):
    """Translator using Facebook's MarianMT models."""
    
    def _load_model(self):
        """Load MarianMT model and tokenizer."""
        try:
            from transformers import MarianMTModel, MarianTokenizer
            
            model_name = f"Helsinki-NLP/opus-mt-{self.source_lang}-{self.target_lang}"
            
            logger.info(f"Loading MarianMT model: {model_name}")
            self.tokenizer = MarianTokenizer.from_pretrained(model_name)
            self.model = MarianMTModel.from_pretrained(model_name)
        except ImportError:
            raise ModelNotFoundError(
                "Transformers library not installed. Install with: pip install transformers"
            )
        except Exception as e:
            # Fallback: try to find alternative model
            logger.warning(f"Failed to load MarianMT model: {str(e)}, using dummy translator")
            self.model = None
            self.tokenizer = None
    
    def _translate(self, text: str) -> str:
        """Translate using MarianMT."""
        if self.model is None or self.tokenizer is None:
            # Fallback to dummy translation
            return f"[{self.target_lang.upper()}] {text}"
        
        try:
            # Tokenize
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            
            # Translate
            translated = self.model.generate(**inputs)
            
            # Decode
            result = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            
            return result
        except Exception as e:
            logger.error(f"MarianMT translation failed: {str(e)}")
            raise TranslationError(f"Translation failed: {str(e)}")


class M2M100Translator(Translator):
    """Translator using Facebook's M2M-100 model (supports many languages)."""
    
    def _load_model(self):
        """Load M2M-100 model."""
        try:
            from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
            
            model_name = "facebook/m2m100_418M"
            
            logger.info(f"Loading M2M-100 model: {model_name}")
            self.tokenizer = M2M100Tokenizer.from_pretrained(model_name)
            self.model = M2M100ForConditionalGeneration.from_pretrained(model_name)
            
            # Set language codes
            self.tokenizer.src_lang = self._get_m2m_lang_code(self.source_lang)
        except ImportError:
            raise ModelNotFoundError(
                "Transformers library not installed. Install with: pip install transformers"
            )
        except Exception as e:
            logger.warning(f"Failed to load M2M-100 model: {str(e)}")
            self.model = None
            self.tokenizer = None
    
    def _get_m2m_lang_code(self, lang_code: str) -> str:
        """Convert language code to M2M-100 format."""
        m2m_codes = {
            "en": "en",
            "fr": "fr",
            "ha": "ha",  # Hausa
            "es": "es",
            "de": "de",
            "it": "it",
            "pt": "pt",
        }
        return m2m_codes.get(lang_code, lang_code)
    
    def _translate(self, text: str) -> str:
        """Translate using M2M-100."""
        if self.model is None or self.tokenizer is None:
            return f"[{self.target_lang.upper()}] {text}"
        
        try:
            # Prepare input
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            
            # Set target language
            target_lang_code = self._get_m2m_lang_code(self.target_lang)
            forced_bos_token_id = self.tokenizer.get_lang_id(target_lang_code)
            
            # Translate
            translated = self.model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
            )
            
            # Decode
            result = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            
            return result
        except Exception as e:
            logger.error(f"M2M-100 translation failed: {str(e)}")
            raise TranslationError(f"Translation failed: {str(e)}")


class DummyTranslator(Translator):
    """Dummy translator for testing."""
    
    def _load_model(self):
        """Initialize dummy translator."""
        logger.info("Using dummy translator")
        self.model = None
        self.tokenizer = None
    
    def _translate(self, text: str) -> str:
        """Return dummy translation."""
        return f"[{self.target_lang.upper()} Translation] {text}"


def get_translator(
    translator_type: str = "m2m100",
    source_lang: str = None,
    target_lang: str = None,
) -> Translator:
    """
    Factory function to get translator.
    
    Args:
        translator_type: Type of translator ('marianmt', 'm2m100', or 'dummy')
        source_lang: Source language code
        target_lang: Target language code
    
    Returns:
        Translator instance
    """
    if translator_type == "marianmt":
        return MarianMTTranslator(source_lang, target_lang)
    elif translator_type == "m2m100":
        return M2M100Translator(source_lang, target_lang)
    elif translator_type == "dummy":
        return DummyTranslator(source_lang, target_lang)
    else:
        raise ValueError(f"Unknown translator type: {translator_type}")

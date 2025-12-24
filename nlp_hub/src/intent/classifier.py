"""Intent classification module."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from dataclasses import dataclass
from ..utils.logger import get_logger
from ..utils.validators import validate_text, validate_confidence_score
from ..utils.exceptions import ProcessingError, ModelNotFoundError
from ..config.settings import settings


logger = get_logger(__name__, level=settings.log_level)


@dataclass
class Intent:
    """Intent prediction result."""
    name: str
    confidence: float
    metadata: Dict = None
    
    def __post_init__(self):
        """Validate intent data."""
        validate_confidence_score(self.confidence)
        if self.metadata is None:
            self.metadata = {}


class IntentClassifier(ABC):
    """Base class for intent classification."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize intent classifier.
        
        Args:
            model_name: Name of the model to use
        """
        self.model_name = model_name or settings.intent.model_name
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        """Load the classification model."""
        pass
    
    @abstractmethod
    def _predict(self, text: str) -> Intent:
        """Internal prediction method."""
        pass
    
    def classify(self, text: str) -> Intent:
        """
        Classify intent of the given text.
        
        Args:
            text: Input text
        
        Returns:
            Intent prediction result
        
        Raises:
            ProcessingError: If classification fails
        """
        try:
            text = validate_text(text)
            intent = self._predict(text)
            
            logger.info(
                f"Intent classification result",
                extra={
                    "text_length": len(text),
                    "intent": intent.name,
                    "confidence": intent.confidence,
                }
            )
            
            return intent
        except Exception as e:
            logger.error(f"Intent classification failed: {str(e)}")
            raise ProcessingError(f"Intent classification failed: {str(e)}")
    
    def batch_classify(self, texts: List[str]) -> List[Intent]:
        """
        Classify intents for multiple texts.
        
        Args:
            texts: List of input texts
        
        Returns:
            List of intent predictions
        """
        return [self.classify(text) for text in texts]
    
    def get_supported_intents(self) -> List[str]:
        """
        Get list of supported intent labels.
        
        Returns:
            List of intent names
        """
        # Override in subclass
        return []


class TransformerIntentClassifier(IntentClassifier):
    """Intent classifier using Hugging Face transformers."""
    
    def _load_model(self):
        """Load transformer model and tokenizer."""
        try:
            from transformers import pipeline
            
            logger.info(f"Loading transformer model: {self.model_name}")
            self.model = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=0 if settings.translation.use_gpu else -1,
            )
        except ImportError:
            raise ModelNotFoundError(
                "Transformers library not installed. Install with: pip install transformers"
            )
        except Exception as e:
            raise ModelNotFoundError(f"Failed to load model {self.model_name}: {str(e)}")
    
    def _predict(self, text: str) -> Intent:
        """Predict intent using zero-shot classification."""
        candidate_labels = settings.intent.entity_types or [
            "greeting",
            "question",
            "request",
            "statement",
            "command",
        ]
        
        result = self.model(text, candidate_labels)
        
        intent = Intent(
            name=result["labels"][0],
            confidence=result["scores"][0],
            metadata={
                "all_scores": dict(zip(result["labels"], result["scores"])),
            },
        )
        
        return intent


class DummyIntentClassifier(IntentClassifier):
    """Dummy intent classifier for testing/development."""
    
    def _load_model(self):
        """Initialize dummy model."""
        logger.info("Using dummy intent classifier")
        self.model = None
    
    def _predict(self, text: str) -> Intent:
        """Return dummy prediction based on keywords."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["hello", "hi", "hey", "greetings"]):
            return Intent("greeting", 0.95)
        elif any(word in text_lower for word in ["what", "when", "where", "how", "why", "?"]):
            return Intent("question", 0.90)
        elif any(word in text_lower for word in ["please", "can", "could", "would"]):
            return Intent("request", 0.85)
        else:
            return Intent("statement", 0.75)


def get_intent_classifier(classifier_type: str = "transformer") -> IntentClassifier:
    """
    Factory function to get intent classifier.
    
    Args:
        classifier_type: Type of classifier ('transformer' or 'dummy')
    
    Returns:
        IntentClassifier instance
    """
    if classifier_type == "transformer":
        return TransformerIntentClassifier()
    elif classifier_type == "dummy":
        return DummyIntentClassifier()
    else:
        raise ValueError(f"Unknown classifier type: {classifier_type}")

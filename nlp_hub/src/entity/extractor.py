"""Entity extraction and Named Entity Recognition (NER) module."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from dataclasses import dataclass
from ..utils.logger import get_logger
from ..utils.validators import validate_text
from ..utils.exceptions import ProcessingError, ModelNotFoundError
from ..config.settings import settings


logger = get_logger(__name__, level=settings.log_level)


@dataclass
class Entity:
    """Extracted entity."""
    text: str
    label: str
    start: int
    end: int
    confidence: float = 1.0


@dataclass
class ExtractionResult:
    """Entity extraction result."""
    text: str
    entities: List[Entity]
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class EntityExtractor(ABC):
    """Base class for entity extraction."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize entity extractor.
        
        Args:
            model_name: Name of the model to use
        """
        self.model_name = model_name or settings.entity.model_name
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        """Load the extraction model."""
        pass
    
    @abstractmethod
    def _extract(self, text: str) -> ExtractionResult:
        """Internal extraction method."""
        pass
    
    def extract(self, text: str) -> ExtractionResult:
        """
        Extract entities from text.
        
        Args:
            text: Input text
        
        Returns:
            Extraction result with entities
        
        Raises:
            ProcessingError: If extraction fails
        """
        try:
            text = validate_text(text)
            result = self._extract(text)
            
            logger.info(
                f"Entity extraction completed",
                extra={
                    "text_length": len(text),
                    "num_entities": len(result.entities),
                    "entity_types": list(set(e.label for e in result.entities)),
                }
            )
            
            return result
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            raise ProcessingError(f"Entity extraction failed: {str(e)}")
    
    def batch_extract(self, texts: List[str]) -> List[ExtractionResult]:
        """
        Extract entities from multiple texts.
        
        Args:
            texts: List of input texts
        
        Returns:
            List of extraction results
        """
        return [self.extract(text) for text in texts]


class TransformerEntityExtractor(EntityExtractor):
    """Entity extractor using Hugging Face transformers."""
    
    def _load_model(self):
        """Load transformer model and tokenizer."""
        try:
            from transformers import pipeline
            
            logger.info(f"Loading transformer NER model: {self.model_name}")
            self.model = pipeline(
                "ner",
                model=self.model_name,
                aggregation_strategy="simple",
                device=0 if settings.translation.use_gpu else -1,
            )
        except ImportError:
            raise ModelNotFoundError(
                "Transformers library not installed. Install with: pip install transformers"
            )
        except Exception as e:
            raise ModelNotFoundError(f"Failed to load model {self.model_name}: {str(e)}")
    
    def _extract(self, text: str) -> ExtractionResult:
        """Extract entities using transformer model."""
        entities = []
        
        if not self.model:
            return ExtractionResult(text, entities)
        
        predictions = self.model(text)
        
        for pred in predictions:
            # Filter by confidence threshold
            if pred.get("score", 0) >= settings.entity.confidence_threshold:
                entities.append(
                    Entity(
                        text=pred["word"].strip(),
                        label=pred["entity_group"],
                        start=pred.get("start", 0),
                        end=pred.get("end", 0),
                        confidence=pred.get("score", 1.0),
                    )
                )
        
        return ExtractionResult(text, entities)


class DummyEntityExtractor(EntityExtractor):
    """Dummy entity extractor for testing/development."""
    
    def _load_model(self):
        """Initialize dummy model."""
        logger.info("Using dummy entity extractor")
        self.model = None
    
    def _extract(self, text: str) -> ExtractionResult:
        """Extract entities using simple pattern matching."""
        entities = []
        
        # Simple keyword-based extraction
        keywords = {
            "PERSON": ["john", "mary", "bob", "alice"],
            "ORG": ["company", "corporation", "microsoft", "apple"],
            "GPE": ["new york", "london", "paris", "tokyo"],
        }
        
        for label, words in keywords.items():
            for word in words:
                if word.lower() in text.lower():
                    start = text.lower().find(word.lower())
                    entities.append(
                        Entity(
                            text=word,
                            label=label,
                            start=start,
                            end=start + len(word),
                            confidence=0.8,
                        )
                    )
        
        return ExtractionResult(text, entities)


def get_entity_extractor(extractor_type: str = "transformer") -> EntityExtractor:
    """
    Factory function to get entity extractor.
    
    Args:
        extractor_type: Type of extractor ('transformer' or 'dummy')
    
    Returns:
        EntityExtractor instance
    """
    if extractor_type == "transformer":
        return TransformerEntityExtractor()
    elif extractor_type == "dummy":
        return DummyEntityExtractor()
    else:
        raise ValueError(f"Unknown extractor type: {extractor_type}")

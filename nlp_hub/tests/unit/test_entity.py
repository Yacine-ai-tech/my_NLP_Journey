"""Unit tests for entity extraction."""

import pytest
from src.entity import Entity, ExtractionResult, get_entity_extractor


class TestEntity:
    """Test Entity dataclass."""
    
    def test_entity_creation(self):
        """Test creating an entity."""
        entity = Entity(
            text="John",
            label="PERSON",
            start=0,
            end=4,
            confidence=0.95
        )
        assert entity.text == "John"
        assert entity.label == "PERSON"
        assert entity.confidence == 0.95


class TestDummyEntityExtractor:
    """Test dummy entity extractor."""
    
    def test_extract_entities(self):
        """Test extracting entities."""
        extractor = get_entity_extractor("dummy")
        result = extractor.extract("John works at Microsoft")
        assert len(result.entities) > 0
        assert any(e.label == "PERSON" for e in result.entities)
    
    def test_batch_extract(self):
        """Test batch extraction."""
        extractor = get_entity_extractor("dummy")
        texts = [
            "John works at Microsoft",
            "Mary is in New York"
        ]
        results = extractor.batch_extract(texts)
        assert len(results) == 2
        assert all(isinstance(r, ExtractionResult) for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

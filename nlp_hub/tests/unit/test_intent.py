"""Unit tests for intent classification."""

import pytest
from src.intent import Intent, get_intent_classifier


class TestIntent:
    """Test Intent dataclass."""
    
    def test_intent_creation(self):
        """Test creating an intent."""
        intent = Intent(name="greeting", confidence=0.95)
        assert intent.name == "greeting"
        assert intent.confidence == 0.95
        assert intent.metadata == {}
    
    def test_intent_with_metadata(self):
        """Test intent with metadata."""
        intent = Intent(
            name="question",
            confidence=0.88,
            metadata={"question_type": "open"}
        )
        assert intent.metadata["question_type"] == "open"


class TestDummyIntentClassifier:
    """Test dummy intent classifier."""
    
    def test_classify_greeting(self):
        """Test classifying greeting."""
        classifier = get_intent_classifier("dummy")
        intent = classifier.classify("Hello!")
        assert intent.name == "greeting"
        assert intent.confidence > 0.8
    
    def test_classify_question(self):
        """Test classifying question."""
        classifier = get_intent_classifier("dummy")
        intent = classifier.classify("What is this?")
        assert intent.name == "question"
    
    def test_batch_classify(self):
        """Test batch classification."""
        classifier = get_intent_classifier("dummy")
        texts = ["Hello", "What?", "Please help"]
        results = classifier.batch_classify(texts)
        assert len(results) == 3
        assert all(isinstance(r, Intent) for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

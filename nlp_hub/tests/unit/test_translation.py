"""Unit tests for translation."""

import pytest
from src.translation import get_translator, TranslationResult


class TestDummyTranslator:
    """Test dummy translator."""
    
    def test_english_to_french(self):
        """Test English to French translation."""
        translator = get_translator(
            translator_type="dummy",
            source_lang="en",
            target_lang="fr"
        )
        result = translator.translate("Hello")
        assert isinstance(result, TranslationResult)
        assert result.source_language == "en"
        assert result.target_language == "fr"
    
    def test_english_to_hausa(self):
        """Test English to Hausa translation."""
        translator = get_translator(
            translator_type="dummy",
            source_lang="en",
            target_lang="ha"
        )
        result = translator.translate("Good morning")
        assert isinstance(result, TranslationResult)
        assert result.source_language == "en"
        assert result.target_language == "ha"
    
    def test_batch_translate(self):
        """Test batch translation."""
        translator = get_translator(
            translator_type="dummy",
            source_lang="en",
            target_lang="fr"
        )
        texts = ["Hello", "Good bye", "How are you?"]
        results = translator.batch_translate(texts)
        assert len(results) == 3
        assert all(isinstance(r, TranslationResult) for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

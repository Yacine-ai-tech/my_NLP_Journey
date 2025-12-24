"""Example script showing how to use different NLP Hub components."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from intent import get_intent_classifier
from entity import get_entity_extractor
from translation import get_translator
from preprocessing import TextPreprocessor


def example_intent_classification():
    """Example: Intent classification."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Intent Classification")
    print("=" * 60)
    
    classifier = get_intent_classifier("dummy")
    
    test_sentences = [
        "Hello, how are you?",
        "What is the weather today?",
        "Please help me with this issue",
    ]
    
    for sentence in test_sentences:
        intent = classifier.classify(sentence)
        print(f"\nText: {sentence}")
        print(f"Intent: {intent.name} (confidence: {intent.confidence:.2f})")


def example_entity_extraction():
    """Example: Entity extraction."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Entity Extraction")
    print("=" * 60)
    
    extractor = get_entity_extractor("dummy")
    
    test_text = "John Smith works at Microsoft in Seattle. He was born on January 15, 1990."
    print(f"\nText: {test_text}")
    
    result = extractor.extract(test_text)
    print(f"\nExtracted Entities:")
    for entity in result.entities:
        print(f"  {entity.label}: {entity.text}")


def example_translation():
    """Example: Translation."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Translation")
    print("=" * 60)
    
    # English to French
    print("\n[English → French]")
    translator_en_fr = get_translator(
        translator_type="dummy",
        source_lang="en",
        target_lang="fr"
    )
    
    text_en = "Good morning! How are you?"
    result = translator_en_fr.translate(text_en)
    print(f"English: {result.original_text}")
    print(f"French: {result.translated_text}")
    
    # English to Hausa
    print("\n[English → Hausa]")
    translator_en_ha = get_translator(
        translator_type="dummy",
        source_lang="en",
        target_lang="ha"
    )
    
    text_en = "Welcome to our platform!"
    result = translator_en_ha.translate(text_en)
    print(f"English: {result.original_text}")
    print(f"Hausa: {result.translated_text}")


def example_preprocessing():
    """Example: Text preprocessing."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Text Preprocessing")
    print("=" * 60)
    
    raw_text = "Check this out:   http://example.com   @email@test.com   !!!HELLO!!!"
    print(f"\nRaw text: {raw_text}")
    
    preprocessor = TextPreprocessor()
    
    cleaned = preprocessor.preprocess(
        raw_text,
        lowercase=True,
        remove_urls=True,
        remove_emails=True,
        normalize_whitespace=True,
    )
    
    print(f"Preprocessed: {cleaned}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("NLP Hub - Component Examples")
    print("=" * 60)
    
    try:
        example_intent_classification()
        example_entity_extraction()
        example_translation()
        example_preprocessing()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

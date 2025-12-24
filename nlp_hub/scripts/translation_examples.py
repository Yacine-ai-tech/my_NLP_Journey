"""Example usage of translation models with fine-tuning preparation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from translation import get_translator


def example_french_translation():
    """Example: Translate to French."""
    print("\n" + "=" * 60)
    print("EXAMPLE: English → French Translation")
    print("=" * 60)
    
    translator = get_translator(
        translator_type="m2m100",
        source_lang="en",
        target_lang="fr"
    )
    
    texts = [
        "Good morning!",
        "How are you today?",
        "Welcome to our platform.",
        "This is a production-ready NLP system.",
    ]
    
    print("\nTranslation Results:")
    for text in texts:
        result = translator.translate(text)
        print(f"\nEnglish: {result.original_text}")
        print(f"French:  {result.translated_text}")


def example_hausa_translation():
    """Example: Translate to Hausa."""
    print("\n" + "=" * 60)
    print("EXAMPLE: English → Hausa Translation")
    print("=" * 60)
    
    translator = get_translator(
        translator_type="m2m100",
        source_lang="en",
        target_lang="ha"
    )
    
    texts = [
        "Good morning!",
        "Welcome!",
        "Thank you for your help.",
        "Have a great day!",
    ]
    
    print("\nTranslation Results:")
    for text in texts:
        result = translator.translate(text)
        print(f"\nEnglish: {result.original_text}")
        print(f"Hausa:   {result.translated_text}")


def fine_tuning_instructions():
    """Print fine-tuning instructions."""
    print("\n" + "=" * 60)
    print("FINE-TUNING INSTRUCTIONS")
    print("=" * 60)
    
    instructions = """
To fine-tune translation models for specific domains:

1. Prepare Training Data:
   - Collect parallel corpus (source-target language pairs)
   - Clean and preprocess data
   - Split into train/val/test (80/10/10)
   - Save as JSON: [{"src": "...", "tgt": "..."}, ...]

2. Create Fine-tuning Script:
   Location: scripts/training/finetune_translation.py
   
   ```python
   from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
   from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
   
   # Load pre-trained model
   model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
   tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
   
   # Prepare dataset
   # ... load and process your data ...
   
   # Training arguments
   training_args = Seq2SeqTrainingArguments(
       output_dir="models/translation/custom-en-fr",
       num_train_epochs=3,
       per_device_train_batch_size=16,
       per_device_eval_batch_size=64,
       warmup_steps=500,
       weight_decay=0.01,
       save_total_limit=3,
   )
   
   # Trainer
   trainer = Seq2SeqTrainer(
       model=model,
       args=training_args,
       train_dataset=train_dataset,
       eval_dataset=eval_dataset,
   )
   
   trainer.train()
   ```

3. Run Fine-tuning:
   ```bash
   python scripts/training/finetune_translation.py
   ```

4. Evaluate:
   ```bash
   python scripts/training/evaluate_translation.py
   ```

5. Deploy Fine-tuned Model:
   - Save checkpoint: models/translation/custom-en-fr
   - Update config to use new model
   - Deploy with versioning

Domain-Specific Tips:
- Legal Translation: Fine-tune on legal documents
- Medical Translation: Use medical corpora
- Technical: Use technical documentation
- Informal: Use social media or chat data

Data Requirements:
- Minimum: 10,000 parallel sentences
- Better: 50,000+ parallel sentences
- Best: Domain-specific 100,000+ sentences
    """
    
    print(instructions)


if __name__ == "__main__":
    example_french_translation()
    example_hausa_translation()
    fine_tuning_instructions()

"""Quick start script to initialize NLP Hub."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from chatbot.manager import ChatbotManager
from config.settings import settings


def main():
    """Initialize and test NLP Hub."""
    print("=" * 60)
    print("NLP Hub - Quick Start")
    print("=" * 60)
    
    # Initialize chatbot
    print("\n✓ Initializing ChatbotManager...")
    chatbot = ChatbotManager()
    
    # Create conversation
    print("✓ Creating conversation...")
    conversation_id = chatbot.create_conversation()
    print(f"  Conversation ID: {conversation_id}")
    
    # Test message
    print("\n✓ Processing test message...")
    test_message = "Hello! How are you today?"
    print(f"  User: {test_message}")
    
    response = chatbot.process_user_message(
        conversation_id=conversation_id,
        user_message=test_message,
        use_rag=False  # Disable RAG for quick start
    )
    
    print(f"  Assistant: {response}")
    
    # Show configuration
    print("\n" + "=" * 60)
    print("Configuration Summary")
    print("=" * 60)
    print(f"Environment: {settings.env}")
    print(f"Debug Mode: {settings.debug}")
    print(f"LLM Provider: {settings.llm.provider}")
    print(f"LLM Model: {settings.llm.model_name}")
    print(f"Translation Models Path: {settings.translation.models_path}")
    print(f"Vector DB Type: {settings.rag.vector_db_type}")
    
    print("\n" + "=" * 60)
    print("✓ NLP Hub is ready!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Configure your .env file with API keys")
    print("2. Run: python main.py")
    print("3. Access API at: http://localhost:8000")
    print("4. View API docs at: http://localhost:8000/docs")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()

"""
Integration tests for ChatbotManager.
"""

import pytest
from src.chatbot import ChatbotManager
from src.intent import get_intent_classifier
from src.entity import get_entity_extractor
from src.llm import get_llm_manager


class TestChatbotIntegration:
    """Integration tests for chatbot."""
    
    def test_chatbot_initialization(self):
        """Test chatbot initialization."""
        chatbot = ChatbotManager()
        assert chatbot.llm_manager is not None
        assert chatbot.intent_classifier is not None
        assert chatbot.entity_extractor is not None
    
    def test_create_conversation(self):
        """Test creating conversation."""
        chatbot = ChatbotManager()
        conv_id = chatbot.create_conversation()
        assert conv_id in chatbot.conversations
    
    def test_process_message(self):
        """Test processing user message."""
        chatbot = ChatbotManager()
        conv_id = chatbot.create_conversation()
        
        response = chatbot.process_user_message(
            conversation_id=conv_id,
            user_message="Hello!",
            use_rag=False
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_conversation_history(self):
        """Test conversation history."""
        chatbot = ChatbotManager()
        conv_id = chatbot.create_conversation()
        
        chatbot.process_user_message(conv_id, "Hello!", use_rag=False)
        history = chatbot.get_conversation_history(conv_id)
        
        assert len(history) >= 2  # At least user and assistant message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

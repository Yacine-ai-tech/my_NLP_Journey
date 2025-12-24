"""Chatbot manager module."""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from ..utils.logger import get_logger
from ..utils.validators import validate_text
from ..utils.exceptions import ChatbotError
from ..config.settings import settings
from ..intent.classifier import IntentClassifier, get_intent_classifier
from ..entity.extractor import EntityExtractor, get_entity_extractor
from ..llm.manager import LLMManager, Message, get_llm_manager
from ..rag.retriever import RAGRetriever, get_rag_retriever


logger = get_logger(__name__, level=settings.log_level)


@dataclass
class ChatMessage:
    """Chat message with metadata."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ChatContext:
    """Conversation context."""
    conversation_id: str
    messages: List[ChatMessage] = field(default_factory=list)
    entities: Dict = field(default_factory=dict)
    intent: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    def add_message(self, message: ChatMessage):
        """Add message to context."""
        self.messages.append(message)
        
        # Keep only recent messages (maintain context window)
        max_messages = settings.chatbot.max_history
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]
    
    def get_conversation_history(self) -> List[Message]:
        """Get conversation history formatted for LLM."""
        return [
            Message(role=msg.role, content=msg.content)
            for msg in self.messages
        ]


class ChatbotManager:
    """Central chatbot manager orchestrating all NLP components."""
    
    def __init__(
        self,
        llm_manager: LLMManager = None,
        intent_classifier: IntentClassifier = None,
        entity_extractor: EntityExtractor = None,
        rag_retriever: RAGRetriever = None,
    ):
        """
        Initialize chatbot manager.
        
        Args:
            llm_manager: LLM manager instance
            intent_classifier: Intent classifier instance
            entity_extractor: Entity extractor instance
            rag_retriever: RAG retriever instance
        """
        logger.info("Initializing ChatbotManager")
        
        self.llm_manager = llm_manager or get_llm_manager("dummy")
        self.intent_classifier = intent_classifier or get_intent_classifier("dummy")
        self.entity_extractor = entity_extractor or get_entity_extractor("dummy")
        self.rag_retriever = rag_retriever or get_rag_retriever("dummy")
        
        self.conversations: Dict[str, ChatContext] = {}
    
    def create_conversation(self, conversation_id: str = None) -> str:
        """
        Create a new conversation.
        
        Args:
            conversation_id: Optional conversation ID
        
        Returns:
            Conversation ID
        """
        if conversation_id is None:
            conversation_id = f"conv_{datetime.now().timestamp()}"
        
        self.conversations[conversation_id] = ChatContext(conversation_id)
        logger.info(f"Created conversation: {conversation_id}")
        
        return conversation_id
    
    def process_user_message(
        self,
        conversation_id: str,
        user_message: str,
        use_rag: bool = True,
    ) -> str:
        """
        Process user message and generate response.
        
        Args:
            conversation_id: Conversation ID
            user_message: User input message
            use_rag: Whether to use RAG for context
        
        Returns:
            Assistant response
        
        Raises:
            ChatbotError: If processing fails
        """
        try:
            # Validate input
            user_message = validate_text(user_message)
            
            # Get or create conversation
            if conversation_id not in self.conversations:
                self.create_conversation(conversation_id)
            
            context = self.conversations[conversation_id]
            
            # Add user message to context
            context.add_message(ChatMessage(role="user", content=user_message))
            
            # Extract intent
            if settings.enable_intent_recognition:
                intent_result = self.intent_classifier.classify(user_message)
                context.intent = intent_result.name
                logger.debug(f"Detected intent: {intent_result.name}")
            
            # Extract entities
            if settings.enable_entity_extraction:
                extraction_result = self.entity_extractor.extract(user_message)
                context.entities = {
                    entity.label: entity.text
                    for entity in extraction_result.entities
                }
                logger.debug(f"Extracted entities: {context.entities}")
            
            # Retrieve relevant documents with RAG
            rag_context = ""
            if use_rag and settings.enable_rag:
                try:
                    retrieval_results = self.rag_retriever.search(user_message)
                    if retrieval_results:
                        rag_context = "\n".join(
                            f"Source: {r.source}\n{r.content}"
                            for r in retrieval_results[:3]
                        )
                        logger.debug(f"Retrieved {len(retrieval_results)} documents")
                except Exception as e:
                    logger.warning(f"RAG retrieval failed: {str(e)}")
            
            # Build system prompt
            system_prompt = self._build_system_prompt(context, rag_context)
            
            # Prepare messages for LLM
            messages = [Message(role="system", content=system_prompt)]
            messages.extend(context.get_conversation_history())
            
            # Generate response
            llm_response = self.llm_manager.chat(messages)
            assistant_message = llm_response.content
            
            # Add assistant response to context
            context.add_message(ChatMessage(role="assistant", content=assistant_message))
            
            logger.info(
                f"Generated chatbot response",
                extra={
                    "conversation_id": conversation_id,
                    "message_length": len(user_message),
                    "response_length": len(assistant_message),
                }
            )
            
            return assistant_message
        except Exception as e:
            logger.error(f"Message processing failed: {str(e)}")
            raise ChatbotError(f"Message processing failed: {str(e)}")
    
    def _build_system_prompt(self, context: ChatContext, rag_context: str = "") -> str:
        """
        Build system prompt with personality and context.
        
        Args:
            context: Chat context
            rag_context: Retrieved RAG context
        
        Returns:
            System prompt
        """
        personality_prompts = {
            "professional": "You are a professional, helpful AI assistant.",
            "friendly": "You are a friendly and conversational AI assistant.",
            "formal": "You are a formal and respectful AI assistant.",
        }
        
        personality = settings.chatbot.personality
        base_prompt = personality_prompts.get(personality, personality_prompts["professional"])
        
        system_prompt = base_prompt
        
        if context.intent:
            system_prompt += f"\nThe user's intent is: {context.intent}"
        
        if context.entities:
            system_prompt += f"\nExtracted entities: {context.entities}"
        
        if rag_context:
            system_prompt += f"\n\nRelevant context:\n{rag_context}"
        
        system_prompt += "\n\nProvide helpful, accurate, and relevant responses."
        
        return system_prompt
    
    def get_conversation_history(self, conversation_id: str) -> List[ChatMessage]:
        """
        Get conversation history.
        
        Args:
            conversation_id: Conversation ID
        
        Returns:
            List of chat messages
        """
        if conversation_id not in self.conversations:
            return []
        
        return self.conversations[conversation_id].messages
    
    def delete_conversation(self, conversation_id: str):
        """
        Delete a conversation.
        
        Args:
            conversation_id: Conversation ID to delete
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Deleted conversation: {conversation_id}")
    
    def clear_all_conversations(self):
        """Clear all conversations."""
        self.conversations.clear()
        logger.info("Cleared all conversations")

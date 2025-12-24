"""LLM (Large Language Model) integration module."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass
from ..utils.logger import get_logger
from ..utils.validators import validate_text
from ..utils.exceptions import LLMError, ModelNotFoundError
from ..config.settings import settings


logger = get_logger(__name__, level=settings.log_level)


@dataclass
class Message:
    """Chat message."""
    role: str  # "user", "assistant", "system"
    content: str


@dataclass
class LLMResponse:
    """LLM response."""
    content: str
    model: str
    tokens_used: int = 0
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class LLMManager(ABC):
    """Base class for LLM integration."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize LLM manager.
        
        Args:
            model_name: Name of the model to use
        """
        self.model_name = model_name or settings.llm.model_name
        self.client = None
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        """Initialize LLM client."""
        pass
    
    @abstractmethod
    def _call(self, messages: List[Message], **kwargs) -> LLMResponse:
        """Internal LLM call method."""
        pass
    
    def chat(self, messages: List[Message], **kwargs) -> LLMResponse:
        """
        Send chat messages to LLM.
        
        Args:
            messages: List of chat messages
            **kwargs: Additional parameters
        
        Returns:
            LLM response
        
        Raises:
            LLMError: If LLM call fails
        """
        try:
            if not messages:
                raise ValueError("Messages list cannot be empty")
            
            response = self._call(messages, **kwargs)
            
            logger.info(
                f"LLM call completed",
                extra={
                    "model": self.model_name,
                    "num_messages": len(messages),
                    "tokens_used": response.tokens_used,
                }
            )
            
            return response
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise LLMError(f"LLM call failed: {str(e)}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
        
        Returns:
            Generated text
        """
        prompt = validate_text(prompt)
        messages = [Message(role="user", content=prompt)]
        response = self.chat(messages, **kwargs)
        return response.content


class OpenAILLMManager(LLMManager):
    """LLM manager using OpenAI API."""
    
    def _load_model(self):
        """Initialize OpenAI client."""
        try:
            import openai
            
            logger.info(f"Initializing OpenAI LLM: {self.model_name}")
            openai.api_key = settings.llm.api_key
            self.client = openai
        except ImportError:
            raise ModelNotFoundError(
                "OpenAI library not installed. Install with: pip install openai"
            )
        except Exception as e:
            raise ModelNotFoundError(f"Failed to initialize OpenAI: {str(e)}")
    
    def _call(self, messages: List[Message], **kwargs) -> LLMResponse:
        """Call OpenAI API."""
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            response = self.client.ChatCompletion.create(
                model=self.model_name,
                messages=formatted_messages,
                temperature=kwargs.get("temperature", settings.llm.temperature),
                max_tokens=kwargs.get("max_tokens", settings.llm.max_tokens),
                top_p=kwargs.get("top_p", settings.llm.top_p),
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=self.model_name,
                tokens_used=response.usage.total_tokens if hasattr(response, "usage") else 0,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                },
            )
        except Exception as e:
            raise LLMError(f"OpenAI API call failed: {str(e)}")


class AnthropicLLMManager(LLMManager):
    """LLM manager using Anthropic API."""
    
    def _load_model(self):
        """Initialize Anthropic client."""
        try:
            import anthropic
            
            logger.info(f"Initializing Anthropic LLM: {self.model_name}")
            self.client = anthropic.Anthropic(api_key=settings.llm.api_key)
        except ImportError:
            raise ModelNotFoundError(
                "Anthropic library not installed. Install with: pip install anthropic"
            )
        except Exception as e:
            raise ModelNotFoundError(f"Failed to initialize Anthropic: {str(e)}")
    
    def _call(self, messages: List[Message], **kwargs) -> LLMResponse:
        """Call Anthropic API."""
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages if msg.role in ["user", "assistant"]
            ]
            
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=kwargs.get("max_tokens", settings.llm.max_tokens),
                messages=formatted_messages,
            )
            
            return LLMResponse(
                content=response.content[0].text if response.content else "",
                model=self.model_name,
                tokens_used=response.usage.output_tokens if hasattr(response, "usage") else 0,
            )
        except Exception as e:
            raise LLMError(f"Anthropic API call failed: {str(e)}")


class DummyLLMManager(LLMManager):
    """Dummy LLM manager for testing."""
    
    def _load_model(self):
        """Initialize dummy manager."""
        logger.info("Using dummy LLM manager")
        self.client = None
    
    def _call(self, messages: List[Message], **kwargs) -> LLMResponse:
        """Return dummy response."""
        if messages:
            last_message = messages[-1].content
            response_text = f"Dummy response to: '{last_message[:50]}...'"
        else:
            response_text = "Dummy response"
        
        return LLMResponse(
            content=response_text,
            model="dummy-model",
            tokens_used=10,
        )


def get_llm_manager(manager_type: str = "openai") -> LLMManager:
    """
    Factory function to get LLM manager.
    
    Args:
        manager_type: Type of manager ('openai', 'anthropic', or 'dummy')
    
    Returns:
        LLMManager instance
    """
    if manager_type == "openai":
        return OpenAILLMManager()
    elif manager_type == "anthropic":
        return AnthropicLLMManager()
    elif manager_type == "dummy":
        return DummyLLMManager()
    else:
        raise ValueError(f"Unknown manager type: {manager_type}")

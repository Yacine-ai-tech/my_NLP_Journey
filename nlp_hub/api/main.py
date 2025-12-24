"""FastAPI application for NLP Hub."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from ..config.settings import settings
from ..chatbot.manager import ChatbotManager
from ..utils.logger import get_logger


logger = get_logger(__name__, level=settings.log_level)


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model."""
    conversation_id: str
    message: str
    use_rag: bool = True


class ChatResponse(BaseModel):
    """Chat response model."""
    conversation_id: str
    response: str
    intent: Optional[str] = None
    entities: dict = {}


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


# Initialize chatbot manager
chatbot_manager: Optional[ChatbotManager] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    global chatbot_manager
    logger.info("Starting NLP Hub API")
    chatbot_manager = ChatbotManager()
    yield
    # Shutdown
    logger.info("Shutting down NLP Hub API")


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="NLP Hub API",
        description="Comprehensive NLP Pipeline API",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        return HealthResponse(status="healthy", version="1.0.0")
    
    # Chat endpoint
    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        """Chat endpoint."""
        try:
            if chatbot_manager is None:
                raise HTTPException(status_code=503, detail="Service not initialized")
            
            response = chatbot_manager.process_user_message(
                conversation_id=request.conversation_id,
                user_message=request.message,
                use_rag=request.use_rag,
            )
            
            context = chatbot_manager.conversations.get(request.conversation_id)
            
            return ChatResponse(
                conversation_id=request.conversation_id,
                response=response,
                intent=context.intent if context else None,
                entities=context.entities if context else {},
            )
        except Exception as e:
            logger.error(f"Chat endpoint error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Create conversation endpoint
    @app.post("/conversations")
    async def create_conversation():
        """Create new conversation."""
        try:
            if chatbot_manager is None:
                raise HTTPException(status_code=503, detail="Service not initialized")
            
            conversation_id = chatbot_manager.create_conversation()
            return {"conversation_id": conversation_id}
        except Exception as e:
            logger.error(f"Create conversation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Get conversation history
    @app.get("/conversations/{conversation_id}/history")
    async def get_history(conversation_id: str):
        """Get conversation history."""
        try:
            if chatbot_manager is None:
                raise HTTPException(status_code=503, detail="Service not initialized")
            
            history = chatbot_manager.get_conversation_history(conversation_id)
            return {
                "conversation_id": conversation_id,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat(),
                    }
                    for msg in history
                ],
            }
        except Exception as e:
            logger.error(f"Get history error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Delete conversation
    @app.delete("/conversations/{conversation_id}")
    async def delete_conversation(conversation_id: str):
        """Delete conversation."""
        try:
            if chatbot_manager is None:
                raise HTTPException(status_code=503, detail="Service not initialized")
            
            chatbot_manager.delete_conversation(conversation_id)
            return {"message": f"Conversation {conversation_id} deleted"}
        except Exception as e:
            logger.error(f"Delete conversation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

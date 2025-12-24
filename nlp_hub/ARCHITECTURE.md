"""
Architecture Guide for NLP Hub

This document describes the system architecture and design patterns.

Author: Yacine-ai-tech (siddoyacinetech227@gmail.com)
Repository: https://github.com/Yacine-ai-tech/my_NLP_Journey
Last Updated: December 24, 2025
"""

# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                    │
│              /chat, /conversations, /health                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────v──────────────────────────────────────┐
│                   ChatbotManager                            │
│          (Orchestration & Conversation Logic)               │
└──────────────────┬──────────────────┬───────────────────────┘
                   │                  │
         ┌─────────v─────────┐    ┌──v──────────────┐
         │                   │    │                 │
    ┌────v────┐ ┌──────────┐│  ┌──v──────┐ ┌─────v────┐
    │ Intent  │ │ Entity   ││  │   RAG   │ │   LLM    │
    │Classify │ │Extract   ││  │Retriever│ │ Manager  │
    └────────┘ │          ││  │         │ └──────────┘
               └──────────┘│  └─────────┘
               │                    │
       ┌───────v────────────────────v────────┐
       │         Translation Engine           │
       │  (MarianMT / M2M-100 Models)        │
       └────────────────────────────────────┘
```

## Component Details

### 1. API Layer
- **Technology**: FastAPI + Uvicorn
- **Endpoints**:
  - `POST /chat` - Send message
  - `POST /conversations` - Create conversation
  - `GET /conversations/{id}/history` - Get history
  - `DELETE /conversations/{id}` - Delete conversation
  - `GET /health` - Health check

### 2. ChatbotManager
- **Responsibility**: Orchestrate all NLP components
- **Features**:
  - Conversation management
  - Message context tracking
  - Intent extraction
  - Entity recognition
  - RAG integration
  - Response generation

### 3. Intent Classifier
- **Models**: Transformer-based (DistilBERT, BERT)
- **Task**: Classify user intent
- **Output**: Intent name + confidence score

### 4. Entity Extractor
- **Models**: Transformer-based NER
- **Task**: Extract named entities
- **Output**: Entity list with labels and confidence

### 5. RAG Retriever
- **Vector DB**: FAISS
- **Embeddings**: Sentence Transformers
- **Task**: Retrieve relevant documents
- **Output**: Top-k similar documents with scores

### 6. LLM Manager
- **Providers**: OpenAI, Anthropic, Local
- **Task**: Generate contextual responses
- **Features**: Temperature, max_tokens, top_p control

### 7. Translation Engine
- **Models**: 
  - MarianMT (single language pair)
  - M2M-100 (100 languages)
- **Languages**: English, French, Hausa, Spanish, etc.
- **Task**: Translate between languages

## Data Flow

### Conversation Flow

```
User Input
  ↓
[Preprocessing]
  - Lowercase
  - Clean URLs/emails
  - Normalize whitespace
  ↓
[Intent Classification]
  - Extract user intent
  - Confidence scoring
  ↓
[Entity Extraction]
  - Find named entities
  - Categorize entities
  ↓
[RAG Retrieval] (optional)
  - Embed user query
  - Search vector database
  - Retrieve top-k documents
  ↓
[Context Building]
  - Compile system prompt
  - Include conversation history
  - Add extracted entities
  - Include RAG context
  ↓
[LLM Generation]
  - Send to LLM with context
  - Generate response
  ↓
[Post-processing]
  - Format response
  - Apply translation if needed
  ↓
Response to User
```

### Message Format

```json
{
  "role": "user|assistant",
  "content": "text content",
  "timestamp": "2024-01-15T10:30:45.123456",
  "metadata": {
    "intent": "greeting",
    "entities": {"PERSON": "John"},
    "language": "en"
  }
}
```

## Design Patterns

### 1. Factory Pattern

All major components use factory functions:

```python
classifier = get_intent_classifier("transformer")
extractor = get_entity_extractor("dummy")
translator = get_translator("m2m100", "en", "fr")
```

### 2. Strategy Pattern

Multiple implementations for same interface:

```python
class IntentClassifier(ABC):
    @abstractmethod
    def _predict(self, text: str) -> Intent:
        pass

class TransformerIntentClassifier(IntentClassifier):
    def _predict(self, text: str) -> Intent:
        # Transformer implementation
        
class DummyIntentClassifier(IntentClassifier):
    def _predict(self, text: str) -> Intent:
        # Simple keyword-based implementation
```

### 3. Dependency Injection

```python
chatbot = ChatbotManager(
    llm_manager=custom_llm,
    intent_classifier=custom_classifier,
    entity_extractor=custom_extractor,
    rag_retriever=custom_retriever,
)
```

### 4. Configuration Management

```python
from src.config.settings import settings

# Access settings
llm_temperature = settings.llm.temperature
batch_size = settings.rag.chunk_size
```

## Database Design (Optional)

### Tables

```sql
-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    context JSONB
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID,
    role VARCHAR(20),
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- User Feedback
CREATE TABLE feedback (
    id UUID PRIMARY KEY,
    message_id UUID,
    rating INT,
    comments TEXT,
    created_at TIMESTAMP
);
```

## Performance Considerations

### Caching Strategy

```python
@cache(ttl=3600)
def get_embedding(text: str):
    """Cache embeddings for 1 hour."""
    return embeddings.encode(text)
```

### Batch Processing

```python
# Process multiple items efficiently
results = classifier.batch_classify(texts)
```

### Model Optimization

1. **Quantization**: Use int8/fp16 models
2. **Distillation**: Use smaller models
3. **Caching**: Cache model predictions
4. **GPU**: Enable CUDA for faster inference

## Security Considerations

### Input Validation

```python
from src.utils.validators import validate_text
text = validate_text(user_input)
```

### API Security

- CORS configuration
- Rate limiting
- Authentication (JWT)
- Input sanitization

### Data Protection

- Encrypt sensitive data at rest
- Use HTTPS in production
- Implement access controls
- Log security events

## Monitoring & Observability

### Logging

```python
logger.info(
    "Message processed",
    extra={
        "conversation_id": conv_id,
        "message_length": len(text),
        "intent": intent.name,
    }
)
```

### Metrics

- API response time
- Token usage
- Model accuracy
- User satisfaction

### Health Checks

```bash
curl http://localhost:8000/health
```

## Deployment Architecture

### Development

```
Laptop/Desktop
    ↓
Python REPL / Scripts
```

### Staging

```
Single Server
    ├── API (FastAPI)
    ├── PostgreSQL
    └── FAISS DB
```

### Production

```
Load Balancer
    ├── API Server 1
    ├── API Server 2
    └── API Server 3
         ↓
    PostgreSQL (Replicated)
         ↓
    Redis (Caching)
         ↓
    FAISS DB (Shared)
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI, Uvicorn |
| ML/NLP | PyTorch, Transformers |
| Embeddings | Sentence Transformers |
| Vector DB | FAISS, Pinecone |
| Database | PostgreSQL, SQLAlchemy |
| Caching | Redis |
| Logging | JSON Logger, Structlog |
| Testing | pytest |
| Containerization | Docker, Docker Compose |
| Monitoring | Prometheus, Grafana (optional) |

---

For more information, see [README.md](README.md)

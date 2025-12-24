"""
QUICK REFERENCE GUIDE

NLP Hub - Command Reference and Common Tasks

Author: Yacine-ai-tech (siddoyacinetech227@gmail.com)
Repository: https://github.com/Yacine-ai-tech/my_NLP_Journey
Last Updated: December 24, 2025
"""

# Quick Reference Guide

## Installation & Setup

```bash
# Clone and setup
git clone <repo>
cd nlp-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys
```

## Running the Application

```bash
# Start API server
python main.py

# Access documentation
http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_intent.py -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v
```

## Docker

```bash
# Build image
docker build -f docker/Dockerfile -t nlp-hub:latest .

# Run container
docker run -p 8000:8000 -e LLM_API_KEY=your_key nlp-hub:latest

# Using Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker logs -f <container_id>

# Stop container
docker-compose -f docker/docker-compose.yml down
```

## Python API Usage

### Chatbot
```python
from src import ChatbotManager

chatbot = ChatbotManager()
conv_id = chatbot.create_conversation()
response = chatbot.process_user_message(conv_id, "Hello")
print(response)
```

### Intent Classification
```python
from src.intent import get_intent_classifier

classifier = get_intent_classifier("dummy")
intent = classifier.classify("What is this?")
print(f"{intent.name}: {intent.confidence}")
```

### Entity Extraction
```python
from src.entity import get_entity_extractor

extractor = get_entity_extractor("dummy")
result = extractor.extract("John works at Google")
for entity in result.entities:
    print(f"{entity.label}: {entity.text}")
```

### Translation
```python
from src.translation import get_translator

# English to French
translator = get_translator("m2m100", "en", "fr")
result = translator.translate("Hello world")
print(result.translated_text)
```

### RAG
```python
from src.rag import get_rag_retriever

retriever = get_rag_retriever("dummy")
retriever.add_documents(["Doc 1", "Doc 2"])
results = retriever.search("query")
```

### LLM
```python
from src.llm import get_llm_manager, Message

llm = get_llm_manager("dummy")
messages = [Message(role="user", content="Hi")]
response = llm.chat(messages)
```

## API Endpoints

### Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_123",
    "message": "Hello!",
    "use_rag": true
  }'
```

### Create Conversation
```bash
curl -X POST http://localhost:8000/conversations
```

### Get History
```bash
curl http://localhost:8000/conversations/conv_123/history
```

### Delete Conversation
```bash
curl -X DELETE http://localhost:8000/conversations/conv_123
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Configuration

### Environment Variables
```env
ENVIRONMENT=development
DEBUG=false
API_HOST=127.0.0.1
API_PORT=8000
LOG_LEVEL=INFO
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
LLM_API_KEY=sk-...
USE_GPU=false
```

### Python Configuration
```python
from src.config.settings import settings

# Access settings
print(settings.llm.model_name)
print(settings.env)
print(settings.data_dir)

# Modify settings
settings.llm.temperature = 0.8
```

## Logging

### View Logs
```bash
# Real-time logs
tail -f logs/app.log

# Filter errors
grep "ERROR" logs/app.log

# Parse JSON logs
tail -f logs/app.log | jq .
```

### Configure Logging
```python
from src.utils.logger import get_logger

logger = get_logger(__name__, level="DEBUG")
logger.info("Message", extra={"key": "value"})
```

## Development Tasks

### Format Code
```bash
# Auto-format with Black
black src/

# Sort imports
isort src/

# Lint with Flake8
flake8 src/

# Type checking
mypy src/
```

### Run Example Scripts
```bash
# Quick start
python scripts/quickstart.py

# Component examples
python scripts/examples.py

# Translation examples
python scripts/translation_examples.py
```

## Project Structure Commands

```bash
# View project structure
tree nlp_hub/

# Count Python files
find . -name "*.py" | wc -l

# View file sizes
du -sh nlp_hub/

# List modules
ls -la src/
```

## Common Issues & Solutions

### Issue: ImportError
```python
# Solution: Add src to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

### Issue: Model not found
```python
# Solution: Use dummy implementations
classifier = get_intent_classifier("dummy")
```

### Issue: No GPU
```bash
# Solution: Update .env
USE_GPU=false
```

### Issue: Database connection
```bash
# Solution: Check PostgreSQL running
sudo systemctl status postgresql
```

## Database Commands

```bash
# Connect to PostgreSQL
psql -U nlp_hub -d nlp_hub

# Create backup
pg_dump nlp_hub > backup.sql

# Restore backup
psql nlp_hub < backup.sql

# List databases
\l

# List tables
\dt

# Quit psql
\q
```

## Performance Tips

```python
# Use batch processing
results = classifier.batch_classify(texts)

# Cache results
from functools import lru_cache

@lru_cache(maxsize=128)
def get_embedding(text):
    return embeddings.encode(text)

# Monitor performance
import time
start = time.time()
# ... code ...
print(f"Took {time.time() - start:.2f}s")
```

## Useful Links

- [Hugging Face Models](https://huggingface.co/models)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PyTorch Docs](https://pytorch.org/docs/)
- [Transformers Library](https://huggingface.co/docs/transformers/)

## File Locations

| Component | File |
|-----------|------|
| Chatbot | `src/chatbot/manager.py` |
| Intent | `src/intent/classifier.py` |
| Entity | `src/entity/extractor.py` |
| RAG | `src/rag/retriever.py` |
| Speech | `src/speech/processor.py` |
| LLM | `src/llm/manager.py` |
| Translation | `src/translation/translator.py` |
| API | `api/main.py` |
| Config | `src/config/settings.py` |
| Utils | `src/utils/` |

## Documentation

| Document | Purpose |
|----------|---------|
| README.md | Main documentation |
| ARCHITECTURE.md | System design |
| CONTRIBUTING.md | Development guide |
| DEPLOYMENT.md | Production deployment |
| CHANGELOG.md | Version history |
| SETUP_SUMMARY.md | Setup overview |

---

**For more details, see the full documentation in README.md and other guide files.**

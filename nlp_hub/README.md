# NLP Hub - Production-Ready NLP Pipeline

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/code%20quality-production%2D-brightgreen.svg)]()

A comprehensive, production-ready NLP platform integrating **Chatbot**, **Intent Recognition**, **Entity Extraction**, **RAG (Retrieval Augmented Generation)**, **Speech Processing**, **LLM Integration**, and **Multi-language Translation** (French, Hausa, and more).

## 🚀 Features

### Core NLP Components

- **🤖 Chatbot Manager**: Orchestrates all NLP components for conversational AI
- **🎯 Intent Classification**: Recognizes user intent (greeting, question, request, etc.)
- **🏷️ Named Entity Recognition (NER)**: Extracts entities (PERSON, ORG, GPE, DATE, etc.)
- **📚 RAG (Retrieval Augmented Generation)**: Retrieves relevant context from knowledge base
- **🎤 Speech Processing**: Speech-to-Text (STT) and Text-to-Speech (TTS)
- **🧠 LLM Integration**: Support for OpenAI, Anthropic, and local models
- **🌍 Multi-Language Translation**: English ↔ French, English ↔ Hausa, and more

### Production Features

- ✅ Modular architecture with clean separation of concerns
- ✅ RESTful API with FastAPI
- ✅ Comprehensive logging and error handling
- ✅ Configuration management with environment variables
- ✅ Docker support for containerized deployment
- ✅ Type hints and Pydantic validation
- ✅ Extensible plugin architecture
- ✅ Unit and integration tests
- ✅ CI/CD ready

## 📁 Project Structure

```
nlp_hub/
├── src/
│   ├── __init__.py
│   ├── chatbot/              # Chatbot orchestration
│   ├── intent/               # Intent classification
│   ├── entity/               # Named entity recognition
│   ├── rag/                  # Retrieval augmented generation
│   ├── speech/               # Speech processing (STT/TTS)
│   ├── llm/                  # LLM integration layer
│   ├── translation/          # Multi-language translation
│   ├── preprocessing/        # Text preprocessing utilities
│   ├── config/               # Configuration management
│   └── utils/                # Logging, validators, exceptions
├── api/                      # FastAPI application
├── models/
│   ├── pretrained/           # Pre-trained models
│   ├── checkpoints/          # Fine-tuned checkpoints
│   └── translation/          # Translation models
├── data/
│   ├── raw/                  # Raw datasets
│   ├── processed/            # Processed data
│   ├── embeddings/           # Vector embeddings
│   └── translations/         # Translation data
├── tests/
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── notebooks/                # Jupyter notebooks for analysis
├── docker/                   # Docker configuration
├── scripts/                  # Utility scripts
├── logs/                     # Application logs
├── requirements.txt          # Python dependencies
├── setup.py                  # Setup script
├── pyproject.toml           # Project metadata
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip or conda package manager
- 8GB+ RAM (16GB+ recommended for LLMs)
- GPU (optional, for faster inference)

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nlp-hub.git
cd nlp-hub
```

#### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n nlp_hub python=3.10
conda activate nlp_hub
```

#### 3. Install Dependencies

```bash
# Install basic dependencies
pip install -r requirements.txt

# Or with development tools
pip install -e ".[dev]"

# For GPU support (NVIDIA)
pip install -e ".[gpu]"

# For speech processing
pip install -e ".[speech]"

# For LLM APIs
pip install -e ".[llm]"
```

#### 4. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration
nano .env  # Or use your preferred editor
```

**Important settings:**
```env
# LLM API (choose one)
LLM_PROVIDER=openai
LLM_API_KEY=sk-...

# Or use Anthropic
# LLM_PROVIDER=anthropic
# LLM_API_KEY=sk-ant-...

# Database (optional)
DB_HOST=localhost
DB_PORT=5432
DB_USER=nlp_hub
DB_PASSWORD=password

# GPU Support
USE_GPU=true
```

## 📖 Usage

### 1. Using the Python API

```python
from src import ChatbotManager

# Initialize chatbot
chatbot = ChatbotManager()

# Create a conversation
conversation_id = chatbot.create_conversation()

# Process user message
response = chatbot.process_user_message(
    conversation_id=conversation_id,
    user_message="Hello! What's the weather today?",
    use_rag=True
)

print(response)
```

### 2. Using Individual Components

#### Intent Classification

```python
from src.intent import get_intent_classifier

classifier = get_intent_classifier()
intent = classifier.classify("What is your name?")
print(f"Intent: {intent.name}, Confidence: {intent.confidence}")
```

#### Entity Extraction

```python
from src.entity import get_entity_extractor

extractor = get_entity_extractor()
result = extractor.extract("John Smith works at Microsoft in Seattle")
for entity in result.entities:
    print(f"{entity.label}: {entity.text}")
```

#### Translation (French & Hausa)

```python
from src.translation import get_translator

# English to French
translator_en_fr = get_translator(
    translator_type="m2m100",
    source_lang="en",
    target_lang="fr"
)
result = translator_en_fr.translate("Hello, how are you?")
print(result.translated_text)  # Bonjour, comment allez-vous?

# English to Hausa
translator_en_ha = get_translator(
    translator_type="m2m100",
    source_lang="en",
    target_lang="ha"
)
result = translator_en_ha.translate("Good morning")
print(result.translated_text)  # Sannu da safiya
```

#### Speech Processing

```python
from src.speech import get_speech_processor
from pathlib import Path

processor = get_speech_processor()

# Speech to Text
result = processor.transcribe(Path("audio.wav"))
print(f"Transcribed: {result.text}")

# Text to Speech
output = processor.synthesize(
    "Hello, this is a test",
    Path("output.mp3")
)
print(f"Audio saved to: {output.audio_path}")
```

#### RAG (Retrieval Augmented Generation)

```python
from src.rag import get_rag_retriever

retriever = get_rag_retriever()

# Add documents to knowledge base
documents = [
    "Python is a programming language",
    "Machine learning is a subset of AI",
    "NLP deals with natural language understanding"
]
retriever.add_documents(documents)

# Retrieve relevant documents
results = retriever.search("What is Python?")
for result in results:
    print(f"Score: {result.score}, Content: {result.content}")
```

#### LLM Integration

```python
from src.llm import get_llm_manager, Message

# Choose LLM provider
llm = get_llm_manager("openai")  # or "anthropic"

# Chat with LLM
messages = [
    Message(role="system", content="You are a helpful assistant"),
    Message(role="user", content="What is machine learning?")
]
response = llm.chat(messages)
print(response.content)
```

### 3. Using the REST API

Start the API server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Create Conversation

```bash
curl -X POST http://localhost:8000/conversations
# Response: {"conversation_id": "conv_1234567890"}
```

#### Send Message

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_1234567890",
    "message": "Hello, how are you?",
    "use_rag": true
  }'
```

#### Get Conversation History

```bash
curl http://localhost:8000/conversations/conv_1234567890/history
```

#### Delete Conversation

```bash
curl -X DELETE http://localhost:8000/conversations/conv_1234567890
```

## 🔧 Configuration

### Environment Variables

All configuration is managed through environment variables (see `.env.example`):

```env
# Environment
ENVIRONMENT=production  # development, staging, production
DEBUG=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# LLM Configuration
LLM_PROVIDER=openai     # openai, anthropic, local
LLM_MODEL=gpt-3.5-turbo
LLM_API_KEY=your_key_here

# Intent Classification
INTENT_MODEL=transformer
INTENT_MODEL_NAME=distilbert-base-uncased

# Entity Recognition
ENTITY_MODEL=transformer
ENTITY_MODEL_NAME=distilbert-base-uncased

# RAG Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB=faiss
VECTOR_DB_PATH=data/embeddings/vectors

# Translation
TRANSLATION_MODELS_PATH=models/translation
USE_GPU=true

# Speech Processing
SPEECH_PROVIDER=google
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### Python Configuration

Configuration can also be modified in code:

```python
from src.config.settings import settings

# Modify settings
settings.llm.temperature = 0.8
settings.rag.top_k = 10
settings.chatbot.max_history = 20
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_intent_classifier.py

# Run integration tests only
pytest tests/integration/
```

## 🐳 Docker

Build and run with Docker:

```bash
# Build image
docker build -f docker/Dockerfile -t nlp-hub:latest .

# Run container
docker run -p 8000:8000 \
  -e LLM_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  nlp-hub:latest

# Using Docker Compose (if available)
docker-compose -f docker/docker-compose.yml up
```

## 📚 Translation Models

### Supported Language Pairs

The translation module supports:

| Language | Code | Availability |
|----------|------|--------------|
| English | en | ✅ Full Support |
| French | fr | ✅ Full Support |
| Hausa | ha | ✅ Full Support |
| Spanish | es | ✅ Full Support |
| German | de | ✅ Full Support |
| Italian | it | ✅ Full Support |
| Portuguese | pt | ✅ Full Support |

### Fine-tuning Translation Models

To fine-tune translation models for specific domains:

```python
from src.translation import Translator

# Instructions for fine-tuning
# 1. Prepare parallel corpus (source and target language pairs)
# 2. Create training scripts in scripts/training/
# 3. Use transformers library with Seq2Seq trainer
# 4. Save checkpoints in models/translation/
# 5. Load fine-tuned model in production

# Load fine-tuned model
from transformers import MarianMTModel, MarianTokenizer

model_name = "models/translation/custom-en-fr"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
```

**Model Architecture:**
- **MarianMT**: Fast, single language pair translation
- **M2M-100**: Universal 100-language translation model (recommended for multiple language pairs)

## 🔌 Extension Points

### Adding Custom Components

1. **Custom Intent Classifier:**

```python
from src.intent import IntentClassifier

class CustomIntentClassifier(IntentClassifier):
    def _load_model(self):
        # Load your custom model
        pass
    
    def _predict(self, text: str) -> Intent:
        # Implement your logic
        pass
```

2. **Custom Entity Extractor:**

```python
from src.entity import EntityExtractor

class CustomEntityExtractor(EntityExtractor):
    def _load_model(self):
        # Load your custom model
        pass
    
    def _extract(self, text: str) -> ExtractionResult:
        # Implement your logic
        pass
```

3. **Custom Translator:**

```python
from src.translation import Translator

class CustomTranslator(Translator):
    def _load_model(self):
        # Load your custom model
        pass
    
    def _translate(self, text: str) -> str:
        # Implement your logic
        pass
```

## 📊 Architecture

### Component Interaction

```
User Input
    ↓
[ChatbotManager]
    ├── → [IntentClassifier] → Extract intent
    ├── → [EntityExtractor] → Extract entities
    ├── → [RAGRetriever] → Fetch context
    ├── → [Translator] → (Optional) Translate
    └── → [LLMManager] → Generate response
        ↓
    Assistant Response
```

### Data Flow

```
Text Input
    ↓
[Preprocessing] - Clean & normalize
    ↓
[Tokenization] - Split into tokens
    ↓
[Embedding] - Convert to vectors
    ↓
[Classification/Extraction/Retrieval]
    ↓
[Post-processing] - Format results
    ↓
Output
```

## 🚀 Production Deployment

### Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up API key for LLM provider
- [ ] Configure CORS properly
- [ ] Set strong `SECRET_KEY`
- [ ] Enable logging to files
- [ ] Set up monitoring/alerting
- [ ] Configure backup for vector databases
- [ ] Use reverse proxy (nginx/Apache)
- [ ] Set up SSL/TLS certificates
- [ ] Load test the system

### Performance Optimization

1. **Model Optimization:**
   - Use quantized models (int8, fp16)
   - Enable model caching
   - Use batch processing

2. **API Optimization:**
   - Enable response compression
   - Use caching for frequent queries
   - Implement rate limiting

3. **Database Optimization:**
   - Index frequently queried fields
   - Implement query caching
   - Regular backups

4. **Vector Database:**
   - Periodically rebuild FAISS indices
   - Archive old embeddings
   - Monitor memory usage

## 📝 Logging

Logs are generated in JSON format for easy parsing:

```json
{
    "timestamp": "2024-01-15T10:30:45.123456",
    "level": "INFO",
    "logger": "src.chatbot.manager",
    "message": "Generated chatbot response",
    "conversation_id": "conv_123",
    "response_length": 256
}
```

View logs:

```bash
tail -f logs/app.log | jq .
```

## 🤝 Contributing

For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md). All contributions are welcome!

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- 📧 Email: siddoyacinetech227@gmail.com
- 💬 Discussions: [GitHub Discussions](https://github.com/Yacine-ai-tech/my_NLP_Journey/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/Yacine-ai-tech/my_NLP_Journey/issues)
- 👤 Author: [@Yacine-ai-tech](https://github.com/Yacine-ai-tech)

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) - Transformers and Models
- [Facebook Research](https://research.facebook.com/) - MarianMT, M2M-100
- [OpenAI](https://openai.com/) - GPT Models
- [Anthropic](https://www.anthropic.com/) - Claude
- [Google Cloud](https://cloud.google.com/) - Speech APIs

## 📚 References

- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [RAG Systems](https://arxiv.org/abs/2005.11401)
- [Named Entity Recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)

---

**Built with ❤️ for the NLP Community**

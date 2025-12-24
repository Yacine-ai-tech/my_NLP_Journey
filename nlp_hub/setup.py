"""Setup script for NLP Hub."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nlp-hub",
    version="1.0.0",
    author="Yacine-ai-tech",
    author_email="siddoyacinetech227@gmail.com",
    description="Comprehensive NLP Pipeline with Chatbot, Intent Recognition, Entity Extraction, RAG, Speech, LLM, and Translation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yacine-ai-tech/my_NLP_Journey",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=0.21.0",
        "pydantic>=2.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.4",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "gpu": [
            "torch[cuda11]>=2.0.0",
            "faiss-gpu>=1.7.4",
        ],
        "speech": [
            "google-cloud-speech>=2.21.0",
            "google-cloud-texttospeech>=2.14.0",
        ],
        "llm": [
            "openai>=1.3.0",
            "anthropic>=0.7.0",
        ],
    },
)

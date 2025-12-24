"""RAG (Retrieval Augmented Generation) module."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from dataclasses import dataclass
from ..utils.logger import get_logger
from ..utils.validators import validate_text
from ..utils.exceptions import RAGError, ModelNotFoundError
from ..config.settings import settings


logger = get_logger(__name__, level=settings.log_level)


@dataclass
class RetrievalResult:
    """Retrieved document result."""
    content: str
    source: str
    score: float
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class RAGRetriever(ABC):
    """Base class for RAG retrieval."""
    
    def __init__(self, embedding_model: str = None):
        """
        Initialize RAG retriever.
        
        Args:
            embedding_model: Name of embedding model to use
        """
        self.embedding_model = embedding_model or settings.rag.embedding_model
        self.embeddings = None
        self.vector_store = None
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        """Load embedding model and vector store."""
        pass
    
    @abstractmethod
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the vector store."""
        pass
    
    @abstractmethod
    def retrieve(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        """Retrieve relevant documents."""
        pass
    
    def search(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of retrieved documents
        
        Raises:
            RAGError: If retrieval fails
        """
        try:
            query = validate_text(query)
            top_k = top_k or settings.rag.top_k
            
            results = self.retrieve(query, top_k)
            
            logger.info(
                f"RAG retrieval completed",
                extra={
                    "query_length": len(query),
                    "num_results": len(results),
                }
            )
            
            return results
        except Exception as e:
            logger.error(f"RAG retrieval failed: {str(e)}")
            raise RAGError(f"RAG retrieval failed: {str(e)}")


class FAISSRetriever(RAGRetriever):
    """RAG retriever using FAISS for vector storage."""
    
    def _load_model(self):
        """Load embedding model and initialize FAISS."""
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            
            logger.info(f"Loading embedding model: {self.embedding_model}")
            self.embeddings = SentenceTransformer(self.embedding_model)
            self.vector_store = None
            self.documents = []
            self.metadata_list = []
        except ImportError:
            raise ModelNotFoundError(
                "Required libraries not installed. Install with: "
                "pip install sentence-transformers faiss-cpu"
            )
        except Exception as e:
            raise ModelNotFoundError(f"Failed to load model: {str(e)}")
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to FAISS index."""
        try:
            import faiss
            import numpy as np
            
            if not documents:
                return
            
            # Embed documents
            embeddings = self.embeddings.encode(documents)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.vector_store = faiss.IndexFlatL2(dimension)
            self.vector_store.add(np.array(embeddings).astype("float32"))
            
            self.documents = documents
            self.metadata_list = metadata or [{} for _ in documents]
            
            logger.info(f"Added {len(documents)} documents to FAISS index")
        except Exception as e:
            raise RAGError(f"Failed to add documents: {str(e)}")
    
    def retrieve(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        """Retrieve documents using FAISS similarity search."""
        if self.vector_store is None or not self.documents:
            return []
        
        top_k = top_k or settings.rag.top_k
        
        try:
            import numpy as np
            
            # Embed query
            query_embedding = self.embeddings.encode([query])
            
            # Search in FAISS
            distances, indices = self.vector_store.search(
                np.array(query_embedding).astype("float32"),
                k=min(top_k, len(self.documents)),
            )
            
            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx >= 0:  # Valid index
                    # Convert L2 distance to similarity score
                    score = 1 / (1 + distance)
                    
                    if score >= settings.rag.similarity_threshold:
                        results.append(
                            RetrievalResult(
                                content=self.documents[idx],
                                source=self.metadata_list[idx].get("source", "unknown"),
                                score=score,
                                metadata=self.metadata_list[idx],
                            )
                        )
            
            return results
        except Exception as e:
            raise RAGError(f"Retrieval failed: {str(e)}")


class DummyRetriever(RAGRetriever):
    """Dummy RAG retriever for testing."""
    
    def _load_model(self):
        """Initialize dummy retriever."""
        logger.info("Using dummy RAG retriever")
        self.documents = []
        self.metadata_list = []
    
    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Store documents in memory."""
        self.documents = documents
        self.metadata_list = metadata or [{} for _ in documents]
        logger.info(f"Added {len(documents)} documents to dummy retriever")
    
    def retrieve(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        """Return dummy results."""
        top_k = top_k or settings.rag.top_k
        
        if not self.documents:
            return []
        
        # Return first top_k documents with fake scores
        results = []
        for i, (doc, metadata) in enumerate(zip(self.documents[:top_k], self.metadata_list[:top_k])):
            results.append(
                RetrievalResult(
                    content=doc,
                    source=metadata.get("source", f"doc_{i}"),
                    score=0.9 - (i * 0.05),
                    metadata=metadata,
                )
            )
        
        return results


def get_rag_retriever(retriever_type: str = "faiss") -> RAGRetriever:
    """
    Factory function to get RAG retriever.
    
    Args:
        retriever_type: Type of retriever ('faiss' or 'dummy')
    
    Returns:
        RAGRetriever instance
    """
    if retriever_type == "faiss":
        return FAISSRetriever()
    elif retriever_type == "dummy":
        return DummyRetriever()
    else:
        raise ValueError(f"Unknown retriever type: {retriever_type}")

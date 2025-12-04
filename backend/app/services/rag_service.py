"""
RAG (Retrieval-Augmented Generation) Service for EchoMind.
Handles document retrieval, synthesis, and answer generation.
"""
from typing import List, Dict, Tuple, Optional
import os
from datetime import datetime
import numpy as np

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb

from app.core.config import settings
from app.models.schemas import (
    SynthesizedAnswer, SourceReference, ConfidenceLevel,
    SourceType
)
from loguru import logger


class RAGService:
    """Service for RAG-based information retrieval and synthesis."""
    
    def __init__(self):
        """Initialize RAG service with embedding model and vector store."""
        self.embedding_model_name = settings.EMBEDDING_MODEL
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
        self.top_k = settings.TOP_K_RESULTS
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {self.embedding_model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB
        self._init_vector_store()
        
        # Text splitter for document chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        logger.info("RAG Service initialized successfully")
    
    def _init_vector_store(self):
        """Initialize or load the ChromaDB vector store."""
        persist_dir = settings.CHROMA_PERSIST_DIR
        
        # Create directory if it doesn't exist
        os.makedirs(persist_dir, exist_ok=True)
        
        try:
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(path=persist_dir)
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"Vector store initialized with {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def ingest_document(
        self,
        document_text: str,
        source_name: str,
        source_type: SourceType,
        source_url: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Ingest a document into the vector store.
        
        Args:
            document_text: The text content to ingest
            source_name: Name of the source
            source_type: Type of source (university, government, etc.)
            source_url: Optional URL of the source
            metadata: Additional metadata
            
        Returns:
            Dictionary with ingestion results
        """
        try:
            # Split document into chunks
            chunks = self.text_splitter.split_text(document_text)
            
            logger.info(f"Split document into {len(chunks)} chunks")
            
            # Prepare metadata for each chunk
            chunk_metadatas = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    "source_name": source_name,
                    "source_type": source_type.value,
                    "source_url": source_url or "",
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "ingested_at": datetime.utcnow().isoformat(),
                    **(metadata or {})
                }
                chunk_metadatas.append(chunk_metadata)
            
            # Generate embeddings and add to collection
            embeddings = self.embeddings.embed_documents(chunks)
            
            # Generate unique IDs for each chunk
            base_id = f"{source_name}_{datetime.utcnow().timestamp()}"
            ids = [f"{base_id}_chunk_{i}" for i in range(len(chunks))]
            
            # Add to ChromaDB
            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=chunk_metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully ingested document: {source_name}")
            
            return {
                "status": "success",
                "source_name": source_name,
                "chunks_created": len(chunks),
                "document_ids": ids
            }
            
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def retrieve_relevant_documents(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve the most relevant documents for a query.
        
        Args:
            query: User's query text
            top_k: Number of documents to retrieve (default from settings)
            
        Returns:
            List of relevant documents with metadata and scores
        """
        try:
            k = top_k or self.top_k
            
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Process results
            relevant_docs = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    doc = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                    }
                    relevant_docs.append(doc)
            
            logger.info(f"Retrieved {len(relevant_docs)} relevant documents for query")
            return relevant_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def synthesize_answer(
        self,
        query: str,
        retrieved_docs: List[Dict]
    ) -> SynthesizedAnswer:
        """
        Synthesize an answer from retrieved documents.
        
        Args:
            query: User's original query
            retrieved_docs: List of retrieved relevant documents
            
        Returns:
            SynthesizedAnswer with synthesized response and citations
        """
        try:
            if not retrieved_docs:
                return self._create_no_info_response()
            
            # Calculate overall confidence based on relevance scores
            relevance_scores = [doc['relevance_score'] for doc in retrieved_docs]
            avg_confidence = np.mean(relevance_scores)
            
            # Determine confidence level
            if avg_confidence >= 0.8:
                confidence_level = ConfidenceLevel.HIGH
            elif avg_confidence >= 0.6:
                confidence_level = ConfidenceLevel.MEDIUM
            else:
                confidence_level = ConfidenceLevel.LOW
            
            # Extract unique sources
            sources = self._extract_sources(retrieved_docs)
            
            # Synthesize answer from multiple documents
            synthesized_text = self._synthesize_text(query, retrieved_docs)
            
            # Extract key points
            key_points = self._extract_key_points(retrieved_docs)
            
            # Generate related topics
            related_topics = self._generate_related_topics(retrieved_docs)
            
            return SynthesizedAnswer(
                answer=synthesized_text,
                confidence=confidence_level,
                confidence_score=float(avg_confidence),
                sources=sources,
                key_points=key_points,
                related_topics=related_topics
            )
            
        except Exception as e:
            logger.error(f"Error synthesizing answer: {e}")
            return self._create_error_response()
    
    def _synthesize_text(self, query: str, docs: List[Dict]) -> str:
        """
        Synthesize text from multiple documents.
        For production, this would use an LLM. For now, we do basic extraction.
        """
        # Combine relevant excerpts
        excerpts = []
        for doc in docs[:3]:  # Use top 3 documents
            content = doc['content']
            # Take first 200 characters as excerpt
            excerpt = content[:200] + "..." if len(content) > 200 else content
            excerpts.append(excerpt)
        
        # Create synthesized answer
        intro = f"Based on trusted mental wellness resources, here's what we found regarding your question:\n\n"
        body = "\n\n".join([f"• {excerpt}" for excerpt in excerpts])
        conclusion = "\n\nThese insights come from verified sources. For personalized guidance, please consult with a mental health professional."
        
        return intro + body + conclusion
    
    def _extract_sources(self, docs: List[Dict]) -> List[SourceReference]:
        """Extract unique source references from retrieved documents."""
        sources_dict = {}
        
        for doc in docs:
            metadata = doc['metadata']
            source_name = metadata.get('source_name', 'Unknown')
            
            if source_name not in sources_dict:
                sources_dict[source_name] = SourceReference(
                    source_id=source_name.replace(" ", "_").lower(),
                    source_name=source_name,
                    source_type=metadata.get('source_type', 'ngo'),
                    source_url=metadata.get('source_url'),
                    trust_score=metadata.get('trust_score', 0.8),
                    last_verified=datetime.fromisoformat(metadata.get('ingested_at', datetime.utcnow().isoformat())),
                    excerpt=doc['content'][:150] + "..." if len(doc['content']) > 150 else doc['content']
                )
        
        return list(sources_dict.values())
    
    def _extract_key_points(self, docs: List[Dict]) -> List[str]:
        """Extract key points from documents."""
        # Simple extraction - in production, use NLP
        key_points = []
        for doc in docs[:3]:
            sentences = doc['content'].split('.')
            if sentences:
                key_points.append(sentences[0].strip() + ".")
        
        return key_points[:5]  # Return top 5 key points
    
    def _generate_related_topics(self, docs: List[Dict]) -> List[str]:
        """Generate related topics for follow-up."""
        # Extract topics from metadata or content
        topics = set()
        for doc in docs:
            metadata = doc['metadata']
            if 'topics' in metadata:
                topics.update(metadata['topics'].split(','))
        
        # Default related topics if none found
        if not topics:
            topics = {"stress management", "counseling services", "self-care techniques"}
        
        return list(topics)[:5]
    
    def _create_no_info_response(self) -> SynthesizedAnswer:
        """Create response when no relevant information is found."""
        return SynthesizedAnswer(
            answer="I couldn't find specific information in our knowledge base for your query. However, I recommend speaking with a mental health professional who can provide personalized guidance.",
            confidence=ConfidenceLevel.LOW,
            confidence_score=0.0,
            sources=[],
            key_points=["Consider reaching out to a mental health professional", "Emergency hotlines are available 24/7"],
            related_topics=["professional counseling", "crisis support", "mental health resources"]
        )
    
    def _create_error_response(self) -> SynthesizedAnswer:
        """Create response for error cases."""
        return SynthesizedAnswer(
            answer="I encountered an issue processing your request. Please try rephrasing your question or contact support if the issue persists.",
            confidence=ConfidenceLevel.LOW,
            confidence_score=0.0,
            sources=[],
            key_points=[],
            related_topics=[]
        )
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector store collection."""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "status": "healthy" if count > 0 else "empty"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"status": "error", "error": str(e)}

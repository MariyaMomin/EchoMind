"""
RAG (Retrieval-Augmented Generation) Service for EchoMind.

This is a lightweight, in-memory implementation that avoids heavy ML/vector DB
dependencies so the project can run without native build tools.
"""
from typing import List, Dict, Optional
from datetime import datetime

from app.core.config import settings
from app.models.schemas import (
    SynthesizedAnswer,
    SourceReference,
    ConfidenceLevel,
    SourceType,
)
from loguru import logger


class RAGService:
    """Service for simple information retrieval and synthesis (no external DB)."""

    def __init__(self):
        """Initialize an in-memory store for ingested documents."""
        self.top_k = settings.TOP_K_RESULTS
        # Each entry is a dict with keys: content, metadata
        self._documents: List[Dict] = []
        logger.info("RAG Service initialized with in-memory store (no ChromaDB)")

    def ingest_document(
        self,
        document_text: str,
        source_name: str,
        source_type: SourceType,
        source_url: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Ingest a document into the in-memory store.

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
            # For simplicity, treat the whole text as a single "chunk"
            chunk_metadata = {
                "source_name": source_name,
                "source_type": source_type.value,
                "source_url": source_url or "",
                "chunk_index": 0,
                "total_chunks": 1,
                "ingested_at": datetime.utcnow().isoformat(),
                **(metadata or {}),
            }

            self._documents.append(
                {
                    "content": document_text,
                    "metadata": chunk_metadata,
                }
            )

            logger.info(f"Successfully ingested document: {source_name}")

            return {
                "status": "success",
                "source_name": source_name,
                "chunks_created": 1,
                "document_ids": [f"{source_name}_0"],
            }

        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    def retrieve_relevant_documents(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve the most relevant documents for a query using a simple
        keyword-overlap scoring (no embeddings/vector DB).

        Args:
            query: User's query text
            top_k: Number of documents to retrieve (default from settings)

        Returns:
            List of relevant documents with metadata and scores
        """
        try:
            k = top_k or self.top_k

            if not self._documents:
                logger.info("No documents available in in-memory store")
                return []

            query_terms = {t.lower() for t in query.split() if t.strip()}
            scored_docs: List[Dict] = []

            for doc in self._documents:
                content_terms = {t.lower() for t in doc["content"].split() if t.strip()}
                if not content_terms:
                    continue
                overlap = query_terms.intersection(content_terms)
                if not overlap:
                    score = 0.0
                else:
                    score = len(overlap) / len(query_terms or {1})

                scored_docs.append(
                    {
                        "content": doc["content"],
                        "metadata": doc["metadata"],
                        "distance": 1.0 - score,
                        "relevance_score": score,
                    }
                )

            # Sort by score descending and take top_k
            scored_docs.sort(key=lambda d: d["relevance_score"], reverse=True)
            relevant_docs = scored_docs[:k]

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
            avg_confidence = sum(relevance_scores) / len(relevance_scores)

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
        """Get statistics about the in-memory collection."""
        try:
            count = len(self._documents)
            return {
                "total_documents": count,
                "collection_name": settings.CHROMA_COLLECTION_NAME,
                "status": "healthy" if count > 0 else "empty",
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"status": "error", "error": str(e)}

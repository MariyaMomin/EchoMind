"""
EchoMind FastAPI Application
Main application entry point and API configuration.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import uuid

from app.core.config import settings
from app.models.schemas import (
    QueryRequest, QueryResponse, HealthCheckResponse,
    IngestDocumentRequest, UrgencyLevel, ResourceRecommendation
)
from app.services.rag_service import RAGService
from app.services.urgency_classifier import UrgencyClassifier
from loguru import logger

# Global service instances
rag_service: RAGService = None
urgency_classifier: UrgencyClassifier = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    global rag_service, urgency_classifier
    logger.info("Initializing EchoMind services...")
    
    try:
        rag_service = RAGService()
        urgency_classifier = UrgencyClassifier()
        logger.info("✓ All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down EchoMind services...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="RAG-powered Mental Wellness Resource Architect",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get RAG service
def get_rag_service() -> RAGService:
    """Dependency to inject RAG service."""
    return rag_service


# Dependency to get urgency classifier
def get_urgency_classifier() -> UrgencyClassifier:
    """Dependency to inject urgency classifier."""
    return urgency_classifier


# Health Check Endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint to verify service status."""
    try:
        # Check RAG service
        rag_stats = rag_service.get_collection_stats()
        rag_status = "healthy" if rag_stats.get("status") in ["healthy", "empty"] else "unhealthy"
        
        return HealthCheckResponse(
            status="healthy" if rag_status == "healthy" else "degraded",
            version="1.0.0",
            timestamp=datetime.utcnow(),
            services={
                "rag_service": rag_status,
                "urgency_classifier": "healthy",
                "vector_db": rag_stats.get("status", "unknown")
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            version="1.0.0",
            timestamp=datetime.utcnow(),
            services={
                "error": str(e)
            }
        )


# Main Query Endpoint
@app.post(f"{settings.API_V1_PREFIX}/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    rag: RAGService = Depends(get_rag_service),
    classifier: UrgencyClassifier = Depends(get_urgency_classifier)
):
    """
    Process a user query and return synthesized information with resources.
    
    This is the main endpoint for the EchoMind chatbot.
    """
    try:
        logger.info(f"Processing query: {request.query[:50]}...")
        
        # Generate response ID
        response_id = str(uuid.uuid4())
        
        # 1. Classify urgency level
        urgency_level, emergency_contacts = classifier.classify_urgency(request.query)
        logger.info(f"Urgency level: {urgency_level}")
        
        # 2. Retrieve relevant documents from vector store
        retrieved_docs = rag.retrieve_relevant_documents(request.query)
        logger.info(f"Retrieved {len(retrieved_docs)} relevant documents")
        
        # 3. Synthesize answer from retrieved documents
        synthesized_answer = rag.synthesize_answer(request.query, retrieved_docs)
        
        # 4. Generate resource recommendations (mock for now)
        recommended_resources = _generate_mock_resources(urgency_level, request.user_location)
        
        # 5. Generate next steps
        next_steps = _generate_next_steps(urgency_level)
        
        # Build response
        response = QueryResponse(
            response_id=response_id,
            session_id=request.session_id,
            urgency_level=urgency_level,
            emergency_contacts=emergency_contacts,
            synthesized_answer=synthesized_answer,
            recommended_resources=recommended_resources,
            next_steps=next_steps,
            timestamp=datetime.utcnow()
        )
        
        logger.info(f"Query processed successfully. Response ID: {response_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# Document Ingestion Endpoint
@app.post(f"{settings.API_V1_PREFIX}/ingest")
async def ingest_document(
    request: IngestDocumentRequest,
    rag: RAGService = Depends(get_rag_service)
):
    """
    Ingest a new document into the knowledge base.
    
    This endpoint allows administrators to add new trusted sources.
    """
    try:
        logger.info(f"Ingesting document: {request.source_name}")
        
        # Use provided text or fetch from URL
        document_text = request.document_text
        if not document_text and request.document_url:
            # In production, fetch content from URL
            raise HTTPException(status_code=400, detail="URL fetching not implemented yet. Please provide document_text.")
        
        # Ingest document
        result = rag.ingest_document(
            document_text=document_text,
            source_name=request.source_name,
            source_type=request.source_type,
            source_url=request.document_url,
            metadata=request.metadata
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=f"Error ingesting document: {str(e)}")


# Stats Endpoint
@app.get(f"{settings.API_V1_PREFIX}/stats")
async def get_stats(rag: RAGService = Depends(get_rag_service)):
    """Get statistics about the knowledge base."""
    try:
        stats = rag.get_collection_stats()
        return JSONResponse(content=stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper Functions
def _generate_mock_resources(urgency: UrgencyLevel, location: str = None) -> list:
    """Generate mock resource recommendations."""
    resources = []
    
    if urgency in [UrgencyLevel.CRITICAL, UrgencyLevel.HIGH]:
        resources.append(ResourceRecommendation(
            resource_id="crisis_hotline",
            name="24/7 Crisis Hotline",
            resource_type="hotline",
            description="Immediate crisis support available now",
            location="National",
            cost_range="Free",
            contact_info={"phone": "988"},
            trust_score=1.0,
            match_score=1.0
        ))
    
    resources.append(ResourceRecommendation(
        resource_id="university_counseling",
        name="University Counseling Center",
        resource_type="counselor",
        description="Professional counseling services for students",
        location=location or "Campus",
        cost_range="Free for students",
        contact_info={"website": "https://counseling.university.edu"},
        trust_score=0.95,
        match_score=0.9
    ))
    
    resources.append(ResourceRecommendation(
        resource_id="mental_health_app",
        name="Mindfulness & Meditation App",
        resource_type="self_help",
        description="Guided meditation and stress relief exercises",
        location="Online",
        cost_range="Free - $10/month",
        contact_info={"website": "https://example-app.com"},
        trust_score=0.85,
        match_score=0.75
    ))
    
    return resources


def _generate_next_steps(urgency: UrgencyLevel) -> list:
    """Generate actionable next steps based on urgency."""
    if urgency == UrgencyLevel.CRITICAL:
        return [
            "Call 988 immediately for crisis support",
            "Go to your nearest emergency room if you're in immediate danger",
            "Reach out to a trusted friend or family member",
            "Use the Crisis Text Line: Text HOME to 741741"
        ]
    elif urgency == UrgencyLevel.HIGH:
        return [
            "Contact a crisis hotline for immediate support",
            "Schedule an urgent appointment with a mental health professional",
            "Reach out to your support network",
            "Practice grounding techniques to manage acute distress"
        ]
    elif urgency == UrgencyLevel.MEDIUM:
        return [
            "Schedule an appointment with a counselor",
            "Explore self-help resources and coping strategies",
            "Connect with a support group",
            "Practice self-care activities"
        ]
    else:
        return [
            "Explore the recommended resources",
            "Learn more about mental wellness practices",
            "Consider preventive mental health support",
            "Build a self-care routine"
        ]


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )

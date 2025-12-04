"""
Pydantic models for API request and response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class UrgencyLevel(str, Enum):
    """Urgency classification levels."""
    CRITICAL = "critical"  # Immediate crisis
    HIGH = "high"          # Urgent need for support
    MEDIUM = "medium"      # Moderate concern
    LOW = "low"            # Informational query


class ConfidenceLevel(str, Enum):
    """Confidence levels for synthesized answers."""
    HIGH = "high"      # >= 0.8
    MEDIUM = "medium"  # 0.6 - 0.79
    LOW = "low"        # < 0.6


class SourceType(str, Enum):
    """Types of information sources."""
    UNIVERSITY = "university"
    GOVERNMENT = "government"
    NGO = "ngo"
    MEDICAL = "medical"
    VERIFIED_HOTLINE = "verified_hotline"


# Request Models
class QueryRequest(BaseModel):
    """User query request model."""
    query: str = Field(..., min_length=1, max_length=2000, description="User's mental wellness query")
    session_id: Optional[str] = Field(None, description="Session identifier for context tracking")
    user_location: Optional[str] = Field(None, description="User's location for localized resources")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User preferences (cost, insurance, etc.)")
    
    @validator('query')
    def query_not_empty(cls, v):
        """Ensure query is not just whitespace."""
        if not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()


class TriageRequest(BaseModel):
    """Triage assessment request."""
    responses: Dict[str, str] = Field(..., description="User responses to triage questions")
    location: Optional[str] = Field(None, description="User's geographic location")


class FeedbackRequest(BaseModel):
    """User feedback on response quality."""
    session_id: str
    response_id: str
    helpful: bool
    feedback_text: Optional[str] = None


# Response Models
class SourceReference(BaseModel):
    """Reference to an information source."""
    source_id: str
    source_name: str
    source_type: SourceType
    source_url: Optional[str] = None
    trust_score: float = Field(..., ge=0.0, le=1.0, description="Trust score (0-1)")
    last_verified: datetime
    excerpt: Optional[str] = Field(None, description="Relevant excerpt from source")


class EmergencyContact(BaseModel):
    """Emergency hotline information."""
    name: str
    phone: str
    description: str
    available_247: bool = True
    country: str


class SynthesizedAnswer(BaseModel):
    """RAG-synthesized answer with citations."""
    answer: str = Field(..., description="Synthesized answer text")
    confidence: ConfidenceLevel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    sources: List[SourceReference] = Field(default_factory=list, description="Source citations")
    key_points: List[str] = Field(default_factory=list, description="Key takeaways")
    related_topics: List[str] = Field(default_factory=list, description="Related topics for follow-up")


class ResourceRecommendation(BaseModel):
    """Personalized resource recommendation."""
    resource_id: str
    name: str
    resource_type: str  # e.g., "counselor", "support_group", "self_help"
    description: str
    location: Optional[str] = None
    cost_range: Optional[str] = None  # e.g., "Free", "$50-100/session", "Insurance accepted"
    contact_info: Optional[Dict[str, str]] = None
    trust_score: float = Field(..., ge=0.0, le=1.0)
    match_score: float = Field(..., ge=0.0, le=1.0, description="How well it matches user needs")


class QueryResponse(BaseModel):
    """Complete response to a user query."""
    response_id: str
    session_id: Optional[str] = None
    urgency_level: UrgencyLevel
    emergency_contacts: List[EmergencyContact] = Field(default_factory=list)
    synthesized_answer: Optional[SynthesizedAnswer] = None
    recommended_resources: List[ResourceRecommendation] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list, description="Actionable next steps")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TriageResult(BaseModel):
    """Results from triage assessment."""
    urgency_level: UrgencyLevel
    recommended_path: str
    filtered_resources: List[ResourceRecommendation]
    immediate_actions: List[str]


class HealthCheckResponse(BaseModel):
    """API health check response."""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, str]  # Service name -> status
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class IngestDocumentRequest(BaseModel):
    """Request to ingest a new document into the knowledge base."""
    document_url: Optional[str] = None
    document_text: Optional[str] = None
    source_name: str
    source_type: SourceType
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('document_url', 'document_text')
    def at_least_one_source(cls, v, values):
        """Ensure either URL or text is provided."""
        if not v and not values.get('document_text') and not values.get('document_url'):
            raise ValueError('Either document_url or document_text must be provided')
        return v

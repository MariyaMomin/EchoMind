"""
Configuration settings for EchoMind backend.
Uses Pydantic settings for environment variable management.
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "EchoMind - Mental Wellness Resource Architect"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/echomind"
    DB_POOL_SIZE: int = 10
    
    # Vector Database (ChromaDB)
    CHROMA_PERSIST_DIR: str = "../data/chromadb"
    CHROMA_COLLECTION_NAME: str = "wellness_resources"
    
    # AI Model Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt2"
    URGENCY_CLASSIFIER_PATH: str = "models/urgency_classifier.joblib"
    MAX_TOKENS: int = 512
    TEMPERATURE: float = 0.7
    
    # RAG Configuration
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    CONFIDENCE_THRESHOLD: float = 0.6
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Emergency Hotlines
    EMERGENCY_HOTLINE_US: str = "988"
    EMERGENCY_HOTLINE_INDIA: str = "9152987821"
    CRISIS_TEXT_LINE: str = "741741"
    
    # Data Sources
    TRUSTED_DOMAINS: str = ".edu,.gov,.org"
    SOURCE_UPDATE_INTERVAL_HOURS: int = 24
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/echomind.log"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def trusted_domains_list(self) -> List[str]:
        """Parse trusted domains into a list."""
        return [domain.strip() for domain in self.TRUSTED_DOMAINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

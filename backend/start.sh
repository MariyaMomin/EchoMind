#!/bin/bash
# Startup script for Render deployment

echo "Starting EchoMind Backend..."

# Create necessary directories
mkdir -p /opt/render/project/data/chromadb
mkdir -p logs

# Check if vector database is empty and ingest sample data
python -c "
from app.services.rag_service import RAGService
try:
    rag = RAGService()
    stats = rag.get_collection_stats()
    if stats.get('total_documents', 0) == 0:
        print('Vector database is empty. Ingesting sample data...')
        import sys
        sys.path.append('../data')
        from sample_ingest import ingest_sample_data
        ingest_sample_data()
except Exception as e:
    print(f'Note: {e}')
"

# Start the application
echo "Starting FastAPI server..."
python -m app.main

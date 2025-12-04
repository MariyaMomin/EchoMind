# 🧠 EchoMind - Mental Wellness Resource Architect

**EchoMind** is a RAG-powered AI platform that synthesizes fragmented mental wellness information into trustworthy, actionable support paths for individuals in need. Built to solve the "Information Fragmentation and Accessibility Gap" in youth mental wellness resources.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Problem Statement

**The Core Problem:** Information Fragmentation and Accessibility Gap

When a young person or their guardian seeks help for a mental health challenge, they face:
- **Fragmented Information**: Data spread across university sites, government pages, private blogs, and hotlines
- **Unverified Sources**: Difficulty distinguishing trustworthy information
- **Accessibility Barriers**: Complex medical jargon and lengthy documents
- **Time-Critical Delays**: Hours spent navigating chaos when immediate help is needed

**EchoMind Solution:** A single, trustworthy, synthesized source that guides users from initial concern to actionable next steps using AI-powered RAG (Retrieval-Augmented Generation).

---

## ✨ Key Features

### 🤖 AI-Powered RAG Pipeline
- **Semantic Search**: Vector-based document retrieval using sentence transformers
- **Information Synthesis**: Combines multiple trusted sources into coherent answers
- **Confidence Scoring**: Transparent confidence levels for all synthesized responses
- **Source Citations**: Every answer links back to verified institutional documents

### 🚨 Crisis Detection & Support
- **Urgency Classification**: Real-time detection of crisis keywords
- **Emergency Overlay**: Immediate display of crisis hotlines for critical situations
- **Risk Assessment**: Multi-level urgency triage (Critical, High, Medium, Low)
- **24/7 Hotline Integration**: Direct access to national crisis resources

### 💬 Conversational Interface
- **Mobile-First Design**: Responsive chatbot UI built with React
- **Personalized Triage**: Guided decision tree for filtering resources
- **Resource Recommendations**: Localized, cost-aware resource matching
- **Actionable Next Steps**: Clear, prioritized guidance based on urgency

### 🔒 Privacy & Security
- **Confidential**: No personal health information stored
- **Session-Based**: Temporary session IDs for context tracking
- **Data Minimization**: Only essential data processed
- **Secure API**: CORS-protected endpoints

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│              React + Tailwind CSS (Mobile-First)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓ REST API
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                               │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Query      │  │   Urgency    │  │   Resource         │   │
│  │   Endpoint   │  │   Classifier │  │   Recommender      │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬───────────┘   │
│         │                  │                    │                │
│         └──────────────────┴────────────────────┘                │
│                           │                                      │
│                           ↓                                      │
│                   ┌───────────────┐                             │
│                   │  RAG Service  │                             │
│                   └───────┬───────┘                             │
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                  │
│         ↓                 ↓                 ↓                    │
│  ┌──────────┐      ┌──────────┐     ┌───────────┐             │
│  │ ChromaDB │      │Embedding │     │  NLP/LLM  │             │
│  │ (Vector) │      │  Model   │     │ Synthesis │             │
│  └──────────┘      └──────────┘     └───────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

#### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Vector Database**: ChromaDB for document embeddings
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **NLP**: SpaCy, NLTK for text processing
- **Database**: PostgreSQL (optional for user analytics)

#### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios

#### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Deployment**: Nginx (frontend), Uvicorn (backend)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)

### Option 1: Local Development

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/echomind.git
cd echomind
```

#### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
```

#### 3. Ingest Sample Data
```bash
# From the backend directory
cd ../data
python sample_ingest.py
```

#### 4. Start Backend Server
```bash
cd ../backend
python -m app.main
```
Backend will run at: http://localhost:8000

#### 5. Setup Frontend
```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend will run at: http://localhost:3000

### Option 2: Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 📊 Project Structure

```
echomind/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── api/                  # API endpoints
│   │   ├── core/                 # Configuration
│   │   │   └── config.py         # Settings management
│   │   ├── models/               # Pydantic schemas
│   │   │   └── schemas.py        # Request/Response models
│   │   ├── services/             # Business logic
│   │   │   ├── rag_service.py    # RAG pipeline
│   │   │   └── urgency_classifier.py  # Crisis detection
│   │   ├── utils/                # Utilities
│   │   └── main.py               # Application entry point
│   ├── models/                   # ML model storage
│   ├── logs/                     # Application logs
│   ├── Dockerfile                # Backend container config
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment template
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.jsx          # Main chat interface
│   │   │   ├── EmergencyBanner.jsx  # Crisis alert banner
│   │   │   ├── MessageBubble.jsx    # Message display
│   │   │   └── ResourceCard.jsx     # Resource cards
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   ├── App.jsx               # Main app component
│   │   └── main.jsx              # Entry point
│   ├── public/                   # Static assets
│   ├── Dockerfile                # Frontend container config
│   ├── package.json              # Node dependencies
│   └── tailwind.config.js        # Tailwind configuration
│
├── data/                         # Data storage
│   ├── chromadb/                 # Vector database
│   └── sample_ingest.py          # Data ingestion script
│
├── docs/                         # Documentation
├── docker-compose.yml            # Multi-container config
└── README.md                     # This file
```

---

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development

# Vector Database
CHROMA_PERSIST_DIR=../data/chromadb
CHROMA_COLLECTION_NAME=wellness_resources

# AI Models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_TOKENS=512

# RAG Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=5

# Emergency Hotlines
EMERGENCY_HOTLINE_US=988
EMERGENCY_HOTLINE_INDIA=9152987821

# Security
SECRET_KEY=your-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
VITE_API_URL=http://localhost:8000
```

---

## 📖 API Documentation

### Main Endpoints

#### POST `/api/v1/query`
Process a user query and return synthesized information.

**Request:**
```json
{
  "query": "I'm feeling anxious about exams",
  "session_id": "session_123",
  "user_location": "New York",
  "preferences": {}
}
```

**Response:**
```json
{
  "response_id": "uuid",
  "urgency_level": "medium",
  "emergency_contacts": [],
  "synthesized_answer": {
    "answer": "Based on trusted resources...",
    "confidence": "high",
    "confidence_score": 0.85,
    "sources": [...],
    "key_points": [...],
    "related_topics": [...]
  },
  "recommended_resources": [...],
  "next_steps": [...]
}
```

#### POST `/api/v1/ingest`
Ingest a new document (admin endpoint).

#### GET `/health`
Health check endpoint.

#### GET `/api/v1/stats`
Get knowledge base statistics.

**Interactive API Docs:** http://localhost:8000/docs

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Manual Testing Flow
1. Start backend: `python -m app.main`
2. Ingest sample data: `python data/sample_ingest.py`
3. Start frontend: `npm run dev`
4. Test queries:
   - Low urgency: "What are stress management techniques?"
   - Medium urgency: "I'm feeling anxious"
   - High urgency: "I'm having a panic attack"
   - Critical: "I'm thinking about suicide"

---

## 🎨 Features Demo

### 1. Crisis Detection
```
User: "I feel hopeless and want to end it all"
→ System detects CRITICAL urgency
→ Emergency banner displays with hotlines
→ Immediate crisis resources provided
```

### 2. RAG-Powered Answers
```
User: "What helps with anxiety?"
→ Retrieves relevant documents from vector DB
→ Synthesizes answer from multiple sources
→ Displays confidence score and citations
→ Recommends personalized resources
```

### 3. Resource Recommendations
```
Filters based on:
- Urgency level
- User location
- Cost preferences
- Service type
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📊 Performance Metrics

- **Query Response Time**: < 2 seconds
- **Embedding Generation**: ~100ms per document
- **Vector Search**: ~50ms for top-5 results
- **Confidence Threshold**: 0.6 (customizable)

---

## 🛣️ Roadmap

### Phase 1: Core Functionality ✅
- [x] RAG pipeline with ChromaDB
- [x] Urgency classification
- [x] React chatbot UI
- [x] Emergency banner system

### Phase 2: Enhanced Features 🚧
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Session persistence with user profiles
- [ ] Advanced NLP (BERT fine-tuning)
- [ ] Geolocation-based resource filtering

### Phase 3: Scale & Deploy 📈
- [ ] Production deployment (AWS/GCP)
- [ ] Load testing and optimization
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IIT Nagpur Claude Solve-A-Thon**: Initial consensus mapping research
- **National Institute of Mental Health (NIMH)**: Mental health resources
- **988 Suicide & Crisis Lifeline**: Crisis support framework
- **Open Source Community**: For amazing tools (FastAPI, React, ChromaDB)

---

## ⚠️ Disclaimer

**EchoMind is not a substitute for professional mental health care.** 

If you're experiencing a mental health crisis, please:
- **Call 988** (US Suicide & Crisis Lifeline)
- **Text HOME to 741741** (Crisis Text Line)
- **Visit your nearest emergency room**
- **Contact a mental health professional**

This platform provides information and resource recommendations only. Always consult with qualified healthcare providers for diagnosis and treatment.

---

## 📧 Contact

- **Project Lead**: [Your Name]
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🌟 Star this Repository

If you find EchoMind helpful, please ⭐ star this repository to show your support!

---

**Made with ❤️ for mental wellness accessibility**

# ⚡ EchoMind - Quick Start Guide

Get EchoMind running in 5 minutes!

## Prerequisites
- Python 3.10+ installed
- Node.js 18+ installed
- Git installed

## Step-by-Step Setup

### 1. Open Terminal/PowerShell
Navigate to your projects directory:
```powershell
cd C:\Users\Mariya\Documents\dev\echomind
```

### 2. Setup Backend

#### Create Virtual Environment (Windows PowerShell)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Install Python Dependencies
```powershell
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### Copy Environment File
```powershell
Copy-Item .env.example .env
```

### 3. Ingest Sample Data
```powershell
cd ..\data
python sample_ingest.py
```

You should see:
```
Initializing RAG Service...
Ingesting 4 sample documents...

[1/4] Ingesting: University Mental Health Guide
    ✓ Success! Created X chunks
...
Ingestion Complete!
```

### 4. Start Backend Server
Open a **new terminal** window:
```powershell
cd C:\Users\Mariya\Documents\dev\echomind\backend
.\venv\Scripts\Activate.ps1
python -m app.main
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is now running at http://localhost:8000

### 5. Setup Frontend
Open **another new terminal** window:
```powershell
cd C:\Users\Mariya\Documents\dev\echomind\frontend
npm install
```

### 6. Start Frontend Server
```powershell
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

✅ Frontend is now running at http://localhost:3000

## 🎉 You're Ready!

Open your browser and go to: **http://localhost:3000**

### Test Queries to Try:

1. **Low Urgency** (Informational)
   - "What are some stress management techniques?"
   - "How do I know if I need therapy?"

2. **Medium Urgency** (General concern)
   - "I'm feeling anxious about exams"
   - "I've been feeling sad lately"

3. **High Urgency** (Acute distress)
   - "I'm having a panic attack"
   - "I feel overwhelmed and desperate"

4. **Critical** (Crisis detection)
   - "I'm thinking about suicide"
   - "I want to hurt myself"

## Verify Installation

### Check Backend API
Open http://localhost:8000/docs in your browser to see the interactive API documentation.

### Check Health
```powershell
curl http://localhost:8000/health
```

### Check Stats
```powershell
curl http://localhost:8000/api/v1/stats
```

## Troubleshooting

### Backend won't start?
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Verify all dependencies installed: `pip list`

### Frontend won't start?
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is already in use
- Verify Node.js version: `node --version` (should be 18+)

### No data in responses?
- Run the data ingestion script again: `python data/sample_ingest.py`
- Check backend logs for errors

### ChromaDB errors?
- Delete the `data/chromadb` folder
- Run data ingestion again

## Next Steps

1. **Explore the UI**: Try different types of queries
2. **Review the Code**: Check out `backend/app/main.py` and `frontend/src/components/Chat.jsx`
3. **Add More Data**: Modify `data/sample_ingest.py` to add your own mental wellness resources
4. **Customize**: Edit `.env` files to change configuration
5. **Deploy**: Use Docker for easy deployment (see README.md)

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 💬 Check API docs at http://localhost:8000/docs

---

**Happy Building! 🚀**

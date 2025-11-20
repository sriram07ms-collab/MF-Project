# 🚀 Quick Start Guide

Get the Facts-Only MF Assistant running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- Google Gemini API key ([Get free one here](https://makersuite.google.com/app/apikey)) - for answer generation (free tier)
- (Optional) Fast internet for downloading Hugging Face embedding model on first run

## Step-by-Step

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy the example and add your API key
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Mac/Linux

# Edit .env and add:
# GEMINI_API_KEY=your-gemini-key-here (for answer generation - free tier)
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2  # optional override

# Run data ingestion (scrapes fund pages)
python scripts/ingest_data.py

# Start backend server
uvicorn main:app --reload --port 8000
```

✅ Backend running at `http://localhost:8000`

### 2. Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
echo NEXT_PUBLIC_API_BASE=http://localhost:8000 > .env.local

# Start development server
npm run dev
```

✅ Frontend running at `http://localhost:3000`

### 3. Test It!

1. Open browser: `http://localhost:3000`
2. Click an example question or type:
   - "What's the exit load on Nippon India Large Cap Fund?"
   - "What is the minimum SIP amount?"
   - "How to download capital gains statement?"

3. Verify you get answers with source links! 🎉

## Troubleshooting

### ❌ "Vector store not loaded"
**Fix:** Run `python scripts/ingest_data.py` in the backend directory

### ❌ "GEMINI_API_KEY not set"
**Fix:** Create `.env` file in `backend/` with `GEMINI_API_KEY=your-gemini-key-here` (optional but recommended for better answers). Embeddings run locally and do not need an API key.

### ❌ Frontend can't connect
**Fix:** 
- Check backend is running on port 8000
- Verify `NEXT_PUBLIC_API_BASE` in `frontend/.env.local`

### ❌ No answers returned
**Fix:**
- Check backend logs for errors
- Verify data ingestion completed
- Ensure the Hugging Face embedding model finished downloading (rerun ingestion if interrupted)

## What's Next?

- See `SETUP.md` for detailed setup
- See `DEPLOYMENT.md` for production deployment
- Customize UI colors in `frontend/tailwind.config.js`

## Need Help?

Check the logs:
- Backend: Look at terminal 1
- Frontend: Look at terminal 2
- Browser: Open Developer Console (F12)

---

**Happy coding! 🎯**



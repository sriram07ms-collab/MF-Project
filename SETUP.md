# Quick Setup Guide

Follow these steps to get the Facts-Only MF Assistant running locally.

## Step 1: Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Add optional API keys/settings:
# GEMINI_API_KEY=your_gemini_key (for answer generation - free tier)
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2  # optional override
# Get Gemini key: https://makersuite.google.com/app/apikey

# Run data ingestion (scrapes fund pages and creates vector store)
python scripts/ingest_data.py

# Start backend server
uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

## Step 2: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Step 3: Test

1. Open `http://localhost:3000` in your browser
2. Try asking: "What's the exit load on Nippon India Large Cap Fund?"
3. Verify you get an answer with a source link

## Troubleshooting

### "Vector store not loaded"
- Make sure you ran `python scripts/ingest_data.py` in the backend directory
- Check that `backend/data/faiss_index` directory exists

### "GEMINI_API_KEY not set"
- Create `.env` file in `backend/` directory
- Add `GEMINI_API_KEY=your-gemini-key-here` (optional but recommended for better answers)
- Embeddings run locally via Hugging Face models (no key required). The first run will download the model weights.

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_BASE` in `frontend/.env.local`

### No answers returned
- Check backend logs for errors
- Verify data ingestion completed successfully
- Ensure the Hugging Face model finished downloading (rerun if network interrupted)

## Next Steps

- See `DEPLOYMENT.md` for production deployment
- Customize fund URLs in `backend/scripts/ingest_data.py`
- Adjust UI colors in `frontend/tailwind.config.js`



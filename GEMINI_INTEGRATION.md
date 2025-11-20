# Google Gemini Integration

The Facts-Only MF Assistant now uses **Google Gemini (free tier)** for intelligent answer generation!

## What Changed?

- **Before**: Rule-based extraction with regex patterns
- **Now**: Google Gemini LLM generates natural, context-aware answers from retrieved documents

## Benefits

✅ **Free Tier**: Generous free usage limits  
✅ **Better Answers**: LLM-generated responses are more natural and context-aware  
✅ **Fast**: Using `gemini-1.5-flash` for quick responses  
✅ **Fallback**: System still works if Gemini API is unavailable (uses rule-based extraction)

## Setup

### 1. Get Your Free Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 2. Add to Environment Variables

In your `backend/.env` file, add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Install Dependencies

The `google-generativeai` package is already in `requirements.txt`. Just run:

```bash
cd backend
pip install -r requirements.txt
```

### 4. Restart Backend

Restart your backend server to load the new configuration:

```bash
uvicorn main:app --reload --port 8000
```

## How It Works

1. **User asks a question** → Query is embedded using a local Hugging Face sentence-transformer
2. **Vector search** → FAISS finds relevant documents
3. **Gemini generates answer** → LLM creates concise, factual response from context
4. **Fallback** → If Gemini unavailable, uses rule-based extraction

## Model Options

The system uses `gemini-1.5-flash` by default (fastest, free tier).

To switch to `gemini-pro` (better quality, also free tier), edit `backend/services/rag_service.py`:

```python
# Change this line:
self.llm = genai.GenerativeModel('gemini-1.5-flash')

# To:
self.llm = genai.GenerativeModel('gemini-pro')
```

## Troubleshooting

### "GEMINI_API_KEY not set"
- Add the key to your `.env` file
- Restart the backend server

### "Error calling Gemini API"
- Check your API key is valid
- Verify you have internet connection
- System will automatically fall back to rule-based extraction

### Answers not improving
- Make sure Gemini is initialized (check backend logs for "Gemini LLM initialized successfully")
- Verify the API key is correct
- Check Gemini API status: https://status.google.com/

## Cost

**Free Tier Limits:**
- 15 requests per minute (RPM)
- 1,500 requests per day (RPD)
- More than enough for development and small-scale production!

For higher limits, see: https://ai.google.dev/pricing

## Architecture

```
User Question
    ↓
Hugging Face Embeddings (sentence-transformers/all-MiniLM-L6-v2)
    ↓
FAISS Vector Search
    ↓
Retrieve Top 3 Documents
    ↓
Google Gemini (gemini-1.5-flash)
    ↓
Generate Answer (max 3 sentences)
    ↓
Return with Source Citation
```

---

**Note**: The system gracefully falls back to rule-based extraction if Gemini is unavailable, ensuring reliability.



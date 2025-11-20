# Facts-Only MF Assistant

A RAG-based chatbot that answers factual questions about Nippon India Mutual Fund schemes using verified sources from AMC websites. Provides concise, citation-backed responses while strictly avoiding any investment advice.

## Features

- ✅ Answers factual queries only (expense ratio, exit load, minimum SIP, lock-in, riskometer, benchmark, statement downloads)
- ✅ Shows one clear citation link in every answer
- ✅ Refuses opinionated/portfolio questions with polite, facts-only message
- ✅ No PII collection (no PAN, Aadhaar, account numbers, OTPs, emails, phone numbers)
- ✅ No performance claims or return calculations
- ✅ Clean, Groww-inspired UI design

## Project Structure

```
MF-Testing-Project/
├── backend/          # FastAPI RAG service
├── frontend/         # Next.js chatbot UI
├── docker-compose.yml
└── README.md
```

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI
- LangChain
- FAISS (vector store)
- Google Gemini (free tier) - for answer generation
- Hugging Face sentence-transformers - for semantic search
- BeautifulSoup4 (web scraping)

**Frontend:**
- Next.js 14
- TypeScript
- Tailwind CSS
- React

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with API keys:
# GEMINI_API_KEY=your_key (for answer generation - get free key: https://makersuite.google.com/app/apikey)
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2  # optional override

python scripts/ingest_data.py
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions.

## Important Notes

- **Facts-only**: This assistant provides factual information only. No investment advice.
- **Source Links**: Every answer includes a citation to the official AMC page.
- **No PII**: The system does not collect or store any personal information.

## License

MIT

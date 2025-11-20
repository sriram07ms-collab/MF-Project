"""
FastAPI backend for Facts-Only MF Assistant
Provides RAG-based query service for mutual fund facts
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from datetime import datetime

from .services.rag_service import RAGService
from .services.query_validator import QueryValidator

load_dotenv()

app = FastAPI(
    title="Facts-Only MF Assistant API",
    description="RAG-based chatbot for mutual fund factual queries",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
rag_service = RAGService()
query_validator = QueryValidator()

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    context: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    source: str
    lastUpdated: str
    isRefusal: bool = False
    educationalLink: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    vectorStoreLoaded: bool

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "vectorStoreLoaded": rag_service.is_ready()
    }

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Main query endpoint for factual MF questions
    Returns answer with citation or refusal message
    """
    try:
        # Validate query
        validation_result = query_validator.validate(request.question)
        
        if not validation_result["is_valid"]:
            return QueryResponse(
                answer=validation_result["message"],
                source="",
                lastUpdated=os.getenv("LAST_UPDATED", "2025-11-18"),
                isRefusal=True,
                educationalLink=validation_result.get("educational_link")
            )
        
        # Process query through RAG
        result = rag_service.query(request.question)
        
        return QueryResponse(
            answer=result["answer"],
            source=result["source"],
            lastUpdated=os.getenv("LAST_UPDATED", "2025-11-18"),
            isRefusal=False
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/admin/reindex")
async def reindex():
    """
    Reindexing is not supported in the serverless deployment.
    """
    raise HTTPException(
        status_code=501,
        detail="Reindexing is disabled in the serverless deployment. "
               "Update the FAISS artifacts offline and redeploy.",
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




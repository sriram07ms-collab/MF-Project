@echo off
echo ====================================
echo Starting Backend Server
echo ====================================
cd backend

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check for .env file
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy ENV_TEMPLATE.txt .env
    echo.
    echo ====================================
    echo OPTIONAL: Add your GEMINI_API_KEY to backend\.env for answer quality
    echo ====================================
    echo GEMINI_API_KEY=your_key_here
    echo EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
    echo.
    echo Note: Embeddings run locally via Hugging Face models (download on first run)
    echo.
    echo Press any key after updating backend\.env...
    pause > nul
)

REM Check if vector store exists
if not exist data\faiss_index (
    echo.
    echo Running data ingestion (this may take a few minutes)...
    python scripts/ingest_data.py
    echo.
)

REM Start server
echo.
echo Starting backend server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
uvicorn main:app --reload --port 8000
pause



# Deployment Guide

This guide covers deploying the Facts-Only MF Assistant to production.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (for containerized deployment)
- Domain/Server for hosting
- (Optional) Google Gemini API key for answer generation

## Local Development Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add optional settings (e.g., GEMINI_API_KEY)

# Run data ingestion
python scripts/ingest_data.py

# Start server
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Visit `http://localhost:3000`

## Docker Deployment

### Using Docker Compose

1. **Create `.env` file in project root:**

```env
GEMINI_API_KEY=your_gemini_api_key_here
SOURCE_ALLOWED_DOMAINS=mf.nipponindiaim.com,www.sebi.gov.in,www.amfiindia.com
LAST_UPDATED=2025-11-18
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

2. **Build and run:**

```bash
docker-compose up -d
```

3. **Run data ingestion (first time):**

```bash
docker-compose exec backend python scripts/ingest_data.py
```

4. **Check logs:**

```bash
docker-compose logs -f
```

## Production Deployment

### Option 1: Azure App Service (Backend) + Vercel (Frontend)

#### Backend on Azure App Service

1. **Create Azure App Service:**
   ```bash
   az webapp create --resource-group <rg-name> --plan <plan-name> --name <app-name> --runtime "PYTHON:3.11"
   ```

2. **Configure environment variables:**
   ```bash
   az webapp config appsettings set --resource-group <rg-name> --name <app-name> --settings \
     GEMINI_API_KEY=<your-key> \
     SOURCE_ALLOWED_DOMAINS=mf.nipponindiaim.com,www.sebi.gov.in,www.amfiindia.com \
     LAST_UPDATED=2025-11-18
   ```

3. **Deploy:**
   ```bash
   cd backend
   az webapp up --resource-group <rg-name> --name <app-name>
   ```

4. **Run ingestion (SSH into container):**
   ```bash
   az webapp ssh --resource-group <rg-name> --name <app-name>
   python scripts/ingest_data.py
   ```

#### Frontend on Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

3. **Set environment variable:**
   - Go to Vercel dashboard → Project Settings → Environment Variables
   - Add `NEXT_PUBLIC_API_BASE` pointing to your Azure backend URL

### Option 2: Render.com (Full Stack)

1. **Create Web Service for Backend:**
   - Connect GitHub repo
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables

2. **Create Web Service for Frontend:**
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm start`
   - Add `NEXT_PUBLIC_API_BASE` environment variable

### Option 3: AWS (EC2 + S3)

1. **Launch EC2 instance** (Ubuntu 22.04)
2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip nginx
   ```

3. **Clone and setup backend:**
   ```bash
   git clone <repo>
   cd MF-Testing-Project/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python scripts/ingest_data.py
   ```

4. **Setup systemd service:**
   Create `/etc/systemd/system/mf-assistant.service`:
   ```ini
   [Unit]
   Description=MF Assistant Backend
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/MF-Testing-Project/backend
   Environment="PATH=/home/ubuntu/MF-Testing-Project/backend/venv/bin"
   ExecStart=/home/ubuntu/MF-Testing-Project/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. **Deploy frontend to S3 + CloudFront:**
   ```bash
   cd frontend
   npm run build
   aws s3 sync out/ s3://your-bucket-name
   ```

## Environment Variables

### Backend (.env)

```env
GEMINI_API_KEY=sk-...
SOURCE_ALLOWED_DOMAINS=mf.nipponindiaim.com,www.sebi.gov.in,www.amfiindia.com
DATABASE_PATH=./data/mf_assistant.db
VECTOR_STORE_PATH=./data/faiss_index
LAST_UPDATED=2025-11-18
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_BASE=https://your-backend-url.com
```

## Data Ingestion Updates

To update the vector store with latest fund information:

```bash
# Local
cd backend
python scripts/ingest_data.py

# Docker
docker-compose exec backend python scripts/ingest_data.py

# Production (Azure)
az webapp ssh --resource-group <rg> --name <app>
python scripts/ingest_data.py
```

**Recommended:** Set up a cron job or GitHub Action to run ingestion weekly.

## Monitoring & Health Checks

- **Health endpoint:** `GET /health`
- **Monitor:** Set up uptime monitoring (e.g., UptimeRobot, Healthchecks.io)
- **Logs:** Check application logs for errors

## Security Checklist

- ✅ HTTPS enabled
- ✅ CORS configured for frontend domain only
- ✅ Environment variables secured (use Key Vault/Secrets Manager)
- ✅ No PII collection
- ✅ Rate limiting (add if needed)
- ✅ Input validation on all endpoints

## Troubleshooting

### Backend not starting
- Verify vector store exists (run ingestion)
- Ensure Hugging Face model downloaded successfully (rerun if needed)
- Check port 8000 is available

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_BASE` is correct
- Check CORS settings in backend
- Ensure backend is running

### No answers returned
- Run data ingestion: `python scripts/ingest_data.py`
- Check vector store path in .env
- Confirm the Hugging Face embedding model is available (rerun ingestion if download failed)

## Support

For issues, check:
1. Application logs
2. Health endpoint status
3. Vector store exists and is loaded
4. Environment variables are set correctly




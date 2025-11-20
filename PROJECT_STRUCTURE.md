# Project Structure

```
MF-Testing-Project/
├── backend/                    # FastAPI backend service
│   ├── services/              # Core business logic
│   │   ├── __init__.py
│   │   ├── rag_service.py     # RAG query processing
│   │   └── query_validator.py # Query validation & refusal logic
│   ├── scripts/               # Utility scripts
│   │   ├── __init__.py
│   │   ├── ingest_data.py     # Data scraping & indexing
│   │   └── setup.sh           # Setup script
│   ├── data/                  # Data storage (gitignored)
│   │   ├── faiss_index/       # Vector store
│   │   └── mf_assistant.db    # Metadata database
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend container
│   └── .env.example           # Environment variables template
│
├── frontend/                   # Next.js frontend
│   ├── app/                   # Next.js 14 app directory
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   ├── globals.css        # Global styles
│   │   └── not-found.tsx      # 404 page
│   ├── components/            # React components
│   │   ├── ChatInterface.tsx  # Main chat UI
│   │   ├── ChatInput.tsx      # Input component
│   │   ├── MessageBubble.tsx  # Message display
│   │   └── WelcomeCard.tsx    # Welcome section
│   ├── lib/                   # Utilities
│   │   └── api.ts             # API client
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── tailwind.config.js     # Tailwind CSS config
│   ├── next.config.js         # Next.js config
│   ├── Dockerfile             # Frontend container
│   └── .env.example           # Environment variables template
│
├── .github/
│   └── workflows/
│       └── update-data.yml    # Automated data updates
│
├── docker-compose.yml         # Docker Compose config
├── .gitignore                 # Git ignore rules
├── README.md                  # Main documentation
├── SETUP.md                   # Quick setup guide
├── DEPLOYMENT.md              # Deployment instructions
└── PROJECT_STRUCTURE.md       # This file
```

## Key Files Explained

### Backend

- **main.py**: FastAPI application with `/query` and `/health` endpoints
- **services/rag_service.py**: Handles vector search and answer generation
- **services/query_validator.py**: Validates queries and refuses investment advice
- **scripts/ingest_data.py**: Scrapes fund pages and creates vector embeddings

### Frontend

- **app/page.tsx**: Main landing page with chat interface
- **components/ChatInterface.tsx**: Manages chat state and API calls
- **components/MessageBubble.tsx**: Displays messages with source links
- **lib/api.ts**: API client for backend communication

### Configuration

- **docker-compose.yml**: Orchestrates backend and frontend containers
- **.env.example**: Template for environment variables
- **requirements.txt**: Python dependencies
- **package.json**: Node.js dependencies




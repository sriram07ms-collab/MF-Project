from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .rag_service import rag_service
from .schemas import QueryRequest, QueryResponse, ReindexResponse


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup_event() -> None:
        try:
            rag_service.load_index()
        except FileNotFoundError:
            # Defer ingestion to manual step; surface friendly error later.
            pass

    @app.get("/health")
    async def health_check() -> dict:
        return {"status": "ok"}

    @app.post("/query", response_model=QueryResponse)
    async def query(request: QueryRequest) -> QueryResponse:
        try:
            return rag_service.answer(request.question)
        except FileNotFoundError:
            raise HTTPException(
                status_code=503,
                detail="Vector store missing. Please run ingestion first.",
            )

    @app.post("/admin/reindex", response_model=ReindexResponse)
    async def reindex() -> ReindexResponse:
        from .ingest import run_ingestion

        run_ingestion()
        return ReindexResponse(
            documents_indexed=len(rag_service._documents),
            message="Re-index completed.",
        )

    return app


app = create_app()



import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.config import settings
from backend.database import init_db, get_db_connection
from backend.services.retrieval_service import RetrievalService

# Routers
from backend.api.dashboard import router as dashboard_router
from backend.api.documents import router as documents_router, seed_sample_documents
from backend.api.research import router as research_router
from backend.api.comparison import router as comparison_router
from backend.api.reports import router as reports_router
from backend.api.settings import router as settings_router
from backend.api.evaluation import router as evaluation_router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize SQLite database, load FAISS index, and auto-seed sample papers."""
    init_db()
    RetrievalService.load_index()

    # If documents table is empty, auto-seed the sample academic papers
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    conn.close()

    if doc_count == 0:
        try:
            print("[ResearchIQ] Initial startup detected: Seeding 3 sample academic papers...")
            seed_sample_documents()
            print("[ResearchIQ] Sample papers successfully seeded and indexed.")
        except Exception as e:
            print(f"[ResearchIQ] Note: Sample seeding skipped or failed: {e}")
    yield

app = FastAPI(
    title="ResearchIQ: Multi-Document Research Assistant",
    description="Evidence-Grounded RAG Platform with Hybrid Retrieval, Contradiction Detection, and Executive Brief Synthesis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api
app.include_router(dashboard_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(research_router, prefix="/api")
app.include_router(comparison_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(settings_router, prefix="/api")
app.include_router(evaluation_router, prefix="/api")

@app.get("/api/health", tags=["Health"])
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "ResearchIQ",
        "version": "1.0.0",
        "llm_configured": bool(settings.GROQ_API_KEY),
        "embedding_model": settings.EMBEDDING_MODEL_NAME
    }

# Frontend Single Page Application (SPA) Serving
FRONTEND_DIST = settings.BASE_DIR / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Don't intercept API routes or docs
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return JSONResponse(status_code=404, content={"detail": "Not found"})
        
        target_file = FRONTEND_DIST / full_path
        if target_file.is_file():
            return FileResponse(target_file)
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    @app.get("/")
    def dev_index():
        return {
            "message": "ResearchIQ API is running.",
            "docs": "/docs",
            "frontend_status": "Vite frontend not built yet. Run 'npm run build' in frontend directory."
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)

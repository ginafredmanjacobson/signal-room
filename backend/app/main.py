from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router
from app.db.database import init_db

# Initialize database
init_db()

app = FastAPI(title=settings.APP_NAME)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # your actual Vercel frontend URL
  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "SignalRoom API is running"}

@app.get("/ping")
def ping():
    return {"status": "ok"}
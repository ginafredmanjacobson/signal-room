from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.ingest_reddit import fetch_reddit_posts, store_reddit_posts
from app.services.ingest_rss import fetch_rss_feeds, store_rss_entries
from app.core.config import settings

router = APIRouter()

@router.post("/run")
async def run_ingestion(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Trigger ingestion from all sources."""
    # Reddit - default subreddits (you can make this configurable)
    subreddits = ["technology", "futurology", "marketing"]
    
    # RSS feeds from env
    rss_feeds = [f.strip() for f in settings.RSS_FEEDS.split(",") if f.strip()]
    
    background_tasks.add_task(ingest_all, db, subreddits, rss_feeds)
    return {"message": "Ingestion started in background"}

def ingest_all(db: Session, subreddits: list, rss_feeds: list):
    """Background task to ingest and then cluster."""
    # Reddit
    reddit_posts = fetch_reddit_posts(subreddits)
    store_reddit_posts(db, reddit_posts)
    
    # RSS
    rss_entries = fetch_rss_feeds(rss_feeds)
    store_rss_entries(db, rss_entries)
    
    # After ingestion, run clustering (import here to avoid circular)
    from app.services.cluster import cluster_items, calculate_momentum
    cluster_items(db)
    calculate_momentum(db)
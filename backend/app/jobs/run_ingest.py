#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, init_db
from app.core.config import settings
from app.services.ingest_reddit import fetch_reddit_posts, store_reddit_posts
from app.services.ingest_rss import fetch_rss_feeds, store_rss_entries
from app.services.cluster import cluster_items, calculate_momentum

def run():
    init_db()
    db = SessionLocal()
    try:
        # Reddit
        subreddits = ["technology", "futurology", "marketing"]
        reddit_posts = fetch_reddit_posts(subreddits)
        store_reddit_posts(db, reddit_posts)
        print(f"Ingested {len(reddit_posts)} Reddit posts")
        
        # RSS
        rss_feeds = [f.strip() for f in settings.RSS_FEEDS.split(",") if f.strip()]
        rss_entries = fetch_rss_feeds(rss_feeds)
        store_rss_entries(db, rss_entries)
        print(f"Ingested {len(rss_entries)} RSS entries")
        
        # Cluster
        clusters = cluster_items(db)
        calculate_momentum(db)
        print(f"Created {len(clusters)} clusters")
    finally:
        db.close()

if __name__ == "__main__":
    run()
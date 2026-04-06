import feedparser
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from app import models, schemas

logger = logging.getLogger(__name__)

def fetch_rss_feeds(feed_urls: list, limit=50):
    """Fetch entries from RSS feeds."""
    entries = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                published = None
                if hasattr(entry, 'published_parsed'):
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed'):
                    published = datetime(*entry.updated_parsed[:6])
                
                entries.append({
                    "external_id": entry.get('id', entry.link),
                    "title": entry.title,
                    "content": entry.get('summary', '') or entry.get('description', ''),
                    "url": entry.link,
                    "author": entry.get('author', None),
                    "published_at": published or datetime.now(),
                    "score": 0,  # RSS doesn't have score
                    "source_name": feed.feed.get('title', url)
                })
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {e}")
    return entries

def store_rss_entries(db: Session, entries: list):
    """Store RSS entries."""
    source_cache = {}
    for entry in entries:
        source_name = entry["source_name"]
        if source_name not in source_cache:
            source = db.query(models.Source).filter_by(name=source_name).first()
            if not source:
                source = models.Source(name=source_name, type="rss")
                db.add(source)
                db.flush()
            source_cache[source_name] = source
        else:
            source = source_cache[source_name]
        
        existing = db.query(models.Item).filter_by(external_id=entry["external_id"]).first()
        if not existing:
            item = models.Item(
                source_id=source.id,
                external_id=entry["external_id"],
                title=entry["title"],
                content=entry["content"],
                url=entry["url"],
                author=entry["author"],
                published_at=entry["published_at"],
                score=entry["score"]
            )
            db.add(item)
    db.commit()
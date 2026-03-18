import praw
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from app import models, schemas

logger = logging.getLogger(__name__)

def fetch_reddit_posts(subreddits: list, limit=100):
    """Fetch hot posts from given subreddits."""
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_USER_AGENT
    )
    posts = []
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.hot(limit=limit):
                posts.append({
                    "external_id": post.id,
                    "title": post.title,
                    "content": post.selftext,
                    "url": post.url,
                    "author": str(post.author) if post.author else None,
                    "published_at": datetime.fromtimestamp(post.created_utc),
                    "score": post.score,
                    "source_name": f"r/{subreddit_name}"
                })
        except Exception as e:
            logger.error(f"Error fetching r/{subreddit_name}: {e}")
    return posts

def store_reddit_posts(db: Session, posts: list):
    """Store posts in database, avoid duplicates."""
    source_cache = {}
    for post in posts:
        # Find or create source
        source_name = post["source_name"]
        if source_name not in source_cache:
            source = db.query(models.Source).filter_by(name=source_name).first()
            if not source:
                source = models.Source(name=source_name, type="reddit")
                db.add(source)
                db.flush()
            source_cache[source_name] = source
        else:
            source = source_cache[source_name]
        
        # Check if item already exists
        existing = db.query(models.Item).filter_by(external_id=post["external_id"]).first()
        if not existing:
            item = models.Item(
                source_id=source.id,
                external_id=post["external_id"],
                title=post["title"],
                content=post["content"],
                url=post["url"],
                author=post["author"],
                published_at=post["published_at"],
                score=post["score"]
            )
            db.add(item)
    db.commit()
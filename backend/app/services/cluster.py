import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import logging
from sqlalchemy.orm import Session
from app import models

logger = logging.getLogger(__name__)

def cluster_items(db: Session, n_clusters=5):
    """Cluster unclustered items using TF-IDF + KMeans."""
    # Get items not yet assigned to any cluster
    # We need to find items that are not referenced in cluster_items table
    subquery = db.query(models.cluster_items.c.item_id).subquery()
    items = db.query(models.Item).filter(~models.Item.id.in_(subquery.select())).all()
    
    if len(items) < n_clusters:
        logger.info(f"Not enough items to cluster ({len(items)}), need at least {n_clusters}")
        return []
    
    texts = [f"{item.title} {item.content}" for item in items]
    
    # Vectorize
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    # Cluster
    km = KMeans(n_clusters=min(n_clusters, len(items)), random_state=42)
    labels = km.fit_predict(X)
    
    # For each cluster, create a Cluster record and associate items
    clusters = []
    for label in set(labels):
        cluster_items_indices = [i for i, l in enumerate(labels) if l == label]
        cluster_texts = [texts[i] for i in cluster_items_indices]
        
        # Find representative topic: use item with highest TF-IDF similarity to centroid
        cluster_X = X[cluster_items_indices]
        centroid = km.cluster_centers_[label]
        similarities = cosine_similarity(cluster_X, centroid.reshape(1, -1)).flatten()
        best_idx = cluster_items_indices[np.argmax(similarities)]
        topic = items[best_idx].title[:100]  # placeholder topic
        
        # Create cluster
        cluster = models.Cluster(topic=topic, momentum=0.0)
        db.add(cluster)
        db.flush()
        
        # Associate items using the association table
        for idx in cluster_items_indices:
            stmt = models.cluster_items.insert().values(
                cluster_id=cluster.id,
                item_id=items[idx].id
            )
            db.execute(stmt)
        
        clusters.append(cluster)
    
    db.commit()
    return clusters

def calculate_momentum(db: Session):
    """Update momentum for clusters based on recency and scores."""
    from datetime import datetime, timedelta
    clusters = db.query(models.Cluster).all()
    for cluster in clusters:
        # Access items directly via relationship (should now work)
        items = cluster.items
        if not items:
            continue
        now = datetime.utcnow()
        total_weight = 0
        weighted_score = 0
        for item in items:
            days_old = (now - item.published_at).days
            if days_old < 7:
                weight = 1.0 / (days_old + 1)
                weighted_score += item.score * weight
                total_weight += weight
        momentum = weighted_score / total_weight if total_weight > 0 else 0
        cluster.momentum = momentum
    db.commit()
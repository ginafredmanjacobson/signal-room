from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app import models, schemas
from app.services.ai_service import generate_brief

router = APIRouter()

@router.get("/", response_model=List[schemas.Cluster])
def get_clusters(db: Session = Depends(get_db)):
    clusters = db.query(models.Cluster).order_by(models.Cluster.momentum.desc()).all()
    return clusters

@router.get("/{cluster_id}", response_model=schemas.Cluster)
def get_cluster(cluster_id: int, db: Session = Depends(get_db)):
    cluster = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return cluster

@router.post("/{cluster_id}/brief")
def generate_cluster_brief(cluster_id: int, db: Session = Depends(get_db)):
    cluster = db.query(models.Cluster).filter(models.Cluster.id == cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Directly use cluster.items (already list of Item objects)
    items = cluster.items
    texts = [f"{item.title}: {item.content}" for item in items if item.content]
    if not texts:
        return {"summary": "No content available", "bullets": []}
    
    brief = generate_brief(texts, cluster.topic)
    # Optionally store the summary in the cluster
    cluster.summary = brief["summary"]
    db.commit()
    return brief
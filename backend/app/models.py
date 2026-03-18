from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String) # "reddit" or "rss"
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    external_id = Column(String, unique=True, index=True)  # Reddit post ID or RSS guid
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    author = Column(String)
    published_at = Column(DateTime)
    score = Column(Integer, default=0)  # Reddit score or RSS popularity
    created_at = Column(DateTime, default=datetime.utcnow)
    
    source = relationship("Source")

class Cluster(Base):
    __tablename__ = "clusters"
    
    id = Column(Integer, primary_key=True)
    topic = Column(String)  # generated topic label
    summary = Column(Text)  # brief summary
    momentum = Column(Float, default=0.0)  # calculated score
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = relationship("ClusterItem", back_populates="cluster")

class ClusterItem(Base):
    __tablename__ = "cluster_items"
    
    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    
    cluster = relationship("Cluster", back_populates="items")
    item = relationship("Item")

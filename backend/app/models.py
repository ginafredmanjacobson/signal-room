from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

# Association table (no separate model class)
cluster_items = Table(
    "cluster_items",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("cluster_id", Integer, ForeignKey("clusters.id")),
    Column("item_id", Integer, ForeignKey("items.id")),
)

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)  # "reddit" or "rss"
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    items = relationship("Item", back_populates="source")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    external_id = Column(String, unique=True, index=True)
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    author = Column(String)
    published_at = Column(DateTime)
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    source = relationship("Source", back_populates="items")
    clusters = relationship("Cluster", secondary=cluster_items, back_populates="items")

class Cluster(Base):
    __tablename__ = "clusters"
    
    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    momentum = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = relationship("Item", secondary=cluster_items, back_populates="clusters")
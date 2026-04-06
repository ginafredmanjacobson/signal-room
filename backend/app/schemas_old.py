from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Source schemas
class SourceBase(BaseModel):
    name: str
    type: str
    url: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Item schemas
class ItemBase(BaseModel):
    external_id: str
    title: str
    content: str
    url: str
    author: Optional[str] = None
    published_at: datetime
    score: int = 0

class ItemCreate(ItemBase):
    source_id: int

class Item(ItemBase):
    id: int
    source_id: int
    created_at: datetime
    source: Optional[Source] = None
    
    class Config:
        from_attributes = True

# Cluster schemas
class ClusterBase(BaseModel):
    topic: str
    summary: Optional[str] = None
    momentum: float = 0.0

class ClusterCreate(ClusterBase):
    pass

class Cluster(ClusterBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[Item] = []
    
    class Config:
        from_attributes = True
# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnalysisBase(BaseModel):
    text: str

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisResponse(BaseModel):
    id: int
    text: str
    summary: Optional[str]
    title: Optional[str]
    topics: Optional[List[str]]
    sentiment: Optional[str]
    keywords: Optional[List[str]]
    confidence_score: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True

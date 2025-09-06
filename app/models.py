# app/models.py
from sqlalchemy import Column, Integer, Text, JSON, Float, DateTime
from datetime import datetime
from .database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    summary = Column(Text)
    title = Column(Text)
    topics = Column(Text)
    sentiment = Column(Text)
    keywords = Column(Text)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

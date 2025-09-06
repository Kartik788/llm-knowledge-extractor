from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, services, database

# Initialize app
app = FastAPI(title="LLM Knowledge Extractor")

# Create tables (Use database.Base instead of models.Base)
models.Base.metadata.create_all(bind=database.engine)

# Dependency
get_db = database.get_db

# POST /analyze
@app.post("/analyze", response_model=schemas.AnalysisResponse)
def analyze_text(analysis: schemas.AnalysisCreate, db: Session = Depends(get_db)):
    if not analysis.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Generate analysis using LLM + keyword extractor
    data = services.analyze_text_with_llm(analysis.text)
    
    # Save to DB
    db_analysis = models.Analysis(
        text=analysis.text,
        summary=data["summary"],
        title=data["title"],
        topics=",".join([t.lower() for t in data["topics"]]),
        sentiment=data["sentiment"],
        keywords=",".join([k.lower() for k in data["keywords"]]),
        confidence_score=data["confidence_score"]

        
        
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    

    # Convert back to list before returning
    db_analysis.topics = db_analysis.topics.split(",") if db_analysis.topics else []
    db_analysis.keywords = db_analysis.keywords.split(",") if db_analysis.keywords else []
    return db_analysis

# GET /search?topic=xyz
@app.get("/search", response_model=List[schemas.AnalysisResponse])
def search(topic: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    topic_lower = topic.lower()
    results = db.query(models.Analysis).filter(
        (models.Analysis.topics.ilike(f"%{topic_lower}%")) |
        (models.Analysis.keywords.ilike(f"%{topic_lower}%"))
    ).all()

    # Convert comma-separated strings to lists for response
    for r in results:
        if isinstance(r.topics, str):
            r.topics = [t.strip() for t in r.topics.split(",")]
        if isinstance(r.keywords, str):
            r.keywords = [k.strip() for k in r.keywords.split(",")]
    return results




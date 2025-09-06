# app/services.py
import spacy
import json
from collections import Counter
from openai import OpenAI

# Initialize OpenAI client with hardcoded API key 
client = OpenAI(api_key="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")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, top_n=3):
    
    #Extracts the top N most frequent nouns from text.
    
    doc = nlp(text)
    nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
    freq = Counter(nouns)
    top_keywords = [word for word, _ in freq.most_common(top_n)]
    return top_keywords

def analyze_text_with_llm(text: str):
    
    prompt = f"""
    Analyze the following text. Return JSON with fields:
    - title (short headline)
    - summary (2 sentences max)
    - topics (list of 3 themes)
    - sentiment (positive/neutral/negative)

    Text: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts structured information from text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"} 
    )

    try:
        llm_output = json.loads(response.choices[0].message.content)
    except:
        llm_output = {
            "title": "Untitled",
            "summary": "Could not parse response.",
            "topics": [],
            "sentiment": "neutral"
        }

    # Add keywords (from spaCy)
    keywords = extract_keywords(text)
    llm_output["keywords"] = keywords

    # Add confidence score (simple heuristic)
    llm_output["confidence_score"] = round(len(keywords) / 3, 2)

    return llm_output

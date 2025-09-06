# app/services.py
import spacy
import requests
import json
from collections import Counter
from openai import OpenAI

# Initialize OpenAI client
GIST_URL = "https://gist.githubusercontent.com/Kartik788/9241d05875026ece873f4bcdc1842d4a/raw/a91fe2d7baa09dc718b7630ddbd13ef3971c3d49/openai_key.txt"

response = requests.get(GIST_URL)
if response.status_code == 200:
    OPENAI_API_KEY = response.text.strip()
else:
    raise Exception("Failed to fetch API key")

client = OpenAI(api_key=OPENAI_API_KEY)

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

# app/ui.py
import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="LLM Knowledge Extractor", layout="wide")
st.title("🧠 LLM Knowledge Extractor")

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", ["Analyze Text", "Search Past Analyses"])

# ----------------- Analyze Text -----------------
if page == "Analyze Text":
    st.header("Submit Text for Analysis")
    user_text = st.text_area("Enter your text here:", height=200)

    if st.button("Analyze"):
        if not user_text.strip():
            st.error("Please enter some text!")
        else:
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(f"{API_URL}/analyze", json={"text": user_text})
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Analysis Complete ✅")
                        st.subheader("Summary")
                        st.write(data["summary"])
                        st.subheader("Title")
                        st.write(data["title"])
                        st.subheader("Topics")
                        st.write(", ".join(data["topics"]))
                        st.subheader("Sentiment")
                        st.write(data["sentiment"])
                        st.subheader("Keywords")
                        st.write(", ".join(data["keywords"]))
                        st.subheader("Confidence Score")
                        st.write(data["confidence_score"])
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"API Error: {e}")

# ----------------- Search Past Analyses -----------------
elif page == "Search Past Analyses":
    st.header("Search Stored Analyses by Topic/Keyword")
    query = st.text_input("Enter topic or keyword:")
    
    if st.button("Search"):
        if not query.strip():
            st.error("Please enter a topic or keyword!")
        else:
            with st.spinner("Searching..."):
                try:
                    response = requests.get(f"{API_URL}/search", params={"topic": query})
                    if response.status_code == 200:
                        results = response.json()
                        if results:
                            st.success(f"Found {len(results)} result(s)")
                            for r in results:
                                st.markdown("---")
                                st.subheader(r["title"])
                                st.write("**Summary:**", r["summary"])
                                st.write("**Topics:**", ", ".join(r["topics"]))
                                st.write("**Sentiment:**", r["sentiment"])
                                st.write("**Keywords:**", ", ".join(r["keywords"]))
                                st.write("**Confidence Score:**", r["confidence_score"])
                                st.write("**Submitted At:**", r["created_at"])
                        else:
                            st.warning("No results found for this query.")
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"API Error: {e}")

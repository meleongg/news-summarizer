import streamlit as st
import requests

st.title("AI News Summarizer & Sentiment Analyzer 📰🤖")

# User enters a search phrase instead of a URL
query = st.text_input("Enter a topic or keyword to analyze:")

# Store articles in session state
if "articles" not in st.session_state:
    st.session_state.articles = []

if "selected_url" not in st.session_state:
    st.session_state.selected_url = None

if st.button("Search News"):
    if query:
        response = requests.get("http://127.0.0.1:8000/fetch_news/", params={"query": query})
        if response.status_code == 200:
            st.session_state.articles = response.json()  # Store articles in session state
            st.session_state.selected_url = None  # Reset selected URL on new search
        else:
            st.error("Failed to fetch news. Check your API key or query.")

# Display articles if available
if st.session_state.articles:
    selected_title = st.selectbox(
        "Choose an article:",
        [a["title"] for a in st.session_state.articles],
        key="article_select"
    )

    # Update selected URL dynamically when user picks a new article
    for a in st.session_state.articles:
        if a["title"] == selected_title:
            st.session_state.selected_url = a["url"]

    st.write("**Selected URL:**", st.session_state.selected_url)

# Analyze button (outside of search logic)
if st.session_state.selected_url and st.button("Analyze Article"):
    try:
        analysis_response = requests.get(
            "http://127.0.0.1:8000/analyze/",
            params={"url": st.session_state.selected_url}
        )
        if analysis_response.status_code == 200:
            analysis_data = analysis_response.json()
            st.subheader("Article Title")
            st.write(analysis_data["title"])
            st.subheader("Article Content")
            st.write(analysis_data["text"])
        else:
            st.error(f"Error analyzing article. Status code: {analysis_response.status_code}")
    except Exception as e:
        st.error(f"Error making request: {str(e)}")
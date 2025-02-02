import streamlit as st
import requests

st.title("AI News Summarizer & Sentiment Analyzer 📰🤖")

if "selected_url" not in st.session_state:
    st.session_state.selected_url = None

query = st.text_input("Enter a topic or keyword to analyze:")
sort_by = st.selectbox("Sort articles by:", ["Relevancy", "Popularity", "Publish Date"])
page_size = st.selectbox("Number of articles to show:", [5, 10, 15, 20])

if st.button("Search News"):
    loading_text = st.empty()  # Placeholder for "Loading..."
    loading_text.text("Searching for articles... Please wait ⏳")  # Show loading message

    if query:
        sort_map = {
          "Relevancy": "relevancy",
          "Popularity": "popularity",
          "Publish Date": "publishedAt"
        }
        sort_by = sort_map[sort_by]

        response = requests.get(
            f"http://127.0.0.1:8000/fetch_news/",
            params={"query": query, "sort_by": sort_by, "page_size": page_size}
        )

        if response.status_code == 200:
            loading_text.empty()
            articles = response.json()
            if articles:
                st.session_state.articles = articles
                st.session_state.selected_url = None
            else:
                st.warning("No articles found.")
        else:
            loading_text.empty()
            st.error("Failed to fetch news. Check your API key.")

if "articles" in st.session_state and st.session_state.articles:
    selected_title = st.selectbox(
        "Choose an article:",
        [a["title"] for a in st.session_state.articles],
        key="article_select"
    )
    for a in st.session_state.articles:
        if a["title"] == selected_title:
            st.session_state.selected_url = a["url"]

    st.write("**Selected URL:**", st.session_state.selected_url)

if st.session_state.selected_url and st.button("Analyze Article"):
    loading_text = st.empty()  # Placeholder for "Loading..."
    loading_text.text("Analyzing... Please wait ⏳")  # Show loading message

    try:
        analysis_response = requests.get("http://127.0.0.1:8000/analyze/", params={"url": st.session_state.selected_url})

        if analysis_response.status_code == 200:
            analysis_data = analysis_response.json()

            loading_text.empty()  # Remove loading message

            st.subheader("Article Title")
            st.write(analysis_data["title"])
            st.subheader("Article Content")
            st.write(analysis_data["text"])
        else:
            loading_text.empty()
            st.error(f"Error analyzing article. Status code: {analysis_response.status_code}")

    except Exception as e:
        loading_text.empty()
        st.error(f"Error making request: {str(e)}")
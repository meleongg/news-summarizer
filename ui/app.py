import streamlit as st
import requests

st.title("AI News Summarizer & Sentiment Analyzer 📰🤖")

# User enters a search phrase instead of a URL
query = st.text_input("Enter a topic or keyword to analyze:")

if st.button("Search News"):
    if query:
        response = requests.get(f"http://127.0.0.1:8000/fetch_news/", params={"query": query})
        if response.status_code == 200:
            articles = response.json()

            if not articles:
                st.warning("No articles found. Try another search.")
            else:
                # Let user select an article
                selected_article = st.selectbox("Choose an article:",
                                                [f"{a['title']} ({a['url']})" for a in articles])

                # Extract the URL from the selected article
                selected_url = [a["url"] for a in articles if a["title"] in selected_article][0]

                if st.button("Analyze Article"):
                    analysis_response = requests.get(f"http://127.0.0.1:8000/analyze/", params={"url": selected_url})

                    if analysis_response.status_code == 200:
                        data = analysis_response.json()
                        st.subheader("Article Title")
                        st.write(data["title"])
                        st.subheader("Article Content")
                        st.write(data["text"])
                    else:
                        st.error("Error analyzing article.")
        else:
            st.error("Failed to fetch news. Check your API key or query.")
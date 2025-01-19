import streamlit as st
from app.search import fetch_papers, index_papers, search_papers, vector_store

st.title("📚 Paper Scholar")

# Search bar for papers
query = st.text_input("Search for research papers:")
if query:
    with st.spinner("Fetching and indexing papers..."):
        papers = fetch_papers(query)
        vector_store = index_papers(papers)
        results = search_papers(query, vector_store)

    st.subheader("Search Results")
    for result in results:
        st.markdown(f"### [{result['title']}]({result['url']})")
        st.write(result['summary'])
        st.markdown("---")

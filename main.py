import streamlit as st
from app.search import fetch_papers, index_papers, search_papers, vector_store


# Set page configuration
st.set_page_config(
    page_title="Paper Scholar",  
    page_icon=":page_with_curl:", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

st.title(":page_with_curl: Paper Scholar")

# User control for number of shown papers
n_shown_paper = st.slider("Number of papers to display:", min_value=1, max_value=20, value=5, step=1)
search_multiplier = 5
top_k = n_shown_paper
max_results = search_multiplier * top_k

# Search bar for papers
query = st.text_input("Search for research papers:")
if query:
    with st.spinner("Fetching and indexing papers..."):
        papers = fetch_papers(query, max_results=max_results)
        vector_store = index_papers(papers)
        results = search_papers(query, vector_store, top_k=top_k)

    st.subheader("Search Results")
    for result in results:
        # Display title with a link to the full paper
        st.markdown(f"### [{result['title']}]({result['url']})")

        # Foldable summary using expander
        with st.expander("View Summary"):
            st.write(result['summary'])
        
        st.markdown("---")

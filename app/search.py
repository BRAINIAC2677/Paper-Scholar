import arxiv
import faiss 
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore


def fetch_papers(query, max_results=60):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id
        })
    return papers


# Initialize embeddings and FAISS vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

def index_papers(papers, vector_store=vector_store):
    """
    Indexes papers into the given vector store, checking for duplicates.

    Args:
        papers: A list of papers, where each paper is a dictionary containing 
               "title", "summary", and "url".
        vector_store: The existing FAISS vector store.

    Returns:
        The updated FAISS vector store.
    """

    new_papers = []
    for paper in papers:
        # Check if a document with the same URL already exists
        existing_docs = vector_store.similarity_search_with_score(
            query="",  # You'll need to provide a query here 
            n_results=1, 
            filter={"url": paper["url"]} 
        )

        if not existing_docs:
            new_papers.append(paper)

    if new_papers:
        documents = [
            {"text": paper["summary"], "metadata": {"title": paper["title"], "url": paper["url"]}}
            for paper in new_papers
        ]
        vector_store.add_texts(
            texts=[doc["text"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents]
        )

    return vector_store

def search_papers(query, vector_store, top_k=5):
    results = vector_store.similarity_search(query, k=top_k)
    return [{"title": result.metadata["title"], "summary": result.page_content, "url": result.metadata["url"]} for result in results]








import os
import uuid
import chromadb
import streamlit as st

@st.cache_resource
def get_collection():
    client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"), port=8000)
    return client.get_or_create_collection(name="notes")

collection = get_collection()

st.title("🔎 Notes Search")
st.caption(f"Notes stored: {collection.count()}")

# Add notes
with st.sidebar:
    st.header("Add a note")
    text = st.text_area("Note")
    topic = st.text_input("Topic", value="general")
    if st.button("Save note") and text.strip():
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text.strip()],
            metadatas=[{"topic": topic.strip() or "general"}],
        )
        st.success("Saved!")
        st.rerun()

# Search notes
query = st.text_input("Search by meaning")
topic_filter = st.text_input("Filter by topic (optional)")
n = st.slider("Results", 1, 10, 3)

if query and collection.count() > 0:
    results = collection.query(
        query_texts=[query],
        n_results=min(n, collection.count()),
        where={"topic": topic_filter.strip()} if topic_filter.strip() else None,
        include=["documents", "metadatas", "distances"],
    )
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        st.markdown(f"**{doc}**")
        st.caption(f"topic: {meta['topic']} | distance: {dist:.3f}")
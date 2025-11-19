import os
import streamlit as st

from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings


# ==============================
# API KEY (from Streamlit secrets)
# ==============================
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# ==============================
# Streamlit UI
# ==============================
st.title("📰 News Research Tool")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"Enter URL {i+1}", key=f"url_{i}")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")

main_placeholder = st.empty()


# ==============================
# LLMs
# ==============================

# 1️⃣ Summaries LLM — cheap & fast
summary_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    groq_api_key=GROQ_API_KEY,
    max_tokens=500
)

# 2️⃣ Q&A LLM — powerful
qa_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=GROQ_API_KEY,
    max_tokens=500
)


# ============================================================
# PROCESS URLs → BUILD VECTOR INDEX + SUMMARIES
# ============================================================

if process_url_clicked:

    if len(urls) == 0:
        st.warning("Please enter at least one URL.")
        st.stop()

    # 1. Load Data (Unstructured)
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("📥 Loading article data...")
    data = loader.load()

    # Clean up text content
    for d in data:
        d.page_content = d.page_content.strip()

    # 2. Split Data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=1000,
        chunk_overlap=100,
    )
    main_placeholder.text("✂️ Splitting text into chunks...")
    docs = text_splitter.split_documents(documents=data)

    # 3. Embeddings using MiniLM (clean & cloud-safe)
    main_placeholder.text("🔢 Generating embeddings…")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Build FAISS Index
    main_placeholder.text("📦 Building FAISS index…")
    vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)

    # 5. Save FAISS index
    vector_store.save_local("faiss_index")

    # 6. Summaries
    main_placeholder.text("📝 Generating summaries…")

    summaries = []

    for i, article in enumerate(data):
        content = article.page_content[:4000]

        prompt = f"""
        Provide a structured summary of the following article:
        - 2–3 sentence overview
        - Five bullet-point key takeaways
        - Two key insights or implications


        Provide a professional looking structured summary. Keep the 5 bullet points in different lines. Do no mention how many sentences or points you will upload in the final output.

        ARTICLE:
        {content}
        """

        response = summary_llm.invoke(prompt)

        summaries.append({
            "url": article.metadata.get("source", f"Article {i+1}"),
            "summary": response.content
        })

    # Save summaries to session_state so they don't disappear
    st.session_state["summaries"] = summaries
    st.session_state["urls_processed"] = True

    main_placeholder.text("✅ Processing Completed!")


# ============================================================
# SHOW SUMMARIES IF PRESENT
# ============================================================

if "summaries" in st.session_state:

    summaries = st.session_state["summaries"]

    st.subheader("📝 Article Summaries")

    tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

    for idx, tab in enumerate(tabs):
        with tab:
            st.markdown(f"### 🌐 Source: {summaries[idx]['url']}")
            with st.expander("📄 View Summary", expanded=False):
                st.write(summaries[idx]["summary"])


# ============================================================
# QUESTION ANSWERING
# ============================================================

st.subheader("🔍 Ask a Question About the Articles:")
query = st.text_input("Your Question:")

if query:

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=qa_llm,
        retriever=vector_store.as_retriever()
    )

    result = chain({"question": query}, return_only_outputs=True)

    st.header("Answer:")
    st.write(result["answer"])

    st.subheader("Sources:")
    st.write(result["sources"])

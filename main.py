import os
import streamlit as st
import time

from langchain_groq import ChatGroq, GroqEmbeddings
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS


# ==============================
# API KEY
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

# 1️⃣ Cheap & Fast model for SUMMARIES
summary_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    groq_api_key=GROQ_API_KEY,
    max_tokens=350,
    timeout=None,
    max_retries=2
)

# 2️⃣ Most powerful model for QA
qa_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=GROQ_API_KEY,
    max_tokens=500,
    timeout=None,
    max_retries=2
)


# ============================================================
# PROCESS URLs → BUILD VECTOR INDEX + SUMMARIES
# ============================================================

if process_url_clicked:

    if len(urls) == 0:
        st.warning("Please enter at least one URL.")
        st.stop()

    # 1. Load Data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("📥 Loading article data...")
    data = loader.load()

    # 2. Split Data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=1000,
        chunk_overlap=100,
    )
    main_placeholder.text("✂️ Splitting text into chunks...")
    docs = text_splitter.split_documents(documents=data)

    # 3. Groq Embeddings (WORKS ON STREAMLIT CLOUD)
    main_placeholder.text("🔢 Generating embeddings (Groq)…")
    embeddings = GroqEmbeddings(
        model="nomic-embed-text",
        groq_api_key=GROQ_API_KEY
    )

    # 4. Build FAISS Index
    main_placeholder.text("📦 Building FAISS index...")
    vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)

    # 5. Save FAISS Index
    vector_store.save_local("faiss_index")

    # 6. Generate Summaries Using CHEAP LLM
    main_placeholder.text("📝 Generating article summaries...")

    summaries = []

    for i, article in enumerate(data):
        content = article.page_content[:4000]  # safe token limit

        prompt = f"""
        Provide a well-structured summary of the following news article with:
        - A 2–3 sentence overview  
        - Five bullet-point key takeaways  
        - Three key insights or implications  

        ARTICLE:
        {content}
        """

        response = summary_llm.invoke(prompt)

        summaries.append({
            "url": article.metadata.get("source", f"Article {i+1}"),
            "summary": response.content
        })

    # SAVE SUMMARIES TO SESSION STATE
    st.session_state["summaries"] = summaries
    st.session_state["urls_processed"] = True

    main_placeholder.text("✅ Processing + Summaries Completed!")


# ============================================================
# SHOW SUMMARIES IF THEY EXIST
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
# QUESTION ANSWERING SECTION
# ============================================================

st.subheader("🔍 Ask a Question About the Articles:")
query = st.text_input("Your Question:")

if query:

    embeddings = GroqEmbeddings(
        model="nomic-embed-text",
        groq_api_key=GROQ_API_KEY
    )

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

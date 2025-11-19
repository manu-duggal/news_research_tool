# import os
# import streamlit as st

# from langchain_groq import ChatGroq
# from langchain_classic.chains import RetrievalQAWithSourcesChain
# from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import SentenceTransformerEmbeddings

# from io import BytesIO
# from datetime import datetime
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet


# # ==============================
# # API KEY (from Streamlit secrets)
# # ==============================
# GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# # ==============================
# # Streamlit UI
# # ==============================
# st.title("📰 News Research Tool")
# st.sidebar.title("News Article URLs")

# urls = []
# for i in range(3):
#     url = st.sidebar.text_input(f"Enter URL {i+1}", key=f"url_{i}")
#     if url:
#         urls.append(url)

# process_url_clicked = st.sidebar.button("Process URLs")

# main_placeholder = st.empty()


# # ==============================
# # LLMs
# # ==============================

# # 1️⃣ Summaries LLM — cheap & fast
# summary_llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0.2,
#     groq_api_key=GROQ_API_KEY,
#     max_tokens=500
# )

# # 2️⃣ Q&A LLM — powerful
# qa_llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0.7,
#     groq_api_key=GROQ_API_KEY,
#     max_tokens=500
# )


# # ============================================================
# # PROCESS URLs → BUILD VECTOR INDEX + SUMMARIES
# # ============================================================

# if process_url_clicked:

#     if len(urls) == 0:
#         st.warning("Please enter at least one URL.")
#         st.stop()

#     # 1. Load Data (Unstructured)
#     loader = UnstructuredURLLoader(urls=urls)
#     main_placeholder.text("📥 Loading article data...")
#     data = loader.load()

#     # Clean up text content
#     for d in data:
#         d.page_content = d.page_content.strip()

#     # 2. Split Data
#     text_splitter = RecursiveCharacterTextSplitter(
#         separators=["\n\n", "\n", ".", " "],
#         chunk_size=1000,
#         chunk_overlap=100,
#     )
#     main_placeholder.text("✂️ Splitting text into chunks...")
#     docs = text_splitter.split_documents(documents=data)

#     # 3. Embeddings using MiniLM (clean & cloud-safe)
#     main_placeholder.text("🔢 Generating embeddings…")
#     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#     # 4. Build FAISS Index
#     main_placeholder.text("📦 Building FAISS index…")
#     vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)

#     # 5. Save FAISS index
#     vector_store.save_local("faiss_index")

#     # 6. Summaries
#     main_placeholder.text("📝 Generating summaries…")

#     summaries = []

#     for i, article in enumerate(data):
#         content = article.page_content[:4000]

#         prompt = f"""
#         Provide a structured summary of the following article:
#         - 2–3 sentence overview
#         - Five key takeaways
#         - Two key insights or implications


#         Provide a professional looking structured summary. Do no mention how many sentences or points you will upload in the final output.

#         ARTICLE:
#         {content}
#         """

#         response = summary_llm.invoke(prompt)

#         summaries.append({
#             "url": article.metadata.get("source", f"Article {i+1}"),
#             "summary": response.content
#         })

#     # Save summaries to session_state so they don't disappear
#     st.session_state["summaries"] = summaries
#     st.session_state["urls_processed"] = True

#     main_placeholder.text("✅ Processing Completed!")


# # ============================================================
# # SHOW SUMMARIES IF PRESENT
# # ============================================================

# if "summaries" in st.session_state:

#     summaries = st.session_state["summaries"]

#     st.subheader("📝 Article Summaries")

#     tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

#     for idx, tab in enumerate(tabs):
#         with tab:
#             st.markdown(f"### 🌐 Source: {summaries[idx]['url']}")
#             with st.expander("📄 View Summary", expanded=False):
#                 st.write(summaries[idx]["summary"])


# # ============================================================
# # PDF REPORT GENERATOR (STYLE A: CLEAN PROFESSIONAL)
# # ============================================================

# def generate_pdf_report(summaries):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     elements = []

#     title = Paragraph("<b>News Research Report</b>", styles["Title"])
#     elements.append(title)
#     elements.append(Spacer(1, 20))

#     timestamp = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#                           styles["Normal"])
#     elements.append(timestamp)
#     elements.append(Spacer(1, 20))

#     for idx, article in enumerate(summaries):
#         elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
#         elements.append(Paragraph(f"URL: {article['url']}", styles["Normal"]))
#         elements.append(Spacer(1, 10))

#         clean_summary = article['summary']
#         clean_summary = clean_summary.replace("**", "")  # remove markdown bold markers
#         clean_summary = clean_summary.replace("\n", "<br/>")  # newlines to HTML breaks
        
#         elements.append(Paragraph(clean_summary, styles["Normal"]))
#         elements.append(Spacer(1, 20))

#     doc.build(elements)
#     buffer.seek(0)
#     return buffer


# if "summaries" in st.session_state:
#     pdf_buffer = generate_pdf_report(st.session_state["summaries"])
#     st.download_button(
#         label="📄 Download PDF Report",
#         data=pdf_buffer,
#         file_name="news_report.pdf",
#         mime="application/pdf"
#     )


# # ============================================================
# # QUESTION ANSWERING
# # ============================================================

# st.subheader("🔍 Ask a Question About the Articles:")
# query = st.text_input("Your Question:")

# if query:

#     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#     vector_store = FAISS.load_local(
#         "faiss_index",
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     chain = RetrievalQAWithSourcesChain.from_llm(
#         llm=qa_llm,
#         retriever=vector_store.as_retriever()
#     )

#     result = chain({"question": query}, return_only_outputs=True)

#     st.header("Answer:")
#     st.write(result["answer"])

#     st.subheader("Sources:")
#     st.write(result["sources"])



import os
import streamlit as st

from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ==============================
#  CUSTOM CSS — (LinkedIn + Notion hybrid)
# ==============================
st.markdown("""
<style>

    /* GLOBAL */
    .stApp {
        background-color: #F8F9FB;
        font-family: 'Inter', sans-serif;
    }

    /* HEADERS */
    h1 {
        color: #1A1A1A !important;
        font-weight: 700 !important;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem;
    }

    h2, h3 {
        color: #1A1A1A !important;
        font-weight: 600 !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #E0E0E0;
    }

    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        color: #1A1A1A;
    }

    /* NOTION-STYLE CARDS */
    .summary-card {
        background-color: #ffffff;
        padding: 1.2rem 1.4rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    /* DIVIDER */
    .divider {
        border-top: 1px solid #E5E7EB;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

</style>
""", unsafe_allow_html=True)


# ==============================
# API KEY
# ==============================
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# ==============================
# Streamlit UI
# ==============================
st.title("📰 News Research Tool")

st.sidebar.markdown("<div class='sidebar-title'>News Article URLs</div>", unsafe_allow_html=True)

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

summary_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    groq_api_key=GROQ_API_KEY,
    max_tokens=500
)

qa_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=GROQ_API_KEY,
    max_tokens=500
)


# ============================================================
# PROCESS URLs
# ============================================================

if process_url_clicked:

    if len(urls) == 0:
        st.warning("Please enter at least one URL.")
        st.stop()

    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("📥 Loading article data...")
    data = loader.load()

    for d in data:
        d.page_content = d.page_content.strip()

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=1000,
        chunk_overlap=100,
    )

    main_placeholder.text("✂️ Splitting text into chunks...")
    docs = text_splitter.split_documents(documents=data)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    main_placeholder.text("📦 Building FAISS index…")
    vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)

    vector_store.save_local("faiss_index")

    main_placeholder.text("📝 Generating summaries…")

    summaries = []

    for i, article in enumerate(data):
        content = article.page_content[:4000]

        prompt = f"""
        Provide a structured summary of the following article:
        - 2–3 sentence overview
        - Five key takeaways
        - Two key insights or implications

        Provide a professional looking structured summary.
        ARTICLE:
        {content}
        """

        response = summary_llm.invoke(prompt)

        summaries.append({
            "url": article.metadata.get("source", f"Article {i+1}"),
            "summary": response.content
        })

    st.session_state["summaries"] = summaries
    st.session_state["urls_processed"] = True

    main_placeholder.text("✅ Processing Completed!")


# ============================================================
# SHOW SUMMARIES
# ============================================================

if "summaries" in st.session_state:

    summaries = st.session_state["summaries"]

    st.subheader("📝 Article Summaries")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

    for idx, tab in enumerate(tabs):
        with tab:
            st.markdown(f"### 🌐 Source: {summaries[idx]['url']}")
            with st.expander("📄 View Summary", expanded=False):
                st.markdown(f"""
                <div class="summary-card">
                    {summaries[idx]['summary']}
                </div>
                """, unsafe_allow_html=True)


# ============================================================
# PDF GENERATION
# ============================================================

def generate_pdf_report(summaries):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("<b>News Research Report</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 20))

    timestamp = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                          styles["Normal"])
    elements.append(timestamp)
    elements.append(Spacer(1, 20))

    for idx, article in enumerate(summaries):
        elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
        elements.append(Paragraph(f"URL: {article['url']}", styles["Normal"]))
        elements.append(Spacer(1, 10))

        clean_summary = (
            article['summary']
            .replace("**", "")
            .replace("\n", "<br/>")
        )

        elements.append(Paragraph(clean_summary, styles["Normal"]))
        elements.append(Spacer(1, 20))

    doc.build(elements)
    buffer.seek(0)
    return buffer


if "summaries" in st.session_state:
    pdf_buffer = generate_pdf_report(st.session_state["summaries"])
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_buffer,
        file_name="news_report.pdf",
        mime="application/pdf"
    )


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

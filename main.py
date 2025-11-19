# # import os
# # import streamlit as st

# # from langchain_groq import ChatGroq
# # from langchain_classic.chains import RetrievalQAWithSourcesChain
# # from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
# # from langchain_community.document_loaders import UnstructuredURLLoader
# # from langchain_community.vectorstores import FAISS
# # from langchain_community.embeddings import SentenceTransformerEmbeddings

# # from io import BytesIO
# # from datetime import datetime
# # from reportlab.lib.pagesizes import letter
# # from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# # from reportlab.lib.styles import getSampleStyleSheet


# # # ==============================
# # # API KEY (from Streamlit secrets)
# # # ==============================
# # GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# # # ==============================
# # # Streamlit UI
# # # ==============================
# # st.title("📰 News Research Tool")
# # st.sidebar.title("News Article URLs")

# # urls = []
# # for i in range(3):
# #     url = st.sidebar.text_input(f"Enter URL {i+1}", key=f"url_{i}")
# #     if url:
# #         urls.append(url)

# # process_url_clicked = st.sidebar.button("Process URLs")

# # main_placeholder = st.empty()


# # # ==============================
# # # LLMs
# # # ==============================

# # # 1️⃣ Summaries LLM — cheap & fast
# # summary_llm = ChatGroq(
# #     model="llama-3.1-8b-instant",
# #     temperature=0.2,
# #     groq_api_key=GROQ_API_KEY,
# #     max_tokens=500
# # )

# # # 2️⃣ Q&A LLM — powerful
# # qa_llm = ChatGroq(
# #     model="llama-3.3-70b-versatile",
# #     temperature=0.7,
# #     groq_api_key=GROQ_API_KEY,
# #     max_tokens=500
# # )


# # # ============================================================
# # # PROCESS URLs → BUILD VECTOR INDEX + SUMMARIES
# # # ============================================================

# # if process_url_clicked:

# #     if len(urls) == 0:
# #         st.warning("Please enter at least one URL.")
# #         st.stop()

# #     # 1. Load Data (Unstructured)
# #     loader = UnstructuredURLLoader(urls=urls)
# #     main_placeholder.text("📥 Loading article data...")
# #     data = loader.load()

# #     # Clean up text content
# #     for d in data:
# #         d.page_content = d.page_content.strip()

# #     # 2. Split Data
# #     text_splitter = RecursiveCharacterTextSplitter(
# #         separators=["\n\n", "\n", ".", " "],
# #         chunk_size=1000,
# #         chunk_overlap=100,
# #     )
# #     main_placeholder.text("✂️ Splitting text into chunks...")
# #     docs = text_splitter.split_documents(documents=data)

# #     # 3. Embeddings using MiniLM (clean & cloud-safe)
# #     main_placeholder.text("🔢 Generating embeddings…")
# #     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# #     # 4. Build FAISS Index
# #     main_placeholder.text("📦 Building FAISS index…")
# #     vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)

# #     # 5. Save FAISS index
# #     vector_store.save_local("faiss_index")

# #     # 6. Summaries
# #     main_placeholder.text("📝 Generating summaries…")

# #     summaries = []

# #     for i, article in enumerate(data):
# #         content = article.page_content[:4000]

# #         prompt = f"""
# #         Provide a structured summary of the following article:
# #         - 2–3 sentence overview
# #         - Five key takeaways
# #         - Two key insights or implications


# #         Provide a professional looking structured summary. Do no mention how many sentences or points you will upload in the final output.

# #         ARTICLE:
# #         {content}
# #         """

# #         response = summary_llm.invoke(prompt)

# #         summaries.append({
# #             "url": article.metadata.get("source", f"Article {i+1}"),
# #             "summary": response.content
# #         })

# #     # Save summaries to session_state so they don't disappear
# #     st.session_state["summaries"] = summaries
# #     st.session_state["urls_processed"] = True

# #     main_placeholder.text("✅ Processing Completed!")


# # # ============================================================
# # # SHOW SUMMARIES IF PRESENT
# # # ============================================================

# # if "summaries" in st.session_state:

# #     summaries = st.session_state["summaries"]

# #     st.subheader("📝 Article Summaries")

# #     tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

# #     for idx, tab in enumerate(tabs):
# #         with tab:
# #             st.markdown(f"### 🌐 Source: {summaries[idx]['url']}")
# #             with st.expander("📄 View Summary", expanded=False):
# #                 st.write(summaries[idx]["summary"])


# # # ============================================================
# # # PDF REPORT GENERATOR (STYLE A: CLEAN PROFESSIONAL)
# # # ============================================================

# # def generate_pdf_report(summaries):
# #     buffer = BytesIO()
# #     doc = SimpleDocTemplate(buffer, pagesize=letter)
# #     styles = getSampleStyleSheet()
# #     elements = []

# #     title = Paragraph("<b>News Research Report</b>", styles["Title"])
# #     elements.append(title)
# #     elements.append(Spacer(1, 20))

# #     timestamp = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
# #                           styles["Normal"])
# #     elements.append(timestamp)
# #     elements.append(Spacer(1, 20))

# #     for idx, article in enumerate(summaries):
# #         elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
# #         elements.append(Paragraph(f"URL: {article['url']}", styles["Normal"]))
# #         elements.append(Spacer(1, 10))

# #         clean_summary = article['summary']
# #         clean_summary = clean_summary.replace("**", "")  # remove markdown bold markers
# #         clean_summary = clean_summary.replace("\n", "<br/>")  # newlines to HTML breaks
        
# #         elements.append(Paragraph(clean_summary, styles["Normal"]))
# #         elements.append(Spacer(1, 20))

# #     doc.build(elements)
# #     buffer.seek(0)
# #     return buffer


# # if "summaries" in st.session_state:
# #     pdf_buffer = generate_pdf_report(st.session_state["summaries"])
# #     st.download_button(
# #         label="📄 Download PDF Report",
# #         data=pdf_buffer,
# #         file_name="news_report.pdf",
# #         mime="application/pdf"
# #     )


# # # ============================================================
# # # QUESTION ANSWERING
# # # ============================================================

# # st.subheader("🔍 Ask a Question About the Articles:")
# # query = st.text_input("Your Question:")

# # if query:

# #     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# #     vector_store = FAISS.load_local(
# #         "faiss_index",
# #         embeddings,
# #         allow_dangerous_deserialization=True
# #     )

# #     chain = RetrievalQAWithSourcesChain.from_llm(
# #         llm=qa_llm,
# #         retriever=vector_store.as_retriever()
# #     )

# #     result = chain({"question": query}, return_only_outputs=True)

# #     st.header("Answer:")
# #     st.write(result["answer"])

# #     st.subheader("Sources:")
# #     st.write(result["sources"])



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
# #  GRADIENT LUXURY CSS
# # ==============================
# st.markdown("""
# <style>

#     /* GLOBAL BACKGROUND GRADIENT */
#     .stApp {
#         background: linear-gradient(135deg, #f3e7ff, #e3f0ff, #fdf2ff);
#         background-size: 300% 300%;
#         animation: gradientFlow 12s ease infinite;
#         font-family: "Inter", sans-serif;
#     }

#     @keyframes gradientFlow {
#         0% {background-position: 0% 50%;}
#         50% {background-position: 100% 50%;}
#         100% {background-position: 0% 50%;}
#     }

#     /* HERO HEADER */
#     .hero {
#         padding: 2.2rem 1rem;
#         border-radius: 18px;
#         text-align: center;
#         background: linear-gradient(135deg, rgba(120,70,255,0.25), rgba(255,100,150,0.25));
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(255,255,255,0.4);
#         box-shadow: 0px 8px 25px rgba(120,70,255,0.15);
#         margin-bottom: 2rem;
#     }

#     .hero h1 {
#         font-size: 2.7rem !important;
#         font-weight: 800 !important;
#         background: linear-gradient(to right, #7936ff, #ff2da5);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }

#     /* SIDEBAR */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #faf5ff, #f7f2ff);
#         border-right: 1px solid rgba(150,150,150,0.2);
#     }

#     .sidebar-title {
#         font-size: 1.25rem;
#         font-weight: 700;
#         padding-top: 1rem;
#         padding-bottom: 0.5rem;
#         background: linear-gradient(to right, #7c3aed, #ec4899);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }

#     /* INPUT FIELDS */
#     .stTextInput>div>div>input {
#         border-radius: 12px;
#         border: 1px solid #d0c8ff;
#         background: rgba(255,255,255,0.7);
#     }

#     /* LUXURY BUTTONS */
#     .stButton>button {
#         background: linear-gradient(135deg, #7c3aed, #d946ef);
#         border: none;
#         padding: 0.7rem 1.4rem;
#         border-radius: 12px;
#         color: white;
#         font-weight: 600;
#         box-shadow: 0px 4px 14px rgba(124,58,237,0.4);
#         transition: 0.25s;
#     }

#     .stButton>button:hover {
#         transform: translateY(-3px);
#         box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
#     }

#     /* DOWNLOAD BUTTON MATCHING UI */
#     .stDownloadButton>button {
#         background: linear-gradient(135deg, #7c3aed, #d946ef);
#         border: none;
#         padding: 0.7rem 1.4rem;
#         border-radius: 12px;
#         color: white !important;
#         font-weight: 600;
#         box-shadow: 0px 4px 14px rgba(124,58,237,0.4);
#         transition: 0.25s;
#     }

#     .stDownloadButton>button:hover {
#         transform: translateY(-3px);
#         box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
#     }

#     /* SUMMARY CARD */
#     .summary-card {
#         background: rgba(255,255,255,0.55);
#         padding: 1.4rem 1.6rem;
#         border-radius: 16px;
#         border: 1px solid rgba(255,255,255,0.65);
#         backdrop-filter: blur(14px);
#         box-shadow: 0px 6px 22px rgba(150,50,250,0.15);
#         margin-bottom: 1.2rem;
#     }

#     /* DIVIDER */
#     .divider {
#         border-top: 1px solid rgba(130,60,255,0.4);
#         margin-top: 1.5rem;
#         margin-bottom: 1.5rem;
#     }

#     /* SMALL SOURCE TEXT */
#     .small-source {
#         font-size: 0.82rem;
#         color: #5a4a70;
#         opacity: 0.85;
#     }

# </style>
# """, unsafe_allow_html=True)


# # ==============================
# # API KEY
# # ==============================
# GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# # ==============================
# # HERO HEADER
# # ==============================
# st.markdown("""
# <div class="hero">
#     <h1>News Research Tool</h1>
# </div>
# """, unsafe_allow_html=True)

# st.sidebar.markdown("<div class='sidebar-title'>News Article URLs</div>", unsafe_allow_html=True)


# # ==============================
# # URL INPUTS
# # ==============================
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
# summary_llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0.2,
#     groq_api_key=GROQ_API_KEY,
#     max_tokens=500
# )

# qa_llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0.7,
#     groq_api_key=GROQ_API_KEY,
#     max_tokens=500
# )


# # ============================================================
# # PROCESS URLs
# # ============================================================
# if process_url_clicked:

#     if len(urls) == 0:
#         st.warning("Please enter at least one URL.")
#         st.stop()

#     loader = UnstructuredURLLoader(urls=urls)
#     main_placeholder.text("📥 Loading article data...")
#     data = loader.load()

#     for d in data:
#         d.page_content = d.page_content.strip()

#     text_splitter = RecursiveCharacterTextSplitter(
#         separators=["\n\n", "\n", ".", " "],
#         chunk_size=1000,
#         chunk_overlap=100,
#     )

#     docs = text_splitter.split_documents(documents=data)

#     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#     vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)
#     vector_store.save_local("faiss_index")

#     summaries = []

#     for i, article in enumerate(data):
#         content = article.page_content[:4000]

#         prompt = f"""
#         Provide a structured summary:
#         - Overview
#         - Key takeaways
#         - Key insights

#         ARTICLE:
#         {content}
#         """

#         response = summary_llm.invoke(prompt)

#         summaries.append({
#             "url": article.metadata.get("source", f"Article {i+1}"),
#             "summary": response.content
#         })

#     st.session_state["summaries"] = summaries

#     main_placeholder.text("✅ Processing Completed!")


# # ============================================================
# # SHOW SUMMARIES
# # ============================================================
# if "summaries" in st.session_state:

#     summaries = st.session_state["summaries"]

#     st.subheader("📝 Article Summaries")
#     st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

#     tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

#     for idx, tab in enumerate(tabs):
#         with tab:
#             st.markdown(f"### 🌐 Source: {summaries[idx]['url']}")
#             st.markdown(f"""
#             <div class="summary-card">
#                 {summaries[idx]['summary']}
#             </div>
#             """, unsafe_allow_html=True)


# # ============================================================
# # PDF GENERATION
# # ============================================================
# def generate_pdf_report(summaries):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     elements = []

#     title = Paragraph("<b>News Research Report</b>", styles["Title"])
#     elements.append(title)
#     elements.append(Spacer(1, 20))

#     timestamp = Paragraph(
#         f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#         styles["Normal"]
#     )
#     elements.append(timestamp)
#     elements.append(Spacer(1, 20))

#     for idx, article in enumerate(summaries):
#         elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
#         elements.append(Paragraph(f"URL: {article['url']}", styles["Normal"]))
#         elements.append(Spacer(1, 10))

#         clean = (
#             article["summary"]
#             .replace("**", "")
#             .replace("\n", "<br/>")
#         )

#         elements.append(Paragraph(clean, styles["Normal"]))
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
#     st.markdown(
#         f"<div class='small-source'>{result['sources']}</div>",
#         unsafe_allow_html=True
#     )





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
#  GRADIENT LUXURY CSS + DARK MODE FIX
# ==============================
st.markdown("""
<style>

    /* ==========================================
       DARK MODE FIX (FORCE TEXT DARK)
       ========================================== */
    html, body, [class*="st-"], .stApp {
        color: #1a1a1a !important;
    }
    p, div, span, label, h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    @media (prefers-color-scheme: dark) {
        html, body, [class*="st-"], .stApp,
        p, div, span, label, h1, h2, h3, h4, h5, h6 {
            color: #1a1a1a !important;
        }
    }

    /* ==========================================
       BACKGROUND GRADIENT
       ========================================== */
    .stApp {
        background: linear-gradient(135deg, #f3e7ff, #e3f0ff, #fdf2ff);
        background-size: 300% 300%;
        animation: gradientFlow 12s ease infinite;
        font-family: "Inter", sans-serif;
    }

    @keyframes gradientFlow {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* ==========================================
       HERO HEADER
       ========================================== */
    .hero {
        padding: 2.2rem 1rem;
        border-radius: 18px;
        text-align: center;
        background: linear-gradient(135deg, rgba(120,70,255,0.25), rgba(255,100,150,0.25));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0px 8px 25px rgba(120,70,255,0.15);
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 2.7rem !important;
        font-weight: 800 !important;
        background: linear-gradient(to right, #7936ff, #ff2da5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ==========================================
       SIDEBAR
       ========================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #faf5ff, #f7f2ff);
        border-right: 1px solid rgba(150,150,150,0.2);
    }
    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        background: linear-gradient(to right, #7c3aed, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ==========================================
       INPUT STYLING
       ========================================== */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #d0c8ff;
        background: rgba(255,255,255,0.7);
    }

    /* ==========================================
       LUXURY GRADIENT BUTTONS
       ========================================== */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed, #d946ef);
        border: none;
        padding: 0.7rem 1.4rem;
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
        box-shadow: 0px 4px 14px rgba(124,58,237,0.4);
        transition: 0.25s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
    }

    /* ==========================================
       DOWNLOAD BUTTON MATCHING STYLE
       ========================================== */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #7c3aed, #d946ef);
        border: none;
        padding: 0.7rem 1.4rem;
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
        box-shadow: 0px 4px 14px rgba(124,58,237,0.4);
        transition: 0.25s;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
    }

    /* ==========================================
       SUMMARY CARDS
       ========================================== */
    .summary-card {
        background: rgba(255,255,255,0.55);
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.65);
        backdrop-filter: blur(14px);
        box-shadow: 0px 6px 22px rgba(150,50,250,0.15);
        margin-bottom: 1.2rem;
    }

    /* ==========================================
       UPDATED LUXURY TABS (ONLY CHANGE)
       ========================================== */
    .stTabs [data-baseweb="tabs"] {
        gap: 14px !important;
        padding-bottom: 14px !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: #f0f0f0 !important;
        padding: 10px 26px !important;
        border-radius: 14px !important;
        border: 1px solid #e2e2e2 !important;
        font-family: "Playfair Display", serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: #403b4a !important;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.12);
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px);
        background: #ffffff !important;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e8e8e8, #ffffff) !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.22);
        font-weight: 700 !important;
    }

    /* ==========================================
       SMALL SOURCE TEXT
       ========================================== */
    .small-source {
        font-size: 0.82rem;
        color: #5a4a70;
        opacity: 0.85;
    }

</style>
""", unsafe_allow_html=True)



# ==============================
# API KEY
# ==============================
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# ==============================
# HERO HEADER
# ==============================
st.markdown("""
<div class="hero">
    <h1>News Research Tool</h1>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-title'>News Article URLs</div>", unsafe_allow_html=True)


# ==============================
# URL INPUTS
# ==============================
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

    docs = text_splitter.split_documents(documents=data)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)
    vector_store.save_local("faiss_index")

    summaries = []

    for i, article in enumerate(data):
        content = article.page_content[:4000]

        prompt = f"""
        Provide a structured summary:
        - Overview
        - Key takeaways
        - Key insights

        ARTICLE:
        {content}
        """

        response = summary_llm.invoke(prompt)

        summaries.append({
            "url": article.metadata.get("source", f"Article {i+1}"),
            "summary": response.content
        })

    st.session_state["summaries"] = summaries

    main_placeholder.text("✅ Processing Completed!")



# ============================================================
# SHOW SUMMARIES
# ============================================================
if "summaries" in st.session_state:

    summaries = st.session_state["summaries"]

    st.subheader("Article Summaries")

    tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

    for idx, tab in enumerate(tabs):
        with tab:
            st.markdown(f"#### Source: {summaries[idx]['url']}")
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

    timestamp = Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"]
    )
    elements.append(timestamp)
    elements.append(Spacer(1, 20))

    for idx, article in enumerate(summaries):
        elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
        elements.append(Paragraph(f"URL: {article['url']}", styles["Normal"]))
        elements.append(Spacer(1, 10))

        clean = (
            article["summary"]
            .replace("**", "")
            .replace("\n", "<br/>")
        )

        elements.append(Paragraph(clean, styles["Normal"]))
        elements.append(Spacer(1, 20))

    doc.build(elements)
    buffer.seek(0)
    return buffer


if "summaries" in st.session_state:
    pdf_buffer = generate_pdf_report(st.session_state["summaries"])
    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name="news_report.pdf",
        mime="application/pdf"
    )



# ============================================================
# QUESTION ANSWERING
# ============================================================
st.subheader(" Ask a Question About the Articles:")
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
    st.markdown(
        f"<div class='small-source'>{result['sources']}</div>",
        unsafe_allow_html=True
    )

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
# # #  GRADIENT LUXURY CSS + DARK MODE 
# # # ==============================
# # st.markdown("""
# # <style>

    
# #     html, body, [class*="st-"], .stApp {
# #         color: #1a1a1a !important;
# #     }
# #     p, div, span, label, h1, h2, h3, h4, h5, h6 {
# #         color: #1a1a1a !important;
# #     }
# #     @media (prefers-color-scheme: dark) {
# #         html, body, [class*="st-"], .stApp,
# #         p, div, span, label, h1, h2, h3, h4, h5, h6 {
# #             color: #1a1a1a !important;
# #         }
# #     }

# #     /* ==========================================
# #        BACKGROUND GRADIENT
# #        ========================================== */
# #     .stApp {
# #         background: linear-gradient(135deg, #f3e7ff, #e3f0ff, #fdf2ff);
# #         background-size: 300% 300%;
# #         animation: gradientFlow 12s ease infinite;
# #         font-family: "Inter", sans-serif;
# #     }

# #     @keyframes gradientFlow {
# #         0% {background-position: 0% 50%;}
# #         50% {background-position: 100% 50%;}
# #         100% {background-position: 0% 50%;}
# #     }

# #     /* ==========================================
# #        HERO HEADER
# #        ========================================== */
# #     .hero {
# #         padding: 2.2rem 1rem;
# #         border-radius: 18px;
# #         text-align: center;
# #         background: linear-gradient(135deg, rgba(120,70,255,0.25), rgba(255,100,150,0.25));
# #         backdrop-filter: blur(10px);
# #         border: 1px solid rgba(255,255,255,0.4);
# #         box-shadow: 0px 8px 25px rgba(120,70,255,0.15);
# #         margin-bottom: 2rem;
# #     }
# #     .hero h1 {
# #         font-size: 2.7rem !important;
# #         font-weight: 800 !important;
# #         background: linear-gradient(to right, #7936ff, #ff2da5);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #     }

# #     /* ==========================================
# #        SIDEBAR
# #        ========================================== */
# #     [data-testid="stSidebar"] {
# #         background: linear-gradient(180deg, #faf5ff, #f7f2ff);
# #         border-right: 1px solid rgba(150,150,150,0.2);
# #     }
# #     .sidebar-title {
# #         font-size: 1.25rem;
# #         font-weight: 700;
# #         padding-top: 1rem;
# #         padding-bottom: 0.5rem;
# #         background: linear-gradient(to right, #7c3aed, #ec4899);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #     }

# #     /* ==========================================
# #        INPUT STYLING
# #        ========================================== */
# #     .stTextInput>div>div>input {
# #         border-radius: 12px;
# #         border: 1px solid #d0c8ff;
# #         background: rgba(255,255,255,0.7);
# #     }

# #     /* ==========================================
# #        LUXURY GRADIENT BUTTONS
# #        ========================================== */
# #     .stButton>button {
# #         background: linear-gradient(135deg, #7c3aed, #d946ef);
# #         border: none;
# #         padding: 0.7rem 1.4rem;
# #         border-radius: 12px;
# #         color: white !important;
# #         font-weight: 600;
# #         box-shadow: 0px 4px 14px rgba(124,58,237,0.4);
# #         transition: 0.25s;
# #     }
# #     .stButton>button:hover {
# #         transform: translateY(-3px);
# #         box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
# #     }

# #     /* ==========================================
# #        DOWNLOAD BUTTON MATCHING STYLE
# #        ========================================== */
# #     .stDownloadButton>button {
# #         background: linear-gradient(135deg, #7c3aed, #d946ef);
# #         border: none;
# #         padding: 0.7rem 1.4rem;
# #         border-radius: 12px;
# #         color: white !important;
# #         font-weight: 600;
# #         box-shadow: 0px 4px 14px rgba(124,58,237,0.4);
# #         transition: 0.25s;
# #     }
# #     .stDownloadButton>button:hover {
# #         transform: translateY(-3px);
# #         box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
# #     }

# #     /* ==========================================
# #        SUMMARY CARDS
# #        ========================================== */
# #     .summary-card {
# #         background: rgba(255,255,255,0.55);
# #         padding: 1.4rem 1.6rem;
# #         border-radius: 16px;
# #         border: 1px solid rgba(255,255,255,0.65);
# #         backdrop-filter: blur(14px);
# #         box-shadow: 0px 6px 22px rgba(150,50,250,0.15);
# #         margin-bottom: 1.2rem;
# #     }

# #     /* ==========================================
# #        UPDATED LUXURY TABS (ONLY CHANGE)
# #        ========================================== */
# #     .stTabs [data-baseweb="tabs"] {
# #         gap: 14px !important;
# #         padding-bottom: 14px !important;
# #     }

# #     .stTabs [data-baseweb="tab"] {
# #         background: #f0f0f0 !important;
# #         padding: 10px 26px !important;
# #         border-radius: 14px !important;
# #         border: 1px solid #e2e2e2 !important;
# #         font-family: "Playfair Display", serif !important;
# #         font-weight: 600 !important;
# #         font-size: 1rem !important;
# #         color: #403b4a !important;
# #         box-shadow: 0px 4px 14px rgba(0,0,0,0.12);
# #         transition: all 0.25s ease;
# #     }

# #     .stTabs [data-baseweb="tab"]:hover {
# #         transform: translateY(-3px);
# #         background: #ffffff !important;
# #         box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
# #     }

# #     .stTabs [aria-selected="true"] {
# #         background: linear-gradient(135deg, #e8e8e8, #ffffff) !important;
# #         color: #000000 !important;
# #         border: 1px solid #cccccc !important;
# #         box-shadow: 0px 6px 20px rgba(0,0,0,0.22);
# #         font-weight: 700 !important;
# #     }

# #     /* ==========================================
# #        SMALL SOURCE TEXT
# #        ========================================== */
# #     .small-source {
# #         font-size: 0.82rem;
# #         color: #5a4a70;
# #         opacity: 0.85;
# #     }

# # </style>
# # """, unsafe_allow_html=True)



# # # ==============================
# # # API KEY
# # # ==============================
# # GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# # # ==============================
# # # HERO HEADER
# # # ==============================
# # st.markdown("""
# # <div class="hero">
# #     <h1>News Research Tool</h1>
# # </div>
# # """, unsafe_allow_html=True)

# # st.sidebar.markdown("<div class='sidebar-title'>News Article URLs</div>", unsafe_allow_html=True)


# # # ==============================
# # # URL INPUTS
# # # ==============================
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
# # summary_llm = ChatGroq(
# #     model="llama-3.1-8b-instant",
# #     temperature=0.2,
# #     groq_api_key=GROQ_API_KEY,
# #     max_tokens=500
# # )

# # qa_llm = ChatGroq(
# #     model="llama-3.3-70b-versatile",
# #     temperature=0.7,
# #     groq_api_key=GROQ_API_KEY,
# #     max_tokens=500
# # )



# # # ============================================================
# # # PROCESS URLs
# # # ============================================================
# # if process_url_clicked:

# #     if len(urls) == 0:
# #         st.warning("Please enter at least one URL.")
# #         st.stop()

# #     loader = UnstructuredURLLoader(urls=urls)
# #     main_placeholder.text("📥 Loading article data...")
# #     data = loader.load()

# #     for d in data:
# #         d.page_content = d.page_content.strip()

# #     text_splitter = RecursiveCharacterTextSplitter(
# #         separators=["\n\n", "\n", ".", " "],
# #         chunk_size=1000,
# #         chunk_overlap=100,
# #     )

# #     docs = text_splitter.split_documents(documents=data)

# #     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# #     vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)
# #     vector_store.save_local("faiss_index")

# #     summaries = []

# #     for i, article in enumerate(data):
# #         content = article.page_content[:4000]

# #         prompt = f"""
# #         Provide a structured summary:
# #         - Overview
# #         - Key takeaways
# #         - Key insights

# #         ARTICLE:
# #         {content}
# #         """

# #         response = summary_llm.invoke(prompt)

# #         summaries.append({
# #             "url": article.metadata.get("source", f"Article {i+1}"),
# #             "summary": response.content
# #         })

# #     st.session_state["summaries"] = summaries

# #     main_placeholder.text("✅ Processing Completed!")



# # # ============================================================
# # # SHOW SUMMARIES
# # # ============================================================
# # if "summaries" in st.session_state:

# #     summaries = st.session_state["summaries"]

# #     st.subheader("Article Summaries")

# #     tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

# #     for idx, tab in enumerate(tabs):
# #         with tab:
# #             st.markdown(f"#### Source: {summaries[idx]['url']}")
# #             st.markdown(f"""
# #             <div class="summary-card">
# #                 {summaries[idx]['summary']}
# #             </div>
# #             """, unsafe_allow_html=True)



# # # ============================================================
# # # PDF GENERATION
# # # ============================================================
# # def generate_pdf_report(summaries):
# #     buffer = BytesIO()
# #     doc = SimpleDocTemplate(buffer, pagesize=letter)
# #     styles = getSampleStyleSheet()
# #     elements = []

# #     title = Paragraph("<b>News Research Report</b>", styles["Title"])
# #     elements.append(title)
# #     elements.append(Spacer(1, 20))

# #     timestamp = Paragraph(
# #         f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
# #         styles["Normal"]
# #     )
# #     elements.append(timestamp)
# #     elements.append(Spacer(1, 20))

# #     for idx, article in enumerate(summaries):
# #         elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
# #         elements.append(Paragraph(f"URL: {article['url']}", styles["Normal"]))
# #         elements.append(Spacer(1, 10))

# #         clean = (
# #             article["summary"]
# #             .replace("**", "")
# #             .replace("\n", "<br/>")
# #         )

# #         elements.append(Paragraph(clean, styles["Normal"]))
# #         elements.append(Spacer(1, 20))

# #     doc.build(elements)
# #     buffer.seek(0)
# #     return buffer


# # if "summaries" in st.session_state:
# #     pdf_buffer = generate_pdf_report(st.session_state["summaries"])
# #     st.download_button(
# #         label="Download PDF Report",
# #         data=pdf_buffer,
# #         file_name="news_report.pdf",
# #         mime="application/pdf"
# #     )



# # # ============================================================
# # # QUESTION ANSWERING
# # # ============================================================
# # st.subheader(" Ask a Question About the Articles:")
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
# #     st.markdown(
# #         f"<div class='small-source'>{result['sources']}</div>",
# #         unsafe_allow_html=True
# #     )




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


# # ============================================================
# #  GLOBAL LUXURY STYLING (Gradient + Glass + Tabs)
# # ============================================================
# st.markdown("""
# <style>

#     /* MAKE ALL TEXT BLACK ALWAYS — FIX FOR DARK MODE */
#     html, body, [class*="st-"], .stApp {
#         color: #1a1a1a !important;
#     }
#     p, div, span, label, h1, h2, h3, h4, h5, h6 {
#         color: #1a1a1a !important;
#     }
#     @media (prefers-color-scheme: dark) {
#         html, body, [class*="st-"], .stApp,
#         p, div, span, label, h1, h2, h3, h4, h5, h6 {
#             color: #1a1a1a !important;
#         }
#     }

#     /* =======================================================
#        APP BACKGROUND GLOBAL
#        ======================================================= */
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

#     /* =======================================================
#        LUXURY BUTTONS
#        ======================================================= */
#     .stButton>button {
#         background: linear-gradient(135deg, #7c3aed, #d946ef);
#         border: none;
#         padding: 0.7rem 1.4rem;
#         border-radius: 12px;
#         color: white !important;
#         font-weight: 600;
#         box-shadow: 0px 4px 14px rgba(124,58,237,0.4);
#         transition: 0.25s;
#     }
#     .stButton>button:hover {
#         transform: translateY(-3px);
#         box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
#     }

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

#     /* =======================================================
#        SUMMARY CARD
#        ======================================================= */
#     .summary-card {
#         background: rgba(255,255,255,0.55);
#         padding: 1.4rem 1.6rem;
#         border-radius: 16px;
#         border: 1px solid rgba(255,255,255,0.65);
#         backdrop-filter: blur(14px);
#         box-shadow: 0px 6px 22px rgba(150,50,250,0.15);
#         margin-bottom: 1.2rem;
#     }

#     /* =======================================================
#        PREMIUM LUXURY TABS
#        ======================================================= */
#     .stTabs [data-baseweb="tabs"] {
#         gap: 14px !important;
#         padding-bottom: 14px !important;
#     }

#     .stTabs [data-baseweb="tab"] {
#         background: #f0f0f0 !important;
#         padding: 10px 26px !important;
#         border-radius: 14px !important;
#         border: 1px solid #e2e2e2 !important;
#         font-family: "Playfair Display", serif !important;
#         font-weight: 600 !important;
#         font-size: 1rem !important;
#         color: #403b4a !important;
#         box-shadow: 0px 4px 14px rgba(0,0,0,0.12);
#         transition: all 0.25s ease;
#     }

#     .stTabs [data-baseweb="tab"]:hover {
#         transform: translateY(-3px);
#         background: #ffffff !important;
#         box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
#     }

#     .stTabs [aria-selected="true"] {
#         background: linear-gradient(135deg, #e8e8e8, #ffffff) !important;
#         color: #000000 !important;
#         border: 1px solid #cccccc !important;
#         box-shadow: 0px 6px 20px rgba(0,0,0,0.22);
#         font-weight: 700 !important;
#     }

#     .small-source {
#         font-size: 0.82rem;
#         color: #5a4a70;
#         opacity: 0.85;
#     }

#     /* =======================================================
#        CINEMATIC LANDING PAGE
#        ======================================================= */
#     .landing-container {
#         height: 88vh;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         text-align: center;
#         flex-direction: column;
#         padding: 2rem;
#     }

#     .landing-hero {
#         background: rgba(255,255,255,0.25);
#         padding: 3rem 3rem;
#         border-radius: 28px;
#         backdrop-filter: blur(18px);
#         border: 1px solid rgba(255,255,255,0.45);
#         box-shadow: 0px 10px 35px rgba(120,50,220,0.18);
#         animation: fadeIn 1.2s ease;
#     }

#     .landing-title {
#         font-size: 3.2rem !important;
#         font-weight: 900 !important;
#         background: linear-gradient(90deg, #6b2dff, #ff1493);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 1rem;
#     }

#     .landing-subtitle {
#         font-size: 1.15rem;
#         opacity: 0.75;
#         margin-bottom: 2rem;
#     }

#     /* Glass button */
#     .glass-button {
#         padding: 0.9rem 2rem;
#         border-radius: 14px;
#         background: rgba(255,255,255,0.25);
#         border: 1px solid rgba(255,255,255,0.55);
#         backdrop-filter: blur(12px);
#         color: #4a0072 !important;
#         font-size: 1.1rem;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.25s ease;
#         box-shadow: 0px 6px 18px rgba(120,50,220,0.25);
#     }

#     .glass-button:hover {
#         transform: translateY(-4px);
#         background: rgba(255,255,255,0.45);
#         box-shadow: 0px 8px 24px rgba(120,50,220,0.38);
#     }

#     @keyframes fadeIn {
#         from {opacity: 0; transform: translateY(25px);}
#         to   {opacity: 1; transform: translateY(0);}
#     }

# </style>
# """, unsafe_allow_html=True)




# # ============================================================
# # SESSION STATE PAGE CONTROLLER
# # ============================================================
# if "page" not in st.session_state:
#     st.session_state.page = "landing"



# # ============================================================
# # LANDING PAGE FUNCTION (CINEMATIC)
# # ============================================================
# def show_landing_page():
#     st.markdown("""
#     <div class="landing-container">
#         <div class="landing-hero">
#             <div class="landing-title">News Research Tool</div>
#             <div class="landing-subtitle">
#                 AI-powered summaries, insights & fast research for long-form news articles.
#             </div>
#             <button class="glass-button" onclick="window.location.reload();">
#                 Get Started
#             </button>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     st.stop()



# # ============================================================
# # MAIN APPLICATION FUNCTION
# # ============================================================
# def show_main_app():

#     # ==============================
#     # HEADER
#     # ==============================
#     st.markdown("""
#     <div style="padding: 2rem 1rem; text-align:center;">
#         <h1 style="background: linear-gradient(90deg,#7c3aed,#d946ef);
#             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
#             font-weight:800; font-size:2.4rem;">
#             News Research Tool
#         </h1>
#     </div>
#     """, unsafe_allow_html=True)

#     st.sidebar.markdown(
#         "<div class='sidebar-title'>News Article URLs</div>",
#         unsafe_allow_html=True
#     )

#     # ==============================
#     # URL INPUTS
#     # ==============================
#     urls = []
#     for i in range(3):
#         url = st.sidebar.text_input(f"Enter URL {i+1}", key=f"url_{i}")
#         if url:
#             urls.append(url)

#     process_url_clicked = st.sidebar.button("Process URLs")

#     main_placeholder = st.empty()

#     # ==============================
#     # LLMs
#     # ==============================
#     summary_llm = ChatGroq(
#         model="llama-3.1-8b-instant",
#         temperature=0.2,
#         groq_api_key=GROQ_API_KEY,
#         max_tokens=500
#     )

#     qa_llm = ChatGroq(
#         model="llama-3.3-70b-versatile",
#         temperature=0.7,
#         groq_api_key=GROQ_API_KEY,
#         max_tokens=500
#     )

#     # ============================================================
#     # PROCESS URLs
#     # ============================================================
#     if process_url_clicked:

#         if len(urls) == 0:
#             st.warning("Please enter at least one URL.")
#             st.stop()

#         loader = UnstructuredURLLoader(urls=urls)
#         main_placeholder.text("📥 Loading article data...")
#         data = loader.load()

#         for d in data:
#             d.page_content = d.page_content.strip()

#         text_splitter = RecursiveCharacterTextSplitter(
#             separators=["\n\n", "\n", ".", " "],
#             chunk_size=1000,
#             chunk_overlap=100,
#         )

#         docs = text_splitter.split_documents(documents=data)

#         embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#         vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)
#         vector_store.save_local("faiss_index")

#         summaries = []

#         for i, article in enumerate(data):
#             content = article.page_content[:4000]

#             prompt = f"""
#             Provide a structured summary:
#             - Overview
#             - Key takeaways
#             - Key insights

#             ARTICLE:
#             {content}
#             """

#             response = summary_llm.invoke(prompt)

#             summaries.append({
#                 "url": article.metadata.get("source", f"Article {i+1}"),
#                 "summary": response.content
#             })

#         st.session_state["summaries"] = summaries

#         main_placeholder.text("✅ Processing Completed!")



#     # ============================================================
#     # SHOW SUMMARIES
#     # ============================================================
#     if "summaries" in st.session_state:

#         summaries = st.session_state["summaries"]

#         st.subheader("Article Summaries")

#         tabs = st.tabs([f"Article {i+1}" for i in range(len(summaries))])

#         for idx, tab in enumerate(tabs):
#             with tab:
#                 st.markdown(f"#### Source: {summaries[idx]['url']}")
#                 st.markdown(
#                     f"<div class='summary-card'>{summaries[idx]['summary']}</div>",
#                     unsafe_allow_html=True
#                 )



#     # ============================================================
#     # PDF GENERATION
#     # ============================================================
#     def generate_pdf_report(summaries):
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)
#         styles = getSampleStyleSheet()
#         elements = []

#         title = Paragraph("<b>News Research Report</b>", styles["Title"])
#         elements.append(title)
#         elements.append(Spacer(1, 20))

#         timestamp = Paragraph(
#             f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#             styles["Normal"]
#         )
#         elements.append(timestamp)
#         elements.append(Spacer(1, 20))

#         for idx, article in enumerate(summaries):
#             elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
#             elements.append(Paragraph(f"URL: {article['url']}", styles["Normal"]))
#             elements.append(Spacer(1, 10))

#             clean = (
#                 article["summary"]
#                 .replace("**", "")
#                 .replace("\n", "<br/>")
#             )

#             elements.append(Paragraph(clean, styles["Normal"]))
#             elements.append(Spacer(1, 20))

#         doc.build(elements)
#         buffer.seek(0)
#         return buffer


#     if "summaries" in st.session_state:
#         pdf_buffer = generate_pdf_report(st.session_state["summaries"])
#         st.download_button(
#             label="Download PDF Report",
#             data=pdf_buffer,
#             file_name="news_report.pdf",
#             mime="application/pdf"
#         )



#     # ============================================================
#     # QUESTION ANSWERING
#     # ============================================================
#     st.subheader("Ask a Question About the Articles:")
#     query = st.text_input("Your Question:")

#     if query:

#         embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#         vector_store = FAISS.load_local(
#             "faiss_index",
#             embeddings,
#             allow_dangerous_deserialization=True
#         )

#         chain = RetrievalQAWithSourcesChain.from_llm(
#             llm=qa_llm,
#             retriever=vector_store.as_retriever()
#         )

#         result = chain({"question": query}, return_only_outputs=True)

#         st.header("Answer:")
#         st.write(result["answer"])

#         st.subheader("Sources:")
#         st.markdown(
#             f"<div class='small-source'>{result['sources']}</div>",
#             unsafe_allow_html=True
#         )



# # ============================================================
# # PAGE ROUTER
# # ============================================================
# if st.session_state.page == "landing":
#     show_landing_page()
# else:
#     show_main_app()



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


# ============================================================
#  GLOBAL LUXURY STYLING  (GRADIENT + GLASS + TABS + HIDING BUTTON)
# ============================================================
st.markdown("""
<style>

    /* Hide the internal Streamlit button */
    button[aria-label="start_app_internal"] {
        display: none !important;
    }

    /* Force black text always */
    html, body, [class*="st-"], .stApp {
        color: #1a1a1a !important;
    }

    /* Background gradient */
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

    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(to right, #7c3aed, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #d0c8ff;
        background: rgba(255,255,255,0.8);
    }

    /* Buttons */
    .stButton>button,
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
    .stButton>button:hover,
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 6px 18px rgba(124,58,237,0.55);
    }

    /* Summary Card */
    .summary-card {
        background: rgba(255,255,255,0.55);
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.65);
        backdrop-filter: blur(14px);
        box-shadow: 0px 6px 22px rgba(150,50,250,0.15);
        margin-bottom: 1.2rem;
    }

    /* Premium Tabs */
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
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e8e8e8, #ffffff) !important;
        border: 1px solid #ccc !important;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.22);
        font-weight: 700 !important;
    }

    .small-source {
        font-size: 0.82rem;
        opacity: 0.85;
    }

    /* Landing Page */
    .landing-container {
        height: 90vh;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
    }
    .landing-hero {
        background: rgba(255,255,255,0.30);
        padding: 3rem 3rem;
        width: 70%;
        border-radius: 28px;
        backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.45);
        box-shadow: 0px 10px 35px rgba(120,50,220,0.18);
        animation: fadeIn 1.2s ease;
    }
    .landing-title {
        font-size: 3.3rem !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #6b2dff, #ff1493);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.2rem;
    }
    .landing-subtitle {
        font-size: 1.25rem;
        opacity: 0.8;
        margin-bottom: 2.4rem;
    }
    .feature-box {
        background: rgba(255,255,255,0.35);
        backdrop-filter: blur(12px);
        border-radius: 18px;
        padding: 1rem 1.4rem;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0px 6px 16px rgba(120,50,220,0.15);
        margin-bottom: 1rem;
        font-size: 1rem;
    }
    .glass-button {
        padding: 0.9rem 2rem;
        border-radius: 14px;
        background: rgba(255,255,255,0.25);
        border: 1px solid rgba(255,255,255,0.55);
        backdrop-filter: blur(12px);
        color: #4a0072 !important;
        font-size: 1.1rem;
        font-weight: 600;
        transition: 0.25s;
        cursor: pointer;
        margin-top: 1rem;
        box-shadow: 0px 8px 20px rgba(120,50,220,0.3);
    }
    .glass-button:hover {
        transform: translateY(-4px);
        background: rgba(255,255,255,0.45);
        box-shadow: 0px 10px 28px rgba(120,50,220,0.45);
    }

    @keyframes fadeIn {
        from {opacity:0; transform:translateY(25px);}
        to   {opacity:1; transform:translateY(0);}
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# PAGE STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "landing"


# ============================================================
# LANDING PAGE
# ============================================================
def show_landing_page():

    # HIDDEN INTERNAL BUTTON (triggered by HTML button)
    hidden_start = st.button("start_app_internal", key="start_hidden_button")

    if hidden_start:
        st.session_state.page = "app"
        st.experimental_rerun()

    st.markdown("""
    <div class="landing-container">

        <div class="landing-hero">

            <div class="landing-title">News Research Tool</div>

            <div class="landing-subtitle">
                AI-powered summaries, insights, and research for long-form news articles.
            </div>

            <div class="feature-box">Smart automated summarization</div>
            <div class="feature-box">Key insights & takeaways</div>
            <div class="feature-box">Instant PDF report creation</div>

            <button class="glass-button"
                onclick="document.querySelector('button[aria-label=\'start_app_internal\']').click();">
                Get Started
            </button>

        </div>

        <div style="
            text-align:center;
            margin-top:40px;
            opacity:0.75;
            font-family:'Playfair Display', serif;
            font-size:1rem;">
            Made with ❤️ by <b>MD</b>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ============================================================
# MAIN APP
# ============================================================
def show_main_app():

    st.markdown("""
    <div style='padding:2rem 1rem; text-align:center;'>
        <h1 style="
            background: linear-gradient(90deg,#7c3aed,#d946ef);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            font-weight:800;
            font-size:2.4rem;">
            News Research Tool
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<div class='sidebar-title'>News Article URLs</div>", unsafe_allow_html=True)

    urls = []
    for i in range(3):
        u = st.sidebar.text_input(f"Enter URL {i+1}", key=f"url_{i}")
        if u:
            urls.append(u)

    process_clicked = st.sidebar.button("Process URLs")
    main_area = st.empty()

    summary_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        groq_api_key=st.secrets["GROQ_API_KEY"],
        max_tokens=500
    )

    qa_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=st.secrets["GROQ_API_KEY"],
        max_tokens=500
    )

    if process_clicked:
        if len(urls) == 0:
            st.warning("Please enter at least one URL.")
            st.stop()

        loader = UnstructuredURLLoader(urls=urls)
        main_area.text("📥 Loading articles...")
        data = loader.load()

        for d in data:
            d.page_content = d.page_content.strip()

        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ".", " "],
            chunk_size=1000,
            chunk_overlap=100,
        )
        docs = splitter.split_documents(documents=data)

        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vec = FAISS.from_documents(documents=docs, embedding=embeddings)
        vec.save_local("faiss_index")

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

            resp = summary_llm.invoke(prompt)

            summaries.append({
                "url": article.metadata.get("source", f"Article {i+1}"),
                "summary": resp.content
            })

        st.session_state["summaries"] = summaries
        main_area.text("✅ Processing Completed!")

    if "summaries" in st.session_state:
        sums = st.session_state["summaries"]
        st.subheader("Article Summaries")

        tabs = st.tabs([f"Article {i+1}" for i in range(len(sums))])

        for idx, tab in enumerate(tabs):
            with tab:
                st.markdown(f"#### Source: {sums[idx]['url']}")
                st.markdown(f"<div class='summary-card'>{sums[idx]['summary']}</div>", unsafe_allow_html=True)

    def make_pdf(summaries):
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("<b>News Research Report</b>", styles["Title"]))
        elements.append(Spacer(1, 20))

        ts = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"])
        elements.append(ts)
        elements.append(Spacer(1, 20))

        for idx, art in enumerate(summaries):
            elements.append(Paragraph(f"<b>Article {idx+1}</b>", styles["Heading2"]))
            elements.append(Paragraph(f"URL: {art['url']}", styles["Normal"]))
            elements.append(Spacer(1, 10))

            clean = art["summary"].replace("**", "").replace("\n", "<br/>")
            elements.append(Paragraph(clean, styles["Normal"]))
            elements.append(Spacer(1, 20))

        doc.build(elements)
        buf.seek(0)
        return buf

    if "summaries" in st.session_state:
        pdf = make_pdf(st.session_state["summaries"])
        st.download_button(
            label="Download PDF Report",
            data=pdf,
            file_name="news_report.pdf",
            mime="application/pdf"
        )

    st.subheader("Ask a Question About the Articles:")
    q = st.text_input("Your Question:")

    if q:
        emb = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        vec = FAISS.load_local(
            "faiss_index",
            emb,
            allow_dangerous_deserialization=True
        )

        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=qa_llm,
            retriever=vec.as_retriever()
        )

        res = chain({"question": q}, return_only_outputs=True)

        st.header("Answer:")
        st.write(res["answer"])

        st.subheader("Sources:")
        st.markdown(f"<div class='small-source'>{res['sources']}</div>", unsafe_allow_html=True)


# ============================================================
# PAGE ROUTER
# ============================================================
if st.session_state.page == "landing":
    show_landing_page()
else:
    show_main_app()

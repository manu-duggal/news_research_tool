#  News Research Tool  
AI-powered summarization, insights, and research assistant for long-form news articles.

The **News Research Tool** helps you analyze multiple news articles instantly with:  
 Smart automated summaries  
 Key insights & takeaways  
 Retrieval-Augmented Question Answering (RAG)  
 PDF report generation  
 Clean, animated landing page UI  

Built using **Streamlit**, **Groq LLaMA models**, **FAISS**, and **Sentence Transformers**.

---

## 🌐 Live Demo  
 **Try the app here:**  
 https://md-newstool.streamlit.app/

---

##  Features

###  **1. URL-based Article Extraction**
- Enter up to 3 article URLs  
- Automatic content scraping via `UnstructuredURLLoader`  
- Works with most news websites

###  **2. AI Summaries**
Uses **Groq LLaMA 3.1 8B Instant** to generate:
- Overview  
- Key takeaways  
- Key insights  

Each article gets its own tabbed summary card.

###  **3. RAG Question Answering**
Ask any question about the processed articles.  
The system uses:
- SentenceTransformer `all-MiniLM-L6-v2` embeddings  
- FAISS vector search  
- Groq **LLaMA 3.3 70B Versatile** for answers  

This allows deep research on the article content.

###  **4. PDF Report Export**
Download a formatted PDF with:
- Timestamps  
- Article URLs  
- Generated summaries  

###  **5. Beautiful Landing Page**
- Glassmorphism  
- Gradient animations  
- Mobile-friendly layout  
- Minimal & modern UI  

---

##  Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| LLMs | Groq LLaMA 3.1 & 3.3 |
| Vector DB | FAISS |
| Embeddings | SentenceTransformer MiniLM-L6-v2 |
| PDF | ReportLab |
| Scraper | UnstructuredURLLoader |
| Styling | Custom CSS (Glass UI + Gradient) |

---


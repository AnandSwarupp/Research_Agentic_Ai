Agentic Research Assistant:
A Streamlit-based autonomous AI research agent that takes a research query, searches the web, extracts and
cleans relevant content, and generates a high-quality summary using a local LLM (DeepSeek). You can 
interact with the results and download the summary as a .txt file.

Features:
🌐 Performs automated web searches using SERPER based on user queries

🧹 Scrapes and cleans textual content from relevant URLs

🧠 Summarizes extracted data using DeepSeek (local LLM) or Hugging Face models

💬 Simple UI for interacting with the AI-generated summary

📄 Option to download summary as a .txt file

🔒 Local inference without sending your data to external APIs (DeepSeek)

Tech Stack:
1. Frontend: Streamlit

2. Backend: Python

3. NLP & AI: DeepSeek LLM via LlamaCpp, Hugging Face Transformers, LangChain

4. Vector Store (Optional): FAISS

5. Web Tools: Requests, BeautifulSoup

6. Utilities: dotenv, io, os, PyMuPDF, PyPDF2

Project Structure:
.
├── app.py                  # Main Streamlit interface
├── research.py             # Core functions: search, scrape, summarize
├── models/
│   └── DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf  # Local LLM file
├── .env                    # Stores API keys (e.g., Hugging Face)
└── requirements.txt

import requests
import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from transformers import pipeline
from langchain.llms import LlamaCpp

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)



def search_web(query, num_results=5):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": num_results
    }

    try:
        response = requests.post(SERPER_URL, headers=headers, json=payload)
        response.raise_for_status()
        results = response.json()

        links = []
        for item in results.get("organic", []):
            link = item.get("link")
            if link:
                links.append(link)

        return links
    
    except requests.exceptions.RequestException as e:
        return f"Error querying Serper.dev: {e}"
    
def get_clean_text(url):
    try:
        response = requests.get(url, timeout=10)
        soap = BeautifulSoup(response.text, "html.parser")
        text = ' '.join([p.text for p in soap.find_all("p")])
        return text[:3000]
    except Exception as e:
        return f"Error fetching {url}: {e}"


def summarize_text(text, max_length=130, min_length=30, chunk_token_limit=100):
    if len(text.split()) < 50:
        return "Text too short to summarize meaningfully."
    
    def chunk_text(text, max_tokens=chunk_token_limit):
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len((current_chunk + sentence).split()) <= max_tokens:
                current_chunk += sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    try:
        # Chunking if needed
        if len(text.split()) > chunk_token_limit:
            chunks = chunk_text(text, max_tokens=chunk_token_limit)
            summaries = []
            for chunk in chunks:
                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                
                # Defensive type check
                if isinstance(summary, list) and 'summary_text' in summary[0]:
                    summaries.append(summary[0]['summary_text'])
                else:
                    return f"Unexpected summarizer output: {summary}"
            
            # Combine all summaries
            combined_summary = ' '.join(summaries)
            return combined_summary
        else:
            summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            
            # Defensive type check
            if isinstance(summary, list) and 'summary_text' in summary[0]:
                return summary[0]['summary_text']
            else:
                return f"Unexpected summarizer output: {summary}"
    
    except Exception as e:
        return f"Summarization error: {e}"
    
def agentic_research(query, urls):

    llm = LlamaCpp(
        model_path="./models/DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf",
        temperature=0.7,
        max_tokens=1024,
        top_p=0.9,
        n_ctx=2048,
        verbose=False
    )

    combined_knowledge = ""
    summaries = []

    for url in urls:
        try:
            raw_text = get_clean_text(url)
            summary = summarize_text(raw_text)
            summaries.append(f"From {url}:\n{summary}\n")
            combined_knowledge += f"{summary}\n"
        except Exception as e:
            print(f"Error processing {url} : {e}")
            continue

    prompt = f"""
        [INST] You are a research assistant. Given the query "{query}" and the following summaries:{combined_knowledge}
        Write a detailed, helpful research summary.[/INST]
    """
    
    result = llm(prompt)
    return result.strip(), summaries

"""
Data ingestion script to scrape and index Nippon India MF fund pages
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pickle
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Fund URLs to scrape
FUND_URLS = {
    "large_cap": "https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Large-Cap-Fund.aspx",
    "growth_mid_cap": "https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Growth-Mid-Cap-Fund.aspx",
    "small_cap": "https://mf.nipponindiaim.com/FundsAndPerformance/Pages/NipponIndia-Small-Cap-Fund.aspx"
}

ALLOWED_DOMAINS = os.getenv("SOURCE_ALLOWED_DOMAINS", "mf.nipponindiaim.com").split(",")

def extract_fund_facts(html_content: str, url: str) -> str:
    """
    Extract relevant fund facts from HTML content
    Focuses on: expense ratio, exit load, minimum investment, lock-in, riskometer, benchmark
    """
    soup = BeautifulSoup(html_content, "lxml")
    
    # Remove navigation, scripts, styles
    for element in soup(["script", "style", "nav", "header", "footer"]):
        element.decompose()
    
    facts = []
    
    # Extract key sections
    # Look for fund details section
    fund_details = soup.find_all(["div", "section", "table"], class_=lambda x: x and (
        "fund" in x.lower() or "detail" in x.lower() or "performance" in x.lower()
    ))
    
    # Extract text from tables (NAV, performance, etc.)
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                text = " ".join(cell.get_text(strip=True) for cell in cells)
                if any(keyword in text.lower() for keyword in [
                    "expense", "load", "minimum", "lock", "risk", "benchmark", "nav", "sip"
                ]):
                    facts.append(text)
    
    # Extract from paragraphs
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        text = p.get_text(strip=True)
        if any(keyword in text.lower() for keyword in [
            "expense ratio", "exit load", "entry load", "minimum investment",
            "minimum sip", "lock-in", "riskometer", "benchmark", "fund manager",
            "inception", "investment objective"
        ]):
            facts.append(text)
    
    # Extract from lists
    lists = soup.find_all(["ul", "ol"])
    for ul in lists:
        items = ul.find_all("li")
        for item in items:
            text = item.get_text(strip=True)
            if any(keyword in text.lower() for keyword in [
                "expense", "load", "minimum", "lock", "risk", "benchmark"
            ]):
                facts.append(text)
    
    # Combine all facts
    combined_text = "\n".join(facts)
    
    # If we didn't get much, get main content
    if len(combined_text) < 500:
        main_content = soup.find("main") or soup.find("article") or soup.find("div", class_=lambda x: x and "content" in x.lower())
        if main_content:
            combined_text = main_content.get_text(separator="\n", strip=True)
    
    return combined_text

def scrape_fund_page(url: str) -> tuple:
    """
    Scrape a fund page and return (content, success)
    """
    try:
        # Verify domain
        from urllib.parse import urlparse
        parsed = urlparse(url)
        if not any(domain in parsed.netloc for domain in ALLOWED_DOMAINS):
            print(f"Warning: URL {url} not in allowed domains")
            return None, False
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        content = extract_fund_facts(response.text, url)
        return content, True
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, False

def run_ingestion():
    """Main ingestion function"""
    print("Starting data ingestion...")
    
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    print(f"Using Hugging Face embeddings model: {model_name}")
    
    # Scrape all fund pages
    all_documents = []
    
    for fund_name, url in FUND_URLS.items():
        print(f"Scraping {fund_name}...")
        content, success = scrape_fund_page(url)
        
        if success and content:
            # Create document with metadata
            doc = Document(
                page_content=content,
                metadata={
                    "source": url,
                    "fund_name": fund_name,
                    "scraped_date": datetime.now().isoformat(),
                    "fund_type": fund_name
                }
            )
            all_documents.append(doc)
            print(f"  ✓ Scraped {len(content)} characters")
        else:
            print(f"  ✗ Failed to scrape {fund_name}")
    
    if not all_documents:
        print("No documents scraped. Exiting.")
        return
    
    # Split documents into chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = []
    for doc in all_documents:
        doc_chunks = text_splitter.split_documents([doc])
        chunks.extend(doc_chunks)
    
    print(f"Created {len(chunks)} chunks")
    
    # Create vector store
    print("Creating vector store...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save vector store
    vector_store_path = os.getenv("VECTOR_STORE_PATH", "./data/faiss_index")
    os.makedirs(vector_store_path, exist_ok=True)
    
    vector_store.save_local(vector_store_path)
    
    # Save metadata
    metadata = {
        "fund_urls": FUND_URLS,
        "ingestion_date": datetime.now().isoformat(),
        "num_documents": len(all_documents),
        "num_chunks": len(chunks)
    }
    
    metadata_path = os.path.join(vector_store_path, "metadata.pkl")
    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)
    
    print(f"✓ Vector store saved to {vector_store_path}")
    print(f"✓ Metadata saved to {metadata_path}")
    print("Ingestion complete!")

if __name__ == "__main__":
    run_ingestion()




"""
RAG Service for querying mutual fund facts
Uses FAISS vector store and Google Gemini for answer generation
"""

import os
import pickle
from typing import Dict, List
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import faiss
import google.generativeai as genai

class RAGService:
    """RAG service for retrieving and answering MF factual queries"""
    
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.metadata_store = {}
        self.llm = None
        self.is_ready_flag = False
        self._initialize()
    
    def _initialize(self):
        """Initialize embeddings, LLM, and load vector store"""
        try:
            model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            print(f"Hugging Face embeddings initialised with '{model_name}'")
            
            # Initialize Google Gemini LLM (free tier)
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                print("Warning: GEMINI_API_KEY not set. Will use fallback answer generation.")
            else:
                genai.configure(api_key=gemini_api_key)
                # Use gemini-1.5-flash for free tier (faster and free)
                # Alternative: gemini-pro for better quality (also free tier)
                self.llm = genai.GenerativeModel('gemini-1.5-flash')
                print("Gemini LLM initialized successfully")
            
            # Load vector store if it exists
            vector_store_path = os.getenv("VECTOR_STORE_PATH", "./data/faiss_index")
            metadata_path = os.path.join(vector_store_path, "metadata.pkl")
            
            if os.path.exists(vector_store_path) and os.path.exists(metadata_path):
                self.vector_store = FAISS.load_local(
                    vector_store_path,
                    self.embeddings,
                )
                with open(metadata_path, "rb") as f:
                    self.metadata_store = pickle.load(f)
                self.is_ready_flag = True
                print(f"Vector store loaded from {vector_store_path}")
            else:
                print(f"Vector store not found at {vector_store_path}. Run ingestion first.")
        
        except Exception as e:
            print(f"Error initializing RAG service: {e}")
    
    def is_ready(self) -> bool:
        """Check if RAG service is ready"""
        return self.is_ready_flag and self.vector_store is not None
    
    def query(self, question: str, k: int = 3) -> Dict:
        """
        Query the RAG system and return answer with source
        Returns dict with answer, source, and confidence
        """
        if not self.is_ready():
            return {
                "answer": "Vector store not loaded. Please run data ingestion first.",
                "source": "",
                "confidence": 0.0
            }
        
        try:
            # Retrieve relevant documents
            docs = self.vector_store.similarity_search_with_score(question, k=k)
            
            if not docs:
                return {
                    "answer": "I couldn't find relevant information for your query. Please try rephrasing or ask about expense ratio, exit load, minimum SIP, lock-in period, riskometer, or benchmark.",
                    "source": "",
                    "confidence": 0.0
                }
            
            # Get the most relevant document for source URL
            top_doc, score = docs[0]
            
            # Extract source URL from metadata
            source_url = ""
            if hasattr(top_doc, "metadata") and "source" in top_doc.metadata:
                source_url = top_doc.metadata["source"]
            
            # Generate concise answer using Gemini LLM
            answer = self._generate_answer(question, docs)
            
            return {
                "answer": answer,
                "source": source_url,
                "confidence": float(1.0 - min(score, 1.0))  # Convert distance to confidence
            }
        
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "source": "",
                "confidence": 0.0
            }
    
    def _generate_answer(self, question: str, all_docs: List) -> str:
        """
        Generate concise answer using Google Gemini LLM
        Falls back to rule-based extraction if Gemini is not available
        """
        # Prepare context from retrieved documents
        context_parts = []
        for doc, score in all_docs[:3]:  # Use top 3 documents
            context_parts.append(doc.page_content.strip())
        
        context = "\n\n".join(context_parts)
        
        # Use Gemini LLM if available
        if self.llm:
            try:
                prompt = f"""You are a facts-only assistant for mutual fund information. Answer the user's question based ONLY on the provided context from official Nippon India Mutual Fund sources.

Rules:
- Answer in maximum 3 sentences
- Be concise and factual
- Only use information from the context provided
- If the answer is not in the context, say so
- Always end your answer with: "Facts-only. No investment advice."
- Do not provide investment recommendations or opinions

Context from official sources:
{context}

Question: {question}

Answer:"""

                response = self.llm.generate_content(prompt)
                
                # Extract text from Gemini response
                answer = response.text.strip()
                
                # Ensure the disclaimer is present
                if "Facts-only. No investment advice." not in answer:
                    answer += " Facts-only. No investment advice."
                
                return answer
            
            except Exception as e:
                print(f"Error calling Gemini API: {e}")
                # Fall through to rule-based extraction
        
        # Fallback: Rule-based extraction (original method)
        return self._generate_answer_fallback(question, context)
    
    def _generate_answer_fallback(self, question: str, content: str) -> str:
        """
        Fallback answer generation using rule-based extraction
        Used when Gemini is not available
        """
        import re
        question_lower = question.lower()
        
        # Try to extract specific facts
        if "expense ratio" in question_lower:
            ratio_match = re.search(r"expense.*?ratio.*?(\d+\.?\d*)\s*%", content, re.IGNORECASE)
            if ratio_match:
                return f"The expense ratio is {ratio_match.group(1)}%. This information is sourced from the official Nippon India Mutual Fund website. Facts-only. No investment advice."
        
        if "exit load" in question_lower:
            if "exit load" in content.lower() or "redemption" in content.lower():
                load_match = re.search(r"exit load.*?(\d+\.?\d*)\s*%", content, re.IGNORECASE)
                if load_match:
                    return f"The exit load is {load_match.group(1)}% if redeemed within the specified period. Details are available on the official fund page. Facts-only. No investment advice."
                return "Exit load details are available on the official fund page. Please refer to the load structure section. Facts-only. No investment advice."
        
        if "minimum" in question_lower and ("sip" in question_lower or "investment" in question_lower):
            min_match = re.search(r"minimum.*?(\d+[,\d]*\.?\d*)", content, re.IGNORECASE)
            if min_match:
                amount = min_match.group(1).replace(",", "")
                return f"The minimum investment amount is ₹{amount} and in multiples of Re. 1 thereafter. This information is from the official fund documentation. Facts-only. No investment advice."
        
        if "lock" in question_lower and "in" in question_lower:
            lock_match = re.search(r"lock.?in.*?(\d+)\s*(year|month)", content, re.IGNORECASE)
            if lock_match:
                return f"The lock-in period is {lock_match.group(1)} {lock_match.group(2)}s for ELSS schemes. This is a regulatory requirement. Facts-only. No investment advice."
        
        if "riskometer" in question_lower or "risk" in question_lower:
            return "The riskometer indicates the risk level of the fund. Please refer to the official fund page for the current riskometer rating. Facts-only. No investment advice."
        
        if "benchmark" in question_lower:
            bench_match = re.search(r"benchmark.*?([A-Z][A-Z\s]+(?:TRI|Index))", content, re.IGNORECASE)
            if bench_match:
                return f"The benchmark is {bench_match.group(1)}. This information is available on the official fund factsheet. Facts-only. No investment advice."
        
        if "download" in question_lower or "statement" in question_lower:
            return "You can download statements and factsheets from the 'Downloads' section on the official Nippon India Mutual Fund website. Log in to your account or visit the fund page for access. Facts-only. No investment advice."
        
        # Generic answer from content
        sentences = content.split(".")[:3]
        answer = ". ".join(s.strip() for s in sentences if s.strip())
        if answer:
            answer += ". Facts-only. No investment advice."
        else:
            answer = "I found relevant information, but please refer to the official fund page for complete details. Facts-only. No investment advice."
        
        return answer



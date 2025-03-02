# rag/data_loader.py - Data loading and processing
from datasets import load_dataset
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from huggingface_hub import login
import os

from rag.retriever import RetrieverTool

def authenticate_huggingface():
    """Authenticate with Hugging Face if token is available"""
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        login(token=hf_token)
        return True
    else:
        print("Warning: HF_TOKEN not found in environment variables")
        return False

def load_and_process_data(dataset_name, split="train", chunk_size=500, chunk_overlap=50):
    """Load and process data, returning a retriever tool"""
    # Authenticate with Hugging Face
    authenticate_huggingface()
    
    # Load dataset
    knowledge_base = load_dataset(dataset_name, split=split)
    
    # Create documents
    source_docs = [
        Document(page_content=doc["full_text"], metadata={"source": doc["source"]})
        for doc in knowledge_base
    ]
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    docs_processed = text_splitter.split_documents(source_docs)
    
    # Create and return retriever tool
    return RetrieverTool(docs_processed)
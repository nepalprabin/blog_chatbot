# app.py - Main FastAPI application
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from rag.data_loader import load_and_process_data
from rag.agent import create_agent
from rag.config import AppConfig

# Load environment variables
load_dotenv()

# Initialize configuration
config = AppConfig()

# Initialize FastAPI app
app = FastAPI(title="Blog RAG Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class ChatRequest(BaseModel):
    query: str

# Define response model
class ChatResponse(BaseModel):
    response: str

# Load and process data
print("Loading and processing documents...")
retriever_tool = load_and_process_data(
    dataset_name=config.dataset_name,
    split=config.dataset_split,
    chunk_size=config.chunk_size,
    chunk_overlap=config.chunk_overlap
)

# Endpoint to check if API is running
@app.get("/")
async def root():
    return {"status": "The Blog RAG Chatbot API is running!"}

# Endpoint to process chat requests
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Create a new agent for each request
        agent = create_agent(
            retriever_tool=retriever_tool,
            model_id=config.model_id,
            api_base=config.api_base,
            api_key=config.api_key,
            max_steps=config.max_steps,
            verbosity_level=config.verbosity_level
        )
        
        # Run the agent with the user's query
        response = agent.run(request.query)
        
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Run with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=config.host, port=config.port, reload=True)
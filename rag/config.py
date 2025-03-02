# rag/config.py - Configuration settings
import os
from typing import List

class AppConfig:
    def __init__(self):
        # API settings
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        self.cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
        
        # Dataset settings
        self.dataset_name = os.getenv("DATASET_NAME", "nepalprabin/blog_dataset")
        self.dataset_split = os.getenv("DATASET_SPLIT", "train")
        
        # Document processing settings
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "500"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
        
        # Model settings
        self.model_id = os.getenv("MODEL_ID", "gpt-4o")
        self.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Agent settings
        self.max_steps = int(os.getenv("MAX_STEPS", "4"))
        self.verbosity_level = int(os.getenv("VERBOSITY_LEVEL", "0"))
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
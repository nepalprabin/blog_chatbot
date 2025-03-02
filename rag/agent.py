# rag/agent.py - Agent creation and management
from smolagents import CodeAgent, OpenAIServerModel

def get_openai_model(model_id, api_base, api_key):
    """Create and return an OpenAI model"""
    if not api_key:
        raise ValueError("OpenAI API key is required")
    
    return OpenAIServerModel(
        model_id=model_id,
        api_base=api_base,
        api_key=api_key,
    )

def create_agent(retriever_tool, model_id, api_base, api_key, max_steps=4, verbosity_level=0):
    """Create and return a CodeAgent with the specified configuration"""
    model = get_openai_model(model_id, api_base, api_key)
    
    return CodeAgent(
        tools=[retriever_tool], 
        model=model, 
        max_steps=max_steps, 
        verbosity_level=verbosity_level
    )
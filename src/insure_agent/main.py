from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
import os

# Ensure environment variables are loaded (e.g., for API keys used by crews)
from dotenv import load_dotenv
load_dotenv()

# Import your crew classes
from insure_agent.crews.onboarding_crew.onboarding_crew import OnboardingCrew
from insure_agent.crews.rag_crew.rag_crew import RagCrew
import uvicorn


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


app = FastAPI(
    title="Insurance AI Agent API",
    description="API for interacting with the Insurance AI Agent crews.",
    version="1.0.0"
)

# --- Pydantic Request Models ---
class OnboardingRequest(BaseModel):
    client_name: str = Field(..., example="Emmanuel Eze", description="Client's full name.")
    initial_request_type: str = Field(..., example="New Car Insurance Quote", description="The general type of request.")
    client_query: str = Field(..., example="I need a new car insurance policy for my 2024 Toyota Camry. I'm looking for full coverage and I have a clean driving record.", description="Detailed client query or requirements.")

class RagQueryRequest(BaseModel):
    client_query: str = Field(..., example="What are the benefits of comprehensive coverage?", description="Client's question about their policy.")

# --- Pydantic Response Model ---
class CrewResponse(BaseModel):
    status: str = Field(default="success", description="Status of the operation ('success' or 'error').")
    data: Any = Field(..., description="The result from the executed crew.")
    message: Optional[str] = Field(default=None, description="Optional message, e.g., for errors or additional info.")

# --- API Endpoints ---
@app.post("/onboarding/quote", response_model=CrewResponse, tags=["Onboarding Crew"])
async def handle_onboarding_request(request: OnboardingRequest):
    """
    Initiates the Onboarding Crew to process a new insurance quote request.
    """
    inputs = {
        'client_name': request.client_name,
        'initial_request_type': request.initial_request_type,
        'client_query': request.client_query
    }
    try:
        onboarding_crew_instance = OnboardingCrew()
        result = onboarding_crew_instance.crew().kickoff(inputs=inputs)
        return CrewResponse(data=str(result))
    except Exception as e:
        # Log the exception for debugging
        print(f"Error during Onboarding Crew execution: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the onboarding request: {str(e)}")

@app.post("/rag/query", response_model=CrewResponse, tags=["RAG Crew"])
async def handle_rag_request(request: RagQueryRequest):
    """
    Initiates the RAG Crew to answer a client's policy question.
    """
    inputs = {
        'client_query': request.client_query,
        # The RAG crew's 'analyze_policy_coverage' task expects '{{collect_user_query}}'.
        'collect_user_query': request.client_query
    }
    try:
        rag_crew_instance = RagCrew()
        result = rag_crew_instance.crew().kickoff(inputs=inputs)
        return CrewResponse(data=str(result))
    except Exception as e:
        # Log the exception for debugging
        print(f"Error during RAG Crew execution: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the RAG queries: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # Run the app on port 800
    
    
# To run this FastAPI application:
# Ensure you are in the `insure_agent/src` directory or adjust Python path
# uvicorn insure_agent.main:app --reload
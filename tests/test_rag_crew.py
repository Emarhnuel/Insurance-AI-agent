import pytest
from crewai import Agent, Task, Crew
# Ensure your project's src directory is in PYTHONPATH or pytest is run from project root
# If you move this file to tests/crews/rag_crew/, update the import accordingly:
# from src.insure_agent.crews.rag_crew.rag_crew import RagCrew 
from src.insure_agent.crews.rag_crew.rag_crew import RagCrew # Assuming tests is at the same level as src or PYTHONPATH is set
import os

# Note: rag_crew.py already calls load_dotenv(). 
# Ensure your .env file is at the project root: c:\Users\user\Desktop\AI\Insurance AI agent\insure_agent\.env

@pytest.fixture(scope="module")
def rag_crew_instance():
    """
    Provides a RagCrew instance.
    This fixture assumes:
    1. OPENROUTER_API_KEY and MEM0_API_KEY are set in the environment (e.g., via .env).
    2. Config files (agents.yaml, tasks.yaml) are in src/insure_agent/crews/rag_crew/config/.
    3. Knowledge source files (PDFs, directory for search) are accessible.
    """
    try:
        # OPENROUTER_API_KEY is needed at import time of RagCrew due to class-level LLM instantiation
        if not os.getenv("OPENROUTER_API_KEY"):
            pytest.skip("OPENROUTER_API_KEY not found in environment. Skipping integration tests.")
        if not os.getenv("MEM0_API_KEY"):
            pytest.skip("MEM0_API_KEY not found in environment. Skipping integration tests.")
            
        instance = RagCrew()
        return instance
    except Exception as e:
        pytest.fail(f"Failed to instantiate RagCrew: {e}. Check API keys, config files, and knowledge sources.")

def test_rag_crew_object_creation(rag_crew_instance):
    """Test that the main RagCrew().crew() object can be created."""
    assert rag_crew_instance is not None, "RagCrew instance fixture should not be None."
    crew_obj = rag_crew_instance.crew()
    assert isinstance(crew_obj, Crew), "crew() method should return a Crew object."
    assert crew_obj.verbose == True, "Crew verbose should be True as per rag_crew.py."
    assert crew_obj.memory is True, "Crew memory should be enabled."
    assert crew_obj.memory_config['provider'] == "mem0", "Memory provider should be mem0."
    assert len(crew_obj.knowledge_sources) > 0, "Knowledge sources should be configured."

def test_car_insurance_specialist_agent_creation(rag_crew_instance):
    """Test that the car_insurance_specialist agent can be created."""
    agent = rag_crew_instance.car_insurance_specialist()
    assert isinstance(agent, Agent), "car_insurance_specialist() should return an Agent object."
    assert agent.verbose is True, "Agent verbose should be True."

def test_analyze_policy_coverage_task_creation(rag_crew_instance):
    """Test that the AnalyzePolicyCoverage task can be created."""
    task = rag_crew_instance.analyze_policy_coverage()
    assert isinstance(task, Task), "analyze_policy_coverage() should return a Task object."

def test_explain_claims_process_task_creation(rag_crew_instance):
    """Test that the ExplainClaimsProcess task can be created."""
    task = rag_crew_instance.explain_claims_process()
    assert isinstance(task, Task), "explain_claims_process() should return a Task object."

def test_compare_coverage_options_task_creation(rag_crew_instance):
    """Test that the CompareCoverageOptions task can be created."""
    task = rag_crew_instance.compare_coverage_options()
    assert isinstance(task, Task), "compare_coverage_options() should return a Task object."

@pytest.mark.integration  # Mark as integration test as it makes external calls
def test_rag_crew_kickoff_simple_query(rag_crew_instance):
    """
    Test a simple kickoff of the RAG crew with a basic query.
    This is an INTEGRATION TEST: it depends on live API keys, model access,
    correctly configured and accessible config files, and knowledge sources.
    It will be slower and may consume API credits.
    """
    crew_obj = rag_crew_instance.crew()
    
    inputs = {
        "client_query": "What is the process for filing a claim for a minor accident?",
    }
    
    try:
        result = crew_obj.kickoff(inputs=inputs)
        assert result is not None, "Crew kickoff should produce a result."
        assert isinstance(result, str), "Crew kickoff result should be a string."
        print(f"\n--- RAG Crew Kickoff Result ---")
        print(result)
        print(f"--- End RAG Crew Kickoff Result ---")
    except Exception as e:
        pytest.fail(f"RagCrew kickoff failed: {e}")

# To run: pytest

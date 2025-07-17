from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectorySearchTool
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai import LLM 
import os  
from dotenv import load_dotenv


load_dotenv()

# Set your Mem0 API key
os.environ["MEM0_API_KEY"] = os.getenv("MEM0_API_KEY")


# Calculate the absolute path to the Knowledge directory.
# This navigates up from this script's location to the project root 
# and then into the "Knowledge" folder.
knowledge_base_path = "knowledge"


tool = DirectorySearchTool(
    directory=knowledge_base_path,
    config=dict(
        llm=dict(
            provider="openai", 
            config=dict(
                model="gpt-4o-mini",
                temperature=0.0,  # Zero temperature for search
                api_key=os.getenv("OPENAI_API_KEY")
            ),
        ),
        embedder=dict(
            provider="openai",  
            config=dict(
                model="text-embedding-ada-002",  # More efficient embedding
                api_key=os.getenv("OPENAI_API_KEY")
            ),
        ),
        
        # Chunker configuration
        chunker=dict(
            chunk_size=1000,
            chunk_overlap=200,
            length_function="len",
        )
    )
)


pdf_source = PDFKnowledgeSource(
    file_paths=["Car_Insurance_Policy_Documents.pdf", "Insurance_Plan_Database.pdf",
        "Premium_Calculation_Rules.pdf", "Discount_Program_Information.pdf",
        "Regulatory_Compliance_Information.pdf", "Claims_Process_Documentation.pdf", 
        "Customer_FAQ_Documents.pdf"]
)

 
@CrewBase
class RagCrew:
    """Policy Information RAG Crew
    
    This crew is designed to analyze car insurance policy documents and provide accurate,
    detailed responses to client queries using Retrieval Augmented Generation (RAG).
    It can analyze policy coverage, explain claims processes, and compare coverage options.
    """
    
    # Configuration file paths
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    

    # Define the LLM to be used by all agents
    llm_1 = LLM(
    model="openrouter/google/gemini-2.5-flash-preview-05-20",
    base_url="https://openrouter.ai/api/v1",
    max_tokens=2000,
    temperature=0.1,
    stream=True,
    seed=42,
    api_key=os.getenv("OPENROUTER_API_KEY")
)

    
    @agent
    def car_insurance_specialist(self) -> Agent:
        """Creates the car insurance policy specialist agent"""       
        return Agent(
            config=self.agents_config["CarInsuranceSpecialist"],
            tools=[tool],
            llm=self.llm_1, 
            verbose=True,
            max_rpm=26,
            max_iter=3,
            
        )
    
    @task
    def analyze_policy_coverage(self) -> Task:
        """Task for analyzing specific aspects of policy coverage"""
        return Task(
            config=self.tasks_config["analyze_policy_coverage"],
        )
    
    @task
    def compare_coverage_options(self) -> Task:
        """Task for comparing different coverage options"""
        return Task(
            config=self.tasks_config["compare_coverage_options"],
        )

    @task
    def explain_claims_process(self) -> Task:
        """Task for explaining the claims process to clients"""
        return Task(
            config=self.tasks_config["explain_claims_process"],
        )
    
    @crew
    def crew(self) -> Crew:
        """Assembles the Policy Information RAG Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[pdf_source],
            cache=True,
            memory=True,
            memory_config={
                "provider": "mem0",
                "config": {
                    "user_id": "Emmanuel_RAG",
                    "org_id": "org_qGKjjvHSnVe2ZKBbbtwN7vlYwlGwr7g1sbiiXfN4",        # Optional
                    "project_id": "proj_M1TSScoCtHZlxlUjqG9VwkYEpWMPoiXrfjJX8OsG", # Optional
                },
                "user_memory": {}
            },
         ) 

    
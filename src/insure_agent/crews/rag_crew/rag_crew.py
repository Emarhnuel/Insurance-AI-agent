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

# Tool for semantic search within the 'knowledge' directory.
policy_search_tool = DirectorySearchTool(directory='c:\\Users\\user\\Desktop\\AI\\Insurance AI agent\\insure_agent\\knowledge')

# Defines a source for specific PDF files.
pdf_source = PDFKnowledgeSource(
    file_paths=["Car Insurance Policy Documents.pdf", "Insurance plan database.pdf",
     "Premium Calculation Rules.pdf", "Discount Program Information.pdf", 
     "Regulatory Compliance Information.pdf", "Claims Process Documentation.pdf", "Customer FAQ Documents.pdf"
     ]
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
    model="openrouter/deepseek/deepseek-r1-0528",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

    llm_2 = LLM(
    model="openrouter/deepseek/deepseek-r1-0528",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

    
    @agent
    def car_insurance_specialist(self) -> Agent:
        """Creates the car insurance policy specialist agent"""       
        return Agent(
            config=self.agents_config["CarInsuranceSpecialist"],
            tools=[policy_search_tool],
            llm=self.llm_1,
            verbose=True
        )
    
    @task
    def analyze_policy_coverage(self) -> Task:
        """Task for analyzing specific aspects of policy coverage"""
        return Task(
            config=self.tasks_config["AnalyzePolicyCoverage"],
        )
    
    @task
    def explain_claims_process(self) -> Task:
        """Task for explaining the claims process to clients"""
        return Task(
            config=self.tasks_config["ExplainClaimsProcess"],
        )
    
    @task
    def compare_coverage_options(self) -> Task:
        """Task for comparing different coverage options"""
        return Task(
            config=self.tasks_config["CompareCoverageOptions"],
        )
    
    @task
    def collect_user_query(self) -> Task:
        """Task for collecting user query"""
        return Task(
            config=self.tasks_config["CollectUserQuery"],
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

    
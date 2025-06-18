from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM 
from crewai_tools import DirectorySearchTool
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from insure_agent.tools.premium_calculator_tool import PremiumCalculatorTool
from insure_agent.tools.insurance_plan_database_tool import InsurancePlanDatabaseTool # Added import
import os  
from dotenv import load_dotenv 


load_dotenv()


# Set your Mem0 API key
os.environ["MEM0_API_KEY"] = os.getenv("MEM0_API_KEY")

# Instantiate the PremiumCalculatorTool
premium_calculator_tool = PremiumCalculatorTool()

# Instantiate the InsurancePlanDatabaseTool
insurance_plan_database_tool = InsurancePlanDatabaseTool()


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
            ),
        ),
        embedder=dict(
            provider="openai",  
            config=dict(
                model="text-embedding-ada-002",  # More efficient embedding
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
class OnboardingCrew:
    """Car Insurance Onboarding Crew
    
    This crew guides clients through the process of selecting the most appropriate
    car insurance plan through a structured, personalized assessment and recommendation process.
    """

    # Configuration file paths
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # Define shared LLM for all agents
    llm_1 = LLM(
    model="openrouter/google/gemini-2.5-flash-preview-05-20",
    base_url="https://openrouter.ai/api/v1",
    max_tokens=4000,
    temperature=0.2,
    stream=True,
    seed=42,
    api_key=os.getenv("OPENROUTER_API_KEY")
)

    llm_2 = LLM(
    model="openrouter/deepseek/deepseek-r1-0528",
    base_url="https://openrouter.ai/api/v1",
    max_tokens=4000,
    temperature=0.2,
    stream=True,
    seed=42,
    api_key=os.getenv("OPENROUTER_API_KEY")
)

    @agent
    def needs_assessment_agent(self) -> Agent:
        """Creates the client information gathering specialist"""
        return Agent(
            config=self.agents_config["NeedsAssessmentAgent"],
            llm=self.llm_2,
            max_rpm=40,
            max_iter=3,
            verbose=True
        )

    @agent
    def coverage_analyst_agent(self) -> Agent:
        """Creates the insurance needs analyst with specialized tools"""
        # Initialize specialized tools for coverage analysis
        
        return Agent(
            config=self.agents_config["CoverageAnalystAgent"],
            tools=[tool, premium_calculator_tool, insurance_plan_database_tool],
            llm=self.llm_1,
            max_rpm=40,
            max_iter=3,
            verbose=True
        )

    @agent
    def recommendation_agent(self) -> Agent:
        """Creates the recommendation specialist"""
        return Agent(
            config=self.agents_config["RecommendationAgent"],
            llm=self.llm_2,
            max_rpm=40,
            max_iter=3,
            verbose=True
        )

    @task
    def gather_client_information(self) -> Task:
        """Conducts a comprehensive client profiling interview"""
        return Task(
            config=self.tasks_config["GatherClientInformation"],
        )

    @task
    def analyze_insurance_needs(self) -> Task:
        """Performs actuarial risk assessment and coverage needs analysis"""
        return Task(
            config=self.tasks_config["AnalyzeInsuranceNeeds"],
        )

    @task
    def identify_suitable_plans(self) -> Task:
        """Researches and matches optimal insurance plans"""
        return Task(
            config=self.tasks_config["IdentifySuitablePlans"],
        )

    @task 
    def generate_recommendation(self) -> Task:
        """Creates personalized coverage recommendation and education package"""
        return Task(
            config=self.tasks_config["GenerateRecommendation"],
        )

    @crew
    def crew(self) -> Crew:
        """Assembles the Car Insurance Onboarding Crew"""
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
                     "user_id": "Emmanuel_Onboarding",
                     "org_id": "org_qGKjjvHSnVe2ZKBbbtwN7vlYwlGwr7g1sbiiXfN4",        # Optional
                     "project_id": "proj_M1TSScoCtHZlxlUjqG9VwkYEpWMPoiXrfjJX8OsG", # Optional
                 },
                 "user_memory": {}
             },
        )

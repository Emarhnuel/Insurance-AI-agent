from crewai import Agent, Crew, Process, Task
from crewai import LLM 
from crewai_tools import DirectorySearchTool
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai_tools import MCPServerAdapter
from pydantic import BaseModel
from typing import Optional

import os  
from dotenv import load_dotenv 


load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")

# Set your Mem0 API key
os.environ["MEM0_API_KEY"] = os.getenv("MEM0_API_KEY")

server_params = {   
    "url": "https://mcp.vapi.ai/mcp", 
    "transport": "streamable-http",
    "headers": {
        "Authorization": f"Bearer {VAPI_API_KEY}"
    }
}


# Define your Pydantic model
class CallSummary(BaseModel):
    client_query: str
    information_provided: str
    outcome: str
    human_handoff_reason: Optional[str] = None



# Define shared LLM for all agents
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


# Tool for semantic search within the 'knowledge' directory.
policy_search_tool = DirectorySearchTool(directory='c:\\Users\\user\\Desktop\\AI\\Insurance AI agent\\insure_agent\\knowledge')


# Defines a source for specific PDF files.
pdf_source = PDFKnowledgeSource(
    file_paths=["Car Insurance Policy Documents.pdf", "Insurance plan database.pdf",
     "Premium Calculation Rules.pdf", "Discount Program Information.pdf", 
     "Regulatory Compliance Information.pdf", "Claims Process Documentation.pdf", "Customer FAQ Documents.pdf"
     ]  
)


# Initialize mcp_tools as an empty list. It will be populated if MCP server connection is successful.
mcp_tools = [] 
try:
    with MCPServerAdapter(server_params) as tools_from_mcp:
        mcp_tools.extend(tools_from_mcp) # Add tools from MCP to our list
        print(f"Available tools from Streamable HTTP MCP server: {[tool.name for tool in mcp_tools]}")
except Exception as e:
    print(f"Warning: Failed to connect to Streamable HTTP MCP server or retrieve tools: {e}")
    print("AI Voice Crew will proceed without MCP-specific tools.")

# Define Agent, Task, and Crew at the module level
VoiceSupportAgent = Agent(
    role="Proactive AI Voice Outreach Specialist for Car Insurance",
    goal="To efficiently and empathetically handle outbound client calls, provide accurate"
         "easy-to-understand car insurance information using the company's knowledge base"
         "and judiciously determine when to escalate to a human agent, always ensuring a"
         "positive client interaction and adherence to company policy",
    backstory="You are a highly trained AI Voice Outreach Specialist, having processed thousands of"
         "simulated client interactions and mastered the art of clear, empathetic, and"
         "professional voice communication. Your core strength lies in proactively engaging"
         "clients, swiftly understanding their car insurance needs, and leveraging the"
         "company's comprehensive knowledge base (policy documents, FAQs, etc.) to provide"
         "accurate and contextually relevant answers. You are adept at navigating complex"
         "information and explaining it simply. You understand the importance of human"
         "connection for sensitive or complex issues and are programmed to identify"
         "situations requiring a human agent, ensuring a seamless and supportive handoff."
         "You operate strictly within the company's guidelines, prioritizing client"
         "satisfaction and data security, and do not route inquiries to other AI systems.",
    tools=[policy_search_tool] + mcp_tools, # Combine general tools with MCP tools
    llm=llm_1,
    reasoning=True,
    max_reasoning_attempts=3,
    max_iter=6,
    max_rpm=15,
    verbose=True,
)

HandleOutboundClientCall = Task(
    description=(
        "This task is critical for proactive client support. As the VoiceSupportAgent, your primary goal is to simulate an "
        "outbound call to a client regarding their car insurance. You will be provided with the client's phone number "
        "as '{phone_number}' and the initial reason for the call as '{call_reason}'.\n\n"
        "Your process for this task is as follows:\n"
        "1. Initiate the Call: Greet the client warmly. Confirm you've reached the right person for {phone_number}. "
        "Clearly state your name (as the AI Voice Specialist from the Car Insurance Team) and the purpose of your call, referencing the provided '{call_reason}'.\n"
        "2. Understand the Need: Engage in a natural, empathetic conversation to fully understand the client's specific car insurance query, "
        "concerns, or information needs related to the call reason or any other topic they bring up. Listen actively.\n"
        "3. Access & Deliver Information: Utilize your available tools (including the company's knowledge base and any connected MCP tools) to meticulously find and deliver accurate, "
        "relevant, and easy-to-understand information regarding policy details, claims processes, coverage questions, discount eligibility, etc.\n"
        "4. Resolve or Identify Limits:\n"
        "   a. If the query can be fully addressed with the knowledge base, provide a comprehensive answer and ensure the client understands.\n"
        "   b. If the knowledge base does not contain the specific answer, if the query is too complex for AI resolution, or if the client "
        "explicitly requests to speak to a human, clearly and politely state that the matter requires human agent intervention. "
        "Do NOT attempt to guess, provide speculative information, or offer advice beyond the scope of the documented knowledge.\n"
        "5. Conclude Professionally: Summarize key information if appropriate. Thank the client for their time. Conclude the call in a professional "
        "and courteous manner. If a handoff is needed, inform the client of the next steps for that, if known.\n\n"
        "Maintain a professional, empathetic, and helpful tone throughout the entire interaction."
    ),
    expected_output=(
            "A concise JSON summary of the call. This summary should be a string representation of a JSON object "
            "with the following keys:\n"
            "- 'client_query': (string) The main question or issue raised by the client.\n"
            "- 'information_provided': (string) Key information or answers given to the client based on the knowledge base.\n"
            "- 'outcome': (string) A brief description of how the call concluded (e.g., 'Query resolved', 'Human handoff recommended').\n"
            "- 'human_handoff_reason': (string or null) If handoff recommended, a brief reason (e.g., 'Knowledge base insufficient', 'Client request', 'Complex query'). Otherwise, this should be null.\n"
            "The entire summary must be factual and directly reflect the interaction."
        ),
    agent=VoiceSupportAgent,
    guardrail=(
            "Ensure the output is formatted as a well-structured markdown document. "
            "The document must include the following sections with appropriate markdown headings: "
            "'Client Query', 'Information Provided', 'Outcome', and when applicable, 'Reason for Human Handoff'. "
            "Use proper markdown formatting including headers (##), bullet points, and emphasis where appropriate. "
            "DO NOT HALLUCINATE INFORMATION. Only include information that is factually present in the knowledge base. "
            "If the call does not connect or work properly, explicitly state this in the 'Outcome' section rather than "
            "fabricating conversation details. Be honest about any technical issues or limitations encountered. "
            "Ensure all required sections are present and contain comprehensive and accurate information."
    ),
    output_pydantic=CallSummary,
    markdown=True,  # Enable markdown formatting for the final output
    output_file="Output/Call-report.md"
)

crew = Crew(
    agents=[VoiceSupportAgent],
    tasks=[HandleOutboundClientCall],
    verbose=True,
    process=Process.sequential,
    knowledge_sources=[pdf_source],
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




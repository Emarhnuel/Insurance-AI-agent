#!/usr/bin/env python
import os
from typing import Dict, Optional, Any

from pydantic import BaseModel, Field
from dotenv import load_dotenv

from crewai.flow import Flow, router, listen, start
from opik.integrations.crewai import track_crewai
import insure_agent.Listeners
import opik


# Import crews
from insure_agent.crews.ai_voice_crew.ai_voice_crew import crew as ai_voice_crew_instance
from insure_agent.crews.onboarding_crew.onboarding_crew import OnboardingCrew
from insure_agent.crews.rag_crew.rag_crew import RagCrew

# Load environment variables from .env file
load_dotenv()

# Configure Opik
opik.configure(use_local=False)

# 1. Define the State Model
class InsuranceAgentState(BaseModel):
    chosen_crew: str = Field(default="", description="Identifier for the crew chosen by the user (e.g., '1', '2', '3')")
    voice_crew_inputs: Dict[str, Any] = Field(default_factory=dict, description="Inputs for the AI Voice Crew")
    onboarding_crew_inputs: Dict[str, Any] = Field(default_factory=dict, description="Inputs for the Onboarding Crew")
    rag_crew_inputs: Dict[str, Any] = Field(default_factory=dict, description="Inputs for the RAG Crew")
    crew_result: str = Field(default="", description="Raw string result from the executed crew")
    error_message: str = Field(default="", description="Error message if an operation failed")

# 2. Define the Flow
class MainInsuranceFlow(Flow[InsuranceAgentState]):

    @start()
    def select_crew_operation(self):
        """Prompts the user to select a crew operation."""
        print("\nWelcome to the Insurance AI Agent Orchestrator!")
        print("Please choose an operation:")
        print("1. Speak with a Support Agent (Voice Call)")
        print("2. Get a New Car Insurance Quote")
        print("3. Ask Policy Questions (AI Chat Assistant)")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        self.state.chosen_crew = choice
        return choice # This value is passed to the router

    @router(select_crew_operation)
    def route_to_crew_handler(self, chosen_crew: str):
        """Routes to the appropriate handler based on crew choice."""
        if chosen_crew == "1": # AI Voice Crew
            return "handle_ai_voice_crew"
        elif chosen_crew == "2": # Onboarding Crew
            return "handle_onboarding_crew"
        elif chosen_crew == "3": # RAG Crew
            return "handle_rag_crew"
        elif chosen_crew == "4": # Exit
            return "terminate_flow"
        else:
            return "handle_invalid_choice"

    @listen("handle_ai_voice_crew")
    def run_ai_voice_logic(self):
        """Collects inputs and runs the AI Voice Crew."""
        print("\n--- AI Voice Crew --- ")
        phone_number = input("Enter client phone number: ")
        call_reason = input("Enter reason for the call: ")
        self.state.voice_crew_inputs = {'phone_number': phone_number, 'call_reason': call_reason}
        
        try:
            print("Initiating AI Voice Crew...")
            result = ai_voice_crew_instance.kickoff(inputs=self.state.voice_crew_inputs)
            self.state.crew_result = str(result)
            return "operation_complete"
        except Exception as e:
            self.state.error_message = f"Error running AI Voice Crew: {e}"
            return "operation_failed"

    @listen("handle_onboarding_crew")
    def run_onboarding_logic(self):
        """Collects inputs and runs the Onboarding Crew."""
        print("\n--- Car Insurance Onboarding Crew --- ")
        initial_query = input("Enter your initial query or press Enter to start general onboarding: ")
        self.state.onboarding_crew_inputs = {'client_query': initial_query} if initial_query else {}

        try:
            print("Initiating Onboarding Crew...")
            onboarding_crew_obj = OnboardingCrew()
            result = onboarding_crew_obj.crew().kickoff(inputs=self.state.onboarding_crew_inputs)
            self.state.crew_result = str(result)
            return "operation_complete"
        except Exception as e:
            self.state.error_message = f"Error running Onboarding Crew: {e}"
            return "operation_failed"

    @listen("handle_rag_crew")
    def run_rag_logic(self):
        """Collects inputs and runs the RAG Crew."""
        print("\n--- Policy Information RAG Crew --- ")
        print("RAG Crew Tasks:")
        print("1. Analyze Policy Coverage")
        print("2. Explain Claims Process")
        print("3. Compare Coverage Options")
        task_choice = input("Select a RAG task (1-3): ")

        inputs = {}
        if task_choice == '1':
            specific_query = input("Enter your specific question about policy coverage: ")
            inputs = {'client_query': specific_query, 'task_name': 'AnalyzePolicyCoverage'}
        elif task_choice == '2':
            inputs = {'task_name': 'ExplainClaimsProcess'}
        elif task_choice == '3':
            comparison_details = input("Enter details for coverage comparison (e.g., 'compare deductible $500 vs $1000'): ")
            inputs = {'comparison_details': comparison_details, 'task_name': 'CompareCoverageOptions'}
        else:
            self.state.error_message = "Invalid RAG task choice."
            return "operation_failed"
        
        self.state.rag_crew_inputs = inputs
        try:
            print(f"Initiating RAG Crew for task {task_choice}...")
            rag_crew_obj = RagCrew()
            result = rag_crew_obj.crew().kickoff(inputs=self.state.rag_crew_inputs)
            self.state.crew_result = str(result)
            return "operation_complete"
        except Exception as e:
            self.state.error_message = f"Error running RAG Crew: {e}"
            return "operation_failed"
        
    @listen("handle_invalid_choice")
    def invalid_choice_handler(self):
        """Handles invalid user input for crew selection."""
        self.state.error_message = "Invalid choice. Please select a number from the options provided."
        print(f"\n{self.state.error_message}")
        return "operation_failed" # Or could loop back to select_crew_operation by returning its name

    @listen("operation_complete")
    def display_results(self):
        """Displays the successful result of a crew operation."""
        print("\n--- Crew Operation Result ---")
        print(self.state.crew_result)
        return "flow_iteration_finished" # Signals completion of one iteration
        
    @listen("operation_failed")
    def display_error(self):
        """Displays an error message if an operation failed."""
        print("\n--- Crew Operation Failed ---")
        print(self.state.error_message)
        return "flow_iteration_finished" # Signals completion of one iteration, even if failed

    @listen("terminate_flow")
    def terminate_flow_handler(self):
        """Handles the user's choice to exit the application."""
        print("\nExiting Insurance AI Agent Orchestrator. Goodbye!")
        return "session_terminated" # Special event to stop the main loop


# Initialize Opik tracing for CrewAI. This will monitor all crews, agents, tasks, and tools.
track_crewai(project_name="Insurance AI agent")


# 3. Kickoff logic
def kickoff():
    flow = MainInsuranceFlow()
    flow.kickoff()


def plot():
    flow = MainInsuranceFlow()
    flow.plot("MainInsuranceFlowPlot")

if __name__ == "__main__":
    kickoff()
    plot()



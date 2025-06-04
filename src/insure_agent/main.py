#!/usr/bin/env python
import os
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from crewai.flow import Flow, listen, start, persist, router

# Import your crews
from insure_agent.crews.onboarding_crew.onboarding_crew import OnboardingCrew
from insure_agent.crews.rag_crew.rag_crew import RagCrew
from insure_agent.crews.ai_voice_crew.ai_voice_crew import crew as VoiceCrew

# Load environment variables
load_dotenv()

# Define a structured state model for the Insurance flow
class InsuranceFlowState(BaseModel):
    # Client information
    client_name: str = ""
    client_phone: str = ""
    client_email: str = ""
    
    # User input and flow control
    user_query: str = ""
    current_phase: str = "greeting"  # greeting, query_routing, onboarding, rag, voice, complete
    
    # Insurance data
    client_profile: Dict[str, Any] = Field(default_factory=dict)
    selected_plan: Dict[str, Any] = Field(default_factory=dict)
    policy_questions: List[str] = Field(default_factory=list)
    policy_answers: Dict[str, str] = Field(default_factory=dict)
    
    # Call data
    call_summary: Optional[Dict[str, Any]] = None
    
    # Errors and status
    error_messages: List[str] = Field(default_factory=list)
    completion_status: Dict[str, bool] = Field(default_factory=lambda: {
        "onboarding": False,
        "rag": False,
        "voice": False
    })



class MainInsuranceFlow(Flow[InsuranceFlowState]):
    """
    Main Insurance Agent Flow
    
    This flow orchestrates the different insurance agent crews:
    1. Onboarding Crew: Handles client profiling and plan recommendation
    2. RAG Crew: Answers specific policy questions using knowledge base
    3. AI Voice Crew: Conducts follow-up calls for additional information
    """
    
    @start()
    def initialize_flow(self):
        """Initialize the insurance flow and greet the user"""
        print("Starting Insurance AI Agent Flow")
        print(f"Flow State ID: {self.state.id}")
        
        # Display greeting to the user
        print("\n" + "="*50)
        print("Hello! Welcome to our Insurance AI Agent.")
        print("How can we help you today?")
        print("="*50 + "\n")
        
        # Get user input
        user_input = input("> ")
        self.state.user_query = user_input
        
        print(f"Processing your request: '{user_input}'")
        
        return "query_routing"
    
    @listen(initialize_flow)
    def route_user_query(self, previous_result):
        """Route the user query to the appropriate crew based on content"""
        user_query = self.state.user_query.lower()
        
        # Collect basic information from user
        print("\nBefore we proceed, I need a few details from you:")
        self.state.client_name = input("What is your name? ")
        self.state.client_phone = input("What is your phone number? ")
        self.state.client_email = input("What is your email address? ")
        
        print(f"\nThank you, {self.state.client_name}! Now processing your request...\n")
        
        # Define routing keywords and phrases
        onboarding_keywords = ["new", "sign up", "register", "start", "policy", "buy", "purchase", 
                              "get insurance", "coverage", "quote", "new policy", "vehicle", "car"]
        
        rag_keywords = ["question", "explain", "what is", "how do", "information", "details", 
                       "learn about", "tell me", "understand", "policy details", "coverage details"]
        
        voice_keywords = ["speak", "call", "talk", "human", "agent", "specialist", "representative",
                         "phone", "discuss", "conversation", "chat"]
        
        # Route based on keyword matching
        if any(keyword in user_query for keyword in voice_keywords):
            print("I'll connect you with an insurance specialist via phone call.")
            return "voice"
        elif any(keyword in user_query for keyword in onboarding_keywords):
            print("I'll help you get set up with a new insurance policy.")
            return "onboarding"
        elif any(keyword in user_query for keyword in rag_keywords):
            print("I'll provide information about our insurance policies.")
            return "rag"
        else:
            # If uncertain, let user choose
            print("\nI'm not sure what exactly you need. What would you like to do?")
            print("1. Get a new insurance policy")
            print("2. Ask questions about our insurance policies")
            print("3. Speak with an insurance specialist")
            
            choice = input("\nPlease select an option (1/2/3): ")
            
            if choice == "1":
                return "onboarding"
            elif choice == "2":
                return "rag"
            elif choice == "3":
                return "voice"
            else:
                print("Invalid choice. Let me help you with policy information.")
                return "rag"
    
    @router(route_user_query)
    def route_to_crew(self, crew_type):
        """Route to the appropriate crew based on user query analysis"""
        print(f"Routing to: {crew_type}")
        self.state.current_phase = crew_type
        return crew_type
    
    @listen("onboarding")
    def run_onboarding_crew(self):
        """Run the onboarding process using the Onboarding Crew"""
        print("\n" + "="*50)
        print("INITIATING ONBOARDING PROCESS")
        print("="*50 + "\n")
        
        try:
            # Initialize the OnboardingCrew
            onboarding_crew = OnboardingCrew().crew()
            
            # Run the onboarding process
            # Note: In a real application, you might collect more specific inputs first
            result = onboarding_crew.kickoff(
                inputs={
                    "client_name": self.state.client_name,
                    "client_email": self.state.client_email,
                    "client_phone": self.state.client_phone,
                    "client_query": self.state.user_query
                }
            )
            
            # Store the results in our state
            if hasattr(result, 'dict'):
                self.state.client_profile = result.dict()
                self.state.selected_plan = result.dict().get("recommended_plan", {})
            else:
                self.state.client_profile = {"raw_output": str(result)}
            
            self.state.completion_status["onboarding"] = True
            print("\nOnboarding process completed successfully")
            
            return "complete_flow"
            
        except Exception as e:
            error_msg = f"Error in onboarding process: {str(e)}"
            self.state.error_messages.append(error_msg)
            print(error_msg)
            return "error_handler"
    
    @listen("rag")
    def run_rag_crew(self):
        """Run the RAG process to answer policy questions"""
        print("\n" + "="*50)
        print("ANSWERING POLICY QUESTIONS")
        print("="*50 + "\n")
        
        try:
            # Take the user's initial query as the first question
            self.state.policy_questions = [self.state.user_query]
            
            # Ask if user has additional questions
            print("\nDo you have any specific policy questions? (Type 'done' when finished)")
            
            while True:
                question = input("> ")
                if question.lower() == 'done':
                    break
                self.state.policy_questions.append(question)
            
            # Initialize the RAG Crew
            rag_crew = RagCrew().crew()
            
            # Process each question
            print("\nProcessing your questions...\n")
            for question in self.state.policy_questions:
                print(f"\nQ: {question}")
                
                # Run the RAG process for each question
                result = rag_crew.kickoff(
                    inputs={"user_query": question}
                )
                
                # Store and display the answer
                answer = str(result)
                self.state.policy_answers[question] = answer
                print(f"A: {answer}\n")
            
            self.state.completion_status["rag"] = True
            print("\nAll questions have been answered.")
            
            # Ask if they want to speak with a specialist
            follow_up = input("\nWould you like to speak with an insurance specialist for more details? (yes/no): ")
            
            if follow_up.lower() == 'yes':
                return "voice"
            else:
                return "complete_flow"
            
        except Exception as e:
            error_msg = f"Error in RAG process: {str(e)}"
            self.state.error_messages.append(error_msg)
            print(error_msg)
            return "error_handler"
    
    @listen("voice")
    def run_voice_crew(self):
        """Run the Voice process to conduct follow-up calls"""
        print("\n" + "="*50)
        print("INITIATING SPECIALIST CALL")
        print("="*50 + "\n")
        
        try:
            # Prepare call reason based on user query
            call_reason = f"Follow-up on: {self.state.user_query}"
            
            print(f"\nPreparing to call {self.state.client_name} at {self.state.client_phone}")
            print("An insurance specialist will call you shortly.")
            print("Please confirm your phone number is correct.")
            
            confirm = input("Is this phone number correct? (yes/no): ")
            
            if confirm.lower() != 'yes':
                self.state.client_phone = input("Please enter your correct phone number: ")
                print(f"Updated phone number: {self.state.client_phone}")
            
            print("\nInitiating call...")
            # Run the AI Voice Crew with the client's phone number
            result = VoiceCrew.kickoff(
                inputs={
                    "phone_number": self.state.client_phone,
                    "call_reason": call_reason
                }
            )
            
            # Store the call summary
            if hasattr(result, 'dict'):
                self.state.call_summary = result.dict()
            else:
                self.state.call_summary = {"raw_output": str(result)}
            
            self.state.completion_status["voice"] = True
            print("\nCall has been scheduled. A specialist will contact you shortly.")
            
            return "complete_flow"
            
        except Exception as e:
            error_msg = f"Error in voice process: {str(e)}"
            self.state.error_messages.append(error_msg)
            print(error_msg)
            return "error_handler"
    
    @listen("error_handler")
    def handle_errors(self):
        """Handle any errors that occurred in the flow"""
        print("\n" + "="*50)
        print("ERROR ENCOUNTERED")
        print("="*50 + "\n")
        
        print(f"We apologize, but an error occurred while processing your request:")
        for error in self.state.error_messages:
            print(f"  - {error}")
        
        print("\nPlease contact our customer support at support@insurance.com")
        print("or call us at 1-800-INSURANCE for assistance.")
        
        return "terminate_flow"
    
    @listen("complete_flow")
    def complete_flow_handler(self):
        """Process the completed flow and prepare final output"""
        print("\n" + "="*50)
        print("THANK YOU FOR USING OUR SERVICE")
        print("="*50 + "\n")
        
        print(f"Thank you, {self.state.client_name}, for using our Insurance AI Agent!")
        
        # Display summary based on which services were used
        if self.state.completion_status["onboarding"]:
            print("\n• Your insurance profile has been created.")
            print("• A confirmation email will be sent to your registered email address.")
            
        if self.state.completion_status["rag"]:
            print("\n• We've answered your policy questions.")
            print("• You can access this information anytime by logging into your account.")
            
        if self.state.completion_status["voice"]:
            print("\n• A specialist will call you shortly at your provided number.")
            print("• Please keep your phone available.")
        
        print("\nIs there anything else we can help you with today? (yes/no)")
        restart = input("> ")
        
        if restart.lower() == 'yes':
            print("\nRestarting the insurance agent flow...\n")
            # Create a new flow instance since we can't easily restart this one
            new_flow = MainInsuranceFlow()
            new_flow.kickoff()
            return "terminate_flow"
        else:
            return "terminate_flow"
    
    @listen("terminate_flow")
    def terminate_flow_handler(self):
        """Clean up and terminate the flow"""
        print("\nThank you for choosing our insurance services.")
        print("Have a great day!")
        
        return {"status": "completed", "flow_id": self.state.id}


def kickoff():
    """Run the insurance flow"""
    flow = MainInsuranceFlow()
    flow.kickoff()


def plot():
    """Generate a visual plot of the insurance flow"""
    flow = MainInsuranceFlow()
    flow.plot("InsuranceAgentFlowPlot")


if __name__ == "__main__":
    kickoff()
    plot()

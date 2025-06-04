from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import json

# --- Structured Insurance Plan Data ---
INSURANCE_PLANS_DATA: List[Dict[str, Any]] = [
    {
        "plan_name": "Basic Protection Plan",
        "purpose": "Designed for drivers seeking the most economical option to meet minimum legal requirements for vehicle operation.",
        "core_coverages": [
            "Bodily Injury Liability", 
            "Property Damage Liability"
        ],
        "ideal_for": [
            "Drivers on a very tight budget.",
            "Individuals with older vehicles that have minimal market value.",
            "Those who prefer to self-insure for damage to their own vehicle."
        ],
        "key_considerations": "This plan offers no coverage for damage to your own vehicle (e.g., from collisions, theft, or natural disasters) and does not include medical payments for you or your passengers. It provides essential legal compliance but limited personal financial protection beyond third-party liability."
    },
    {
        "plan_name": "Standard Shield Plan",
        "purpose": "A popular choice offering a balanced combination of protection for both you and your vehicle, covering common risks.",
        "core_coverages": [
            "Bodily Injury Liability", 
            "Property Damage Liability", 
            "Collision Coverage", 
            "Comprehensive Coverage", 
            "Uninsured/Underinsured Motorist (UM/UIM) Coverage"
        ],
        "ideal_for": [
            "The majority of drivers who want reliable protection for their own vehicle investment.",
            "Drivers with newer or moderately valued vehicles.",
            "Those who want peace of mind against common road hazards and unforeseen events."
        ],
        "key_benefits": "Provides robust coverage for your vehicle, ensuring repairs or replacement in many scenarios. It bridges the gap between minimum legal requirements and comprehensive personal protection. Deductibles apply to Collision and Comprehensive coverages."
    },
    {
        "plan_name": "Premium Peace Plan",
        "purpose": "Our most comprehensive offering, providing maximum protection, convenience, and a wide array of added benefits for ultimate peace of mind.",
        "core_coverages": [
            "Bodily Injury Liability", 
            "Property Damage Liability", 
            "Collision Coverage", 
            "Comprehensive Coverage", 
            "Uninsured/Underinsured Motorist (UM/UIM) Coverage",
            "Medical Payments (MedPay) / Personal Injury Protection (PIP)",
            "Roadside Assistance",
            "Rental Car Reimbursement"
        ],
        "ideal_for": [
            "Drivers who want the highest level of protection for themselves, their passengers, and their vehicle.",
            "Owners of new or high-value vehicles.",
            "Those who prioritize convenience and want minimal out-of-pocket costs or disruptions in the event of an incident."
        ],
        "key_advantages": "Offers extensive financial security and practical support, minimizing stress during unexpected events. It's designed for drivers who demand comprehensive coverage and value added services. Optional Add-ons: Often includes eligibility for premium endorsements like Gap Insurance, New Car Replacement, or Accident Forgiveness (subject to terms)."
    }
]

# --- Pydantic Model for Tool Arguments ---
class InsurancePlanDatabaseToolInput(BaseModel):
    """Input schema for the InsurancePlanDatabaseTool."""
    action: str = Field(description="The action to perform: 'list_all_plans', 'get_plan_details', 'find_plans_by_coverage'.")
    plan_name: Optional[str] = Field(default=None, description="Name of the plan to get details for (required if action is 'get_plan_details'). Case-sensitive.")
    coverage_type: Optional[str] = Field(default=None, description="Type of coverage to search for (required if action is 'find_plans_by_coverage'). Case-insensitive partial match.")

# --- InsurancePlanDatabaseTool ---
class InsurancePlanDatabaseTool(BaseTool):
    name: str = "Insurance Plan Database Tool"
    description: str = (
        "Queries a database of available insurance plans. "
        "Use this tool to: "
        "1. List all available insurance plans (action: 'list_all_plans'). "
        "2. Get detailed information for a specific plan by its name (action: 'get_plan_details', requires 'plan_name'). "
        "3. Find plans that include a specific type of coverage (action: 'find_plans_by_coverage', requires 'coverage_type')."
    )
    args_schema: type[BaseModel] = InsurancePlanDatabaseToolInput

    def _run(self, action: str, plan_name: Optional[str] = None, coverage_type: Optional[str] = None) -> str:
        if action == "list_all_plans":
            return self._list_all_plans()
        elif action == "get_plan_details":
            if not plan_name:
                return json.dumps({"error": "'plan_name' is required for action 'get_plan_details'."})
            return self._get_plan_details(plan_name)
        elif action == "find_plans_by_coverage":
            if not coverage_type:
                return json.dumps({"error": "'coverage_type' is required for action 'find_plans_by_coverage'."})
            return self._find_plans_by_coverage(coverage_type)
        else:
            return json.dumps({"error": f"Invalid action: {action}. Valid actions are 'list_all_plans', 'get_plan_details', 'find_plans_by_coverage'."})

    def _list_all_plans(self) -> str:
        """Returns a summary of all available insurance plans."""
        plan_summaries = [
            {"plan_name": plan["plan_name"], "purpose": plan["purpose"]}
            for plan in INSURANCE_PLANS_DATA
        ]
        return json.dumps(plan_summaries)

    def _get_plan_details(self, plan_name: str) -> str:
        """Returns detailed information for a specific plan by its name."""
        for plan in INSURANCE_PLANS_DATA:
            if plan["plan_name"].lower() == plan_name.lower():
                return json.dumps(plan)
        return json.dumps({"error": f"Plan '{plan_name}' not found."})

    def _find_plans_by_coverage(self, coverage_type: str) -> str:
        """Returns plans that include a specific type of coverage."""
        matching_plans = []
        for plan in INSURANCE_PLANS_DATA:
            for coverage in plan["core_coverages"]:
                if coverage_type.lower() in coverage.lower():
                    matching_plans.append({
                        "plan_name": plan["plan_name"],
                        "purpose": plan["purpose"],
                        "core_coverages": plan["core_coverages"]
                    })
                    break # Avoid adding the same plan multiple times if it matches multiple ways
        
        if not matching_plans:
            return json.dumps({"message": f"No plans found offering '{coverage_type}'."})
        return json.dumps(matching_plans)

# Example Usage (for testing purposes):
if __name__ == '__main__':
    tool = InsurancePlanDatabaseTool()

    # Test list_all_plans
    print("--- Listing all plans ---")
    print(tool._run(action='list_all_plans'))

    # Test get_plan_details
    print("\n--- Getting details for 'Standard Shield Plan' ---")
    print(tool._run(action='get_plan_details', plan_name='Standard Shield Plan'))
    print("\n--- Getting details for 'NonExistent Plan' ---")
    print(tool._run(action='get_plan_details', plan_name='NonExistent Plan'))

    # Test find_plans_by_coverage
    print("\n--- Finding plans with 'Collision Coverage' ---")
    print(tool._run(action='find_plans_by_coverage', coverage_type='Collision Coverage'))
    print("\n--- Finding plans with 'Roadside Assistance' ---")
    print(tool._run(action='find_plans_by_coverage', coverage_type='Roadside Assistance'))
    print("\n--- Finding plans with 'Teleportation Insurance' ---")
    print(tool._run(action='find_plans_by_coverage', coverage_type='Teleportation Insurance'))
    print("\n--- Invalid action ---")
    print(tool._run(action='fly_to_moon'))
    print("\n--- Missing plan_name for get_plan_details ---")
    print(tool._run(action='get_plan_details'))

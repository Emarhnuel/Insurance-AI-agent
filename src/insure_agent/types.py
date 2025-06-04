from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ClientProfile(BaseModel):
    """Structured representation of a client's insurance profile"""
    client: Dict[str, any] = Field(description="Client personal information")
    vehicles: List[Dict[str, any]] = Field(description="Details of vehicles to be insured")
    drivers: List[Dict[str, any]] = Field(description="Information about all drivers")
    current_coverage: Optional[Dict[str, any]] = Field(description="Current insurance details if available")
    risk_assessment: Dict[str, any] = Field(description="Risk factors and assessment")
    coverage_preferences: Dict[str, any] = Field(description="Client's coverage priorities and constraints")
    notes: Dict[str, any] = Field(description="Additional notes and client concerns")


class InsuranceRecommendation(BaseModel):
    """Structured representation of an insurance recommendation"""
    recommended_plan: Dict[str, any] = Field(description="Primary recommended insurance plan")
    alternatives: List[Dict[str, any]] = Field(description="Alternative plan options")
    justification: str = Field(description="Detailed explanation of recommendation rationale")
    next_steps: List[str] = Field(description="Actions for the client to take next")

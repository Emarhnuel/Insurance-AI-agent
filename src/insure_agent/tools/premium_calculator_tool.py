from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

# --- Pydantic Model for Tool Arguments ---
class PremiumCalculatorToolInput(BaseModel):
    """Input schema for the PremiumCalculatorTool."""
    vehicle_make: str = Field(description="Make of the vehicle (e.g., Toyota, Honda).")
    vehicle_model: str = Field(description="Model of the vehicle (e.g., Camry, Civic).")
    vehicle_year: int = Field(description="Year of manufacture of the vehicle (e.g., 2022).")
    vehicle_value: float = Field(description="Estimated current market value of the vehicle.")
    safety_features: List[str] = Field(default_factory=list, description="List of safety features in the vehicle (e.g., ['ABS', 'Airbags']).")
    annual_mileage: int = Field(description="Estimated annual mileage driven.")
    primary_driver_age: int = Field(description="Age of the primary driver.")
    primary_driver_experience_years: int = Field(description="Years of driving experience for the primary driver.")
    primary_driver_claims_last_5_years: int = Field(description="Number of at-fault claims by the primary driver in the last 5 years.")
    garage_zip_code: str = Field(description="ZIP code where the vehicle is primarily garaged.")
    coverage_bodily_injury_person: float = Field(description="Bodily injury liability coverage limit per person.")
    coverage_bodily_injury_accident: float = Field(description="Bodily injury liability coverage limit per accident.")
    coverage_property_damage: float = Field(description="Property damage liability coverage limit.")
    coverage_comprehensive_deductible: float = Field(description="Deductible for comprehensive coverage.")
    coverage_collision_deductible: float = Field(description="Deductible for collision coverage.")
    eligible_discounts: List[str] = Field(default_factory=list, description="List of discount codes the client is eligible for (e.g., ['SAFE_DRIVER', 'MULTI_POLICY']).")

# --- PremiumCalculatorTool ---
class PremiumCalculatorTool(BaseTool):
    name: str = "Premium Calculator Tool"
    description: str = (
        "Calculates an estimated car insurance premium based on vehicle details, driver profile, "
        "coverage selections, and eligible discounts. Input should be a JSON object matching the "
        "required schema with vehicle, driver, and coverage information."
    )
    args_schema: type[BaseModel] = PremiumCalculatorToolInput

    def _run(
        self,
        vehicle_make: str,
        vehicle_model: str,
        vehicle_year: int,
        vehicle_value: float,
        safety_features: List[str],
        annual_mileage: int,
        primary_driver_age: int,
        primary_driver_experience_years: int,
        primary_driver_claims_last_5_years: int,
        garage_zip_code: str, # Included in schema, but not used in simplified logic below
        coverage_bodily_injury_person: float,
        coverage_bodily_injury_accident: float, # Included in schema, but not used in simplified logic below
        coverage_property_damage: float,
        coverage_comprehensive_deductible: float,
        coverage_collision_deductible: float,
        eligible_discounts: List[str]
    ) -> str:
        """
        Calculates an estimated car insurance premium.
        NOTE: This is a simplified placeholder implementation.
        The actual calculation logic should be based on 'Premium Calculation Rules.pdf' 
        and would require a more sophisticated model.
        """
        # Placeholder premium calculation logic
        base_premium = 500.0  # Starting base premium

        # Adjust based on vehicle value and age
        if vehicle_value > 30000:
            base_premium += vehicle_value * 0.02 # 2% of value over 30k
        if vehicle_year < 2015:
            base_premium += (2015 - vehicle_year) * 20 # $20 per year older than 2015
        elif vehicle_year > 2020:
            base_premium -= (vehicle_year - 2020) * 15 # $15 reduction per year newer than 2020

        # Adjust based on driver age and experience
        if primary_driver_age < 25:
            base_premium += (25 - primary_driver_age) * 30 # $30 per year younger than 25
        elif primary_driver_age > 65:
             base_premium += (primary_driver_age - 65) * 10 # $10 per year older than 65

        if primary_driver_experience_years < 2:
            base_premium += 150 # Flat increase for less than 2 years experience
        
        # Adjust based on claims
        base_premium += primary_driver_claims_last_5_years * 100 # $100 per claim

        # Adjust based on coverage limits (very simplified)
        base_premium += (coverage_bodily_injury_person / 50000) * 10 
        base_premium += (coverage_property_damage / 25000) * 10

        # Adjust based on deductibles (higher deductible = lower premium)
        base_premium -= (coverage_comprehensive_deductible / 250) * 5 
        base_premium -= (coverage_collision_deductible / 250) * 5
        
        # Apply discounts
        discount_percentage = 0.0
        if "SAFE_DRIVER" in eligible_discounts:
            discount_percentage += 0.10 # 10% discount
        if "MULTI_POLICY" in eligible_discounts:
            discount_percentage += 0.05 # 5% discount
        if "GOOD_STUDENT" in eligible_discounts and primary_driver_age <= 25:
            discount_percentage += 0.07 # 7% discount
        
        calculated_premium = base_premium * (1 - discount_percentage)
        
        # Ensure premium is not negative and has a minimum
        calculated_premium = max(50.0, calculated_premium) # Minimum premium of $50

        return (
            f"Estimated Premium: ${calculated_premium:.2f}. "
            f"Factors considered: vehicle (make: {vehicle_make}, model: {vehicle_model}, year: {vehicle_year}, value: ${vehicle_value:.2f}), "
            f"driver (age: {primary_driver_age}, experience: {primary_driver_experience_years} yrs, claims: {primary_driver_claims_last_5_years}), "
            f"coverages (BI Person: ${coverage_bodily_injury_person:.0f}, PD: ${coverage_property_damage:.0f}, Comp Deduct: ${coverage_comprehensive_deductible:.0f}, Coll Deduct: ${coverage_collision_deductible:.0f}). "
            f"Discounts applied: {', '.join(eligible_discounts) if eligible_discounts else 'None'}. "
            f"Note: This is a simplified estimation based on placeholder logic. Actual premium will vary based on full underwriting according to 'Premium Calculation Rules.pdf'."
        )

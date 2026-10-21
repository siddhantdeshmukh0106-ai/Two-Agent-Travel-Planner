from typing import List, Optional
from pydantic import BaseModel, Field
import math
from pydantic import model_validator


# ==========================================
# ATTRACTION MODEL
# ==========================================

class Attraction(BaseModel):
    name: str
    description: str
    location: str

    entry_fee: Optional[float] = Field(
        default=None,
        ge=0,
        description="Entry fee per person in INR"
    )

    opening_hours: Optional[str] = None

    visit_duration_hours: float = Field(
        gt=0,
        description="Recommended visiting duration in hours"
    )

    source_url: Optional[str] = None


# ==========================================
# LOCAL FOOD MODEL
# ==========================================

class LocalFood(BaseModel):
    name: str
    description: str

    estimated_cost: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated cost per person in INR"
    )

    recommended_place: Optional[str] = None
    source_url: Optional[str] = None


# ==========================================
# DESTINATION RESEARCH MODEL
# ==========================================

class DestinationResearch(BaseModel):

    destination: str
    overview: str

    top_attractions: List[Attraction] = Field(
        min_length=3,
        max_length=3,
        description="Exactly 3 popular tourist attractions"
    )

    hidden_gems: List[Attraction] = Field(
        min_length=2,
        max_length=2,
        description="Exactly 2 lesser-known attractions"
    )

    local_food: List[LocalFood] = Field(
        min_length=3,
        max_length=3,
        description="Exactly 3 local food recommendations"
    )

    travel_tips: List[str]

    budget_notes: str

    verification_notes: Optional[str] = None
    
# ==========================================
# TRAVEL ACTIVITY MODEL
# ==========================================

class TravelActivity(BaseModel):
    activity_name: str
    location: str
    description: str

    start_time: str = Field(
        description="Activity start time in HH:MM format"
    )

    end_time: str = Field(
        description="Activity end time in HH:MM format"
    )

    duration_minutes: int = Field(
        gt=0,
        description="Activity duration in minutes"
    )

    estimated_cost: Optional[float] = Field(
        default=None,
        ge=0,
        description="Total activity cost for all travelers in INR"
    )

    travel_distance_km: Optional[float] = Field(
        default=None,
        ge=0,
        description="Distance from previous location in kilometers"
    )

    travel_time_minutes: Optional[float] = Field(
        default=None,
        ge=0,
        description="Travel time from previous location in minutes"
    )

    activity_type: str = Field(
        description="Attraction, Food, Transport, Rest, or Other"
    )


# ==========================================
# DAILY ITINERARY MODEL
# ==========================================

class DailyItinerary(BaseModel):
    day_number: int = Field(ge=1)

    date: str = Field(
        description="Travel date in YYYY-MM-DD format"
    )

    activities: List[TravelActivity] = Field(
        min_length=1,
        description="Activities scheduled for this day"
    )

    daily_estimated_cost: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated total expenses for the day in INR"
    )

    daily_notes: Optional[str] = None


# ==========================================
# COMPLETE TRAVEL ITINERARY MODEL
# ==========================================

class TravelItinerary(BaseModel):
    destination: str

    start_date: str
    end_date: str

    travelers: int = Field(
        ge=1,
        description="Number of travelers"
    )

    total_budget: float = Field(
        ge=0,
        description="Total trip budget in INR"
    )

    days: List[DailyItinerary] = Field(
        min_length=1,
        description="Day-wise travel itinerary"
    )

    travel_tips: List[str] = Field(
        default_factory=list
    )

    assumptions: List[str] = Field(
        default_factory=list
    )
    
    budget_breakdown: Optional["BudgetBreakdown"] = None
    
# ==========================================
# BUDGET BREAKDOWN MODEL
# ==========================================

class BudgetBreakdown(BaseModel):

    attraction_cost: Optional[float] = Field(default=None, ge=0)
    food_cost: Optional[float] = Field(default=None, ge=0)
    transport_cost: Optional[float] = Field(default=None, ge=0)
    accommodation_cost: Optional[float] = Field(default=None, ge=0)
    other_cost: Optional[float] = Field(default=None, ge=0)

    total_budget: float = Field(ge=0)

    total_expenses: float = Field(
        ge=0,
        description="Sum of all supplied expense categories in INR"
    )

    remaining_budget: float = Field(
        description="Total budget minus calculated expenses"
    )

    within_budget: bool

    budget_status: str = Field(
        description="WITHIN BUDGET, OVER BUDGET, or PARTIAL ESTIMATE"
    )

    budget_notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_budget_calculations(self):

        categories = [
            self.attraction_cost,
            self.food_cost,
            self.transport_cost,
            self.accommodation_cost,
            self.other_cost
        ]

        calculated_total = sum(
            cost for cost in categories if cost is not None
        )

        # Verify expense calculations
        if not math.isclose(
            self.total_expenses,
            calculated_total,
            abs_tol=0.01
        ):
            raise ValueError(
                "Total expenses do not match category expenses."
            )

        calculated_remaining = self.total_budget - calculated_total

        # Verify remaining budget
        if not math.isclose(
            self.remaining_budget,
            calculated_remaining,
            abs_tol=0.01
        ):
            raise ValueError(
                "Remaining budget calculation is incorrect."
            )

        # Verify within-budget status
        expected_status = calculated_total <= self.total_budget

        if self.within_budget != expected_status:
            raise ValueError(
                "Within-budget status is incorrect."
            )

        # Verify budget status
        valid_statuses = {
            "WITHIN BUDGET",
            "OVER BUDGET",
            "PARTIAL ESTIMATE"
        }

        if self.budget_status not in valid_statuses:
            raise ValueError("Invalid budget status.")

        # Unknown expenses mean the total is incomplete
        if any(cost is None for cost in categories):
            if self.budget_status != "PARTIAL ESTIMATE":
                raise ValueError(
                    "Missing expenses require PARTIAL ESTIMATE status."
                )

        elif self.budget_status != "PARTIAL ESTIMATE":
            if expected_status and self.budget_status != "WITHIN BUDGET":
                raise ValueError("Expected WITHIN BUDGET status.")
            if not expected_status and self.budget_status != "OVER BUDGET":
                raise ValueError("Expected OVER BUDGET status.")

        
        return self

TravelItinerary.model_rebuild()
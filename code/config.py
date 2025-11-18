"""
Configuration module for AEON GovTech Platform
Smart City & Community Management System
"""
from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum
import json
from pathlib import Path


class GovernanceType(Enum):
    """Types of communities/governance models"""
    MUNICIPALITY = "municipality"
    ECO_VILLAGE = "eco_village"
    CAMPUS = "campus"
    ECONOMIC_ZONE = "economic_zone"
    DISTRICT = "district"


@dataclass
class CommunityConfig:
    """Configuration for smart city/community management"""
    
    # Community basics
    name: str = "Demo City"
    governance_type: str = "municipality"
    population_size: int = 10000
    area_km2: float = 50.0
    annual_budget: float = 8_000_000.0  # EUR
    
    # Public services capacity (daily)
    service_capacity: Dict[str, float] = field(default_factory=lambda: {
        "water_supply": 50000.0,        # m³/day
        "electricity": 200.0,            # MWh/day
        "waste_management": 15.0,        # tons/day
        "public_transport": 5000.0,      # trips/day
        "internet_bandwidth": 10.0       # Gbps
    })
    # Simulation parameters
    time_scale: float = 1.0  # 1.0 = real-time, higher = faster
    day_duration: int = 24  # Standard day in hours
    
    
    # Service consumption rates (per person per day)
    consumption_rates: Dict[str, float] = field(default_factory=lambda: {
        "water_supply": 0.15,          # m³/person/day
        "electricity": 0.008,           # MWh/person/day
        "waste_management": 0.0015,     # tons/person/day
        "public_transport": 0.5,        # trips/person/day
        "internet_bandwidth": 0.001     # Gbps/person/day
    })
    
    # Infrastructure health parameters
    system_degradation_rate: float = 0.001  # per day
    critical_threshold: float = 0.3  # system health percentage
    
    # Event probabilities (per day)
    event_probabilities: Dict[str, float] = field(default_factory=lambda: {
        "infrastructure_failure": 0.03,
        "public_complaint": 0.15,
        "emergency_call": 0.08,
        "environmental_alert": 0.05,
        "budget_issue": 0.02,
        "civic_event": 0.10,
        "policy_proposal": 0.06
    })
    
    # Budget allocation (% of total)
    budget_allocation: Dict[str, float] = field(default_factory=lambda: {
        "infrastructure": 0.30,
        "public_services": 0.25,
        "healthcare": 0.15,
        "education": 0.15,
        "public_safety": 0.10,
        "administration": 0.05
    })
    
    # AI decision-making parameters
    ai_intervention_threshold: float = 0.7
    human_override_required: List[str] = field(default_factory=lambda: [
        "major_budget_allocation",
        "policy_changes",
        "emergency_declarations"
    ])
    
    # DAO Governance
    voting_quorum: float = 0.20  # 20% citizen participation
    proposal_threshold: int = 100  # signatures needed
    voting_period_days: int = 14
    
    # Logging and persistence
    log_level: str = "INFO"
    save_interval: int = 30  # save state every N days
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        config_dict = {
            "name": self.name,
            "governance_type": self.governance_type,
            "population_size": self.population_size,
            "area_km2": self.area_km2,
            "annual_budget": self.annual_budget,
            "service_capacity": self.service_capacity,
            "time_scale": self.time_scale,
            "day_duration": self.day_duration,
            "consumption_rates": self.consumption_rates,
            "system_degradation_rate": self.system_degradation_rate,
            "critical_threshold": self.critical_threshold,
            "event_probabilities": self.event_probabilities,
            "budget_allocation": self.budget_allocation,
            "ai_intervention_threshold": self.ai_intervention_threshold,
            "human_override_required": self.human_override_required,
            "voting_quorum": self.voting_quorum,
            "proposal_threshold": self.proposal_threshold,
            "voting_period_days": self.voting_period_days,
            "log_level": self.log_level,
            "save_interval": self.save_interval
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'CommunityConfig':
        """Load configuration from JSON file"""
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return cls(**config_dict)


# Default configuration instance
DEFAULT_CONFIG = CommunityConfig()

# Community templates for different use cases
COMMUNITY_TEMPLATES = {
    'small_town': CommunityConfig(
        name="Small Town Demo",
        governance_type="municipality",
        population_size=8000,
        area_km2=25.0,
        annual_budget=5_000_000
    ),
    'eco_village': CommunityConfig(
        name="Eco Village",
        governance_type="eco_village",
        population_size=500,
        area_km2=2.5,
        annual_budget=300_000,
        service_capacity={
            "water_supply": 300.0,
            "electricity": 5.0,
            "waste_management": 0.5,
            "public_transport": 50.0,
            "internet_bandwidth": 1.0
        }
    ),
    'university_campus': CommunityConfig(
        name="University Campus",
        governance_type="campus",
        population_size=12000,
        area_km2=1.5,
        annual_budget=8_000_000
    )
}

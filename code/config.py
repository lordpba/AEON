"""
Configuration module for AEON Autonomous Governance System
"""
from dataclasses import dataclass, field
from typing import Dict, List
import json
from pathlib import Path


@dataclass
class ColonyConfig:
    """Configuration for the Mars colony simulation"""
    
    # Colony basics
    
    # Simulation parameters
    name: str = "AEON Alpha"
    population_size: int = 5
    starting_resources: Dict[str, float] = field(default_factory=lambda: {
        "water": 10000.0,      # liters
        "food": 5000.0,        # kg
        "energy": 50000.0,     # kWh
        "oxygen": 100000.0,    # liters
        "building_materials": 1000.0  # units
    })
    # Simulation parameters
    time_scale: float = 0.1  # 1.0 = real-time, higher = faster
    sol_duration: int = 24.65  # Mars day in hours
    
    # Resource consumption rates (per person per sol)
    consumption_rates: Dict[str, float] = field(default_factory=lambda: {
        "water": 50.0,         # liters/person/sol
        "food": 2.0,           # kg/person/sol
        "energy": 100.0,       # kWh/person/sol
        "oxygen": 800.0        # liters/person/sol
    })
    
    # System health parameters
    system_degradation_rate: float = 0.001  # per sol
    critical_threshold: float = 0.3  # system health percentage
    
    # Event probabilities (per sol)
    event_probabilities: Dict[str, float] = field(default_factory=lambda: {
        "solar_storm": 0.02,
        "equipment_failure": 0.05,
        "medical_emergency": 0.03,
        "conflict": 0.04,
        "discovery": 0.01
    })
    
    # AI decision-making parameters
    ai_intervention_threshold: float = 0.7
    human_override_required: List[str] = field(default_factory=lambda: [
        "major_resource_allocation",
        "population_expansion",
        "emergency_evacuation"
    ])
    
    # Logging and persistence
    log_level: str = "INFO"
    save_interval: int = 100  # save state every N sols
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        config_dict = {
            "name": self.name,
            "population_size": self.population_size,
            "starting_resources": self.starting_resources,
            "time_scale": self.time_scale,
            "sol_duration": self.sol_duration,
            "consumption_rates": self.consumption_rates,
            "system_degradation_rate": self.system_degradation_rate,
            "critical_threshold": self.critical_threshold,
            "event_probabilities": self.event_probabilities,
            "ai_intervention_threshold": self.ai_intervention_threshold,
            "human_override_required": self.human_override_required,
            "log_level": self.log_level,
            "save_interval": self.save_interval
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'ColonyConfig':
        """Load configuration from JSON file"""
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return cls(**config_dict)


# Default configuration instance
DEFAULT_CONFIG = ColonyConfig()

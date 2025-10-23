"""
Simulation Engine for AEON - Time-based event and state management
"""
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from loguru import logger


class EventType(Enum):
    """Types of events that can occur in the simulation"""
    SOLAR_STORM = "solar_storm"
    EQUIPMENT_FAILURE = "equipment_failure"
    MEDICAL_EMERGENCY = "medical_emergency"
    SOCIAL_CONFLICT = "social_conflict"
    RESOURCE_CRISIS = "resource_crisis"
    DISCOVERY = "discovery"
    BIRTH = "birth"
    SYSTEM_UPGRADE = "system_upgrade"


class EventSeverity(Enum):
    """Severity levels for events"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class SimulationEvent:
    """Represents an event in the simulation"""
    event_type: EventType
    severity: EventSeverity
    timestamp: float  # Sol number
    description: str
    affected_systems: List[str] = field(default_factory=list)
    requires_human_intervention: bool = False
    resolved: bool = False
    resolution_time: Optional[float] = None
    consequences: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization"""
        return {
            "event_type": self.event_type.value,
            "severity": self.severity.value,
            "timestamp": self.timestamp,
            "description": self.description,
            "affected_systems": self.affected_systems,
            "requires_human_intervention": self.requires_human_intervention,
            "resolved": self.resolved,
            "resolution_time": self.resolution_time,
            "consequences": self.consequences
        }


class SimulationClock:
    """Manages simulation time progression"""
    
    def __init__(self, time_scale: float = 1.0, sol_duration_hours: float = 24.65):
        self.time_scale = time_scale  # Multiplier for simulation speed
        self.sol_duration = sol_duration_hours * 3600  # Convert to seconds
        self.current_sol = 0.0
        self.start_time = time.time()
        self.paused = False
        self.pause_time = 0.0
        
    def get_current_sol(self) -> float:
        """Get the current sol (Mars day) number"""
        if self.paused:
            return self.current_sol
        
        elapsed_real_time = time.time() - self.start_time - self.pause_time
        elapsed_simulation_time = elapsed_real_time * self.time_scale
        self.current_sol = elapsed_simulation_time / self.sol_duration
        return self.current_sol
    
    def get_sol_progress(self) -> float:
        """Get progress through current sol (0.0 to 1.0)"""
        return self.get_current_sol() % 1.0
    
    def get_local_time(self) -> str:
        """Get local time in Mars colony (HH:MM format)"""
        progress = self.get_sol_progress()
        hours = int(progress * 24.65)
        minutes = int((progress * 24.65 - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    
    def pause(self):
        """Pause the simulation"""
        if not self.paused:
            self.paused = True
            self.pause_time = time.time()
    
    def resume(self):
        """Resume the simulation"""
        if self.paused:
            self.pause_time = time.time() - self.pause_time
            self.paused = False
    
    def set_time_scale(self, scale: float):
        """Change simulation speed"""
        self.time_scale = max(0.1, min(scale, 100.0))  # Limit between 0.1x and 100x


class EventGenerator:
    """Generates random events based on probabilities"""
    
    def __init__(self, event_probabilities: Dict[str, float]):
        self.probabilities = event_probabilities
        self.last_check_sol = 0.0
        
    def check_for_events(self, current_sol: float, colony_state: Dict[str, Any]) -> List[SimulationEvent]:
        """Check if any events should occur"""
        if current_sol - self.last_check_sol < 0.1:  # Check at most every 0.1 sol
            return []
        
        self.last_check_sol = current_sol
        events = []
        
        # Check each event type
        if random.random() < self.probabilities.get("solar_storm", 0.02):
            events.append(self._generate_solar_storm(current_sol))
        
        if random.random() < self.probabilities.get("equipment_failure", 0.05):
            events.append(self._generate_equipment_failure(current_sol, colony_state))
        
        if random.random() < self.probabilities.get("medical_emergency", 0.03):
            events.append(self._generate_medical_emergency(current_sol))
        
        if random.random() < self.probabilities.get("conflict", 0.04):
            events.append(self._generate_conflict(current_sol))
        
        if random.random() < self.probabilities.get("discovery", 0.01):
            events.append(self._generate_discovery(current_sol))
        
        return events
    
    def _generate_solar_storm(self, sol: float) -> SimulationEvent:
        """Generate a solar storm event"""
        severity = random.choice([EventSeverity.MEDIUM, EventSeverity.HIGH, EventSeverity.CRITICAL])
        return SimulationEvent(
            event_type=EventType.SOLAR_STORM,
            severity=severity,
            timestamp=sol,
            description=f"Solar storm detected! Severity: {severity.name}",
            affected_systems=["communications", "power", "radiation_shielding"],
            requires_human_intervention=severity in [EventSeverity.HIGH, EventSeverity.CRITICAL],
            consequences={
                "power_loss": random.uniform(10, 30) if severity == EventSeverity.MEDIUM else random.uniform(30, 60),
                "radiation_exposure": severity.value * 10
            }
        )
    
    def _generate_equipment_failure(self, sol: float, state: Dict[str, Any]) -> SimulationEvent:
        """Generate an equipment failure event"""
        systems = ["life_support", "power", "water_recycling", "air_filtration", "communications"]
        affected = random.choice(systems)
        severity = random.choice([EventSeverity.LOW, EventSeverity.MEDIUM, EventSeverity.HIGH])
        
        return SimulationEvent(
            event_type=EventType.EQUIPMENT_FAILURE,
            severity=severity,
            timestamp=sol,
            description=f"Equipment failure in {affected} system",
            affected_systems=[affected],
            requires_human_intervention=severity == EventSeverity.HIGH,
            consequences={
                "repair_time": severity.value * 2,  # hours
                "resource_cost": severity.value * 100
            }
        )
    
    def _generate_medical_emergency(self, sol: float) -> SimulationEvent:
        """Generate a medical emergency event"""
        conditions = ["injury", "illness", "psychological_crisis", "radiation_sickness"]
        condition = random.choice(conditions)
        severity = random.choice([EventSeverity.LOW, EventSeverity.MEDIUM, EventSeverity.HIGH])
        
        return SimulationEvent(
            event_type=EventType.MEDICAL_EMERGENCY,
            severity=severity,
            timestamp=sol,
            description=f"Medical emergency: {condition}",
            affected_systems=["health"],
            requires_human_intervention=severity in [EventSeverity.HIGH, EventSeverity.CRITICAL],
            consequences={
                "medical_resources_used": severity.value * 50,
                "recovery_time": severity.value * 5
            }
        )
    
    def _generate_conflict(self, sol: float) -> SimulationEvent:
        """Generate a social conflict event"""
        conflict_types = ["resource_dispute", "personal_disagreement", "policy_debate", "workspace_conflict"]
        conflict = random.choice(conflict_types)
        severity = random.choice([EventSeverity.LOW, EventSeverity.MEDIUM])
        
        return SimulationEvent(
            event_type=EventType.SOCIAL_CONFLICT,
            severity=severity,
            timestamp=sol,
            description=f"Social conflict: {conflict}",
            affected_systems=["social_cohesion"],
            requires_human_intervention=severity == EventSeverity.MEDIUM,
            consequences={
                "morale_impact": -severity.value * 5,
                "productivity_loss": severity.value * 2
            }
        )
    
    def _generate_discovery(self, sol: float) -> SimulationEvent:
        """Generate a positive discovery event"""
        discoveries = ["water_ice_deposit", "mineral_resource", "scientific_breakthrough", "efficiency_improvement"]
        discovery = random.choice(discoveries)
        
        return SimulationEvent(
            event_type=EventType.DISCOVERY,
            severity=EventSeverity.LOW,
            timestamp=sol,
            description=f"Discovery: {discovery}!",
            affected_systems=["research"],
            requires_human_intervention=False,
            consequences={
                "morale_boost": 10,
                "research_points": 50,
                "resource_bonus": discovery == "water_ice_deposit" or discovery == "mineral_resource"
            }
        )


class SimulationEngine:
    """Main simulation engine coordinating time, events, and state"""
    
    def __init__(self, config: Any):
        self.config = config
        self.clock = SimulationClock(
            time_scale=config.time_scale,
            sol_duration_hours=config.sol_duration
        )
        self.event_generator = EventGenerator(config.event_probabilities)
        self.events: List[SimulationEvent] = []
        self.state_history: List[Dict[str, Any]] = []
        self.callbacks: Dict[str, List[Callable]] = {
            "on_event": [],
            "on_sol_change": [],
            "on_state_update": []
        }
        self.running = False
        
    def register_callback(self, event_name: str, callback: Callable):
        """Register a callback function for specific events"""
        if event_name in self.callbacks:
            self.callbacks[event_name].append(callback)
    
    def trigger_callbacks(self, event_name: str, *args, **kwargs):
        """Trigger all callbacks for a specific event"""
        for callback in self.callbacks.get(event_name, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def add_event(self, event: SimulationEvent):
        """Add a new event to the simulation"""
        self.events.append(event)
        self.trigger_callbacks("on_event", event)
        logger.info(f"Sol {event.timestamp:.2f}: {event.description}")
    
    def get_active_events(self) -> List[SimulationEvent]:
        """Get all unresolved events"""
        return [e for e in self.events if not e.resolved]
    
    def resolve_event(self, event: SimulationEvent):
        """Mark an event as resolved"""
        event.resolved = True
        event.resolution_time = self.clock.get_current_sol()
        logger.info(f"Event resolved: {event.description}")
    
    def update(self, colony_state: Dict[str, Any]) -> List[SimulationEvent]:
        """Update simulation state - called each frame/tick"""
        current_sol = self.clock.get_current_sol()
        
        # Check for new events
        new_events = self.event_generator.check_for_events(current_sol, colony_state)
        for event in new_events:
            self.add_event(event)
        
        # Trigger sol change callbacks
        if int(current_sol) > int(getattr(self, '_last_sol', 0)):
            self.trigger_callbacks("on_sol_change", int(current_sol))
            self._last_sol = current_sol
        
        return new_events
    
    def save_state(self, filepath: str):
        """Save simulation state to file"""
        state = {
            "current_sol": self.clock.get_current_sol(),
            "events": [e.to_dict() for e in self.events],
            "time_scale": self.clock.time_scale
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        logger.info(f"Simulation state saved to {filepath}")
    
    def load_state(self, filepath: str):
        """Load simulation state from file"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        # Restore state (implementation depends on requirements)
        logger.info(f"Simulation state loaded from {filepath}")

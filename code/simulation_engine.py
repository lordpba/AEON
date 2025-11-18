"""
Simulation Engine for AEON GovTech Platform
Time-based event and state management for smart city simulation
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
    """Types of events that can occur in municipal simulation"""
    INFRASTRUCTURE_FAILURE = "infrastructure_failure"
    PUBLIC_COMPLAINT = "public_complaint"
    EMERGENCY_CALL = "emergency_call"
    ENVIRONMENTAL_ALERT = "environmental_alert"
    BUDGET_ISSUE = "budget_issue"
    CIVIC_EVENT = "civic_event"
    POLICY_PROPOSAL = "policy_proposal"
    SERVICE_OUTAGE = "service_outage"


class EventSeverity(Enum):
    """Severity levels for events"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class SimulationEvent:
    """Represents an event in the municipal simulation"""
    event_type: EventType
    severity: EventSeverity
    timestamp: float  # Day number
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
    
    def __init__(self, time_scale: float = 1.0, day_duration_hours: float = 24.0):
        self.time_scale = time_scale  # Multiplier for simulation speed
        self.day_duration = day_duration_hours * 3600  # Convert to seconds
        self.current_day = 0.0
        self.start_time = time.time()
        self.paused = False
        self.pause_time = 0.0
        
    def get_current_day(self) -> float:
        """Get the current day number"""
        if self.paused:
            return self.current_day
        
        elapsed_real_time = time.time() - self.start_time - self.pause_time
        elapsed_simulation_time = elapsed_real_time * self.time_scale
        self.current_day = elapsed_simulation_time / self.day_duration
        return self.current_day
    
    def get_day_progress(self) -> float:
        """Get progress through current day (0.0 to 1.0)"""
        return self.get_current_day() % 1.0
    
    def get_local_time(self) -> str:
        """Get local time (HH:MM format)"""
        progress = self.get_day_progress()
        hours = int(progress * 24.0)
        minutes = int((progress * 24.0 - hours) * 60)
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
        self.last_check_day = 0.0
        
    def check_for_events(self, current_day: float, city_state: Dict[str, Any]) -> List[SimulationEvent]:
        """Check if any events should occur"""
        if current_day - self.last_check_day < 0.1:  # Check at most every 0.1 day
            return []
        
        self.last_check_day = current_day
        events = []
        
        # Municipal event checks
        if random.random() < self.probabilities.get("infrastructure_failure", 0.03):
            events.append(self._generate_infrastructure_failure(current_day, city_state))
        if random.random() < self.probabilities.get("public_complaint", 0.15):
            events.append(self._generate_public_complaint(current_day))
        if random.random() < self.probabilities.get("emergency_call", 0.08):
            events.append(self._generate_emergency_call(current_day))
        if random.random() < self.probabilities.get("environmental_alert", 0.05):
            events.append(self._generate_environmental_alert(current_day))
        if random.random() < self.probabilities.get("budget_issue", 0.02):
            events.append(self._generate_budget_issue(current_day))
        if random.random() < self.probabilities.get("civic_event", 0.10):
            events.append(self._generate_civic_event(current_day))
        if random.random() < self.probabilities.get("policy_proposal", 0.06):
            events.append(self._generate_policy_proposal(current_day))
        
        return events

    def _generate_infrastructure_failure(self, day: float, state: Dict[str, Any]) -> SimulationEvent:
        components = [
            "roads", "bridges", "public_buildings", "street_lighting",
            "sewers", "water_pipes", "power_grid"
        ]
        affected = random.choice(components)
        severity = random.choice([EventSeverity.LOW, EventSeverity.MEDIUM, EventSeverity.HIGH])
        return SimulationEvent(
            event_type=EventType.INFRASTRUCTURE_FAILURE,
            severity=severity,
            timestamp=day,
            description=f"Infrastructure failure: {affected}",
            affected_systems=[affected],
            requires_human_intervention=severity in [EventSeverity.MEDIUM, EventSeverity.HIGH],
            consequences={
                "repair_time_hours": severity.value * 4,
                "budget_cost": severity.value * 1000
            }
        )

    def _generate_public_complaint(self, day: float) -> SimulationEvent:
        topics = ["noise", "traffic", "waste_collection", "public_transport", "street_lights"]
        topic = random.choice(topics)
        return SimulationEvent(
            event_type=EventType.PUBLIC_COMPLAINT,
            severity=EventSeverity.LOW,
            timestamp=day,
            description=f"Public complaint about {topic}",
            affected_systems=[topic],
            requires_human_intervention=False,
            consequences={"satisfaction_impact": -2}
        )

    def _generate_emergency_call(self, day: float) -> SimulationEvent:
        emergencies = ["fire", "accident", "medical", "flooding"]
        e = random.choice(emergencies)
        severity = random.choice([EventSeverity.MEDIUM, EventSeverity.HIGH])
        return SimulationEvent(
            event_type=EventType.EMERGENCY_CALL,
            severity=severity,
            timestamp=day,
            description=f"Emergency call: {e}",
            affected_systems=["public_safety"],
            requires_human_intervention=True,
            consequences={"response_time_min": 10 / severity.value}
        )

    def _generate_environmental_alert(self, day: float) -> SimulationEvent:
        alerts = ["air_quality", "heatwave", "heavy_rain", "windstorm"]
        a = random.choice(alerts)
        return SimulationEvent(
            event_type=EventType.ENVIRONMENTAL_ALERT,
            severity=EventSeverity.MEDIUM,
            timestamp=day,
            description=f"Environmental alert: {a}",
            affected_systems=["environment"],
            requires_human_intervention=False,
            consequences={"preparedness_actions": True}
        )

    def _generate_budget_issue(self, day: float) -> SimulationEvent:
        return SimulationEvent(
            event_type=EventType.BUDGET_ISSUE,
            severity=EventSeverity.MEDIUM,
            timestamp=day,
            description="Budget shortfall detected",
            affected_systems=["finance"],
            requires_human_intervention=True,
            consequences={"deficit_percent": round(random.uniform(5, 15), 1)}
        )

    def _generate_civic_event(self, day: float) -> SimulationEvent:
        events = ["community_festival", "public_meeting", "cleanup_day", "workshop"]
        e = random.choice(events)
        return SimulationEvent(
            event_type=EventType.CIVIC_EVENT,
            severity=EventSeverity.LOW,
            timestamp=day,
            description=f"Civic event: {e}",
            affected_systems=["community"],
            requires_human_intervention=False,
            consequences={"engagement_boost": 5}
        )

    def _generate_policy_proposal(self, day: float) -> SimulationEvent:
        return SimulationEvent(
            event_type=EventType.POLICY_PROPOSAL,
            severity=EventSeverity.LOW,
            timestamp=day,
            description="New policy proposal submitted",
            affected_systems=["governance"],
            requires_human_intervention=False,
            consequences={}
        )
    
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
            day_duration_hours=getattr(config, "day_duration", 24)
        )
        self.event_generator = EventGenerator(config.event_probabilities)
        self.events: List[SimulationEvent] = []
        self.state_history: List[Dict[str, Any]] = []
        self.callbacks: Dict[str, List[Callable]] = {
            "on_event": [],
            "on_day_change": [],
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
        logger.info(f"Day {event.timestamp:.2f}: {event.description}")
    
    def get_active_events(self) -> List[SimulationEvent]:
        """Get all unresolved events"""
        return [e for e in self.events if not e.resolved]
    
    def resolve_event(self, event: SimulationEvent):
        """Mark an event as resolved"""
        event.resolved = True
        event.resolution_time = self.clock.get_current_day()
        logger.info(f"Event resolved: {event.description}")
    
    def update(self, colony_state: Dict[str, Any]) -> List[SimulationEvent]:
        """Update simulation state - called each frame/tick"""
        current_day = self.clock.get_current_day()
        
        # Check for new events
        new_events = self.event_generator.check_for_events(current_day, colony_state)
        for event in new_events:
            self.add_event(event)
        
        # Trigger day change callbacks
        if int(current_day) > int(getattr(self, '_last_day', 0)):
            self.trigger_callbacks("on_day_change", int(current_day))
            self._last_day = current_day
        
        return new_events
    
    def save_state(self, filepath: str):
        """Save simulation state to file"""
        state = {
            "current_day": self.clock.get_current_day(),
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

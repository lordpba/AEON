"""
AEON GovTech Municipal Simulator
Main integration system for smart city management
"""
import threading
import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from loguru import logger

from config import CommunityConfig, DEFAULT_CONFIG
from simulation_engine import SimulationEngine, SimulationEvent, EventType
from modules.public_services import PublicServicesManagement
from modules.infrastructure import InfrastructureManagement
from modules.citizen_wellbeing import CitizenWellbeing
from modules.governance import MunicipalGovernance
from modules.admin_oversight import AdministratorOversight


@dataclass
class MunicipalState:
    """Complete state of the municipality at any given time"""
    day: float
    population: int
    public_sentiment: float  # -100 to +100
    budget_remaining: float
    service_capacity_utilization: Dict[str, float]
    infrastructure_health: float
    active_events: int
    active_proposals: int
    citizen_satisfaction: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AEONMunicipalSimulator:
    """
    Main simulator class integrating all municipal management subsystems
    """
    
    def __init__(self, config: Optional[CommunityConfig] = None):
        self.config = config or DEFAULT_CONFIG
        logger.info(f"Initializing AEON Municipality: {self.config.name}")
        
        # Initialize simulation engine
        self.engine = SimulationEngine(self.config)
        
        # Initialize all management modules
        self.public_services = PublicServicesManagement()
        self.infrastructure = InfrastructureManagement()
        self.citizen_wellbeing = CitizenWellbeing()
        self.governance = MunicipalGovernance(
            voting_threshold=self.config.proposal_threshold,
            quorum_percentage=self.config.voting_quorum * 100
        )
        self.admin_oversight = AdministratorOversight()
        
        # Simulation state
        self.running = False
        self.state_lock = threading.Lock()
        self.current_state = MunicipalState(
            day=0.0,
            population=self.config.population_size,
            public_sentiment=0.0,
            budget_remaining=self.config.annual_budget,
            service_capacity_utilization={},
            infrastructure_health=100.0,
            active_events=0,
            active_proposals=0,
            citizen_satisfaction=75.0
        )
        
        # Statistics tracking
        self.stats = {
            "total_events": 0,
            "resolved_events": 0,
            "proposals_created": 0,
            "proposals_approved": 0,
            "maintenance_performed": 0,
            "citizen_interventions": 0
        }
        
        # Module threads
        self.threads: List[threading.Thread] = []
        
        logger.success("Municipal simulator initialized successfully")
    
    def start(self):
        """Start the simulation and all subsystems"""
        if self.running:
            logger.warning("Simulator already running")
            return
        
        self.running = True
        logger.info("Starting municipal simulation...")
        
        # Provide engine with a lightweight state provider
        self.engine.set_state_provider(self._build_engine_state)

        # Start simulation engine
        self.engine.start()
        
        # Start all module threads
        threads_config = [
            ("PublicServices", self.public_services.run),
            ("Infrastructure", self.infrastructure.run),
            ("CitizenWellbeing", self.citizen_wellbeing.run),
            ("Governance", self.governance.run),
            ("AdminOversight", self.admin_oversight.run)
        ]
        
        for name, target in threads_config:
            thread = threading.Thread(target=target, name=name, daemon=True)
            thread.start()
            self.threads.append(thread)
            logger.info(f"Started {name} module")
        
        # Start main update loop
        update_thread = threading.Thread(target=self._update_loop, daemon=True)
        update_thread.start()
        self.threads.append(update_thread)
        
        logger.success("All municipal systems online")
    
    def _update_loop(self):
        """Main update loop - runs every second"""
        while self.running:
            try:
                current_day = self.engine.clock.get_current_day()
                
                # Update all modules with current time
                self.infrastructure.update(current_day)
                
                # Update simulation state
                self._update_state(current_day)
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                logger.error(f"Error in update loop: {e}")
                time.sleep(1)
    
    def _update_state(self, current_day: float):
        """Update the current state of the municipality"""
        with self.state_lock:
            self.current_state.day = current_day
            
            # Get infrastructure health
            infra_status = self.infrastructure.preventive_monitoring()
            self.current_state.infrastructure_health = infra_status.get("overall_health", 100.0)
            
            # Get citizen wellbeing
            wellbeing_status = self.citizen_wellbeing.get_status()
            self.current_state.public_sentiment = wellbeing_status.get("public_sentiment", 0.0)
            self.current_state.citizen_satisfaction = wellbeing_status.get("average_satisfaction", 75.0)
            
            # Get governance status
            governance_status = self.governance.get_governance_status()
            self.current_state.active_proposals = governance_status.get("active_proposals", 0)
            
            # Get active events
            self.current_state.active_events = len(self.engine.get_active_events())

    def _build_engine_state(self) -> Dict[str, Any]:
        """Build a compact snapshot for the engine's event generator."""
        try:
            infra = self.infrastructure.preventive_monitoring()
            services = self.public_services.get_status()
            wellbeing = self.citizen_wellbeing.get_status()
            governance = self.governance.get_governance_status()
            return {
                "infrastructure": {
                    "overall_health": infra.get("overall_health", 100.0)
                },
                "services": services,
                "wellbeing": {
                    "public_sentiment": wellbeing.get("public_sentiment", 0.0),
                    "average_satisfaction": wellbeing.get("average_satisfaction", 75.0)
                },
                "governance": {
                    "active_proposals": governance.get("active_proposals", 0)
                }
            }
        except Exception:
            return {}
    
    def get_state(self) -> Dict[str, Any]:
        """Get current simulation state"""
        with self.state_lock:
            return {
                "state": self.current_state.to_dict(),
                "stats": self.stats.copy(),
                "config": {
                    "name": self.config.name,
                    "population": self.config.population_size,
                    "governance_type": self.config.governance_type
                }
            }
    
    def get_detailed_status(self) -> Dict[str, Any]:
        """Get detailed status from all modules"""
        return {
            "time": {
                "current_day": self.engine.clock.get_current_day(),
                "time_scale": self.engine.clock.time_scale
            },
            "public_services": self.public_services.get_status(),
            "infrastructure": self.infrastructure.preventive_monitoring(),
            "citizen_wellbeing": self.citizen_wellbeing.get_status(),
            "governance": self.governance.get_governance_status(),
            "admin_oversight": self.admin_oversight.get_oversight_status(),
            "events": [event.to_dict() for event in self.engine.get_active_events()]
        }
    
    def stop(self):
        """Stop the simulation"""
        logger.info("Stopping municipal simulation...")
        self.running = False
        self.engine.stop()
        
        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2.0)
        
        logger.success("Municipal simulation stopped")
    
    def save_state(self, filepath: str):
        """Save complete simulation state to file"""
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "state": self.get_state(),
            "detailed_status": self.get_detailed_status()
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(state_data, f, indent=2)
        
        logger.info(f"State saved to {filepath}")
    
    def load_state(self, filepath: str):
        """Load simulation state from file"""
        with open(filepath, 'r') as f:
            state_data = json.load(f)
        
        # TODO: Implement state restoration
        logger.info(f"State loaded from {filepath}")
        return state_data


# Quick test function
def test_municipal_simulator():
    """Quick test of the municipal simulator"""
    logger.info("Testing AEON Municipal Simulator...")
    
    # Create simulator with default config
    simulator = AEONMunicipalSimulator()
    
    # Start simulation
    simulator.start()
    
    # Run for 10 seconds
    time.sleep(10)
    
    # Get status
    status = simulator.get_detailed_status()
    logger.info(f"Current day: {status['time']['current_day']:.2f}")
    logger.info(f"Infrastructure health: {status['infrastructure'].get('overall_health', 'N/A')}")
    logger.info(f"Citizen satisfaction: {status['citizen_wellbeing'].get('average_satisfaction', 'N/A')}")
    
    # Stop simulation
    simulator.stop()
    
    logger.success("Test completed successfully")


if __name__ == "__main__":
    test_municipal_simulator()

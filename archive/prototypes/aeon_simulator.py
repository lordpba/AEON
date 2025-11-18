"""
AEON Colony Simulator - Main Integration System
Combines all modules into a unified simulation
"""
import threading
import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from loguru import logger

from config import ColonyConfig, DEFAULT_CONFIG
from simulation_engine import SimulationEngine, SimulationEvent, EventType
from modules.resources import ResourceManagement
from modules.maintenance import MaintenanceAndRepairs
from modules.health import HealthMonitoring
from modules.policy import ConflictManagementAndPolicy
from modules.human import HumanSupervision


@dataclass
class ColonyState:
    """Complete state of the colony at any given time"""
    sol: float
    population: int
    morale: float  # 0-100
    research_points: int
    resources: Dict[str, float]
    system_health: float
    active_events: int
    critical_systems_failed: int
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AEONColonySimulator:
    """
    Main simulator class that integrates all subsystems
    and manages the colony simulation
    """
    
    def __init__(self, config: Optional[ColonyConfig] = None):
        self.config = config or DEFAULT_CONFIG
        logger.info(f"Initializing AEON Colony: {self.config.name}")
        
        # Initialize simulation engine
        self.engine = SimulationEngine(self.config)
        
        # Initialize all subsystems
        self.resources = ResourceManagement()
        self.maintenance = MaintenanceAndRepairs()
        self.health = HealthMonitoring()
        self.policy = ConflictManagementAndPolicy()
        self.human = HumanSupervision()
        
        # Colony state
        self.population = self.config.population_size
        self.morale = 75.0  # Starting morale
        self.research_points = 0
        
        # Initialize resources from config
        for resource, amount in self.config.starting_resources.items():
            if resource in self.resources.resources:
                self.resources.resources[resource] = amount
        
        # Simulation control
        self.running = False
        self.paused = False
        self.update_thread: Optional[threading.Thread] = None
        
        # Statistics and history
        self.stats_history: List[ColonyState] = []
        self.save_counter = 0
        
        # Register event callbacks
        self._register_callbacks()
        
        logger.success("AEON Colony initialized successfully")
    
    def _register_callbacks(self):
        """Register callbacks for simulation events"""
        self.engine.register_callback("on_event", self._handle_event)
        self.engine.register_callback("on_sol_change", self._handle_sol_change)
    
    def _handle_event(self, event: SimulationEvent):
        """Handle simulation events"""
        logger.info(f"Event occurred: {event.description}")
        
        # Apply event consequences
        if event.event_type == EventType.SOLAR_STORM:
            # Damage power systems
            for system in event.affected_systems:
                if system in ["power", "power_generation"]:
                    damage = event.consequences.get("power_loss", 20)
                    self.maintenance.handle_system_damage("power_generation", damage)
        
        elif event.event_type == EventType.EQUIPMENT_FAILURE:
            # Damage specific system
            if event.affected_systems:
                system = event.affected_systems[0].replace(" ", "_").lower()
                self.maintenance.handle_system_damage(system, 30)
        
        elif event.event_type == EventType.MEDICAL_EMERGENCY:
            # Affect morale and health
            self.morale = max(0, self.morale - 5)
        
        elif event.event_type == EventType.SOCIAL_CONFLICT:
            # Reduce morale
            impact = event.consequences.get("morale_impact", -5)
            self.morale = max(0, self.morale + impact)
        
        elif event.event_type == EventType.DISCOVERY:
            # Boost morale and research
            self.morale = min(100, self.morale + event.consequences.get("morale_boost", 10))
            self.research_points += event.consequences.get("research_points", 50)
    
    def _handle_sol_change(self, sol: int):
        """Handle end of sol (Mars day)"""
        logger.info(f"=== Sol {sol} Complete ===")
        
        # Consume resources based on population
        self._consume_daily_resources()
        
        # Record stats
        self._record_stats()
        
        # Auto-save periodically
        if sol % self.config.save_interval == 0:
            self.save_state(f"saves/autosave_sol_{sol}.json")
    
    def _consume_daily_resources(self):
        """Consume resources based on population needs"""
        current_sol = self.engine.clock.get_current_sol()
        
        for resource, rate in self.config.consumption_rates.items():
            if resource in self.resources.resources:
                daily_consumption = rate * self.population
                self.resources.allocate_resource(resource, daily_consumption)
                
                # Check for resource shortages
                if self.resources.resources[resource] < daily_consumption * 3:  # Less than 3 days supply
                    logger.warning(f"Resource shortage warning: {resource}")
                    self.morale = max(0, self.morale - 2)
                
                if self.resources.resources[resource] <= 0:
                    logger.error(f"CRITICAL: {resource} depleted!")
                    self.morale = max(0, self.morale - 10)
    
    def _record_stats(self):
        """Record current state for statistics"""
        state = ColonyState(
            sol=self.engine.clock.get_current_sol(),
            population=self.population,
            morale=self.morale,
            research_points=self.research_points,
            resources=dict(self.resources.resources),
            system_health=self.maintenance._calculate_overall_health(),
            active_events=len(self.engine.get_active_events()),
            critical_systems_failed=sum(
                1 for s in self.maintenance.systems.values() 
                if s.critical and s.health < 30
            )
        )
        self.stats_history.append(state)
    
    def start(self):
        """Start the simulation"""
        if self.running:
            logger.warning("Simulation already running")
            return
        
        self.running = True
        self.engine.running = True
        
        logger.info("Starting AEON Colony Simulation...")
        
        # Start subsystem threads
        threads = [
            threading.Thread(target=self.resources.run, daemon=True),
            threading.Thread(target=self.maintenance.run, daemon=True),
            threading.Thread(target=self.health.run, daemon=True),
            threading.Thread(target=self.policy.run, daemon=True),
        ]
        
        for thread in threads:
            thread.start()
        
        # Start main update loop
        self.update_thread = threading.Thread(target=self._main_loop, daemon=True)
        self.update_thread.start()
        
        logger.success("Simulation started!")
    
    def _main_loop(self):
        """Main simulation update loop"""
        while self.running:
            if not self.paused:
                current_sol = self.engine.clock.get_current_sol()
                
                # Update maintenance systems
                self.maintenance.update(current_sol)
                
                # Get colony state for event generation
                colony_state = self.get_current_state()
                
                # Update simulation engine (checks for events, etc.)
                self.engine.update(colony_state)
                
                # Small delay to control update rate
                time.sleep(0.1)
            else:
                time.sleep(0.5)
    
    def pause(self):
        """Pause the simulation"""
        self.paused = True
        self.engine.clock.pause()
        logger.info("Simulation paused")
    
    def resume(self):
        """Resume the simulation"""
        self.paused = False
        self.engine.clock.resume()
        logger.info("Simulation resumed")
    
    def stop(self):
        """Stop the simulation"""
        self.running = False
        self.engine.running = False
        logger.info("Simulation stopped")
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get complete current state of the colony"""
        return {
            "sol": self.engine.clock.get_current_sol(),
            "local_time": self.engine.clock.get_local_time(),
            "population": self.population,
            "morale": self.morale,
            "research_points": self.research_points,
            "resources": dict(self.resources.resources),
            "resource_forecast": self.resources.forecast_needs(),
            "system_health": self.maintenance.preventive_monitoring(),
            "maintenance_queue": self.maintenance.get_maintenance_queue(),
            "active_events": [e.to_dict() for e in self.engine.get_active_events()],
            "health_overview": {
                "population_count": len(self.health.get_population()),
                "average_stress": sum(
                    self.health.health_data.get(p, {}).get('stress_level', 0) 
                    for p in self.health.get_population()
                ) / max(1, len(self.health.get_population()))
            },
            "conflicts": {
                "active": len(self.policy.conflicts),
                "total_policies": len(self.policy.policies)
            }
        }
    
    def get_summary(self) -> str:
        """Get a human-readable summary of colony status"""
        state = self.get_current_state()
        
        summary = f"""
╔══════════════════════════════════════════════════════════╗
║         AEON COLONY STATUS - {self.config.name}
╠══════════════════════════════════════════════════════════╣
║ Sol: {state['sol']:.2f} | Time: {state['local_time']}
║ Population: {state['population']} | Morale: {state['morale']:.1f}%
║ Research Points: {state['research_points']}
╠══════════════════════════════════════════════════════════╣
║ RESOURCES:
"""
        for resource, amount in state['resources'].items():
            summary += f"║   {resource.capitalize()}: {amount:.1f}\n"
        
        summary += f"""╠══════════════════════════════════════════════════════════╣
║ SYSTEMS HEALTH: {state['system_health']['overall_health']:.1f}%
║ Maintenance Queue: {len(state['maintenance_queue'])} items
║ Active Events: {len(state['active_events'])}
║ Active Conflicts: {state['conflicts']['active']}
╚══════════════════════════════════════════════════════════╝
        """
        return summary
    
    def save_state(self, filepath: str):
        """Save complete simulation state"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "name": self.config.name,
                "population_size": self.config.population_size,
                "time_scale": self.config.time_scale
            },
            "current_state": self.get_current_state(),
            "stats_history": [s.to_dict() for s in self.stats_history[-100:]]  # Last 100 records
        }
        
        with open(filepath, 'w') as f:
            json.dump(state_data, f, indent=2)
        
        logger.success(f"State saved to {filepath}")
    
    def set_time_scale(self, scale: float):
        """Change simulation speed"""
        self.engine.clock.set_time_scale(scale)
        logger.info(f"Time scale set to {scale}x")


def main():
    """Main entry point for the simulation"""
    # Configure logging
    logger.add("logs/aeon_{time}.log", rotation="1 day", retention="7 days")
    
    # Create and start simulation
    simulator = AEONColonySimulator()
    simulator.start()
    
    # Keep running and print status periodically
    try:
        while True:
            time.sleep(30)  # Print status every 30 seconds
            print("\n" + simulator.get_summary())
            
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
        simulator.save_state("saves/manual_save.json")
        simulator.stop()
        logger.info("Simulation ended")


if __name__ == "__main__":
    main()

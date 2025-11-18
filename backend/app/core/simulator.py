"""
Simulator manager for the backend
Wraps the municipal simulator for API access
"""
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

# Add code directory to path
CODE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "code"
sys.path.insert(0, str(CODE_DIR))

from municipal_simulator import AEONMunicipalSimulator
from config import CommunityConfig, COMMUNITY_TEMPLATES


class SimulatorManager:
    """Manages the municipal simulator instance"""
    
    def __init__(self):
        self.simulator: Optional[AEONMunicipalSimulator] = None
        self.initialized = False
    
    def start(self, template: str = "small_town"):
        """Start the simulator with a specific template"""
        if self.initialized:
            logger.warning("Simulator already running")
            return
        
        try:
            # Load configuration template
            if template in COMMUNITY_TEMPLATES:
                config = COMMUNITY_TEMPLATES[template]
            else:
                config = CommunityConfig()
            
            # Increase time scale for demo
            config.time_scale = 10.0
            
            # Create and start simulator
            self.simulator = AEONMunicipalSimulator(config)
            self.simulator.start()
            
            self.initialized = True
            logger.success(f"Simulator started with template: {template}")
            
        except Exception as e:
            logger.error(f"Failed to start simulator: {e}")
            raise
    
    def stop(self):
        """Stop the simulator"""
        if self.simulator and self.initialized:
            self.simulator.stop()
            self.initialized = False
            logger.info("Simulator stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current simulator status"""
        if not self.simulator or not self.initialized:
            return {"error": "Simulator not running"}
        
        try:
            return self.simulator.get_state()
        except Exception as e:
            logger.error(f"Error getting simulator status: {e}")
            return {"error": str(e)}
    
    def get_detailed_status(self) -> Dict[str, Any]:
        """Get detailed status from all modules"""
        if not self.simulator or not self.initialized:
            return {"error": "Simulator not running"}
        
        try:
            return self.simulator.get_detailed_status()
        except Exception as e:
            logger.error(f"Error getting detailed status: {e}")
            return {"error": str(e)}
    
    def get_module(self, module_name: str):
        """Get direct access to a specific module"""
        if not self.simulator or not self.initialized:
            return None
        
        modules = {
            "public_services": self.simulator.public_services,
            "infrastructure": self.simulator.infrastructure,
            "citizen_wellbeing": self.simulator.citizen_wellbeing,
            "governance": self.simulator.governance,
            "admin_oversight": self.simulator.admin_oversight
        }
        
        return modules.get(module_name)


# Global simulator instance
simulator_manager = SimulatorManager()

"""Municipal Administrator Oversight Module
Provides human oversight and control over autonomous municipal systems
"""
from typing import Dict, Any, List
import time
import threading
from loguru import logger

class AdministratorOversight:
    def __init__(self):
        self.lock = threading.Lock()
        self.manual_interventions: List[Dict[str, Any]] = []
        self.active_overrides: Dict[str, Any] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.oversight_mode = "monitoring"  # monitoring, intervening, emergency

    def run(self):
        """Provide continuous administrator oversight."""
        while True:
            self.check_for_alerts()
            self.review_active_overrides()
            time.sleep(60)  # Check every minute

    def create_alert(self, severity: str, message: str, source: str):
        """Create an alert for administrator attention."""
        with self.lock:
            alert = {
                "timestamp": time.time(),
                "severity": severity,  # info, warning, critical
                "message": message,
                "source": source,
                "acknowledged": False
            }
            self.alerts.append(alert)
            logger.warning(f"ADMIN ALERT [{severity}] from {source}: {message}")
    
    def acknowledge_alert(self, alert_index: int):
        """Acknowledge an alert."""
        with self.lock:
            if 0 <= alert_index < len(self.alerts):
                self.alerts[alert_index]["acknowledged"] = True
                logger.info(f"Alert {alert_index} acknowledged")

    def apply_override(self, subsystem: str, parameter: str, value: Any, reason: str) -> bool:
        """
        Apply manual override to a subsystem parameter.
        
        Args:
            subsystem: Which system to override (public_services, infrastructure, etc.)
            parameter: Specific parameter to modify
            value: New value to set
            reason: Justification for override
        
        Returns:
            bool: True if override was applied
        """
        with self.lock:
            override_id = f"OVR-{len(self.manual_interventions) + 1:04d}"
            
            override_data = {
                "id": override_id,
                "subsystem": subsystem,
                "parameter": parameter,
                "value": value,
                "reason": reason,
                "timestamp": time.time()
            }
            
            self.active_overrides[override_id] = override_data
            self.manual_interventions.append(override_data)
            
            logger.warning(f"Manual override applied: {subsystem}.{parameter} = {value} (reason: {reason})")
            return True

    def remove_override(self, override_id: str):
        """Remove a manual override."""
        with self.lock:
            if override_id in self.active_overrides:
                override = self.active_overrides.pop(override_id)
                logger.info(f"Override removed: {override_id} - {override['subsystem']}.{override['parameter']}")
                return True
            return False
    
    def check_for_alerts(self):
        """Check for conditions requiring administrator attention."""
        with self.lock:
            unacknowledged = [a for a in self.alerts if not a["acknowledged"]]
            if unacknowledged:
                logger.debug(f"{len(unacknowledged)} unacknowledged alerts pending")
    
    def review_active_overrides(self):
        """Review and log active overrides."""
        with self.lock:
            if self.active_overrides:
                logger.debug(f"{len(self.active_overrides)} manual overrides active")

    def get_oversight_status(self) -> Dict[str, Any]:
        """Get current oversight status."""
        with self.lock:
            return {
                "mode": self.oversight_mode,
                "active_overrides": len(self.active_overrides),
                "total_interventions": len(self.manual_interventions),
                "pending_alerts": len([a for a in self.alerts if not a["acknowledged"]]),
                "recent_overrides": list(self.active_overrides.values())[-5:]
            }
    
    def emergency_shutdown(self, reason: str):
        """Initiate emergency shutdown of all systems."""
        with self.lock:
            self.oversight_mode = "emergency"
            logger.critical(f"EMERGENCY SHUTDOWN initiated: {reason}")
            self.create_alert("critical", f"Emergency shutdown: {reason}", "admin_oversight")
            return True
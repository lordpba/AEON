"""Infrastructure Management Module
Manages municipal infrastructure: roads, bridges, buildings, utilities
"""
import threading
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger


class InfrastructureStatus(Enum):
    OPTIMAL = "optimal"
    GOOD = "good"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    FAILED = "failed"


@dataclass
class InfrastructureComponent:
    name: str
    health: float = 100.0
    status: InfrastructureStatus = InfrastructureStatus.OPTIMAL
    last_maintenance: float = 0.0  # day number
    degradation_rate: float = 0.1  # per day
    failure_threshold: float = 30.0
    maintenance_cost: float = 100.0
    critical: bool = False

    def update_health(self, delta_days: float):
        self.health = max(0, self.health - (self.degradation_rate * delta_days))
        self._update_status()

    def _update_status(self):
        if self.health >= 90:
            self.status = InfrastructureStatus.OPTIMAL
        elif self.health >= 70:
            self.status = InfrastructureStatus.GOOD
        elif self.health >= 50:
            self.status = InfrastructureStatus.DEGRADED
        elif self.health >= self.failure_threshold:
            self.status = InfrastructureStatus.CRITICAL
        else:
            self.status = InfrastructureStatus.FAILED

    def perform_maintenance(self, current_day: float) -> bool:
        if self.status == InfrastructureStatus.FAILED:
            self.health = min(100, self.health + 30)
        else:
            self.health = min(100, self.health + 50)
        self.last_maintenance = current_day
        self._update_status()
        return True

    def apply_damage(self, damage: float):
        self.health = max(0, self.health - damage)
        self._update_status()


class InfrastructureManagement:
    def __init__(self):
        self.infrastructure = {
            "roads": InfrastructureComponent(name="Road Network", degradation_rate=0.05, critical=True),
            "bridges": InfrastructureComponent(name="Bridges & Overpasses", degradation_rate=0.03, critical=True),
            "public_buildings": InfrastructureComponent(name="Public Buildings", degradation_rate=0.04, critical=False),
            "street_lighting": InfrastructureComponent(name="Street Lighting", degradation_rate=0.08, critical=False),
            "parks": InfrastructureComponent(name="Parks & Green Spaces", degradation_rate=0.06, critical=False),
            "sewers": InfrastructureComponent(name="Sewer System", degradation_rate=0.04, critical=True),
            "water_pipes": InfrastructureComponent(name="Water Distribution", degradation_rate=0.05, critical=True),
            "power_grid": InfrastructureComponent(name="Electrical Grid", degradation_rate=0.03, critical=True),
        }

        self.lock = threading.Lock()
        self.maintenance_queue: List[str] = []
        self.anomalies: List[Dict[str, Any]] = []
        self.last_update_day = 0.0
        self.maintenance_in_progress: Optional[str] = None

    def run(self):
        while True:
            self.preventive_monitoring()
            self.diagnose_anomalies()
            self.plan_maintenance()
            time.sleep(10)

    def update(self, current_day: float):
        with self.lock:
            delta_days = current_day - self.last_update_day
            if delta_days > 0:
                for component in self.infrastructure.values():
                    component.update_health(delta_days)
                self.last_update_day = current_day

    def preventive_monitoring(self) -> Dict[str, Any]:
        with self.lock:
            status_report: Dict[str, Any] = {
                "overall_health": self._calculate_overall_health(),
                "systems": {},
            }
            for key, system in self.infrastructure.items():
                status_report["systems"][key] = {
                    "name": system.name,
                    "health": system.health,
                    "status": system.status.value,
                    "critical": system.critical,
                }
            for key, system in self.infrastructure.items():
                if system.health < 70 and key not in self.maintenance_queue:
                    self.maintenance_queue.append(key)
                    logger.warning(
                        f"System {system.name} added to maintenance queue (health: {system.health:.1f}%)"
                    )
            return status_report

    def _calculate_overall_health(self) -> float:
        if not self.infrastructure:
            return 0.0
        total_weight = 0.0
        weighted_health = 0.0
        for system in self.infrastructure.values():
            weight = 2.0 if system.critical else 1.0
            weighted_health += system.health * weight
            total_weight += weight
        return weighted_health / total_weight if total_weight > 0 else 0.0

    def diagnose_anomalies(self) -> List[Dict[str, Any]]:
        with self.lock:
            self.anomalies = []
            for key, component in self.infrastructure.items():
                if component.status == InfrastructureStatus.CRITICAL:
                    self.anomalies.append({
                        "component": key,
                        "type": "critical_health",
                        "severity": "high",
                        "message": f"{component.name} is in critical condition ({component.health:.1f}%)",
                    })
                elif component.status == InfrastructureStatus.FAILED:
                    self.anomalies.append({
                        "component": key,
                        "type": "infrastructure_failure",
                        "severity": "critical",
                        "message": f"{component.name} has FAILED! Immediate action required!",
                    })
                elif component.status == InfrastructureStatus.DEGRADED and component.critical:
                    self.anomalies.append({
                        "component": key,
                        "type": "degradation",
                        "severity": "medium",
                        "message": f"Critical infrastructure {component.name} is degraded ({component.health:.1f}%)",
                    })
            return self.anomalies

    def plan_maintenance(self) -> Optional[str]:
        with self.lock:
            if not self.maintenance_queue:
                return None
            priority_queue = sorted(
                self.maintenance_queue,
                key=lambda k: (not self.infrastructure[k].critical, self.infrastructure[k].health),
            )
            if priority_queue:
                next_maintenance = priority_queue[0]
                system = self.infrastructure[next_maintenance]
                logger.info(
                    f"Next maintenance scheduled: {system.name} (health: {system.health:.1f}%)"
                )
                return next_maintenance
            return None

    def perform_maintenance(self, component_key: str, current_day: float) -> bool:
        with self.lock:
            if component_key not in self.infrastructure:
                logger.error(f"System {component_key} not found")
                return False
            system = self.infrastructure[component_key]
            success = system.perform_maintenance(current_day)
            if success and component_key in self.maintenance_queue:
                self.maintenance_queue.remove(component_key)
            return success

    def handle_system_damage(self, component_key: str, damage: float):
        with self.lock:
            if component_key in self.infrastructure:
                self.infrastructure[component_key].apply_damage(damage)
                logger.warning(
                    f"System {self.infrastructure[component_key].name} damaged: -{damage:.1f}% health"
                )

    def get_system_status(self, component_key: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            if component_key not in self.infrastructure:
                return None
            system = self.infrastructure[component_key]
            return {
                "name": system.name,
                "health": system.health,
                "status": system.status.value,
                "last_maintenance": system.last_maintenance,
                "degradation_rate": system.degradation_rate,
                "critical": system.critical,
                "in_queue": component_key in self.maintenance_queue,
            }

    def get_maintenance_queue(self) -> List[Dict[str, Any]]:
        with self.lock:
            queue_info = []
            for component_key in self.maintenance_queue:
                system = self.infrastructure[component_key]
                queue_info.append({
                    "key": component_key,
                    "name": system.name,
                    "health": system.health,
                    "critical": system.critical,
                    "status": system.status.value,
                })
            return queue_info

    def emergency_repair(self, component_key: str, current_day: float) -> bool:
        with self.lock:
            if component_key not in self.infrastructure:
                return False
            system = self.infrastructure[component_key]
            system.health = min(100, system.health + 70)
            system.last_maintenance = current_day
            system._update_status()
            logger.warning(
                f"EMERGENCY REPAIR: {system.name} restored to {system.health:.1f}%"
            )
            if component_key in self.maintenance_queue:
                self.maintenance_queue.remove(component_key)
            return True
            system._update_status()
            
            logger.warning(f"EMERGENCY REPAIR: {system.name} restored to {system.health:.1f}%")
            
            if component_key in self.maintenance_queue:
                self.maintenance_queue.remove(component_key)
            
>>>>>>> 334d9b9 (Implement municipal governance, infrastructure management, public services, and simulation modules):code/modules/infrastructure.py
            return True

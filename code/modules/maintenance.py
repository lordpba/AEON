"""Maintenance and repairs module for AEON.

This module provides a SystemComponent dataclass and a MaintenanceAndRepairs
manager that tracks systems, schedules maintenance and identifies anomalies.
"""

import threading
import time
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger


class SystemStatus(Enum):
    """Status levels for colony systems"""
    OPTIMAL = "optimal"
    GOOD = "good"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    FAILED = "failed"


@dataclass
class SystemComponent:
    """Represents a component in the colony infrastructure"""
    name: str
    health: float = 100.0  # 0-100%
    status: SystemStatus = SystemStatus.OPTIMAL
    last_maintenance: float = 0.0  # sol number
    degradation_rate: float = 0.1  # per sol
    failure_threshold: float = 30.0
    maintenance_cost: float = 100.0
    critical: bool = False  # If true, failure is catastrophic

    def update_health(self, delta_sols: float):
        """Update component health based on time passed"""
        self.health = max(0, self.health - (self.degradation_rate * delta_sols))
        self._update_status()

    def _update_status(self):
        """Update status based on health"""
        if self.health >= 90:
            self.status = SystemStatus.OPTIMAL
        elif self.health >= 70:
            self.status = SystemStatus.GOOD
        elif self.health >= 50:
            self.status = SystemStatus.DEGRADED
        elif self.health >= self.failure_threshold:
            self.status = SystemStatus.CRITICAL
        else:
            self.status = SystemStatus.FAILED

    def perform_maintenance(self, current_sol: float) -> bool:
        """Perform maintenance on the component"""
        if self.status == SystemStatus.FAILED:
            # Failed components require more extensive repair
            self.health = min(100, self.health + 30)
        else:
            self.health = min(100, self.health + 50)

        self.last_maintenance = current_sol
        self._update_status()
        return True

    def apply_damage(self, damage: float):
        """Apply damage to component (from events)"""
        self.health = max(0, self.health - damage)
        self._update_status()


class MaintenanceAndRepairs:
    """Manager for maintenance operations across colony systems."""

    def __init__(self):
        # Initialize all colony systems
        self.systems: Dict[str, SystemComponent] = {
            "life_support": SystemComponent(
                name="Life Support System",
                degradation_rate=0.05,
                critical=True,
            ),
            "power_generation": SystemComponent(
                name="Power Generation",
                degradation_rate=0.08,
                critical=True,
            ),
            "power_storage": SystemComponent(
                name="Power Storage",
                degradation_rate=0.06,
                critical=False,
            ),
            "water_recycling": SystemComponent(
                name="Water Recycling System",
                degradation_rate=0.07,
                critical=True,
            ),
            "air_filtration": SystemComponent(
                name="Air Filtration",
                degradation_rate=0.06,
                critical=True,
            ),
            "communications": SystemComponent(
                name="Communications Array",
                degradation_rate=0.04,
                critical=False,
            ),
            "habitat_structure": SystemComponent(
                name="Habitat Structure",
                degradation_rate=0.02,
                critical=True,
            ),
            "heating_cooling": SystemComponent(
                name="Temperature Control",
                degradation_rate=0.05,
                critical=True,
            ),
            "waste_management": SystemComponent(
                name="Waste Management",
                degradation_rate=0.06,
                critical=False,
            ),
            "food_production": SystemComponent(
                name="Food Production",
                degradation_rate=0.05,
                critical=False,
            ),
        }

        self.lock = threading.Lock()
        self.maintenance_queue: List[str] = []
        self.anomalies: List[Dict[str, Any]] = []
        self.last_update_sol = 0.0
        self.maintenance_in_progress: Optional[str] = None

    def run(self):
        """Main maintenance loop"""
        while True:
            self.preventive_monitoring()
            self.diagnose_anomalies()
            self.plan_maintenance()
            time.sleep(10)  # Check every 10 seconds

    def update(self, current_sol: float):
        """Update all systems based on elapsed time"""
        with self.lock:
            delta_sols = current_sol - self.last_update_sol
            if delta_sols > 0:
                for system in self.systems.values():
                    system.update_health(delta_sols)
                self.last_update_sol = current_sol

    def preventive_monitoring(self) -> Dict[str, Any]:
        """Monitor all systems and return status report"""
        with self.lock:
            status_report: Dict[str, Any] = {
                "overall_health": self._calculate_overall_health(),
                "systems": {},
            }

            for key, system in self.systems.items():
                status_report["systems"][key] = {
                    "name": system.name,
                    "health": system.health,
                    "status": system.status.value,
                    "critical": system.critical,
                }

            # Check for systems needing maintenance
            for key, system in self.systems.items():
                if system.health < 70 and key not in self.maintenance_queue:
                    self.maintenance_queue.append(key)
                    logger.warning(f"System {system.name} added to maintenance queue (health: {system.health:.1f}%)")

            return status_report

    def _calculate_overall_health(self) -> float:
        """Calculate overall colony infrastructure health"""
        if not self.systems:
            return 0.0

        total_weight = 0.0
        weighted_health = 0.0

        for system in self.systems.values():
            weight = 2.0 if system.critical else 1.0
            weighted_health += system.health * weight
            total_weight += weight

        return weighted_health / total_weight if total_weight > 0 else 0.0

    def diagnose_anomalies(self) -> List[Dict[str, Any]]:
        """Identify anomalies and potential issues"""
        with self.lock:
            self.anomalies = []

            for key, system in self.systems.items():
                if system.status == SystemStatus.CRITICAL:
                    self.anomalies.append({
                        "system": key,
                        "type": "critical_health",
                        "severity": "high",
                        "message": f"{system.name} is in critical condition ({system.health:.1f}%)",
                    })
                elif system.status == SystemStatus.FAILED:
                    self.anomalies.append({
                        "system": key,
                        "type": "system_failure",
                        "severity": "critical",
                        "message": f"{system.name} has FAILED! Immediate action required!",
                    })
                elif system.status == SystemStatus.DEGRADED and system.critical:
                    self.anomalies.append({
                        "system": key,
                        "type": "degradation",
                        "severity": "medium",
                        "message": f"Critical system {system.name} is degraded ({system.health:.1f}%)",
                    })

            return self.anomalies

    def plan_maintenance(self) -> Optional[str]:
        """Plan and prioritize maintenance tasks"""
        with self.lock:
            if not self.maintenance_queue:
                return None

            priority_queue = sorted(
                self.maintenance_queue,
                key=lambda k: (
                    not self.systems[k].critical,
                    self.systems[k].health,
                ),
            )

            if priority_queue:
                next_maintenance = priority_queue[0]
                system = self.systems[next_maintenance]
                logger.info(f"Next maintenance scheduled: {system.name} (health: {system.health:.1f}%)")
                return next_maintenance

            return None

    def perform_maintenance(self, system_key: str, current_sol: float) -> bool:
        """Execute maintenance on a specific system"""
        with self.lock:
            if system_key not in self.systems:
                logger.error(f"System {system_key} not found")
                return False

            system = self.systems[system_key]
            success = system.perform_maintenance(current_sol)

            if success:
                logger.info(f"Maintenance completed on {system.name}. New health: {system.health:.1f}%")
                if system_key in self.maintenance_queue:
                    self.maintenance_queue.remove(system_key)

            return success

    def handle_system_damage(self, system_key: str, damage: float):
        """Apply damage to a system (from events like solar storms)"""
        with self.lock:
            if system_key in self.systems:
                self.systems[system_key].apply_damage(damage)
                logger.warning(f"System {self.systems[system_key].name} damaged: -{damage:.1f}% health")

    def get_system_status(self, system_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a specific system"""
        with self.lock:
            if system_key not in self.systems:
                return None

            system = self.systems[system_key]
            return {
                "name": system.name,
                "health": system.health,
                "status": system.status.value,
                "last_maintenance": system.last_maintenance,
                "degradation_rate": system.degradation_rate,
                "critical": system.critical,
                "in_queue": system_key in self.maintenance_queue,
            }

    def get_maintenance_queue(self) -> List[Dict[str, Any]]:
        """Get the current maintenance queue"""
        with self.lock:
            queue_info = []
            for system_key in self.maintenance_queue:
                system = self.systems[system_key]
                queue_info.append({
                    "key": system_key,
                    "name": system.name,
                    "health": system.health,
                    "critical": system.critical,
                    "status": system.status.value,
                })
            return queue_info

    def emergency_repair(self, system_key: str, current_sol: float) -> bool:
        """Perform emergency repair with higher resource cost"""
        with self.lock:
            if system_key not in self.systems:
                return False

            system = self.systems[system_key]
            # Emergency repairs restore more health
            system.health = min(100, system.health + 70)
            system.last_maintenance = current_sol
            system._update_status()

            logger.warning(f"EMERGENCY REPAIR: {system.name} restored to {system.health:.1f}%")

            if system_key in self.maintenance_queue:
                self.maintenance_queue.remove(system_key)

            return True

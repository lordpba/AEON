from typing import List, Dict, Any
import random  # For simulation purposes
from loguru import logger
import time

# Simple event throttling: keep last emit timestamps per event key
_last_emit: Dict[str, float] = {}
_THROTTLE_SECONDS = 1.0  # default cooldown per event key in seconds


def _allow_emit(key: str, cooldown: float = _THROTTLE_SECONDS) -> bool:
    now = time.time()
    last = _last_emit.get(key, 0.0)
    if now - last >= cooldown:
        _last_emit[key] = now
        return True
    return False


class ConflictManagementAndPolicy:
    def __init__(self):
        self.conflicts = []  # List to store ongoing conflicts
        self.policies = {}   # Dictionary to store current policies
        self.participation_records = []  # List to record democratic participation
        # Genera alcune policy standard all'avvio
        try:
            from .llm_interface import generate_policy
            standard_data = [
                {"morale": 80, "resources": {"water": 9000, "food": 4000, "energy": 45000}, "conflicts": 0, "population": 5},
                {"morale": 70, "resources": {"water": 7000, "food": 3000, "energy": 30000}, "conflicts": 1, "population": 5},
                {"morale": 60, "resources": {"water": 5000, "food": 2000, "energy": 20000}, "conflicts": 2, "population": 5}
            ]
            for i, data in enumerate(standard_data, 1):
                llm_policy = generate_policy(data)
                descrizione = llm_policy['descrizione']
                self.policies[f"policy_{i}"] = descrizione
        except Exception as e:
            self.policies["policy_1"] = "Standard policy: errore generazione LLM."

    def run(self):
        """Continuously manage conflicts and update policies based on democratic input."""
        while True:
            self.detect_conflicts()
            self.resolve_conflicts()
            self.update_policies()
            self.democratic_participation()

    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """Detect new conflicts within the community."""
        # In a real system, this might involve monitoring social media, forums, or direct reports
        new_conflicts = [
            {"id": f"conflict_{len(self.conflicts) + i}", "description": f"New conflict about {random.choice(['resource allocation', 'noise', 'space', 'policy'])}"}
            for i in range(random.randint(0, 3))  # Simulating 0 to 3 new conflicts each cycle
        ]
        self.conflicts.extend(new_conflicts)
        return new_conflicts

    def resolve_conflicts(self):
        """Attempt to resolve reported conflicts."""
        for conflict in self.conflicts[:]:  # Iterate over a copy to safely remove items
            if random.random() < 0.7:  # 70% chance of resolution for simulation
                self.conflicts.remove(conflict)
                if _allow_emit('conflict_resolved'):
                    logger.info(f"Conflict resolved: {conflict['description']}")

    def political_decision_making(self) -> str:
        """Simulate political decision making process."""
        # Here you could implement a more complex decision-making algorithm
        decision = random.choice(["New Policy", "Policy Revision", "Policy Rejected"])
        return decision

    def update_policies(self):
        """Update policies based on the current situation or community feedback."""
        from .llm_interface import generate_policy
        decision = self.political_decision_making()
        if decision == "New Policy":
            # Prepara dati sintetici della colonia (puoi migliorare)
            colony_data = {
                "morale": random.randint(60, 90),
                "resources": {"water": random.randint(5000, 10000), "food": random.randint(2000, 5000), "energy": random.randint(20000, 50000)},
                "conflicts": len(self.conflicts),
                "population": 5
            }
            llm_policy = generate_policy(colony_data)
            descrizione = llm_policy['descrizione']
            self.policies[f"policy_{len(self.policies) + 1}"] = descrizione
        elif decision == "Policy Revision":
            if self.policies:
                policy_to_revise = random.choice(list(self.policies.keys()))
                self.policies[policy_to_revise] = "Policy revised."
        elif decision == "Policy Rejected" and random.random() < 0.15:
            if self.policies:
                policy_to_remove = random.choice(list(self.policies.keys()))
                del self.policies[policy_to_remove]
                if _allow_emit('policy_removed'):
                    logger.info(f"Policy removed: {policy_to_remove} (obsolete)")
        if _allow_emit('policy_update'):
            logger.info(f"Policy update: {decision}")

    def democratic_participation(self) -> int:
        """Facilitate democratic participation and record it."""
        participants = random.randint(0, 20)  # Random number of participants for simulation
        self.participation_records.append({"date": "Today", "participants": participants})
        return participants

    def get_conflict_status(self) -> Dict[str, Any]:
        """Retrieve the status of conflicts."""
        return {"active_conflicts": len(self.conflicts), "total_resolved": len(self.conflicts)}

    def get_policy_overview(self) -> Dict[str, Any]:
        """Get an overview of current policies."""
        return self.policies

    def get_participation_stats(self) -> List[Dict[str, Any]]:
        """Get statistics on democratic participation."""
        return self.participation_records

from typing import Dict, Any
import time
import random
from loguru import logger

_last_emit_human: Dict[str, float] = {}
_HUMAN_THROTTLE = 2.0  # seconds between log emits for human module


def _allow_emit_human(key: str, cooldown: float = _HUMAN_THROTTLE) -> bool:
    now = time.time()
    last = _last_emit_human.get(key, 0.0)
    if now - last >= cooldown:
        _last_emit_human[key] = now
        return True
    return False


class HumanSupervision:
    def __init__(self):
        self.current_overrides = {}  # Dictionary to store active overrides
        self.user_interface_active = False  # Flag to indicate if UI is currently in use

    def run(self):
        """Provide continuous human oversight capability."""
        while True:
            self.monitor_for_intervention()
            time.sleep(60)  # Check for intervention requests every minute

    def user_interface(self):
        """Activate the user interface for human supervisors."""
        self.user_interface_active = True
        if _allow_emit_human('ui_activate'):
            logger.info("User Interface Activated. Awaiting commands...")
        while self.user_interface_active:
            try:
                command = input("Enter command (override, deactivate, exit): ").strip().lower()
            except EOFError:
                # Non-interactive environment: exit gracefully
                self.user_interface_active = False
                return
            if command == "override":
                self.override_mechanisms()
            elif command == "deactivate":
                self.user_interface_active = False
            elif command == "exit":
                self.user_interface_active = False
                return
            else:
                if _allow_emit_human('invalid_command'):
                    logger.warning("Invalid command. Please try again.")

    def override_mechanisms(self) -> bool:
        """
        Implement override mechanisms allowing humans to take control of autonomous systems.
        
        Returns:
            bool: True if an override was initiated, False otherwise.
        """
        try:
            override_request = input("Enter subsystem to override or 'cancel' to abort: ")
        except EOFError:
            return False
        if override_request.lower() == 'cancel':
            return False
        elif override_request.lower() in ['resource', 'maintenance', 'health', 'conflict']:
            try:
                action = input(f"Enter action for {override_request}: ")
            except EOFError:
                return False
            self.current_overrides[override_request] = action
            if _allow_emit_human('override_applied'):
                logger.info(f"Override applied: {override_request} - {action}")
            return True
        else:
            if _allow_emit_human('override_invalid'):
                logger.warning("Invalid subsystem or action. Override not applied.")
            return False

    def monitor_for_intervention(self):
        """Check for conditions or signals indicating a need for human intervention."""
        # This method would typically interface with other systems to detect issues
        # For simulation, we'll just check if there's a need based on a random event
        if random.random() < 0.05:  # 5% chance of needing human intervention each cycle
            if _allow_emit_human('intervention_alert'):
                logger.warning("Alert: Human intervention required. Activating User Interface.")
            self.user_interface()

    def check_active_overrides(self) -> Dict[str, str]:
        """Return the current active overrides."""
        return self.current_overrides

    def cancel_override(self, subsystem: str):
        """Cancel an active override for a specific subsystem."""
        if subsystem in self.current_overrides:
            del self.current_overrides[subsystem]
            if _allow_emit_human('override_cancelled'):
                logger.info(f"Override for {subsystem} cancelled.")
        else:
            if _allow_emit_human('override_none'):
                logger.info(f"No active override for {subsystem} to cancel.")

    def emergency_stop(self):
        """Implement an emergency stop function."""
        if _allow_emit_human('emergency_stop'):
            logger.critical("Emergency stop initiated. All systems are being powered down.")
        # In reality, this would interface with all other systems to halt operations safely

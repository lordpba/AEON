from typing import Dict, Any
import time

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
        print("User Interface Activated. Awaiting commands...")
        while self.user_interface_active:
            command = input("Enter command (override, deactivate, exit): ").strip().lower()
            if command == "override":
                self.override_mechanisms()
            elif command == "deactivate":
                self.user_interface_active = False
            elif command == "exit":
                self.user_interface_active = False
                return
            else:
                print("Invalid command. Please try again.")

    def override_mechanisms(self) -> bool:
        """
        Implement override mechanisms allowing humans to take control of autonomous systems.
        
        Returns:
            bool: True if an override was initiated, False otherwise.
        """
        override_request = input("Enter subsystem to override or 'cancel' to abort: ")
        if override_request.lower() == 'cancel':
            return False
        elif override_request.lower() in ['resource', 'maintenance', 'health', 'conflict']:
            action = input(f"Enter action for {override_request}: ")
            self.current_overrides[override_request] = action
            print(f"Override applied: {override_request} - {action}")
            return True
        else:
            print("Invalid subsystem or action. Override not applied.")
            return False

    def monitor_for_intervention(self):
        """Check for conditions or signals indicating a need for human intervention."""
        # This method would typically interface with other systems to detect issues
        # For simulation, we'll just check if there's a need based on a random event
        if random.random() < 0.05:  # 5% chance of needing human intervention each cycle
            print("Alert: Human intervention required. Activating User Interface.")
            self.user_interface()

    def check_active_overrides(self) -> Dict[str, str]:
        """Return the current active overrides."""
        return self.current_overrides

    def cancel_override(self, subsystem: str):
        """Cancel an active override for a specific subsystem."""
        if subsystem in self.current_overrides:
            del self.current_overrides[subsystem]
            print(f"Override for {subsystem} cancelled.")
        else:
            print(f"No active override for {subsystem} to cancel.")

    def emergency_stop(self):
        """Implement an emergency stop function."""
        print("Emergency stop initiated. All systems are being powered down.")
        # In reality, this would interface with all other systems to halt operations safely
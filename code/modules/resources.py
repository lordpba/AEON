import time
from threading import Thread, Lock

class ResourceManagement:
    def __init__(self):
        # Dictionary to store available resources
        self.resources = {
            "water": 100,  # Liters
            "food": 100,   # Units
            "energy": 100  # kWh
        }
        # Lock for thread-safe access to resources
        self.lock = Lock()

    def monitor_resources(self):
        """Continuously monitor the available resources."""
        while True:
            with self.lock:  # Ensure thread-safe monitoring
                print("Current resources:", self.resources)
            time.sleep(5)  # Check every 5 seconds

    def allocate_resource(self, resource_type, amount):
        """
        Allocate a specific amount of a resource type.
        
        Args:
            resource_type (str): Type of resource to allocate.
            amount (int): Amount of resource to allocate.
        """
        with self.lock:
            if resource_type in self.resources:
                if self.resources[resource_type] >= amount:
                    self.resources[resource_type] -= amount
                    print(f"{amount} of {resource_type} allocated.")
                else:
                    print(f"Not enough {resource_type} to allocate {amount}.")
            else:
                print(f"Resource {resource_type} not recognized.")

    def forecast_needs(self):
        """
        Forecast future resource needs based on fixed values.
        
        Returns:
            dict: A dictionary with forecasted needs for each resource type.
        """
        needs = {
            "water": 10,  # Liters per unit time
            "food": 5,    # Units per unit time
            "energy": 20  # kWh per unit time
        }
        return needs

    def run(self):
        """Start the resource monitoring thread."""
        monitoring_thread = Thread(target=self.monitor_resources)
        monitoring_thread.start()

# Example usage:
if __name__ == "__main__":
    rm = ResourceManagement()
    rm.run()
    rm.allocate_resource("water", 10)
    print("Forecasted needs:", rm.forecast_needs())
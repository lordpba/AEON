"""
Public Services Management Module
Manages municipal services: water, electricity, waste, transport, internet
"""
import time
from threading import Thread, Lock


class PublicServicesManagement:
    def __init__(self):
        # Dictionary to store service metrics
        self.services = {
            "water_supply": 5000.0,      # m³
            "electricity": 200.0,         # MWh
            "waste_management": 15.0,     # tons
            "public_transport": 500.0,    # available capacity
            "internet_bandwidth": 10.0    # Gbps
        }
        # Lock for thread-safe access
        self.lock = Lock()

    def monitor_services(self):
        """Continuously monitor the available services."""
        while True:
            with self.lock:  # Ensure thread-safe monitoring
                print("Current service levels:", self.services)
            time.sleep(5)  # Check every 5 seconds

    def allocate_service(self, service_type, amount):
        """
        Allocate a specific amount of a service.
        
        Args:
            service_type (str): Type of service to allocate.
            amount (float): Amount of service to allocate.
        """
        with self.lock:
            if service_type in self.services:
                if self.services[service_type] >= amount:
                    self.services[service_type] -= amount
                    print(f"{amount} units of {service_type} allocated.")
                else:
                    print(f"Insufficient {service_type} to allocate {amount}.")
            else:
                print(f"Service {service_type} not recognized.")

    def forecast_needs(self):
        """
        Forecast future service needs based on population and trends.
        
        Returns:
            dict: A dictionary with forecasted needs for each service type.
        """
        needs = {
            "water_supply": 150.0,         # m³ per day
            "electricity": 8.0,             # MWh per day
            "waste_management": 1.5,        # tons per day
            "public_transport": 500.0,      # trips per day
            "internet_bandwidth": 1.0       # Gbps needed
        }
        return needs

    def run(self):
        """Start the service monitoring thread."""
        monitoring_thread = Thread(target=self.monitor_services)
        monitoring_thread.start()


# Example usage:
if __name__ == "__main__":
    psm = PublicServicesManagement()
    psm.run()
    psm.allocate_service("water_supply", 100.0)
    print("Forecasted needs:", psm.forecast_needs())
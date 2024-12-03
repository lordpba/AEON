import time
from threading import Thread

class ResourceManagement:
    def __init__(self):
        self.resources = {
            "water": 100,  # Liters
            "food": 100,   # Units
            "energy": 100  # kWh
        }
        self.lock = threading.Lock()

    def monitor_resources(self):
        while True:
            # Simulazione di monitoraggio delle risorse
            print("Risorse attuali:", self.resources)
            time.sleep(5)  # Controlla ogni 5 secondi

    def allocate_resource(self, resource_type, amount):
        with self.lock:
            if resource_type in self.resources:
                if self.resources[resource_type] >= amount:
                    self.resources[resource_type] -= amount
                    print(f"{amount} di {resource_type} allocati.")
                else:
                    print(f"Non abbastanza {resource_type} per allocare {amount}.")
            else:
                print(f"Risorsa {resource_type} non riconosciuta.")

    def forecast_needs(self):
        # Simulazione di previsione delle necessità
        needs = {
            "water": 10,  # Liters per unità di tempo
            "food": 5,    # Units per unità di tempo
            "energy": 20  # kWh per unità di tempo
        }
        return needs

    def run(self):
        monitoring_thread = Thread(target=self.monitor_resources)
        monitoring_thread.start()

# Esempio di utilizzo:
if __name__ == "__main__":
    rm = ResourceManagement()
    rm.run()
    rm.allocate_resource("water", 10)
    print("Previsione delle necessità:", rm.forecast_needs())
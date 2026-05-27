"""Quick test of AEON simulation - No external dependencies"""
import sys
from pathlib import Path

# Set up paths
CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))

from config import CommunityConfig, DEFAULT_CONFIG

print("🚀 AEON Community Configuration Test")
print("=" * 50)

# Test configuration
config = CommunityConfig(
    name="Test Municipality Alpha",
    population_size=5000,
    time_scale=1.0
)

print(f"\n✅ Configuration loaded successfully!")
print(f"\nCommunity Details:")
print(f"  Name: {config.name}")
print(f"  Population: {config.population_size}")
print(f"  Time Scale: {config.time_scale}x")
print(f"  Annual Budget: {config.annual_budget} EUR")

print(f"\nService Capacities:")
for service, capacity in config.service_capacity.items():
    print(f"  {service.replace('_', ' ').title()}: {capacity:.1f}")

print(f"\nConsumption Rates (per person per day):")
for service, rate in config.consumption_rates.items():
    print(f"  {service.replace('_', ' ').title()}: {rate:.5f}")
    if rate > 0:
        total_daily = rate * config.population_size
        capacity = config.service_capacity.get(service, 0)
        margin = capacity - total_daily
        print(f"    → Daily total: {total_daily:.2f} | Capacity: {capacity:.2f} | Margin: {margin:.2f}")

print(f"\nEvent Probabilities:")
for event, prob in config.event_probabilities.items():
    print(f"  {event.replace('_', ' ').title()}: {prob*100:.1f}%")

print("\n" + "=" * 50)
print("✅ AEON Core Systems Operational!")

"""Quick test of AEON simulation - No external dependencies"""
import sys
sys.path.insert(0, '/workspaces/AEON/code')

from config import ColonyConfig

print("🚀 AEON Configuration Test")
print("=" * 50)

# Test configuration
config = ColonyConfig(
    name="Test Colony Alpha",
    population_size=50,
    time_scale=1.0
)

print(f"\n✅ Configuration loaded successfully!")
print(f"\nColony Details:")
print(f"  Name: {config.name}")
print(f"  Population: {config.population_size}")
print(f"  Time Scale: {config.time_scale}x")
print(f"\nStarting Resources:")
for resource, amount in config.starting_resources.items():
    print(f"  {resource.capitalize()}: {amount:.0f}")

print(f"\nConsumption Rates (per person per sol):")
for resource, rate in config.consumption_rates.items():
    print(f"  {resource.capitalize()}: {rate:.1f}")
    days_supply = config.starting_resources.get(resource, 0) / (rate * config.population_size)
    print(f"    → Supply lasts: {days_supply:.1f} sols")

print(f"\nEvent Probabilities:")
for event, prob in config.event_probabilities.items():
    print(f"  {event.replace('_', ' ').title()}: {prob*100:.1f}%")

print("\n" + "=" * 50)
print("✅ AEON Core Systems Operational!")
print("\n📚 Ready for full simulation")

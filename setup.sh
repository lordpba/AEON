#!/bin/bash
# AEON Quick Setup Script

echo "🚀 AEON Colony Simulator - Quick Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p saves logs data
echo "✓ Directories created"
echo ""

# Install Python dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "⚠️  Some dependencies may have failed to install"
    echo "   Please check the output above"
fi
echo ""

# Create a simple test script
echo "Creating test configuration..."
cat > code/test_sim.py << 'EOF'
"""Quick test of AEON simulation"""
from aeon_simulator import AEONColonySimulator
from config import ColonyConfig
import time

print("🚀 Starting AEON Test Simulation...")
print("=" * 50)

# Create a fast test configuration
config = ColonyConfig(
    name="Test Colony",
    population_size=20,
    time_scale=10.0  # 10x speed for quick testing
)

# Initialize simulator
sim = AEONColonySimulator(config)
sim.start()

print("✓ Simulation started successfully!")
print("\nRunning for 30 seconds (will simulate ~5 sols)...")
print("Watch for events and status updates...")
print("-" * 50)

# Run for 30 seconds
try:
    for i in range(6):
        time.sleep(5)
        print(f"\n📊 Status Update ({i+1}/6):")
        state = sim.get_current_state()
        print(f"  Sol: {state['sol']:.2f}")
        print(f"  Morale: {state['morale']:.1f}%")
        print(f"  System Health: {state['system_health']['overall_health']:.1f}%")
        print(f"  Active Events: {len(state['active_events'])}")
        
        if state['active_events']:
            print(f"  Latest Event: {state['active_events'][0]['description']}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed successfully!")
    print("\nFinal Summary:")
    print(sim.get_summary())
    
    # Save test state
    sim.save_state("saves/test_run.json")
    print("\n💾 Saved to saves/test_run.json")
    
except KeyboardInterrupt:
    print("\n⚠️  Test interrupted by user")
except Exception as e:
    print(f"\n❌ Error during test: {e}")
finally:
    sim.stop()
    print("\n🛑 Simulation stopped")

print("\n🎉 AEON is ready to use!")
print("\nNext steps:")
print("  1. Run the dashboard: streamlit run code/dashboard.py")
print("  2. Run CLI simulation: python code/aeon_simulator.py")
print("  3. Check documentation: README_NEW.md")
EOF

echo "✓ Test script created"
echo ""

echo "======================================"
echo "✅ Setup Complete!"
echo ""
echo "Quick Start Options:"
echo ""
echo "  1️⃣  Test the simulation:"
echo "     python code/test_sim.py"
echo ""
echo "  2️⃣  Launch interactive dashboard:"
echo "     streamlit run code/dashboard.py"
echo ""
echo "  3️⃣  Run CLI simulation:"
echo "     python code/aeon_simulator.py"
echo ""
echo "📚 For more information, see README_NEW.md"
echo ""
echo "🚀 Welcome to AEON!"
echo "======================================"

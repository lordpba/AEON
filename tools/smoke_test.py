"""Simple smoke tests for AEON core modules.

This script imports key modules and runs a few non-blocking checks to ensure
that basic functions execute without raising exceptions.
"""

import sys
import os

# Ensure project `code/` directory is on sys.path for imports
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CODE_DIR = os.path.join(ROOT, 'code')
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from modules.maintenance import MaintenanceAndRepairs
from AeonMainCore import ResourceManagement, AutonomousGovernance


def run_smoke_tests():
    print("Starting smoke tests...")

    # Maintenance tests
    maint = MaintenanceAndRepairs()
    print("Created MaintenanceAndRepairs")
    status = maint.preventive_monitoring()
    print("Preventive monitoring returned overall_health=", status.get("overall_health"))

    # Resource management tests
    rm = ResourceManagement()
    print("Created ResourceManagement")
    resources = rm.monitor_resources()
    print("Resource levels:", resources)

    # AutonomousGovernance instantiation
    ag = AutonomousGovernance()
    print("Created AutonomousGovernance (threads not started)")

    print("Smoke tests completed successfully.")


if __name__ == '__main__':
    run_smoke_tests()

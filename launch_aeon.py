"""
AEON Launcher Script
Avvia solo la dashboard Streamlit come processo principale.
"""

import os
import sys
import subprocess

def main():
    CODE_DIR = os.path.join(os.path.dirname(__file__), 'code')
    dashboard_path = os.path.join(CODE_DIR, 'dashboard.py')
    print("Avvio la dashboard Streamlit...")
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', dashboard_path
    ])

if __name__ == "__main__":
    main()

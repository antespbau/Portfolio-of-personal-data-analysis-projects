import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

scripts = [
     
]

for script in scripts:
    script_path = BASE_DIR / script
    print(f"\nRunning {script_path}...")

    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error in {script}:")
        print(result.stderr)
        break
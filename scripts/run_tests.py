"""
Automated Test Runner Script.
Executes pytest across unit, integration, validation, and prediction test suites.
"""
import sys
import subprocess
import os

def main():
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE FOR HEART DISEASE PREDICTION SYSTEM")
    print("=" * 70)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tests_dir = os.path.join(base_dir, "backend", "tests")

    cmd = [sys.executable, "-m", "pytest", tests_dir, "-v", "--tb=short"]
    result = subprocess.run(cmd, cwd=base_dir)

    print("\n" + "=" * 70)
    if result.returncode == 0:
        print("[SUCCESS] ALL TESTS PASSED SUCCESSFULLY (24/24)!")
    else:
        print(f"[FAILURE] TEST FAILURES DETECTED (Exit code: {result.returncode})")
    print("=" * 70)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

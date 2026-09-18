"""
StackOfFifty - Unified Local Dev Process Launcher
Spawns both the FastAPI backend and Next.js dashboard concurrently.
"""
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

root_dir = Path(__file__).resolve().parent

def main():
    print("=" * 55)
    print("       StackOfFifty Cybersecurity Platform Launcher       ")
    print("=" * 55)

    print("\n[1/2] Starting FastAPI Backend (Port 8000)...")
    api_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=str(root_dir)
    )

    time.sleep(2)

    print("[2/2] Starting Next.js SOC Dashboard (Port 3000)...")
    dashboard_dir = root_dir / "dashboard"
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    dashboard_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(dashboard_dir)
    )

    print("\n[+] StackOfFifty services running!")
    print("    - Backend API: http://localhost:8000/docs")
    print("    - SOC Dashboard: http://localhost:3000")
    print("\nPress Ctrl+C to stop all services.")

    try:
        webbrowser.open("http://localhost:3000")
        api_proc.wait()
        dashboard_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping StackOfFifty services...")
        api_proc.terminate()
        dashboard_proc.terminate()
        print("All services stopped.")

if __name__ == "__main__":
    main()

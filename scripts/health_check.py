"""
Diagnostic and platform health check CLI for StackOfFifty.
"""
import sys
import psutil
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from core.config_loader import config_loader
from core.database.connection import engine, SessionLocal
from core.database.models import User, ModuleModel, Alert
from core.module_registry import module_registry
from core.event_bus import event_bus

def run_health_check():
    print("\n=======================================================")
    print("      StackOfFifty Platform Diagnostic Health Check       ")
    print("=======================================================\n")

    errors = 0

    # 1. Config Check
    try:
        cfg = config_loader.load()
        platform_name = cfg.get("platform", {}).get("display_name", "Unknown")
        total_modules = len(cfg.get("modules", []))
        print(f"[+] Configuration: OK (Platform: {platform_name}, {total_modules} modules configured)")
    except Exception as e:
        print(f"[-] Configuration Error: {e}")
        errors += 1

    # 2. Database Check
    try:
        db = SessionLocal()
        user_count = db.query(User).count()
        alert_count = db.query(Alert).count()
        db.close()
        print(f"[+] Database Connection: OK (DB URL: {engine.url}, Users: {user_count}, Alerts: {alert_count})")
    except Exception as e:
        print(f"[-] Database Error: {e}")
        errors += 1

    # 3. Module Registry Check
    try:
        module_registry.load_all()
        loaded = len(module_registry.modules)
        print(f"[+] Module Registry: OK ({loaded} active modules loaded)")
        for mod_id, mod in module_registry.modules.items():
            print(f"    - {mod_id}: {mod.display_name} [{mod.category}] (Status: {mod.status})")
    except Exception as e:
        print(f"[-] Module Registry Error: {e}")
        errors += 1

    # 4. System Telemetry Check
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        print(f"[+] System Telemetry: OK (CPU: {cpu}%, RAM: {mem.percent}% used, {round(mem.available / (1024*1024), 1)} MB free)")
    except Exception as e:
        print(f"[-] System Telemetry Error: {e}")
        errors += 1

    # 5. Event Bus Check
    try:
        event_bus.emit("health_check", "diagnostic_ping", {"status": "ok"})
        print("[+] Event Bus: OK (In-memory / Redis bus operational)")
    except Exception as e:
        print(f"[-] Event Bus Error: {e}")
        errors += 1

    print("\n-------------------------------------------------------")
    if errors == 0:
        print(" Platform Status: ALL SYSTEMS OPERATIONAL (GREEN) ")
    else:
        print(f" Platform Status: {errors} SYSTEM(S) REPORTED ERRORS ")
    print("-------------------------------------------------------\n")
    return 0 if errors == 0 else 1

if __name__ == "__main__":
    sys.exit(run_health_check())

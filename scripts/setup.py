"""
First-time platform setup and bootstrapper for StackOfFifty.
"""
import os
import sys
import secrets
from pathlib import Path

# Ensure root directory is on sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from core.database.connection import init_db, SessionLocal
from core.database.models import User, Alert
from core.auth.jwt_handler import hash_password
from core.config_loader import config_loader
from core.logger import get_logger

logger = get_logger("setup")

def run_setup(interactive: bool = True):
    print("\n=======================================================")
    print("      StackOfFifty Cybersecurity Platform Setup           ")
    print("=======================================================\n")

    print("[*] Verifying master configuration...")
    cfg = config_loader.load()
    print(f"    Platform: {cfg['platform']['display_name']}")
    print(f"    Version : {cfg['platform']['version']}")
    print(f"    Modules : {len(cfg.get('modules', []))} configured")

    print("\n[*] Initializing database schemas...")
    init_db()
    print("    Database initialized successfully.")

    print("\n[*] Configuring Administrator Account...")
    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if existing_admin:
            print(f"    Existing admin account found: '{existing_admin.username}'")
        else:
            username = os.environ.get("ADMIN_SEED_USERNAME", "admin").strip()
            email = os.environ.get("ADMIN_SEED_EMAIL", "admin@stackoffifty.local").strip()
            password = os.environ.get("ADMIN_SEED_PASSWORD", "").strip()

            if not password and interactive and sys.stdin.isatty():
                print(f"    Setting up admin user '{username}'.")
                user_input = input("    Enter master admin password (leave empty to generate secure random): ").strip()
                if user_input:
                    password = user_input

            if not password:
                password = secrets.token_urlsafe(18)
                print("\n    [!] SECURE ADMIN CREDENTIALS GENERATED:")
                print(f"    [!] Username: {username}")
                print(f"    [!] Password: {password}")
                print("    [!] Please record this password safely.\n")
            else:
                print(f"    Admin account configured for '{username}'.")

            admin = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("    Admin account created successfully.")
    finally:
        db.close()

    print("\n[*] Setup Complete! You can now start the platform with:")
    print("    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload\n")

if __name__ == "__main__":
    interactive_mode = "--non-interactive" not in sys.argv
    run_setup(interactive=interactive_mode)

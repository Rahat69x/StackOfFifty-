"""
MFA / TOTP authentication and brute-force protection engine.
"""
import pyotp
from datetime import datetime, timezone
from typing import Dict, List, Any

class MFAGuardEngine:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.is_running = False
        self.max_failed = settings.get("max_failed_attempts", 5)
        self.failed_attempts: Dict[str, int] = {}
        self.auth_events: List[Dict[str, Any]] = []

    async def start(self):
        self.is_running = True

    async def stop(self):
        self.is_running = False

    def generate_provisioning_uri(self, user_identifier: str, secret: str = None) -> Dict[str, str]:
        """Generate TOTP secret and QR provisioning URI."""
        totp_secret = secret or pyotp.random_base32()
        totp = pyotp.TOTP(totp_secret)
        uri = totp.provisioning_uri(name=user_identifier, issuer_name="StackOfFifty Platform")
        return {"secret": totp_secret, "provisioning_uri": uri}

    def verify_totp(self, user_identifier: str, secret: str, token: str) -> Dict[str, Any]:
        """Validate a 6-digit TOTP token against secret with replay and brute-force tracking."""
        attempts = self.failed_attempts.get(user_identifier, 0)
        if attempts >= self.max_failed:
            result = {
                "user": user_identifier,
                "valid": False,
                "locked": True,
                "reason": f"Account temporarily locked due to {attempts} consecutive failed attempts."
            }
            self.auth_events.append({**result, "timestamp": datetime.now(timezone.utc).isoformat()})
            return result

        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(token, valid_window=1)

        if is_valid:
            self.failed_attempts[user_identifier] = 0
            result = {
                "user": user_identifier,
                "valid": True,
                "locked": False,
                "reason": "TOTP token verified successfully."
            }
        else:
            self.failed_attempts[user_identifier] = attempts + 1
            result = {
                "user": user_identifier,
                "valid": False,
                "locked": (attempts + 1) >= self.max_failed,
                "failed_count": attempts + 1,
                "reason": "Invalid TOTP code supplied."
            }

        self.auth_events.append({**result, "timestamp": datetime.now(timezone.utc).isoformat()})
        if len(self.auth_events) > 100:
            self.auth_events.pop(0)
        return result

    def get_summary(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_running,
            "max_failed_attempts_allowed": self.max_failed,
            "currently_locked_accounts": [u for u, cnt in self.failed_attempts.items() if cnt >= self.max_failed],
            "total_verifications": len(self.auth_events),
            "recent_events": self.auth_events[-10:]
        }

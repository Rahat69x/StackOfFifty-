"""
Core implementation logic for Honeypot Deception Sensor.
"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any

class HoneypotEngine:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.is_running = False
        self.events: List[Dict[str, Any]] = []
        self.decoy_stats = {
            "http_admin_decoy": {"connections": 0, "probes": 0},
            "ssh_decoy": {"connections": 0, "auth_attempts": 0},
            "telnet_decoy": {"connections": 0, "commands": 0}
        }

    async def start(self):
        self.is_running = True
        # Seed initial baseline decoy status
        if not self.events:
            self.record_intrusion(
                source_ip="192.168.1.145",
                decoy_service="http_admin_decoy",
                details="HTTP GET /admin/config.php probe detected",
                severity="medium"
            )

    async def stop(self):
        self.is_running = False

    def record_intrusion(self, source_ip: str, decoy_service: str, details: str, severity: str = "medium") -> Dict[str, Any]:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": source_ip,
            "decoy_service": decoy_service,
            "details": details,
            "severity": severity
        }
        self.events.append(event)
        max_buffer = self.settings.get("max_event_buffer", 200)
        if len(self.events) > max_buffer:
            self.events.pop(0)

        if decoy_service in self.decoy_stats:
            self.decoy_stats[decoy_service]["connections"] += 1
            if "probe" in details.lower():
                self.decoy_stats[decoy_service]["probes"] = self.decoy_stats[decoy_service].get("probes", 0) + 1
        return event

    def get_summary(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_running,
            "total_intrusions_logged": len(self.events),
            "decoy_statistics": self.decoy_stats,
            "recent_intrusions": self.events[-10:]
        }

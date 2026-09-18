"""
Firewall policy rule engine and packet evaluator.
"""
from typing import Dict, List, Any

class FirewallRuleEngine:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.is_running = False
        self.default_action = settings.get("default_policy", "DROP")
        # Preloaded defensive baseline rules
        self.rules: List[Dict[str, Any]] = [
            {"id": "rule_01", "action": "ALLOW", "proto": "TCP", "src": "any", "dst_port": 443, "desc": "Allow HTTPS inbound"},
            {"id": "rule_02", "action": "ALLOW", "proto": "TCP", "src": "any", "dst_port": 80, "desc": "Allow HTTP inbound"},
            {"id": "rule_03", "action": "ALLOW", "proto": "UDP", "src": "any", "dst_port": 53, "desc": "Allow DNS outbound"},
            {"id": "rule_04", "action": "DROP", "proto": "TCP", "src": "any", "dst_port": 23, "desc": "Drop Telnet"},
            {"id": "rule_05", "action": "DROP", "proto": "TCP", "src": "any", "dst_port": 445, "desc": "Block SMB from public"}
        ]
        self.evaluated_packets: List[Dict[str, Any]] = []

    async def start(self):
        self.is_running = True

    async def stop(self):
        self.is_running = False

    def add_rule(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        rule["id"] = f"rule_{len(self.rules) + 1:02d}"
        self.rules.append(rule)
        return rule

    def evaluate_packet(self, proto: str, src_ip: str, dst_port: int) -> Dict[str, Any]:
        """Test a packet against ACL rules in top-down order."""
        proto = proto.upper()
        decision = self.default_action
        matched_rule = None

        for r in self.rules:
            if r.get("proto", "ANY").upper() in (proto, "ANY"):
                if r.get("dst_port") == dst_port or r.get("dst_port") is None:
                    decision = r.get("action", self.default_action)
                    matched_rule = r
                    break

        result = {
            "proto": proto,
            "src_ip": src_ip,
            "dst_port": dst_port,
            "decision": decision,
            "matched_rule_id": matched_rule["id"] if matched_rule else "DEFAULT_POLICY"
        }
        self.evaluated_packets.append(result)
        if len(self.evaluated_packets) > 100:
            self.evaluated_packets.pop(0)
        return result

    def get_summary(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_running,
            "default_policy": self.default_action,
            "active_rules_count": len(self.rules),
            "rules": self.rules,
            "recent_evaluations": self.evaluated_packets[-10:]
        }

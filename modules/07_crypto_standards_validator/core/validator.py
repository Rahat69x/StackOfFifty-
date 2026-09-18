"""
Cryptographic algorithm and key compliance engine.
"""
from typing import Dict, List, Any

class CryptoStandardsEngine:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.is_running = False
        self.disallowed_ciphers = [c.upper() for c in settings.get("disallowed_ciphers", ["DES", "3DES", "RC4", "RC2", "BLOWFISH"])]
        self.disallowed_hashes = [h.upper() for h in settings.get("disallowed_hashes", ["MD4", "MD5", "SHA1"])]
        self.min_rsa_bits = settings.get("min_rsa_bits", 2048)
        self.min_ecc_bits = settings.get("min_ecc_bits", 256)
        self.audit_log: List[Dict[str, Any]] = []

    async def start(self):
        self.is_running = True

    async def stop(self):
        self.is_running = False

    def audit_primitive(self, primitive_type: str, name: str, key_size: int = 0) -> Dict[str, Any]:
        """Audit a single cryptographic primitive for compliance."""
        name_upper = name.upper()
        violations = []
        status = "compliant"

        if primitive_type.lower() == "cipher":
            if any(bad in name_upper for bad in self.disallowed_ciphers):
                violations.append(f"Cipher '{name}' is deprecated due to structural weaknesses or small block sizes.")
                status = "non_compliant"
        elif primitive_type.lower() == "hash":
            if any(bad == name_upper for bad in self.disallowed_hashes):
                violations.append(f"Hash function '{name}' is vulnerable to collision attacks (NIST SP 800-131A disallowance).")
                status = "non_compliant"
        elif primitive_type.lower() == "asymmetric":
            if "RSA" in name_upper and key_size < self.min_rsa_bits:
                violations.append(f"RSA key size {key_size} is below the mandatory minimum of {self.min_rsa_bits} bits.")
                status = "non_compliant"
            elif ("ECC" in name_upper or "ECDSA" in name_upper) and key_size < self.min_ecc_bits:
                violations.append(f"ECC curve size {key_size} is below the recommended {self.min_ecc_bits} bits.")
                status = "non_compliant"

        result = {
            "primitive_type": primitive_type,
            "name": name,
            "key_size": key_size,
            "status": status,
            "violations": violations,
            "nist_standard": "NIST SP 800-131A Rev 2"
        }
        self.audit_log.append(result)
        if len(self.audit_log) > 100:
            self.audit_log.pop(0)
        return result

    def get_summary(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_running,
            "standards_enforced": ["NIST SP 800-131A Rev 2", "FIPS 140-3"],
            "disallowed_ciphers": self.disallowed_ciphers,
            "disallowed_hashes": self.disallowed_hashes,
            "min_rsa_bits": self.min_rsa_bits,
            "total_audits_performed": len(self.audit_log),
            "recent_audits": self.audit_log[-10:]
        }

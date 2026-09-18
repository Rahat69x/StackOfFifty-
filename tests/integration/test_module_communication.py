"""
Integration tests for inter-module event bus dispatch and subscriptions.
"""
import pytest
from core.event_bus import event_bus

def test_event_bus_pub_sub():
    received = []

    def handler(payload):
        received.append(payload)

    event_bus.subscribe("test_security_alert", handler)
    event_bus.emit("mod_001", "test_security_alert", {"threat_score": 95})

    assert len(received) >= 1
    latest = received[-1]
    assert latest["sender"] == "mod_001"
    assert latest["event_type"] == "test_security_alert"
    assert latest["data"]["threat_score"] == 95

    # Check history
    history = event_bus.get_recent_events(limit=5)
    assert any(e["event_type"] == "test_security_alert" for e in history)

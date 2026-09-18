"""
Unit tests for configuration loader and environment variable substitution.
"""
import os
import pytest
from core.config_loader import ConfigLoader

def test_config_loader_reads_platform_config():
    loader = ConfigLoader("platform.config.json")
    cfg = loader.get_config()
    assert "platform" in cfg
    assert cfg["platform"]["name"] == "StackOfFifty"
    assert "modules" in cfg
    assert len(cfg["modules"]) >= 50

def test_env_var_substitution(monkeypatch):
    monkeypatch.setenv("TEST_CYBER_ENV", "secure_value_123")
    loader = ConfigLoader("platform.config.json")
    result = loader._substitute_env_vars("value is ${TEST_CYBER_ENV}")
    assert result == "value is secure_value_123"

"""
API endpoint tests for /api/modules routes.
"""
import pytest
from starlette.testclient import TestClient
from api.main import app

def test_module_api_endpoints():
    with TestClient(app) as client:
        # 1. Health
        health_res = client.get("/api/health")
        assert health_res.status_code == 200
        assert health_res.json()["status"] == "healthy"

        # 2. List modules
        mod_res = client.get("/api/modules")
        assert mod_res.status_code == 200
        modules = mod_res.json()
        assert len(modules) >= 50

        # 3. Categories
        cat_res = client.get("/api/modules/categories")
        assert cat_res.status_code == 200
        assert len(cat_res.json()) == 12

        # 4. Search
        search_res = client.get("/api/modules/search?q=honeypot")
        assert search_res.status_code == 200
        assert len(search_res.json()) >= 1

        # 5. Module status check
        stat_res = client.get("/api/modules/mod_001/status")
        assert stat_res.status_code == 200
        assert stat_res.json()["module_id"] == "mod_001"

        # 6. Module results
        res_res = client.get("/api/modules/mod_001/results")
        assert res_res.status_code == 200
        assert "is_active" in res_res.json()

        # 7. Module report
        rep_res = client.get("/api/modules/mod_001/report")
        assert rep_res.status_code == 200
        assert "results" in rep_res.json()

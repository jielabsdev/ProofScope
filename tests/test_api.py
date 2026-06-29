from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_verify_passing_artifact() -> None:
    response = client.post(
        "/api/v1/audits/verify",
        files={"file": ("passing.proof", b"valid proof bytes", "application/octet-stream")},
    )

    assert response.status_code == 200
    report = response.json()
    assert report["verified"] is True
    assert report["status"] == "pass"
    assert report["artifact_name"] == "passing.proof"
    assert report["constraints"]


def test_verify_policy_failure() -> None:
    response = client.post(
        "/api/v1/audits/verify",
        files={"file": ("policy.proof", b"policy_deviation", "application/octet-stream")},
    )

    assert response.status_code == 200
    report = response.json()
    assert report["verified"] is False
    assert report["status"] == "fail"
    assert any("Layer 4" == item["layer"] for item in report["constraints"])

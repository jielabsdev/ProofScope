from __future__ import annotations

from api.verifier import verify_proof_artifact


def test_python_fallback_report_shape() -> None:
    report = verify_proof_artifact(b"demo proof", "demo.proof")

    assert report.artifact_name == "demo.proof"
    assert report.status in {"pass", "fail"}
    assert len(report.constraints) == 3
    assert len(report.trace) == 3

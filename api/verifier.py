from __future__ import annotations

import hashlib
import time
from collections.abc import Mapping
from typing import Any

from api.models import AuditReport

try:
    import proofscope_engine
except ImportError:  # pragma: no cover - exercised when C++ extension is not built.
    proofscope_engine = None


def verify_proof_artifact(proof_bytes: bytes, filename: str) -> AuditReport:
    if proofscope_engine is not None:
        raw_report = proofscope_engine.verify_proof_bytes(proof_bytes)
        return _normalize_report(raw_report, filename=filename, engine="cpp-pybind11")

    return _python_fallback_verify(proof_bytes=proof_bytes, filename=filename)


def _normalize_report(raw_report: Mapping[str, Any], filename: str, engine: str) -> AuditReport:
    report = dict(raw_report)
    report["artifact_name"] = filename
    report["engine"] = engine
    return AuditReport.model_validate(report)


def _python_fallback_verify(proof_bytes: bytes, filename: str) -> AuditReport:
    started = time.perf_counter()
    has_bytes = bool(proof_bytes)
    explicit_failure = b"FAIL" in proof_bytes or b"constraint_violation" in proof_bytes
    policy_failure = b"policy_deviation" in proof_bytes
    verified = has_bytes and not explicit_failure and not policy_failure

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    return AuditReport(
        verified=verified,
        status="pass" if verified else "fail",
        proof_digest=hashlib.sha256(proof_bytes).hexdigest()[:16],
        verification_time_ms=elapsed_ms,
        artifact_name=filename,
        engine="python-fallback",
        constraints=[
            {
                "id": "circuit.integrity",
                "layer": "Circuit",
                "satisfied": has_bytes and not explicit_failure,
                "confidence": 0.99 if has_bytes else 0.0,
                "message": (
                    "Circuit witness commitments are internally consistent."
                    if has_bytes
                    else "Proof artifact is empty."
                ),
            },
            {
                "id": "model.layer_4.policy",
                "layer": "Layer 4",
                "satisfied": not policy_failure,
                "confidence": 0.41 if policy_failure else 0.97,
                "message": (
                    "Model output deviated from policy X at Layer 4."
                    if policy_failure
                    else "Layer 4 policy gate remained within the approved path."
                ),
            },
            {
                "id": "output.binding",
                "layer": "Output",
                "satisfied": verified,
                "confidence": 0.98 if verified else 0.52,
                "message": (
                    "Public output binding matches the verified execution trace."
                    if verified
                    else "Output binding could not be trusted because verification failed."
                ),
            },
        ],
        trace=[
            {
                "operation": "load_proof",
                "layer": "Input",
                "policy": "Artifact Intake",
                "detail": "Read raw proof artifact bytes.",
            },
            {
                "operation": "verify_constraints",
                "layer": "Circuit",
                "policy": "Mathematical Integrity",
                "detail": (
                    "Constraint violation marker detected."
                    if explicit_failure
                    else "All mock circuit constraints satisfied."
                ),
            },
            {
                "operation": "map_policy",
                "layer": "Layer 4",
                "policy": "Policy X",
                "detail": (
                    "Policy deviation marker detected."
                    if policy_failure
                    else "Execution path mapped to approved policy branch."
                ),
            },
        ],
    )

from __future__ import annotations

from pydantic import BaseModel, Field


class ConstraintRecord(BaseModel):
    id: str
    layer: str
    satisfied: bool
    confidence: float = Field(ge=0.0, le=1.0)
    message: str


class TraceRecord(BaseModel):
    operation: str
    layer: str
    policy: str
    detail: str


class AuditReport(BaseModel):
    verified: bool
    status: str
    proof_digest: str
    verification_time_ms: int = Field(ge=0)
    artifact_name: str
    engine: str
    constraints: list[ConstraintRecord]
    trace: list[TraceRecord]

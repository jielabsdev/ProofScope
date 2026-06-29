from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from schemas.error_codes import AuditErrorCode


class AuditReport(BaseModel):
    proof_id: str = Field(..., description="Unique hash of the proof artifact")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="UTC generation timestamp")
    status: str = Field(..., description="Result of verification: PASS or FAIL")
    model_version: str = Field(..., description="Target machine learning model iteration version")
    error_code: AuditErrorCode = Field(default=AuditErrorCode.VALID, description="Diagnostic classification tracking reason code")
    
    # Compliance Metrics
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Mathematical certainty weight coefficient")
    constraint_utilization: float = Field(..., ge=0.0, le=1.0, description="Percentage of circuit constraints actively validated")

    # Technical Metrics
    execution_time_ms: float = Field(..., description="Total cryptographic verification runtime duration")
    circuit_depth: int = Field(..., description="Number of sequential layers in the arithmetic circuit")
    gate_count: int = Field(..., description="Total number of constraint gates mapped inside the circuit")
    
    # Compliance & Traceability
    policy_compliance: bool = Field(..., description="Indicates if the model execution respected rule sets")
    policy_flags: List[str] = Field(default_factory=list, description="Collection of warnings or policy labels triggered")
    execution_path_hash: str = Field(..., description="Cryptographic trace of the execution path")

from enum import Enum

class AuditErrorCode(str, Enum):
    VALID = "SUCCESS"
    ERR_INVALID_PROOF = "ERR_001_INVALID_PROOF"       # Malformed, empty, or corrupt proof artifact
    ERR_ENGINE_TIMEOUT = "ERR_002_ENGINE_TIMEOUT"     # Verification hit structural threshold window (30s)
    ERR_CONSTRAINT_FAIL = "ERR_003_CONSTRAINT_FAIL"   # Proof fundamentally failed circuit arithmetic math validation
    ERR_CONFIDENCE_LOW = "ERR_004_CONFIDENCE_LOW"     # Confidence verification score falls below acceptance parameters
    ERR_UNSUPPORTED_FORMAT = "ERR_005_UNSUPPORTED"    # Version, layout, or curve parameter mismatch
    ERR_INTERNAL = "ERR_999_INTERNAL_SYSTEM"          # Unhandled native engine exception or OS memory barrier crash

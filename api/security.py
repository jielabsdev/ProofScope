import os
from fastapi import HTTPException, Security, status, UploadFile
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROOF_SCOPE_KEY")
if not API_KEY:
    raise RuntimeError("FATAL: PROOF_SCOPE_KEY environment variable is not set. Refusing to start with an empty or default secret.")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def validate_api_key(key: str = Security(api_key_header)):
    """Gates routing pathways against unauthorized system-to-system resource access."""
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Invalid cryptographic or operational API Key."
        )

async def validate_file_security(file: UploadFile) -> bytes:
    """Enforces size limits and MIME-type constraints to protect upstream CPU resources."""
    MAX_SIZE = 10 * 1024 * 1024 # 10MB Threshold
    
    # Read the data stream asynchronously into memory to inspect content lengths
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Resource Violation: Upload footprint exceeds maximum allowable limit of 10MB."
        )
        
    # Restrict ingest parameters exclusively to standard binary and JSON vectors
    ALLOWED_TYPES = ["application/octet-stream", "application/json"]
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Media Exception: Content-Type '{file.content_type}' is unauthorized."
        )
        
    return content

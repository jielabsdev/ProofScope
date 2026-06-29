import hashlib
import json
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.getenv("DB_PATH", "./audit_vault.db")

def verify_ledger_integrity() -> int:
    print(f"[Auditor Core] Opening deep verification scan against: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("[Auditor Core] Initial launch warning: database target not yet created. Skipping sweep.")
        return 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, prev_record_hash, record_hash, data_blob FROM reports ORDER BY timestamp ASC, id ASC")
    records = cursor.fetchall()
    conn.close()
    
    expected_parent_hash = "0" * 64
    
    for idx, row in enumerate(records):
        report_id, stored_prev, stored_hash, data_blob = row
        
        if stored_prev != expected_parent_hash:
            raise RuntimeError(
                f"CRITICAL LEDGER MISMATCH: Continuity broke at row index [{idx}] (ID: {report_id}).\n"
                f" -> Expected Parent Hash Reference:  {expected_parent_hash}\n"
                f" -> Stored Parent Hash Reference:    {stored_prev}"
            )
            
        raw_json_payload = json.loads(data_blob)
        serialized_payload = json.dumps(raw_json_payload, sort_keys=True)
        combined_context = serialized_payload + stored_prev
        recomputed_hash = hashlib.sha256(combined_context.encode('utf-8')).hexdigest()
        
        if recomputed_hash != stored_hash:
            raise RuntimeError(
                f"CRITICAL DATA CORRUPTION: Cryptographic fraud detected at row index [{idx}] (ID: {report_id}).\n"
                f" -> Recalculated Payload Hash Signature: {recomputed_hash}\n"
                f" -> Immutable Block Stored Signature:   {stored_hash}"
            )
            
        expected_parent_hash = stored_hash
        
    print(f"[SUCCESS] Replay integrity validation passed cleanly. Confirmed {len(records)} blocks tracking seamlessly.")
    return len(records)

def generate_state_root() -> str:
    if not os.path.exists(DB_PATH):
        return "0" * 64

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT record_hash FROM reports ORDER BY timestamp DESC, id DESC LIMIT 1")
    latest_row = cursor.fetchone()
    conn.close()
    
    return latest_row[0] if latest_row else "0" * 64

if __name__ == "__main__":
    try:
        total_verified = verify_ledger_integrity()
        current_root = generate_state_root()
        print(f"[Auditor Core] Active System State Root: {current_root}")
    except Exception as err:
        print(f"\n=======================================================\n{str(err)}\n=======================================================", file=sys.stderr)
        sys.exit(1)

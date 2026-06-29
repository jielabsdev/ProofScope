import sqlite3
import os
import hashlib
import json
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "./audit_vault.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Establish the immutable structured ledger schema matrix
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            status TEXT,
            prev_record_hash TEXT,
            record_hash TEXT,
            data_blob TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[Vault Chain] Schema initialized with cryptographic anchors at: {DB_PATH}")

def get_last_hash() -> str:
    """Extracts the head block hash pointer from the sequential history chain."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Grab the latest chronological hash to serve as the parent context pointer
    cursor.execute("SELECT record_hash FROM reports ORDER BY timestamp DESC, id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    # Return 64-character zero-string genesis block hash if ledger is empty
    return row[0] if row else "0" * 64

def compute_record_hash(report_dict: dict, prev_hash: str) -> str:
    """Calculates a deterministic SHA-256 block fingerprint string."""
    # Serialize with sorted keys to guarantee deterministic string alignments across architectures
    serialized_payload = json.dumps(report_dict, sort_keys=True)
    combined_context = serialized_payload + prev_hash
    return hashlib.sha256(combined_context.encode('utf-8')).hexdigest()

def save_report_to_chain(report_data) -> str:
    """Atomically binds and commits an audit verification block to the ledger chain."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Fetch parent hash anchor
        prev_hash = get_last_hash()
        
        # 2. Extract and format the dict structures matching standard data schemas
        report_dict = report_data.dict()
        # Cast datetime to string format inside the dictionary for serialization consistency
        if isinstance(report_dict.get("timestamp"), datetime):
            report_dict["timestamp"] = report_dict["timestamp"].isoformat()
            
        # 3. Compute current cryptographic block signature
        current_hash = compute_record_hash(report_dict, prev_hash)
        
        # 4. Insert structured trace into sequential database matrices
        cursor.execute(
            "INSERT INTO reports (id, timestamp, status, prev_record_hash, record_hash, data_blob) VALUES (?, ?, ?, ?, ?, ?)",
            (
                report_data.proof_id,
                report_dict["timestamp"],
                report_data.status,
                prev_hash,
                current_hash,
                report_data.json() # Complete raw telemetry dump
            )
        )
        conn.commit()
        print(f"[Vault Chain] Sequentially chained block linked successfully. Hash: {current_hash[:12]}...")
        return current_hash
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Ledger Chain Appending Interruption Error: {str(e)}")
    finally:
        conn.close()

def get_report_by_id(report_id: str) -> dict | None:
    """Retrieves a specific verification row from the ledger, unpacks the blob, and injects chain metadata."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT prev_record_hash, record_hash, data_blob FROM reports WHERE id = ?", 
        (report_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    prev_hash, current_hash, data_blob = row
    
    try:
        report_data = json.loads(data_blob)
        report_data["id"] = report_id
        report_data["prev_record_hash"] = prev_hash
        report_data["record_hash"] = current_hash
        return report_data
    except Exception as e:
        print(f"[Vault DB] Error parsing record payload blob structure: {str(e)}")
        return None

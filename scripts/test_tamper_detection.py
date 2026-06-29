import sqlite3
import os
import subprocess
import sys

DB_PATH = "./audit_vault.db"

def execute_simulated_tampering():
    print("[Simulation] Step 1: Running validation check across a healthy codebase state...")
    result = subprocess.run([sys.executable, "api/verify_ledger.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print("[Simulation] Aborting test: Ledger is currently failing structural compilation or link matches.")
        print(result.stderr)
        return

    print("[Simulation] Step 2: Injecting fraudulent string modifications inside a database record data blob...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, data_blob FROM reports LIMIT 1")
    target_row = cursor.fetchone()
    
    if not target_row:
        print("[Simulation] Test cancelled: Database contains 0 transaction entries. Pass a test file first.")
        conn.close()
        return
        
    target_id, original_blob = target_row
    
    malicious_blob = original_blob.replace('"status":"PASS"', '"status":"FAIL"')
        
    cursor.execute("UPDATE reports SET data_blob = ? WHERE id = ?", (malicious_blob, target_id))
    conn.commit()
    conn.close()
    print(f"[Simulation] Success: Record Row '{target_id}' data tracking contents have been maliciously altered.")

    print("[Simulation] Step 3: Triggering Auditor Core verification to test trap interception response...")
    audit_check = subprocess.run([sys.executable, "api/verify_ledger.py"], capture_output=True, text=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.cursor().execute("UPDATE reports SET data_blob = ? WHERE id = ?", (original_blob, target_id))
    conn.commit()
    conn.close()

    if audit_check.returncode != 0 and "CRITICAL DATA CORRUPTION" in audit_check.stderr:
        print("\n[TEST RESULT: PASSED] Replay Integrity Verifier intercepted database tampering instantly!")
        print(audit_check.stderr.strip())
    else:
        print("\n[TEST RESULT: FAILED] Security loop allowed tampered database records to bypass validation vectors.")
        print("Stdout:", audit_check.stdout)
        print("Stderr:", audit_check.stderr)

if __name__ == "__main__":
    execute_simulated_tampering()

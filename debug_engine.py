import subprocess, os, json, tempfile

# Simulate what api/main.py does
ENGINE_BINARY_PATH = os.getenv("ENGINE_PATH", "./bin/verifier_cli")
print(f"ENGINE_BINARY_PATH from env: '{ENGINE_BINARY_PATH}'")
print(f"Resolved: {os.path.abspath(ENGINE_BINARY_PATH)}")
print(f"Exists: {os.path.exists(ENGINE_BINARY_PATH)}")

# Create a temp file
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.proof')
tmp.write(b'VALID_PROOF')
tmp_path = tmp.name
tmp.close()

try:
    result = subprocess.run(
        f'"{ENGINE_BINARY_PATH}" "{tmp_path}"',
        capture_output=True, text=True, timeout=30.0, shell=True
    )
    
    print(f"Return code: {result.returncode}")
    print(f"Stdout: [{result.stdout}]")
    print(f"Stderr: [{result.stderr}]")
    
    if result.returncode == 0:
        parsed = json.loads(result.stdout)
        print(f"Parsed JSON: {parsed}")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")
finally:
    os.unlink(tmp_path)

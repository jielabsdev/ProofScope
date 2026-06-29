import sys, json, time

file_path = sys.argv[1]
file_name = file_path.lower()

# Timeout trigger: sleep past the 30s circuit breaker
if 'timeout' in file_name:
    time.sleep(31)
    sys.exit(124)

result = {
    "status": "PASS",
    "version": "v1.0.2",
    "confidence_score": 0.994,
    "constraint_utilization": 0.875,
    "depth": 12,
    "gates": 4500,
    "is_compliant": True,
    "flags": ["NO_UNAUTHORIZED_INPUT"],
    "path_hash": "0xdef987654321"
}

# Corrupt math → constraint failure (exit 2)
if 'corrupt' in file_name:
    sys.exit(2)

# Invalid proof → malformed artifact (exit 1)
if 'invalid' in file_name or 'empty' in file_name:
    sys.exit(1)

# Valid path
print(json.dumps(result))
sys.exit(0)

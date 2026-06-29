# ProofScope Hardened Infrastructure Deployment Runbook

This runbook maintains the target procedures for compiling, establishing dependencies, and spinning up the high-resilience ProofScope validation architecture.

## 1. Cryptographic Engine Native Compilation

To configure the performance C++ execution units using CMake tooling parameters, execute the structural build system commands:

```bash
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```

## 2. Infrastructure Environment Setup

Establish your unique localized directory environments by copying and modifying baseline paths within `.env`.

Initialize the local structural database framework storage vault using the target initialization command sequence:

```bash
python -c "from api.db import init_db; init_db()"
```

## 3. High-Concurrency Multi-Worker Execution Run

Launch the production performance web API using a pool of four pre-forked worker interfaces running under the Uvicorn application loop:

```bash
uvicorn api.main:app --workers 4 --host 127.0.0.1 --port 8057
```

## 4. Verification Code Validation Check Runs

Trigger syntax parsing and operational unit validity tests across your code base to guarantee that all architectural elements integrate smoothly:

```bash
# Validate python syntax state maps
python -m py_compile api/db.py api/main.py

# Verify the local database initialization script initializes correctly
python -c "from api.db import init_db; init_db()"
```

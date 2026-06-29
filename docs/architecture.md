# ProofScope Architecture

ProofScope is built around a stable audit contract and a replaceable verifier engine.

## Components

### C++ Proof Verifier

The engine owns proof verification and trace extraction. In this starter version it performs deterministic mock verification, but the boundary is intentionally shaped for real ZK verification backends.

The key function is:

```cpp
proofscope::AuditReport verify_proof_bytes(const std::vector<std::uint8_t>& proof_bytes);
```

### pybind11 Bridge

The `proofscope_engine` extension exposes the C++ verifier to Python as:

```python
proofscope_engine.verify_proof_bytes(proof_bytes)
```

It returns a dictionary matching the ProofScope audit schema.

### FastAPI Inspector

The API accepts uploaded proof artifacts, calls the verifier, validates the report with Pydantic, and returns JSON to the dashboard.

### Dashboard

The web UI is static HTML, CSS, and JavaScript served by FastAPI. It supports drag-and-drop proof uploads and renders a color-coded audit report.

## Audit Schema

The schema is versioned in `schemas/audit_report.schema.json` and includes:

- Verification result
- Proof digest
- Engine metadata
- Constraint satisfaction records
- Human-readable execution trace records

## Backend Roadmap

1. Add adapter interfaces for Groth16, PLONK, and STARK verification backends.
2. Store circuit manifests alongside proof artifacts.
3. Map circuit constraints to model-layer provenance metadata.
4. Add signed audit exports for compliance workflows.

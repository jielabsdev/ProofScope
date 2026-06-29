# ProofScope Roadmap

## Phase 1: Bridge

- Build the C++ verifier library.
- Expose verifier calls through `pybind11`.
- Keep the FastAPI layer independent from verifier internals.

## Phase 2: Logic Mapping

- Formalize the audit schema.
- Add circuit manifest parsing.
- Map constraint groups to model layers, policies, and operational controls.

## Phase 3: Dashboard

- Add report history.
- Add signed export bundles.
- Add side-by-side proof comparisons.
- Add backend-specific diagnostics for ZK-SNARK and ZK-STARK adapters.

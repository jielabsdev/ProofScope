# Contributing To ProofScope

Thanks for helping make cryptographic audit trails easier to inspect.

## Local Workflow

1. Create a virtual environment with `.\scripts\setup_dev.ps1`.
2. Run tests with `.\scripts\test.ps1`.
3. Keep changes focused and include tests for behavior changes.

## Code Style

- Python code should be typed where practical and formatted with `ruff`.
- C++ code should prefer small, testable functions and plain data structures at the engine boundary.
- Public API changes should update `schemas/audit_report.schema.json` and `docs/architecture.md`.

## Security

Do not report security issues in public issues. Use a private maintainer contact once one is published.

# Security Policy

ProofScope takes security seriously. We maintain a hardened perimeter, implement cryptographic ledger integrity, and strive to keep the verification stack secure. 

## Supported Versions

Only the latest version of ProofScope is actively supported for security updates.

| Version | Supported |
| :--- | :--- |
| 1.4.x | Yes |

## Reporting a Vulnerability

If you discover a security vulnerability in ProofScope, please report it via email. We ask that you provide a clear description of the vulnerability, the potential impact, and steps to reproduce the issue.

**Contact Email:** [jielabs.dev@gmail.com](mailto:jielabs.dev@gmail.com)

Please allow us a reasonable time to respond and address the issue before disclosing it publicly.

## Security Features
We encourage users to leverage the built-in security features:
- **Ledger Integrity:** ProofScope automatically performs cryptographic re-verification of the audit chain on startup. If tampering is detected, the system enters a fail-safe state.
- **Perimeter Hardening:** API-Key gated ingestion with strict MIME-type and size limits (10MB).
- **Isolation:** Verification engine runs in isolated subprocesses to prevent host system exposure.
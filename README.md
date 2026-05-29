# LifeCarePharmacy12 — Security Research Artifacts

IMPORTANT: This directory contains security-research artifacts and proof‑of‑concept code related to the LifeCarePharmacy12 application. All materials here are intended for defensive research, auditing, and remediation testing only.

DO NOT use these files to access or modify systems you do not own or have explicit, written authorization to test. The authors of these files and the repository owner accept no responsibility for misuse.

## Purpose
- Collect and document findings from a security review of LifeCarePharmacy12.
- Provide safe, reproducible artifacts for defensive testing in isolated lab environments.
- Record remediation recommendations for vendors and system administrators.

## Directory Contents (summary)
- `LIFECAREPHARMACY_SECURITY_AUDIT.md` — Full audit report, findings, and recommendations.
- `PHARMACY_FREE.py` — A “free edition” reimplementation/utility that demonstrates how the original app's DB operations are performed. May attempt SQL Server connections if executed.
- `PHARMACY_LOCAL.py` — Standalone SQLite-based demo GUI for local testing with seeded sample data.
- `LICENSE_BYPASS.py` — Research tool that contains examples of database/registry/binary modification approaches used during the audit. THIS FILE CAN MODIFY SYSTEM STATE (registry, DB, executables) and must NOT be run against production or third‑party systems.
- `lifecare_activate.reg`, `lifecare_reset.reg` — Registry export snippets collected during analysis.
- `requirements.txt` — Python dependencies used by some scripts.

## Intended Use
- Use these artifacts only inside an isolated, snapshot‑backed laboratory environment you control.
- Prefer the SQLite demo (`PHARMACY_LOCAL.py`) for user‑interface testing and training — it does not attempt to connect to external SQL Server instances.
- Treat `LICENSE_BYPASS.py` as analysis notes / reference only. Do not execute any part of it on systems without explicit authorization from the system owner.

## Responsible Disclosure
If you discover security issues in a third‑party product, follow a responsible disclosure process:

1. Obtain and preserve proof that demonstrates the issue on systems you control.
2. Do not exploit or exfiltrate production data or personally identifiable information (PII).
3. Contact the vendor via their security/contact address with an executive summary and reproduction steps (safe, non‑destructive).
4. Give the vendor reasonable time to respond and patch before publishing details.
5. If required, coordinate disclosure with a CERT or other authorized party.

## Remediation Recommendations (high level)
- Hash and salt all user passwords (bcrypt, Argon2, or PBKDF2); never store plaintext passwords.
- Remove hardcoded or embedded credentials from databases and configuration files.
- Encrypt backups and restrict their storage and access to authorized roles.
- Use parameterized queries / prepared statements to prevent SQL injection.
- Apply least privilege for database and Windows accounts; rotate database/SMTP/SMS credentials regularly.
- Harden application logging and audit trails; monitor for suspicious account activity.

## Precautions
The following precautions are mandatory when working with these files or reproducing the audit:

1. Authorization: Obtain explicit, written authorization before interacting with any system you do not own. Unauthorized use may be illegal.
2. Isolated Environment: Run tests in an isolated lab (VM or container) with no network access to production; take a snapshot before any changes.
3. Backups & Snapshots: Create and verify backups or VM snapshots before experimenting; be prepared to fully restore systems.
4. No Production Data: Never run audit tools against live production systems containing real customer or patient data. Use anonymized or synthetic datasets.
5. Minimize Scope: Limit tests to the specific components listed in your authorization; avoid lateral movement or data exfiltration.
6. Data Handling: Treat any discovered credentials or PII as sensitive — do not publish or share them. Sanitize artifacts before sharing.
7. Legal Counsel: If in doubt about the legality of a test, consult legal counsel or your organization's security team before proceeding.
8. Vendor Coordination: Coordinate with the vendor for remediation; provide clear, minimal reproduction steps that do not disclose secrets.
9. Monitor & Audit: Ensure activity is logged and monitored; notify stakeholders immediately if accidental access to production occurs.
10. Clean Up: After testing, remove any created accounts, restore registry or DB changes from backups, and document actions taken.

## If You Are the Vendor
If these findings apply to your product, contact the repository owner with proof of mitigation and a patch plan. Prioritize removing plaintext credentials, securing backups, and issuing updated builds.

---
This README was added to summarize the repository contents and to provide strict usage guidance and precautions for researchers and vendors.

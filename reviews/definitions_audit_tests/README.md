The seven audit tests are stored with a `.lean.txt` suffix so that the Palomar source scan, which requires every
`.lean` file in the checkout to use the module system, does not read them as package sources. They were run on
7 October 2026 as `AuditTestN.lean` at the package root, importing `Challenge`; to re-run them, copy them to the
root, drop the `.txt` suffix, and `lake env lean AuditTestN.lean`. `audit_defs.py` generated them.

"""Candidate only: index exact names from Lean defining-module metadata.

The compiler supplies membership; source hashes bind that membership to the
materialized/embedded source, and the separate axiom report supplies proof
status. Aliases never choose between distinct fully qualified names.
"""
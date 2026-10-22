"""Auditable memory: immutable inscription, append-only state and flow.

This is a local application ledger, not access to a model's hidden state/KV cache.
Hashes detect inconsistent storage; they are not an external trust anchor.

Schema v2 (12/10/2026): events store deltas, the current state is materialized
per context, every mutation is journaled before commit and the database is
copied by bytes on a mutation/time policy. A v1 database raises
``SchemaMigrationRequired`` until the explicit migration runs.
"""
from .store import (
    MemoryStore, MemoryError, InvalidInput, ContextNotFound, ScopeViolation,
    AnchorConflict, RevisionConflict, IdempotencyConflict, IntegrityError,
    ProjectionOverflow, InvariantViolation, SchemaMigrationRequired,
)
# D4 (12/10/2026): fail-closed confidentiality guard shared by sessions, app and queue.
from . import guard
from .guard import ConfidentialContent

__all__ = [
    'MemoryStore', 'MemoryError', 'InvalidInput', 'ContextNotFound',
    'ScopeViolation', 'AnchorConflict', 'RevisionConflict',
    'IdempotencyConflict', 'IntegrityError', 'ProjectionOverflow',
<<<<<<< ours
    'InvariantViolation', 'SchemaMigrationRequired',
]
=======
    'InvariantViolation', 'ConfidentialContent', 'guard',
]
>>>>>>> theirs

"""Auditable memory: immutable inscription, append-only state and flow.

This is a local application ledger, not access to a model's hidden state/KV cache.
Hashes detect inconsistent storage; they are not an external trust anchor.
"""
from .store import (
    MemoryStore, MemoryError, InvalidInput, ContextNotFound, ScopeViolation,
    AnchorConflict, RevisionConflict, IdempotencyConflict, IntegrityError,
    ProjectionOverflow, InvariantViolation,
)

__all__ = [
    'MemoryStore', 'MemoryError', 'InvalidInput', 'ContextNotFound',
    'ScopeViolation', 'AnchorConflict', 'RevisionConflict',
    'IdempotencyConflict', 'IntegrityError', 'ProjectionOverflow',
    'InvariantViolation',
]
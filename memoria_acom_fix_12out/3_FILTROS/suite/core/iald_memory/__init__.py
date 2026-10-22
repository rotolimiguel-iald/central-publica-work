"""Auditable memory: immutable inscription, append-only state and flow.

This is a local application ledger, not access to a model's hidden state/KV cache.
Hashes detect inconsistent storage; they are not an external trust anchor.
"""
from .store import (
    MemoryStore, MemoryError, InvalidInput, ContextNotFound, ScopeViolation,
    AnchorConflict, RevisionConflict, IdempotencyConflict, IntegrityError,
    ProjectionOverflow, InvariantViolation,
)
# D4 (12/10/2026): fail-closed confidentiality guard shared by sessions, app and queue.
from . import guard
from .guard import ConfidentialContent

__all__ = [
    'MemoryStore', 'MemoryError', 'InvalidInput', 'ContextNotFound',
    'ScopeViolation', 'AnchorConflict', 'RevisionConflict',
    'IdempotencyConflict', 'IntegrityError', 'ProjectionOverflow',
    'InvariantViolation', 'ConfidentialContent', 'guard',
]
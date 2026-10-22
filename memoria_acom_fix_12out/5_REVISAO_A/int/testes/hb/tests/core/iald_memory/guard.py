"""Fail-closed confidentiality guard for the common IALD memory (D4/D6, 12/10/2026).

Three layers; every refusal is visible and recorded, nothing is redacted silently:

1. NAMES  -- basename patterns after NFKC + casefold with repeated removal of
   backup/temp suffixes (`.bak_*`, `.tmp_*`, ...): `iald_psion_state*`,
   `iald_stack_v*`, `.env`, `.env.*`, `*.key`, `*.pem`; and any path component
   that starts with `escritorio` (accents stripped), i.e. the Escritório house.
2. IDENTITY -- the requested path AND `os.path.realpath` (junctions, symbolic
   links) are both name-checked; a file with more than one hard link is refused;
   `(st_dev, st_ino)` is compared with the identities of the real confidential
   files (stat only, never read); a file system without identifiers is refused.
3. CONTENT -- `scan_text` returns RULE NAMES only. The matched text is never put
   in a message, an exception or the refusal log.

Standard library only. No network. Hashes are computed, never remembered.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat as _stat
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from .store import MemoryError, ScopeViolation

__all__ = [
    'ConfidentialContent', 'confidential_basename', 'escritorio_component',
    'is_confidential_path', 'confidential_identities', 'scan_text',
    'assert_clean_text', 'assert_scope_allowed', 'log_refusal', 'fold',
    'IDENTITY_ROOTS', 'RULE_NAMES',
]

GUARD_VERSION = 'iald-memory-guard/2026-10-12'

# Folders whose real confidential files feed the identity registry (stat only).
IDENTITY_ROOTS = (
    Path(r'C:\IALD\projetos_pyhton\IALD'),
    Path(r'C:\IALD\projetos_pyhton\IALD\files'),
    Path(r'C:\IALD\MEMORIA_IALD'),
    Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923'),
)


class ConfidentialContent(MemoryError):
    """Visible refusal of confidential CONTENT. Carries rule names, never the text."""

    def __init__(self, rules, where, text_sha16=None):
        self.rules = tuple(rules)
        self.where = where
        self.text_sha16 = text_sha16
        super().__init__('confidential content refused at %s: rules=%s text_sha16=%s'
                         % (where, ','.join(self.rules), text_sha16 or '-'))


# --------------------------------------------------------------------------- names

def fold(value):
    """NFKD, strip combining marks, casefold: `Escritório` -> `escritorio` (NFC or NFD input)."""
    decomposed = unicodedata.normalize('NFKD', str(value))
    return ''.join(c for c in decomposed if not unicodedata.combining(c)).casefold()


_STRIP_SUFFIX = re.compile(r'\.(?:bak|backup|tmp|temp|orig|old|save|swp|copy)(?:[_.\-][^.]*)?\Z')
_NAME_RULES = (
    ('psion_name', re.compile(r'\Aiald_psion_state')),
    ('stack_name', re.compile(r'\Aiald_stack_v')),
    ('dotenv_name', re.compile(r'\A\.env(?:\.|\Z)')),
    ('key_name', re.compile(r'\A.+\.key(?:\.|\Z)')),
    ('pem_name', re.compile(r'\A.+\.pem(?:\.|\Z)')),
)


def normalized_basename(name):
    """Casefolded basename with backup/temp suffixes removed repeatedly."""
    base = fold(name)
    while True:
        stripped = _STRIP_SUFFIX.sub('', base)
        if stripped == base or not stripped:
            return base
        base = stripped


def confidential_basename(name):
    """Rule name when `name` (a basename) is a confidential file name, else None."""
    base = normalized_basename(name)
    for rule, pattern in _NAME_RULES:
        if pattern.search(base):
            return rule
    return None


def escritorio_component(path):
    """True when any component of `path` starts with `escritorio` (accents/case ignored)."""
    text = os.fsdecode(path) if isinstance(path, bytes) else str(path)
    for part in re.split(r'[\\/]+', text):
        if fold(part).startswith('escritorio'):
            return True
    return False


def _name_reason(path_text):
    if escritorio_component(path_text):
        return 'escritorio_path'
    tail = re.split(r'[\\/]+', path_text.rstrip('\\/'))[-1] if path_text else ''
    rule = confidential_basename(tail)
    return rule


# ------------------------------------------------------------------------ identity

def confidential_identities(roots=None):
    """{(st_dev, st_ino)} of the real confidential files under `roots` (stat only, no read)."""
    identities = set()
    for root in (roots if roots is not None else IDENTITY_ROOTS):
        try:
            entries = list(os.scandir(root))
        except OSError:
            continue
        for entry in entries:
            if confidential_basename(entry.name) is None:
                continue
            try:
                if not entry.is_file(follow_symlinks=False):
                    continue
                st = os.stat(entry.path)  # DirEntry.stat() has no st_ino/st_nlink on Windows
            except OSError:
                continue
            if st.st_ino:
                identities.add((st.st_dev, st.st_ino))
    return identities


def path_reason(path, roots=None):
    """Reason string when `path` must not be read/written through the memory, else None."""
    requested = os.fsdecode(path) if isinstance(path, bytes) else os.fspath(path)
    reason = _name_reason(requested)
    if reason:
        return reason
    try:
        real = os.path.realpath(requested, strict=False)
    except (OSError, ValueError):
        return 'realpath_failed'
    reason = _name_reason(real)
    if reason:
        return 'resolved:' + reason
    try:
        st = os.stat(real)
    except FileNotFoundError:
        return None  # nothing exists to leak; names already checked
    except OSError:
        return 'stat_failed'
    if _stat.S_ISDIR(st.st_mode):
        return None
    if not st.st_ino:
        return 'no_file_identity'
    if st.st_nlink > 1:
        return 'hardlink'
    if (st.st_dev, st.st_ino) in confidential_identities(roots):
        return 'identity_of_confidential_file'
    return None


def is_confidential_path(path, *, log_path=None, where='path', roots=None):
    """Reason (truthy) when the path is refused; None when allowed. Logs refusals."""
    reason = path_reason(path, roots)
    if reason and log_path is not None:
        text = os.fsdecode(path) if isinstance(path, bytes) else os.fspath(path)
        log_refusal(log_path, kind='path', where=where, reason=reason,
                    path_sha16=hashlib.sha256(text.encode('utf-8', 'surrogatepass')).hexdigest()[:16])
    return reason


# ------------------------------------------------------------------------- content

_CONTENT_RULES = (
    ('openai_key', re.compile(r'\bsk-[A-Za-z0-9_-]{12,}')),            # includes sk-proj-
    ('google_api_key', re.compile(r'\bAIza[0-9A-Za-z_-]{20,}')),
    ('github_token', re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}')),
    ('slack_token', re.compile(r'\bxox[abposr]-[A-Za-z0-9-]{10,}')),
    ('bearer_token', re.compile(r'\bbearer\s+[A-Za-z0-9._~+/=-]{16,}', re.I)),
    ('psion_name', re.compile(r'iald_psion_state', re.I)),
    ('stack_name', re.compile(r'iald_stack_v\d', re.I)),
    ('dotenv_name', re.compile(r'(?:\A|[\\/\s"\'`(\[{=:,;])\.env(?:\.[A-Za-z0-9_.\-]+)?(?=\Z|[\s"\'`)\]}:;,])', re.I)),
    ('key_pem_name', re.compile(r'\b[\w\-]+\.(?:key|pem)\b', re.I)),
)
# Escritório as a PATH (drive, UNC or slash-delimited component), never the loose word.
_ESCRITORIO_PATH = re.compile(r'(?:\b[a-z]:[\\/]+(?:[^\\/\s]+[\\/]+)*|\\\\[^\\/\s]+[\\/]+(?:[^\\/\s]+[\\/]+)*|[\\/])escritorio')
RULE_NAMES = tuple(name for name, _ in _CONTENT_RULES) + ('escritorio_path',)


def scan_text(text):
    """Names of the rules matched by `text` (never the matched spans)."""
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False, sort_keys=True, default=str)
    rules = [name for name, pattern in _CONTENT_RULES if pattern.search(text)]
    if _ESCRITORIO_PATH.search(fold(text)):
        rules.append('escritorio_path')
    return rules


def assert_clean_text(text, where, *, log_path=None):
    """Raise ConfidentialContent (rule names only) when `text` carries confidential content."""
    rules = scan_text(text)
    if not rules:
        return text
    raw = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False, sort_keys=True, default=str)
    sha16 = hashlib.sha256(raw.encode('utf-8', 'surrogatepass')).hexdigest()[:16]
    if log_path is not None:
        log_refusal(log_path, kind='content', where=where, rules=rules, text_sha16=sha16, text_chars=len(raw))
    raise ConfidentialContent(rules, where, sha16)


# --------------------------------------------------------------------------- scope

def assert_scope_allowed(scope):
    """D6: the Escritório house never enters the common IALD memory."""
    if isinstance(scope, dict):
        for key in ('house', 'principal'):
            if 'escritorio' in fold(scope.get(key, '')):
                raise ScopeViolation('Escritório house never enters the IALD common memory')
    return scope


# ----------------------------------------------------------------------------- log

def log_refusal(log_path, **fields):
    """Append one JSON line (never the text). A log failure never hides the refusal."""
    record = {'at': datetime.now(timezone.utc).isoformat(timespec='microseconds'),
              'guard': GUARD_VERSION, 'pid': os.getpid()}
    record.update(fields)
    try:
        path = Path(log_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as out:
            out.write(json.dumps(record, ensure_ascii=False, sort_keys=True, default=str) + '\n')
            out.flush()
            os.fsync(out.fileno())
        return True
    except OSError:
        return False

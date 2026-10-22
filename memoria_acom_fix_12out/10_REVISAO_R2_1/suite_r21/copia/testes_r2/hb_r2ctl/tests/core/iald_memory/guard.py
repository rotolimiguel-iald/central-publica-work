"""Fail-closed confidentiality guard for the common IALD memory (D4/D6, 12/10/2026; R2.1 13/10/2026).

Three layers; every refusal is visible and recorded, nothing is redacted silently:

1. NAMES  -- basename patterns on a SKELETON of the name (NFKC, format characters
   removed, casefold, common Cyrillic/Greek look-alikes and Unicode dashes mapped
   to ASCII, accents stripped) with repeated removal of backup/temp suffixes
   (`.bak_*`, `.tmp_*`, ..., trailing `~`) in LINEAR time (R2.1, review N1):
   the radicals `iald?psion?state` and `iald?stack?v` anywhere in the name,
   `.env`, `*.env`, `*.env.*`, `*.env_*`, `.envrc`, `*.key`, `*.pem` (R2.1, review N2);
   and any path component that starts with `escritorio`, i.e. the Escritório house.
2. IDENTITY -- the requested path AND `os.path.realpath` (junctions, symbolic
   links) are both name-checked; a file with more than one hard link is refused;
   `(st_dev, st_ino)` is compared with the identities of the real confidential
   files (stat only, never read); a file system without identifiers is refused.
   R2.1 (review N3): `read_checked` opens a HANDLE first (read access, without
   FILE_SHARE_DELETE, so the name cannot be unlinked or renamed while it is held),
   checks link count, identity and the FINAL path of THAT handle, and only then
   reads from the same handle: a swap of the name cannot change what is read.
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
    'IDENTITY_ROOTS', 'RULE_NAMES', 'PathRefused', 'NotRegularFile', 'read_checked', 'skeleton',
    'normalized_basename', 'path_reason',
]

GUARD_VERSION = 'iald-memory-guard/2026-10-13-r2.1'

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


# R2.1 (13/10/2026, review N2 and the review-B name gaps): the name rules run on a SKELETON of the name.
# NFKC alone does not map Cyrillic/Greek look-alikes (U+0455 'ѕ' stays 'ѕ'), so the common ones are mapped
# explicitly, Unicode dashes become '-', and format characters (zero-width, soft hyphen, bidi marks) vanish.
_DASHES = '‐‑‒–—―⁃−﹘﹣－'
_CONFUSABLE_SRC = ('аеорсухѕіјԁһӏԛԝ'
                   'үкмнтвɡıɑ'
                   'αικνορτυχϲϳ'
                   'օս')
_CONFUSABLE_DST = ('aeopcyxsijdhlqw'
                   'ykmhtbgia'
                   'aikvoptuxcj'
                   'ou')
_SKELETON_MAP = {ord(d): '-' for d in _DASHES}
_SKELETON_MAP.update({ord(c): t for c, t in zip(_CONFUSABLE_SRC, _CONFUSABLE_DST)})
assert len(_CONFUSABLE_SRC) == len(_CONFUSABLE_DST)


def skeleton(value):
    """NFKC, format characters removed, casefold, look-alikes and dashes mapped to ASCII, accents stripped."""
    text = unicodedata.normalize('NFKC', str(value))
    text = ''.join(c for c in text if unicodedata.category(c) != 'Cf').casefold().translate(_SKELETON_MAP)
    return fold(text)


_SUFFIX_WORDS = frozenset(('bak', 'backup', 'tmp', 'temp', 'orig', 'old', 'save', 'swp', 'copy'))
# One dot-free segment that is a backup/temp suffix: `bak`, `bak_20261013`, `tmp-x` ...
_SUFFIX_SEGMENT = re.compile(r'(?:bak|backup|tmp|temp|orig|old|save|swp|copy)(?:[_\-][^.]*)?')
_SEP = r'[\W_]{0,4}'
_NAME_RULES = (
    ('psion_name', re.compile(r'iald' + _SEP + r'psion' + _SEP + r'state')),      # radical, anywhere (R2.1)
    ('stack_name', re.compile(r'iald' + _SEP + r'stack' + _SEP + r'v')),           # radical, anywhere (R2.1)
    ('dotenv_name', None),                                                         # _dotenv_rule (R2.1)
    ('key_name', re.compile(r'\A.+\.key(?:\.|\Z)')),
    ('pem_name', re.compile(r'\A.+\.pem(?:\.|\Z)')),
)


# R2.1 (review N2): dotenv files by NAME. Refused: `.env`, `.envrc`, `.env<sep>...` (R2), bare `env`, `*.env`,
# `*.envrc` and `*.env<sep><tail>` (app.env.local, x.env_prod) unless <tail> ends in a DOCUMENT/CODE extension
# (the frente-3 suite keeps `envelope.env.txt` allowed: a text ABOUT an env file is not one).
_DOTENV_HEAD = re.compile(r'\A(?:\.env(?:rc)?(?:\Z|[._\-])|env\Z)')
_DOTENV_TAIL = re.compile(r'\.env(?:rc)?\Z')
_DOTENV_MID = re.compile(r'\.env(?:rc)?[._\-]')
_DOC_EXT = frozenset(('txt', 'md', 'rst', 'html', 'htm', 'pdf', 'doc', 'docx', 'odt', 'rtf', 'tex', 'csv', 'log',
                      'py', 'js', 'ts', 'sh', 'ps1', 'bat', 'png', 'jpg', 'svg'))


def _dotenv_rule(base):
    if _DOTENV_HEAD.search(base) or _DOTENV_TAIL.search(base):
        return True
    last_dot = base.rfind('.')
    last_ext = base[last_dot + 1:]
    for m in _DOTENV_MID.finditer(base):
        # the extension of the tail is the extension of the whole name, unless the tail has no dot (linear)
        ext = last_ext if last_dot >= m.end() else base[m.end():]
        if ext not in _DOC_EXT:
            return True
    return False


def normalized_basename(name):
    r"""Skeleton of the basename with backup/temp suffixes (and trailing '~') removed repeatedly.

    R2.1 (review N1): same decision as the R2 loop `re.sub(r'\.(?:bak|...)(?:[_.\-][^.]*)?\Z', '', base)` repeated
    until stable (plus trailing '~'), but walking back from the end over at most the last two dot segments per
    step: every character is visited a bounded number of times, so the cost is LINEAR in the name (the R2 loop
    re-scanned the whole name once per suffix: 32 KB of '.bak' took seconds).
    """
    base = skeleton(name)
    end = len(base)
    while end > 0:
        tilde = end
        while tilde > 0 and base[tilde - 1] == '~':
            tilde -= 1
        if tilde != end:
            if tilde == 0:
                break
            end = tilde
            continue
        p1 = base.rfind('.', 0, end)
        if p1 < 0:
            break
        cut = None
        p2 = base.rfind('.', 0, p1)
        if p2 >= 0 and base[p2 + 1:p1] in _SUFFIX_WORDS:
            cut = p2        # '.<word>.<rest without dot>' (the leftmost match of the R2 pattern)
        elif _SUFFIX_SEGMENT.fullmatch(base, p1 + 1, end):
            cut = p1        # '.<word>' or '.<word>[_-]<rest without dot>'
        if cut is None or cut == 0:
            break           # nothing to strip, or the whole name is a suffix (kept, as in R2)
        end = cut
    return base[:end]


def confidential_basename(name):
    """Rule name when `name` (a basename) is a confidential file name, else None."""
    base = normalized_basename(name)
    for rule, pattern in _NAME_RULES:
        if (_dotenv_rule(base) if pattern is None else pattern.search(base)):
            return rule
    return None


def escritorio_component(path):
    """True when any component of `path` starts with `escritorio` (accents/case ignored)."""
    text = os.fsdecode(path) if isinstance(path, bytes) else str(path)
    for part in re.split(r'[\\/]+', text):
        if skeleton(part).startswith('escritorio'):
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


# ------------------------------------------------------------------- guarded read

class PathRefused(MemoryError):
    """Visible refusal of a PATH by the guard. Carries the rule name, never the bytes."""

    def __init__(self, reason, where):
        self.reason = reason
        self.where = where
        super().__init__('path refused at %s: %s' % (where, reason))


class NotRegularFile(MemoryError):
    """The path names a directory, a device or another non-regular object (nothing was read)."""


_WIN = None


def _win():
    """kernel32 entry points used by read_checked (lazy; Windows only)."""
    global _WIN
    if _WIN is None:
        import ctypes
        from ctypes import wintypes
        k = ctypes.WinDLL('kernel32', use_last_error=True)
        k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                                  wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        k.CreateFileW.restype = wintypes.HANDLE
        k.GetFinalPathNameByHandleW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
        k.GetFinalPathNameByHandleW.restype = wintypes.DWORD
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CloseHandle.restype = wintypes.BOOL
        _WIN = (ctypes, k)
    return _WIN


def _win_invalid(handle):
    return handle is None or handle == 0 or handle == (1 << 64) - 1 or handle == -1


def _win_final_path(ctypes, k, handle):
    size = 1024
    while True:
        buf = ctypes.create_unicode_buffer(size)
        n = k.GetFinalPathNameByHandleW(handle, buf, size, 0)   # FILE_NAME_NORMALIZED | VOLUME_NAME_DOS
        if n == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        if n < size:
            text = buf.value
            break
        size = n + 1
    if text.startswith('\\\\?\\UNC\\'):
        return '\\\\' + text[8:]
    if text.startswith('\\\\?\\'):
        return text[4:]
    return text


def _refuse(reason, path_text, where, log_path):
    if log_path is not None:
        log_refusal(log_path, kind='path', where=where, reason=reason,
                    path_sha16=hashlib.sha256(path_text.encode('utf-8', 'surrogatepass')).hexdigest()[:16])
    raise PathRefused(reason, where)


def _handle_checks(st, final_text, roots):
    if not _stat.S_ISREG(st.st_mode):
        return 'not_regular'
    if not st.st_ino:
        return 'no_file_identity'
    if st.st_nlink > 1:
        return 'hardlink'
    if (st.st_dev, st.st_ino) in confidential_identities(roots):
        return 'identity_of_confidential_file'
    reason = _name_reason(final_text)
    if reason:
        return 'final:' + reason
    return None


def read_checked(path, *, max_bytes, log_path=None, where='read', roots=None):
    """Read a file only after the guard accepted the very file object that is read. Returns (final_path, bytes).

    R2.1 (review N3, TOCTOU): R2 checked the NAME (name, realpath, st_nlink, identity) and then opened by name,
    so a hard link swapped in between was read. Here: (1) the requested and resolved names are checked BEFORE any
    open (a confidential name is never opened); (2) on Windows a handle is opened with READ access and WITHOUT
    FILE_SHARE_DELETE: while it is held nobody can unlink or rename that name (an attributes-only handle does
    not take part in sharing checks: the first R2.1 draft used one and the swap test still read the canary
    13 times, because the link was removed between the open and the link count); (3) link count, file identity
    and the FINAL path of that handle are checked, no byte read yet; (4) only then the bytes are read from the
    SAME handle, never through the name. At most `max_bytes + 1` bytes are read, so the caller can refuse an
    oversized file without reading it all.
    Raises PathRefused (rule name only), NotRegularFile, or the OSError of the open (e.g. FileNotFoundError).
    """
    requested = os.fsdecode(path) if isinstance(path, bytes) else os.fspath(path)
    reason = _name_reason(requested)
    if reason:
        _refuse(reason, requested, where, log_path)
    try:
        real = os.path.realpath(requested, strict=False)
    except (OSError, ValueError):
        _refuse('realpath_failed', requested, where, log_path)
    reason = _name_reason(real)
    if reason:
        _refuse('resolved:' + reason, requested, where, log_path)
    if os.name != 'nt':
        flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_CLOEXEC', 0)
        fd = os.open(real, flags)
        with os.fdopen(fd, 'rb') as stream:
            st = os.fstat(stream.fileno())
            if _stat.S_ISDIR(st.st_mode):
                raise NotRegularFile('directory')
            reason = _handle_checks(st, real, roots)
            if reason == 'not_regular':
                raise NotRegularFile('not_regular')
            if reason:
                _refuse(reason, requested, where, log_path)
            return real, stream.read(max_bytes + 1)
    import msvcrt
    ctypes, k = _win()
    target = os.path.abspath(real)
    if len(target) > 240 and not target.startswith('\\\\?\\'):
        target = '\\\\?\\UNC\\' + target[2:] if target.startswith('\\\\') else '\\\\?\\' + target
    FILE_READ_ATTRIBUTES, GENERIC_READ = 0x80, 0x80000000
    SHARE_READ_WRITE = 0x1 | 0x2                 # no FILE_SHARE_DELETE: no rename/delete while held
    OPEN_EXISTING, BACKUP_SEMANTICS = 3, 0x02000000
    handle = k.CreateFileW(target, GENERIC_READ | FILE_READ_ATTRIBUTES, SHARE_READ_WRITE, None, OPEN_EXISTING,
                           BACKUP_SEMANTICS, None)
    if _win_invalid(handle):
        raise ctypes.WinError(ctypes.get_last_error())
    attr_fd = None
    try:
        try:
            final_text = _win_final_path(ctypes, k, handle)
        except OSError:
            _refuse('final_path_failed', requested, where, log_path)
        attr_fd = msvcrt.open_osfhandle(handle, os.O_RDONLY | getattr(os, 'O_BINARY', 0))
        st = os.fstat(attr_fd)                   # link count and identity OF THE HANDLE (no byte read yet)
        if _stat.S_ISDIR(st.st_mode):
            raise NotRegularFile('directory')
        reason = _handle_checks(st, final_text, roots)
        if reason == 'not_regular':
            raise NotRegularFile('not_regular')
        if reason:
            _refuse(reason, requested, where, log_path)
        with os.fdopen(attr_fd, 'rb') as stream:  # the SAME handle; the stream owns and closes it
            attr_fd = -1
            return final_text, stream.read(max_bytes + 1)
    finally:
        if attr_fd is None:
            k.CloseHandle(handle)
        elif attr_fd >= 0:
            os.close(attr_fd)                    # closes `handle`


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
    ('key_pem_name', None),   # R2: linear scanner _key_pem_name (the regex was quadratic on '-'-joined words)
)
# Escritório as a PATH (drive, UNC or slash-delimited component), never the loose word.
# R2 (13/10/2026, review finding 2): the R1 pattern
#   (?:\b[a-z]:[\\/]+(?:[^\\/\s]+[\\/]+)*|\\\\[^\\/\s]+[\\/]+(?:[^\\/\s]+[\\/]+)*|[\\/])escritorio
# re-scanned the rest of the text from every drive letter (quadratic: 240 KB of compact JSON with 4,000
# Windows paths took 71 s inside the app lock). Its first two alternatives always end in a slash right
# before `escritorio`, so the whole pattern has the same truth value as `[\\/]escritorio`. R2 keeps that and
# adds two path forms R1 missed: drive-relative `c:escritorio` and percent-encoded separators (`%5c`, `%2f`).
# Every alternative has a fixed length, so the search is linear in the text.
_ESCRITORIO_PATH = re.compile(r'(?:[\\/]|%5c|%2f|\b[a-z]:)escritorio')
_KEY_PEM_EXT = re.compile(r'\.(?:key|pem)\b', re.I)
_WORD_CHAR = re.compile(r'\w')
RULE_NAMES = tuple(name for name, _ in _CONTENT_RULES) + ('escritorio_path',)


def _key_pem_name(text):
    r"""Same truth value as r'\b[\w\-]+\.(?:key|pem)\b' (re.I), in linear time.

    That pattern matches iff the maximal run of [\w-] right before some `.key`/`.pem` (followed by a word
    boundary) contains a word character. Walk back from each extension over hyphens only: every walk stops
    at the first word character (match) or at the first character outside the run, so the walks are disjoint.
    """
    for m in _KEY_PEM_EXT.finditer(text):
        i = m.start() - 1
        while i >= 0:
            ch = text[i]
            if _WORD_CHAR.match(ch):
                return True
            if ch != '-':
                break
            i -= 1
    return False


def scan_text(text):
    """Names of the rules matched by `text` (never the matched spans). Linear time in len(text) (R2)."""
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False, sort_keys=True, default=str)
    rules = []
    for name, pattern in _CONTENT_RULES:
        hit = _key_pem_name(text) if pattern is None else pattern.search(text) is not None
        if hit:
            rules.append(name)
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

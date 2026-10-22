# -*- coding: utf-8 -*-
"""R2.1: acrescenta read_checked (abre o handle antes de checar; caminho final do handle) ao guard.py do candidato."""
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'candidato_r2_1' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / 'guard.py'
s = P.read_bytes().decode('utf-8')
anchor = "# ------------------------------------------------------------------------- content"
assert s.count(anchor) == 1
assert 'def read_checked' not in s
new = r'''# ------------------------------------------------------------------- guarded read

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
        k.ReOpenFile.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD]
        k.ReOpenFile.restype = wintypes.HANDLE
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
    open (a confidential name is never opened); (2) on Windows a handle is opened with FILE_READ_ATTRIBUTES only
    (no data access) and without FILE_SHARE_DELETE (the name cannot be renamed or deleted while it is held);
    (3) link count, file identity and the FINAL path of that handle are checked; (4) only then the same file
    object is reopened for reading (ReOpenFile), never the name. At most `max_bytes + 1` bytes are read, so the
    caller can refuse an oversized file without reading it all.
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
    handle = k.CreateFileW(target, FILE_READ_ATTRIBUTES, SHARE_READ_WRITE, None, OPEN_EXISTING, BACKUP_SEMANTICS, None)
    if _win_invalid(handle):
        raise ctypes.WinError(ctypes.get_last_error())
    attr_fd = None
    try:
        try:
            final_text = _win_final_path(ctypes, k, handle)
        except OSError:
            _refuse('final_path_failed', requested, where, log_path)
        attr_fd = msvcrt.open_osfhandle(handle, os.O_RDONLY)
        st = os.fstat(attr_fd)                   # link count and identity OF THE HANDLE
        if _stat.S_ISDIR(st.st_mode):
            raise NotRegularFile('directory')
        reason = _handle_checks(st, final_text, roots)
        if reason == 'not_regular':
            raise NotRegularFile('not_regular')
        if reason:
            _refuse(reason, requested, where, log_path)
        data_handle = k.ReOpenFile(handle, GENERIC_READ, SHARE_READ_WRITE, 0)
        if _win_invalid(data_handle):
            raise ctypes.WinError(ctypes.get_last_error())
        data_fd = msvcrt.open_osfhandle(data_handle, os.O_RDONLY | getattr(os, 'O_BINARY', 0))
        with os.fdopen(data_fd, 'rb') as stream:
            return final_text, stream.read(max_bytes + 1)
    finally:
        if attr_fd is not None:
            os.close(attr_fd)                    # closes `handle`
        else:
            k.CloseHandle(handle)


'''
s = s.replace(anchor, new + anchor)
P.write_bytes(s.encode('utf-8'))
print('ok', P.stat().st_size)

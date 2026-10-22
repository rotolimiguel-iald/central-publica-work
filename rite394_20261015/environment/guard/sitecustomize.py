"""Python-side IO guard for the unmodified full rite and its Python children.

This is NOT an OS sandbox: native Lean/Lake/MiKTeX processes are constrained by
their explicit executable paths, working directory and local/offline settings.
No scientific functions, inputs, results, global flags or imports are replaced.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

_ROOT = Path(os.environ["TGL_RITE_SANDBOX"]).resolve()
_PHASE = os.environ.get("TGL_RITE_GUARD_PHASE", "actual")
if _PHASE not in {"actual", "preflight"}:
    raise RuntimeError("Invalid guard phase")
_LOGDIR = _ROOT / "environment" / "guard_logs" / _PHASE
_LOGDIR.mkdir(parents=True, exist_ok=True)
_FD = os.open(_LOGDIR / ("audit_%d.jsonl" % os.getpid()), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
_BUSY = False
_SEEN_READS = set()
_TRUSTED = {
    os.path.normcase(os.path.abspath(sys.executable)),
    os.path.normcase(os.path.abspath(os.environ["TGL_LAKE"])),
    os.path.normcase(os.path.abspath(str(Path(os.environ["TGL_LAKE"]).with_name("lean.exe")))),
    os.path.normcase(os.path.abspath(r"C:\Users\rotol\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe")),
}
_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND


def _log(kind, **kwargs):
    os.write(_FD, (json.dumps({"time_ns": time.time_ns(), "pid": os.getpid(),
                              "kind": kind, **kwargs}, ensure_ascii=False) + "\n").encode())


def _path(value):
    if isinstance(value, int):
        return None
    if isinstance(value, bytes):
        value = os.fsdecode(value)
    return Path(value).resolve()


def _inside(value):
    p = _path(value)
    return p is None or p.is_relative_to(_ROOT)


def _refuse(event, args, reason):
    _log("REFUSAL", event=event, arguments=repr(args)[:3000], reason=reason)
    raise PermissionError("Full rite IO guard: " + reason)


def _record_external_read(value):
    global _BUSY
    p = _path(value)
    if p is None or p.is_relative_to(_ROOT):
        return
    # Record the scientific historical inputs; standard-library/DLL reads are
    # environment dependencies, not claimed scientific evidence.
    if not str(p).lower().startswith("c:\\iald\\") or not p.is_file():
        return
    key = os.path.normcase(str(p))
    if key in _SEEN_READS:
        return
    _BUSY = True
    try:
        st = p.stat()
        with p.open("rb") as f:
            h = hashlib.file_digest(f, "sha256").hexdigest()
        _log("EXTERNAL_READ_BEFORE", path=str(p), sha256=h, bytes=st.st_size,
             mtime_ns=st.st_mtime_ns)
        _SEEN_READS.add(key)
    finally:
        _BUSY = False


def _audit(event, args):
    if _BUSY:
        return
    if event == "open":
        path, mode, flags = args
        if isinstance(path, (str, bytes)) and os.fsdecode(path).upper() in {"NUL", "\\\\.\\NUL"}:
            return
        writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or bool(flags & _WRITE_FLAGS)
        if writing and not _inside(path):
            _refuse(event, args, "write outside sandbox")
        if not writing:
            # v376 intentionally reads the Coma revelation from 19 Aug 2026.
            # The old v36/v39 path still receives TGL_COMA_REVEAL=0. This is
            # historical replay, not a new opening; both are retained.
            _record_external_read(path)
    elif event in {"os.remove", "os.rmdir", "os.mkdir", "os.chmod", "os.utime", "os.truncate"}:
        if not _inside(args[0]):
            _refuse(event, args, "mutation outside sandbox")
    elif event in {"os.rename", "os.replace", "os.link", "os.symlink"}:
        if event == "os.symlink" or not all(_inside(x) for x in args[:2]):
            _refuse(event, args, "link or cross-boundary mutation refused")
    elif event in {"socket.connect", "socket.connect_ex", "socket.bind", "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr"}:
        _refuse(event, args, "network access refused")
    elif event in {"os.system", "os.startfile", "os.startfile/2"}:
        _refuse(event, args, "shell or application launch refused")
    elif event == "subprocess.Popen":
        exe, argv, cwd, _env = args
        # On Windows CPython emits executable=None plus its quoted command line.
        first = re.match(r'^(?:"([^"]+)"|(\S+))', argv) if isinstance(argv, str) else None
        resolved_exe = exe or ((first.group(1) or first.group(2)) if first else argv[0])
        name = os.path.normcase(os.path.abspath(os.fsdecode(resolved_exe)))
        if name not in _TRUSTED:
            _refuse(event, args[:3], "executable not on the explicit allowlist")
        if cwd is not None and not _inside(cwd):
            _refuse(event, args[:3], "child working directory outside sandbox")
        tokens = list(argv) if isinstance(argv, (list, tuple)) else [str(argv)]
        full_gpu_run = ("run" in tokens if not isinstance(argv, str)
                        else bool(re.search(r'--mode\s+"?run"?(?:\s|$)', argv)))
        if any("pilar_quantico_worker.py" in str(x) for x in tokens) and full_gpu_run:
            _refuse(event, args[:3], "full GPU recomputation requires a separate resource decision; reuse/selftest allowed")
        _log("PROCESS", executable=str(resolved_exe), argv=argv, cwd=str(cwd))


sys.addaudithook(_audit)
_log("GUARD_ACTIVE", sandbox=str(_ROOT), python=sys.version,
     scope="Python audit events only; not native OS containment")

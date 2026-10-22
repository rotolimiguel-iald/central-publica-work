# -*- coding: utf-8 -*-
# GUARDA DO AUDITOR c1 (E_ACOM). Carregado por PYTHONPATH em todo processo de teste (pai e filhos).
# Recusa: rede; escrita/remocao/renomeacao fora da pasta do auditor; sqlite gravavel fora dela; leitura de confidenciais
# (iald_stack_v7.py, iald_psion_state.json, .env*) e de qualquer caminho sob C:\Escritorio; subprocesso que nao seja Python.
# Registra tudo em guard_log/<pid>.jsonl. Nao altera nada fora da pasta do auditor.
import os, sys, json, time
_ROOT = os.environ.get("ACOM_AUDIT_ROOT", "")
if _ROOT:
    _ALLOWED = [os.path.normcase(os.path.abspath(_ROOT))]
    _ALLOWED.append("\\\\?\\" + _ALLOWED[0])
    _LOG = os.path.join(_ROOT, "guard_log", "guard_%d.jsonl" % os.getpid())
    _busy = [False]
    _seen_reads = set()
    _CONF = ("iald_stack_v7.py", "iald_psion_state.json")
    def _norm(p):
        try:
            return os.path.normcase(os.path.abspath(os.fsdecode(p)))
        except Exception:
            return None
    def _inside(n):
        return n is not None and any(n == a or n.startswith(a + os.sep) for a in _ALLOWED)
    def _is_null(n):
        return n is not None and os.path.basename(n) in ("nul",) or (n or "").endswith("\\.\nul")
    def _log(kind, **kw):
        if _busy[0]:
            return
        _busy[0] = True
        try:
            with open(_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(dict(t=time.time(), pid=os.getpid(), kind=kind, **kw), ensure_ascii=False, default=str) + "\n")
        except Exception:
            pass
        finally:
            _busy[0] = False
    def _confidential(n):
        if n is None:
            return False
        b = os.path.basename(n)
        if b in _CONF or b == ".env" or b.startswith(".env."):
            return True
        parts = [x for x in n.replace("/", "\\").split("\\") if x]
        return any(x in ("escritorio", "escritório") for x in parts)
    _STD = tuple(sorted({os.path.normcase(os.path.abspath(x)) + os.sep for x in (sys.base_prefix, sys.prefix, sys.exec_prefix)}))
    _W = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
    def _hook(event, args):
        if _busy[0]:
            return
        try:
            if event == "open":
                path, mode, flags = (list(args) + [None, None, None])[:3]
                if isinstance(path, int) or path is None:
                    return
                n = _norm(path)
                write = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (isinstance(flags, int) and (flags & _W))
                if _confidential(n):
                    _log("BLOCK_CONFIDENTIAL_OPEN", path=n, mode=mode)
                    raise PermissionError("auditor guard: confidential path refused")
                if write and not _inside(n) and not _is_null(n):
                    _log("BLOCK_WRITE_OUTSIDE", path=n, mode=mode, flags=flags)
                    raise PermissionError("auditor guard: write outside audit root refused")
                if not write and not _inside(n) and n not in _seen_reads and not any(n.startswith(x) for x in _STD):
                    _seen_reads.add(n)
                    _log("READ_OUTSIDE", path=n)
            elif event in ("os.remove", "os.rmdir", "os.mkdir", "os.truncate", "os.chmod", "os.utime", "shutil.rmtree"):
                p = args[0]
                if isinstance(p, int):
                    return
                n = _norm(p)
                if not _inside(n):
                    _log("BLOCK_MUTATION_OUTSIDE", event=event, path=n)
                    raise PermissionError("auditor guard: mutation outside audit root refused")
            elif event in ("os.rename", "os.link", "os.symlink", "shutil.copyfile", "shutil.copytree", "shutil.move"):
                a, b = args[0], args[1]
                na, nb = _norm(a), _norm(b)
                if not _inside(nb) or (event in ("os.rename", "shutil.move") and not _inside(na)):
                    _log("BLOCK_MUTATION_OUTSIDE", event=event, src=na, dst=nb)
                    raise PermissionError("auditor guard: mutation outside audit root refused")
                if _confidential(na):
                    _log("BLOCK_CONFIDENTIAL_COPY", event=event, src=na)
                    raise PermissionError("auditor guard: confidential copy refused")
            elif event == "sqlite3.connect":
                db = args[0] if args else None
                s = os.fsdecode(db) if db is not None and not isinstance(db, int) else str(db)
                if s in (":memory:", "") or s.startswith("file::memory:"):
                    return
                if s.startswith("file:"):
                    ro = ("mode=ro" in s) or ("immutable=1" in s)
                    path = s[5:].split("?", 1)[0]
                    if path.startswith("///"):
                        path = path[3:]
                    from urllib.parse import unquote
                    n = _norm(unquote(path))
                else:
                    ro = False; n = _norm(s)
                if _confidential(n):
                    _log("BLOCK_CONFIDENTIAL_SQLITE", path=n)
                    raise PermissionError("auditor guard: confidential sqlite refused")
                if not _inside(n):
                    if ro:
                        _log("SQLITE_RO_OUTSIDE", path=n)
                    else:
                        _log("BLOCK_SQLITE_RW_OUTSIDE", path=n)
                        raise PermissionError("auditor guard: writable sqlite outside audit root refused")
            elif event in ("socket.connect", "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr", "socket.bind", "socket.sendto", "socket.sendmsg"):
                _log("BLOCK_NETWORK", event=event, args=repr(args)[:300])
                raise PermissionError("auditor guard: network refused")
            elif event == "subprocess.Popen":
                exe, argv = args[0], args[1]
                if exe:
                    first = os.fsdecode(exe)
                elif isinstance(argv, (list, tuple)) and argv:
                    first = os.fsdecode(argv[0])
                else:
                    cl = os.fsdecode(argv) if isinstance(argv, (bytes, str)) else str(argv)
                    cl = cl.strip()
                    if cl.startswith('"'):
                        first = cl[1:].split('"', 1)[0]
                    else:
                        first = cl.split(None, 1)[0] if cl else ""
                ok = os.path.normcase(os.path.abspath(first)) == os.path.normcase(os.path.abspath(sys.executable)) if first else False
                _log("SUBPROCESS", ok=ok, argv=repr(argv)[:600], cwd=str(args[2]) if len(args) > 2 else None)
                if not ok:
                    raise PermissionError("auditor guard: non-python subprocess refused")
            elif event in ("os.system", "os.exec", "os.spawn", "os.posix_spawn"):
                _log("BLOCK_SIDE_EFFECT", event=event, args=repr(args)[:300])
                raise PermissionError("auditor guard: shell/exec refused")
            elif event in ("os.startfile", "webbrowser.open", "winreg.CreateKey", "winreg.DeleteKey", "winreg.DeleteValue", "winreg.SetValue", "winreg.CreateKeyEx", "winreg.DeleteKeyEx"):
                _log("BLOCK_SIDE_EFFECT", event=event, args=repr(args)[:300])
                raise PermissionError("auditor guard: side effect refused")
            elif event == "ctypes.dlopen":
                _log("CTYPES_DLOPEN", name=repr(args)[:200])
        except PermissionError:
            raise
        except Exception as exc:
            _log("GUARD_INTERNAL", event=event, err=repr(exc)[:300])
    sys.addaudithook(_hook)
    _log("GUARD_ON", argv=sys.argv, exe=sys.executable)

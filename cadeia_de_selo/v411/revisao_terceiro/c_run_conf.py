# roda o conferir_rito_v411.py REAL, em processo, com os WRITES sob a pasta da cadeia redirecionados para C:\t\k411c\revisao_C\redir
import sys, os, io, builtins, runpy, json, time
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
REDIR = r"C:\t\k411c\revisao_C\redir"
nos, suf = sys.argv[1], sys.argv[2]
extra = sys.argv[3:]
os.environ["V411_NOS"] = nos
os.makedirs(REDIR, exist_ok=True)
_open = builtins.open; _iopen = io.open
low = V.lower()
def red(p):
    ap = os.path.abspath(os.fspath(p))
    if ap.lower().startswith(low):
        r = os.path.join(REDIR, os.path.relpath(ap, V)); os.makedirs(os.path.dirname(r), exist_ok=True); return r
    return p
def myopen(file, mode="r", *a, **k):
    if isinstance(file, (str, bytes, os.PathLike)) and any(c in mode for c in "wax+"):
        file = red(file)
    return _open(file, mode, *a, **k)
builtins.open = myopen; io.open = myopen
_rep = os.replace
def myrep(s, d, *a, **k):
    return _rep(red(s), red(d), *a, **k)
os.replace = myrep
_mk = os.makedirs
sys.argv = [V + r"\conferir_rito_v411.py", suf] + extra
sys.path.insert(0, V); os.chdir(V)
sys.dont_write_bytecode = True
t0 = time.time()
try:
    runpy.run_path(V + r"\conferir_rito_v411.py", run_name="__main__")
    rc = 0
except SystemExit as e:
    rc = e.code
print("WRAPPER rc=%s %.1fs" % (rc, time.time() - t0))

# -*- coding: utf-8 -*-
"""/api/organismo/medir: o subprocesso do medidor sem janela de console sob pythonw (achado do agente da Torre, 24/10). Troca contada; backup; py_compile."""
import os, py_compile, time
from pathlib import Path
P = Path("C:/IALD/Central de Patentes/backend/app/main.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
A = "        r = _sp.run(args, capture_output=True, timeout=900, cwd=str(C.CENTRAL))"
B = '        r = _sp.run(args, capture_output=True, timeout=900, cwd=str(C.CENTRAL), creationflags=getattr(_sp, "CREATE_NO_WINDOW", 0))   # sem janela sob pythonw'
if B in s:
    raise SystemExit("ja aplicado")
assert s.count(A) == 1, s.count(A)
s = s.replace(A, B)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("organismo_medir: sem janela | %d -> %d" % (len(raw), P.stat().st_size))

# -*- coding: utf-8 -*-
"""O medidor confere a release de ciência do APP (iald_nucleo_fixo.json: operational_core.current_release) contra o selo (24/10/2026)."""
import os, py_compile, time
from pathlib import Path
P = Path("C:/IALD/Central de Patentes/tools/estado_do_organismo.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
if "iald_nucleo_fixo.json" in s:
    raise SystemExit("ja aplicado")
A = '    item("Memória canônica (fila/app)", "ACTIVE.json release = selo corrente", V, rel, rel == V)\n'
B = ('    item("Memória canônica (fila)", "ACTIVE.json release = selo corrente", V, rel, rel == V)\n'
     '    # 24/10/2026: o APP tem pacote de ciência próprio (iald_nucleo_fixo.json), fora da cadeia até a release entrar nela (G1)\n'
     '    nuc = Path("C:/IALD/projetos_pyhton/IALD/iald_nucleo_fixo.json")\n'
     '    try:\n'
     '        nj = json.loads(nuc.read_text(encoding="utf-8", errors="replace"))\n'
     '        rel_app = str(((nj.get("operational_core") or {}).get("current_release")) or ((nj.get("active_cluster") or {}).get("release")) or "?")\n'
     '    except Exception as e:  # noqa: BLE001\n'
     '        rel_app = "sem leitura (%s)" % type(e).__name__\n'
     '    item("App IALD (ciência própria)", "release instalada no app = selo corrente (release do app: pipeline work/iald_vNNN_*/app)", V, rel_app, rel_app == V)\n')
assert s.count(A) == 1, s.count(A)
s = s.replace(A, B)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("estado_do_organismo.py: item do app instalado | %d -> %d bytes" % (len(raw), P.stat().st_size))

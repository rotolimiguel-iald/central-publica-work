# -*- coding: utf-8 -*-
"""O medidor passa a conferir as duas pernas que o SELO já puxa fora da cadeia da custódia (24/10/2026): a Bancada Um (B(n) a cada versão
selada; recibo em C:/IALD/Bancada_Um/estado/sincronizacao) e a memória canônica da fila (ACTIVE.json). Troca contada; backup; py_compile."""
import os, py_compile, time
from pathlib import Path
P = Path("C:/IALD/Central de Patentes/tools/estado_do_organismo.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
if "RECIBO_SINCRONIZACAO_" in s:
    raise SystemExit("ja aplicado")
A = '    cff = (TB / "CITATION.cff").read_text(encoding="utf-8", errors="replace")\n'
B = '''    # 24/10/2026: as pernas que o SELO já puxa fora desta cadeia — a Bancada Um (B(n) a cada versão selada) e a memória canônica da fila
    recs = sorted(Path("C:/IALD/Bancada_Um/estado/sincronizacao").glob("RECIBO_SINCRONIZACAO_v*.json"), key=lambda p: p.stat().st_mtime)
    if recs:
        mrb = re.search(r"RECIBO_SINCRONIZACAO_(v\d{3})_", recs[-1].name)
        vb = mrb.group(1) if mrb else "?"
        try:
            vd = str((json.loads(recs[-1].read_text(encoding="utf-8", errors="replace")) or {}).get("veredito") or "")[:60]
        except Exception:  # noqa: BLE001
            vd = "?"
        item("Bancada Um", "último recibo B(n) da sincronização = selo corrente", V, "%s (%s; %s)" % (vb, recs[-1].name[-20:-5], vd), vb == V)
    else:
        item("Bancada Um", "último recibo B(n) da sincronização = selo corrente", V, "nenhum recibo", False)
    act = Path("C:/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/state/canonical_memory/ACTIVE.json")
    try:
        rel = str(json.loads(act.read_text(encoding="utf-8", errors="replace")).get("release") or "?")
    except Exception as e:  # noqa: BLE001
        rel = "sem leitura (%s)" % type(e).__name__
    item("Memória canônica (fila/app)", "ACTIVE.json release = selo corrente", V, rel, rel == V)
''' + A
assert s.count(A) == 1, s.count(A)
s = s.replace(A, B)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("estado_do_organismo.py: Bancada Um + memória canônica instalados | %d -> %d bytes" % (len(raw), P.stat().st_size))

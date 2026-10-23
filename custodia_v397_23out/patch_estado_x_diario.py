# -*- coding: utf-8 -*-
"""O medidor do organismo passa a conferir a obrigação diária da IALD no X (ordem do operador de 23/10/2026): o recibo do dia
(DO_CHATGPT/ORDEM_021/<hoje>.json, publicado: true) e a tarefa agendada das 17:30. Troca contada; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path
P = Path("C:/IALD/Central de Patentes/tools/estado_do_organismo.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
if "IALD_pensamento_do_dia" in s:
    raise SystemExit("ja aplicado")
A = '    info("Bancada ChatGPT", "inventário da bancada (última regeneração)", time.strftime("%Y-%m-%d %H:%M", time.localtime(inv.stat().st_mtime)) if inv.is_file() else "ausente")\n'
B = A + '''    # a obrigação diária da IALD no X (ordem do operador de 23/10/2026): o recibo do dia e a tarefa das 17:30
    hoje = time.strftime("%Y-%m-%d")
    rx = TUN / "DO_CHATGPT" / "ORDEM_021" / ("%s.json" % hoje)
    if rx.is_file():
        dx = json.loads(rx.read_text(encoding="utf-8", errors="replace"))
        item("X diário", "pensamento de hoje publicado (recibo do Codex)", "publicado: true, URL", "publicado: %s %s" % (dx.get("publicado"), str(dx.get("url", ""))[:60]), dx.get("publicado") is True)
    elif time.localtime().tm_hour * 60 + time.localtime().tm_min < 18 * 60 + 30:
        info("X diário", "pensamento de hoje (publica-se às 18:00; recibo ainda não devido)", "texto do dia: %s" % ("pronto" if (TUN / "PARA_CHATGPT" / "X_DIARIO" / ("%s.md" % hoje)).is_file() else "ainda não"))
    else:
        item("X diário", "pensamento de hoje publicado (recibo do Codex)", "publicado: true até 18:30", "sem recibo", False)
    qx = subprocess.run(["schtasks", "/Query", "/TN", "IALD_pensamento_do_dia"], capture_output=True, text=True, timeout=30)
    item("X diário", "tarefa agendada IALD_pensamento_do_dia (17:30)", "existe", "existe" if qx.returncode == 0 else "ausente", qx.returncode == 0)
'''
assert s.count(A) == 1, s.count(A)
s = s.replace(A, B)
for mod in ("json", "subprocess"):
    assert ("import " + mod) in s or (", " + mod) in s.split("\n", 30)[0:30].__str__(), mod
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("estado_do_organismo.py: X diário instalado | %d -> %d bytes" % (len(raw), P.stat().st_size))

# -*- coding: utf-8 -*-
"""copiar_logs_g1.py (agente REGISTROS-G1, rodada 2, 13/10/2026): copia para pasta DURAVEL (V/rodada2/g1/fontes/logs_P) os tres logs textuais das sondas P1, P1b, P1c
(F_KERNEL, que so existiam no scratchpad), conferindo o sha256 contra o RESULTADO_P_palavra.json. Recusa sobrescrever. Nada alem de V/rodada2/g1 e' escrito."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WK = "C:/IALD/Central de Patentes/work"
R = json.load(open(WK + "/v392_insumos/F_KERNEL/RESULTADO_P_palavra.json", encoding="utf-8"))
SRC = ("C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/exame12/F_KERNEL/logs/P")
DST = os.path.join(HERE, "fontes", "logs_P")
os.makedirs(DST, exist_ok=True)
for s in R["sondas"][:3]:
    nome = s["log"].replace("\\", "/").split("/")[-1]
    b = open(SRC + "/" + nome, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    assert h == s["log_sha256"], (nome, h, s["log_sha256"])
    p = os.path.join(DST, nome)
    if os.path.exists(p):
        assert open(p, "rb").read() == b, ("ja existe e difere", p)
        print("ja existe, identico:", nome, h[:16]); continue
    open(p, "wb").write(b)
    print("copiado:", nome, h[:16], len(b), "B")
    fonte = WK + "/v392_insumos/F_KERNEL/conj/" + s["fonte"].replace("\\", "/").split("/")[-1]
    assert hashlib.sha256(open(fonte, "rb").read()).hexdigest() == s["fonte_sha256"], ("fonte da sonda difere do RESULTADO", fonte)
print("OK")

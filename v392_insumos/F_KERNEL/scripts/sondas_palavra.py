import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L  # noqa: E402

F = L.F
OV = os.path.join(F, "ov")
CONJ = os.path.join(F, "conj")
LOG = os.path.join(F, "logs", "P")
res = []
for nome in ["P1_PalavraEaLetra", "P1b_FechoDaPalavra", "P1c_FechoTransitivoPalavra", "P3_PostoRankA4"]:
    r = L.run_lean(nome, os.path.join(CONJ, nome + ".lean"), CONJ, None, LOG, kernel_lib=OV)
    out = open(r["log"], "rb").read().decode("utf-8", "replace")
    print(nome, "rc", r["rc"], "s", r["segundos"], "ax", r["axiomas"] if nome.startswith("P3") else "")
    print("\n".join(l[:900] for l in out.splitlines() if l.startswith(("USA", "AUSENTE", "FECHO")) or "error" in l))
    res.append(r)
print(L.dump({"sondas": res}, os.path.join(F, "RESULTADO_P_palavra.json")))

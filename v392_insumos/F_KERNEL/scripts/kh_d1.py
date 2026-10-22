# KH-N1, D1: re-roda o AuditoriaCobertura73.lean de 07/10 (bytes identicos) contra o kernel do Nos (so leitura)
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L  # noqa: E402

F = L.F
KH = os.path.join(F, "kh")
LOG = os.path.join(F, "logs", "KH")
os.makedirs(KH, exist_ok=True)
ORIG = r"C:\IALD\PROGRAMA_IALD\levantamento_qg\cobertura_axiomas\sandbox\AuditoriaCobertura73.lean"
src = os.path.join(KH, "AuditoriaCobertura73.lean")
if not os.path.exists(src):
    shutil.copyfile(ORIG, src)
assert L.sha(src) == "71c83b21fadf09348c2e37487955e3eaab80f4cd56c41c447fa81dadbb5cda35" == L.sha(ORIG)
r = L.run_lean("D1_cobertura73", src, KH, None, LOG)  # kernel_lib=None: os .olean do Nos no lugar
out = open(r["log"], "rb").read().decode("utf-8", "replace")
novo = sorted(l for l in out.splitlines() if l.startswith("COBERTURA"))
velho = sorted(l for l in open(r"C:\IALD\PROGRAMA_IALD\levantamento_qg\cobertura_axiomas\sandbox\saida_auditoria_73.txt",
                                encoding="utf-8").read().splitlines() if l.startswith("COBERTURA"))
r["linhas_novas"] = len(novo)
r["linhas_0710"] = len(velho)
r["identico_ao_0710_como_conjunto"] = (novo == velho)
r["so_novo"] = [l for l in novo if l not in set(velho)][:20]
r["so_velho"] = [l for l in velho if l not in set(novo)][:20]
r["total"] = [l for l in novo if l.startswith("COBERTURA_TOTAL")]
import collections  # noqa: E402
r["distribuicao_0710"] = dict(collections.Counter((x.split("\t")[4] if len(x.split("\t")) > 4 else "") for x in velho if x.startswith("COBERTURA\t")))
print("rc", r["rc"], "s", r["segundos"], "linhas", len(novo), len(velho), "identico", r["identico_ao_0710_como_conjunto"], r["total"], r["distribuicao_0710"])
print(L.dump(r, os.path.join(F, "RESULTADO_KH_D1.json")))

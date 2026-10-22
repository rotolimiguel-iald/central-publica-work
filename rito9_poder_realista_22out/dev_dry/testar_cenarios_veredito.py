"""Exercita o veredito.py PINADO em dados FALSOS (saida do dry fora das familias) nos tres desfechos + adulteracao.

Cenarios: base (UNDERPOWERED), A (taxa fantasia 1 fusao/neutrino -> POWERED_BNS), B (linha MC adulterada -> INCONCLUSIVE),
C (CSV adulterado sem refazer o manifesto -> erro MANIFEST_RODADA divergente), D (veredito.py alterado -> PIN_CHANGED).
Grava dev_dry/cenarios_veredito.json e remove a pasta de teste (que contem um PREREGISTRO.json FALSO).
Uso: python testar_cenarios_veredito.py
"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
subprocess.run([PY, "-B", "-X", "utf8", os.path.join(AQUI, "preparar_teste_veredito.py")], check=True, capture_output=True)
T = os.path.join(AQUI, "teste_veredito")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def manifesto(pasta):
    man = {n: sha(os.path.join(pasta, n)) for n in sorted(os.listdir(pasta)) if n != "MANIFEST_RODADA.json"}
    json.dump(dict(sha256=man), open(os.path.join(pasta, "MANIFEST_RODADA.json"), "w", encoding="utf-8"), indent=2)


def rodar(prereg, pins, saida, out):
    os.makedirs(os.path.join(T, "out_" + out[:-5]), exist_ok=True)       # cada cenario escreve o seu derivados_KK_por_caso.csv
    out = os.path.join("out_" + out[:-5], out)
    r = subprocess.run([PY, "-B", "-X", "utf8", "veredito.py", prereg, pins, saida, out], cwd=T, capture_output=True, text=True)
    txt = (r.stdout.strip() or r.stderr.strip().splitlines()[-1])
    try:
        return json.loads(txt)["veredito"]
    except Exception:
        return txt[-160:]


res = {}
res["base"] = rodar("PREREGISTRO.json", "PINS.json", "saida", "v_base.json")

pr = json.load(open(os.path.join(T, "PREREGISTRO.json"), encoding="utf-8"))
pr["taxa_KK"]["fusoes_por_neutrino_esperado"] = 1
json.dump(pr, open(os.path.join(T, "PREREGISTRO_A.json"), "w", encoding="utf-8"), indent=2)
shutil.copytree(os.path.join(T, "saida"), os.path.join(T, "saidaA"))
amb = json.load(open(os.path.join(T, "saidaA", "AMBIENTE_RODADA.json"), encoding="utf-8"))
amb["prereg_sha256"] = sha(os.path.join(T, "PREREGISTRO_A.json"))
json.dump(amb, open(os.path.join(T, "saidaA", "AMBIENTE_RODADA.json"), "w", encoding="utf-8"), indent=2)
manifesto(os.path.join(T, "saidaA"))
json.dump(dict(sha256={"PREREGISTRO_A.json": sha(os.path.join(T, "PREREGISTRO_A.json")), "veredito.py": sha(os.path.join(T, "veredito.py"))}),
          open(os.path.join(T, "PINS_A.json"), "w", encoding="utf-8"), indent=2)
res["A_taxa_fantasia"] = rodar("PREREGISTRO_A.json", "PINS_A.json", "saidaA", "v_A.json")

shutil.copytree(os.path.join(T, "saida"), os.path.join(T, "saidaB"))
rows = list(csv.DictReader(open(os.path.join(T, "saidaB", "verificacao_mc.csv"), encoding="utf-8")))
rows[0]["ok"] = "False"
with open(os.path.join(T, "saidaB", "verificacao_mc.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
manifesto(os.path.join(T, "saidaB"))
res["B_linha_mc_adulterada"] = rodar("PREREGISTRO.json", "PINS.json", "saidaB", "v_B.json")

shutil.copytree(os.path.join(T, "saida"), os.path.join(T, "saidaC"))
open(os.path.join(T, "saidaC", "n_req_por_caso.csv"), "a", encoding="utf-8").write("\n")
res["C_csv_adulterado_sem_manifesto"] = rodar("PREREGISTRO.json", "PINS.json", "saidaC", "v_C.json")

open(os.path.join(T, "veredito.py"), "a", encoding="utf-8").write("\n# adulterado\n")
res["D_veredito_py_alterado"] = rodar("PREREGISTRO.json", "PINS.json", "saida", "v_D.json")

json.dump(res, open(os.path.join(AQUI, "cenarios_veredito.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
shutil.rmtree(T)
print(json.dumps(res, indent=2, ensure_ascii=False))

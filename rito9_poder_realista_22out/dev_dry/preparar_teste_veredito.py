"""Prepara uma pasta FALSA para testar veredito.py (nada disto e a rodada oficial).

Copia a saida do dry (saida2) para dev_dry/teste_veredito/saida, marca modo=OFICIAL no ambiente (so no teste),
recalcula o manifesto, monta PREREGISTRO/PINS falsos e copia veredito.py para ao lado.
"""
import hashlib
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ALVO = os.path.join(AQUI, "teste_veredito")
if os.path.exists(ALVO):
    shutil.rmtree(ALVO)
os.makedirs(ALVO)
saida = os.path.join(ALVO, "saida")
shutil.copytree(os.path.join(AQUI, "saida2"), saida)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


cfg = json.load(open(os.path.join(AQUI, "config_dry.json"), encoding="utf-8"))
cfg["veredito"] = dict(familias_realistas=["P1", "P2"], max_eventos=10, tol_massa=1e-9, tol_fora=1e-12,
                       mc_min_linhas=10, robustez_min_linhas=10)
cfg["taxa_KK"] = dict(fusoes_por_neutrino_esperado=2500, exposicao_Mt_ano_por_neutrino_esperado=80,
                      massa_detector_declarada_Mt=1.0, N_nu_a_100Mpc_por_Mt=6.25e-4, R_Mpc3_por_Myr=1.0, D_eff_Mpc=200)
pr = os.path.join(ALVO, "PREREGISTRO.json")
json.dump(cfg, open(pr, "w", encoding="utf-8"), indent=2)
shutil.copy(os.path.join(RAIZ, "veredito.py"), os.path.join(ALVO, "veredito.py"))
amb_p = os.path.join(saida, "AMBIENTE_RODADA.json")
amb = json.load(open(amb_p, encoding="utf-8"))
amb["modo"] = "OFICIAL"
amb["prereg_sha256"] = sha(pr)
json.dump(amb, open(amb_p, "w", encoding="utf-8"), indent=2)
man = {n: sha(os.path.join(saida, n)) for n in sorted(os.listdir(saida)) if n != "MANIFEST_RODADA.json"}
json.dump(dict(sha256=man), open(os.path.join(saida, "MANIFEST_RODADA.json"), "w", encoding="utf-8"), indent=2)
pins = dict(sha256={"PREREGISTRO.json": sha(pr), "veredito.py": sha(os.path.join(ALVO, "veredito.py"))})
json.dump(pins, open(os.path.join(ALVO, "PINS.json"), "w", encoding="utf-8"), indent=2)
print("pasta de teste pronta:", ALVO)

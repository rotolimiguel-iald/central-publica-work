# -*- coding: utf-8 -*-
import json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prove_heart_and_gravity_seal import prove_heart_and_gravity_seal, chi_from_alpha, SOURCE_RECONSTRUCTED, SOURCE_SPECTRAL
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/"
core = json.load(open(NOS + "um_absoluto.json", encoding="utf-8"))["core"]
src = open(NOS + "um.py", "rb").read().decode("utf-8")
m = re.search(r"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)", src, re.M)
alpha = float(m.group(1))
chi = chi_from_alpha(alpha)
def show(nome, r):
    print("==", nome, "|", r["verdict"], "| all_verified", r["all_verified"], "| prev_indep", r["previsao_independente"], "| G_derivado", r["G_derivado"])
    for c in r["checks"]:
        print("  [%s] %s -> %s" % ("OK" if c["ok"] else "FALHA", c["nome"], str(c["valor"])[:90]))
    print("  elos:", [(l["elo"], l["rotulo"], l["ok"]) for l in r["links"]])
r1 = prove_heart_and_gravity_seal(core, SOURCE_RECONSTRUCTED, chi); show("CODATA_RECONSTRUCTED", r1)
r2 = prove_heart_and_gravity_seal(core, SOURCE_RECONSTRUCTED, chi * 1.001); show("NEGATIVO chi adulterado", r2)
r3 = prove_heart_and_gravity_seal(core, SOURCE_SPECTRAL, chi); show("SPECTRAL sem meta", r3)
r4 = prove_heart_and_gravity_seal(core, SOURCE_SPECTRAL, chi, {"origem": "TESTE_SINTETICO", "metodo": "x", "incerteza": 1e-9}); show("SPECTRAL com meta (sintetico)", r4)
assert r1["all_verified"] and not r1["previsao_independente"] and r1["verdict"].startswith("FORM_VERIFIED")
assert not r2["all_verified"] and not r3["all_verified"]
assert r4["previsao_independente"] and r4["verdict"].startswith("PURE_DERIVATION")
print("TESTES OK; alpha lido do um.py =", alpha, "chi =", chi)

# -*- coding: utf-8 -*-
"""Revisor terceiro v406: o que a integracao R3 mudou, alem dos imports, entre a fonte da bancada (MANIFEST.fonte) e o modulo do bundle no sandbox k406c. Conta os blocos #eval removidos."""
import difflib, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
m = json.load(open(R + "insumos/MANIFEST_integracao_R3_20261102_192452.json", encoding="utf-8"))
b = json.load(open(R + "BUNDLE_v406.json", encoding="utf-8"))
n_eval = {x["rel"].split("/")[-1][:-5]: x.get("n_eval_removidos", 0) for x in b["modulos"]}
tot_blocos = 0; tot_linhas = 0; porcls = {"IO.println": [0, 0], "IO.FS.withFile": [0, 0]}; so_import_e_eval = True; mods = []
for nome, e in m.items():
    if e.get("status") != "novo_compilado": continue
    ob = open(e["fonte"], "rb").read()
    assert hashlib.sha256(ob).hexdigest() == e["sha256_fonte"], ("fonte da bancada difere do manifesto", nome)
    o = ob.decode("utf-8").replace("\r\n", "\n").split("\n"); c = open("C:/t/k406c/final/TGLExt/F1Fecho394/" + nome + ".lean", "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n")
    rem = []; add = []
    for x in difflib.unified_diff(o, c, lineterm="", n=0):
        if x.startswith(("---", "+++", "@@")): continue
        if re.match(r"[+-]\s*import\b", x): continue
        (rem if x.startswith("-") else add).append(x[1:])
    if rem or add:
        txt = "\n".join(rem)
        n_ioprintln = len(re.findall(r"^#eval IO\.println", txt, re.M)); n_iofs = len(re.findall(r"^#eval IO\.FS\.withFile", txt, re.M))
        resto = [l for l in rem if l.strip() and not l.startswith("#eval") and not l.startswith("  h.")]
        mods.append((nome, n_ioprintln, n_iofs, len(rem), len(add), n_eval.get(nome)))
        tot_blocos += n_ioprintln + n_iofs; tot_linhas += len(rem); porcls["IO.println"][0] += n_ioprintln; porcls["IO.println"][1] += 1 if n_ioprintln else 0; porcls["IO.FS.withFile"][0] += n_iofs; porcls["IO.FS.withFile"][1] += 1 if n_iofs else 0
        if add or resto: so_import_e_eval = False; print("ATENCAO: diferenca que nao e' import nem #eval em", nome, add[:3], resto[:3])
for r in mods: print(r)
print("modulos com #eval removido:", len(mods), "| blocos #eval:", tot_blocos, "| linhas removidas:", tot_linhas, "| por classe [blocos, modulos]:", porcls, "| soma n_eval_removidos do BUNDLE:", sum(n_eval.values()), "| so' imports e #eval mudam:", so_import_e_eval)

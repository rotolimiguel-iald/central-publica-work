# -*- coding: utf-8 -*-
"""A3a -- varredura PROPRIA de beta (e vizinhos) literal no CODIGO dos construtores (.py e .lean de 2_OPTICO e 3_KERNEL,
inclusive tentativas). Padroes amplos: ponto OU virgula decimal, notacao cientifica, digitos colados."""
import json, os, re

U = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PADROES = {
    "beta_decimal": r"0[.,]0120\d*",
    "beta_cientifico": r"1[.,]20\d*\s*[eE]\s*-\s*0*2\b",
    "beta_cientifico_e3": r"12[.,]0\d*\s*[eE]\s*-\s*0*3\b",
    "beta_digitos": r"120313\d*",
    "beta_curto_0_012": r"(?<![\d.])0[.,]012(?![\d])",
    "alpha_literal": r"7[.,]297\d*",
    "alpha_inverso": r"137[.,]03\d*",
    "sqrt_e_literal": r"1[.,]6487\d*",
    "thetaM_literal": r"0[.,]1099\d*",
    "um_menos_beta": r"0[.,]98796\d*",
    "cos_thetaM": r"0[.,]99396\d*",
    "dois_beta": r"0[.,]02406\d*",
}
alvos = []
for sub in ("2_OPTICO", "3_KERNEL"):
    for dp, dns, fns in os.walk(os.path.join(U, sub)):
        for fn in fns:
            if fn.endswith(".py") or ".py." in fn or fn.endswith(".lean") or ".lean." in fn:
                alvos.append(os.path.join(dp, fn))
res = {"n_arquivos_de_codigo": len(alvos), "achados": []}
for p in sorted(alvos):
    t = open(p, encoding="utf-8", errors="replace").read()
    for nome, pat in PADROES.items():
        for m in re.finditer(pat, t):
            ln = t.count("\n", 0, m.start()) + 1
            linha = t.splitlines()[ln - 1].strip()
            res["achados"].append(dict(arquivo=os.path.relpath(p, U), linha=ln, padrao=nome, trecho=linha[:200]))
res["n_achados"] = len(res["achados"])
os.makedirs(os.path.join(R2, "saidas"), exist_ok=True)
with open(os.path.join(R2, "saidas", "A3a_LITERAIS.json"), "x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
print("arquivos de codigo varridos:", res["n_arquivos_de_codigo"], "| achados:", res["n_achados"])
for a in res["achados"]:
    print("  %s:%d [%s] %s" % (a["arquivo"], a["linha"], a["padrao"], a["trecho"][:150]))

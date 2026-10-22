# -*- coding: utf-8 -*-
"""05 -- (3) palavras proibidas com contexto e linha, nos TXT PT/EN; e o inventario dos 'Ao lado (vNNN)' / 'Beside (vNNN)' nos .tex;
(4) presenca no artigo das erratas de 28/09 (palavras-chave)."""
import re, os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = os.path.dirname(os.path.abspath(__file__))
TXT = {l: open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8").read() for l in ("pt", "en")}
TEX = {l: open(os.path.join(NOS, "um_absoluto_%s.tex" % l), encoding="utf-8").read() for l in ("pt", "en")}
rep = {}
print("### (3) PALAVRAS PROIBIDAS: confirmad|confirmed (TXT), com linha e contexto")
rx = re.compile(r"confirmad|confirmed", re.I)
rep["proibidas"] = {}
for l in ("pt", "en"):
    rows = []
    for i, line in enumerate(TXT[l].splitlines(), 1):
        for m in rx.finditer(line):
            a, b = max(0, m.start() - 70), min(len(line), m.end() + 70)
            rows.append({"linha": i, "trecho": line[a:b]})
    rep["proibidas"][l] = rows
    print("== %s: %d ocorrencias" % (l, len(rows)))
    for r in rows:
        print("  L%-5d ...%s..." % (r["linha"], r["trecho"].replace("\n", " ")))
print()
print("### 'Ao lado (v' / 'Beside (v' nos .tex (linha, titulo)")
rep["aolado"] = {}
for l, pat in (("pt", r"Ao lado \(v(\d+)\)[^\\}]{0,140}"), ("en", r"Beside \(v(\d+)\)[^\\}]{0,140}")):
    rows = []
    for i, line in enumerate(TEX[l].splitlines(), 1):
        for m in re.finditer(pat, line):
            rows.append({"linha": i, "v": int(m.group(1)), "titulo": m.group(0)[:160]})
    rep["aolado"][l] = rows
    print("== %s: %d marcas" % (l, len(rows)))
    for r in rows:
        print("  L%-5d v%-4d %s" % (r["linha"], r["v"], r["titulo"]))
print()
print("### contagem por versao (PT vs EN)")
from collections import Counter
cp, ce = Counter(r["v"] for r in rep["aolado"]["pt"]), Counter(r["v"] for r in rep["aolado"]["en"])
for v in sorted(set(cp) | set(ce)):
    flag = "" if cp[v] == ce[v] else "  <-- DIVERGE"
    print("  v%-4d PT %d  EN %d%s" % (v, cp[v], ce[v], flag))
print()
print("### (4) ERRATAS DE 28/09 -- palavras-chave no TXT (esperado: ausentes)")
KW = {
    "gate: degrau experimental = V11 unilateral": [r"V11 unilateral", r"unilateral", r"one-sided", r"degrau experimental", r"experimental step"],
    "ringdown no ramo canonico": [r"ramo can[oô]nico", r"canonical branch", r"BRANCH_A_INVISIBLE", r"branch A", r"ramo A"],
    "amplitude do eco sob a tipagem v372": [r"amplitude do eco", r"echo amplitude", r"sqrt\(beta\)", r"√β", r"AMPLITUDE_SQRT_BETA"],
    "D1 condicional ao mapa de R": [r"mapa de R", r"R_nu", r"R_eff", r"R_\\nu", r"map of R"],
    "DR1 sem correlacoes": [r"sem correla", r"without correlation", r"uncorrelated", r"DR1"],
    "covariancia do Planck de Chen\+2019": [r"Chen", r"2019", r"covari[aâ]ncia do Planck", r"Planck covariance"],
    "neutrino massivo duas vezes": [r"duas vezes", r"twice", r"dupla contagem", r"double count"],
    "neutrino na borda de 3 sigma dependente da entrada": [r"3σ", r"3 sigma", r"2,95", r"2\.95", r"NuFIT", r"borda de", r"edge of"],
    "Coma ja revelada": [r"revela", r"reveal", r"COMA_DEPHASING"],
    "evidencia primaria reclassificada": [r"evid[eê]ncia prim[aá]ria", r"primary evidence", r"reclassificad", r"reclassified"],
    "data 28/09": [r"28/09/2026", r"2026-09-28", r"28 de setembro", r"September 28"],
}
rep["erratas_28_09"] = {}
for k, pats in KW.items():
    rep["erratas_28_09"][k] = {}
    for l in ("pt", "en"):
        cnts = {}
        for p in pats:
            n = len(re.findall(p, TXT[l], re.I))
            cnts[p] = n
        rep["erratas_28_09"][k][l] = cnts
    print("- %s:\n    PT %s\n    EN %s" % (k, rep["erratas_28_09"][k]["pt"], rep["erratas_28_09"][k]["en"]))
json.dump(rep, open(os.path.join(OUT, "05_proibidas_e_aolado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

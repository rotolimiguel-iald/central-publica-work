# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R1): as 44 bandeiras ext_tu409_* (_LEAN_THEOREM_FLAGS do candidato, por AST) apontam para declaracoes que (a) existem no audit.log do build,
(b) estao no trio, (c) tem TGL_DECL_SOURCE no modulo esperado do bundle; e as 82 ancoras estao entre elas; nenhuma outra bandeira da base mudou."""
import ast, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
cs = open(R + "um_v409_candidato.py", "rb").read().decode("utf-8"); bs = open(R + "base_v408/um.py", "rb").read().decode("utf-8")


def lf(src):
    tr = ast.parse(src)
    for n in tr.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS": return ast.literal_eval(n.value)


F7 = lf(cs); F6 = lf(bs)
novas = {k: v for k, v in F7.items() if k not in F6}
print("flags base:", len(F6), "cand:", len(F7), "novas:", len(novas), "(esperado 158) | base e' sub-dict igual:", all(F7.get(k) == v for k, v in F6.items()), "| prefixo ext_tu409_:", all(k.startswith("ext_tu409_") for k in novas))
al = open(R + "kernel/audit.log", "rb").read().decode("utf-8", "replace")
trio = {"propext", "Classical.choice", "Quot.sound"}
ax = {}
for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", al):
    ax[m.group(1)] = {x.strip() for x in m.group(2).split(",")}
src = {}
for m in re.finditer(r"^TGL_DECL_SOURCE\t([^\t]+)\t(\S+)", al, re.M): src[m.group(1)] = m.group(2)
print("audit.log: depends-on-axioms", len(ax), "| DECL_SOURCE", len(src))
BJ = json.load(open(R + "BUNDLE_v409.json", encoding="utf-8")); mods = {b["rel"][:-5].replace("/", "."): b["rel"] for b in BJ["modulos"]}
bad = []
for fl, nm in novas.items():
    if nm not in ax or not ax[nm] <= trio or not ax[nm]: bad.append((fl, nm, "axiomas", ax.get(nm)))
    elif src.get(nm) not in mods: bad.append((fl, nm, "modulo", src.get(nm)))
print("bandeiras novas com problema:", bad[:5], "| n:", len(bad))
por_mod = {}
for fl, nm in novas.items(): por_mod[src.get(nm)] = por_mod.get(src.get(nm), 0) + 1
print("por modulo:", por_mod)
c = json.load(open(R + "CANDIDATO_v409.json", encoding="utf-8")); anc = c["kernel"]["ancoras"]
nomes_flag = set(novas.values())
print("ancoras:", len(anc), "| todas com bandeira:", all(a in nomes_flag for a in anc), "| sem bandeira:", [a for a in anc if a not in nomes_flag][:5])
print("ancoras no trio no audit.log:", all(a in ax and ax[a] <= trio and ax[a] for a in anc), "| sorryAx em qualquer axioma do log:", any("sorryAx" in v for v in ax.values()))
# todas as declaracoes dos 2 modulos no audit com TGL_DECL_SOURCE no bundle -> fora do trio?
decl_bundle = [n for n, r in src.items() if r in mods]
fora = [n for n in decl_bundle if n in ax and not ax[n] <= trio]
print("declaracoes com DECL_SOURCE nos 2 modulos:", len(decl_bundle), "| fora do trio:", fora[:5])
# declaracoes publicas vs bandeiras: quantas declaracoes do bundle NAO tem bandeira e porque (auxiliares)
sem = sorted(n for n in decl_bundle if n not in nomes_flag)
print("declaracoes do bundle sem bandeira:", len(sem), "(auxiliares da politica v394):", sem[:6])

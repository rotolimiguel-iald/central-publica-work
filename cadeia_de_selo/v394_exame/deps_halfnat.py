# -*- coding: utf-8 -*-
# Exame final v394 (c1, modelo forte): fecho reverso de TGL.HalfNat no kernel do sandbox v394
# (o autoteste do fail-closed injeta sorry no HalfNat e roda build+Audit 2 vezes).
# Estima o caminho critico de recompilacao com os tempos por modulo do lake_build.log do sandbox.
# So' LE o sandbox e a cadeia; escreve so' em v394_exame.
import os, re, json, sys, collections
K = r"C:\t\k394\final"
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v394"
H = os.path.dirname(os.path.abspath(__file__))
mods = {}
for top in ("TGL", "TGLExt"):
    for dp, dn, fn in os.walk(os.path.join(K, top)):
        if ".lake" in dp:
            continue
        for f in fn:
            if f.endswith(".lean"):
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, K)[:-5].replace(os.sep, ".")
                mods[rel] = p
for r in ("TGL", "TGLExt"):
    mods[r] = os.path.join(K, r + ".lean")
imp_re = re.compile(r"^\s*(?:public\s+)?import\s+(.+)$")
deps = {}
for m, p in mods.items():
    src = open(p, encoding="utf-8", errors="replace").read()
    # imports ficam no topo; corta no primeiro comando que nao e' import/comentario
    ds = set()
    for line in src.splitlines():
        s = line.strip()
        mm = imp_re.match(line)
        if mm:
            for tok in mm.group(1).split():
                if tok.startswith("--"):
                    break
                ds.add(tok)
    deps[m] = ds
rev = collections.defaultdict(set)
for m, ds in deps.items():
    for d in ds:
        rev[d].add(m)
def closure(start):
    seen, st = set(), [start]
    while st:
        x = st.pop()
        for y in rev.get(x, ()):
            if y not in seen:
                seen.add(y); st.append(y)
    return seen
cl = closure("TGL.HalfNat")
# tempos do sandbox
LB = open(os.path.join(V, "kernel", "lake_build.log"), encoding="utf-8", errors="replace").read()
tm = {}
for mm in re.finditer(r"\] Built ([^\s]+) \(([0-9.]+)(ms|s)\)", LB):
    t = float(mm.group(2)) / (1000.0 if mm.group(3) == "ms" else 1.0)
    tm[mm.group(1)] = t
novos = set(json.load(open(os.path.join(V, "kernel_modulos_novos_v394.lista.json"), encoding="utf-8")).get("modulos", []) or [])
# se a lista tiver outro formato, recolhe nomes de modulo por regex
if not novos:
    raw = open(os.path.join(V, "kernel_modulos_novos_v394.lista.json"), encoding="utf-8").read()
    novos = set(x.replace("/", ".")[:-5] for x in re.findall(r"TGLExt/[A-Za-z0-9_/]+\.lean", raw))
cl_novos = sorted(cl & novos)
# caminho critico (em s) do fecho, usando tempos do sandbox quando houver; ausentes = 15 s (HalfNat ~13 s na v393)
memo = {}
def cp(m):
    if m in memo:
        return memo[m]
    base = tm.get(m, 15.0)
    best = 0.0
    for d in deps.get(m, ()):
        if d in cl or d == "TGL.HalfNat":
            best = max(best, cp(d))
    memo[m] = base + best
    return memo[m]
memo["TGL.HalfNat"] = tm.get("TGL.HalfNat", 13.0)
crit = max((cp(m), m) for m in cl) if cl else (0, None)
soma = sum(tm.get(m, 15.0) for m in cl)
R = {"n_modulos_kernel": len(mods), "fecho_reverso_HalfNat": len(cl), "novos_v394_no_fecho": len(cl_novos),
     "novos_v394_total": len(novos), "exemplos_novos_no_fecho": cl_novos[:12],
     "caminho_critico_s": round(crit[0], 1), "fim_do_caminho_critico": crit[1],
     "soma_tempos_fecho_s": round(soma, 1), "fecho_sem_tempo_no_log": sorted(m for m in cl if m not in tm)[:20],
     "tempo_Audit_no_build_sandbox_s": tm.get("TGL.Audit"), "tempo_TGLExt_raiz_s": tm.get("TGLExt"),
     "importa_HalfNat_direto": sorted(rev.get("TGL.HalfNat", ()))[:40]}
json.dump(R, open(os.path.join(H, "DEPS_HALFNAT_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))

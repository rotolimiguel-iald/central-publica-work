# -*- coding: utf-8 -*-
"""prova_indice_v393.py -- chama prove_the_iald_index de um CANDIDATO, importado em processo ISOLADO, sobre o nucleo da tentativa 1 com o kernel verde
(mesma tecnica de exame_preflight/t10_index.py). uso: python -B -X utf8 prova_indice_v393.py <candidato.py> [--medir] [--sem-ambiguos] [--sem-gerados]
--medir: escreve indice_v393_medicao.json (ambiguos novos e nomes_lean das bandeiras sem referente), a partir do candidato ANTERIOR.
--sem-ambiguos / --sem-gerados: controle negativo (retira o conjunto V393 correspondente da copia temporaria; a copia temporaria nunca e' o candidato)."""
import sys, os, io, json, re, tempfile, shutil
H = os.path.dirname(os.path.abspath(__file__)); cand = os.path.abspath(sys.argv[1]); arg = set(sys.argv[2:])
src = open(cand, "rb").read().decode("utf-8")
if "--sem-ambiguos" in arg:
    n = src.count(" | _AMBIGUOS_CONJUNTO_V393)"); assert n == 1, n
    src = src.replace(" | _AMBIGUOS_CONJUNTO_V393)", ")")
if "--sem-gerados" in arg:
    n = src.count("_REFERENTES_GERADOS_V393 = frozenset(["); assert n == 1, n
    src = re.sub(r"_REFERENTES_GERADOS_V393 = frozenset\(\[.*?\n    \]\)", "_REFERENTES_GERADOS_V393 = frozenset([])", src, count=1, flags=re.S)
    assert "_REFERENTES_GERADOS_V393 = frozenset([])" in src
tmp = tempfile.mkdtemp(prefix="idx393_"); open(os.path.join(tmp, "um.py"), "wb").write(src.encode("utf-8"))
sys.path.insert(0, tmp); os.chdir(tmp)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
core = json.load(open(os.path.join(H, "base_v392", "um_absoluto.json"), encoding="utf-8"))["core"]
kf = core["kernel_formalization"]
FJ = json.load(open(os.path.join(H, "kernel", "FLAGS_v393.json"), encoding="utf-8"))
LOG = open(os.path.join(H, "kernel", "lake_build.log"), encoding="utf-8", errors="replace").read() + chr(10) + open(os.path.join(H, "kernel", "audit.log"), encoding="utf-8", errors="replace").read()
for m_ in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    kf["axiom_report"][m_.group(1)] = [a.strip() for a in m_.group(2).replace(chr(10), " ").split(",") if a.strip()]
for m_ in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    kf["axiom_report"].setdefault(m_.group(1), [])
for f_, n_, mod_, kind_ in FJ["flags"]:
    kf[f_] = True
if "--medir" in arg:
    ix = um.build_the_iald_index(core)
    fam = (("", um._LEAN_THEOREM_FLAGS), ("qgc_", um._QG_CERTIFICATE_FLAGS), ("qgp_", um._QG_PHYSICS_FLAGS), ("qgf_", um._QG_FRONTIER_FLAGS), ("gpf_", um._GRAVITY_PRICE_FLAGS), ("red_", um._REDUCTION_FLAGS), ("gpi_", um._GRAVITY_IMPORT_FLAGS), ("gpc_", um._GRAVITY_CITATION_FLAGS))
    ch2n = {p + c: n for p, d in fam for c, n in d.items()}
    base = set()
    for sfx in ("V369", "V372", "V375", "V383", "V392"):
        m = re.search(r"_AMBIGUOS_CONJUNTO_%s = frozenset\(\[(.*?)\]\)" % sfx, src, re.S); assert m, sfx
        base |= set(re.findall(r'"([^"]+)"', m.group(1)))
    viol = sorted(ix["violacoes"])
    out = {"ambiguos_todos": ix["ambiguos"], "ambiguos_novos": sorted(set(ix["ambiguos"]) - base), "n_congelados_anteriores": len(base), "violacoes_chaves": viol, "nomes_lean_sem_referente": sorted({ch2n[c] for c in viol}),
           "chaves_por_nome": {n: sorted(c for c in viol if ch2n[c] == n) for n in sorted({ch2n[c] for c in viol})}}
    json.dump(out, open(os.path.join(H, "indice_v393_medicao.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out["ambiguos_todos"]), len(viol), len(out["nomes_lean_sem_referente"])); sys.exit(0)
r = um.prove_the_iald_index(core)
res = {"candidato_sha16": __import__("hashlib").sha256(open(cand, "rb").read()).hexdigest()[:16], "flags": sorted(arg), "all_verified": r["all_verified"], "verdict": r.get("verdict"),
       "n_ausentes": r["n_ausentes"], "n_ambiguos": r["n_ambiguos"], "fails": [str(c[0])[:240] for c in r["checks"] if not c[1]]}
print(json.dumps(res, ensure_ascii=False)); shutil.rmtree(tmp, ignore_errors=True)

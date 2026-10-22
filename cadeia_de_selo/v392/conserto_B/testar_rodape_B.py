# -*- coding: utf-8 -*-
"""testar_rodape_B.py -- mede o CONSERTO B da PROPOSTA_V392 (rodape que le o axioma de TODA declaracao do modulo) nos controles Lean da bancada.
Importa o candidato como o ensaio_a_seco_v392.py (copia em V\\dry_v392\\um.py; NAO o um.py do Nos), extrai _BENCH_LEAN_CONTROLS + _bench_any_bytes (sha256 conferido pelo proprio
candidato), transpoe `import TGLV350.X` -> `import TGLExt.V350X` como a run_one, e compila cada controle com `lean --root=<pasta temporaria>` e o LEAN_PATH da run_one
(build do sandbox + packages), SEM e COM o rodape (RODAPE_B_v392.lean, lido do arquivo). Os dependentes (is_dep) sao compilados antes, com -o, em cada variante.
Controle negativo artificial: `theorem ... : False := by sorry` + rodape tem de mostrar sorryAx. Escreve RESULTADO_B_v392.json.
Uso: python -B -X utf8 testar_rodape_B.py <sandbox_kernel_construido> (ex.: C:/t/k392/final)   [sem -I: o candidato precisa de numpy do site do usuario]"""
import concurrent.futures as cf, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
KB = sys.argv[1] if len(sys.argv) > 1 else os.path.join("C:" + os.sep, "t", "k392", "final")
DRY = os.path.join(V, "dry_v392"); CAND = os.path.join(V, "um_v392_candidato.py")
sha = lambda b: hashlib.sha256(b).hexdigest()
if not os.path.exists(os.path.join(DRY, "um.py")) or sha(open(os.path.join(DRY, "um.py"), "rb").read()) != sha(open(CAND, "rb").read()):
    os.makedirs(DRY, exist_ok=True); shutil.copyfile(CAND, os.path.join(DRY, "um.py"))
assert sha(open(os.path.join(DRY, "um.py"), "rb").read()) == sha(open(CAND, "rb").read())
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
FOOT = open(os.path.join(HERE, "RODAPE_B_v392.lean"), "rb").read().decode("utf-8")
FOOT_SHA = sha(FOOT.encode("utf-8"))
TRIO = {"propext", "Classical.choice", "Quot.sound"}
UM_DEP = re.compile(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", re.S); UM_NONE = re.compile(r"'([\w.']+)' does not depend on any axioms")
SEL = ["IndependentAssemblyControls", "IndependentCompatibilityControls", "IndependentA2Controls", "GoodAntiunitaryPhase", "GoodDampingIntertwining", "GoodImaginaryScaling",
       "GoodPolarConjugation", "GoodRightScaling", "GoodScaledCoordinate", "GoodScaledDamping"]
CTRL_POS_COM_PRINT = "GoodTraceCompletion012"; CTRL_NEG = ["BadPolarIdentity", "BadTraceZero012"]
base = lambda c: os.path.basename(c[0])[:-5]
todos = list(um._BENCH_LEAN_CONTROLS)
by = {base(c): c for c in todos}
for n in SEL + [CTRL_POS_COM_PRINT] + CTRL_NEG:
    assert n in by, n
deps = [c for c in todos if c[5]]
sel_ctrl = [c for c in todos if c[3] == "POSITIVO"] + [by[n] for n in CTRL_NEG]   # TODOS os positivos (o patch vale para todos) + 2 negativos de controle
exe = "lean.exe" if os.name == "nt" else "lean"
tc = open(os.path.join(KB, "lean-toolchain"), encoding="utf-8").read().strip()
lean = os.path.join(os.path.expanduser("~"), ".elan", "toolchains", tc.replace("/", "--").replace(":", "---"), "bin", exe)   # como a run_one
assert os.path.exists(lean), lean
canon = os.path.join(KB, ".lake", "build", "lib", "lean"); pk = os.path.join(KB, ".lake", "packages")
pkgs = [os.path.join(pk, d, ".lake", "build", "lib", "lean") for d in sorted(os.listdir(pk))]
enverr = re.compile(r"unknown module prefix|object file .* does not exist|failed to read file|unknown package|file not found|No such file|could not resolve import", re.I)


def preparar(work):
    build = os.path.join(work, "build"); n = 0
    for r_, _, fs in os.walk(canon):
        rel = os.path.relpath(r_, canon); os.makedirs(os.path.join(build, rel), exist_ok=True)
        for f in fs:
            try:
                os.link(os.path.join(r_, f), os.path.join(build, rel, f))
            except OSError:
                shutil.copyfile(os.path.join(r_, f), os.path.join(build, rel, f))
            n += 1
    env = dict(os.environ); env["LEAN_PATH"] = os.pathsep.join([build] + [p for p in pkgs if os.path.isdir(p)]); env.pop("LEAN_SRC_PATH", None)
    return build, env, n


def run_one(idx, c, work, build, env, modo):
    """modo: sem | B (rodape nos POSITIVOS, como o patch) | Bex (B + `example` -> `theorem` nos POSITIVOS) | Bneg (rodape forcado nos NEGATIVOS, controle)"""
    pth, emb, sha_, kind, module, is_dep = c[0], c[1], c[2], c[3], c[4], c[5]
    res = {"control": os.path.basename(pth)[:-5], "kind": kind, "module": module, "is_dep": is_dep, "rodape": False, "examples_reescritos": 0}
    data = um._bench_any_bytes(emb)
    assert hashlib.sha256(data).hexdigest() == sha_, "sha256 do controle nao confere"
    src = data.decode("utf-8"); trans = []

    def _sub(m):
        mod = m.group(1)
        if mod.startswith("TGLV350."):
            new = "TGLExt.V350" + mod.split(".", 1)[1]; trans.append([mod, new]); return "import " + new
        return m.group(0)
    src = re.sub(r"^import\s+(\S+)", _sub, src, flags=re.M)
    res["transposition"] = trans; res["print_axioms_na_fonte"] = len(re.findall(r"(?m)^#print axioms", src)); res["examples_na_fonte"] = len(re.findall(r"(?m)^example\b", src))
    if modo == "Bex" and kind == "POSITIVO":
        k_ = [0]

        def _ex(m):
            k_[0] += 1; return "theorem _bench_example_%d" % k_[0]
        src = re.sub(r"(?m)^example\b", _ex, src); res["examples_reescritos"] = k_[0]
    if (modo in ("B", "Bex") and kind == "POSITIVO") or (modo == "Bneg" and kind == "NEGATIVO"):
        src = src.rstrip("\n") + "\n" + FOOT; res["rodape"] = True
    root = os.path.join(work, "src", "%03d" % idx); sp = os.path.join(root, *module.split(".")) + ".lean"
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    with open(sp, "w", encoding="utf-8", newline="") as fh:
        fh.write(src)
    cmd = [lean, "--root=" + root]
    if is_dep:
        op = os.path.join(build, *module.split(".")) + ".olean"; os.makedirs(os.path.dirname(op), exist_ok=True); cmd += ["-o", op]
    t1 = time.time()
    pr = subprocess.run(cmd + [sp], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=root, timeout=3600)
    out = (pr.stdout or "") + (pr.stderr or "")
    errs = [m.group(0) for m in re.finditer(r":(\d+):\d+: error[^\n]*", out)]
    ax = {m.group(1): [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()] for m in UM_DEP.finditer(out)}
    for m in UM_NONE.finditer(out):
        ax.setdefault(m.group(1), [])
    tot = re.search(r"TGL_FOOTER_B_TOTAL decl=(\d+) fora_do_trio=(\d+)", out)
    fora = sorted({a for v in ax.values() for a in v if a not in TRIO})
    res.update({"rc": pr.returncode, "seconds": round(time.time() - t1, 1), "errors": len(errs), "first_error": (errs[0].replace(root, "<src>")[:160] if errs else ""),
                "warning_sorry_msg": bool(re.search(r"declaration uses [`'‘]sorry", out)), "sorryAx": any("sorryAx" in v for v in ax.values()) or ("sorryAx" in out),
                "linhas_axioma_lidas_pelo_regex_do_umpy": len(ax), "axiomas_fora_do_trio": fora, "environment_error": bool(enverr.search(out)),
                "rodape_total": ([int(tot.group(1)), int(tot.group(2))] if tot else None), "ax": ax, "out_bytes": len(out)})
    return res


def rodada(modo, rotulo):
    work = tempfile.mkdtemp(prefix="tgl_B_" + rotulo + "_", dir=os.path.join("C:" + os.sep, "t", "k392")); t0 = time.time()
    build, env, nlink = preparar(work); out = {}
    try:
        for k, c in enumerate(deps):
            out[base(c)] = run_one(900 + k, c, work, build, env, modo)
        resto = [c for c in sel_ctrl if c not in deps]
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            for c, r in zip(resto, ex.map(lambda t: run_one(t[0], t[1], work, build, env, modo), list(enumerate(resto)))):
                out[base(c)] = r
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return out, round(time.time() - t0, 1), nlink


sem, t_sem, nl1 = rodada("sem", "sem")
com, t_com, nl2 = rodada("B", "B")                 # o patch como proposto: rodape so em kind POSITIVO
comx, t_cx, _ = rodada("Bex", "Bex")               # extensao medida: + `example` -> `theorem _bench_example_N` (os `example` nao deixam constante no ambiente)
com_neg, t_cn, _ = rodada("Bneg", "Bneg")          # controle: o rodape tambem nos negativos nao pode mudar o veredito deles


def linha(r_sem, r_x):
    d = r_x["rodape_total"][0] if r_x["rodape_total"] else None
    out = {"rc": r_x["rc"], "seconds": r_x["seconds"], "segundos_a_mais": round(r_x["seconds"] - r_sem["seconds"], 1), "errors": r_x["errors"], "first_error": r_x["first_error"],
           "declaracoes_do_modulo": d, "linhas_lidas_pelo_regex_do_umpy": r_x["linhas_axioma_lidas_pelo_regex_do_umpy"], "axiomas_fora_do_trio": r_x["axiomas_fora_do_trio"], "sorryAx": r_x["sorryAx"],
           "examples_reescritos": r_x["examples_reescritos"]}
    out["compila"] = bool(r_x["rc"] == 0 and r_x["errors"] == 0 and not r_x["sorryAx"] and not r_x["warning_sorry_msg"] and r_x["rodape_total"])
    out["cobre_ao_menos_uma_declaracao"] = bool(d and d > 0)
    out["uma_linha_lida_por_declaracao"] = bool(d is not None and d > 0 and r_x["linhas_axioma_lidas_pelo_regex_do_umpy"] == d)
    out["consistente_com_print_axioms_da_fonte"] = all(k in r_x["ax"] and set(r_x["ax"][k]) == set(v) for k, v in r_sem["ax"].items())
    return out


por = []
for c in sel_ctrl:
    n = base(c); a = sem[n]
    r = {"control": n, "kind": c[3], "pedido": n in SEL, "print_axioms_na_fonte": a["print_axioms_na_fonte"], "examples_na_fonte": a["examples_na_fonte"], "sem_rodape": {k: a[k] for k in ("rc", "seconds", "errors")}}
    if c[3] == "POSITIVO":
        r["B_rodape_como_proposto"] = linha(a, com[n]); r["Bex_rodape_e_example_viram_theorem"] = linha(a, comx[n])
    else:
        ln = com_neg[n]
        r["veredito_negativo_sem_rodape"] = a["rc"] != 0 and a["errors"] > 0 and not a["environment_error"]
        r["veredito_negativo_com_rodape_forcado"] = ln["rc"] != 0 and ln["errors"] > 0 and not ln["environment_error"]
    por.append(r)
# controle negativo artificial
neg_src = os.path.join(HERE, "neg_sorry_artificial.lean")
open(neg_src, "w", encoding="utf-8", newline="\n").write("import Mathlib.Tactic\ntheorem x_sorry : False := by sorry\ntheorem y_ok : 1 + 1 = 2 := by norm_num\n" + FOOT)
env_n = dict(os.environ); env_n["LEAN_PATH"] = os.pathsep.join([canon] + [p for p in pkgs if os.path.isdir(p)])
pr = subprocess.run([lean, neg_src], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env_n, cwd=HERE, timeout=1800)
o = (pr.stdout or "") + (pr.stderr or ""); axn = {m.group(1): [a.strip() for a in m.group(2).split(",")] for m in UM_DEP.finditer(o)}
neg_art = {"arquivo": neg_src, "sha256": sha(open(neg_src, "rb").read()), "rc": pr.returncode, "saida": o[-600:], "revela_sorryAx": any("sorryAx" in v for v in axn.values()), "ax": axn}
pos = [r for r in por if r["kind"] == "POSITIVO"]; ped = [r for r in pos if r["control"] in SEL]
negs_ok = all(r.get("veredito_negativo_sem_rodape") and r.get("veredito_negativo_com_rodape_forcado") for r in por if r["kind"] == "NEGATIVO")


def agrega(chave, grupo):
    g = [r[chave] for r in grupo]
    return {"n": len(g), "compilam": sum(x["compila"] for x in g), "cobrem_ao_menos_uma_declaracao": sum(x["cobre_ao_menos_uma_declaracao"] for x in g),
            "uma_linha_por_declaracao": sum(x["uma_linha_lida_por_declaracao"] for x in g), "com_axioma_fora_do_trio": sum(bool(x["axiomas_fora_do_trio"]) for x in g),
            "inconsistentes_com_print_axioms": sum(not x["consistente_com_print_axioms_da_fonte"] for x in g), "sem_cobertura": [r["control"] for r in grupo if not r[chave]["cobre_ao_menos_uma_declaracao"]]}


agg = {"B_pedidos10": agrega("B_rodape_como_proposto", ped), "B_todos_positivos": agrega("B_rodape_como_proposto", pos),
       "Bex_pedidos10": agrega("Bex_rodape_e_example_viram_theorem", ped), "Bex_todos_positivos": agrega("Bex_rodape_e_example_viram_theorem", pos)}
comp_B = agg["B_todos_positivos"]["compilam"] == len(pos); comp_Bx = agg["Bex_todos_positivos"]["compilam"] == len(pos)
veredito = "COMPILA" if (comp_B and neg_art["revela_sorryAx"] and negs_ok) else "NAO_COMPILA"
veredito_x = "COMPILA" if (comp_Bx and neg_art["revela_sorryAx"] and negs_ok) else "NAO_COMPILA"
res = {"contrato": "RESULTADO_CONSERTO_B_v392", "veredito": veredito, "veredito_Bex": veredito_x,
       "leitura": "veredito = o rodape como a PROPOSTA o descreve (so run_cmd no fim, kind POSITIVO) compila em todos os positivos e revela sorryAx no controle artificial; mas so cobre os controles que tem declaracao NOMEADA: "
                  "os `example` nao deixam constante no ambiente (decl=0). Bex = extensao medida (example -> theorem _bench_example_N nos positivos).",
       "estatuto": "[REAL] medido aqui por script no sandbox da v392; o um.py nao foi editado nem rodado",
       "rodape_sha256": FOOT_SHA, "candidato_sha256": sha(open(CAND, "rb").read()), "sandbox_construido": KB.replace("\\", "/"), "lean": lean.replace("\\", "/"),
       "agregados": agg, "controles": por, "controle_negativo_artificial": neg_art, "negativos_de_controle_mantem_o_veredito": negs_ok,
       "tempo_total_s": {"sem_rodape": t_sem, "B": t_com, "Bex": t_cx, "rodape_tambem_nos_negativos": t_cn},
       "nota": "todos os %d positivos + 2 negativos; as 10 pedidas marcadas `pedido`; dependentes (is_dep) compilados antes, com -o, em cada variante" % len(pos)}
json.dump(res, open(os.path.join(HERE, "RESULTADO_B_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("VEREDITO B:", veredito, "| Bex:", veredito_x, "| negativo artificial revela sorryAx:", neg_art["revela_sorryAx"], "| tempos (s):", t_sem, t_com, t_cx, t_cn)
print(json.dumps(agg, ensure_ascii=False, indent=1))

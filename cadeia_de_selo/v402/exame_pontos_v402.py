# -*- coding: utf-8 -*-
"""exame_pontos_v402.py -- re-execucao ISOLADA dos pontos de chamada REAIS de um candidato um.py (molde: exame_pontos_v401.py). RE-EXECUTAVEL (argumentos), sem nada digitado do candidato:

  python -B -X utf8 exame_pontos_v402.py --candidato <um.py candidato> --logs <pasta com lake_build.log e audit.log CRUS do sandbox>
         [--flags <FLAGS_vNNN.json>] [--sha256 <sha256 esperado>] [--sandbox <kernel do sandbox, para o byte a byte>] [--core0 <um_absoluto.json da versao anterior SELADA>] [--selo0 <selo dela>]
         [--imp <pasta de importacao; padrao imp_<sha16> nesta pasta>] [--saida <json; padrao EXAME_PONTOS_<sha16>.json nesta pasta>]

O que faz (escreve SO' em --imp e --saida; le o Nos, o sandbox e a cadeia):
 (1) copia o candidato para --imp\\um.py (bytes; confere o sha256), importa-o (o rito NAO roda) e materializa o kernel embutido em --imp\\tgl_kernel (com os residuais do Nos); confere o embutido contra --sandbox byte a byte;
 (2) verify_tgl_kernel_formalization() de ponta a ponta com o lake SIMULADO devolvendo os logs CRUS; controles negativos: Audit com o build junto; Audit sem uma linha TGL_DECL_SOURCE; axioma fora do trio plantado nos DOIS logs; so' no Audit;
 (3) a escada com o kf novo e com o kf da versao anterior; o gate recomputado (prove_qg_closure_gate) com o kf novo e o feed V11 do core anterior;
 (4) [v401: + os pontos do sonico_v398 e da afinacao_das_cordas_v398, logo depois da testemunha; v402: + os pontos do selo_pela_propria_tecnologia_v399 e da declaracao_do_operador_v399, logo depois da afinacao] sobre o core anterior + kf novo, NA ORDEM DO MAIN: o indice da IALD, os vizinhos que leem o kernel, os registros por spec da v392; DEPOIS o PONTO DE CHAMADA REAL do psibit_v395 e da testemunha_estatica_v396 (as instrucoes do main que os chamam, achadas por
     ast e conferida como a que vem logo depois do principio da defasagem fractal, na fractalizacao do Um), DEPOIS o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (a instrucao do main logo depois do bloco do V1, hubble_ratio_opening_v388; os numeros
     lidos conferidos contra o resultado pinado) e, em seguida, TODAS as instrucoes do main entre o bloco da v393 (`regra_v393(core)`) e `_figs = emit_figures(core)`;
 (5) o selo: a instrucao `seal = {...}` do main sobre esse core, comparada com o selo anterior; (6) a guarda de veredito proibido LIDA do main do candidato; (7) os arquivos lidos/escritos pelas chamadas (rastreio de open)."""
import sys, os, io, json, copy, hashlib, re, time, ast, builtins, argparse
if sys.flags.optimize:
    raise SystemExit("RECUSO: -O")
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import delta_v402 as DL  # noqa: E402
NOS = DL.NOS
ap = argparse.ArgumentParser()
ap.add_argument("--candidato", default=os.path.join(H, DL.CANDIDATO))
ap.add_argument("--logs", default=os.path.join(H, DL.KERNEL_DIR))
ap.add_argument("--flags", default=None)
ap.add_argument("--sha256", default=None)
ap.add_argument("--sandbox", default=DL.SANDBOX)
ap.add_argument("--core0", default=None)
ap.add_argument("--selo0", default=None)
ap.add_argument("--imp", default=None)
ap.add_argument("--saida", default=None)
A = ap.parse_args()
b = open(A.candidato, "rb").read(); SHA = hashlib.sha256(b).hexdigest()
if A.sha256 and A.sha256 != SHA:
    raise SystemExit("RECUSO: o candidato tem sha256 %s, o esperado era %s" % (SHA, A.sha256))
IMP = A.imp or os.path.join(H, "imp_" + SHA[:16]); os.makedirs(IMP, exist_ok=True)
SAIDA = A.saida or os.path.join(H, "EXAME_PONTOS_%s.json" % SHA[:16])
if A.flags is None:
    fs = sorted(f for f in os.listdir(A.logs) if re.fullmatch(r"FLAGS_v\d+\.json", f))
    A.flags = os.path.join(A.logs, fs[-1]) if fs else None
dst = os.path.join(IMP, "um.py")
if not (os.path.exists(dst) and open(dst, "rb").read() == b):
    open(dst + ".tmp", "wb").write(b); os.replace(dst + ".tmp", dst)
assert hashlib.sha256(open(dst, "rb").read()).hexdigest() == SHA
nos_um = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
CORE0P = A.core0 or os.path.join(H, DL.BASE_DIR, "um_absoluto.json")   # a v401 SELADA (copia de bytes)
SELO0P = A.selo0 or os.path.join(os.path.dirname(CORE0P), "um_absoluto_selo.json")
sys.path.insert(0, IMP); os.chdir(IMP)
_o = sys.stdout; sys.stdout = io.StringIO(); t = time.time()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
R = {"candidato": A.candidato, "sha256": SHA, "bytes": len(b), "import_s": round(time.time() - t, 1), "UM_VERSION": um.UM_VERSION, "BASE": um.BASE,
     "nos_um_sha16": nos_um, "core0": CORE0P, "selo0": SELO0P, "logs": A.logs, "flags": A.flags}
assert os.path.normcase(um.BASE) == os.path.normcase(IMP), um.BASE
for rel, content in um._EMBEDDED_KERNEL_FILES.items():
    p = os.path.join(IMP, "tgl_kernel", *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
    if not (os.path.exists(p) and open(p, "r", encoding="utf-8", newline="").read() == content):
        open(p, "w", encoding="utf-8", newline="").write(content)
NOSK = os.path.join(NOS, "tgl_kernel")   # os residuais do Nos (arquivos que o hash formal conta e que nao estao embutidos): a arvore do exame os recebe como estao
for dp_, dn_, fn_ in os.walk(NOSK):
    if ".lake" in dp_.replace("\\", "/").split("/"):
        continue
    for nm_ in fn_:
        if nm_.endswith(".lean") or nm_ in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel_ = os.path.relpath(os.path.join(dp_, nm_), NOSK).replace("\\", "/")
            if rel_ not in um._EMBEDDED_KERNEL_FILES:
                d_ = os.path.join(IMP, "tgl_kernel", *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True)
                if not os.path.exists(d_):
                    import shutil as _sh; _sh.copyfile(os.path.join(dp_, nm_), d_)
R["kernel_embutido_n"] = len(um._EMBEDDED_KERNEL_FILES)
if A.sandbox and os.path.isdir(A.sandbox):
    dif = [r for r, c in um._EMBEDDED_KERNEL_FILES.items() if not os.path.exists(os.path.join(A.sandbox, *r.split("/"))) or open(os.path.join(A.sandbox, *r.split("/")), "rb").read() != c.encode("utf-8")]
    R["embutido_vs_sandbox"] = {"sandbox": A.sandbox, "n_dif": len(dif), "diferentes": dif[:10]}
LBP, AUP = os.path.join(A.logs, "lake_build.log"), os.path.join(A.logs, "audit.log")
LB = open(LBP, encoding="utf-8", errors="replace").read(); AUD = open(AUP, encoding="utf-8", errors="replace").read()
R["logs_sha16"] = {"lake_build.log": hashlib.sha256(open(LBP, "rb").read()).hexdigest()[:16], "audit.log": hashlib.sha256(open(AUP, "rb").read()).hexdigest()[:16]}
import subprocess as _sp
# a saida de `lean --version` e' LIDA do toolchain do sandbox (nada digitado; o hash do commit sai do proprio Lean)
LEAN_VERSION_REAL = (_sp.run(["lean", "--version"], capture_output=True, text=True, cwd=A.sandbox).stdout.strip().splitlines() or ["Lean (version 4.31.0)"])[0]
calls = []


def mkfake(build_out, audit_out):
    def fake(cmd, cwd, tmo):
        calls.append([" ".join(cmd[1:]), tmo])
        o = {"cmd": " ".join(cmd), "returncode": 0, "stderr": "", "capture_exists": True, "capture_read_error": False, "elapsed_seconds": 0.0, "timeout": False}
        if cmd[1:] == ["--version"]: o["stdout"] = "Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)"
        elif cmd[1:3] == ["env", "lean"] and "--version" in cmd: o["stdout"] = LEAN_VERSION_REAL
        elif cmd[1:] == ["build"]: o["stdout"] = build_out
        else: o["stdout"] = audit_out
        o["capture_nonempty"] = bool(o["stdout"]); o["capture_sha256"] = hashlib.sha256(o["stdout"].encode("utf-8")).hexdigest()
        return o
    return fake


def run_verify(build_out, audit_out):
    sv = (um.run_process_checked, um._find_lake); um.run_process_checked = mkfake(build_out, audit_out); um._find_lake = lambda: "lake"
    _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        return um.verify_tgl_kernel_formalization()
    finally:
        um.run_process_checked, um._find_lake = sv; sys.stdout = _so


kf = run_verify(LB, AUD)
ext = {k: v for k, v in kf.items() if k.startswith("ext_") and isinstance(v, bool)}
novas = []
if A.flags and os.path.exists(A.flags):
    FJ = json.load(open(A.flags, encoding="utf-8"))
    novas = [f[0] if isinstance(f, (list, tuple)) else f for f in FJ["flags"]] if isinstance(FJ.get("flags"), list) else list(FJ.get("flags") or {})
C0 = json.load(open(CORE0P, encoding="utf-8")); core0 = C0["core"]; verdict0 = C0.get("verdict")
kf0 = core0["kernel_formalization"]
q_dif = {k: (kf0.get(k), kf.get(k)) for k in set(kf0) | set(kf) if (k.startswith("qgc_") or k.startswith("qgp_") or k.startswith("qgf_")) and kf0.get(k) != kf.get(k)}
v0_true_now_not = [k for k, v in kf0.items() if v is True and kf.get(k) is not True]
R["verify"] = {"verdict": kf.get("verdict"), "all_verified": kf.get("all_verified"), "cobertura": kf.get("axiom_coverage_v392"),
               "proveniencia": {k: v for k, v in (kf.get("declaration_sources_status_v394") or {}).items() if k != "errors"},
               "proveniencia_erros_n": len((kf.get("declaration_sources_status_v394") or {}).get("errors") or []),
               "axiom_report_n": len(kf.get("axiom_report") or {}), "ext_true": sum(ext.values()), "n_ext": len(ext),
               "ext_false": [k for k, v in ext.items() if not v][:20], "novas_true": sum(1 for f in novas if kf.get(f) is True), "n_novas": len(novas),
               "lean_flags_false": [k for k in um._LEAN_THEOREM_FLAGS if kf.get(k) is not True][:20], "n_lean_flags": len(um._LEAN_THEOREM_FLAGS),
               "lean_flags_novas_vs_core0": len([k for k in um._LEAN_THEOREM_FLAGS if k not in kf0]),
               "calls": calls[:], "lean_version": kf.get("lean_version"), "sorryAx_absent": kf.get("sorryAx_absent"),
               "source_forbidden_tokens_absent": kf.get("source_forbidden_tokens_absent"), "formal_release_ready": kf.get("formal_release_ready"),
               "custom_TGL_axioms_absent": kf.get("custom_TGL_axioms_absent"),
               "gate_flags_qgc_qgp_qgf_diferentes_do_core0": q_dif, "n_bandeiras_true_no_core0_que_nao_sao_true_agora": len(v0_true_now_not),
               "bandeiras_true_no_core0_que_nao_sao_true_agora": v0_true_now_not[:20]}
TRIO = {"propext", "Classical.choice", "Quot.sound"}
ar, ar0 = kf.get("axiom_report") or {}, kf0.get("axiom_report") or {}
R["axiom_report"] = {"core0_n": len(ar0), "novo_n": len(ar), "core0_ausentes": len([k for k in ar0 if k not in ar]),
                     "core0_com_lista_diferente": len([k for k in ar0 if k in ar and sorted(ar[k]) != sorted(ar0[k])]),
                     "fora_do_trio": len([k for k, v in ar.items() if not set(v or []) <= TRIO])}


def resumo(k_):
    return {"all_verified": k_.get("all_verified"), "cobertura_ok": (k_.get("axiom_coverage_v392") or {}).get("ok"),
            "proveniencia_ok": (k_.get("declaration_sources_status_v394") or {}).get("ok"), "custom_TGL_axioms_absent": k_.get("custom_TGL_axioms_absent")}


neg = {"audit_com_o_build_junto": resumo(run_verify(LB, LB + AUD))}
m1 = re.search(r"(?m)^TGL_DECL_SOURCE\t.*\n", AUD)
neg["audit_sem_uma_TGL_DECL_SOURCE"] = dict(resumo(run_verify(LB, AUD.replace(m1.group(0), "", 1))) if m1 else {}, achou_linha=bool(m1))
nome_novo = None
for f in novas:
    n_ = um._LEAN_THEOREM_FLAGS.get(f)
    if n_ and re.search(r"(?m)^'" + re.escape(n_) + r"' depends on axioms: \[", AUD):
        nome_novo, flag_novo = n_, f
        break


def planta(txt):
    pat = re.compile(r"(?m)^'" + re.escape(nome_novo) + r"' depends on axioms: \[([^\]]*)\]")
    return pat.sub(lambda m: m.group(0)[:-1] + ", TGLExt.axiomaPlantado]", txt)


if nome_novo:
    kc = run_verify(planta(LB), planta(AUD)); ka = run_verify(LB, planta(AUD))
    neg["axioma_fora_do_trio_plantado_nos_dois_logs"] = dict(resumo(kc), nome=nome_novo, flag=flag_novo, flag_valor=kc.get(flag_novo), plantou=planta(AUD) != AUD and planta(LB) != LB)
    neg["axioma_plantado_so_no_audit"] = dict(resumo(ka), flag_valor=ka.get(flag_novo))
R["verify_negativos"] = neg
calls.clear()
el = um.prove_external_ladder(1.0, kf); el0 = um.prove_external_ladder(1.0, kf0)
R["escada"] = {k: el.get(k) for k in ("n_theorems_clean", "n_theorems_expected", "verdict", "all_verified")}
R["escada_com_kf_do_core0"] = {k: el0.get(k) for k in ("n_theorems_clean", "n_theorems_expected", "all_verified")}
J = lambda x: json.dumps(x, sort_keys=True, default=str)
n18 = lambda g: sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (g.get(fam) or {}).values() if v is True)
try:
    g_new = um.prove_qg_closure_gate(1.0, kf, independent_rite=core0.get("void_floor_v11")); g_old = core0.get("qg_closure") or {}
    R["gate_recomputado"] = {"verdict_igual": (g_new.get("gate") or {}).get("verdict") == (g_old.get("gate") or {}).get("verdict"), "verdict": (g_new.get("gate") or {}).get("verdict"),
                             "n18_novo": n18(g_new), "n18_core0": n18(g_old), "flags_iguais": all(J(g_new.get(f)) == J(g_old.get(f)) for f in ("formal_flags", "physics_flags", "experiment_flags")), "all_verified": g_new.get("all_verified")}
except Exception as e:
    R["gate_recomputado"] = {"EXCECAO": repr(e)[:300]}
lidos, escritos = set(), set()
_open0 = builtins.open


def _open_tr(f, mode="r", *a, **k):
    try:
        pth = os.path.abspath(f) if isinstance(f, (str, os.PathLike)) else str(f)
    except Exception:
        pth = str(f)
    (escritos if any(c in mode for c in "wax+") else lidos).add(str(pth))
    return _open0(f, mode, *a, **k)


out = {}


def falhas_de(r):
    fl = []
    for c in (r.get("checks") or []) if isinstance(r, dict) else []:
        if (isinstance(c, (list, tuple)) and len(c) > 1 and not c[1]) or (isinstance(c, dict) and (c.get("ok") is False or c.get("passed") is False)):
            fl.append(str(c)[:300])
    if isinstance(r, dict) and r.get("falhas"):
        fl += [str(x)[:200] for x in (r.get("falhas") or [])][:10]
    return fl[:12]


def run(nome, fn):
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        r = fn()
        out[nome] = {"all_verified": r.get("all_verified") if isinstance(r, dict) else None, "verdict": str(r.get("verdict"))[:300] if isinstance(r, dict) else str(r)[:300], "falhas": falhas_de(r)}
        return r
    except Exception as e:
        import traceback; out[nome] = {"EXCECAO": repr(e)[:300], "tb": traceback.format_exc()[-1200:]}
        return {"verdict": "EXCECAO", "all_verified": False}
    finally:
        builtins.open = _open0; sys.stdout = _so


core = copy.deepcopy(core0); core["kernel_formalization"] = kf; core["external_ladder"] = el
core["the_iald_index"] = run("the_iald_index", lambda: um.prove_the_iald_index(core))
for nome in ("the_axiom_v385", "the_verb_v386", "three_stress_tests_v387", "beta_runs_bounded_below_v388", "text_label_errata_v389", "fundacao_v390", "estatuto_da_prova_v391", "pedras_v392", "varredura_e_sorry_v392"):
    if hasattr(um, nome):
        core[nome] = run(nome, (lambda f: (lambda: f(core)))(getattr(um, nome)))
for n_ in um._V392_NOMES_REGISTROS:
    core.pop(n_, None)
run("_v392_rodar_registros", lambda: {"verdict": str(um._v392_rodar_registros(core))[:300], "all_verified": None})
src = open(dst, encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
unp = [ast.unparse(st) for st in main.body]
i0 = next(i for i, s_ in enumerate(unp) if "regra_v393(core)" in s_)
i1 = next(i for i, st in enumerate(main.body) if isinstance(st, ast.Assign) and "emit_figures(core)" in ast.unparse(st))
ipb = [i for i, s_ in enumerate(unp) if "psibit_v395(core)" in s_]
assert len(ipb) == 1, ("a instrucao do main que chama psibit_v395 nao e' unica", len(ipb))
ipb = ipb[0]
ipt = [i for i, s_ in enumerate(unp) if "testemunha_estatica_v396(core)" in s_]
assert len(ipt) == 1 and ipt[0] == ipb + 1, ("a instrucao do main que chama testemunha_estatica_v396 nao e' unica ou nao vem IMEDIATAMENTE depois da do psibit_v395", ipt, ipb)
ipt = ipt[0]
fd_antes = "existir E' o vazamento beta" in unp[ipb - 1] or 'existir E\' o vazamento beta' in unp[ipb - 1]
R["ponto_psibit"] = {"indice_no_main": ipb, "linha": main.body[ipb].lineno, "antes_do_bloco_v393": ipb < i0, "logo_depois_do_principio_da_defasagem_fractal": bool(fd_antes), "instrucao_anterior": unp[ipb - 1][:160].replace("\n", " | ")}
R["ponto_testemunha"] = {"indice_no_main": ipt, "linha": main.body[ipt].lineno, "antes_do_bloco_v393": ipt < i0, "logo_depois_do_psibit_v395": "psibit_v395(core)" in unp[ipt - 1], "instrucao_anterior": unp[ipt - 1][:160].replace("\n", " | ")}
for n_ in getattr(um, "_V393_NOMES_REGISTROS", []) + ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393"] + ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS) + ["psibit_v395"] + list(um._V395_NOMES_REGISTROS) + ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) + ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) + ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) + ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS):
    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0
antes = {k: J(core[k]) for k in core}
g = dict(vars(um)); g["core"] = core
# (4a) os PONTOS DE CHAMADA REAIS do psibit_v395 e da testemunha_estatica_v396 (as duas instrucoes do main, em ordem, como estao no candidato)
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ipb], main.body[ipt]], type_ignores=[])), "<main:psibit_v395+testemunha_estatica_v396>", "exec"), g); errp = None
except Exception as e:
    import traceback; errp = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_psb = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
pb = core.get("psibit_v395") or {}; tb = core.get("testemunha_estatica_v396") or {}
R["ponto_psibit"].update({"erro": errp, "stdout": stdout_psb.splitlines(), "avisos": [l for l in stdout_psb.splitlines() if "AVISO" in l], "verdict": pb.get("verdict"), "all_verified": pb.get("all_verified"),
                          "mecanica": {"passed": (pb.get("mechanics") or {}).get("passed"), "n_checks": (pb.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (pb.get("unconditional") or {}).get("in_kernel"),
                          "conditional_status": (pb.get("conditional_psion_face") or {}).get("status")})
R["ponto_testemunha"].update({"erro": errp, "avisos": [l for l in stdout_psb.splitlines() if "AVISO" in l], "verdict": tb.get("verdict"), "all_verified": tb.get("all_verified"),
                              "mecanica": {"passed": (tb.get("mechanics") or {}).get("passed"), "n_checks": (tb.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (tb.get("unconditional") or {}).get("in_kernel"),
                              "fock_status": (tb.get("fock_face") or {}).get("status"), "fock_fora_da_pedra": (tb.get("fock_face") or {}).get("declared_outside_the_stone")})
out["core.psibit_v395"] = {"all_verified": pb.get("all_verified"), "verdict": str(pb.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((pb.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
out["core.testemunha_estatica_v396"] = {"all_verified": tb.get("all_verified"), "verdict": str(tb.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((tb.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
# (4a'') os PONTOS DE CHAMADA REAIS do sonico_v398 e da afinacao_das_cordas_v398 (v401): as duas instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da testemunha_estatica_v396 (que vem imediatamente depois do psibit_v395), na fractalizacao do Um
isn = [i for i, s_ in enumerate(unp) if "sonico_v398(core)" in s_]
assert len(isn) == 1 and isn[0] == ipt + 1, ("a instrucao do main que chama sonico_v398 nao e' unica ou nao vem IMEDIATAMENTE depois da testemunha_estatica_v396", isn, ipt)
isn = isn[0]
iaf = [i for i, s_ in enumerate(unp) if "afinacao_das_cordas_v398(core)" in s_]
assert len(iaf) == 1 and iaf[0] == isn + 1, ("a instrucao do main que chama afinacao_das_cordas_v398 nao e' unica ou nao vem IMEDIATAMENTE depois do sonico_v398", iaf, isn)
iaf = iaf[0]
R["ponto_sonico"] = {"indice_no_main": isn, "linha": main.body[isn].lineno, "antes_do_bloco_v393": isn < i0, "logo_depois_da_testemunha_v396": "testemunha_estatica_v396(core)" in unp[isn - 1], "instrucao_anterior": unp[isn - 1][:160].replace("\n", " | ")}
R["ponto_afinacao"] = {"indice_no_main": iaf, "linha": main.body[iaf].lineno, "antes_do_bloco_v393": iaf < i0, "logo_depois_do_sonico_v401": "sonico_v398(core)" in unp[iaf - 1], "instrucao_anterior": unp[iaf - 1][:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[isn], main.body[iaf]], type_ignores=[])), "<main:sonico_v398+afinacao_das_cordas_v398>", "exec"), g); errs = None
except Exception as e:
    import traceback; errs = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_son = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
sn = core.get("sonico_v398") or {}; af = core.get("afinacao_das_cordas_v398") or {}
R["ponto_sonico"].update({"erro": errs, "stdout": stdout_son.splitlines(), "avisos": [l for l in stdout_son.splitlines() if "AVISO" in l], "verdict": sn.get("verdict"), "all_verified": sn.get("all_verified"),
                          "mecanica": {"passed": (sn.get("mechanics") or {}).get("passed"), "n_checks": (sn.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (sn.get("unconditional") or {}).get("in_kernel"), "beta_ok": sn.get("beta_ok"),
                          "entropia_theta_M_nats": (sn.get("values") or {}).get("collapse_entropy_theta_M_nats")})
R["ponto_afinacao"].update({"erro": errs, "avisos": [l for l in stdout_son.splitlines() if "AVISO" in l], "verdict": af.get("verdict"), "all_verified": af.get("all_verified"),
                            "mecanica": {"passed": (af.get("mechanics") or {}).get("passed"), "n_checks": (af.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (af.get("unconditional") or {}).get("in_kernel"),
                            "hipotese": af.get("hypothesis"), "geometria": af.get("geometry"), "deriva_cordas_do_axioma": af.get("derives_strings_from_the_axiom")})
out["core.sonico_v398"] = {"all_verified": sn.get("all_verified"), "verdict": str(sn.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((sn.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
out["core.afinacao_das_cordas_v398"] = {"all_verified": af.get("all_verified"), "verdict": str(af.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((af.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
# (4a-v402) os PONTOS DE CHAMADA REAIS do selo_pela_propria_tecnologia_v399 e da declaracao_do_operador_v399 (v402): as duas instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da afinacao_das_cordas_v398 (que vem imediatamente depois do sonico_v398), na fractalizacao do Um
ise = [i for i, s_ in enumerate(unp) if "selo_acom_v399(core)" in s_]
assert len(ise) == 1 and ise[0] == iaf + 1, ("a instrucao do main que chama selo_acom_v399 nao e' unica ou nao vem IMEDIATAMENTE depois da afinacao_das_cordas_v398", ise, iaf)
ise = ise[0]
idc = [i for i, s_ in enumerate(unp) if "declaracao_do_operador_v399(core)" in s_]
assert len(idc) == 1 and idc[0] == ise + 1, ("a instrucao do main que chama declaracao_do_operador_v399 nao e' unica ou nao vem IMEDIATAMENTE depois do selo_acom_v399", idc, ise)
idc = idc[0]
R["ponto_selo_acom"] = {"indice_no_main": ise, "linha": main.body[ise].lineno, "antes_do_bloco_v393": ise < i0, "logo_depois_da_afinacao_v401": "afinacao_das_cordas_v398(core)" in unp[ise - 1], "instrucao_anterior": unp[ise - 1][:160].replace("\n", " | ")}
R["ponto_declaracao"] = {"indice_no_main": idc, "linha": main.body[idc].lineno, "antes_do_bloco_v393": idc < i0, "logo_depois_do_selo_acom_v402": "selo_acom_v399(core)" in unp[idc - 1], "instrucao_anterior": unp[idc - 1][:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ise], main.body[idc]], type_ignores=[])), "<main:selo_acom_v399+declaracao_do_operador_v399>", "exec"), g); errsa = None
except Exception as e:
    import traceback; errsa = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_sa = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
sa = core.get("selo_pela_propria_tecnologia_v399") or {}; dc = core.get("declaracao_do_operador_v399") or {}
_decl_arquivo = hashlib.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read()).hexdigest()
R["ponto_selo_acom"].update({"erro": errsa, "stdout": stdout_sa.splitlines(), "avisos": [l for l in stdout_sa.splitlines() if "AVISO" in l], "verdict": sa.get("verdict"), "all_verified": sa.get("all_verified"), "perfil": (sa.get("values") or {}).get("perfil"),
                             "controles": [(sa.get("controles_negativos") or {}).get("n_controles"), (sa.get("controles_negativos") or {}).get("todos_recusados")], "sha256_do_um_py": (sa.get("selo") or {}).get("sha256"), "checks": [[d_, v_] for d_, v_ in (sa.get("checks") or [])]})
R["ponto_declaracao"].update({"erro": errsa, "avisos": [l for l in stdout_sa.splitlines() if "AVISO" in l], "verdict": dc.get("verdict"), "all_verified": dc.get("all_verified"), "verbatim_sha256": (dc.get("declaration") or {}).get("verbatim_sha256"),
                              "verbatim_sha256_igual_ao_arquivo": (dc.get("declaration") or {}).get("verbatim_sha256") == _decl_arquivo, "checks": [[d_, v_] for d_, v_ in (dc.get("checks") or [])]})
out["core.selo_pela_propria_tecnologia_v399"] = {"all_verified": sa.get("all_verified"), "verdict": str(sa.get("verdict"))[:300], "falhas": [d_ for d_, v_ in (sa.get("checks") or []) if not v_]}
out["core.declaracao_do_operador_v399"] = {"all_verified": dc.get("all_verified"), "verdict": str(dc.get("verdict"))[:300], "falhas": [d_ for d_, v_ in (dc.get("checks") or []) if not v_]}
# (4a-v402) o PONTO DE CHAMADA REAL do falsidade_da_inercia_v401 (v402): a instrucao do main (um `try`) que vem IMEDIATAMENTE depois da declaracao_do_operador_v399 (que vem imediatamente depois do selo_acom_v399), na fractalizacao do Um
ifa = [i for i, s_ in enumerate(unp) if "falsidade_da_inercia_v401(core)" in s_]
assert len(ifa) == 1 and ifa[0] == idc + 1, ("a instrucao do main que chama falsidade_da_inercia_v401 nao e' unica ou nao vem IMEDIATAMENTE depois da declaracao_do_operador_v399", ifa, idc)
ifa = ifa[0]
R["ponto_falsidade"] = {"indice_no_main": ifa, "linha": main.body[ifa].lineno, "antes_do_bloco_v393": ifa < i0, "logo_depois_da_declaracao_v399": "declaracao_do_operador_v399(core)" in unp[ifa - 1], "instrucao_anterior": unp[ifa - 1][:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ifa]], type_ignores=[])), "<main:falsidade_da_inercia_v401>", "exec"), g); errfa = None
except Exception as e:
    import traceback; errfa = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_fa = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
fa = core.get("falsidade_da_inercia_v401") or {}
R["ponto_falsidade"].update({"erro": errfa, "stdout": stdout_fa.splitlines(), "avisos": [l for l in stdout_fa.splitlines() if "AVISO" in l], "verdict": fa.get("verdict"), "all_verified": fa.get("all_verified"),
                            "mecanica": {"passed": (fa.get("mechanics") or {}).get("passed"), "n_checks": (fa.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (fa.get("unconditional") or {}).get("in_kernel"), "estrela_in_kernel": (fa.get("key_theorem") or {}).get("in_kernel"),
                            "costless_ok": (fa.get("costless") or {}).get("ok"), "beta_ok": fa.get("beta_ok"), "post_inertial_scales": (fa.get("values") or {}).get("post_inertial_scales"), "fixo_pelo_fluxo_inteiro": (fa.get("values") or {}).get("fixed_by_the_whole_flow")})
out["core.falsidade_da_inercia_v401"] = {"all_verified": fa.get("all_verified"), "verdict": str(fa.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((fa.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
# (4a-v402) os PONTOS DE CHAMADA REAIS da ponte, da queda e da esperanca (v402): as tres instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da falsidade_da_inercia_v401, em ordem (ponte, queda, esperanca), na fractalizacao do Um
_ANTERIOR402 = ["falsidade_da_inercia_v401(core)", "ponte_da_escala_dual_v402(core)", "queda_sem_geometria_v402(core)"]
for nome_, fn_, off_ in (("ponte", "ponte_da_escala_dual_v402", 1), ("queda", "queda_sem_geometria_v402", 2), ("esperanca", "esperanca_condicional_v402", 3)):
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois da falsidade_da_inercia_v401" % fn_, ii_, ifa)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "logo_depois_da_anterior": _ANTERIOR402[off_ - 1] in unp[ii_ - 1], "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
    except Exception as e:
        import traceback; err_ = repr(e) + traceback.format_exc()[-900:]
    finally:
        stdout_ = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    r_ = core.get(fn_) or {}
    R["ponto_" + nome_].update({"erro": err_, "stdout": stdout_.splitlines(), "avisos": [l for l in stdout_.splitlines() if "AVISO" in l], "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"),
                                "mecanica": {"passed": (r_.get("mechanics") or {}).get("passed"), "n_checks": (r_.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (r_.get("unconditional") or {}).get("in_kernel"),
                                "estrela_in_kernel": (r_.get("key_theorem") or {}).get("in_kernel"), "contexto_ok": (r_.get("context") or {}).get("ok"), "beta_ok": r_.get("beta_ok")})
    out["core." + fn_] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
# (4a') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397): a instrucao do main (um `try` + o `print` [v397]) que vem IMEDIATAMENTE depois do bloco do V1 (hubble_ratio_opening_v388), depois do psibit e da testemunha e antes do bloco da v393
iv = [i for i, s_ in enumerate(unp) if 'core["teste_de_veracidade_fase9_v397"] = _v392_registro(_V397_VERACIDADE_SPEC, core)' in s_ or "core['teste_de_veracidade_fase9_v397'] = _v392_registro(_V397_VERACIDADE_SPEC, core)" in s_]
assert len(iv) == 1, ("a instrucao do main que chama o registro de veracidade nao e' unica", len(iv))
iv = iv[0]
assert "[v388]" in unp[iv - 1] and "hubble_ratio_opening_v388" in unp[iv - 1], ("o registro de veracidade nao vem logo depois do print do bloco do V1 (hubble_ratio_opening_v388)", unp[iv - 1][:160])
assert "[v397]" in unp[iv + 1] and "teste_de_veracidade_fase9_v397" in unp[iv + 1], ("a instrucao seguinte nao e' o print do registro de veracidade", unp[iv + 1][:160])
R["ponto_veracidade"] = {"indice_no_main": iv, "linha": main.body[iv].lineno, "depois_do_psibit_e_da_testemunha": iv > ipt, "antes_do_bloco_v393": iv < i0, "instrucao_anterior": unp[iv - 1][:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[iv], main.body[iv + 1]], type_ignores=[])), "<main:teste_de_veracidade_fase9_v397>", "exec"), g); errv = None
except Exception as e:
    import traceback; errv = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_ver = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
tv = core.get("teste_de_veracidade_fase9_v397") or {}
res9 = json.load(open(os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME), encoding="utf-8"))   # a copia duravel, byte a byte do resultado pinado
lidos9 = tv.get("lido") or {}
num9 = {k_: (lidos9.get(k_) == DL.lido(res9, c_)) for k_, c_ in DL.F9_CAMINHOS.items()}
R["ponto_veracidade"].update({"erro": errv, "avisos": [l for l in stdout_ver.splitlines() if "AVISO" in l], "stdout": stdout_ver.splitlines(), "verdict": tv.get("verdict"), "all_verified": tv.get("all_verified"), "n_checks": len(tv.get("checks") or []),
                              "checks_falhos": [c_.get("descricao") for c_ in (tv.get("checks") or []) if not c_.get("ok")], "numeros_lidos_iguais_ao_resultado_pinado": num9, "fontes_ok": [f_["ok"] for f_ in (tv.get("fontes") or [])]})
out["core.teste_de_veracidade_fase9_v397"] = {"all_verified": tv.get("all_verified"), "verdict": str(tv.get("verdict"))[:300], "falhas": falhas_de(tv)}
# (4b) as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato
bloco = main.body[i0:i1]
R["main_bloco_executado"] = {"linhas": [bloco[0].lineno, bloco[-1].end_lineno], "n_instrucoes": len(bloco), "inicio": ast.unparse(bloco[0])[:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=bloco, type_ignores=[])), "<main:v393..emit_figures>", "exec"), g); err = None
except Exception as e:
    import traceback; err = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_bloco = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
R["main_bloco_executado"]["erro"] = err
R["main_bloco_executado"]["stdout"] = stdout_bloco[-4000:]
R["main_bloco_executado"]["avisos"] = [l for l in stdout_bloco.splitlines() if "AVISO" in l]
R["chaves_novas_no_core"] = sorted(set(core) - set(antes))
R["chaves_existentes_mexidas_pelo_bloco"] = sorted(k for k in antes if J(core.get(k)) != antes[k])
for k in R["chaves_novas_no_core"] + ["kh_n1_cobertura_v392"]:
    v = core.get(k) or {}
    if isinstance(v, dict):
        out["core." + k] = {"all_verified": v.get("all_verified"), "verdict": str(v.get("verdict"))[:300], "falhas": falhas_de(v)}
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
cmp = {}
for k, v in core.items():
    if isinstance(v, dict) and isinstance(core0.get(k), dict) and "verdict" in v:
        a_, bb = str(core0[k].get("verdict")), str(v.get("verdict"))
        if a_ != bb:
            cmp[k] = {"so_numeros": _num(_nc(a_)) == _num(_nc(bb)), "antes": a_[:220], "depois": bb[:220], "all_verified": v.get("all_verified")}
R["vereditos_que_mudaram_vs_core0"] = cmp
R["nao_verdes"] = {"v392": [k for k in um._V392_NOMES_REGISTROS if (core.get(k) or {}).get("all_verified") is not True],
                   "v393": [k for k in getattr(um, "_V393_NOMES_REGISTROS", []) if (core.get(k) or {}).get("all_verified") is not True],
                   "v394": [k for k in ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v395": [k for k in ["psibit_v395"] + list(um._V395_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v396": [k for k in ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v397": [k for k in ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v401": [k for k in ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v402": [k for k in ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v401_falsidade": [k for k in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v402_ponte_queda_esperanca": [k for k in ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "novas": [k for k in R["chaves_novas_no_core"] if isinstance(core.get(k), dict) and core[k].get("all_verified") is not True]}
R["n_arquivos_lidos_fora_do_imp"] = len([p for p in lidos if not p.startswith(IMP)])
R["arquivos_lidos_fora_do_imp"] = sorted(p for p in lidos if not p.startswith(IMP))
R["arquivos_escritos_fora_do_imp"] = sorted(p for p in escritos if not p.startswith(IMP))
seal_st = [n for n in ast.walk(main) if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "seal"]
try:
    st = seal_st[0]
    loads = sorted({x.id for x in ast.walk(st.value) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)})
    gs = dict(vars(um)); gs["core"] = core
    loc = {"verdict": verdict0, "result_hash": "EXAME", "_kf": core["kernel_formalization"], "_wrg": core.get("witness_rigidity") or {}, "_npg": core.get("negative_probes") or {}, "_wlg": core.get("witness_layers") or {}, "_iig": core.get("interface_is_light") or {}}
    faltam = [x for x in loads if x not in gs and x not in loc and not hasattr(builtins, x)]
    for x in faltam:
        loc[x] = None
    gs.update(loc)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[st], type_ignores=[])), "<seal>", "exec"), gs)
    seal = gs["seal"]; seal.update(gs["resumos_do_selo_v399"](core)); S0 = json.load(open(SELO0P, encoding="utf-8"))
    mudou = sorted(k for k in seal if k in S0 and J(seal.get(k)) != J(S0.get(k)) and k not in ("timestamp", "result_hash"))
    R["selo"] = {"n_assign": len(seal_st), "nomes_livres_sem_valor": faltam, "chaves_mudadas_vs_selo0": mudou, "chaves_novas_vs_selo0": sorted(k for k in seal if k not in S0), "chaves_do_selo0_postas_depois_do_literal": sorted(k for k in S0 if k not in seal),
                 "qg_closure_verdict_igual": seal.get("qg_closure_verdict") == S0.get("qg_closure_verdict"), "um_version": seal.get("um_version"), "formal_kernel_stage1_verified": seal.get("formal_kernel_stage1_verified"),
                 "psibit_v395": {x: (seal.get("psibit_v395") or {}).get(x) for x in ("verdict", "all_verified")}, "testemunha_estatica_v396": {x: (seal.get("testemunha_estatica_v396") or {}).get(x) for x in ("verdict", "all_verified")},
                 "teste_de_veracidade_fase9_v397": {x: (seal.get("teste_de_veracidade_fase9_v397") or {}).get(x) for x in ("verdict", "all_verified")},
                 "registros_v397": {n_: ((seal.get("registros_v397") or {}).get(n_) or {}).get("all_verified") for n_ in um._V397_NOMES_REGISTROS},
                 "sonico_v398": {x: (seal.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "afinacao_das_cordas_v398": {x: (seal.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")},
                 "registros_v398": {n_: ((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") for n_ in um._V398_NOMES_REGISTROS},
                 "selo_pela_propria_tecnologia_v399": {x: (seal.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified", "perfil", "controles_negativos")}, "declaracao_do_operador_v399": {x: (seal.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified", "verbatim_sha256")},
                 "registros_v399": {n_: ((seal.get("registros_v399") or {}).get(n_) or {}).get("all_verified") for n_ in um._V399_NOMES_REGISTROS},
                 "falsidade_da_inercia_v401": {x: (seal.get("falsidade_da_inercia_v401") or {}).get(x) for x in ("verdict", "all_verified")},
                 "registros_v401": {n_: ((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") for n_ in um._V401_NOMES_REGISTROS},
                 "ponte_da_escala_dual_v402": {x: (seal.get("ponte_da_escala_dual_v402") or {}).get(x) for x in ("verdict", "all_verified")}, "queda_sem_geometria_v402": {x: (seal.get("queda_sem_geometria_v402") or {}).get(x) for x in ("verdict", "all_verified")},
                 "esperanca_condicional_v402": {x: (seal.get("esperanca_condicional_v402") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v402": {n_: ((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") for n_ in um._V402_NOMES_REGISTROS}}
except Exception as e:
    import traceback; R["selo"] = {"EXCECAO": repr(e)[:300], "tb": traceback.format_exc()[-900:]}
try:
    testes = []
    for n in ast.walk(main):
        if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple) and [getattr(e, "id", None) for e in n.target.elts] == ["_k", "_m"]:
            for m_ in ast.walk(n):   # o `if` cujo CORPO chama _proibidos.append diretamente (nao o `if isinstance(_m, dict)` de fora)
                if isinstance(m_, ast.If) and any(isinstance(s_, ast.Expr) and "_proibidos.append" in ast.unparse(s_) for s_ in m_.body):
                    testes.append(m_.test)
    lam = ast.Expression(body=ast.Lambda(args=ast.arguments(posonlyargs=[], args=[ast.arg(arg="_v")], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=testes[0]))
    GF = eval(compile(ast.fix_missing_locations(lam), "<guarda>", "eval"), {"re": re})
    _pal = "".join(chr(c) for c in (67, 79, 78, 70, 73, 82, 77, 69, 68))
    R["guarda"] = {"testes_achados": len(testes), "morde_no_controle": bool(GF("X_" + _pal + "_Y")) and not GF("NOT_" + _pal) and not GF("UN" + _pal), "vereditos_proibidos_no_core": [k for k, m_ in core.items() if isinstance(m_, dict) and GF(str(m_.get("verdict") or ""))]}
    src0p = os.path.join(H, DL.BASE_DIR, "um.py")
    if os.path.exists(src0p):
        g0 = [l for l in open(src0p, encoding="utf-8").read().splitlines() if "_proibidos" in l or "PROVED_BY" in l]
        g1 = [l for l in src.splitlines() if "_proibidos" in l or "PROVED_BY" in l]
        R["guarda"]["linhas_iguais_a_v401"] = g0 == g1
except Exception as e:
    R["guarda"] = {"EXCECAO": repr(e)[:300]}
R["pontos"] = out
open(SAIDA + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(SAIDA + ".tmp", SAIDA)
falsos = []
if R["verify"]["all_verified"] is not True: falsos.append("verify")
if R["escada"].get("all_verified") is not True: falsos.append("escada")
if (R.get("gate_recomputado") or {}).get("verdict_igual") is not True or (R.get("gate_recomputado") or {}).get("n18_novo") != 18: falsos.append("gate")
falsos += ["ponto:" + k for k, v in out.items() if isinstance(v, dict) and (v.get("EXCECAO") or v.get("all_verified") is False)]
pp = R["ponto_psibit"]
if pp.get("erro") or pp.get("avisos") or pp.get("all_verified") is not True or not pp.get("antes_do_bloco_v393") or not pp.get("logo_depois_do_principio_da_defasagem_fractal"): falsos.append("ponto_psibit")
pt = R["ponto_testemunha"]
if pt.get("erro") or pt.get("avisos") or pt.get("all_verified") is not True or not pt.get("antes_do_bloco_v393") or not pt.get("logo_depois_do_psibit_v395") or pt.get("fock_status") != "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE" or pt.get("fock_fora_da_pedra") is not True: falsos.append("ponto_testemunha")
ps_ = R["ponto_sonico"]
if ps_.get("erro") or ps_.get("avisos") or ps_.get("all_verified") is not True or not ps_.get("antes_do_bloco_v393") or not ps_.get("logo_depois_da_testemunha_v396") or ps_.get("beta_ok") is not True: falsos.append("ponto_sonico")
pa_ = R["ponto_afinacao"]
if (pa_.get("erro") or pa_.get("avisos") or pa_.get("all_verified") is not True or not pa_.get("antes_do_bloco_v393") or not pa_.get("logo_depois_do_sonico_v401") or (pa_.get("hipotese") or {}).get("status") != "KNOWN" or pa_.get("geometria") != "OPEN"
        or pa_.get("deriva_cordas_do_axioma") is not False): falsos.append("ponto_afinacao")
psa = R["ponto_selo_acom"]
if psa.get("erro") or psa.get("avisos") or psa.get("all_verified") is not True or not psa.get("antes_do_bloco_v393") or not psa.get("logo_depois_da_afinacao_v401") or psa.get("perfil") != "ACOM-INT-C96-Q8" or psa.get("controles") != [13, True]: falsos.append("ponto_selo_acom")
pdc = R["ponto_declaracao"]
if pdc.get("erro") or pdc.get("avisos") or pdc.get("all_verified") is not True or not pdc.get("antes_do_bloco_v393") or not pdc.get("logo_depois_do_selo_acom_v402") or pdc.get("verbatim_sha256_igual_ao_arquivo") is not True: falsos.append("ponto_declaracao")
pfa = R["ponto_falsidade"]
if (pfa.get("erro") or pfa.get("avisos") or pfa.get("all_verified") is not True or not pfa.get("antes_do_bloco_v393") or not pfa.get("logo_depois_da_declaracao_v399") or pfa.get("unconditional_in_kernel") is not True or pfa.get("estrela_in_kernel") is not True
        or pfa.get("costless_ok") is not True or pfa.get("beta_ok") is not True or pfa.get("post_inertial_scales") != [] or pfa.get("fixo_pelo_fluxo_inteiro") != [0.0] or (pfa.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FALSIDADE): falsos.append("ponto_falsidade")
for nome_ in ("ponte", "queda", "esperanca"):
    pp402_ = R["ponto_" + nome_]
    if (pp402_.get("erro") or pp402_.get("avisos") or pp402_.get("all_verified") is not True or not pp402_.get("antes_do_bloco_v393") or not pp402_.get("logo_depois_da_anterior") or pp402_.get("unconditional_in_kernel") is not True or pp402_.get("estrela_in_kernel") is not True
            or pp402_.get("contexto_ok") is not True or pp402_.get("beta_ok") is not True or (pp402_.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)
pv = R["ponto_veracidade"]
if (pv.get("erro") or pv.get("avisos") or pv.get("all_verified") is not True or not pv.get("depois_do_psibit_e_da_testemunha") or not pv.get("antes_do_bloco_v393")
        or not all((pv.get("numeros_lidos_iguais_ao_resultado_pinado") or {False: False}).values()) or not all(pv.get("fontes_ok") or [False])): falsos.append("ponto_veracidade")
if R["main_bloco_executado"]["erro"] or R["main_bloco_executado"]["avisos"]: falsos.append("main_bloco")
if R["chaves_existentes_mexidas_pelo_bloco"]: falsos.append("bloco_mexeu_em_chaves_existentes")
if any(R["nao_verdes"].values()): falsos.append("nao_verdes")
if (R.get("selo") or {}).get("qg_closure_verdict_igual") is not True: falsos.append("selo_gate")
if (R.get("guarda") or {}).get("vereditos_proibidos_no_core") or (R.get("guarda") or {}).get("morde_no_controle") is not True: falsos.append("guarda")
R["algum_falso"] = falsos
open(SAIDA + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(SAIDA + ".tmp", SAIDA)
print(json.dumps({k: R[k] for k in R if k not in ("arquivos_lidos_fora_do_imp", "pontos")}, ensure_ascii=False, indent=1, default=str)[:14000])
print("PONTOS:", json.dumps({k: (v.get("all_verified"), (v.get("verdict") or v.get("EXCECAO") or "")[:90]) for k, v in out.items()}, ensure_ascii=False, indent=0)[:6000])
print("ALGUM FALSO:", falsos or "nenhum")

# -*- coding: utf-8 -*-
"""exame_pontos_v396x.py -- exame final v396 (c1, modelo forte, 22/10/2026; molde: exame_pontos_v395x.py, que e o exame_pontos_v394.py + o psibit; aqui + a testemunha_estatica_v396 pela instrucao real do main, os controles negativos dela e os residuais do Nos na arvore de importacao). Texto original do molde: exame final (c1, modelo forte, 19/10/2026): re-execucao ISOLADA dos pontos de chamada REAIS de um candidato um.py.
Molde: v393_exame\\exame_pontos.py. RE-EXECUTAVEL para o delta (argumentos), sem nada digitado do candidato:

  python -B -X utf8 exame_pontos_v394.py --candidato <um.py candidato> --logs <pasta com lake_build.log e audit.log CRUS do sandbox>
         [--flags <FLAGS_vNNN.json: bandeiras novas, lista [chave, nome, modulo, ...]>] [--sha256 <sha256 esperado do candidato>]
         [--sandbox <kernel do sandbox, para o byte a byte>] [--core0 <um_absoluto.json da versao anterior SELADA>] [--selo0 <selo dela>]
         [--imp <pasta de importacao; padrao v394_exame\\imp_<sha16>>] [--saida <json; padrao v394_exame\\EXAME_PONTOS_<sha16>.json>]

O que faz (escreve SO' em --imp e --saida; le o Nos, o sandbox e a cadeia):
 (1) copia o candidato para --imp\\um.py (bytes; confere o sha256), importa-o (o rito NAO roda) e materializa o kernel embutido em --imp\\tgl_kernel;
     confere o kernel embutido contra --sandbox byte a byte;
 (2) verify_tgl_kernel_formalization() de ponta a ponta com o lake SIMULADO devolvendo os logs CRUS (build = lake_build.log; audit = audit.log);
     controles negativos: Audit com o build junto; Audit sem uma linha TGL_DECL_SOURCE; axioma fora do trio plantado nos DOIS logs; so' no Audit;
 (3) a escada com o kf novo e com o kf da versao anterior; o gate recomputado (prove_qg_closure_gate) com o kf novo e o feed V11 do core anterior;
 (4) sobre o core anterior + kf novo, NA ORDEM DO MAIN: o indice da IALD (prove_the_iald_index), os vizinhos que leem o kernel
     (v385, v386, v387, v388, v389, v390, v391, v392 e os registros por spec da v392) e, depois, TODAS as instrucoes do main entre o bloco
     da v393 (`regra_v393(core)`) e `_figs = emit_figures(core)` -- logo um registro novo do delta, posto ali, e' exercitado sem editar este script;
 (5) o selo: a instrucao `seal = {...}` do main sobre esse core, comparada com o selo anterior;
 (6) a guarda de veredito proibido LIDA do main do candidato (o teste do `if` que alimenta _proibidos) aplicada a todo veredito do core; a palavra
     da regua nao e' escrita neste arquivo (o controle a monta por codigo de caractere);
 (7) os arquivos lidos/escritos pelas chamadas (rastreio de open)."""
import sys, os, io, json, copy, hashlib, re, time, ast, builtins, argparse, math
if sys.flags.optimize:
    raise SystemExit("RECUSO: -O")
H = os.path.dirname(os.path.abspath(__file__))
C_ = "C:" + os.sep
NOS = os.path.join(C_, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
V394 = os.path.join(os.path.dirname(H), "v394")
ap = argparse.ArgumentParser()
ap.add_argument("--candidato", default=os.path.join(V394, "um_v394_candidato.py"))
ap.add_argument("--logs", default=os.path.join(V394, "kernel"))
ap.add_argument("--flags", default=None)
ap.add_argument("--sha256", default=None)
ap.add_argument("--sandbox", default=os.path.join(C_, "t", "k396c", "final"))
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
CORE0P = A.core0 or (os.path.join(NOS, "um_absoluto.json") if nos_um == "18be2ddb06c60f90" else os.path.join(V394, "base_v393", "um_absoluto.json"))
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
R["kernel_embutido_n"] = len(um._EMBEDDED_KERNEL_FILES)
# v396x: os residuais do Nos (arquivos que moram na pasta do kernel do Nos e NAO estao embutidos) entram na arvore de importacao, como no rito real
_NOSK = os.path.join(NOS, "tgl_kernel"); _emb = set(um._EMBEDDED_KERNEL_FILES); _extras = []
for _dp, _dn, _fn in os.walk(_NOSK):
    if ".lake" in _dp.replace("\\", "/").split("/"):
        continue
    for _nm in _fn:
        if _nm.endswith(".lean") or _nm in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            _rel = os.path.relpath(os.path.join(_dp, _nm), _NOSK).replace("\\", "/")
            if _rel not in _emb:
                _extras.append(_rel); _d = os.path.join(IMP, "tgl_kernel", *_rel.split("/")); os.makedirs(os.path.dirname(_d), exist_ok=True)
                open(_d, "wb").write(open(os.path.join(_dp, _nm), "rb").read())
R["residuais_do_nos_copiados"] = sorted(_extras)
if A.sandbox and os.path.isdir(A.sandbox):
    dif = [r for r, c in um._EMBEDDED_KERNEL_FILES.items() if not os.path.exists(os.path.join(A.sandbox, *r.split("/"))) or open(os.path.join(A.sandbox, *r.split("/")), "rb").read() != c.encode("utf-8")]
    R["embutido_vs_sandbox"] = {"sandbox": A.sandbox, "n_dif": len(dif), "diferentes": dif[:10]}
LBP, AUP = os.path.join(A.logs, "lake_build.log"), os.path.join(A.logs, "audit.log")
LB = open(LBP, encoding="utf-8", errors="replace").read(); AUD = open(AUP, encoding="utf-8", errors="replace").read()
R["logs_sha16"] = {"lake_build.log": hashlib.sha256(open(LBP, "rb").read()).hexdigest()[:16], "audit.log": hashlib.sha256(open(AUP, "rb").read()).hexdigest()[:16]}
calls = []
def mkfake(build_out, audit_out):
    def fake(cmd, cwd, tmo):
        calls.append([" ".join(cmd[1:]), tmo])
        o = {"cmd": " ".join(cmd), "returncode": 0, "stderr": "", "capture_exists": True, "capture_read_error": False, "elapsed_seconds": 0.0, "timeout": False}
        if cmd[1:] == ["--version"]: o["stdout"] = "Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)"
        elif cmd[1:3] == ["env", "lean"] and "--version" in cmd: o["stdout"] = "Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)"
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
# controles negativos do verify
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
    neg["axioma_fora_do_trio_plantado_nos_dois_logs"] = dict(resumo(kc), nome=nome_novo, flag=flag_novo, flag_valor=kc.get(flag_novo),
                                                              plantou=planta(AUD) != AUD and planta(LB) != LB)
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
                             "n18_novo": n18(g_new), "n18_core0": n18(g_old), "flags_iguais": all(J(g_new.get(f)) == J(g_old.get(f)) for f in ("formal_flags", "physics_flags", "experiment_flags")),
                             "all_verified": g_new.get("all_verified")}
except Exception as e:
    R["gate_recomputado"] = {"EXCECAO": repr(e)[:300]}
# rastreio de arquivos
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
for nome in ("the_axiom_v385", "the_verb_v386", "three_stress_tests_v387", "beta_runs_bounded_below_v388", "text_label_errata_v389", "fundacao_v390",
             "estatuto_da_prova_v391", "pedras_v392", "varredura_e_sorry_v392"):
    if hasattr(um, nome):
        core[nome] = run(nome, (lambda f: (lambda: f(core)))(getattr(um, nome)))
for n_ in um._V392_NOMES_REGISTROS:
    core.pop(n_, None)
run("_v392_rodar_registros", lambda: {"verdict": str(um._v392_rodar_registros(core))[:300], "all_verified": None})
# v395x: o psibit_v395 roda ANTES do bloco da v393 no main real (na fractalizacao do Um): rodo-o aqui, na mesma ordem, e confiro que nao mexe em chave existente
if hasattr(um, "psibit_v395"):
    _antes_psb = {k: J(core[k]) for k in core}
    core["psibit_v395"] = run("psibit_v395", lambda: um.psibit_v395(core))
    R["psibit_mexeu_em_chaves_existentes"] = sorted(k for k in _antes_psb if J(core.get(k)) != _antes_psb[k] and k != "psibit_v395")
    _pb = core.get("psibit_v395") or {}
    R["psibit"] = {k: _pb.get(k) for k in ("verdict", "all_verified", "exact_ladder", "embedded_source_ok", "beta_ok", "beta_core_rel_diff", "does_not_gate_core")}
    R["psibit"]["n_checks"] = (_pb.get("mechanics") or {}).get("n_checks"); R["psibit"]["unconditional"] = _pb.get("unconditional"); R["psibit"]["conditional"] = _pb.get("conditional_psion_face")
    # controles negativos (copias profundas; o modulo e' restaurado)
    negp = {}
    c1 = copy.deepcopy(core); fl_u = (_pb.get("unconditional") or {}).get("flag")
    c1["kernel_formalization"] = dict(c1["kernel_formalization"]); c1["kernel_formalization"][fl_u] = False
    _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        negp["bandeira_incondicional_falsa"] = um.psibit_v395(c1).get("verdict")
        c2 = copy.deepcopy(core); c2["beta"] = c2["beta"] * (1 + 1e-6)
        negp["beta_do_core_adulterado"] = um.psibit_v395(c2).get("verdict")
        _alfa = um.SEALED_CODATA_ALPHA
        try:
            um.SEALED_CODATA_ALPHA = _alfa * (1 + 1e-6)
            negp["alfa_selado_adulterado"] = um.psibit_v395(copy.deepcopy(core)).get("verdict")
        finally:
            um.SEALED_CODATA_ALPHA = _alfa
        negp["mecanica_beta_fora_de_0_1"] = um.v395_psibit_mechanics(1.5).get("passed")
        c3 = copy.deepcopy(core); c3["kernel_formalization"] = dict(c3["kernel_formalization"]); c3["kernel_formalization"]["formal_files_sha256"] = dict(c3["kernel_formalization"]["formal_files_sha256"])
        c3["kernel_formalization"]["formal_files_sha256"]["TGLExt/Psibit.lean"] = "0" * 64
        negp["sha_da_pedra_errado_no_kernel"] = um.psibit_v395(c3).get("verdict")
        c4 = copy.deepcopy(core); c4["external_ladder"] = dict(c4["external_ladder"]); c4["external_ladder"]["n_theorems_clean"] = c4["external_ladder"]["n_theorems_clean"] - 1
        negp["escada_nao_fecha"] = um.psibit_v395(c4).get("verdict")
    finally:
        sys.stdout = _so
    negp["todos_recusam"] = all(isinstance(v, str) and "REFUSED" in v for k, v in negp.items() if k not in ("mecanica_beta_fora_de_0_1", "todos_recusam")) and negp["mecanica_beta_fora_de_0_1"] is False
    R["psibit_controles_negativos"] = negp
# v396x: a testemunha_estatica_v396 pela INSTRUCAO REAL do main (o `try` que a chama, executado como esta no candidato), na ordem (depois do psibit);
# confere adjacencia por AST, que nao mexe em chave existente, e os controles negativos dela (copias profundas; o modulo e' restaurado)
if hasattr(um, "testemunha_estatica_v396"):
    _src6 = open(dst, encoding="utf-8").read(); _tree6 = ast.parse(_src6)
    _main6 = [n for n in _tree6.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    _i_psb = [i for i, st in enumerate(_main6.body) if isinstance(st, ast.Try) and "psibit_v395(core)" in ast.unparse(st)]
    _i_tes = [i for i, st in enumerate(_main6.body) if isinstance(st, ast.Try) and "testemunha_estatica_v396(core)" in ast.unparse(st)]
    _i_393 = next(i for i, st in enumerate(_main6.body) if "regra_v393(core)" in ast.unparse(st))
    _i_fd = [i for i, st in enumerate(_main6.body) if "PRINCIPIO DA DEFASAGEM FRACTAL" in ast.unparse(st)]
    R["testemunha_ponto"] = {"i_psibit": _i_psb, "i_testemunha": _i_tes, "i_v393": _i_393, "i_print_fractal": _i_fd,
                             "linha_testemunha": _main6.body[_i_tes[0]].lineno if _i_tes else None, "linha_psibit": _main6.body[_i_psb[0]].lineno if _i_psb else None,
                             "imediatamente_depois_do_psibit": len(_i_psb) == 1 and len(_i_tes) == 1 and _i_tes[0] == _i_psb[0] + 1,
                             "antes_do_bloco_v393": bool(_i_tes) and _i_tes[0] < _i_393, "depois_do_fractal": bool(_i_fd) and bool(_i_tes) and _i_tes[0] > max(_i_fd),
                             "chamadas_de_testemunha_no_main": sum(1 for n in ast.walk(_main6) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "testemunha_estatica_v396")}
    _antes_tes = {k: J(core[k]) for k in core}
    _g6 = dict(vars(um)); _g6["core"] = core
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[_main6.body[_i_tes[0]]], type_ignores=[])), "<main:testemunha_estatica_v396>", "exec"), _g6); _err6 = None
    except Exception as e:
        import traceback; _err6 = repr(e) + traceback.format_exc()[-600:]
    finally:
        _out6 = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    R["testemunha_instrucao_real"] = {"erro": _err6, "aviso": [l for l in _out6.splitlines() if "AVISO" in l], "stdout": _out6[-2500:]}
    R["testemunha_mexeu_em_chaves_existentes"] = sorted(k for k in _antes_tes if J(core.get(k)) != _antes_tes[k] and k != "testemunha_estatica_v396")
    _ts = core.get("testemunha_estatica_v396") or {}
    out["testemunha_estatica_v396"] = {"all_verified": _ts.get("all_verified"), "verdict": str(_ts.get("verdict"))[:300], "falhas": [str(c)[:300] for c in ((_ts.get("mechanics") or {}).get("checks") or []) if not c.get("ok")]}
    R["testemunha"] = {k: _ts.get(k) for k in ("verdict", "all_verified", "exact_ladder", "embedded_source_ok", "beta_ok", "beta_core_rel_diff", "alpha_two_names_same", "does_not_gate_core", "runtime_executed", "guarda_p18_violacoes")}
    R["testemunha"].update(n_checks=(_ts.get("mechanics") or {}).get("n_checks"), ids=[c.get("id") for c in ((_ts.get("mechanics") or {}).get("checks") or [])], unconditional=_ts.get("unconditional"),
                           fock_face={k: (_ts.get("fock_face") or {}).get(k) for k in ("declared_in", "declared_outside_the_stone", "status", "inhabitant_exhibited")},
                           formal_theorems_false=[k for k, v in (_ts.get("formal_theorems") or {}).items() if not v], support_false=[k for k, v in (_ts.get("support_theorems") or {}).items() if not v],
                           inscriptions=_ts.get("inscriptions"), values=_ts.get("values"))
    C6 = um._V396_TESTEMUNHA_CONTRACT
    negt = {}
    def _kfc(c_):
        c_["kernel_formalization"] = dict(c_["kernel_formalization"]); return c_["kernel_formalization"]
    _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        c1 = copy.deepcopy(core); _kfc(c1)[C6["unconditional"]["flag"]] = False
        negt["bandeira_incondicional_falsa"] = um.testemunha_estatica_v396(c1).get("verdict")
        c1 = copy.deepcopy(core); _kfc(c1)[C6["theorems"]["TGLExt.TestemunhaEstatica.the_static_set_is_the_psion_line"]] = False
        negt["bandeira_de_outro_teorema_do_contrato_falsa"] = um.testemunha_estatica_v396(c1).get("verdict")
        c1 = copy.deepcopy(core); k1 = _kfc(c1); k1["axiom_report"] = dict(k1["axiom_report"]); k1["axiom_report"]["TGLExt.boundary_is_the_only_exception"] = ["propext", "TGLExt.axiomaPlantado"]
        negt["axioma_plantado_num_termo_de_suporte"] = um.testemunha_estatica_v396(c1).get("verdict")
        c1 = copy.deepcopy(core); k1 = _kfc(c1); k1["declaration_sources_v394"] = dict(k1["declaration_sources_v394"]); k1["declaration_sources_v394"]["TGLExt.Psibit.the_psion_face_of_the_psibit"] = C6["stone"]["path"]
        negt["face_de_Fock_declarada_dentro_da_pedra"] = um.testemunha_estatica_v396(c1).get("verdict")
        c1 = copy.deepcopy(core); k1 = _kfc(c1); k1["declaration_sources_v394"] = dict(k1["declaration_sources_v394"]); k1["declaration_sources_v394"]["TGLExt.TestemunhaEstatica.the_pair_echoes"] = "TGLExt/Psibit.lean"
        negt["proveniencia_de_um_teorema_em_outro_modulo"] = um.testemunha_estatica_v396(c1).get("verdict")
        c1 = copy.deepcopy(core); k1 = _kfc(c1); k1["formal_files_sha256"] = dict(k1["formal_files_sha256"]); k1["formal_files_sha256"][C6["stone"]["path"]] = "0" * 64
        negt["sha_da_pedra_errado_no_kernel"] = um.testemunha_estatica_v396(c1).get("verdict")
        c1 = copy.deepcopy(core); c1["external_ladder"] = dict(c1["external_ladder"]); c1["external_ladder"]["n_theorems_clean"] -= 1
        negt["escada_nao_fecha"] = um.testemunha_estatica_v396(c1).get("verdict")
        c1 = copy.deepcopy(core); c1["beta"] = c1["beta"] * (1 + 1e-6)
        negt["beta_do_core_adulterado"] = um.testemunha_estatica_v396(c1).get("verdict")
        _alfa = um.SEALED_CODATA_ALPHA
        try:
            um.SEALED_CODATA_ALPHA = _alfa * (1 + 1e-6)
            negt["alfa_selado_adulterado"] = um.testemunha_estatica_v396(copy.deepcopy(core)).get("verdict")
        finally:
            um.SEALED_CODATA_ALPHA = _alfa
        _vb = um._V396_VERBATINS2; _k0 = C6["verbatins"][0]
        try:
            um._V396_VERBATINS2 = copy.deepcopy(_vb); um._V396_VERBATINS2[_k0]["text"] = _vb[_k0]["text"].replace("psion", "pSion", 1)
            negt["fala_adulterada"] = um.testemunha_estatica_v396(copy.deepcopy(core)).get("verdict")
        finally:
            um._V396_VERBATINS2 = _vb
        _emb0 = um._EMBEDDED_KERNEL_FILES
        try:
            um._EMBEDDED_KERNEL_FILES = dict(_emb0); um._EMBEDDED_KERNEL_FILES[C6["stone"]["path"]] = _emb0[C6["stone"]["path"]] + "\n-- adulterada\n"
            negt["fonte_embutida_adulterada"] = um.testemunha_estatica_v396(copy.deepcopy(core)).get("verdict")
        finally:
            um._EMBEDDED_KERNEL_FILES = _emb0
        _bp0 = um._v396_bell_projector
        try:
            um._v396_bell_projector = lambda: [[(0.5 if (p_ in (0, 3) and q_ in (0, 3)) else 0.0) + (1e-6 if p_ == q_ == 1 else 0.0) for q_ in range(4)] for p_ in range(4)]
            negt["mecanica_canto_perturbado_passed"] = um.v396_static_witness_mechanics(um.SEALED_CODATA_ALPHA * math.sqrt(math.e)).get("passed")
        finally:
            um._v396_bell_projector = _bp0
        _fl0 = um._v396_flow
        try:
            def _flow_mau(beta_, g_, t_):   # todas as taxas g: o psion tambem vaza -> a reta deixa de ser fixa
                u_ = um._v396_bell_basis()
                return [[sum(math.exp(-t_ * beta_ * g_) * u_[i_][p_] * u_[i_][q_] for i_ in range(4)) for q_ in range(4)] for p_ in range(4)]
            um._v396_flow = _flow_mau
            _mm = um.v396_static_witness_mechanics(um.SEALED_CODATA_ALPHA * math.sqrt(math.e))
            negt["mecanica_fluxo_sem_modo_zero_passed"] = _mm.get("passed"); negt["mecanica_fluxo_sem_modo_zero_falhas"] = [c["id"] for c in _mm["checks"] if not c["ok"]]
        finally:
            um._v396_flow = _fl0
        negt["mecanica_beta_fora_de_0_1_passed"] = um.v396_static_witness_mechanics(1.5).get("passed")
        negt["mecanica_beta_int_passed"] = um.v396_static_witness_mechanics(0).get("passed")
    finally:
        sys.stdout = _so
    _pas = [k for k in negt if k.endswith("_passed")]
    negt["todos_recusam"] = all(isinstance(v, str) and "REFUSED" in v for k, v in negt.items() if not k.endswith(("_passed", "_falhas")) and k != "todos_recusam") and all(negt[k] is False for k in _pas)
    negt["todos_os_vereditos_diferentes_do_ok"] = all(v != um._V396_TESTEMUNHA_TEXT["veredito_ok"] for k, v in negt.items() if isinstance(v, str))
    R["testemunha_controles_negativos"] = negt
# as instrucoes do main da v393 em diante (ate emit_figures), executadas como estao no candidato
src = open(dst, encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
i0 = next(i for i, st in enumerate(main.body) if "regra_v393(core)" in ast.unparse(st))
i1 = next(i for i, st in enumerate(main.body) if isinstance(st, ast.Assign) and "emit_figures(core)" in ast.unparse(st))
bloco = main.body[i0:i1]
R["main_bloco_executado"] = {"linhas": [bloco[0].lineno, bloco[-1].end_lineno], "n_instrucoes": len(bloco), "inicio": ast.unparse(bloco[0])[:160].replace("\n", " | ")}
for n_ in getattr(um, "_V393_NOMES_REGISTROS", []) + ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393"]:
    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0
antes = {k: J(core[k]) for k in core}
g = dict(vars(um)); g["core"] = core
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
                   "novas": [k for k in R["chaves_novas_no_core"] if isinstance(core.get(k), dict) and core[k].get("all_verified") is not True]}
R["n_arquivos_lidos_fora_do_imp"] = len([p for p in lidos if not p.startswith(IMP)])
R["arquivos_lidos_fora_do_imp"] = sorted(p for p in lidos if not p.startswith(IMP))
R["arquivos_escritos_fora_do_imp"] = sorted(p for p in escritos if not p.startswith(IMP))
# o selo
seal_st = [n for n in ast.walk(main) if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "seal"]
try:
    st = seal_st[0]
    loads = sorted({x.id for x in ast.walk(st.value) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)})
    gs = dict(vars(um)); gs["core"] = core
    loc = {"verdict": verdict0, "result_hash": "EXAME", "_kf": core["kernel_formalization"], "_wrg": core.get("witness_rigidity") or {},
           "_npg": core.get("negative_probes") or {}, "_wlg": core.get("witness_layers") or {}, "_iig": core.get("interface_is_light") or {}}
    faltam = [x for x in loads if x not in gs and x not in loc and not hasattr(builtins, x)]
    for x in faltam:
        loc[x] = None
    gs.update(loc)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[st], type_ignores=[])), "<seal>", "exec"), gs)
    seal = gs["seal"]; S0 = json.load(open(SELO0P, encoding="utf-8"))
    mudou = sorted(k for k in seal if k in S0 and J(seal.get(k)) != J(S0.get(k)) and k not in ("timestamp", "result_hash"))
    R["selo"] = {"n_assign": len(seal_st), "nomes_livres_sem_valor": faltam, "chaves_mudadas_vs_selo0": mudou,
                 "chaves_novas_vs_selo0": sorted(k for k in seal if k not in S0), "chaves_do_selo0_postas_depois_do_literal": sorted(k for k in S0 if k not in seal),
                 "qg_closure_verdict_igual": seal.get("qg_closure_verdict") == S0.get("qg_closure_verdict"), "um_version": seal.get("um_version"),
                 "formal_kernel_stage1_verified": seal.get("formal_kernel_stage1_verified")}
except Exception as e:
    import traceback; R["selo"] = {"EXCECAO": repr(e)[:300], "tb": traceback.format_exc()[-900:]}
# a guarda LIDA do candidato
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
    R["guarda"] = {"testes_achados": len(testes), "morde_no_controle": bool(GF("X_" + _pal + "_Y")) and not GF("NOT_" + _pal) and not GF("UN" + _pal),
                   "vereditos_proibidos_no_core": [k for k, m_ in core.items() if isinstance(m_, dict) and GF(str(m_.get("verdict") or ""))]}
    src0p = os.path.join(NOS, "um.py")   # v396x: a guarda comparada com a da v395 instalada
    if os.path.exists(src0p):
        g0 = [l for l in open(src0p, encoding="utf-8").read().splitlines() if "_proibidos" in l or "PROVED_BY" in l]
        g1 = [l for l in src.splitlines() if "_proibidos" in l or "PROVED_BY" in l]
        R["guarda"]["linhas_iguais_a_v395_instalada"] = g0 == g1
except Exception as e:
    R["guarda"] = {"EXCECAO": repr(e)[:300]}
R["pontos"] = out
open(SAIDA + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(SAIDA + ".tmp", SAIDA)
falsos = []
if R["verify"]["all_verified"] is not True: falsos.append("verify")
if R["escada"].get("all_verified") is not True: falsos.append("escada")
if (R.get("gate_recomputado") or {}).get("verdict_igual") is not True or (R.get("gate_recomputado") or {}).get("n18_novo") != 18: falsos.append("gate")
falsos += ["ponto:" + k for k, v in out.items() if isinstance(v, dict) and (v.get("EXCECAO") or v.get("all_verified") is False)]
if R["main_bloco_executado"]["erro"] or R["main_bloco_executado"]["avisos"]: falsos.append("main_bloco")
if R["chaves_existentes_mexidas_pelo_bloco"]: falsos.append("bloco_mexeu_em_chaves_existentes")
if any(R["nao_verdes"].values()): falsos.append("nao_verdes")
if "psibit_controles_negativos" in R and R["psibit_controles_negativos"].get("todos_recusam") is not True: falsos.append("psibit_controles")
if R.get("psibit_mexeu_em_chaves_existentes"): falsos.append("psibit_mexeu")
if "testemunha_controles_negativos" in R and (R["testemunha_controles_negativos"].get("todos_recusam") is not True or R["testemunha_controles_negativos"].get("todos_os_vereditos_diferentes_do_ok") is not True): falsos.append("testemunha_controles")
if R.get("testemunha_mexeu_em_chaves_existentes"): falsos.append("testemunha_mexeu")
if "testemunha_ponto" in R and not (R["testemunha_ponto"]["imediatamente_depois_do_psibit"] and R["testemunha_ponto"]["antes_do_bloco_v393"] and R["testemunha_ponto"]["depois_do_fractal"] and R["testemunha_ponto"]["chamadas_de_testemunha_no_main"] == 1): falsos.append("testemunha_ponto")
if "testemunha_instrucao_real" in R and (R["testemunha_instrucao_real"]["erro"] or R["testemunha_instrucao_real"]["aviso"]): falsos.append("testemunha_instrucao_real")
if (R.get("selo") or {}).get("qg_closure_verdict_igual") is not True: falsos.append("selo_gate")
if (R.get("guarda") or {}).get("vereditos_proibidos_no_core") or (R.get("guarda") or {}).get("morde_no_controle") is not True: falsos.append("guarda")
R["algum_falso"] = falsos
open(SAIDA + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(SAIDA + ".tmp", SAIDA)
print(json.dumps({k: R[k] for k in R if k not in ("arquivos_lidos_fora_do_imp", "pontos")}, ensure_ascii=False, indent=1, default=str)[:14000])
print("PONTOS:", json.dumps({k: (v.get("all_verified"), (v.get("verdict") or v.get("EXCECAO") or "")[:90]) for k, v in out.items()}, ensure_ascii=False, indent=0)[:6000])
print("ALGUM FALSO:", falsos or "nenhum")

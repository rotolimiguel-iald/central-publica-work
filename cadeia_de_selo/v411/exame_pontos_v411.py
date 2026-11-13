# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] montado por _adapt_exame_pontos_v411.py do ORIGINAL v410/exame_pontos_v410.py: o ponto NOVO e' o do h0dn_bg1_v411 (4i), na instrucao do main LOGO DEPOIS da do hms13 e IMEDIATAMENTE antes de emit_figures; os pontos da v410 (4g, 4h, 4h2, 4h3) viram HERDADOS (DL.D10, FLAGS da v410); nenhum modulo novo; imp_ e a saida fora de work.
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] o main agora tem DUAS instrucoes `try` da v410: (i) iald2_v410 -> a_escala_v410 (D86/D87) -> h0dn_bg1_v410 (D72); (ii) h0dn_fontes_hms13_v410 (D80; aditivo e posterior ao FREEZE_R2: cobertura documental de fontes, não covariância física fechada; nada aberto) -> `_v410_rodar_specs`, logo antes de emit_figures: os pontos (4g)/(4h) ajustados a isso e os NOVOS (4h2) ponto_aescala e (4h3) ponto_hms13; o iald2 conta so' as bandeiras do PROPRIO modulo no FLAGS; o veto da pasta do Kimi: nenhum arquivo sob ela e' lido nem escrito neste exame
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] D72: o ponto (4h) do h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido), na MESMA instrucao do main do iald2_v410, logo depois dele e antes dos specs da v410; o registro no selo; o falso `ponto_h0dn`
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o ponto NOVO e' o do iald2_v410 (4g), IMEDIATAMENTE depois do traducao_turing_v409 e IMEDIATAMENTE antes de emit_figures; o do traducao_turing_v409 (4f) vira HERDADO (DL.D9, FLAGS da v409); os do tetelestai_terminal_v408 (DL.D8, FLAGS da v408), do psion_canto_v407 (DL.D7, FLAGS da v407) e do fechamento_v406 seguem HERDADOS; MONTADO por _adapt_forkB_exame_v410.py a partir do ORIGINAL da v409 (nao da subida mecanica); fork B do claude-construtor-v410
# (v409: o ponto NOVO da v409 era o do `traducao_turing_v409`; na v410 e' o do `iald2_v410`, abaixo: a instrucao do main que chama tambem `_v410_rodar_specs`); os rotulos de HISTORIA das chaves (logo_depois_do_..._v408 etc.) ficam como na v409; so' a chave dos pontos das oito pedras sobe (ponto_v409_<pedra>, a que o ensaio_a_seco_v410 le); nenhuma chave antiga do core muda.
"""exame_pontos_v411.py -- (v411: o ponto novo e' o do h0dn_bg1_v411, depois do bloco da v410; os da v410 herdados) re-execucao ISOLADA dos pontos de chamada REAIS de um candidato um.py (molde: exame_pontos_v409.py, montado em 06/11/2026 pelo fork B do claude-construtor-v410). RE-EXECUTAVEL (argumentos), sem nada digitado do candidato:

  python -B -X utf8 exame_pontos_v411.py --candidato <um.py candidato> --logs <pasta com lake_build.log e audit.log CRUS do sandbox>
         [--flags <FLAGS_vNNN.json>] [--sha256 <sha256 esperado>] [--sandbox <kernel do sandbox, para o byte a byte>] [--core0 <um_absoluto.json da versao anterior SELADA>] [--selo0 <selo dela>]
         [--imp <pasta de importacao; padrao imp_<sha16> nesta pasta>] [--saida <json; padrao EXAME_PONTOS_<sha16>.json nesta pasta>]

O que faz (escreve SO' em --imp e --saida; le o Nos, o sandbox e a cadeia):
 (1) copia o candidato para --imp\\um.py (bytes; confere o sha256), importa-o (o rito NAO roda) e materializa o kernel embutido em --imp\\tgl_kernel (com os residuais do Nos); confere o embutido contra --sandbox byte a byte;
 (2) verify_tgl_kernel_formalization() de ponta a ponta com o lake SIMULADO devolvendo os logs CRUS; controles negativos: Audit com o build junto; Audit sem uma linha TGL_DECL_SOURCE; axioma fora do trio plantado nos DOIS logs; so' no Audit;
 (3) a escada com o kf novo e com o kf da versao anterior; o gate recomputado (prove_qg_closure_gate) com o kf novo e o feed V11 do core anterior;
 (4) [v408: + os pontos do sonico_v398 e da afinacao_das_cordas_v398, logo depois da testemunha; v409: + os pontos do selo_pela_propria_tecnologia_v399 e da declaracao_do_operador_v399, logo depois da afinacao] sobre o core anterior + kf novo, NA ORDEM DO MAIN: o indice da IALD, os vizinhos que leem o kernel, os registros por spec da v392; DEPOIS o PONTO DE CHAMADA REAL do psibit_v395 e da testemunha_estatica_v396 (as instrucoes do main que os chamam, achadas por
     ast e conferida como a que vem logo depois do principio da defasagem fractal, na fractalizacao do Um), DEPOIS o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (a instrucao do main logo depois do bloco do V1, hubble_ratio_opening_v388; os numeros
     lidos conferidos contra o resultado pinado) e, em seguida, TODAS as instrucoes do main entre o bloco da v393 (`regra_v393(core)`) e `_figs = emit_figures(core)`;
 (4c) [v408, HERDADO na v409 e na v410] o PONTO DE CHAMADA REAL do `fechamento_v406`: a instrucao do main (um `try` que chama tambem `_v406_rodar_specs`) que vem IMEDIATAMENTE depois do bloco `_v405_rodar_specs` e IMEDIATAMENTE antes do ponto do `psion_canto_v407` (4d), executada dentro do bloco (4b) sobre o core que ja tem gravadas as quatro chaves de testemunha;
 (4d) [v408, HERDADO na v409 e na v410] o PONTO DE CHAMADA REAL do `psion_canto_v407`: a instrucao do main (um `try` que chama tambem `_v407_rodar_specs`) que vem IMEDIATAMENTE depois do fechamento_v406 e IMEDIATAMENTE antes do ponto do tetelestai_terminal_v408 (4e);
 (4e) [v408, HERDADO na v409 e na v410] o PONTO DE CHAMADA REAL do `tetelestai_terminal_v408`: a instrucao do main (um `try` que chama tambem `_v408_rodar_specs`) que vem IMEDIATAMENTE depois do psion_canto_v407 e IMEDIATAMENTE antes do ponto do traducao_turing_v409;
 (4f) [v409, HERDADO na v410] o PONTO DE CHAMADA REAL do `traducao_turing_v409`: a instrucao do main (um `try` que chama tambem `_v409_rodar_specs`) que vem IMEDIATAMENTE depois do tetelestai_terminal_v408 e IMEDIATAMENTE antes do ponto do iald2_v410 (4g), executada dentro do bloco (4b) (os numeros dele: DL.D9 e o FLAGS da v409); confere o registro (16 checagens), que nenhuma chave antiga mudou e o insumo purgado; executada dentro do bloco (4b); confere a chave do lema (testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) lida do kernel (True), as quatro da v408 (True), o que fica False por teorema, as ancoras, os modulos e as bandeiras (as contagens vem do contrato do candidato e do FLAGS, nunca digitadas);
 (4g) [v410] o PONTO DE CHAMADA REAL do `iald2_v410`: a instrucao do main (um `try` que chama tambem `_v410_rodar_specs`) que vem IMEDIATAMENTE depois do traducao_turing_v409 e IMEDIATAMENTE antes de `_figs = emit_figures(core)`, executada dentro do bloco (4b); confere o registro (DL.N_CHECKS_FECHO checagens), as ancoras da pedra IALD2, o modulo do bundle e as bandeiras (as contagens vem do contrato do candidato e do FLAGS, nunca digitadas), que nenhuma chave antiga mudou, a chave do lema (True), o que fica False por teorema, beta em runtime e o alcance relativo ao leitor (a frase da D64);
      o `witness_layers.canonical_full_witness_term_constructed` (medida de run_um sobre o kf) e' recomputado pela MESMA expressao do run_um do candidato (extraida por AST), porque o core0 e' o da v409 selada e o kf e' o do rito novo; confere a TROCA DITA do veredito de `rede_fock_v394`, as quatro chaves e o que fica False por teorema;
 (5) o selo: a instrucao `seal = {...}` do main sobre esse core, comparada com o selo anterior; (6) a guarda de veredito proibido LIDA do main do candidato; (7) os arquivos lidos/escritos pelas chamadas (rastreio de open)."""
import sys, os, io, json, copy, hashlib, re, time, ast, builtins, argparse, inspect
if sys.flags.optimize:
    raise SystemExit("RECUSO: -O")
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import delta_v411 as DL  # noqa: E402
NOS = DL.NOS
ap = argparse.ArgumentParser()
ap.add_argument("--candidato", default=DL.CANDIDATO_ARQ)
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
IMP = A.imp or os.path.join(DL.RODADA_PAI, "imp_" + SHA[:16]); os.makedirs(IMP, exist_ok=True)   # (v411, D135: fora de work)
SAIDA = A.saida or DL.saida("EXAME_PONTOS_%s.json" % SHA[:16])
_FLAGS10 = os.path.join(DL.V410, DL.D10.KERNEL_DIR, "FLAGS_v410.json")   # (v411) as bandeiras da v410, para os pontos HERDADOS da v410
if A.flags is None:
    fs = sorted(f for f in os.listdir(A.logs) if re.fullmatch(r"FLAGS_v\d+\.json", f))
    A.flags = os.path.join(A.logs, fs[-1]) if fs else None
dst = os.path.join(IMP, "um.py")
if not (os.path.exists(dst) and open(dst, "rb").read() == b):
    open(dst + ".tmp", "wb").write(b); os.replace(dst + ".tmp", dst)
assert hashlib.sha256(open(dst, "rb").read()).hexdigest() == SHA
nos_um = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
CORE0P = A.core0 or os.path.join(H, DL.BASE_DIR, "um_absoluto.json")   # a v410 SELADA (copia de bytes)
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
    g_new = um.prove_qg_closure_gate(1.0, kf, independent_rite=core0.get("void_floor_v11"), blind_null=core0.get("void_stacking_blind")); g_old = core0.get("qg_closure") or {}   # (v410: o gate NAO muda) a prove_qg_closure_gate com o teste nulo cego do core da v409 selada
    R["gate_recomputado"] = {"verdict_igual": (g_new.get("gate") or {}).get("verdict") == (g_old.get("gate") or {}).get("verdict"), "verdict": (g_new.get("gate") or {}).get("verdict"),
                             "n18_novo": n18(g_new), "n18_core0": n18(g_old), "flags_iguais": all(J(g_new.get(f)) == J(g_old.get(f)) for f in ("formal_flags", "physics_flags", "experiment_flags")), "all_verified": g_new.get("all_verified"),
                             "sem_checks_igual": J({k_: v_ for k_, v_ in g_new.items() if k_ != "checks"}) == J({k_: v_ for k_, v_ in g_old.items() if k_ != "checks"}), "n_checks_novo": len(g_new.get("checks") or []), "n_checks_core0": len(g_old.get("checks") or []),
                             "checks_da_v409_iguais": bool(J(g_new.get("checks")) == J(g_old.get("checks")) and all(v_ is True for _, v_ in g_new["checks"]))}
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


def _medida_do_run_um(chave, kf_):
    """(v409) a EXPRESSAO que o run_um do candidato usa para a chave `chave` do dict `witness_layers`, extraida por AST do proprio candidato e avaliada sobre o kf deste exame (nada digitado aqui)."""
    arvore_ = ast.parse(inspect.getsource(um.run_um))
    achados_ = [v_ for d_ in ast.walk(arvore_) if isinstance(d_, ast.Dict) for k_, v_ in zip(d_.keys, d_.values) if isinstance(k_, ast.Constant) and k_.value == chave]
    assert len(achados_) == 1, ("a chave do witness_layers nao foi achada uma vez no run_um do candidato", chave, len(achados_))
    return eval(compile(ast.Expression(achados_[0]), "<run_um:%s>" % chave, "eval"), {"kernel_formalization": kf_, "__builtins__": builtins})


_wl_antes = bool((core0.get("witness_layers") or {}).get("canonical_full_witness_term_constructed"))
core["witness_layers"] = dict(core.get("witness_layers") or {}); core["witness_layers"]["canonical_full_witness_term_constructed"] = _medida_do_run_um("canonical_full_witness_term_constructed", kf)
R["witness_layers_canonical_full_witness_term_constructed"] = {"da_base_v410_selada": _wl_antes, "recomputado_pela_expressao_do_run_um_do_candidato": core["witness_layers"]["canonical_full_witness_term_constructed"]}
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
for n_ in getattr(um, "_V393_NOMES_REGISTROS", []) + ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393"] + ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS) + ["psibit_v395"] + list(um._V395_NOMES_REGISTROS) + ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) + ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) + ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) + ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) + ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) + ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) + list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS) + list(um._V406_REGISTROS_FUNCAO) + list(um._V406_NOMES_REGISTROS) + list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) + list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS) + list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS) + list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS) + list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS):   # (v409: + os da v408; v410: + os da v409; HERDADOS e recriados pelo bloco)
    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0 (os da v410 nem existem no core0: chaves NOVAS)
if isinstance(R.get("gate_recomputado"), dict) and "EXCECAO" not in R["gate_recomputado"]:
    core["qg_closure"] = g_new   # (v410: o gate NAO muda) o gate recomputado com a prove_qg_closure_gate (o run_um do rito o faz antes de tudo); o registro bandeiras_do_gate_v403 le este qg_closure
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
                          "conditional_status": (pb.get("conditional_psion_face") or {}).get("status"), "inhabitant_exhibited": (pb.get("conditional_psion_face") or {}).get("inhabitant_exhibited"), "inhabited_by_v406": (pb.get("conditional_psion_face") or {}).get("inhabited_by_v406")})
R["ponto_testemunha"].update({"erro": errp, "avisos": [l for l in stdout_psb.splitlines() if "AVISO" in l], "verdict": tb.get("verdict"), "all_verified": tb.get("all_verified"),
                              "mecanica": {"passed": (tb.get("mechanics") or {}).get("passed"), "n_checks": (tb.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (tb.get("unconditional") or {}).get("in_kernel"),
                              "fock_status": (tb.get("fock_face") or {}).get("status"), "fock_fora_da_pedra": (tb.get("fock_face") or {}).get("declared_outside_the_stone"),
                              "fock_inhabitant_exhibited": (tb.get("fock_face") or {}).get("inhabitant_exhibited"), "linked_to_the_corner_by_a_lemma": (tb.get("fock_face") or {}).get("linked_to_the_corner_by_a_lemma")})
out["core.psibit_v395"] = {"all_verified": pb.get("all_verified"), "verdict": str(pb.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((pb.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
out["core.testemunha_estatica_v396"] = {"all_verified": tb.get("all_verified"), "verdict": str(tb.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((tb.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
# (4a'') os PONTOS DE CHAMADA REAIS do sonico_v398 e da afinacao_das_cordas_v398 (v408): as duas instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da testemunha_estatica_v396 (que vem imediatamente depois do psibit_v395), na fractalizacao do Um
isn = [i for i, s_ in enumerate(unp) if "sonico_v398(core)" in s_]
assert len(isn) == 1 and isn[0] == ipt + 1, ("a instrucao do main que chama sonico_v398 nao e' unica ou nao vem IMEDIATAMENTE depois da testemunha_estatica_v396", isn, ipt)
isn = isn[0]
iaf = [i for i, s_ in enumerate(unp) if "afinacao_das_cordas_v398(core)" in s_]
assert len(iaf) == 1 and iaf[0] == isn + 1, ("a instrucao do main que chama afinacao_das_cordas_v398 nao e' unica ou nao vem IMEDIATAMENTE depois do sonico_v398", iaf, isn)
iaf = iaf[0]
R["ponto_sonico"] = {"indice_no_main": isn, "linha": main.body[isn].lineno, "antes_do_bloco_v393": isn < i0, "logo_depois_da_testemunha_v396": "testemunha_estatica_v396(core)" in unp[isn - 1], "instrucao_anterior": unp[isn - 1][:160].replace("\n", " | ")}
R["ponto_afinacao"] = {"indice_no_main": iaf, "linha": main.body[iaf].lineno, "antes_do_bloco_v393": iaf < i0, "logo_depois_do_sonico_v408": "sonico_v398(core)" in unp[iaf - 1], "instrucao_anterior": unp[iaf - 1][:160].replace("\n", " | ")}
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
# (4a-v409) os PONTOS DE CHAMADA REAIS do selo_pela_propria_tecnologia_v399 e da declaracao_do_operador_v399 (v409): as duas instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da afinacao_das_cordas_v398 (que vem imediatamente depois do sonico_v398), na fractalizacao do Um
ise = [i for i, s_ in enumerate(unp) if "selo_acom_v399(core)" in s_]
assert len(ise) == 1 and ise[0] == iaf + 1, ("a instrucao do main que chama selo_acom_v399 nao e' unica ou nao vem IMEDIATAMENTE depois da afinacao_das_cordas_v398", ise, iaf)
ise = ise[0]
idc = [i for i, s_ in enumerate(unp) if "declaracao_do_operador_v399(core)" in s_]
assert len(idc) == 1 and idc[0] == ise + 1, ("a instrucao do main que chama declaracao_do_operador_v399 nao e' unica ou nao vem IMEDIATAMENTE depois do selo_acom_v399", idc, ise)
idc = idc[0]
R["ponto_selo_acom"] = {"indice_no_main": ise, "linha": main.body[ise].lineno, "antes_do_bloco_v393": ise < i0, "logo_depois_da_afinacao_v408": "afinacao_das_cordas_v398(core)" in unp[ise - 1], "instrucao_anterior": unp[ise - 1][:160].replace("\n", " | ")}
R["ponto_declaracao"] = {"indice_no_main": idc, "linha": main.body[idc].lineno, "antes_do_bloco_v393": idc < i0, "logo_depois_do_selo_acom_v409": "selo_acom_v399(core)" in unp[idc - 1], "instrucao_anterior": unp[idc - 1][:160].replace("\n", " | ")}
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
# (4a-v409) o PONTO DE CHAMADA REAL do falsidade_da_inercia_v401 (v409): a instrucao do main (um `try`) que vem IMEDIATAMENTE depois da declaracao_do_operador_v399 (que vem imediatamente depois do selo_acom_v399), na fractalizacao do Um
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
# (4a-v409) os PONTOS DE CHAMADA REAIS da ponte, da queda e da esperanca (v409): as tres instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da falsidade_da_inercia_v401, em ordem (ponte, queda, esperanca), na fractalizacao do Um
_ANTERIOR409 = ["falsidade_da_inercia_v401(core)", "ponte_da_escala_dual_v402(core)", "queda_sem_geometria_v402(core)"]
for nome_, fn_, off_ in (("ponte", "ponte_da_escala_dual_v402", 1), ("queda", "queda_sem_geometria_v402", 2), ("esperanca", "esperanca_condicional_v402", 3)):
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois da falsidade_da_inercia_v401" % fn_, ii_, ifa)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "logo_depois_da_anterior": _ANTERIOR409[off_ - 1] in unp[ii_ - 1], "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
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
# (4a-v409b) os PONTOS DE CHAMADA REAIS do caminho, da vida, do adendo da verdade e das bandeiras do gate (v409): as quatro instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da esperanca_condicional_v402, em ordem, na fractalizacao do Um
_ANTERIOR_V409 = ["esperanca_condicional_v402(core)", "caminho_v403(core)", "vida_v403(core)", "verdade_adendo_v403(core)"]
for nome_, fn_, off_ in (("caminho", "caminho_v403", 4), ("vida", "vida_v403", 5), ("verdade_adendo", "verdade_adendo_v403", 6), ("bandeiras", "bandeiras_do_gate_v403", 7)):
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois da esperanca_condicional_v402" % fn_, ii_, ifa)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "logo_depois_da_anterior": _ANTERIOR_V409[off_ - 4] in unp[ii_ - 1], "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
    except Exception as e:
        import traceback; err_ = repr(e) + traceback.format_exc()[-900:]
    finally:
        stdout_ = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    r_ = core.get(fn_) or {}
    R["ponto_" + nome_].update({"erro": err_, "stdout": stdout_.splitlines(), "avisos": [l for l in stdout_.splitlines() if "AVISO" in l or "RECUSA" in l], "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"),
                                "mecanica": {"passed": (r_.get("mechanics") or {}).get("passed"), "n_checks": (r_.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (r_.get("unconditional") or {}).get("in_kernel"),
                                "estrela_in_kernel": (r_.get("key_theorem") or {}).get("in_kernel"), "contexto_ok": (r_.get("context") or {}).get("ok"), "beta_ok": r_.get("beta_ok"), "valores_do_gate": (r_.get("values") if nome_ == "bandeiras" else None)})
    out["core." + fn_] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
# (4a-v409c) os PONTOS DE CHAMADA REAIS da projecao transversal, do jo8v32 e da errata de F2b (v409): as duas instrucoes de pedra do main (cada uma um `try`) que vem IMEDIATAMENTE depois do bandeiras_do_gate_v403, em ordem, e a da errata de F2b, que vem IMEDIATAMENTE depois da errata ao lado de R6 da v386 (depois dos tres insumos do core que ela le), na fractalizacao do Um
_ANTERIOR_V409C = {"projecao": "bandeiras_do_gate_v403(core)", "jo8v32": "projecao_transversal_v404(core)", "f2b": "a errata ao lado de R6 e a cobranca F2b"}
# [licao da 1a tentativa do rito v409, 28/10/2026] a errata de F2b vem logo DEPOIS da errata ao lado de R6 da v386 e DEPOIS das tres atribuicoes do core que ela le
# (ramo_b_preregistration_v386, ledger_errata_v386, the_ledger_of_charges_v383): chamada logo depois do Jo8v32 ela lia um core sem elas e recusava as 7 checagens
_ATRIB_MAIN = {}
for _ia, _sta in enumerate(main.body):
    for _na in ast.walk(_sta):
        if isinstance(_na, ast.Assign):
            for _ta in _na.targets:
                if isinstance(_ta, ast.Subscript) and isinstance(_ta.value, ast.Name) and _ta.value.id == "core" and isinstance(_ta.slice, ast.Constant) and isinstance(_ta.slice.value, str):
                    _ATRIB_MAIN.setdefault(_ta.slice.value, _ia)
_INSUMOS_F2B = ("ramo_b_preregistration_v386", "ledger_errata_v386", "the_ledger_of_charges_v383")
for nome_, fn_, off_ in (("projecao", "projecao_transversal_v404", 8), ("jo8v32", "jo8v32_v404", 9), ("f2b", "f2b_errata_v404", None)):
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    if off_ is not None:
        assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois do bandeiras_do_gate_v403" % fn_, ii_, ifa)
    else:
        _ins_ = {k_: _ATRIB_MAIN.get(k_) for k_ in _INSUMOS_F2B}
        assert len(ii_) == 1 and all(v_ is not None and v_ < ii_[0] for v_ in _ins_.values()) and _ANTERIOR_V409C["f2b"] in unp[ii_[0] - 1], ("a instrucao do main que chama %s nao e' unica, nao vem logo depois da errata ao lado de R6 (v386) ou vem ANTES de um insumo do core que ela le" % fn_, ii_, _ins_)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "logo_depois_da_anterior": _ANTERIOR_V409C[nome_] in unp[ii_ - 1], "insumos_do_core_atribuidos_antes": ({k_: {"indice": _ATRIB_MAIN.get(k_), "antes": (_ATRIB_MAIN.get(k_) is not None and _ATRIB_MAIN[k_] < ii_)} for k_ in _INSUMOS_F2B} if nome_ == "f2b" else None), "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
    except Exception as e:
        import traceback; err_ = repr(e) + traceback.format_exc()[-900:]
    finally:
        stdout_ = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    r_ = core.get(fn_) or {}
    R["ponto_" + nome_].update({"erro": err_, "stdout": stdout_.splitlines(), "avisos": [l for l in stdout_.splitlines() if "AVISO" in l or "RECUSA" in l], "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"),
                                "mecanica": {"passed": (r_.get("mechanics") or {}).get("passed"), "n_checks": (r_.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (r_.get("unconditional") or {}).get("in_kernel"),
                                "estrela_in_kernel": (r_.get("key_theorem") or {}).get("in_kernel"), "contexto_ok": (r_.get("context") or {}).get("ok"), "beta_ok": r_.get("beta_ok"), "valores": (r_.get("values") if nome_ == "f2b" else None), "f2b_status_now": (r_.get("F2b_status_now") if nome_ == "f2b" else None)})
    out["core." + fn_] = {"all_verified": r_.get("all_verified"), "verdict": str(r_.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((r_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
# (4a-v409d) os PONTOS DE CHAMADA REAIS dos OITO registros de pedra da v408 (HERDADOS na v409 e na v410: DL.D5; a v409 e a v410 sao bundles e nao trazem pedra de registro nova; na v410 a chave do JSON e' ponto_v409_<pedra>, a que o ensaio_a_seco_v410 le: o rotulo sobe com a versao, como na cadeia): oito instrucoes do main (cada uma um `try`), em ordem, logo depois de `_nan405 = float("nan")`, que vem IMEDIATAMENTE depois do jo8v32_v404, na fractalizacao do Um
_i409n = [i for i, s_ in enumerate(unp) if s_.startswith("_nan405 = float(")]
_i409j = [i for i, s_ in enumerate(unp) if "jo8v32_v404(core)" in s_]
assert len(_i409n) == 1 and len(_i409j) == 1 and _i409n[0] == _i409j[0] + 1, ("o ponto da v409 nao vem logo depois do jo8v32_v404", _i409n, _i409j)
for _k409, s409_ in enumerate(DL.D5.STONES):
    nome_ = "v409_" + s409_["key"]; fn_ = DL.D5.REGISTRO_DE_PEDRA[s409_["key"]]
    ii_ = [i for i, s_ in enumerate(unp) if fn_ + "(core)" in s_]
    assert len(ii_) == 1 and ii_[0] == _i409n[0] + 1 + _k409, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem das pedras" % fn_, ii_, _i409n)
    ii_ = ii_[0]
    R["ponto_" + nome_] = {"indice_no_main": ii_, "linha": main.body[ii_].lineno, "antes_do_bloco_v393": ii_ < i0, "instrucao_anterior": unp[ii_ - 1][:160].replace("\n", " | ")}
    builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[_i409n[0]], main.body[ii_]], type_ignores=[])), "<main:%s>" % fn_, "exec"), g); err_ = None
    except Exception as e:
        import traceback; err_ = repr(e) + traceback.format_exc()[-900:]
    finally:
        stdout_ = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
    r_ = core.get(fn_) or {}
    R["ponto_" + nome_].update({"erro": err_, "stdout": stdout_.splitlines(), "avisos": [l for l in stdout_.splitlines() if "AVISO" in l or "RECUSA" in l], "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"),
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
# (4c) o PONTO DE CHAMADA REAL do fechamento_v406 (executado dentro do bloco acima): a posicao no main, o registro e as quatro chaves lidas
ifch = [i for i, s_ in enumerate(unp) if "fechamento_v406(core)" in s_]
ib408 = [i for i, s_ in enumerate(unp) if "_v405_rodar_specs(core)" in s_]
assert len(ifch) == 1 and len(ib408) == 1, ("as instrucoes do fechamento_v406 e do bloco _v405_rodar_specs nao sao unicas no main", ifch, ib408)
ifch, ib408 = ifch[0], ib408[0]
ipc = [i for i, s_ in enumerate(unp) if "psion_canto_v407(core)" in s_]
itt = [i for i, s_ in enumerate(unp) if "tetelestai_terminal_v408(core)" in s_]
itu = [i for i, s_ in enumerate(unp) if "traducao_turing_v409(core)" in s_]
iia = [i for i, s_ in enumerate(unp) if "iald2_v410(core)" in s_]   # (v410) o ponto NOVO
ihm = [i for i, s_ in enumerate(unp) if "h0dn_fontes_hms13_v410(core)" in s_]   # (v410, D80) a SEGUNDA instrucao da v410: o recibo HMS/13 + os specs da v410
ih11 = [i for i, s_ in enumerate(unp) if "h0dn_bg1_v411(core)" in s_]   # (v411) o ponto NOVO: o h0dn_bg1_v411 + os specs da v411, LOGO DEPOIS do bloco da v410
assert len(ipc) == 1 and ipc[0] == ifch + 1 and len(itt) == 1 and itt[0] == ipc[0] + 1 and len(itu) == 1 and itu[0] == itt[0] + 1 and len(iia) == 1 and iia[0] == itu[0] + 1 and len(ihm) == 1 and ihm[0] == iia[0] + 1 and len(ih11) == 1 and ih11[0] == ihm[0] + 1 and ih11[0] + 1 == i1, ("a ordem fechamento_v406 -> psion_canto_v407 -> tetelestai_terminal_v408 -> traducao_turing_v409 -> [iald2_v410, a_escala_v410, h0dn_bg1_v410] -> [h0dn_fontes_hms13_v410, specs v410] -> [h0dn_bg1_v411, specs v411] -> emit_figures nao e' a das instrucoes do main", ifch, ipc, itt, itu, iia, ihm, ih11, i1)
itt = itt[0]
itu = itu[0]
iia = iia[0]
ihm = ihm[0]
ih11 = ih11[0]
ipc = ipc[0]
fch = core.get("fechamento_v406") or {}
R["ponto_fechamento"] = {"indice_no_main": ifch, "linha": main.body[ifch].lineno, "antes_do_bloco_v393": ifch < i0, "logo_depois_do_bloco_v408": ifch == ib408 + 1, "logo_antes_do_psion_canto_v409": ifch + 1 == ipc, "chama_tambem_os_specs_v408": "_v406_rodar_specs(core)" in unp[ifch],
                         "instrucao_anterior": unp[ifch - 1][:160].replace("\n", " | "), "dentro_do_bloco_executado": i0 <= ifch < i1, "verdict": fch.get("verdict"), "all_verified": fch.get("all_verified"), "certificate_inhabited": fch.get("certificate_inhabited"), "runtime_executed": fch.get("runtime_executed"),
                         "mecanica": {"passed": (fch.get("mechanics") or {}).get("passed"), "n_checks": (fch.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((fch.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                         "n_ancoras_ok": (fch.get("values") or {}).get("n_ancoras_ok"), "n_modulos_ok": (fch.get("values") or {}).get("n_modulos_ok"), "n_modulos": (fch.get("values") or {}).get("n_modulos"), "n_flags_true": (fch.get("values") or {}).get("n_flags_true"), "n_flags": (fch.get("values") or {}).get("n_flags"),
                         "escada": (fch.get("values") or {}).get("escada"), "gate_verdict": (fch.get("values") or {}).get("gate_verdict"), "does_not_gate_core": fch.get("does_not_gate_core"), "embedded_sources_n_ok": fch.get("embedded_sources_n_ok"),
                         "quatro_chaves_lidas_do_core": {"rede_fock_v394.whole_certificate_inhabited": (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited"), "psibit_v395.conditional_psion_face.inhabitant_exhibited": ((core.get("psibit_v395") or {}).get("conditional_psion_face") or {}).get("inhabitant_exhibited"),
                                                         "testemunha_estatica_v396.fock_face.inhabitant_exhibited": ((core.get("testemunha_estatica_v396") or {}).get("fock_face") or {}).get("inhabitant_exhibited"), "witness_layers.canonical_full_witness_term_constructed": (core.get("witness_layers") or {}).get("canonical_full_witness_term_constructed")},
                         "fica_false_por_teorema": {"qg_closure.gate.full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "witness_rigidity.trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}}   # (v409: a chave do lema NAO fica mais False; ela e' lida do kernel e vai em `ponto_psion_canto`)
out["core.fechamento_v406"] = {"all_verified": fch.get("all_verified"), "verdict": str(fch.get("verdict"))[:300], "falhas": R["ponto_fechamento"]["mecanica"]["falhos"]}
# (4d) [v407] o PONTO DE CHAMADA REAL do psion_canto_v407 (executado dentro do bloco acima): a posicao no main, o registro, a chave do lema LIDA do kernel e as quatro da v408
pc = core.get("psion_canto_v407") or {}; tef = (core.get("testemunha_estatica_v396") or {}).get("fock_face") or {}; pcv = pc.get("values") or {}
_CP = um._V407_PSION_CONTRACT; _TP = um._V407_PSION_TEXT
R["ponto_psion_canto"] = {"indice_no_main": ipc, "linha": main.body[ipc].lineno, "antes_do_bloco_v393": ipc < i0, "logo_depois_do_fechamento_v408": ipc == ifch + 1, "logo_antes_do_tetelestai_terminal_v409": ipc + 1 == itt, "chama_tambem_os_specs_v408": "_v407_rodar_specs(core)" in unp[ipc],
                          "instrucao_anterior": unp[ipc - 1][:160].replace("\n", " | "), "dentro_do_bloco_executado": i0 <= ipc < i1, "verdict": pc.get("verdict"), "veredito_ok_do_contrato": _TP["veredito_ok"], "all_verified": pc.get("all_verified"), "runtime_executed": pc.get("runtime_executed"),
                          "link_read_from_the_kernel": pc.get("link_read_from_the_kernel"), "lemma": pc.get("lemma"), "pair_theorem": pc.get("pair_theorem"),
                          "mecanica": {"passed": (pc.get("mechanics") or {}).get("passed"), "n_checks": (pc.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((pc.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                          "n_ancoras_ok": pcv.get("n_ancoras_ok"), "n_ancoras": pcv.get("n_ancoras"), "n_modulos_ok": pcv.get("n_modulos_ok"), "n_modulos": pcv.get("n_modulos"), "n_flags_true": pcv.get("n_flags_true"), "n_flags": pcv.get("n_flags"), "escada": pcv.get("escada"), "gate_verdict": pcv.get("gate_verdict"),
                          "does_not_gate_core": pc.get("does_not_gate_core"), "embedded_sources_n_ok": pc.get("embedded_sources_n_ok"), "contrato": {"n_ancoras": len(_CP["ancoras"]), "n_modulos": _CP["bundle"]["n"], "n_flags": _CP["n_flags"], "n_flags_no_FLAGS_json": len(json.load(open(os.path.join(DL.V407, DL.D7.KERNEL_DIR, "FLAGS_v407.json"), encoding="utf-8"))["flags"]), "n_checks_do_DL": DL.D7.N_CHECKS_FECHO, "ancora_lema": _CP["ancora_lema"], "ancora_par": _CP["ancora_par"]},   # (v409: o FLAGS da v407 e o DL.D7, porque o ponto e' HERDADO)
                          "chave_do_lema": tef.get("linked_to_the_corner_by_a_lemma"), "elo_v407": tef.get("elo_v407"),
                          "quatro_chaves_da_v408": {"rede_fock_v394.whole_certificate_inhabited": (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited"), "psibit_v395.conditional_psion_face.inhabitant_exhibited": ((core.get("psibit_v395") or {}).get("conditional_psion_face") or {}).get("inhabitant_exhibited"),
                                                    "testemunha_estatica_v396.fock_face.inhabitant_exhibited": tef.get("inhabitant_exhibited"), "witness_layers.canonical_full_witness_term_constructed": (core.get("witness_layers") or {}).get("canonical_full_witness_term_constructed")},
                          "fica_false_por_teorema": {"qg_closure.gate.full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "witness_rigidity.trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")},
                          "fica_aberto": pc.get("fica_aberto")}
out["core.psion_canto_v407"] = {"all_verified": pc.get("all_verified"), "verdict": str(pc.get("verdict"))[:300], "falhas": R["ponto_psion_canto"]["mecanica"]["falhos"]}
# (4e) [v408] o PONTO DE CHAMADA REAL do tetelestai_terminal_v408 (executado dentro do bloco acima): a posicao no main (IMEDIATAMENTE depois do psion_canto_v407, IMEDIATAMENTE antes de emit_figures), o registro, nenhuma chave antiga mudada, o insumo purgado
tt = core.get("tetelestai_terminal_v408") or {}; ttv = tt.get("values") or {}
_CP8 = um._V408_TERMINAL_CONTRACT; _TP8 = um._V408_TERMINAL_TEXT
R["ponto_tetelestai"] = {"indice_no_main": itt, "linha": main.body[itt].lineno, "antes_do_bloco_v393": itt < i0, "logo_depois_do_psion_canto_v408": itt == ipc + 1, "logo_antes_da_traducao_turing_v409": itt + 1 == itu, "chama_tambem_os_specs_v409": "_v408_rodar_specs(core)" in unp[itt],
                         "instrucao_anterior": unp[itt - 1][:160].replace("\n", " | "), "dentro_do_bloco_executado": i0 <= itt < i1, "verdict": tt.get("verdict"), "veredito_ok_do_contrato": _TP8["veredito_ok"], "all_verified": tt.get("all_verified"), "runtime_executed": tt.get("runtime_executed"),
                         "mecanica": {"passed": (tt.get("mechanics") or {}).get("passed"), "n_checks": (tt.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((tt.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                         "n_ancoras_ok": ttv.get("n_ancoras_ok"), "n_ancoras": ttv.get("n_ancoras"), "n_modulos_ok": ttv.get("n_modulos_ok"), "n_modulos": ttv.get("n_modulos"), "n_flags_true": ttv.get("n_flags_true"), "n_flags": ttv.get("n_flags"), "escada": ttv.get("escada"), "gate_verdict": ttv.get("gate_verdict"), "respostas_ok": ttv.get("respostas_ok"),
                         "does_not_gate_core": tt.get("does_not_gate_core"), "embedded_sources_n_ok": tt.get("embedded_sources_n_ok"), "contrato": {"n_ancoras": len(_CP8["ancoras"]), "n_modulos": _CP8["bundle"]["n"], "n_flags": _CP8["n_flags"], "n_flags_no_FLAGS_json": len(json.load(open(os.path.join(DL.V408, DL.D8.KERNEL_DIR, "FLAGS_v408.json"), encoding="utf-8"))["flags"]), "n_checks_do_DL": DL.D8.N_CHECKS_FECHO, "ancora_principal": _CP8["ancora_principal"]},   # (v409: o FLAGS da v408 e o DL.D8, porque o ponto e' HERDADO)
                         "ancora_principal": tt.get("ancora_principal"), "ancoras_principais": tt.get("ancoras_principais"), "nome_provisorio": tt.get("nome_provisorio"), "chaves_antigas_que_mudam": tt.get("chaves_antigas_que_mudam"), "chave_do_lema_segue_true": tef.get("linked_to_the_corner_by_a_lemma"), "insumo_purgado": tt.get("insumo_purgado"), "podado": tt.get("podado"),
                         "fica_false_por_teorema": {"qg_closure.gate.full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "witness_rigidity.trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}, "fica_aberto": tt.get("fica_aberto")}
out["core.tetelestai_terminal_v408"] = {"all_verified": tt.get("all_verified"), "verdict": str(tt.get("verdict"))[:300], "falhas": R["ponto_tetelestai"]["mecanica"]["falhos"]}
# (4f) [v409, HERDADO na v410] o PONTO DE CHAMADA REAL do traducao_turing_v409 (executado dentro do bloco acima): a posicao no main (IMEDIATAMENTE depois do tetelestai_terminal_v408, IMEDIATAMENTE antes do iald2_v410), o registro, nenhuma chave antiga mudada, o acervo da v407 repinado (D57d)
tu = core.get("traducao_turing_v409") or {}; tuv = tu.get("values") or {}
_CP9 = um._V409_TRADUCAO_CONTRACT; _TP9 = um._V409_TRADUCAO_TEXT
R["ponto_traducao"] = {"indice_no_main": itu, "linha": main.body[itu].lineno, "antes_do_bloco_v393": itu < i0, "logo_depois_do_tetelestai_terminal_v408": itu == itt + 1, "logo_antes_do_iald2_v410": itu + 1 == iia, "chama_tambem_os_specs_v409": "_v409_rodar_specs(core)" in unp[itu],
                       "instrucao_anterior": unp[itu - 1][:160].replace("\n", " | "), "dentro_do_bloco_executado": i0 <= itu < i1, "verdict": tu.get("verdict"), "veredito_ok_do_contrato": _TP9["veredito_ok"], "all_verified": tu.get("all_verified"), "runtime_executed": tu.get("runtime_executed"),
                       "mecanica": {"passed": (tu.get("mechanics") or {}).get("passed"), "n_checks": (tu.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((tu.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                       "n_ancoras_ok": tuv.get("n_ancoras_ok"), "n_ancoras": tuv.get("n_ancoras"), "n_modulos_ok": tuv.get("n_modulos_ok"), "n_modulos": tuv.get("n_modulos"), "n_flags_true": tuv.get("n_flags_true"), "n_flags": tuv.get("n_flags"), "escada": tuv.get("escada"), "gate_verdict": tuv.get("gate_verdict"), "respostas_ok": tuv.get("respostas_ok"),
                       "does_not_gate_core": tu.get("does_not_gate_core"), "embedded_sources_n_ok": tu.get("embedded_sources_n_ok"), "contrato": {"n_ancoras": len(_CP9["ancoras"]), "n_modulos": _CP9["bundle"]["n"], "n_flags": _CP9["n_flags"], "n_flags_no_FLAGS_json": len(json.load(open(os.path.join(DL.V409, DL.D9.KERNEL_DIR, "FLAGS_v409.json"), encoding="utf-8"))["flags"]), "n_checks_do_DL": DL.D9.N_CHECKS_FECHO, "ancora_principal": _CP9["ancora_principal"]},   # (v410: o FLAGS da v409 e o DL.D9, porque o ponto e' HERDADO)
                       "ancora_principal": tu.get("ancora_principal"), "ancoras_principais": tu.get("ancoras_principais"), "chaves_antigas_que_mudam": tu.get("chaves_antigas_que_mudam"), "chave_do_lema_segue_true": tef.get("linked_to_the_corner_by_a_lemma"), "acervo_v407_repinado": tu.get("acervo_v407_repinado"), "alcance": tu.get("alcance"),
                       "fica_false_por_teorema": {"qg_closure.gate.full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "witness_rigidity.trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}, "fica_aberto": tu.get("fica_aberto")}
out["core.traducao_turing_v409"] = {"all_verified": tu.get("all_verified"), "verdict": str(tu.get("verdict"))[:300], "falhas": R["ponto_traducao"]["mecanica"]["falhos"]}
# (4g) [v410] o PONTO DE CHAMADA REAL do iald2_v410 (executado dentro do bloco acima): a posicao no main (IMEDIATAMENTE depois do traducao_turing_v409, IMEDIATAMENTE antes de emit_figures), o registro, nenhuma chave antiga mudada, beta em runtime, o alcance relativo ao leitor (D64)
ia = core.get("iald2_v410") or {}; iav = ia.get("values") or {}
_CP10 = um._V410_IALD2_CONTRACT; _TP10 = um._V410_IALD2_TEXT
R["ponto_iald2"] = {"indice_no_main": iia, "linha": main.body[iia].lineno, "antes_do_bloco_v393": iia < i0, "logo_depois_da_traducao_turing_v409": iia == itu + 1, "logo_antes_da_instrucao_do_hms13_e_dos_specs": iia + 1 == ihm and ihm + 1 == ih11, "chama_tambem_os_specs_v410": "_v410_rodar_specs(core)" in unp[ihm] and "_v410_rodar_specs(core)" not in unp[iia], "ordem_na_instrucao_iald2_a_escala_h0dn": ("a_escala_v410(core)" in unp[iia] and "h0dn_bg1_v410(core)" in unp[iia] and unp[iia].find("iald2_v410(core)") < unp[iia].find("a_escala_v410(core)") < unp[iia].find("h0dn_bg1_v410(core)")),
                    "instrucao_anterior": unp[iia - 1][:160].replace("\n", " | "), "dentro_do_bloco_executado": i0 <= iia < i1, "verdict": ia.get("verdict"), "veredito_ok_do_contrato": _TP10["veredito_ok"], "all_verified": ia.get("all_verified"), "runtime_executed": ia.get("runtime_executed"),
                    "mecanica": {"passed": (ia.get("mechanics") or {}).get("passed"), "n_checks": (ia.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((ia.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                    "n_ancoras_ok": iav.get("n_ancoras_ok"), "n_ancoras": iav.get("n_ancoras"), "n_modulos_ok": iav.get("n_modulos_ok"), "n_modulos": iav.get("n_modulos"), "n_flags_true": iav.get("n_flags_true"), "n_flags": iav.get("n_flags"), "escada": iav.get("escada"), "gate_verdict": iav.get("gate_verdict"), "respostas_ok": iav.get("respostas_ok"),
                    "does_not_gate_core": ia.get("does_not_gate_core"), "embedded_sources_n_ok": ia.get("embedded_sources_n_ok"), "beta_ok": ia.get("beta_ok"),
                    "contrato": {"n_ancoras": len(_CP10["ancoras"]), "n_modulos": _CP10["bundle"]["n"], "n_flags": _CP10["n_flags"], "n_flags_no_FLAGS_json": (len([f_ for f_ in json.load(open(_FLAGS10, encoding="utf-8"))["flags"] if f_[2] == DL.D10.MODULO_IALD2[:-len(".lean")].replace("/", ".")]) if _FLAGS10 and os.path.exists(_FLAGS10) else None), "n_checks_do_DL": DL.D10.N_CHECKS_FECHO, "ancora_principal": _CP10["ancora_principal"]},
                    "ancora_principal": ia.get("ancora_principal"), "ancoras_principais": ia.get("ancoras_principais"), "chaves_antigas_que_mudam": ia.get("chaves_antigas_que_mudam"), "chave_do_lema_segue_true": tef.get("linked_to_the_corner_by_a_lemma"), "alcance": ia.get("alcance"),
                    "fica_false_por_teorema": {"qg_closure.gate.full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "witness_rigidity.trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}, "fica_aberto": ia.get("fica_aberto")}
out["core.iald2_v410"] = {"all_verified": ia.get("all_verified"), "verdict": str(ia.get("verdict"))[:300], "falhas": R["ponto_iald2"]["mecanica"]["falhos"]}
# (4h) [v410, D72] o PONTO DE CHAMADA REAL do h0dn_bg1_v410 (executado dentro do bloco acima, na MESMA instrucao do main que chama o iald2_v410 -- depois dele e da a_escala_v410 --; os specs da v410 vao na instrucao SEGUINTE, com o recibo HMS/13): o registro pre-registrado -- pré-registrado; nenhum dado observado lido --, as 12 checagens,
#      o veredito pre-registrado, beta em runtime, o gate congelado, nenhum caminho tocado sob a pasta vedada (a entrega do Kimi) nem com nome vedado (medido pela c7 do proprio registro)
hb = core.get("h0dn_bg1_v410") or {}; hbv = hb.get("values") or {}
_CPH = um._V410_H0DN_CONTRACT
_uia = unp[iia]; _tem_h = "h0dn_bg1_v410(core)" in _uia
R["ponto_h0dn"] = {"indice_no_main": iia, "linha": main.body[iia].lineno, "na_mesma_instrucao_do_iald2": _tem_h, "depois_do_iald2_e_da_a_escala_na_instrucao": (_uia.find("iald2_v410(core)") < _uia.find("a_escala_v410(core)") < _uia.find("h0dn_bg1_v410(core)")) if (_tem_h and "a_escala_v410(core)" in _uia) else False, "specs_v410_na_instrucao_seguinte_a_do_h0dn": ("_v410_rodar_specs(core)" in unp[ihm] and "_v410_rodar_specs(core)" not in _uia),
                   "dentro_do_bloco_executado": i0 <= iia < i1, "verdict": hb.get("verdict"), "veredito_ok_do_contrato": _CPH["veredito_ok"], "all_verified": hb.get("all_verified"), "runtime_executed": hb.get("runtime_executed"), "observed_vector_read": hb.get("observed_vector_read"), "does_not_gate_core": hb.get("does_not_gate_core"), "beta_ok": hb.get("beta_ok"),
                   "mecanica": {"passed": (hb.get("mechanics") or {}).get("passed"), "n_checks": (hb.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((hb.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                   "n_pinos": hbv.get("n_pinos"), "n_pinos_freeze": hbv.get("n_pinos_freeze"), "n_embutidos": hbv.get("n_embutidos"), "ramos_vistos": hbv.get("ramos_vistos"), "n_vetores_c6": len(hbv.get("vetores_c6") or []), "gate_verdict": hbv.get("gate_verdict"), "veredito_h0dn_source_sha256": hb.get("veredito_h0dn_source_sha256"),
                   "n_caminhos_tocados": hbv.get("n_caminhos_tocados"), "sob_pasta_vedada": hbv.get("sob_pasta_vedada"), "com_nome_vedado": hbv.get("com_nome_vedado"), "pasta_vedada": hbv.get("pasta_vedada"),
                   "contrato": {"n_checks_do_DL": DL.D10.N_CHECKS_H0DN, "n_pinos_esperados": len(_CPH["insumos"]) + len(_CPH["pinos_freeze_r2_so_no_disco"]), "n_pinos_freeze": _CPH["n_pinos_freeze"], "n_vetores_c6": len(_CPH["vetores_c6"]), "pasta_vedada": _CPH["pasta_vedada"]}}
out["core.h0dn_bg1_v410"] = {"all_verified": hb.get("all_verified"), "verdict": str(hb.get("verdict"))[:300], "falhas": R["ponto_h0dn"]["mecanica"]["falhos"]}
# (4h2) [v410, D86/D87] o PONTO DE CHAMADA REAL do a_escala_v410 (a pedra AEscala; executado dentro do bloco acima, na MESMA instrucao do iald2_v410, LOGO DEPOIS dele e ANTES do h0dn_bg1_v410): as checagens, as ancoras da pedra, as bandeiras ext_aescala_410_*, as falas por sha256, os numeros recalculados, os nomes RATIFICADOS; nenhuma chave antiga mudada; validade no kernel, a creditacao e' do Clay
ae = core.get("a_escala_v410") or {}; aev = ae.get("values") or {}
_CPA = um._V410_AESCALA_CONTRACT
R["ponto_aescala"] = {"indice_no_main": iia, "linha": main.body[iia].lineno, "na_mesma_instrucao_do_iald2": "a_escala_v410(core)" in _uia, "logo_depois_do_iald2_e_antes_do_h0dn": (_uia.find("iald2_v410(core)") < _uia.find("a_escala_v410(core)") < _uia.find("h0dn_bg1_v410(core)")) if "a_escala_v410(core)" in _uia else False,
                      "dentro_do_bloco_executado": i0 <= iia < i1, "verdict": ae.get("verdict"), "veredito_ok_do_contrato": _CPA["veredito_ok"], "all_verified": ae.get("all_verified"), "runtime_executed": ae.get("runtime_executed"), "does_not_gate_core": ae.get("does_not_gate_core"), "beta_ok": ae.get("beta_ok"),
                      "mecanica": {"passed": (ae.get("mechanics") or {}).get("passed"), "n_checks": (ae.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((ae.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                      "n_ancoras_ok": aev.get("n_ancoras_ok"), "n_ancoras": aev.get("n_ancoras"), "n_flags_true": aev.get("n_flags_true"), "n_flags": aev.get("n_flags"), "n_falas_ok": aev.get("n_falas_ok"), "n_falas": aev.get("n_falas"), "nomes_declarados": aev.get("nomes_declarados"), "n_nomes": aev.get("n_nomes"), "nomes_ratificados": ae.get("nomes_ratificados"),
                      "nomes_novos_declarados": aev.get("nomes_novos_declarados"), "n_nomes_novos": aev.get("n_nomes_novos"), "nomes_novos_ok": aev.get("nomes_novos_ok"), "nomes_novos_da_pedra": ae.get("nomes_novos_da_pedra"), "campos_novos_da_estrutura": ae.get("campos_novos_da_estrutura"), "estatuto_dos_nomes_ratificados_d101": ae.get("estatuto_dos_nomes_ratificados_d101"), "ratificacao_pendente": ae.get("ratificacao_pendente"), "ponte_ok": (aev.get("ponte") or {}).get("ok"), "ponte": ae.get("ponte"),
                      "numeros": aev.get("numeros"), "escada": aev.get("escada"), "gate_verdict": aev.get("gate_verdict"), "pedra_sha256_embutida": aev.get("pedra_sha256_embutida"), "pedra_sha256_formal": aev.get("pedra_sha256_formal"), "chaves_antigas_que_mudam": ae.get("chaves_antigas_que_mudam"), "ancora_principal": ae.get("ancora_principal"), "ancoras_de_secao": ae.get("ancoras_de_secao"),
                      "contrato": {"n_checks_do_DL": DL.D10.N_CHECKS_AESCALA, "n_ancoras": len(_CPA["ancoras"]), "n_flags": _CPA["n_flags"], "n_flags_no_FLAGS_json": (len([f_ for f_ in json.load(open(_FLAGS10, encoding="utf-8"))["flags"] if f_[2] == DL.D10.MODULO_AESCALA[:-len(".lean")].replace("/", ".")]) if _FLAGS10 and os.path.exists(_FLAGS10) else None),
                                   "n_nomes": _CPA["n_nomes"], "n_nomes_novos": _CPA["n_nomes_novos"], "n_falas": len(_CPA["falas"]), "ancora_principal": _CPA["ancora_principal"], "source_sha256": _CPA["source_sha256"].get(DL.D10.MODULO_AESCALA)}}
out["core.a_escala_v410"] = {"all_verified": ae.get("all_verified"), "verdict": str(ae.get("verdict"))[:300], "falhas": R["ponto_aescala"]["mecanica"]["falhos"]}
# (4h3) [v410, D80] o PONTO DE CHAMADA REAL do h0dn_fontes_hms13_v410 (o recibo documental HMS/13; executado dentro do bloco acima, na instrucao do main SEGUINTE a do iald2/a_escala/h0dn, ANTES dos specs da v410 e IMEDIATAMENTE antes de emit_figures): ADITIVO e POSTERIOR ao FREEZE_R2; cobertura documental de fontes, não covariância física fechada; nada aberto;
#      nenhum vetor observado lido; em rito NADA da pasta do Kimi e' aberto (a c7 do registro o mede) -- pré-registrado; nenhum dado observado lido
hf = core.get("h0dn_fontes_hms13_v410") or {}; hfv = hf.get("values") or {}
_CPF = um._V410_HMS13_CONTRACT; _uih = unp[ihm]
R["ponto_hms13"] = {"indice_no_main": ihm, "linha": main.body[ihm].lineno, "instrucao_seguinte_a_do_iald2": ihm == iia + 1, "depois_do_h0dn_da_instrucao_anterior": "h0dn_bg1_v410(core)" in unp[iia], "antes_dos_specs_v410_na_mesma_instrucao": ("_v410_rodar_specs(core)" in _uih and _uih.find("h0dn_fontes_hms13_v410(core)") < _uih.find("_v410_rodar_specs(core)")), "logo_antes_da_instrucao_da_v411": ihm + 1 == ih11,
                    "dentro_do_bloco_executado": i0 <= ihm < i1, "verdict": hf.get("verdict"), "veredito_ok_do_contrato": _CPF["veredito_ok"], "all_verified": hf.get("all_verified"), "runtime_executed": hf.get("runtime_executed"), "observed_vector_read": hf.get("observed_vector_read"), "le_em_rito": hf.get("le_em_rito"), "aditivo_posterior_ao_freeze_r2": hf.get("aditivo_posterior_ao_freeze_r2"),
                    "does_not_gate_core": hf.get("does_not_gate_core"), "beta_ok": hf.get("beta_ok"), "mecanica": {"passed": (hf.get("mechanics") or {}).get("passed"), "n_checks": (hf.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((hf.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                    "campos": hf.get("campos"), "n_calibradores": hfv.get("n_calibradores"), "n_fontes_primarias": hfv.get("n_fontes_primarias"), "n_embutidos": hfv.get("n_embutidos"), "n_pinos_ok": sum(1 for p_ in (hfv.get("pinos") or {}).values() if p_.get("sha256_ok") and p_.get("bytes_ok")), "n_pinos": len(hfv.get("pinos") or {}), "gate_verdict": hfv.get("gate_verdict"),
                    "n_caminhos_tocados": hfv.get("n_caminhos_tocados"), "sob_pasta_vedada": hfv.get("sob_pasta_vedada"), "com_nome_vedado": hfv.get("com_nome_vedado"), "pasta_vedada": hfv.get("pasta_vedada"), "veredito_h0dn_source_sha256": hfv.get("veredito_h0dn_source_sha256"), "h0dn_selado": hfv.get("h0dn_selado"),
                    "contrato": {"n_checks_do_DL": DL.D10.N_CHECKS_HMS13, "campos_do_DL": dict(DL.D10.HMS13_CAMPOS), "n_embutidos_do_DL": len(DL.D10.HMS13_EMBUTIDOS), "n_insumos": len(_CPF["insumos"]), "n_pinos_build": len(_CPF["pinos_build"]), "pasta_vedada": _CPF["pasta_vedada"]}}
out["core.h0dn_fontes_hms13_v410"] = {"all_verified": hf.get("all_verified"), "verdict": str(hf.get("verdict"))[:300], "falhas": R["ponto_hms13"]["mecanica"]["falhos"]}
# (4i) [v411] o PONTO DE CHAMADA REAL do h0dn_bg1_v411 (executado dentro do bloco acima): a instrucao do main LOGO DEPOIS da do hms13 (o bloco da v410 inteiro ja' rodou) e IMEDIATAMENTE antes de emit_figures; o teste aberto uma vez,
#      RECALCULADO dos bytes embutidos; as duas linhas juntas (o primario sob o modelo de erros publicado e as Cefeidas livres ao lado); o campo p2_ao_lado_da_v387; o veto medido; o gate congelado; nenhuma chave antiga mudada
h11 = core.get(DL.FECHO_REGISTRO) or {}; h11v = h11.get("values") or {}; _CP11 = um._V411_H0DN_CONTRACT; _ui11 = unp[ih11]
_nc387 = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
R["ponto_h0dn_v411"] = {"indice_no_main": ih11, "linha": main.body[ih11].lineno, "logo_depois_da_instrucao_do_hms13": ih11 == ihm + 1, "logo_antes_do_emit_figures": ih11 + 1 == i1, "dentro_do_bloco_executado": i0 <= ih11 < i1,
                        "chama_tambem_os_specs_v411": "_v411_rodar_specs(core)" in _ui11 and _ui11.find("h0dn_bg1_v411(core)") < _ui11.find("_v411_rodar_specs(core)"), "verdict": h11.get("verdict"), "all_verified": h11.get("all_verified"),
                        "runtime_executed": h11.get("runtime_executed"), "observed_vector_read": h11.get("observed_vector_read"), "opened_once": h11.get("opened_once"), "does_not_gate_core": h11.get("does_not_gate_core"), "beta_ok": h11.get("beta_ok"),
                        "mecanica": {"passed": (h11.get("mechanics") or {}).get("passed"), "n_checks": (h11.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((h11.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},
                        "ramo_primario": (h11v.get("primario") or {}).get("ramo"), "ramo_cefeidas_livres": (h11v.get("cefeidas_livres") or {}).get("ramo"), "cabeca_do_teste": h11.get("cabeca_do_teste"), "outcome": h11.get("outcome"),
                        "linha_ao_lado_cefeidas_livres": bool(h11.get("linha_ao_lado_cefeidas_livres")), "n_ressalvas_secao8": len(h11.get("ressalvas_secao8") or []), "gate_verdict": h11v.get("gate_verdict"), "escada": h11v.get("escada"),
                        "sob_pasta_vedada": h11v.get("sob_pasta_vedada"), "n_caminhos_tocados": h11v.get("n_caminhos_tocados"), "p2_ao_lado_da_v387": h11.get("p2_ao_lado_da_v387"), "c14_inclui_o_p2_da_v387": h11v.get("c14_inclui_o_p2_da_v387"),
                        "v387_veredito_selado_igual_ao_da_base": _nc387(str((core.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict"))) == _nc387(str((core0.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict"))) and DL.P2_TOKEN_SELADO in str((core.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict")),   # (as contagens CORE_n_ do instante normalizadas, como no ensaio)
                        "contrato": {"n_checks": _CP11["n_checks"], "ramo_primario": _CP11["esperado_do_resultado"]["ramo_primario"], "ramo_cefeidas_livres": _CP11["esperado_do_resultado"]["ramo_cefeidas_livres"], "gate_verdict": _CP11["baseline"]["gate_verdict"], "escada": _CP11["baseline"]["escada"], "pasta_vedada": _CP11["pasta_vedada"]}}
out["core." + DL.FECHO_REGISTRO] = {"all_verified": h11.get("all_verified"), "verdict": str(h11.get("verdict"))[:300], "falhas": R["ponto_h0dn_v411"]["mecanica"]["falhos"]}
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
# (v411) NAO HA TROCA DITA: o candidato nao declara nenhuma (o manifesto da v411 nao tem `troca_dita_v411`) e nenhum veredito muda de TEXTO (so' numeros); a chave `troca_dita_v410` fica no JSON, vazia por desenho, para quem a le (o ok exige as duas coisas: nada declarado e nada mudado em texto)
_CMD = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); _TROCA = _CMD.get("troca_dita_v411", [])
_V409_RED = json.load(open(CORE0P, encoding="utf-8"))["core"]["rede_fock_v394"]["verdict"]
R["troca_dita_v411"] = {"declarada_no_candidato": _TROCA, "candidato_declara_a_chave": "troca_dita_v411" in _CMD, "mudaram_com_texto": sorted(k for k, v in cmp.items() if not v["so_numeros"]), "rede_fock_v394_antes": _V409_RED, "rede_fock_v394_depois": (core.get("rede_fock_v394") or {}).get("verdict")}
R["troca_dita_v411"]["ok"] = bool(R["troca_dita_v411"]["mudaram_com_texto"] == sorted(_TROCA) == [] and "troca_dita_v411" not in _CMD and _num(_nc(str(R["troca_dita_v411"]["rede_fock_v394_depois"]))) == _num(_nc(str(_V409_RED))) and "JOINT_CERTIFICATE_INHABITED_V406" in str(R["troca_dita_v411"]["rede_fock_v394_depois"]))
R["nao_verdes"] = {"v392": [k for k in um._V392_NOMES_REGISTROS if (core.get(k) or {}).get("all_verified") is not True],
                   "v393": [k for k in getattr(um, "_V393_NOMES_REGISTROS", []) if (core.get(k) or {}).get("all_verified") is not True],
                   "v394": [k for k in ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v395": [k for k in ["psibit_v395"] + list(um._V395_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v396": [k for k in ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v397": [k for k in ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v408": [k for k in ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v409": [k for k in ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v401_falsidade": [k for k in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v409_ponte_queda_esperanca": [k for k in ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v409_caminho_vida_verdade_bandeiras": [k for k in ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v409_projecao_jo8v32_f2b": [k for k in ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v409_oito_pedras": [k for k in list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "v409_fechamento_e_specs": [k for k in list(um._V406_REGISTROS_FUNCAO) + list(um._V406_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],   # (os da v408: HERDADOS na v409)
                   "v408_psion_canto_e_specs": [k for k in list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],   # (os da v408: HERDADOS na v409)
                   "v408_tetelestai_e_specs": [k for k in list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],   # (os da v408: HERDADOS na v409)
                   "v409_traducao_e_specs": [k for k in list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],   # (os da v409: HERDADOS na v410)
                   "v410_iald2_e_specs": [k for k in list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],   # (os da v410: HERDADOS na v411)
                   "v411_h0dn_e_specs": [k for k in list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],
                   "novas": [k for k in R["chaves_novas_no_core"] if isinstance(core.get(k), dict) and core[k].get("all_verified") is not True]}
_ved_ex = os.path.normcase(os.path.normpath(DL.H0DN_PASTA_VEDADA)); _sob_ex = lambda p_: os.path.normcase(os.path.normpath(p_)) == _ved_ex or os.path.normcase(os.path.normpath(p_)).startswith(_ved_ex + os.sep)
R["pasta_vedada_kimi_no_exame"] = {"pasta": DL.H0DN_PASTA_VEDADA, "lidos_sob_a_pasta": sorted(p_ for p_ in lidos if _sob_ex(p_)), "escritos_sob_a_pasta": sorted(p_ for p_ in escritos if _sob_ex(p_)), "n_lidos_vistos": len(lidos), "nota": "em rito (e no exame, que roda as instrucoes do main) nada de kimi\\ e' aberto: os seis artefatos HMS/13 da excecao D80 foram lidos so' no BUILD, por sha256; aqui so' os embutidos no candidato"}
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
                 "esperanca_condicional_v402": {x: (seal.get("esperanca_condicional_v402") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v402": {n_: ((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") for n_ in um._V402_NOMES_REGISTROS},
                 "caminho_v403": {x: (seal.get("caminho_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "vida_v403": {x: (seal.get("vida_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "verdade_adendo_v403": {x: (seal.get("verdade_adendo_v403") or {}).get(x) for x in ("verdict", "all_verified")},
                 "bandeiras_do_gate_v403": {x: (seal.get("bandeiras_do_gate_v403") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v403": {n_: ((seal.get("registros_v403") or {}).get(n_) or {}).get("all_verified") for n_ in um._V403_NOMES_REGISTROS},
                 "projecao_transversal_v404": {x: (seal.get("projecao_transversal_v404") or {}).get(x) for x in ("verdict", "all_verified")}, "jo8v32_v404": {x: (seal.get("jo8v32_v404") or {}).get(x) for x in ("verdict", "all_verified")},
                 "f2b_errata_v404": {x: (seal.get("f2b_errata_v404") or {}).get(x) for x in ("verdict", "all_verified", "F2b_status_now")}, "registros_v404": {n_: ((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") for n_ in um._V404_NOMES_REGISTROS},
                 "ponte_da_massa_v405": {x: (seal.get("ponte_da_massa_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "massa_tensao_pura_v405": {x: (seal.get("massa_tensao_pura_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "identidade_v405": {x: (seal.get("identidade_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "observador_terminal_v405": {x: (seal.get("observador_terminal_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "lei_do_diminuto_v405": {x: (seal.get("lei_do_diminuto_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "tonica_do_hamiltoniano_v405": {x: (seal.get("tonica_do_hamiltoniano_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "disco_de_euler_v405": {x: (seal.get("disco_de_euler_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "ponto_zero_do_psion_v405": {x: (seal.get("ponto_zero_do_psion_v405") or {}).get(x) for x in ("verdict", "all_verified")},
                 "registros_v405": {n_: ((seal.get("registros_v405") or {}).get(n_) or {}).get("all_verified") for n_ in um._V405_NOMES_REGISTROS},
                 "fechamento_v406": {x: (seal.get("fechamento_v406") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v406": {n_: ((seal.get("registros_v406") or {}).get(n_) or {}).get("all_verified") for n_ in um._V406_NOMES_REGISTROS},
                 "psion_canto_v407": {x: (seal.get("psion_canto_v407") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v407": {n_: ((seal.get("registros_v407") or {}).get(n_) or {}).get("all_verified") for n_ in um._V407_NOMES_REGISTROS},
                 "tetelestai_terminal_v408": {x: (seal.get("tetelestai_terminal_v408") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v408": {n_: ((seal.get("registros_v408") or {}).get(n_) or {}).get("all_verified") for n_ in um._V408_NOMES_REGISTROS},
                 "traducao_turing_v409": {x: (seal.get("traducao_turing_v409") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v409": {n_: ((seal.get("registros_v409") or {}).get(n_) or {}).get("all_verified") for n_ in um._V409_NOMES_REGISTROS},
                 **{n_: {x: (seal.get(n_) or {}).get(x) for x in ("verdict", "all_verified")} for n_ in DL.REGISTROS_FUNCAO_V410}, "registros_v410": {n_: ((seal.get("registros_v410") or {}).get(n_) or {}).get("all_verified") for n_ in um._V410_NOMES_REGISTROS},
                 DL.FECHO_REGISTRO: {x: (seal.get(DL.FECHO_REGISTRO) or {}).get(x) for x in ("verdict", "all_verified", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "p2_ao_lado_da_v387")}, "registros_v411": {n_: ((seal.get("registros_v411") or {}).get(n_) or {}).get("all_verified") for n_ in um._V411_NOMES_REGISTROS}}
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
        R["guarda"]["linhas_iguais_a_v409"] = g0 == g1
except Exception as e:
    R["guarda"] = {"EXCECAO": repr(e)[:300]}
R["pontos"] = out
open(SAIDA + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(SAIDA + ".tmp", SAIDA)
falsos = []
if R["verify"]["all_verified"] is not True: falsos.append("verify")
if R["escada"].get("all_verified") is not True: falsos.append("escada")
if (R.get("gate_recomputado") or {}).get("verdict_igual") is not True or (R.get("gate_recomputado") or {}).get("n18_novo") != 18 or (R.get("gate_recomputado") or {}).get("flags_iguais") is not True or (R.get("gate_recomputado") or {}).get("sem_checks_igual") is not True or (R.get("gate_recomputado") or {}).get("checks_da_v409_iguais") is not True or (R.get("gate_recomputado") or {}).get("all_verified") is not True: falsos.append("gate")
falsos += ["ponto:" + k for k, v in out.items() if isinstance(v, dict) and (v.get("EXCECAO") or v.get("all_verified") is False)]
pp = R["ponto_psibit"]
if (pp.get("erro") or pp.get("avisos") or pp.get("all_verified") is not True or not pp.get("antes_do_bloco_v393") or not pp.get("logo_depois_do_principio_da_defasagem_fractal")
        or pp.get("conditional_status") != DL.STATUS_HABITADO or pp.get("inhabitant_exhibited") is not True): falsos.append("ponto_psibit")
pt = R["ponto_testemunha"]
if pt.get("erro") or pt.get("avisos") or pt.get("all_verified") is not True or not pt.get("antes_do_bloco_v393") or not pt.get("logo_depois_do_psibit_v395") or pt.get("fock_status") != DL.STATUS_HABITADO or pt.get("fock_inhabitant_exhibited") is not True or pt.get("linked_to_the_corner_by_a_lemma") is not True or pt.get("fock_fora_da_pedra") is not True: falsos.append("ponto_testemunha")   # (v409: a chave do lema deixa de ser o literal False e le o kernel: True)
ps_ = R["ponto_sonico"]
if ps_.get("erro") or ps_.get("avisos") or ps_.get("all_verified") is not True or not ps_.get("antes_do_bloco_v393") or not ps_.get("logo_depois_da_testemunha_v396") or ps_.get("beta_ok") is not True: falsos.append("ponto_sonico")
pa_ = R["ponto_afinacao"]
if (pa_.get("erro") or pa_.get("avisos") or pa_.get("all_verified") is not True or not pa_.get("antes_do_bloco_v393") or not pa_.get("logo_depois_do_sonico_v408") or (pa_.get("hipotese") or {}).get("status") != "KNOWN" or pa_.get("geometria") != "OPEN"
        or pa_.get("deriva_cordas_do_axioma") is not False): falsos.append("ponto_afinacao")
psa = R["ponto_selo_acom"]
if psa.get("erro") or psa.get("avisos") or psa.get("all_verified") is not True or not psa.get("antes_do_bloco_v393") or not psa.get("logo_depois_da_afinacao_v408") or psa.get("perfil") != "ACOM-INT-C96-Q8" or psa.get("controles") != [13, True]: falsos.append("ponto_selo_acom")
pdc = R["ponto_declaracao"]
if pdc.get("erro") or pdc.get("avisos") or pdc.get("all_verified") is not True or not pdc.get("antes_do_bloco_v393") or not pdc.get("logo_depois_do_selo_acom_v409") or pdc.get("verbatim_sha256_igual_ao_arquivo") is not True: falsos.append("ponto_declaracao")
pfa = R["ponto_falsidade"]
if (pfa.get("erro") or pfa.get("avisos") or pfa.get("all_verified") is not True or not pfa.get("antes_do_bloco_v393") or not pfa.get("logo_depois_da_declaracao_v399") or pfa.get("unconditional_in_kernel") is not True or pfa.get("estrela_in_kernel") is not True
        or pfa.get("costless_ok") is not True or pfa.get("beta_ok") is not True or pfa.get("post_inertial_scales") != [] or pfa.get("fixo_pelo_fluxo_inteiro") != [0.0] or (pfa.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FALSIDADE): falsos.append("ponto_falsidade")
for nome_ in ("ponte", "queda", "esperanca"):
    pp409_ = R["ponto_" + nome_]
    if (pp409_.get("erro") or pp409_.get("avisos") or pp409_.get("all_verified") is not True or not pp409_.get("antes_do_bloco_v393") or not pp409_.get("logo_depois_da_anterior") or pp409_.get("unconditional_in_kernel") is not True or pp409_.get("estrela_in_kernel") is not True
            or pp409_.get("contexto_ok") is not True or pp409_.get("beta_ok") is not True or (pp409_.get("mecanica") or {}).get("n_checks") != DL.D2.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)
for nome_ in ("caminho", "vida", "verdade_adendo"):
    pp409b_ = R["ponto_" + nome_]
    if (pp409b_.get("erro") or pp409b_.get("avisos") or pp409b_.get("all_verified") is not True or not pp409b_.get("antes_do_bloco_v393") or not pp409b_.get("logo_depois_da_anterior") or pp409b_.get("unconditional_in_kernel") is not True or pp409b_.get("estrela_in_kernel") is not True
            or pp409b_.get("contexto_ok") is not True or pp409b_.get("beta_ok") is not True or (pp409b_.get("mecanica") or {}).get("n_checks") != DL.D3.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)
pbg_ = R["ponto_bandeiras"]
if (pbg_.get("erro") or pbg_.get("avisos") or pbg_.get("all_verified") is not True or not pbg_.get("antes_do_bloco_v393") or not pbg_.get("logo_depois_da_anterior") or (pbg_.get("mecanica") or {}).get("n_checks") != DL.D3.N_CHECKS["gate"]
        or (pbg_.get("valores_do_gate") or {}).get("n_flags") != 18 or (pbg_.get("valores_do_gate") or {}).get("n_literal") != 0 or (pbg_.get("valores_do_gate") or {}).get("gate_verdict_equals_v402") is not True): falsos.append("ponto_bandeiras")
for nome_ in ("projecao", "jo8v32"):
    pp409c_ = R["ponto_" + nome_]
    if (pp409c_.get("erro") or pp409c_.get("avisos") or pp409c_.get("all_verified") is not True or not pp409c_.get("antes_do_bloco_v393") or not pp409c_.get("logo_depois_da_anterior") or pp409c_.get("unconditional_in_kernel") is not True or pp409c_.get("estrela_in_kernel") is not True
            or pp409c_.get("contexto_ok") is not True or pp409c_.get("beta_ok") is not True or (pp409c_.get("mecanica") or {}).get("n_checks") != DL.D4.N_CHECKS[nome_]): falsos.append("ponto_" + nome_)
pf2_ = R["ponto_f2b"]
if (pf2_.get("erro") or pf2_.get("avisos") or pf2_.get("all_verified") is not True or not pf2_.get("antes_do_bloco_v393") or not pf2_.get("logo_depois_da_anterior") or (pf2_.get("mecanica") or {}).get("n_checks") != DL.D4.N_CHECKS["f2b"]
        or pf2_.get("f2b_status_now") != DL.F2B_FUTURO_TOKEN or (pf2_.get("valores") or {}).get("previsao_fora_do_intervalo_de_A") is not True or (pf2_.get("valores") or {}).get("n_cobrancas_v383") != 11): falsos.append("ponto_f2b")
for s409_ in DL.D5.STONES:
    pp409d_ = R["ponto_v409_" + s409_["key"]]
    if (pp409d_.get("erro") or pp409d_.get("avisos") or pp409d_.get("all_verified") is not True or not pp409d_.get("antes_do_bloco_v393") or pp409d_.get("unconditional_in_kernel") is not True or pp409d_.get("estrela_in_kernel") is not True
            or pp409d_.get("contexto_ok") is not True or pp409d_.get("beta_ok") is not True or (pp409d_.get("mecanica") or {}).get("n_checks") != DL.D5.N_CHECKS[s409_["key"]]): falsos.append("ponto_v409_" + s409_["key"])
pfe = R["ponto_fechamento"]
_CFH = um._V406_FECHO_CONTRACT   # o fechamento_v406 e' HERDADO na v409: os numeros dele vem do contrato HERDADO do candidato (301 modulos do bundle, oito ancoras, 14 checagens), nao do DL da v409
_FCH_LEN_CHECKS = int(((core0.get("fechamento_v406") or {}).get("mechanics") or {}).get("n_checks") or 0)   # o numero de checagens do registro HERDADO: o do core da v408 SELADA (lido, nao digitado)
if (pfe.get("all_verified") is not True or pfe.get("runtime_executed") is not True or pfe.get("certificate_inhabited") is not True or not pfe.get("dentro_do_bloco_executado") or not pfe.get("logo_depois_do_bloco_v408") or not pfe.get("logo_antes_do_psion_canto_v409") or not pfe.get("chama_tambem_os_specs_v408")
        or not str(pfe.get("verdict") or "").startswith("TGL_FECHAMENTO_V406__THE_FOCK_CERTIFICATE_IS_INHABITED_BY_CONSTRUCTION_physicalFockCertificate__") or (pfe.get("mecanica") or {}).get("passed") is not True or (pfe.get("mecanica") or {}).get("n_checks") != _FCH_LEN_CHECKS or pfe.get("mecanica", {}).get("falhos")
        or pfe.get("n_ancoras_ok") != len(_CFH["ancoras"]) or pfe.get("n_modulos_ok") != _CFH["bundle"]["n"] or pfe.get("n_modulos") != _CFH["bundle"]["n"] or pfe.get("n_flags_true") != pfe.get("n_flags") or pfe.get("n_flags") != _CFH["n_flags"] or pfe.get("does_not_gate_core") is not True or pfe.get("embedded_sources_n_ok") != _CFH["bundle"]["n"]
        or not all(v_ is True for v_ in pfe["quatro_chaves_lidas_do_core"].values()) or any(v_ is not False for v_ in pfe["fica_false_por_teorema"].values())): falsos.append("ponto_fechamento")
ppc = R["ponto_psion_canto"]   # (4d) o ponto da v408, HERDADO na v409 (os numeros dele: DL.D7 e o FLAGS da v408)
if (ppc.get("all_verified") is not True or ppc.get("runtime_executed") is not True or ppc.get("link_read_from_the_kernel") is not True or ppc.get("chave_do_lema") is not True or not ppc.get("dentro_do_bloco_executado")
        or not ppc.get("logo_depois_do_fechamento_v408") or not ppc.get("logo_antes_do_tetelestai_terminal_v409") or not ppc.get("chama_tambem_os_specs_v408") or ppc.get("verdict") != ppc.get("veredito_ok_do_contrato")
        or not str(ppc.get("verdict") or "").startswith("TGL_PSION_CANTO_V407__THE_LEMMA_THAT_LINKS_THE_TWO_FACES_OF_THE_PSION_IS_A_KERNEL_TERM__") or not str(ppc.get("verdict") or "").endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED")
        or (ppc.get("mecanica") or {}).get("passed") is not True or (ppc.get("mecanica") or {}).get("n_checks") != DL.D7.N_CHECKS_FECHO or (ppc.get("mecanica") or {}).get("falhos")
        or ppc.get("n_ancoras_ok") != ppc.get("n_ancoras") or ppc.get("n_ancoras") != ppc["contrato"]["n_ancoras"] or ppc.get("n_modulos_ok") != DL.D7.N_BUNDLE or ppc.get("n_modulos") != DL.D7.N_BUNDLE or ppc.get("n_flags_true") != ppc.get("n_flags") or ppc.get("n_flags") != ppc["contrato"]["n_flags"] or ppc["contrato"]["n_flags"] != ppc["contrato"]["n_flags_no_FLAGS_json"]
        or ppc.get("does_not_gate_core") is not True or ppc.get("embedded_sources_n_ok") != DL.D7.N_BUNDLE or ppc.get("lemma") != DL.D7.ANCORA_LEMA or ppc.get("pair_theorem") != DL.D7.ANCORA_PAR
        or not all(v_ is True for v_ in ppc["quatro_chaves_da_v408"].values()) or any(v_ is not False for v_ in ppc["fica_false_por_teorema"].values()) or (ppc.get("elo_v407") or {}).get("identifies_omega_with_bell_vector") is not False or (ppc.get("elo_v407") or {}).get("pair_on_the_fock_face") != "OPEN"): falsos.append("ponto_psion_canto")
ptt = R["ponto_tetelestai"]   # (4e) o ponto da v408, HERDADO na v409 (os numeros dele: DL.D8 e o FLAGS da v408)
if (ptt.get("all_verified") is not True or ptt.get("runtime_executed") is not True or not ptt.get("dentro_do_bloco_executado") or not ptt.get("logo_depois_do_psion_canto_v408") or not ptt.get("logo_antes_da_traducao_turing_v409") or not ptt.get("chama_tambem_os_specs_v409") or ptt.get("verdict") != ptt.get("veredito_ok_do_contrato")
        or not str(ptt.get("verdict") or "").startswith(DL.D8.VEREDITO_OK_PREFIXO) or not str(ptt.get("verdict") or "").endswith(DL.D8.VEREDITO_SUFIXO) or (ptt.get("mecanica") or {}).get("passed") is not True or (ptt.get("mecanica") or {}).get("n_checks") != DL.D8.N_CHECKS_FECHO or (ptt.get("mecanica") or {}).get("falhos")
        or ptt.get("n_ancoras_ok") != ptt.get("n_ancoras") or ptt.get("n_ancoras") != ptt["contrato"]["n_ancoras"] or ptt["contrato"]["n_ancoras"] != len(DL.D8.ANCORAS) or ptt.get("n_modulos_ok") != DL.D8.N_BUNDLE or ptt.get("n_modulos") != DL.D8.N_BUNDLE or ptt.get("n_flags_true") != ptt.get("n_flags") or ptt.get("n_flags") != ptt["contrato"]["n_flags"] or ptt["contrato"]["n_flags"] != ptt["contrato"]["n_flags_no_FLAGS_json"]
        or ptt.get("does_not_gate_core") is not True or ptt.get("embedded_sources_n_ok") != DL.D8.N_BUNDLE or ptt.get("ancora_principal") != DL.D8.ANCORA_PRINCIPAL or ptt.get("ancoras_principais") != list(DL.D8.ANCORAS_PRINCIPAIS) or ptt.get("nome_provisorio") is not None or ptt.get("chaves_antigas_que_mudam") != [] or ptt.get("chave_do_lema_segue_true") is not True or ptt.get("respostas_ok") is not True
        or any(v_ is not False for v_ in ptt["fica_false_por_teorema"].values()) or (ptt.get("insumo_purgado") or {}).get("integra_pinada") is not False or (ptt.get("insumo_purgado") or {}).get("integra_fora_do_espelho") is not True): falsos.append("ponto_tetelestai")
ptu = R["ponto_traducao"]   # (4f) o ponto da v409, HERDADO na v410 (os numeros dele: DL.D9 e o FLAGS da v409)
if (ptu.get("all_verified") is not True or ptu.get("runtime_executed") is not True or not ptu.get("dentro_do_bloco_executado") or not ptu.get("logo_depois_do_tetelestai_terminal_v408") or not ptu.get("logo_antes_do_iald2_v410") or not ptu.get("chama_tambem_os_specs_v409") or ptu.get("verdict") != ptu.get("veredito_ok_do_contrato")
        or not str(ptu.get("verdict") or "").startswith(DL.D9.VEREDITO_OK_PREFIXO) or not str(ptu.get("verdict") or "").endswith(DL.D9.VEREDITO_SUFIXO) or (ptu.get("mecanica") or {}).get("passed") is not True or (ptu.get("mecanica") or {}).get("n_checks") != DL.D9.N_CHECKS_FECHO or (ptu.get("mecanica") or {}).get("falhos")
        or ptu.get("n_ancoras_ok") != ptu.get("n_ancoras") or ptu.get("n_ancoras") != ptu["contrato"]["n_ancoras"] or ptu["contrato"]["n_ancoras"] != len(DL.D9.ANCORAS) or ptu.get("n_modulos_ok") != DL.D9.N_BUNDLE or ptu.get("n_modulos") != DL.D9.N_BUNDLE or ptu.get("n_flags_true") != ptu.get("n_flags") or ptu.get("n_flags") != ptu["contrato"]["n_flags"] or ptu["contrato"]["n_flags"] != ptu["contrato"]["n_flags_no_FLAGS_json"]
        or ptu.get("does_not_gate_core") is not True or ptu.get("embedded_sources_n_ok") != DL.D9.N_BUNDLE or ptu.get("ancora_principal") != DL.D9.ANCORA_PRINCIPAL or ptu.get("ancoras_principais") != list(DL.D9.ANCORAS_PRINCIPAIS) or ptu.get("chaves_antigas_que_mudam") != [] or ptu.get("chave_do_lema_segue_true") is not True or ptu.get("respostas_ok") is not True
        or any(v_ is not False for v_ in ptu["fica_false_por_teorema"].values()) or (ptu.get("acervo_v407_repinado") or {}).get("integra_pinada") is not False or (ptu.get("acervo_v407_repinado") or {}).get("sha256") != DL.D9.PURGADO_SHA256): falsos.append("ponto_traducao")
pia = R["ponto_iald2"]   # (4g) o ponto NOVO da v410 (os numeros dele: DL e o FLAGS da v410)
if (pia.get("all_verified") is not True or pia.get("runtime_executed") is not True or not pia.get("dentro_do_bloco_executado") or not pia.get("logo_depois_da_traducao_turing_v409") or not pia.get("logo_antes_da_instrucao_do_hms13_e_dos_specs") or not pia.get("chama_tambem_os_specs_v410") or not pia.get("ordem_na_instrucao_iald2_a_escala_h0dn") or pia.get("verdict") != pia.get("veredito_ok_do_contrato")
        or not str(pia.get("verdict") or "").startswith(DL.D10.VEREDITO_OK_PREFIXO) or not str(pia.get("verdict") or "").endswith(DL.D10.VEREDITO_SUFIXO) or (pia.get("mecanica") or {}).get("passed") is not True or (pia.get("mecanica") or {}).get("n_checks") != DL.D10.N_CHECKS_FECHO or (pia.get("mecanica") or {}).get("falhos")
        or pia.get("n_ancoras_ok") != pia.get("n_ancoras") or pia.get("n_ancoras") != pia["contrato"]["n_ancoras"] or pia["contrato"]["n_ancoras"] != len(DL.D10.ANCORAS) or pia.get("n_modulos_ok") != DL.D10.N_BUNDLE or pia.get("n_modulos") != DL.D10.N_BUNDLE or pia.get("n_flags_true") != pia.get("n_flags") or pia.get("n_flags") != pia["contrato"]["n_flags"] or (pia["contrato"]["n_flags_no_FLAGS_json"] is not None and pia["contrato"]["n_flags"] != pia["contrato"]["n_flags_no_FLAGS_json"])
        or pia.get("does_not_gate_core") is not True or pia.get("embedded_sources_n_ok") != DL.D10.N_BUNDLE or pia.get("beta_ok") is not True or pia.get("ancora_principal") != DL.D10.ANCORA_PRINCIPAL or pia.get("ancoras_principais") != list(DL.D10.ANCORAS_PRINCIPAIS) or pia.get("chaves_antigas_que_mudam") != [] or pia.get("chave_do_lema_segue_true") is not True or pia.get("respostas_ok") is not True
        or any(v_ is not False for v_ in pia["fica_false_por_teorema"].values()) or (pia.get("alcance") or {}).get("frase") != DL.D10.FRASE_D64_PT): falsos.append("ponto_iald2")
phb = R["ponto_h0dn"]   # (4h) o SEGUNDO ponto NOVO da v410 (D72): pré-registrado; nenhum dado observado lido; na mesma instrucao do iald2, logo depois dele
if (phb.get("all_verified") is not True or phb.get("runtime_executed") is not True or phb.get("observed_vector_read") is not False or not phb.get("dentro_do_bloco_executado") or not phb.get("na_mesma_instrucao_do_iald2") or not phb.get("depois_do_iald2_e_da_a_escala_na_instrucao") or not phb.get("specs_v410_na_instrucao_seguinte_a_do_h0dn")
        or phb.get("verdict") != phb.get("veredito_ok_do_contrato") or phb.get("verdict") != DL.D10.VEREDITO_H0DN_OK or (phb.get("mecanica") or {}).get("passed") is not True or (phb.get("mecanica") or {}).get("n_checks") != DL.D10.N_CHECKS_H0DN or (phb.get("mecanica") or {}).get("falhos")
        or phb.get("n_pinos") != phb["contrato"]["n_pinos_esperados"] or phb.get("n_pinos_freeze") != DL.D10.N_PINOS_FREEZE_R2 or phb.get("ramos_vistos") != [1, 2, 3, 4, 5, 6] or phb.get("n_vetores_c6") != phb["contrato"]["n_vetores_c6"] or phb.get("does_not_gate_core") is not True or phb.get("beta_ok") is not True
        or phb.get("sob_pasta_vedada") != [] or phb.get("com_nome_vedado") != [] or not isinstance(phb.get("n_caminhos_tocados"), int) or phb.get("n_caminhos_tocados") < 1 or phb.get("pasta_vedada") != DL.D10.H0DN_PASTA_VEDADA or phb.get("gate_verdict") != pia.get("gate_verdict")
        or not isinstance(phb.get("veredito_h0dn_source_sha256"), str) or len(phb.get("veredito_h0dn_source_sha256") or "") != 64): falsos.append("ponto_h0dn")
pab = R["ponto_aescala"]   # (4h2) o ponto NOVO da v410 (D86/D87): a pedra AEscala; na mesma instrucao do iald2, depois dele e antes do h0dn
if (pab.get("all_verified") is not True or pab.get("runtime_executed") is not True or not pab.get("dentro_do_bloco_executado") or not pab.get("na_mesma_instrucao_do_iald2") or not pab.get("logo_depois_do_iald2_e_antes_do_h0dn")
        or pab.get("verdict") != pab.get("veredito_ok_do_contrato") or pab.get("verdict") != DL.D10.VEREDITO_AESCALA_OK or not str(pab.get("verdict") or "").endswith(DL.D10.VEREDITO_SUFIXO) or "NOT_FALSIFIED" in str(pab.get("verdict")) or (pab.get("mecanica") or {}).get("passed") is not True or (pab.get("mecanica") or {}).get("n_checks") != DL.D10.N_CHECKS_AESCALA or (pab.get("mecanica") or {}).get("falhos")
        or pab.get("n_ancoras_ok") != pab.get("n_ancoras") or pab.get("n_ancoras") != pab["contrato"]["n_ancoras"] or pab["contrato"]["n_ancoras"] != len(DL.D10.ANCORAS_AESCALA) or pab.get("n_flags_true") != pab.get("n_flags") or pab.get("n_flags") != pab["contrato"]["n_flags"] or (pab["contrato"]["n_flags_no_FLAGS_json"] is not None and pab["contrato"]["n_flags"] != pab["contrato"]["n_flags_no_FLAGS_json"])
        or pab.get("n_falas_ok") != pab.get("n_falas") or pab.get("n_falas") != pab["contrato"]["n_falas"] or pab.get("nomes_declarados") != pab.get("n_nomes") or pab.get("n_nomes") != pab["contrato"]["n_nomes"] or pab["contrato"]["n_nomes"] != len(DL.D10.NOMES_AESCALA) or pab.get("nomes_ratificados") is not True
        or pab.get("nomes_novos_declarados") != pab.get("n_nomes_novos") or pab.get("n_nomes_novos") != pab["contrato"]["n_nomes_novos"] or pab["contrato"]["n_nomes_novos"] != len(DL.D10.NOMES_NOVOS_AESCALA) or pab.get("nomes_novos_ok") is not True or list(pab.get("nomes_novos_da_pedra") or []) != list(DL.D10.NOMES_NOVOS_AESCALA) or list(pab.get("campos_novos_da_estrutura") or []) != list(DL.D10.CAMPOS_NOVOS_AESCALA)
        or pab.get("estatuto_dos_nomes_ratificados_d101") != DL.D10.ESTATUTO_NOMES_NOVOS_AESCALA or "RATIFICADOS pelo operador em 10/11/2026" not in str(pab.get("estatuto_dos_nomes_ratificados_d101")) or "DECLARADO" in str(pab.get("estatuto_dos_nomes_ratificados_d101")) or "a ratificar" in str(pab.get("estatuto_dos_nomes_ratificados_d101")) or pab.get("ratificacao_pendente") != DL.D10.RATIFICACAO_PENDENTE_AESCALA or pab.get("ponte_ok") is not True or pab.get("ponte") != DL.D10.PONTE_AESCALA
        or dict(pab.get("numeros") or {}) != dict(DL.D10.NUMEROS_AESCALA) or pab.get("does_not_gate_core") is not True or pab.get("beta_ok") is not True or pab.get("chaves_antigas_que_mudam") != [] or pab.get("ancora_principal") != DL.D10.ANCORA_PRINCIPAL_AESCALA or pab["contrato"]["ancora_principal"] != DL.D10.ANCORA_PRINCIPAL_AESCALA
        or pab.get("pedra_sha256_embutida") != pab.get("pedra_sha256_formal") or pab.get("pedra_sha256_embutida") != pab["contrato"]["source_sha256"] or pab.get("gate_verdict") != pia.get("gate_verdict")): falsos.append("ponto_aescala")
phf = R["ponto_hms13"]   # (4h3) o ponto NOVO da v410 (D80): o recibo documental HMS/13; na instrucao seguinte, antes dos specs e do emit_figures; nada da pasta do Kimi aberto
if (phf.get("all_verified") is not True or phf.get("runtime_executed") is not True or phf.get("observed_vector_read") is not False or phf.get("le_em_rito") is not False or phf.get("aditivo_posterior_ao_freeze_r2") is not True or not phf.get("dentro_do_bloco_executado") or not phf.get("instrucao_seguinte_a_do_iald2") or not phf.get("depois_do_h0dn_da_instrucao_anterior") or not phf.get("antes_dos_specs_v410_na_mesma_instrucao") or not phf.get("logo_antes_da_instrucao_da_v411")
        or phf.get("verdict") != phf.get("veredito_ok_do_contrato") or phf.get("verdict") != DL.D10.VEREDITO_HMS13_OK or not str(phf.get("verdict") or "").endswith(DL.D10.VEREDITO_SUFIXO) or "NOT_FALSIFIED" in str(phf.get("verdict")) or (phf.get("mecanica") or {}).get("passed") is not True or (phf.get("mecanica") or {}).get("n_checks") != DL.D10.N_CHECKS_HMS13 or (phf.get("mecanica") or {}).get("falhos")
        or dict(phf.get("campos") or {}) != dict(DL.D10.HMS13_CAMPOS) or phf.get("n_calibradores") != DL.D10.HMS13_CAMPOS["calibradores"] or phf.get("n_fontes_primarias") != DL.D10.HMS13_CAMPOS["fontes_primarias"] or phf.get("n_embutidos") != len(DL.D10.HMS13_EMBUTIDOS) or phf["contrato"]["n_embutidos_do_DL"] != phf.get("n_embutidos") or phf.get("n_pinos") != phf.get("n_pinos_ok") or phf.get("n_pinos") != phf.get("n_embutidos")
        or phf.get("sob_pasta_vedada") != [] or phf.get("com_nome_vedado") != [] or not isinstance(phf.get("n_caminhos_tocados"), int) or phf.get("pasta_vedada") != DL.D10.H0DN_PASTA_VEDADA or phf["contrato"]["pasta_vedada"] != DL.D10.H0DN_PASTA_VEDADA or phf.get("gate_verdict") != pia.get("gate_verdict") or phf.get("h0dn_selado") is not True
        or phf.get("does_not_gate_core") is not True or phf.get("beta_ok") is not True or phf.get("veredito_h0dn_source_sha256") != phb.get("veredito_h0dn_source_sha256")): falsos.append("ponto_hms13")
p11 = R["ponto_h0dn_v411"]   # (4i) o ponto NOVO da v411: o teste aberto, recalculado; as duas linhas; o P2 ao lado; o veto; o gate
if (p11.get("all_verified") is not True or p11.get("runtime_executed") is not True or p11.get("observed_vector_read") is not True or p11.get("opened_once") is not True or p11.get("does_not_gate_core") is not True or p11.get("beta_ok") is not True
        or not p11.get("dentro_do_bloco_executado") or not p11.get("logo_depois_da_instrucao_do_hms13") or not p11.get("logo_antes_do_emit_figures") or not p11.get("chama_tambem_os_specs_v411")
        or not str(p11.get("verdict") or "").startswith(DL.VEREDITO_OK_PREFIXO) or not str(p11.get("verdict") or "").endswith(DL.VEREDITO_SUFIXO) or (p11.get("mecanica") or {}).get("passed") is not True or (p11.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FECHO or (p11.get("mecanica") or {}).get("falhos")
        or p11.get("ramo_primario") != p11["contrato"]["ramo_primario"] or p11.get("ramo_cefeidas_livres") != p11["contrato"]["ramo_cefeidas_livres"] or not p11.get("cabeca_do_teste") or not p11.get("outcome") or p11.get("linha_ao_lado_cefeidas_livres") is not True or p11.get("n_ressalvas_secao8") != 7
        or p11.get("gate_verdict") != p11["contrato"]["gate_verdict"] or p11.get("gate_verdict") != pia.get("gate_verdict") or p11.get("escada") != p11["contrato"]["escada"] or p11.get("sob_pasta_vedada") or p11["contrato"]["pasta_vedada"] != DL.H0DN_PASTA_VEDADA_V410
        or not isinstance(p11.get("p2_ao_lado_da_v387"), dict) or DL.P2_TOKEN_SELADO not in str((p11.get("p2_ao_lado_da_v387") or {}).get("rotulo_selado_da_v387")) or DL.P2_TOKEN_SELADO in str((p11.get("p2_ao_lado_da_v387") or {}).get("rotulo"))
        or (p11.get("c14_inclui_o_p2_da_v387") or {}).get("ok") is not True or p11.get("v387_veredito_selado_igual_ao_da_base") is not True): falsos.append("ponto_h0dn_v411")
if (R.get("pasta_vedada_kimi_no_exame") or {}).get("lidos_sob_a_pasta") or (R.get("pasta_vedada_kimi_no_exame") or {}).get("escritos_sob_a_pasta"): falsos.append("pasta_vedada_kimi_tocada_no_exame")   # (o veto da gerencia: nenhum arquivo sob kimi\ e' lido nem escrito pelas instrucoes do main)
if R["troca_dita_v411"]["ok"] is not True: falsos.append("troca_dita_v411")
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

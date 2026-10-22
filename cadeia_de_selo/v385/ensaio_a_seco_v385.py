# -*- coding: utf-8 -*-
"""ensaio_a_seco_v385.py -- ENSAIO A SECO da v385 (molde: ensaio_a_seco_v384.py), SEM a GPU do rito e SEM o kernel do rito.

uso: python ensaio_a_seco_v385.py <candidato.py> <rotulo> <resultado_de_fumaca.json>

(1) copia o CANDIDATO para dry_<rotulo>/um.py e materializa ali o kernel EMBUTIDO dele;
(2) IMPORTA o candidato (stdout silenciado; o rito NAO roda);
(3) o FLUXO PRINCIPAL da v385: as instrucoes do main() que COMECAM numa linha marcada v385 sao EXECUTADAS com o core da v384 (o canonico selado) e com:
    o registro do pilar montado pela PROPRIA _qp_summary do candidato a partir de um resultado de FUMACA (marcado ENSAIO); um CACHE SINTETICO em
    dry_<rotulo>/cache_sintetico com esse mesmo resultado (o «anterior», conferido pelo sha256 pela propria _qp_cached_ok); e as bandeiras da v385 (29)
    LIDAS do relatorio do kernel do sandbox (v385/kernel/sandbox_raiz_v385.json) postas no kernel_formalization -- marcadas SINTETICAS no relatorio;
(4) build_pt / build_en (+ _tex_guard_nan), pdflatex x2 com -halt-on-error; e as VARIANTES da v385 (a pedra nao selou; sem rodada anterior; igual a
    menos de arredondamento; diferente) -- cada uma compila e diz a sua frase;
(5) testes de UNIDADE do comparador da reprodutibilidade e do Axioma (bandeiras faltando; nome do kernel ausente);
(6) o markdown canonico (o carimbo v385; a errata ao lado do «postulado irredutivel», que fica) e o manifesto; a guarda do rito (vereditos proibidos)."""
import copy, hashlib, io, json, os, re, shutil, subprocess, sys, time, ast, builtins, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "v383"))
from carregar_embutido import carregar  # noqa: E402

NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CORE0P = os.path.join(NOS, "um_absoluto.json")     # o core da v384 SELADA (o canonico)
cand, rot, fumaca = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
DRY = os.path.join(HERE, "dry_" + rot)
if os.path.isdir(DRY):
    shutil.rmtree(DRY)
os.makedirs(DRY)
shutil.copyfile(os.path.join(HERE, cand), os.path.join(DRY, "um.py"))
EMB, _, _, h16 = carregar(os.path.join(DRY, "um.py"))
for rel, content in EMB.items():
    p = os.path.join(DRY, "tgl_kernel", *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="").write(content)
KREP = json.load(open(os.path.join(HERE, "kernel", "sandbox_raiz_v385.json"), encoding="utf-8"))
rep = {"candidato": cand, "sha16": h16, "kernel_materializado_no_dry": len(EMB), "core0_sha16": hashlib.sha256(open(CORE0P, "rb").read()).hexdigest()[:16],
       "fumaca": fumaca, "fumaca_sha16": hashlib.sha256(open(fumaca, "rb").read()).hexdigest()[:16],
       "SINTETICO": "as bandeiras da v385 (29) no kernel_formalization vem do relatorio do SANDBOX (nao do rito); o resultado anterior do pilar e' a FUMACA num cache sintetico"}
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
t0 = time.time()
try:
    import um
finally:
    _imp = sys.stdout.getvalue(); sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
rep["import_s"] = round(time.time() - t0, 1)
assert os.path.normcase(um.FORMAL_DIR) == os.path.normcase(os.path.join(DRY, "tgl_kernel")), um.FORMAL_DIR
assert um.UM_VERSION == "v385"
R0 = json.load(open(CORE0P, encoding="utf-8"))
core0, verdict = R0["core"], R0["verdict"]
assert "quantum_pillar_v384" in core0 and "the_axiom_v385" not in core0
print("import ok (%.1f s); FORMAL_DIR = dry" % rep["import_s"])

# o registro do pilar a partir da FUMACA (o mesmo codigo do rito), marcado ENSAIO
RF = json.load(open(fumaca, encoding="utf-8"))
_spf = os.path.join(os.path.dirname(fumaca), "spec_fumaca.json")
_SF = json.load(open(_spf, encoding="utf-8"))
assert RF.get("run_id") and str(_SF.get("id", "")).endswith("__FUMACA"), "o resultado nao e' de uma fumaca"
assert RF.get("worker_sha256") == hashlib.sha256(um._QP_WORKER_SRC.encode("utf-8")).hexdigest(), "a fumaca e' de OUTRO trabalhador que o embutido no candidato"
assert str(RF.get("verdict", "")).startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__"), "a fumaca nao completou"
FIX = {"theorem": "ENSAIO A SECO -- registro montado de um resultado de FUMACA; NAO e resultado", "status": "[ENSAIO]", "key": "ENSAIO_SEM_CHAVE", "mode": "COMPUTE",
       "verdict": str(RF.get("verdict")).replace("__GATE_UNTOUCHED", "__ENSAIO_FUMACA_NAO_E_RESULTADO__GATE_UNTOUCHED"), "custody_chain_ok": True,
       "summary": um._qp_summary(RF), "all_verified": False, "reuse": {"reused": False, "reading": "ENSAIO"}, "does_not_gate_core": True,
       "result_sha256": hashlib.sha256(open(fumaca, "rb").read()).hexdigest(), "run_id": RF.get("run_id"), "finished": RF.get("finished"),
       "spec_sha256_in_result": RF.get("spec_sha256"), "worker_sha256": RF.get("worker_sha256"), "beta_hex": RF.get("beta_hex")}   # as ENTRADAS, como o registro do rito
# o CACHE SINTETICO com o resultado «anterior» (a propria fumaca), conferido pela propria _qp_cached_ok do candidato
CS = os.path.join(DRY, "cache_sintetico", "ENSAIO_CHAVE")
os.makedirs(CS)
shutil.copyfile(fumaca, os.path.join(CS, "result.json"))
open(os.path.join(CS, "result.json.sha256"), "w", encoding="ascii").write(hashlib.sha256(open(fumaca, "rb").read()).hexdigest())
ST_STUB = {"mode": "COMPUTE", "cache_dir": CS, "key": "ENSAIO_CHAVE"}
FLAGS = list(um._AXM_FLAGS_V385) + list(um._DKS_FLAGS_V385)
NF = len(FLAGS); assert NF == 29 and all(KREP["bandeiras"].get(f) is True for f in FLAGS)
core_s = json.loads(json.dumps(core0))
core_s["quantum_pillar_v384"] = copy.deepcopy(FIX)
core_s["kernel_formalization"] = dict(core_s.get("kernel_formalization") or {}, **{f: True for f in FLAGS})   # SINTETICO: do relatorio do sandbox

TAG = "v385"
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]
lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if TAG in l}
NL = chr(10)
comeca = [st for st in main.body if st.lineno in tagged]
bad = []
for st in comeca:
    _ligados = {h.name for h in ast.walk(st) if isinstance(h, ast.ExceptHandler) and h.name}   # os nomes ligados no proprio comando (except ... as x)
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ("core", "_QP_ST_V384", "_QP_PREV_V385") or node.id in _ligados):
                bad.append((node.lineno, node.id))
ns = dict(vars(um)); ns["core"] = core_s; ns["_QP_ST_V384"] = copy.deepcopy(ST_STUB)
code = NL.join(textwrap.dedent(NL.join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:%s>" % TAG, "exec"), ns)
    _mf_out = sys.stdout.getvalue(); _mf_err = None
except Exception as e:  # noqa
    _mf_out = sys.stdout.getvalue(); _mf_err = repr(e)
finally:
    sys.stdout = _o
c = ns["core"]
rep["mainflow"] = {"comeca": len(comeca), "nomes_nao_resolvidos": bad, "erro": _mf_err, "chaves_novas_no_core": [k for k in c if k not in core0], "stdout": _mf_out.strip().splitlines()}
_ax = c.get("the_axiom_v385") or {}; _rp = c.get("quantum_pillar_reproducibility_v385") or {}
rep["mainflow"]["axioma"] = {k: _ax.get(k) for k in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "final_step_name_matches_kernel", "final_step_name_from_kernel_error")}
rep["mainflow"]["reprodutibilidade"] = {k: _rp.get(k) for k in ("verdict", "compared", "n_fields", "n_differ")}
print("fluxo principal:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False))
mf_ok = (not bad and not _mf_err and len(comeca) == 5 and sorted(rep["mainflow"]["chaves_novas_no_core"]) == ["quantum_pillar_reproducibility_v385", "the_axiom_v385"]
         and _ax.get("all_verified") is True and _ax.get("kernel_flags_ok") == NF and _ax.get("final_step_name_matches_kernel") is True
         and str(_ax.get("verdict", "")).startswith("TGL_THE_AXIOM_V385__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED__") and ("__KERNEL_%d_OF_%d__" % (NF, NF)) in str(_ax.get("verdict"))
         and "REPRODUCED_BIT_FOR_BIT" in str(_rp.get("verdict")) and _rp.get("n_differ") == 0 and (_rp.get("n_fields") or 0) > 50)

# (5) testes de UNIDADE
U = {}
_rec = copy.deepcopy(FIX); _prev = {"read": True, "summary": copy.deepcopy(FIX["summary"]), "verdict": FIX["verdict"], "sha256": "x", "finished": "x", "run_id": "x", "key": "x",
                                     "inputs": {"spec_sha256": FIX["spec_sha256_in_result"], "worker_sha256": FIX["worker_sha256"], "beta_hex": FIX["beta_hex"]}, "env": {}}
U["igual"] = "REPRODUCED_BIT_FOR_BIT" in um.quantum_pillar_reproducibility_v385(_prev, _rec)["verdict"]
_p2 = copy.deepcopy(_prev); _p2["summary"]["T2"]["gap_rel_min"] = _p2["summary"]["T2"]["gap_rel_min"] * (1 + 1e-12)
_r2 = um.quantum_pillar_reproducibility_v385(_p2, _rec); U["arredondamento"] = "WITHIN_ROUNDOFF" in _r2["verdict"] and _r2["n_differ"] == 1
_p3 = copy.deepcopy(_prev); _p3["summary"]["T4"]["unique"] = (_p3["summary"]["T4"].get("unique") or 0) + 1
_r3 = um.quantum_pillar_reproducibility_v385(_p3, _rec); U["diferente"] = "NOT_REPRODUCED" in _r3["verdict"] and _r3["n_differ"] == 1
U["sem_anterior"] = "NO_PREVIOUS_RUN" in um.quantum_pillar_reproducibility_v385({"read": False, "why_not": "x"}, _rec)["verdict"]
U["anterior_sem_resumo"] = "NO_PREVIOUS_RUN" in um.quantum_pillar_reproducibility_v385(dict(_prev, summary=None), _rec)["verdict"]
U["anterior_lido_do_cache_igual_ao_resumo"] = um.quantum_pillar_previous_v385(ST_STUB).get("summary") == um._qp_summary(RF)
U["reaproveitado"] = "NOT_COMPARED" in um.quantum_pillar_reproducibility_v385(_prev, dict(_rec, reuse={"reused": True}))["verdict"]
U["tempo_ignorado"] = "REPRODUCED_BIT_FOR_BIT" in um.quantum_pillar_reproducibility_v385(dict(_prev, summary=dict(copy.deepcopy(_prev["summary"]), phase_seconds={"T2": 1.0})), _rec)["verdict"]
# (afericao de codigo, achados 1-2 e notas 3-5) as regras novas do comparador
_pn = copy.deepcopy(_prev); _pn["summary"]["T2"]["gap_rel_min"] = float("nan")
_rn = um.quantum_pillar_reproducibility_v385(_pn, _rec); U["nan_e_diferenca"] = "NOT_REPRODUCED" in _rn["verdict"] and _rn["n_nonfinite_differ"] == 1
_fl = [(k_, v_) for k_, v_ in um._qp_flat_v385(_prev["summary"]) if isinstance(v_, float) and 0 < abs(v_) < 1e-10]
if _fl:
    _k0 = _fl[0][0].split("."); _pr = copy.deepcopy(_prev); _d = _pr["summary"]
    for _kk in _k0[:-1]:
        _d = _d[_kk]
    _d[_k0[-1]] = _d[_k0[-1]] * 1.06
    _rr = um.quantum_pillar_reproducibility_v385(_pr, _rec); U["residuo_de_maquina_e_arredondamento"] = "WITHIN_ROUNDOFF" in _rr["verdict"]
else:
    U["residuo_de_maquina_e_arredondamento"] = "SEM_CAMPO_RESIDUAL_NA_FUMACA (nao testado)"
_pd = copy.deepcopy(_prev); _pd["summary"]["D128"] = dict(_pd["summary"].get("D128") or {}, status_code="RAN", cci=0.123)
_rec_d = copy.deepcopy(_rec); _rec_d["summary"]["D128"] = dict(_rec_d["summary"].get("D128") or {}, status_code="NOT_RUN_SKIPPED_BY_DEADLINE")
_rd = um.quantum_pillar_reproducibility_v385(_pd, _rec_d); U["d128_excluido_dito"] = _rd.get("d128_excluded") is True and "D128_EXCLUDED_NOT_RUN_THIS_RUN" in _rd["verdict"] and "REPRODUCED_BIT_FOR_BIT" in _rd["verdict"]
_pi = copy.deepcopy(_prev); _pi["inputs"] = dict(_pi["inputs"], beta_hex="0x1.0p-7")
U["entradas_diferentes_nao_compara"] = "NOT_COMPARED_DIFFERENT_INPUTS" in um.quantum_pillar_reproducibility_v385(_pi, _rec)["verdict"]
_ps = copy.deepcopy(_prev); _ps["summary"]["D128"] = dict(_ps["summary"].get("D128") or {}, started=False)
_rs = copy.deepcopy(_rec); _rs["summary"]["D128"] = dict(_rs["summary"].get("D128") or {}, started=True)
U["started_booleano_comparado"] = "NOT_REPRODUCED" in um.quantum_pillar_reproducibility_v385(_ps, _rs)["verdict"]
_pr0 = um.quantum_pillar_previous_v385({"mode": "REUSE"})
U["sem_calculo_nesta_rodada_token"] = "NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT" in um.quantum_pillar_reproducibility_v385(_pr0, _rec)["verdict"]   # (3a passada, N5)
_p33 = copy.deepcopy(_prev); _r33 = copy.deepcopy(_rec); _p33["summary"]["T2"]["configs"] = 3; _r33["summary"]["T2"]["configs"] = 3.0
U["valor_igual_tipo_diferente_nao_e_bit_a_bit"] = "REPRODUCED_BIT_FOR_BIT" not in um.quantum_pillar_reproducibility_v385(_p33, _r33)["verdict"]   # (3a passada, N4)
U["anterior_fora_de_compute"] = um.quantum_pillar_previous_v385({"mode": "REUSE"})["read"] is False and um.quantum_pillar_previous_v385(None)["read"] is False
_k2 = dict(core_s["kernel_formalization"]); _k2.pop(FLAGS[0]); _a2 = um.the_axiom_v385(dict(core_s, kernel_formalization=_k2))
U["axioma_bandeira_faltando"] = (_a2["all_verified"] is False and "NOT_SEALED_THIS_RUN" in _a2["verdict"] and _a2["missing_flags"] == [FLAGS[0]])
_fd = um.FORMAL_DIR; um.FORMAL_DIR = os.path.join(DRY, "NAO_EXISTE")
try:
    _a3 = um.the_axiom_v385(core_s)
finally:
    um.FORMAL_DIR = _fd
U["axioma_sem_kernel"] = (_a3["all_verified"] is False and _a3["final_step_name_from_kernel"] is None and bool(_a3["final_step_name_from_kernel_error"]))
rep["unidade"] = U
print("unidade:", U)

# (4) o artigo e as variantes
DEVE = {"pt": ["Ao lado (v385): o Axioma e a testemunha falsa", "O Um é posto", "Errata ao lado", "[POSTO]", "Os dois pontos fixos da leitura", "é o Axioma",
               "é a testemunha falsa", "Do posto ao gradiente e à leitura", "O observador é conjugado", "O degrau final do gate chama-se Axioma",
               "AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER", "A reprodutibilidade do mundo quântico", "iguais bit a bit", "Introdução: o que este código faz agora (v384)",
               "compilado desde a v183", "axiomFlow_eq_exp", "testemunha falsa é a testemunha estática é o zero absoluto"],
        "en": ["Beside (v385): the Axiom and the false witness", "The One is posited", "Erratum beside", "[POSTO]", "The two fixed points of the reading", "is the Axiom",
               "is the false witness", "From the post to the gradient and to the reading", "The observer is conjugated", "The final step of the gate is named Axiom",
               "AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER", "The reproducibility of the quantum world", "identical bit for bit", "Introduction: what this code does now (v384)",
               "compiled since v183", "axiomFlow_eq_exp", "testemunha falsa é a testemunha estática é o zero absoluto"]}
NAO_DEVE = {"pt": ["desde a v181", "a testemunha estática, o zero absoluto", "medida [COMPUTED]"], "en": ["since v181", "the static witness, the absolute zero", "measured [COMPUTED]"]}
eng = shutil.which("pdflatex")
rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P))
    txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex)
    open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = []
    for _ in range(2 if duas else 1):
        r = subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
        rcs.append(r.returncode)
    log = open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()
    return tex, txt, rcs, log


for lang in ("pt", "en"):
    t0 = time.time()
    tex, txt, rcs, log = compilar(c, "dry_v385_%s" % lang, lang)
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v385_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in txt and w not in tex], "nan": len(re.findall(r"(?<![A-Za-z])nan(?![A-Za-z])", txt)),
                           "proibidas_na_secao": [w for w in NAO_DEVE[lang] if w in (txt[txt.find("Ao lado (v385)" if lang == "pt" else "Beside (v385)"):][:9000])],
                           "overfull": log.count("Overfull \\hbox"), "s": round(time.time() - t0, 1)}
    i0 = txt.find("Ao lado (v385)" if lang == "pt" else "Beside (v385)"); rep["artigo"][lang]["trecho"] = txt[i0:i0 + 3500] if i0 >= 0 else None
    print("artigo", lang, json.dumps({k: v for k, v in rep["artigo"][lang].items() if k != "trecho"}, ensure_ascii=False))
_ax_nao = um.the_axiom_v385(dict(core_s, kernel_formalization=dict(core0.get("kernel_formalization") or {})))
VARS = {"nao_selou_sem_anterior": ({"the_axiom_v385": _ax_nao, "quantum_pillar_reproducibility_v385": um.quantum_pillar_reproducibility_v385({"read": False, "why_not": "ENSAIO: sem rodada anterior"}, FIX)},
                                   {"pt": ["Nesta rodada a pedra não selou", "não houve comparação nesta rodada"], "en": ["In this run the stone did not seal", "there was no comparison in this run"]}),
        "arredondamento": ({"quantum_pillar_reproducibility_v385": _r2}, {"pt": ["iguais a menos de arredondamento"], "en": ["identical up to round-off"]}),
        "diferente": ({"quantum_pillar_reproducibility_v385": _r3}, {"pt": ["diferentes", "é resultado, e fica dito"], "en": ["different", "a result, and it is stated"]})}
rep["variantes"] = {}
for vn, (upd, deve) in VARS.items():
    cv = dict(copy.deepcopy(c), **copy.deepcopy(upd))
    for lang in ("pt", "en"):
        _tex, _txt, _rcs, _log = compilar(cv, "dry_v385_%s_%s" % (vn, lang), lang, duas=False)
        rep["variantes"]["%s_%s" % (vn, lang)] = {"pdflatex_rc": _rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v385_%s_%s.pdf" % (vn, lang))), "faltam": [w for w in deve[lang] if w not in _txt]}
print("variantes:", json.dumps(rep["variantes"], ensure_ascii=False))
mau_var = [k for k, v in rep["variantes"].items() if v["pdflatex_rc"] != [0] or not v["pdf_ok"] or v["faltam"]]
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["nan"] or v["proibidas_na_secao"]]
# as citacoes do operador, VERBATIM contra o transcrito (afericao de texto, achado 1), e as formas da errata no texto antigo (achado 7)
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v385.py"), DRY], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_do_operador"] = {"rc": _cc.returncode, "ultima": (_cc.stdout.strip().splitlines() or [""])[-1]}
print("citacoes:", rep["citacoes_do_operador"])

# (6) o markdown canonico e o manifesto
um.OUT = DRY
um.emit_canonical_md(c, verdict)
md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v385**" in md, "errata_posto": "Errata ao lado (v385, 05/10/2026, o operador)" in md, "postulado_antigo_fica": "o postulado irredutível" in md,
                   "axioma_no_md": "the_axiom_v385" in md, "todos_os_modulos": "TODOS OS MODULOS COM VEREDITO" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md")
um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c)
rep["manifest"] = {"carimbo": "**Versão v385**" in open(mani, encoding="utf-8").read()}
print("markdown:", rep["markdown"], "| manifesto:", rep["manifest"])
_GUARDA = ['if (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", _v)', 'or re.search(r"(?<!AP)PROVED_BY", _v)', 'or "TGL_PROVED" in _v or "CONSCIOUSNESS_PROVED" in _v):']
assert all(src.count(g) == 1 for g in _GUARDA), "a guarda do rito mudou no candidato -- atualizar o ensaio"
_proib = [k for k, _m in c.items() if isinstance(_m, dict) and (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", str(_m.get("verdict") or ""))
          or re.search(r"(?<!AP)PROVED_BY", str(_m.get("verdict") or "")) or "TGL_PROVED" in str(_m.get("verdict") or "") or "CONSCIOUSNESS_PROVED" in str(_m.get("verdict") or ""))]
_sel_read = re.search(r'"the_axiom_reading_v385": "([A-Z0-9_]+)"', src)
rep["guarda_do_rito_vereditos_proibidos"] = _proib
rep["leitura_do_selo_v385_limpa"] = bool(_sel_read) and not (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", _sel_read.group(1)) or re.search(r"(?<!AP)PROVED_BY", _sel_read.group(1)))
ok = (mf_ok and all(v_ is True or str(v_).startswith("SEM_CAMPO") for v_ in U.values()) and not mau and rep["citacoes_do_operador"]["rc"] == 0 and not mau_var and all(rep["markdown"].values()) and rep["manifest"]["carimbo"] and not _proib and rep["leitura_do_selo_v385_limpa"])
rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"fluxo": mf_ok, "unidade": U, "artigo": mau, "variantes": mau_var, "md": rep["markdown"], "mani": rep["manifest"],
                                                                     "proib": _proib, "selo": rep["leitura_do_selo_v385_limpa"]}, ensure_ascii=False))
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"]))
sys.exit(0 if ok else 1)

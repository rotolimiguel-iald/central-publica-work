# -*- coding: utf-8 -*-
"""ensaio_a_seco_v386.py -- ENSAIO A SECO da v386 (molde: ensaio_a_seco_v385.py), SEM a GPU do rito e SEM o kernel do rito.

uso: python ensaio_a_seco_v386.py <candidato.py> <rotulo>

(1) copia o CANDIDATO para dry_<rotulo>/um.py e materializa ali o kernel EMBUTIDO dele;
(2) IMPORTA o candidato (stdout silenciado; o rito NAO roda); confere UM_VERSION, _QP_REUSE_V386, as 110 bandeiras no dicionario e a escada (6137);
(3) o FLUXO PRINCIPAL da v386: as instrucoes do main() que COMECAM numa linha marcada v386 sao EXECUTADAS com o core da v385 (o canonico selado), com o
    registro do pilar na forma REAPROVEITADA (o que o reuse pela chave produz: mode REUSE, reused True, o mesmo veredito/sha256/chave da v385 selada), a
    reprodutibilidade v385 na forma honesta sob reuse (NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT, calculada pela PROPRIA funcao v385 do candidato) e as
    110 bandeiras da v386 LIDAS do relatorio do kernel do sandbox postas no kernel_formalization -- marcadas SINTETICAS no relatorio;
(4) testes de UNIDADE: the_verb_v386 (bandeira faltando; token do pino diferente; kernel materializado ausente; verbatim embutido adulterado); ramo_b (hash
    errado; arquivo ausente; arquivo adulterado; pino errado; beta errado; tudo certo); ledger_errata (ramo B nao lido; livro v383 adulterado; verbatim
    adulterado); quantum_pillar_reuse (reaproveitado ok; sha diferente; calculado de novo; nem um nem outro); a funcao v385 sob reuse;
(5) build_pt / build_en (+ _tex_guard_nan), pdflatex x2 com -halt-on-error; os DEVE/NAO_DEVE; e as VARIANTES (a pedra nao selou + V1 nao lido + pilar calculado
    de novo; pilar nem um nem outro) -- cada uma compila e diz a sua frase;
(6) o markdown canonico (o carimbo v386; a errata ao lado de R6; a errata v385 fica) e o manifesto; a guarda do rito (vereditos proibidos); a leitura v386 do selo;
(7) o conferidor de citacoes (estrito) com rc 0."""
import copy, hashlib, io, json, os, re, shutil, subprocess, sys, time, ast, builtins, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.dirname(HERE); SP = os.path.dirname(V6)
sys.path.insert(0, os.path.join(SP, "v383"))
from carregar_embutido import carregar  # noqa: E402

NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CORE0P = os.path.join(NOS, "um_absoluto.json")     # o core da v385 SELADA (o canonico)
cand, rot = sys.argv[1], sys.argv[2]
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
KREP = json.load(open(os.path.join(V6, "kernel", "sandbox_raiz_v386.json"), encoding="utf-8"))
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v386.json"), encoding="utf-8"))
assert CM["sha16"] == h16, "o candidato copiado nao e' o do registro"
rep = {"candidato": cand, "sha16": h16, "kernel_materializado_no_dry": len(EMB), "core0_sha16": hashlib.sha256(open(CORE0P, "rb").read()).hexdigest()[:16],
       "SINTETICO": "as 110 bandeiras da v386 no kernel_formalization vem do relatorio do SANDBOX (nao do rito); o registro do pilar e' o da v385 selada posto na forma REAPROVEITADA; nenhuma GPU"}
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
assert um.UM_VERSION == "v386" and um._QP_REUSE_V386 is True
R0 = json.load(open(CORE0P, encoding="utf-8"))
core0, verdict = R0["core"], R0["verdict"]
assert "quantum_pillar_v384" in core0 and "the_axiom_v385" in core0 and "the_verb_v386" not in core0
FLAGS = list(um._VRB_FLAGS_V386) + list(um._ANG_FLAGS_V386)
NF = len(FLAGS); assert NF == 110 and all(KREP["bandeiras"].get(f) is True for f in FLAGS) and all(f in um._LEAN_THEOREM_FLAGS for f in FLAGS)
print("import ok (%.1f s); FORMAL_DIR = dry; UM_VERSION %s; bandeiras v386 no dicionario: %d" % (rep["import_s"], um.UM_VERSION, NF))

# o core sintetico: a v385 selada + as bandeiras + o pilar na forma REAPROVEITADA + a reprodutibilidade v385 sob reuse (pela propria funcao do candidato)
core_s = json.loads(json.dumps(core0))
core_s["kernel_formalization"] = dict(core_s.get("kernel_formalization") or {}, **{f: True for f in FLAGS})   # SINTETICO: do relatorio do sandbox
QP = core_s["quantum_pillar_v384"]
CDIR = (QP.get("reuse") or {}).get("saved_to_cache")
assert CDIR and os.path.isdir(CDIR) and hashlib.sha256(open(os.path.join(CDIR, "result.json"), "rb").read()).hexdigest() == QP["result_sha256"]
QP_REUSED = dict(copy.deepcopy(QP), mode="REUSE", run_dir=CDIR, reuse={"reused": True, "from_run_finished": QP.get("finished"), "cache_dir": CDIR,
                                                                      "reading": "V386__PILAR_QUANTICO_REAPROVEITADO_DA_RODADA_SELADA_V385_PELA_CHAVE__O_PILAR_NAO_E_OBJETO_DESTA_VERSAO"})
for k_ in ("worker_rc", "timed_out"):
    QP_REUSED.pop(k_, None)
core_s["quantum_pillar_v384"] = QP_REUSED
ST_REUSE = {"mode": "REUSE", "cache_dir": CDIR, "key": QP["key"], "checkpoint_switch": False}
_prev_reuse = um.quantum_pillar_previous_v385(ST_REUSE)
core_s["quantum_pillar_reproducibility_v385"] = um.quantum_pillar_reproducibility_v385(_prev_reuse, QP_REUSED)
rep["reprodutibilidade_v385_sob_reuse"] = core_s["quantum_pillar_reproducibility_v385"]["verdict"]
assert "NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT" in rep["reprodutibilidade_v385_sob_reuse"] and _prev_reuse.get("not_compute") is True
# a escada com as bandeiras sinteticas: 6137/6137
_el = um.prove_external_ladder(1.0, core_s["kernel_formalization"])
rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]
assert rep["escada"] == [CM["escada"][1], CM["escada"][1]] == [6137, 6137], rep["escada"]

TAG = "v386"
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]
lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if TAG in l}
NL = chr(10)
comeca = [st for st in main.body if st.lineno in tagged]
bad = []
for st in comeca:
    _ligados = {h.name for h in ast.walk(st) if isinstance(h, ast.ExceptHandler) and h.name}
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ("core", "_QP_ST_V384") or node.id in _ligados):
                bad.append((node.lineno, node.id))
ns = dict(vars(um)); ns["core"] = core_s; ns["_QP_ST_V384"] = copy.deepcopy(ST_REUSE)
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
NOVAS = ["ledger_errata_v386", "quantum_pillar_reuse_v386", "ramo_b_preregistration_v386", "the_verb_v386"]
rep["mainflow"] = {"comeca": len(comeca), "nomes_nao_resolvidos": bad, "erro": _mf_err, "chaves_novas_no_core": sorted(k for k in c if k not in core0), "stdout": _mf_out.strip().splitlines()}
_vb = c.get("the_verb_v386") or {}; _rb = c.get("ramo_b_preregistration_v386") or {}; _le = c.get("ledger_errata_v386") or {}; _qr = c.get("quantum_pillar_reuse_v386") or {}
rep["mainflow"]["verbo"] = {k: _vb.get(k) for k in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "token_matches_kernel", "verbatim_hashes_ok", "token_error")}
rep["mainflow"]["ramo_b"] = {k: _rb.get(k) for k in ("verdict", "all_verified", "read_ok", "conjunto_D_n", "beta", "pins_ok", "recompute_ok", "F2b_status", "errors", "forbidden_words_in_transcribed_fields")}
rep["mainflow"]["errata"] = {k: _le.get(k) for k in ("verdict", "all_verified", "v383_ledger_intact")}
rep["mainflow"]["pilar_reuse"] = {k: _qr.get(k) for k in ("verdict", "all_verified", "reused", "result_sha256_matches_v385_sealed", "verdict_same_as_v385_sealed")}
print("fluxo principal:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False)[:3000])
mf_ok = (not bad and not _mf_err and len(comeca) == 8 and rep["mainflow"]["chaves_novas_no_core"] == NOVAS
         and _vb.get("all_verified") is True and _vb.get("kernel_flags_ok") == NF and _vb.get("token_matches_kernel") is True and _vb.get("verbatim_hashes_ok") is True
         and str(_vb.get("verdict", "")).startswith("TGL_THE_VERB_V386__THE_VERB_SELECTS_THE_ACTION__") and ("__KERNEL_%d_OF_%d__" % (NF, NF)) in str(_vb.get("verdict")) and str(_vb.get("verdict")).endswith("__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED")
         and _vb.get("token_from_kernel") == um._VERB_TOKEN_V386 == CM["token_lido_da_pedra"]
         and _rb.get("all_verified") is True and _rb.get("read_ok") is True and _rb.get("conjunto_D_n") == 14 and str(_rb.get("verdict", "")).startswith("TGL_RAMO_B_PREREGISTERED_V386__V1_READ_BY_HASH_")
         and str(_rb.get("verdict", "")).endswith("__AWAITING_DATA__NOTHING_OPENED__GATE_UNTOUCHED") and not _rb.get("errors")
         and _le.get("all_verified") is True and _le.get("v383_ledger_intact") is True and str(_le.get("verdict", "")).startswith("TGL_LEDGER_ERRATA_V386__R6_CLOSED_TO_REOPENED_BY_PREREGISTRATION_BESIDE_NOT_OVERWRITTEN__")
         and (_le.get("charge_F2b") or {}).get("token") == "AWAITING"
         and _qr.get("all_verified") is True and _qr.get("reused") is True and "REUSED_FROM_THE_SEALED_V385_RUN_BY_KEY__RESULT_SHA256_MATCHES__VERDICT_SAME__CUSTODY_CHAIN_OK" in str(_qr.get("verdict")))

# (4) testes de UNIDADE
U = {}
_k2 = dict(core_s["kernel_formalization"]); _k2.pop(FLAGS[0]); _a2 = um.the_verb_v386(dict(core_s, kernel_formalization=_k2))
U["verbo_bandeira_faltando"] = (_a2["all_verified"] is False and "NOT_SEALED_THIS_RUN" in _a2["verdict"] and _a2["missing_flags"] == [FLAGS[0]] and _a2["verdict"].endswith("__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED"))
_tk = um._VERB_TOKEN_V386; um._VERB_TOKEN_V386 = _tk + "_X"
try:
    _a3 = um.the_verb_v386(core_s)
finally:
    um._VERB_TOKEN_V386 = _tk
U["verbo_token_do_pino_diferente"] = (_a3["all_verified"] is False and _a3["token_matches_kernel"] is False and "TOKEN_DOES_NOT_MATCH" in _a3["verdict"])
_fd = um.FORMAL_DIR; um.FORMAL_DIR = os.path.join(DRY, "NAO_EXISTE")
try:
    _a4 = um.the_verb_v386(core_s)
finally:
    um.FORMAL_DIR = _fd
U["verbo_sem_kernel_materializado"] = (_a4["all_verified"] is False and _a4["token_from_materialized_stone"] is None and bool(_a4["token_error"]) and _a4["token_from_kernel"] == _tk)
_vv = um._V386_OPERATOR_VERBATIM; _vv2 = copy.deepcopy(_vv); _vv2["files"]["verbo_20261005_1653"]["text"] = _vv2["files"]["verbo_20261005_1653"]["text"] + " "
um._V386_OPERATOR_VERBATIM = _vv2
try:
    _a5 = um.the_verb_v386(core_s)
finally:
    um._V386_OPERATOR_VERBATIM = _vv
U["verbo_verbatim_adulterado"] = (_a5["all_verified"] is False and _a5["verbatim_hashes_ok"] is False and "VERBATIM_FAILED" in _a5["verdict"] and _a5["verbatim_files"]["verbo_20261005_1653"]["embedded_matches_sha256"] is False)
# ramo B: copias adulteradas no dry
P0 = um._V386_RAMO_B_PREREG
_pj = copy.deepcopy(P0); _pj["files"]["json"]["sha256"] = "0" * 64
_r1 = um.ramo_b_preregistration_v386(core_s, _pj); U["ramo_b_sha_errado"] = (_r1["all_verified"] is False and _r1["read_ok"] is False and "V1_NOT_READ__FILES_JSON__AWAITING_PREREGISTRATION__NOTHING_OPENED__GATE_UNTOUCHED" in _r1["verdict"])
_pm = copy.deepcopy(P0); _pm["files"]["md"]["path"] = os.path.join(DRY, "NAO_EXISTE.md")
_r2 = um.ramo_b_preregistration_v386(core_s, _pm); U["ramo_b_arquivo_ausente"] = (_r2["all_verified"] is False and "FILES_MD" in _r2["verdict"] and bool(_r2["errors"].get("md")))
_adu = os.path.join(DRY, "V1_adulterado.json"); _bj = open(P0["files"]["json"]["path"], "rb").read().replace(b'"n_elegiveis": 14', b'"n_elegiveis": 15')
assert _bj != open(P0["files"]["json"]["path"], "rb").read()
open(_adu, "wb").write(_bj)
_pa = copy.deepcopy(P0); _pa["files"]["json"]["path"] = _adu
_r3 = um.ramo_b_preregistration_v386(core_s, _pa); U["ramo_b_json_adulterado"] = (_r3["all_verified"] is False and "FILES_JSON" in _r3["verdict"])
_pa2 = copy.deepcopy(P0); _pa2["files"]["json"]["path"] = _adu; _pa2["files"]["json"]["sha256"] = hashlib.sha256(_bj).hexdigest(); _pa2["files"]["json"]["bytes"] = len(_bj)
_r3b = um.ramo_b_preregistration_v386(core_s, _pa2); U["ramo_b_json_adulterado_com_hash_trocado_pega_pelo_spec_sha256"] = (_r3b["all_verified"] is False and ("SPEC_SHA256_MISMATCH" in _r3b["verdict"] or "HASHES_FILE_MISMATCH" in _r3b["verdict"]))
_pp = um._V386_RAMO_B_PINS; _pp2 = copy.deepcopy(_pp); _pp2["poder_exato_A31"]["value"] = 0.0
um._V386_RAMO_B_PINS = _pp2
try:
    _r4 = um.ramo_b_preregistration_v386(core_s)
finally:
    um._V386_RAMO_B_PINS = _pp
U["ramo_b_pino_errado"] = (_r4["all_verified"] is False and _r4["read_ok"] is True and "PINS_MISMATCH" in _r4["verdict"] and _r4["pins"]["poder_exato_A31"]["equal"] is False)
_r5 = um.ramo_b_preregistration_v386(dict(core_s, beta=float(core_s["beta"]) * 1.01)); U["ramo_b_beta_errado"] = (_r5["all_verified"] is False and "BETA_MISMATCH" in _r5["verdict"])
_r6 = um.ramo_b_preregistration_v386(core_s)
U["ramo_b_tudo_certo"] = (_r6["all_verified"] is True and _r6["read_ok"] is True and _r6["conjunto_D_n"] == 14 and _r6["pins_ok"] and _r6["recompute_ok"] and _r6["beta_ok"]
                          and abs(_r6["beta"]["rel_diff"]) < 1e-9 and _r6["F2b_status"] == "AWAITING" and _r6["veredito_do_V1"] == "AWAITING_DATA" and len(_r6["transcribed"]) == len(um._V386_RAMO_B_FIELDS)
                          and _r6["nothing_opened"] is True and str(_r6["token_estado"]).endswith("__AWAITING_DATA__PRE_REGISTERED_BY_HASH__GATE_UNTOUCHED"))
rep["ramo_b_beta_v1_vs_core"] = _r6["beta"]; rep["ramo_b_palavras_proibidas_nos_campos_transcritos"] = _r6["forbidden_words_in_transcribed_fields"]
# ledger_errata
_e1 = um.ledger_errata_v386(core_s, _r1); U["errata_com_ramo_b_nao_lido"] = (_e1["all_verified"] is False and "F2B_AWAITING_PREREGISTRATION_V1_NOT_READ" in _e1["verdict"] and _e1["charge_F2b"]["token"] == "AWAITING_PREREGISTRATION__V1_NOT_READ" and _e1["v383_ledger_intact"] is True)
_cl = json.loads(json.dumps(core_s)); _cl["the_ledger_of_charges_v383"]["corrections_beside_20261002"]["R6"] = "x"
_e2 = um.ledger_errata_v386(_cl, _r6); U["errata_com_livro_v383_adulterado"] = (_e2["all_verified"] is False and "V383_LEDGER_NOT_INTACT" in _e2["verdict"])
um._V386_OPERATOR_VERBATIM = _vv2
try:
    _e3 = um.ledger_errata_v386(core_s, _r6)
finally:
    um._V386_OPERATOR_VERBATIM = _vv
U["errata_com_verbatim_adulterado"] = (_e3["all_verified"] is False and "VERBATIM_HASH_FAILED" in _e3["verdict"])
_e4 = um.ledger_errata_v386(core_s, _r6); U["errata_tudo_certo"] = (_e4["all_verified"] is True and _e4["charge_F2b"]["token"] == "AWAITING" and _e4["charge_F2b"]["lado"] == "face" and _e4["v383_n_charges"] == 11 and _e4["F2_untouched"] and _e4["R2_untouched"]
                                                                      and "REABERTO POR PRÉ-REGISTRO" in _e4["corrections_beside_20261005"]["R6"] and _e4["operator_decision_20261005"]["verbatim"].startswith("eu não havia proibido o ramo B"))
# o pilar
_q1 = um.quantum_pillar_reuse_v386(ST_REUSE, QP_REUSED); U["pilar_reaproveitado_ok"] = (_q1["all_verified"] is True and "RESULT_SHA256_MATCHES__VERDICT_SAME__CUSTODY_CHAIN_OK" in _q1["verdict"])
_q2 = um.quantum_pillar_reuse_v386(ST_REUSE, dict(QP_REUSED, result_sha256="0" * 64)); U["pilar_reaproveitado_sha_diferente"] = (_q2["all_verified"] is False and "RESULT_SHA256_DIFFERS" in _q2["verdict"])
_q3 = um.quantum_pillar_reuse_v386({"mode": "COMPUTE", "reuse_refused": {"env_now": {}}}, QP); U["pilar_calculado_de_novo"] = (_q3["all_verified"] is True and "COMPUTED_AGAIN_THIS_RUN_REUSE_REFUSED_ENV_OR_ENGINE_DIFFERS__VERDICT_SAME_AS_V385" in _q3["verdict"])
_q4 = um.quantum_pillar_reuse_v386({"refused": "LAUNCH_FAILED"}, {"mode": None, "verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__X__GATE_UNTOUCHED"}); U["pilar_nem_um_nem_outro"] = (_q4["all_verified"] is False and "NEITHER_REUSED_NOR_COMPUTED" in _q4["verdict"])
U["v385_sob_reuse_diz_nao_comparou"] = "NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT" in um.quantum_pillar_reproducibility_v385(um.quantum_pillar_previous_v385(ST_REUSE), QP_REUSED)["verdict"]
U["v385_registro_intocado_no_candidato"] = (src.count('_QP_PREV_V385 = quantum_pillar_previous_v385(_QP_ST_V384)') == 1 and src.count('core["the_axiom_v385"] = the_axiom_v385(core)') == 1 and src.count("def the_axiom_v385(") == 1)
U["reuse_pela_chave_no_start"] = ("if _RITE_CKPT_ON or _QP_REUSE_V386:" in src) and src.count("_QP_REUSE_V386") >= 5
rep["unidade"] = U
print("unidade:", U)

# (5) o artigo e as variantes
DEVE = {"pt": ["Ao lado (v386): o Verbo seleciona; o ramo B reaberto por pré-registro", "O Verbo seleciona", "Verbo=seleção da ação", "o Nome não é ontologia", "TheVerbSelectsTheAction",
               "Verdade e custo, duas faces do mesmo objeto", "O tempo lido duas vezes; a luz e a gravidade", "a constante da luz ao cubo", "A Lagrangiana; a delegação", "o resto vc consegue responder tudo agroa",
               "O ramo B reaberto por pré-registro; a errata ao lado de R6", "eu não havia proibido o ramo B", "REABERTO POR PRÉ-REGISTRO", "PREREG_RAMO_B_RINGDOWN_20261005_V1", "Nesta rodada o V1 foi lido por hash",
               "conjunto D com 14 eventos elegíveis", "NADA foi aberto", "O pilar quântico nesta versão", "foi REAPROVEITADO da rodada selada v385", "THE_VERB_SELECTS_THE_ACTION__THE_NAME_IS_THE_POST",
               "TGL_THE_VERB_V386__THE_VERB_SELECTS_THE_ACTION__", "TGL_RAMO_B_PREREGISTERED_V386__V1_READ_BY_HASH_", "TGL_LEDGER_ERRATA_V386__R6_CLOSED_TO_REOPENED_BY_PREREGISTRATION",
               "Ao lado (v385): o Axioma e a testemunha falsa", "Introdução: o que este código faz agora (v384)", "nunca o quadrado de", "Selecionar o nome defasa o tempo",
               # W10 (ordem do operador 05/10): o teste em tempo real na GPU na apresentacao, no resumo («O método») e nas palavras-chave
               "calcula em tempo real na GPU", "é calculado em tempo real na GPU, em paralelo com o kernel e os ritos", "sistema quântico aberto (GKLS) calculado em tempo real na GPU"],
        "en": ["Beside (v386): the Verb selects; branch B reopened by preregistration", "The Verb selects", "Verbo=seleção da ação", "o Nome não é ontologia", "TheVerbSelectsTheAction",
               "Truth and cost, two faces of one object", "Time read twice; light and gravity", "a constante da luz ao cubo", "The Lagrangian; the delegation", "o resto vc consegue responder tudo agroa",
               "Branch B reopened by preregistration; the erratum beside R6", "eu não havia proibido o ramo B", "REOPENED BY PREREGISTRATION", "PREREG_RAMO_B_RINGDOWN_20261005_V1", "In this run V1 was read by hash",
               "set D with 14 eligible events", "NOTHING was opened", "The quantum pillar in this version", "it was REUSED from the sealed v385 run", "THE_VERB_SELECTS_THE_ACTION__THE_NAME_IS_THE_POST",
               "TGL_THE_VERB_V386__THE_VERB_SELECTS_THE_ACTION__", "TGL_RAMO_B_PREREGISTERED_V386__V1_READ_BY_HASH_", "TGL_LEDGER_ERRATA_V386__R6_CLOSED_TO_REOPENED_BY_PREREGISTRATION",
               "Beside (v385): the Axiom and the false witness", "Introduction: what this code does now (v384)", "never the square of", "Selecionar o nome defasa o tempo",
               "computes in real time on the GPU", "is computed in real time on the GPU, in parallel with the kernel and the rites", "open quantum system (GKLS) computed in real time on the GPU"]}
# W10: o sumario (.toc do pdflatex) passa a listar «Ao lado (v385)», «Introdução … (v384)» e a «Nota: … GPU e como» (fragmentos sem acento, robustos ao .toc); e a
# oracao da GPU na apresentacao (linha 2 do .txt), no «O método»/«The method» e nas palavras-chave
TOC_DEVE = {"pt": ["Ao lado (v385)", "faz agora (v384)", "GPU e como"], "en": ["Beside (v385)", "does now (v384)", "GPU and how"]}
NAO_DEVE = {"pt": ["α²", "α^2", "alpha^2", "QG confirmada", "gravidade quântica confirmada", "a natureza decidiu a formulação"], "en": ["α²", "α^2", "alpha^2", "QG confirmed", "quantum gravity confirmed", "nature decided the formulation"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
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


def secao(txt, lang):
    a = txt.find("Ao lado (v386)" if lang == "pt" else "Beside (v386)"); b = txt.find("Ao lado (v385)" if lang == "pt" else "Beside (v385)")
    return txt[a:b] if (a >= 0 and b > a) else (txt[a:a + 12000] if a >= 0 else "")


for lang in ("pt", "en"):
    t0 = time.time()
    tex, txt, rcs, log = compilar(c, "dry_v386_%s" % lang, lang)
    sec = secao(txt, lang); flat = txt.replace("\n", "")
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v386_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat and w not in tex], "nan": len(re.findall(r"(?<![A-Za-z])nan(?![A-Za-z])", txt)),
                           "proibidas_na_secao": [w for w in NAO_DEVE[lang] if w in sec] + (["GUARDA:" + m.group(0) for m in GUARDA.finditer(sec)]),
                           "secao_chars": len(sec), "v386_antes_da_v385": (txt.find("Ao lado (v386)" if lang == "pt" else "Beside (v386)") < txt.find("Ao lado (v385)" if lang == "pt" else "Beside (v385)")),
                           "overfull": log.count("Overfull \\hbox"), "s": round(time.time() - t0, 1)}
    _toc_p = os.path.join(DRY, "dry_v386_%s.toc" % lang); _toc = open(_toc_p, encoding="utf-8", errors="replace").read() if os.path.exists(_toc_p) else ""
    _ls = txt.splitlines(); _lin = lambda frag: next((l_ for l_ in _ls if frag in l_), "")
    rep["artigo"][lang]["W10"] = {"toc_contentsline": _toc.count("\\contentsline"), "toc_GPU": _toc.count("GPU"), "toc_faltam": [w for w in TOC_DEVE[lang] if w not in _toc.replace("\n", "")],
                                  "gpu_na_apresentacao_linha2": "GPU" in (_ls[1] if len(_ls) > 1 else ""), "gpu_no_metodo": "GPU" in _lin("O método" if lang == "pt" else "The method"),
                                  "gpu_nas_palavras_chave": "GPU" in _lin("Palavras-chave" if lang == "pt" else "Keywords")}
    rep["artigo"][lang]["trecho"] = sec[:4000]
    print("artigo", lang, json.dumps({k: v for k, v in rep["artigo"][lang].items() if k != "trecho"}, ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["nan"] or v["proibidas_na_secao"] or not v["v386_antes_da_v385"] or v["secao_chars"] < 3000
       or v["W10"]["toc_faltam"] or not v["W10"]["gpu_na_apresentacao_linha2"] or not v["W10"]["gpu_no_metodo"] or not v["W10"]["gpu_nas_palavras_chave"]]
VARS = {"nao_selou_v1_nao_lido_pilar_calculado": ({"the_verb_v386": _a2, "ramo_b_preregistration_v386": _r1, "ledger_errata_v386": _e1, "quantum_pillar_reuse_v386": _q3, "quantum_pillar_v384": QP, "quantum_pillar_reproducibility_v385": core0["quantum_pillar_reproducibility_v385"]},
                                                   {"pt": ["Nesta rodada a pedra não selou", "Nesta rodada o V1 NÃO foi lido por hash", "o reaproveitamento foi recusado", "é o mesmo da v385"],
                                                    "en": ["In this run the stone did not seal", "In this run V1 was NOT read by hash", "reuse was refused", "is the same as v385"]}),
        "pilar_nem_um_nem_outro": ({"quantum_pillar_reuse_v386": _q4}, {"pt": ["nem reaproveitado nem calculado nesta rodada"], "en": ["neither reused nor computed in this run"]})}
rep["variantes"] = {}
for vn, (upd, deve) in VARS.items():
    cv = dict(copy.deepcopy(c), **copy.deepcopy(upd))
    for lang in ("pt", "en"):
        _tex, _txt, _rcs, _log = compilar(cv, "dry_v386_%s_%s" % (vn, lang), lang, duas=False)
        _flat = _txt.replace("\n", "")
        rep["variantes"]["%s_%s" % (vn, lang)] = {"pdflatex_rc": _rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v386_%s_%s.pdf" % (vn, lang))), "faltam": [w for w in deve[lang] if w not in _flat]}
print("variantes:", json.dumps(rep["variantes"], ensure_ascii=False))
mau_var = [k for k, v in rep["variantes"].items() if v["pdflatex_rc"] != [0] or not v["pdf_ok"] or v["faltam"]]

# (6) o markdown canonico e o manifesto
um.OUT = DRY
um.emit_canonical_md(c, verdict)
md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v386**" in md, "errata_R6": "Errata ao lado (v386, 05/10/2026, o operador)" in md and "REABERTO POR PRÉ-REGISTRO" in md, "errata_v385_fica": "Errata ao lado (v385, 05/10/2026, o operador)" in md,
                   "verbo_no_md": "the_verb_v386" in md, "ramo_b_no_md": "ramo_b_preregistration_v386" in md, "errata_no_md": "ledger_errata_v386" in md, "pilar_reuse_no_md": "quantum_pillar_reuse_v386" in md,
                   "todos_os_modulos": "TODOS OS MODULOS COM VEREDITO" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md")
um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c)
rep["manifest"] = {"carimbo": "**Versão v386**" in open(mani, encoding="utf-8").read()}
print("markdown:", rep["markdown"], "| manifesto:", rep["manifest"])
_GUARDA = ['if (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", _v)', 'or re.search(r"(?<!AP)PROVED_BY", _v)', 'or "TGL_PROVED" in _v or "CONSCIOUSNESS_PROVED" in _v):']
assert all(src.count(g) == 1 for g in _GUARDA), "a guarda do rito mudou no candidato -- atualizar o ensaio"
_proib = [k for k, _m in c.items() if isinstance(_m, dict) and (GUARDA.search(str(_m.get("verdict") or "")) or "CONSCIOUSNESS_PROVED" in str(_m.get("verdict") or ""))]
_sel_read = re.search(r'"the_verb_reading_v386": "([A-Za-z0-9_]+)"', src)   # a leitura cita o nome da pedra (TheVerbSelectsTheAction), com minusculas
rep["guarda_do_rito_vereditos_proibidos"] = _proib
rep["leitura_do_selo_v386_limpa"] = bool(_sel_read) and not GUARDA.search(_sel_read.group(1))
# os baldes da custodia de sentido com o core sintetico: nenhum registro v386 em all_verified False
rep["nao_selados_v386"] = [k for k in NOVAS if (c.get(k) or {}).get("all_verified") is not True]
# (7) as citacoes do operador, VERBATIM contra o transcrito (estrito)
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v386.py"), DRY], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_do_operador"] = {"rc": _cc.returncode, "ultimas": (_cc.stdout.strip().splitlines() or [""])[-2:]}
print("citacoes:", rep["citacoes_do_operador"])
ok = (mf_ok and all(v_ is True for v_ in U.values()) and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"]["carimbo"] and not _proib
      and rep["leitura_do_selo_v386_limpa"] and not rep["nao_selados_v386"] and rep["citacoes_do_operador"]["rc"] == 0)
rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if v is not True}, "artigo": mau, "variantes": mau_var, "md": rep["markdown"], "mani": rep["manifest"],
                                                                     "proib": _proib, "selo": rep["leitura_do_selo_v386_limpa"], "nao_selados": rep["nao_selados_v386"], "citacoes_rc": rep["citacoes_do_operador"]["rc"]}, ensure_ascii=False))
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"]))
sys.exit(0 if ok else 1)

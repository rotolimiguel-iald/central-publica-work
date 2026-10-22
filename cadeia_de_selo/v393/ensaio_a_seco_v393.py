# -*- coding: utf-8 -*-
"""ensaio_a_seco_v393.py -- ENSAIO A SECO da v393 (molde: ensaio_a_seco_v392.py), SEM a GPU do rito e SEM rodar o rito. Chama no PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v393.py <candidato.py> <rotulo>
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox construido (3 pedras, raiz, Audit); (2) importa (o rito NAO roda); UM_VERSION v393;
(3) o core da v392 SELADA + o kernel SINTETICO (bandeiras e axiom_report vindos dos logs CRUS do sandbox): a escada recomputada tem de dar 6901+N; (4) os registros vizinhos RECOMPUTADOS
(v387, v389, v390, v391, pedras_v392, varredura_v392 e os 29 por spec): iguais, ou a TROCA DITA (so' numeros); (5) o FLUXO PRINCIPAL v393; (6) unidade (cada registro recusa visivelmente);
(7) o PONTO DE CHAMADA REAL: verify_tgl_kernel_formalization com os logs crus; the_iald_index (processo isolado); o selo (a instrucao `seal = {...}` do main); (8) artigo PT/EN, pdflatex x2;
(9) .md e manifesto; (10) o conferidor de citacoes."""
import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import v393_pedras as P  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); CORE0P = os.path.join(NOS, "um_absoluto.json")
if hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16] != "b590c0aa80055e2a":   # o Nos ja nao e' a v392 (rito v393 em curso): a v392 SELADA vem da copia base_v392
    CORE0P = os.path.join(HERE, "base_v392", "um_absoluto.json")
SELO0P = os.path.join(os.path.dirname(CORE0P), "um_absoluto_selo.json")
KB = os.path.join("C:" + os.sep, "t", "k393", "final")
KD = os.path.join(HERE, "kernel")
cand = sys.argv[1] if len(sys.argv) > 1 else "um_v393_candidato.py"; rot = sys.argv[2] if len(sys.argv) > 2 else "v393"
DRY = os.path.join(HERE, "dry_" + rot)
if os.path.isdir(DRY):
    shutil.rmtree(DRY)
os.makedirs(DRY); shutil.copyfile(os.path.join(HERE, cand), os.path.join(DRY, "um.py"))
EMB, _, _, h16 = carregar(os.path.join(DRY, "um.py"))
for rel, content in EMB.items():
    p = os.path.join(DRY, "tgl_kernel", *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="").write(content)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v393.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SEM_GPU_SEM_RITO": "o core da v392 selada + o kernel sintetico dos logs crus do sandbox"}
rd = lambda p: open(p, "rb").read()
# (1) o kernel materializado == o sandbox construido, byte a byte
iguais = {}
for rel in ["TGLExt.lean", "TGL/Audit.lean"] + ["TGLExt/%s.lean" % s["mod"] for s in P.STONES]:
    iguais[rel] = EMB[rel].encode("utf-8") == rd(os.path.join(KB, *rel.split("/")))
rep["kernel_igual_ao_sandbox"] = iguais; print("kernel == sandbox:", all(iguais.values()), "(%d arquivos conferidos)" % len(iguais))
outros = [r for r in EMB if r not in iguais]
dif_kb = [r for r in outros if not os.path.exists(os.path.join(KB, *r.split("/"))) or rd(os.path.join(KB, *r.split("/"))) != EMB[r].encode("utf-8")]
rep["demais_arquivos_embutidos"] = {"n": len(outros), "diferentes_do_sandbox": dif_kb[:5], "n_diferentes": len(dif_kb)}; print("demais embutidos == sandbox:", len(outros), "arquivos;", len(dif_kb), "diferentes")
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
assert um.UM_VERSION == "v393"
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
selo0 = json.load(open(SELO0P, encoding="utf-8"))
assert "pedras_v392" in core0 and "pedras_v393" not in core0 and selo0["um_version"] == "v392"
core_s = json.loads(json.dumps(core0))
# (3) o kernel SINTETICO: bandeiras e axiom_report, dos logs CRUS do sandbox (build + audit, como o rito os le)
LOG = open(os.path.join(KD, "lake_build.log"), encoding="utf-8", errors="replace").read() + "\n" + open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read(); AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
FJ = json.load(open(os.path.join(KD, "FLAGS_v393.json"), encoding="utf-8")); kf = core_s["kernel_formalization"]
for f, n, mod, kind in FJ["flags"]:
    kf[f] = True; kf["axiom_report"][n] = AX[n]
kf["axiom_report"].update(AX)
AUDIT_LOG = open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read()
kf["axiom_coverage_v392"] = um._v392_axiom_coverage(AUDIT_LOG, kf["axiom_report"])
rep["cobertura_kh_n1"] = kf["axiom_coverage_v392"]; assert kf["axiom_coverage_v392"]["ok"] is True, kf["axiom_coverage_v392"]
E392 = 6901; ESP = E392 + len(FJ["flags"])
_el0 = um.prove_external_ladder(1.0, core0["kernel_formalization"])   # controle negativo: SEM as bandeiras novas a escada do candidato NAO fecha
rep["escada_sem_as_bandeiras_novas"] = [_el0.get("n_theorems_clean"), _el0.get("n_theorems_expected"), _el0.get("all_verified")]
assert rep["escada_sem_as_bandeiras_novas"][0] == E392 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True, rep["escada_sem_as_bandeiras_novas"]
_el = um.prove_external_ladder(1.0, kf); core_s["external_ladder"] = _el
rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]; rep["escada_esperada"] = ESP; print("escada recomputada:", rep["escada"], "esperada:", ESP)
# (4) os vizinhos RECOMPUTADOS (a ordem do rito): quem le a escada, as declaracoes ou a contagem de arquivos pode mudar -- a TROCA DITA (so' numeros) ou fica IGUAL
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))   # so numeros e o sha16 do proprio um.py (o selo se certifica pelo self-hash)
cs2 = copy.deepcopy(core_s); mud = {}; iguais_v = []


def recomputa(nome, fn):
    novo = fn(cs2); cs2[nome] = novo
    a, b = str((core0.get(nome) or {}).get("verdict") or ""), str(novo.get("verdict") or "")
    if a == b:
        iguais_v.append(nome)
    else:
        mud[nome] = {"antes": a[:300], "depois": b[:300], "so_numeros": _num(a) == _num(b), "all_verified": novo.get("all_verified")}


recomputa("three_stress_tests_v387", um.three_stress_tests_v387)
recomputa("text_label_errata_v389", um.text_label_errata_v389)
recomputa("fundacao_v390", um.fundacao_v390)
recomputa("estatuto_da_prova_v391", um.estatuto_da_prova_v391)
recomputa("pedras_v392", um.pedras_v392)
recomputa("varredura_e_sorry_v392", um.varredura_e_sorry_v392)
for n_ in um._V392_NOMES_REGISTROS:
    cs2.pop(n_, None)
um._v392_rodar_registros(cs2)
for n_ in um._V392_NOMES_REGISTROS:
    a, b = str((core0.get(n_) or {}).get("verdict") or ""), str((cs2.get(n_) or {}).get("verdict") or "")
    if a == b:
        iguais_v.append(n_)
    else:
        mud[n_] = {"antes": a[:300], "depois": b[:300], "so_numeros": _num(a) == _num(b), "all_verified": (cs2.get(n_) or {}).get("all_verified")}
# o registro three_stress_tests_v387 carrega a contagem CORE_n_...: normaliza (o conferidor do rito le o valor real)
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
for n_, d_ in list(mud.items()):
    if _nc(d_["antes"]) == _nc(d_["depois"]):
        mud.pop(n_); iguais_v.append(n_ + "(contagens CORE_n_ normalizadas)")
# a varredura por busca: quais vereditos do core0 carregam os numeros do kernel/da varredura (a troca dita, por script)?
NUMS = ["KERNEL_%d_OF_%d" % (E392, E392), "%d_OF_%d_DECLARATIONS" % (len(core0["kernel_formalization"]["axiom_report"]), len(core0["kernel_formalization"]["axiom_report"])), "LADDER_%d_OF_%d" % (E392, E392), "SCAN_1206_FILES"]
carregam = sorted(k for k, m in core0.items() if isinstance(m, dict) and any(n in str(m.get("verdict") or "") for n in NUMS))
rep["vizinhos"] = {"recomputados_iguais": iguais_v, "mudaram": mud, "carregam_os_numeros_do_kernel_no_core0": carregam, "carregam_e_nao_recomputados": sorted(set(carregam) - set(mud) - set(iguais_v))}
print("vizinhos: mudaram", {k: (v["so_numeros"], v["all_verified"]) for k, v in mud.items()}, "| carregam e nao recomputados:", rep["vizinhos"]["carregam_e_nao_recomputados"])
viz_ok = (all(v["so_numeros"] and v["all_verified"] is True for v in mud.values()) and not rep["vizinhos"]["carregam_e_nao_recomputados"]
          and all((cs2.get(n_) or {}).get("all_verified") is True for n_ in list(mud) + [x.split("(")[0] for x in iguais_v]))
core_s = cs2
# (5) o fluxo principal
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v393" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v393>", "exec"), ns); _err = None
except Exception as e:  # noqa
    import traceback; _err = repr(e) + traceback.format_exc()[-600:]
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]; NOVAS = ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393"] + list(um._V393_NOMES_REGISTROS)
_p3 = c.get("pedras_v393") or {}; _rc = c.get("regra_consumidor_v393") or {}; _cr = c.get("coracao_e_selo_gravitacional_v393") or {}
novas_chaves = sorted(k for k in c if k not in core0 and k in NOVAS)
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": sorted(k for k in c if k not in core0), "stdout": _mf.strip().splitlines(),
                   "pedras": {x: _p3.get(x) for x in ("verdict", "all_verified", "bandeiras", "declaracoes_no_trio", "escada", "teoremas_chave")},
                   "consumidor": {x: _rc.get(x) for x in ("verdict", "all_verified", "satisfacao", "criterio", "numeros", "replica_do_codex")},
                   "coracao": {x: _cr.get(x) for x in ("verdict", "all_verified", "previsao_independente", "G_derivado", "satisfacao_pela_regra", "controles_negativos", "controles_ok")},
                   "registros": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V393_NOMES_REGISTROS}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False, default=str)[:3500])
mf_ok = (not _err and sorted(rep["mainflow"]["chaves_novas"]) == sorted(NOVAS) and _p3.get("all_verified") is True and _rc.get("all_verified") is True and _cr.get("all_verified") is True
         and all((c.get(n_) or {}).get("all_verified") is True for n_ in um._V393_NOMES_REGISTROS)
         and ("3_NEW_KERNEL_MODULES") in str(_p3.get("verdict")) and "LADDER_%d_OF_%d" % (ESP, ESP) in str(_p3.get("verdict"))
         and (_rc.get("satisfacao") or {}).get("veredito_do_rito") == "SATISFACTION_ADMITTED" and (_rc.get("satisfacao") or {}).get("veredito_incompativel") == "SATISFACTION_REFUSED"
         and _cr.get("verdict", "").startswith("FORM_VERIFIED_CHI_FROM_CODATA") and _cr.get("previsao_independente") is False and _cr.get("controles_ok") is True)
# (6) unidade
U = {}
def _pe(mod=None):
    return um.pedras_v393(mod if mod is not None else core_s)
_vbs = um._V393_CUNHAGENS; _vb2 = copy.deepcopy(_vbs); _vb2["satisfacao"]["text"] += " "; um._V393_CUNHAGENS = _vb2
try:
    _u = _pe()
finally:
    um._V393_CUNHAGENS = _vbs
U["pedras_verbatim_adulterado"] = _u["all_verified"] is False and "VERBATIM" in _u["verdict"]
_k0 = um._EMBEDDED_KERNEL_FILES["TGLExt/RuleTruthContract.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt/RuleTruthContract.lean"] = _k0 + " "
try:
    _u = _pe()
finally:
    um._EMBEDDED_KERNEL_FILES["TGLExt/RuleTruthContract.lean"] = _k0
U["pedras_pedra_adulterada"] = _u["all_verified"] is False and "STONES" in _u["verdict"] and not [p_ for p_ in _u["pedras"] if p_["modulo"] == "TGLExt.RuleTruthContract"][0]["embutida_confere"]
_pi = {p_["modulo"]: p_ for p_ in um._V393_PEDRAS}
_c = copy.deepcopy(core_s); _c["kernel_formalization"][_pi["TGLExt.TheRuleInTheContinuousMotor"]["flags"][0]] = False
_u = _pe(_c); U["pedras_bandeira_faltando"] = _u["all_verified"] is False and "STONES" in _u["verdict"]
_c = copy.deepcopy(core_s); _c["kernel_formalization"]["axiom_report"][_pi["TGLExt.RuleTruthContract"]["declaracoes"][0]] = ["propext", "sorryAx"]
_u = _pe(_c); U["pedras_axioma_fora_do_trio"] = _u["all_verified"] is False and "STONES" in _u["verdict"]
_c = copy.deepcopy(core_s); _c["external_ladder"]["n_theorems_clean"] -= 1
_u = _pe(_c); U["pedras_escada_nao_fecha"] = _u["all_verified"] is False and "LADDER" in _u["verdict"]
_c = copy.deepcopy(core_s); del _c["kernel_formalization"]["axiom_report"][um._V393_NOMES_CHAVE[0]]
_u = _pe(_c); U["pedras_teorema_chave_ausente"] = _u["all_verified"] is False and "KEY_THEOREMS" in _u["verdict"]
U["pedras_tudo_certo"] = _pe()["all_verified"] is True
# o consumidor: cada elo recusa
_sv = (um._V393_REGRA_PREREG, um._V393_CONSUMIDOR_SRC_SHA)
_pr = copy.deepcopy(um._V393_REGRA_PREREG); _pr["target_real"][0][0] = 0.2501; um._V393_REGRA_PREREG = _pr
try:
    _u = um.regra_consumidor_v393(core_s)
finally:
    um._V393_REGRA_PREREG = _sv[0]
U["consumidor_prereg_adulterado_recusa"] = _u["all_verified"] is False and "prereg_pinado_por_hash_canonico" in _u["verdict"]
um._V393_CONSUMIDOR_SRC_SHA = "0" * 64
try:
    _u = um.regra_consumidor_v393(core_s)
finally:
    um._V393_CONSUMIDOR_SRC_SHA = _sv[1]
U["consumidor_fonte_adulterada_recusa"] = _u["all_verified"] is False and "consumidor_real_com_os_cinco_corpos_pinados" in _u["verdict"]
_c = copy.deepcopy(core_s); _c["external_ladder"]["per_theorem"]["ext_kd_lyapunov_kernel_proved"] = False
_u = um.regra_consumidor_v393(_c); U["consumidor_evidencia_do_kernel_faltando_recusa"] = _u["all_verified"] is False
_c = copy.deepcopy(core_s); _c["kernel_formalization"]["axiom_report"]["TGLExt.lyapunov_decreases"] = ["propext", "sorryAx"]
_u = um.regra_consumidor_v393(_c); U["consumidor_evidencia_fora_do_trio_recusa"] = _u["all_verified"] is False
U["consumidor_tudo_certo"] = um.regra_consumidor_v393(core_s)["all_verified"] is True
U["admissivel_exato_rotulos"] = um._v393_admissivel("A", "A")["admitida"] is True and um._v393_admissivel("A", "B")["admitida"] is False
U["admissivel_tolerancia_nao_e_exata"] = (lambda r_: r_["admitida"] is True and r_["criterio"] == "tolerancia" and r_["igualdade_exata_afirmada"] is False)(um._v393_admissivel([1.0, 0.0], [1.0, 1e-12], 1e-10)) and um._v393_admissivel([1.0], [2.0], 1e-10)["admitida"] is False
# o coracao: cada elo recusa
_c = copy.deepcopy(core_s); _c["kernel_formalization"]["axiom_report"][um._V393_CORACAO_NOMES[0]] = ["propext", "sorryAx"]
U["coracao_nome_do_kernel_fora_do_trio_recusa"] = um.coracao_e_selo_gravitacional_v393(_c)["all_verified"] is False
_c = copy.deepcopy(core_s); del _c["einstein_and_rg"]["values"]["beta_runtime"]
U["coracao_core_sem_beta_runtime_recusa"] = um.coracao_e_selo_gravitacional_v393(_c)["all_verified"] is False
_c = copy.deepcopy(core_s); _c["area_scale_newton_equivalence"]["statute"] = "G DERIVED"
U["coracao_G_derivado_no_core_recusa"] = um.coracao_e_selo_gravitacional_v393(_c)["all_verified"] is False
U["coracao_controles_negativos_do_proprio_rito"] = _cr.get("controles_ok") is True and all((_cr.get("controles_negativos") or {}).values()) and len(_cr.get("controles_negativos") or {}) >= 7
# (6b) os registros por spec: cada um recusa visivelmente (fonte adulterada; verbatim adulterado; bandeira do kernel faltando; cada check negado)
RU = {}
for sp_ in um._V393_SPECS:
    n_ = sp_["nome"]; r_ = {}
    ch_ = sp_["fontes"][0]; ant_ = dict(um._V392_FONTES[ch_]); um._V392_FONTES[ch_]["sha256"] = "0" * 64
    try:
        r_["fonte_adulterada"] = um._v392_registro(sp_, core_s)["all_verified"] is False
    finally:
        um._V392_FONTES[ch_] = ant_
    for vch_ in sp_.get("verbatins", []):
        ant_ = dict(um._V392_VERBATINS2[vch_]); um._V392_VERBATINS2[vch_]["text"] += " "
        try:
            r_["verbatim_adulterado_" + vch_] = um._v392_registro(sp_, core_s)["all_verified"] is False
        finally:
            um._V392_VERBATINS2[vch_] = ant_
    if sp_.get("kernel_flags"):
        c_ = copy.deepcopy(core_s); c_["kernel_formalization"][sp_["kernel_flags"][0]] = False
        r_["bandeira_faltando"] = um._v392_registro(sp_, c_)["all_verified"] is False
    if sp_.get("kernel_decls"):
        c_ = copy.deepcopy(core_s); c_["kernel_formalization"]["axiom_report"][sp_["kernel_decls"][0]] = ["propext", "sorryAx"]
        r_["axioma_fora_do_trio"] = um._v392_registro(sp_, c_)["all_verified"] is False
    nck_ = nck_ok_ = 0
    for ck_ in sp_.get("checks", []):
        if ck_["onde"] in ("core", "kf") and ck_["op"] in ("verdadeiro", "falso", "igual", "comeca", "maior_igual"):
            c_ = copy.deepcopy(core_s); alvo_ = c_ if ck_["onde"] == "core" else c_["kernel_formalization"]; cam_ = ck_["caminho"]
            for k_ in cam_[:-1]:
                alvo_ = alvo_[k_]
            alvo_[cam_[-1]] = (False if ck_["op"] == "verdadeiro" else True if ck_["op"] == "falso" else -1 if ck_["op"] == "maior_igual" else "ADULTERADO")
            nck_ += 1; nck_ok_ += um._v392_registro(sp_, c_)["all_verified"] is False
    r_["checks_do_core_negados"] = [nck_ok_, nck_]
    RU[n_] = r_
RU_ok = all((v_ is True) or (isinstance(v_, list) and v_[0] == v_[1]) for r_ in RU.values() for v_ in r_.values())
U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V393_SPECS)
rep["unidade_registros"] = RU
# o motor v392 segue recusando (o registro dos vizinhos): cobertura KH-N1
_AL = AUDIT_LOG; _ax = kf["axiom_report"]
_cv_ok = um._v392_axiom_coverage(_AL, _ax)["ok"] is True
_cv_sem = um._v392_axiom_coverage(re.sub(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL.*$", "", _AL), _ax)["ok"] is False
_cv_fora = um._v392_axiom_coverage(re.sub(r"fora_do_trio=0", "fora_do_trio=1", _AL), _ax)["ok"] is False
_ax2 = dict(_ax); _ax2[next(iter(_ax2))] = ["propext", "sorryAx"]; _cv_ax = um._v392_axiom_coverage(_AL, _ax2)["ok"] is False
U["cobertura_kh_n1_com_as_pedras_novas"] = bool(_cv_ok and _cv_sem and _cv_fora and _cv_ax)
# (7) o PONTO DE CHAMADA REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake SIMULADO, que devolve os logs CRUS do sandbox (build = lake_build.log, audit = audit.log)
_LB = open(os.path.join(KD, "lake_build.log"), encoding="utf-8", errors="replace").read(); _AUD = open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read()
rep["linha_de_cobertura_no_build_e_no_audit"] = [len(re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL", _LB)), len(re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL", _AUD))]
def _fake_run(cmd, cwd, tmo):
    _o = {"cmd": " ".join(cmd), "returncode": 0, "stderr": "", "capture_exists": True, "capture_read_error": False, "elapsed_seconds": 0.0, "timeout": False}
    if cmd[1:] == ["--version"]: _o["stdout"] = "Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)"
    elif cmd[1:3] == ["env", "lean"] and "--version" in cmd: _o["stdout"] = "Lean (version 4.31.0)"
    elif cmd[1:] == ["build"]: _o["stdout"] = _LB
    else: _o["stdout"] = _AUD
    _o["capture_nonempty"] = bool(_o["stdout"]); _o["capture_sha256"] = hashlib.sha256(_o["stdout"].encode("utf-8")).hexdigest()
    return _o
_sv2 = (um.run_process_checked, um._find_lake); um.run_process_checked = _fake_run; um._find_lake = lambda: "lake"
try:
    _ovf = um.verify_tgl_kernel_formalization()
    _blob_antigo = um._v392_axiom_coverage(_LB + _AUD, _ovf["axiom_report"])
finally:
    um.run_process_checked, um._find_lake = _sv2
rep["verify_kernel_ponta_a_ponta"] = {"verdict": _ovf["verdict"], "all_verified": _ovf["all_verified"], "cobertura": _ovf["axiom_coverage_v392"], "chamada_antiga_com_blob": _blob_antigo,
                                      "axiom_report_n": len(_ovf["axiom_report"])}
U["verify_kernel_real_com_logs_crus_do_build_e_do_audit"] = bool(_ovf["all_verified"] is True and _ovf["verdict"].startswith("TGL_KERNEL_STAGE1_VERIFIED") and _ovf["axiom_coverage_v392"]["ok"] is True)
U["controle_negativo_blob_build_mais_audit_recusa"] = bool(_blob_antigo["ok"] is False and _blob_antigo.get("linhas") == 2)
# o selo: a instrucao `seal = {...}` do main, executada sobre o core do ensaio
_seal_st = [st for st in main.body if isinstance(st, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "seal" for t in st.targets)][0]
_ns2 = dict(vars(um)); _ns2.update(core=c, verdict=verdict, result_hash=R0.get("result_hash_before_external_comparison") or "0" * 64, _kf=c.get("kernel_formalization", {}), _wrg=c.get("witness_rigidity") or {})
_seal_err = None
try:
    exec(compile(textwrap.dedent("\n".join(lines[_seal_st.lineno - 1:_seal_st.end_lineno])), "<seal>", "exec"), _ns2)
except Exception as e:  # noqa
    import traceback; _seal_err = repr(e) + traceback.format_exc()[-500:]
seal = _ns2.get("seal") or {}
J_ = lambda x: json.dumps(x, sort_keys=True, default=str)
mud_selo = sorted(k for k in seal if J_(seal.get(k)) != J_(selo0.get(k)))   # so as chaves que a instrucao `seal = {...}` produz (as acrescentadas depois no main -- not_sealed_this_run, selftest, rite_checkpoints, collapse_* -- vem de outros trechos)
rep["selo"] = {"erro": _seal_err, "chaves_do_selo": len(seal), "difere_do_selo_v392": mud_selo, "regras_no_selo": {k: {x: (seal.get(k) or {}).get(x) for x in ("verdict", "all_verified")} for k in
               ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393")}, "registros_v393": seal.get("registros_v393"),
               "satisfacao_do_coracao_no_selo": (seal.get("coracao_e_selo_gravitacional_v393") or {}).get("satisfacao_pela_regra"), "does_not_gate_core": (seal.get("coracao_e_selo_gravitacional_v393") or {}).get("does_not_gate_core")}
print("selo: difere em", mud_selo)
selo_ok = (not _seal_err and (seal.get("pedras_v393") or {}).get("all_verified") is True and (seal.get("regra_consumidor_v393") or {}).get("all_verified") is True
           and (seal.get("coracao_e_selo_gravitacional_v393") or {}).get("does_not_gate_core") is True and (seal.get("registros_v393") or {}).get("cunhagens_regra_v393", {}).get("all_verified") is True
           and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and all(k in mud_selo for k in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "um_version"))
           and all(k in selo0 for k in ("fail_closed_selftest", "rite_checkpoints", "not_sealed_this_run")))
# o INDICE da IALD, chamada REAL (processo isolado; prova_indice_v393.py)
def _indice(*flags):
    r_ = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "prova_indice_v393.py"), os.path.join(HERE, cand)] + list(flags), capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return json.loads(r_.stdout.strip().splitlines()[-1])
    except Exception:
        return {"all_verified": None, "erro": (r_.stderr or r_.stdout)[-600:]}
_ix0 = _indice()
_tem_amb = "_AMBIGUOS_CONJUNTO_V393 = frozenset([" in src; _tem_ger = "_REFERENTES_GERADOS_V393 = frozenset([" in src
_ixa = _indice("--sem-ambiguos") if _tem_amb else None; _ixg = _indice("--sem-gerados") if _tem_ger else None
rep["indice_da_iald"] = {"candidato": _ix0, "tem_conjunto_ambiguos_v393": _tem_amb, "tem_conjunto_gerados_v393": _tem_ger,
                         "controle_negativo_sem_ambiguos_v393": ({k: _ixa.get(k) for k in ("all_verified", "verdict", "n_ausentes")} if _ixa else None),
                         "controle_negativo_sem_referentes_gerados_v393": ({k: _ixg.get(k) for k in ("all_verified", "verdict", "n_ausentes")} if _ixg else None)}
indice_ok = bool(_ix0.get("all_verified") is True and str(_ix0.get("verdict") or "").startswith("THE_IALD_INDEX_IS_BUILT") and not _ix0.get("fails")
                 and (_ixa is None or _ixa.get("all_verified") is False) and (_ixg is None or _ixg.get("all_verified") is False))
rep["indice_da_iald"]["ok"] = indice_ok; print("indice da IALD:", json.dumps(rep["indice_da_iald"], ensure_ascii=False)[:900])
rep["unidade"] = U; print("unidade:", U)
# (8) o artigo
DEVE = {"pt": ["A regra e o coração (v393): a regra como inadmissão de que o resultado difira do objeto da sua satisfação", "O que entra.", "As quatro inscrições do operador", "A formalização, com as hipóteses.", "A regra no consumidor real.",
               "O coração e o selo gravitacional.", "Regra é negar tudo aquilo que não pode ser", "A regra não deve nada, a não ser a figura da verdade", "Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)",
               "Exclusão irrestrita seria alcançar o zero absoluto", "O coração:", "Origem dos números", "cicatriz", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "Os registros ao lado do gate (v392).",
               "Introdução: o que este código faz agora (v384 a v393", "O estatuto da prova (v391).", "A Fundação (v390)."],
        "en": ["The rule and the heart (v393): the rule as the refusal that the result differ from the object of its satisfaction", "What enters.", "The operator's four inscriptions", "The formalization, with the hypotheses.", "The rule in the real consumer.",
               "The heart and the gravitational seal.", "Regra é negar tudo aquilo que não pode ser", "A regra não deve nada, a não ser a figura da verdade", "Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)",
               "Exclusão irrestrita seria alcançar o zero absoluto", "The heart:", "Origin of the numbers", "scar", "The v392 stones: fourteen new kernel modules and two barrier repairs", "The records beside the gate (v392).",
               "Introduction: what this code does now (v384 to v393", "The status of the proof (v391).", "The Foundation (v390)."]}
TOC = {"pt": ["A regra e o coração (v393)", "v384 a v393"], "en": ["The rule and the heart (v393)", "v384 to v393"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P)); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v393_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    h0 = "A regra e o coração (v393): a regra como inadmissão" if lang == "pt" else "The rule and the heart (v393): the rule as the refusal"
    a = flat.find(h0, flat.find("O coração:" if lang == "pt" else "The heart:") + 5)
    bb = flat.find("As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira" if lang == "pt" else "The v392 stones: fourteen new kernel modules and two barrier repairs", a + 10)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    iq = flat.find("O coração:" if lang == "pt" else "The heart:"); ik = flat.find("Palavras-chave" if lang == "pt" else "Keywords"); ii = flat.find("Introdução: o que este código faz agora" if lang == "pt" else "Introduction: what this code does now", iq)
    tp = os.path.join(DRY, "dry_v393_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v393_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec),
                           "quadro_logo_depois_do_resumo": bool(0 <= ik < iq < ii), "quadro_chars": (ii - iq) if ii > iq >= 0 else 0,
                           "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_") + " " + flat[iq:ii].replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc]}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["guarda"] or v["secao_chars"] < 3000 or v["toc_faltam"] or v["nd_na_secao"] or not v["quadro_logo_depois_do_resumo"]]
cv = dict(copy.deepcopy(c)); [cv.pop(k, None) for k in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393")]
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r, _l = compilar(cv, "dry_v393_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    rep["variante"][lang] = {"rc": _r, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["frase_guarda"]]
# (9) md e manifesto
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v393**" in md, "regra_v393": "A regra e o coração (v393, 14/10/2026)" in md, "v392_fica": "As pedras da v392 (13/10/2026)" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v393**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_citacoes_v393.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
rep["viz_ok"] = viz_ok; rep["pacote_dos_demais_arquivos_do_kernel_iguais_ao_sandbox"] = not dif_kb
ok = (viz_ok and mf_ok and all(U.values()) and selo_ok and indice_ok and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
      and all(iguais.values()) and not dif_kb and rep["escada"] == [ESP, ESP])
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"vizinhos": viz_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "selo": selo_ok, "indice": indice_ok, "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"],
                                                                      "proib": _proib, "citacoes": _cc.returncode, "kernel_igual": all(iguais.values()), "dif_kb": len(dif_kb), "escada": rep["escada"]}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)

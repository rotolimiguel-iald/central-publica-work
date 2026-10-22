# -*- coding: utf-8 -*-
"""ensaio_a_seco_v392.py -- ENSAIO A SECO da v392 (molde: ensaio_a_seco_v391.py + a parte de kernel da v390), SEM a GPU do rito e SEM rodar o rito.
uso: python -I -B -X utf8 ensaio_a_seco_v392.py <candidato.py> <rotulo>
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox construido (14 pedras, raiz, Audit); (2) importa (o rito NAO roda); UM_VERSION v392;
(3) o core da v391 selada + o kernel SINTETICO (bandeiras e axiom_report das pedras vindos do build do sandbox): a escada recomputada tem de dar 6163+N; (4) registros vizinhos
(v389, v390) recomputados: IGUAIS; o v391 recomputado: a troca DITA; (5) o FLUXO PRINCIPAL v392; (6) unidade (cada registro recusa visivelmente); (7) a varredura recursiva e o detector
de sorry, com controles; (8) artigo PT/EN, pdflatex x2, marcas, sumario, variante sem o registro; (9) .md e manifesto; (10) o conferidor de citacoes."""
import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import v392_pedras as P  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); CORE0P = os.path.join(NOS, "um_absoluto.json")
if hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16] != "8e7b9927ceae64b8":   # o Nos ja nao e' a v391 (rito v392 em curso): o core da v391 SELADA vem da copia feita antes do rito
    CORE0P = os.path.join(HERE, "base_v391", "um_absoluto.json")
KB = os.path.join("C:" + os.sep, "t", "k392", "final")
if not os.path.isdir(KB):   # sandbox apagado: as fontes .lean extraidas do candidato 525ab5fc (kb_stub_v392), pinadas pelo gerador contra os sha das pedras e os ANTES
    KB = os.path.join(HERE, "kb_stub_v392")
KD = os.path.join(HERE, "kernel")
cand = sys.argv[1] if len(sys.argv) > 1 else "um_v392_candidato.py"; rot = sys.argv[2] if len(sys.argv) > 2 else "v392"
DRY = os.path.join(HERE, "dry_" + rot)
if os.path.isdir(DRY):
    shutil.rmtree(DRY)
os.makedirs(DRY); shutil.copyfile(os.path.join(HERE, cand), os.path.join(DRY, "um.py"))
EMB, _, _, h16 = carregar(os.path.join(DRY, "um.py"))
for rel, content in EMB.items():
    p = os.path.join(DRY, "tgl_kernel", *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="").write(content)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v392.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SEM_GPU_SEM_RITO": "o core da v391 selada + o kernel sintetico do build do sandbox"}
# (1) o kernel materializado == o sandbox construido, byte a byte
rd = lambda p: open(p, "rb").read()
iguais = {}
for rel in ["TGLExt.lean", "TGL/Audit.lean"] + ["TGLExt/%s.lean" % s["mod"] for s in P.STONES]:
    iguais[rel] = EMB[rel].encode("utf-8") == rd(os.path.join(KB, *rel.split("/")))
rep["kernel_igual_ao_sandbox"] = iguais; print("kernel == sandbox:", all(iguais.values()), "(%d arquivos conferidos)" % len(iguais))
# o kernel embutido SEM as 14 pedras e SEM raiz/Audit == o do Nos v391, arquivo a arquivo
NK = os.path.join(NOS, "tgl_kernel"); outros = [r for r in EMB if r not in iguais]
dif_nos = [r for r in outros if not os.path.exists(os.path.join(NK, *r.split("/"))) or rd(os.path.join(NK, *r.split("/"))) != EMB[r].encode("utf-8")]
rep["demais_arquivos_embutidos"] = {"n": len(outros), "diferentes_do_Nos": dif_nos[:5], "n_diferentes": len(dif_nos)}; print("demais embutidos == Nos:", len(outros), "arquivos;", len(dif_nos), "diferentes")
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
assert um.UM_VERSION == "v392"
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
assert "estatuto_da_prova_v391" in core0 and "pedras_v392" not in core0
core_s = json.loads(json.dumps(core0))
# (3) o kernel SINTETICO: bandeiras e axiom_report das pedras, do build do sandbox
# os logs CRUS (como o rito os le: build + audit); o build_full.log do pos_build e' normalizado em NFKC (subscritos viram digitos) e perde nomes
LOG = open(os.path.join(KD, "lake_build.log"), encoding="utf-8", errors="replace").read() + "\n" + open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read(); AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
FJ = json.load(open(os.path.join(KD, "FLAGS_v392.json"), encoding="utf-8")); kf = core_s["kernel_formalization"]
for f, n, mod, kind in FJ["flags"]:
    kf[f] = True; kf["axiom_report"][n] = AX[n]
kf["axiom_report"].update(AX)   # KH-N1 (a): o axiom_report efetivo do rito = TODAS as entradas do log do Audit (o run_cmd cobre o fecho inteiro)
AUDIT_LOG = open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read()
kf["axiom_coverage_v392"] = um._v392_axiom_coverage(AUDIT_LOG, kf["axiom_report"])
rep["cobertura_kh_n1"] = kf["axiom_coverage_v392"]; assert kf["axiom_coverage_v392"]["ok"] is True, kf["axiom_coverage_v392"]
_el0 = um.prove_external_ladder(1.0, core0["kernel_formalization"])   # controle negativo: SEM as bandeiras novas a escada do candidato NAO fecha (clean 6163 de 6163+N)
rep["escada_sem_as_bandeiras_novas"] = [_el0.get("n_theorems_clean"), _el0.get("n_theorems_expected"), _el0.get("all_verified")]
assert rep["escada_sem_as_bandeiras_novas"][0] == 6163 and rep["escada_sem_as_bandeiras_novas"][1] == 6163 + len(FJ["flags"]) and _el0.get("all_verified") is not True, rep["escada_sem_as_bandeiras_novas"]
_el = um.prove_external_ladder(1.0, kf); core_s["external_ladder"] = _el
rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]; ESP = 6163 + len(FJ["flags"])
rep["escada_esperada"] = ESP; print("escada recomputada:", rep["escada"], "esperada:", ESP)
# (4) os vizinhos
# o registro conta os vereditos do core NO MOMENTO em que roda (192 na rodada da v391); recomputar sobre o core ja completo da v391 da 200: por isso o prefixo CORE_n_... e' normalizado
# na comparacao (a contagem da v392 fica 192 se nada anterior a esse ponto do fluxo mudar -- o conferidor do rito le o valor real)
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
_t3 = um.three_stress_tests_v387(core_s)   # a 2a TROCA DITA: o registro dos tres testes (v387) le a escada em runtime
_t3v0 = core0["three_stress_tests_v387"]["verdict"]
rep["v387_recomputado"] = {"all_verified": _t3["all_verified"], "so_o_kernel_mudou": _nc(_t3["verdict"]) == _nc(_t3v0).replace("KERNEL_6163_OF_6163", "KERNEL_%d_OF_%d" % (ESP, ESP)), "troca": ["KERNEL_6163_OF_6163", "KERNEL_%d_OF_%d" % (ESP, ESP)]}
core_s["three_stress_tests_v387"] = _t3
_v9 = um.text_label_errata_v389(core_s); _v0 = um.fundacao_v390(core_s)
rep["v389_recomputado"] = {"verdict_igual": _v9["verdict"] == core0["text_label_errata_v389"]["verdict"], "all_verified": _v9["all_verified"]}
rep["v390_recomputado"] = {"verdict_igual": _v0["verdict"] == core0["fundacao_v390"]["verdict"], "all_verified": _v0["all_verified"]}
_v1 = um.estatuto_da_prova_v391(core_s)
rep["v391_recomputado"] = {"all_verified": _v1["all_verified"], "falhas": _v1["falhas"], "verdict_igual": _v1["verdict"] == core0["estatuto_da_prova_v391"]["verdict"],
                           "troca_dita": re.findall(r"KERNEL_\d+_OF_\d+_THEOREMS_\d+_OF_\d+_DECLARATIONS", _v1["verdict"]) + ["antes: " + (re.findall(r"KERNEL_\d+_OF_\d+_THEOREMS_\d+_OF_\d+_DECLARATIONS", core0["estatuto_da_prova_v391"]["verdict"]) or ["?"])[0]]}
viz_ok = (rep["v387_recomputado"]["all_verified"] is True and rep["v387_recomputado"]["so_o_kernel_mudou"] and _v9["all_verified"] is True and rep["v389_recomputado"]["verdict_igual"] and _v0["all_verified"] is True and rep["v390_recomputado"]["verdict_igual"]
          and _v1["all_verified"] is True and not rep["v391_recomputado"]["verdict_igual"])   # o v391 DEVE trocar (a escada e as declaracoes crescem), e continuar selando
print("vizinhos:", json.dumps({"v387": rep["v387_recomputado"], "v389": rep["v389_recomputado"], "v390": rep["v390_recomputado"], "v391": rep["v391_recomputado"]}, ensure_ascii=False)[:900])
core_s["estatuto_da_prova_v391"] = _v1
# (5) o fluxo principal
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v392" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v392>", "exec"), ns); _err = None
except Exception as e:  # noqa
    _err = repr(e)
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]; NOVAS = ["pedras_v392", "varredura_e_sorry_v392"] + list(um._V392_NOMES_REGISTROS); _f = c.get("pedras_v392") or {}; _g = c.get("varredura_e_sorry_v392") or {}
rep["registros_v392"] = {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V392_NOMES_REGISTROS}
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": sorted(k for k in c if k not in core0), "stdout": _mf.strip().splitlines(),
                   "pedras": {x: _f.get(x) for x in ("verdict", "all_verified", "bandeiras", "declaracoes_no_trio", "escada")}, "varredura": {x: _g.get(x) for x in ("verdict", "all_verified", "varredura")}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False)[:2500])
mf_ok = (not _err and len(comeca) == 3 and all((c.get(n_) or {}).get("all_verified") is True for n_ in um._V392_NOMES_REGISTROS) and sorted(rep["mainflow"]["chaves_novas"]) == sorted(NOVAS) and _f.get("all_verified") is True and _g.get("all_verified") is True
         and ("%d_NEW_KERNEL_MODULES" % len(P.STONES)) in str(_f.get("verdict")) and "LADDER_%d_OF_%d" % (ESP, ESP) in str(_f.get("verdict")) and "TRUTH_IS_THE_PROJECTION_OF_THE_POST" in str(_f.get("verdict"))
         and (_f.get("verdade_e_a_projecao_do_posto") or {}).get("no_kernel") is True)
# (6) unidade
U = {}
def _pe(mod=None):
    return um.pedras_v392(mod if mod is not None else core_s)
_vbs = um._V392_VERBATINS; _vb2 = copy.deepcopy(_vbs); _vb2["projecao_do_posto_13out"]["text"] += " "; um._V392_VERBATINS = _vb2
try:
    _u = _pe()
finally:
    um._V392_VERBATINS = _vbs
U["verbatim_adulterado"] = _u["all_verified"] is False and "VERBATIM" in _u["verdict"]
_k0 = um._EMBEDDED_KERNEL_FILES["TGLExt/Posto.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt/Posto.lean"] = _k0 + " "
try:
    _u = _pe()
finally:
    um._EMBEDDED_KERNEL_FILES["TGLExt/Posto.lean"] = _k0
U["pedra_adulterada"] = _u["all_verified"] is False and "STONES" in _u["verdict"] and not [p_ for p_ in _u["pedras"] if p_["modulo"] == "TGLExt.Posto"][0]["embutida_confere"]
_pi = {p_["modulo"]: p_ for p_ in um._V392_PEDRAS}
_c = copy.deepcopy(core_s); _fl = _pi["TGLExt.IALD"]["flags"][0]; _c["kernel_formalization"][_fl] = False
_u = _pe(_c); U["bandeira_faltando"] = _u["all_verified"] is False and "STONES" in _u["verdict"]
_c = copy.deepcopy(core_s); _nm = _pi["TGLExt.Posto"]["declaracoes"][0]; _c["kernel_formalization"]["axiom_report"][_nm] = ["propext", "sorryAx"]
_u = _pe(_c); U["axioma_fora_do_trio"] = _u["all_verified"] is False and "STONES" in _u["verdict"]
_c = copy.deepcopy(core_s); _c["external_ladder"]["n_theorems_clean"] -= 1
_u = _pe(_c); U["escada_nao_fecha"] = _u["all_verified"] is False and "LADDER" in _u["verdict"]
_c = copy.deepcopy(core_s); _c["kernel_formalization"][um._V392_FLAG_PROJECAO] = False
_u = _pe(_c); U["projecao_do_posto_nao_lida"] = _u["all_verified"] is False
U["tudo_certo"] = _pe()["all_verified"] is True
# (6b) os registros por spec: cada um recusa visivelmente (fonte adulterada; verbatim adulterado; bandeira do kernel faltando; cada check negado); o motor sem excecao silenciosa
RU = {}
for sp_ in um._V392_SPECS:
    n_ = sp_["nome"]; r_ = {}
    if sp_.get("fontes"):
        ch_ = sp_["fontes"][0]; ant_ = dict(um._V392_FONTES[ch_]); um._V392_FONTES[ch_]["sha256"] = "0" * 64
        try:
            r_["fonte_adulterada"] = um._v392_registro(sp_, core_s)["all_verified"] is False
        finally:
            um._V392_FONTES[ch_] = ant_
    if sp_.get("verbatins"):
        ch_ = sp_["verbatins"][0]; ant_ = dict(um._V392_VERBATINS2[ch_]); um._V392_VERBATINS2[ch_]["text"] += " "
        try:
            r_["verbatim_adulterado"] = um._v392_registro(sp_, core_s)["all_verified"] is False
        finally:
            um._V392_VERBATINS2[ch_] = ant_
    if sp_.get("kernel_flags"):
        c_ = copy.deepcopy(core_s); c_["kernel_formalization"][sp_["kernel_flags"][0]] = False
        r_["bandeira_faltando"] = um._v392_registro(sp_, c_)["all_verified"] is False
    if sp_.get("kernel_decls"):
        c_ = copy.deepcopy(core_s); c_["kernel_formalization"]["axiom_report"][sp_["kernel_decls"][0]] = ["propext", "sorryAx"]
        r_["axioma_fora_do_trio"] = um._v392_registro(sp_, c_)["all_verified"] is False
    nck_ = 0; nck_ok_ = 0
    for ck_ in sp_.get("checks", []):
        if ck_["onde"] in ("core", "kf") and ck_["op"] not in ("existe", "nao_contem", "diferente", "em", "falso"):   # nega o check mudando o valor lido no core sintetico (copia)
            refut_ = None
            for adult_ in (-1, 10 ** 9):   # uma faixa tem dois lados (maior_igual/menor_igual): basta um dos dois adulterados recusar
                c_ = copy.deepcopy(core_s); raiz_ = c_ if ck_["onde"] == "core" else c_["kernel_formalization"]
                cam_ = ck_["caminho"]; alvo_ = raiz_
                try:
                    for k_ in cam_[:-1]:
                        alvo_ = alvo_[k_]
                    alvo_[cam_[-1]] = adult_
                except Exception:   # noqa: BLE001
                    break
                refut_ = bool(refut_) or (um._v392_registro(sp_, c_)["all_verified"] is False)
            if refut_ is None:
                continue
            nck_ += 1; nck_ok_ += bool(refut_)
    if nck_:
        r_["checks_do_core_negados"] = [nck_ok_, nck_]
    RU[n_] = r_
RU_ok = all((v_ is True) or (isinstance(v_, list) and v_[0] == v_[1]) for r_ in RU.values() for v_ in r_.values())
U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V392_SPECS)
rep["unidade_registros"] = RU
# a cobertura KH-N1 (a): o log real passa; sem a linha TOTAL, com fora_do_trio=1, com nome com «» a mais, com axioma fora do trio: recusa
_AL = AUDIT_LOG; _ax = kf["axiom_report"]
_cv_ok = um._v392_axiom_coverage(_AL, _ax)["ok"] is True
_cv_sem = um._v392_axiom_coverage(re.sub(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL.*$", "", _AL), _ax)["ok"] is False
_cv_fora = um._v392_axiom_coverage(re.sub(r"fora_do_trio=0", "fora_do_trio=1", _AL), _ax)["ok"] is False
_cv_nome = um._v392_axiom_coverage(_AL + "\n'Foo.\u00abbar\u00bb' depends on axioms: [propext]\n", _ax)["ok"] is False
_ax2 = dict(_ax); _ax2[next(iter(_ax2))] = ["propext", "sorryAx"]; _cv_ax = um._v392_axiom_coverage(_AL, _ax2)["ok"] is False
_cv_dup = um._v392_axiom_coverage(_AL + "TGL_AXIOM_COVERAGE_TOTAL decl=1 thm=1 fora_do_trio=0\n", _ax)["ok"] is False
U["cobertura_kh_n1"] = bool(_cv_ok and _cv_sem and _cv_fora and _cv_nome and _cv_ax and _cv_dup)
# (6b) r3 (13/10, apos a falha do rito 1): o PONTO DE CHAMADA REAL. verify_tgl_kernel_formalization() roda de ponta a ponta com o lake SIMULADO, que devolve os logs CRUS do sandbox:
#     build = lake_build.log (que TAMBEM traz a linha TGL_AXIOM_COVERAGE_TOTAL, pois o lake build compila TGL/Audit.lean) e audit = audit.log. Na r1/r2 o ensaio chamava a funcao so com o audit.log e a linha
#     aparecia 1x; no rito o blob build+audit tinha 2x e o veredito deu FAILED. O ensaio agora exige o veredito STAGE1_VERIFIED/all_verified=True pela funcao real, e o controle negativo (a chamada antiga com o blob) recusa.
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
_sv = (um.run_process_checked, um._find_lake); um.run_process_checked = _fake_run; um._find_lake = lambda: "lake"
try:
    _ovf = um.verify_tgl_kernel_formalization()
    _blob_antigo = um._v392_axiom_coverage(_LB + _AUD, _ovf["axiom_report"])   # o ponto de chamada ANTIGO (blob build+audit): tem de recusar
finally:
    um.run_process_checked, um._find_lake = _sv
rep["verify_kernel_ponta_a_ponta"] = {"verdict": _ovf["verdict"], "all_verified": _ovf["all_verified"], "cobertura": _ovf["axiom_coverage_v392"], "chamada_antiga_com_blob": _blob_antigo}
U["verify_kernel_real_com_logs_crus_do_build_e_do_audit"] = bool(_ovf["all_verified"] is True and _ovf["verdict"].startswith("TGL_KERNEL_STAGE1_VERIFIED") and _ovf["axiom_coverage_v392"]["ok"] is True)
U["controle_negativo_blob_build_mais_audit_recusa"] = bool(_blob_antigo["ok"] is False and _blob_antigo.get("linhas") == 2)

# (7) a varredura recursiva e o detector de sorry, com controles
tmp = tempfile.mkdtemp(prefix="v392_varr_"); _fd = um.FORMAL_DIR
try:
    os.makedirs(os.path.join(tmp, "TGLExt", "O16", "sub")); os.makedirs(os.path.join(tmp, "TGL"))
    open(os.path.join(tmp, "TGLExt", "O16", "sub", "Mau.lean"), "w", encoding="utf-8").write("theorem t : True := by sorry\n")
    open(os.path.join(tmp, "TGLExt", "Bom.lean"), "w", encoding="utf-8").write("-- sorry so no comentario\ntheorem u : True := trivial\n")
    open(os.path.join(tmp, "TGLExt", "ProbeX.lean"), "w", encoding="utf-8").write("theorem p : True := by sorry\n")
    um.FORMAL_DIR = tmp
    hits, n_, o16_, pul_ = um._v392_scan_tokens(); hits_antigo = um._lean_source_forbidden_tokens()
finally:
    um.FORMAL_DIR = _fd; shutil.rmtree(tmp, ignore_errors=True)
U["varredura_pega_o_O16_aninhado"] = hits == ["TGLExt/O16/sub/Mau.lean:sorry"] and n_ == 2 and o16_ == 1 and pul_ == 1
U["funcao_patchada_pega_o_O16"] = hits_antigo == ["TGLExt/O16/sub/Mau.lean:sorry"]
_hr, _n, _o, _p = um._v392_scan_tokens(); rep["varredura_no_kernel_materializado"] = {"hits": _hr[:5], "arquivos": _n, "TGLExt_O16": _o, "probes_pulados": _p}
U["varredura_do_kernel_materializado_limpa"] = not _hr and _n > 1000 and _o > 100
D1 = um._v392_sorry_detects("x.lean:3:4: warning: declaration uses `sorry`\n")[0]; D2 = um._v392_sorry_detects("warning: declaration uses 'sorry'\n")[0]
D3 = um._v392_sorry_detects("'Foo.bar' depends on axioms: [propext, sorryAx, Quot.sound]\n")[0]; D4 = um._v392_sorry_detects("'Foo.bar' depends on axioms: [propext, Quot.sound]\n")[0]
D5 = um._v392_sorry_detects("o texto diz sorry mas nao e' o aviso\n")[0]
U["detector_de_sorry"] = D1 is True and D2 is True and D3 is True and D4 is False and D5 is False
_fxo = um._v392_sorry_fixture_ok(); U["detector_na_saida_real_do_lean_da_bancada"] = _fxo[0] is True and _fxo[1] is None
U["o_detector_antigo_era_cego_para_crases"] = ("declaration uses 'sorry'" in "warning: declaration uses `sorry`") is False   # o controle: a string da v391 nao casa
_srcw = open(os.path.join(DRY, "um.py"), encoding="utf-8").read()
U["check_novo_no_prove_bench_lean_controls"] = _srcw.count("_v392_sorry_fixture_ok()[0])]") == 1 and _srcw.count("_v392_sorry_detects(out)") == 1 and 'sorry = "declaration uses \'sorry\'" in out' not in _srcw
import hashlib
U["conserto_B_presente"] = (hashlib.sha256(um._V392_FOOTER_B.encode("utf-8")).hexdigest() == um._V392_FOOTER_B_SHA256 if hasattr(um, "_V392_FOOTER_B") else False) and _srcw.count("footer_b = (kind == \"POSITIVO\")") == 1 and "TGL_FOOTER_B_TOTAL" in um._V392_FOOTER_B and _srcw.count("a_.split(\".{\")[0] not in") == 1
rep["unidade"] = U; print("unidade:", U)
# (8) o artigo
DEVE = {"pt": ["As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "rank=posto=nome", "Verdade é a projeção do posto", "O que entra.", "recursiva", "Os registros ao lado do gate (v392).", "PostoAdendo", "Ao lado (v392, 13/10/2026, gerência c1, em nome próprio)", "Errata ao lado do parágrafo da v362",
               "Introdução: o que este código faz agora (v384 a v392", "O estatuto da prova (v391).", "A Fundação (v390)."],
        "en": ["The v392 stones: fourteen new kernel modules and two barrier repairs", "rank=posto=nome", "Verdade é a projeção do posto", "What enters.", "recursive", "The records beside the gate (v392).", "PostoAdendo", "Beside (v392, 13/10/2026, management c1, in its own name)", "Erratum beside the v362 paragraph",
               "Introduction: what this code does now (v384 to v392", "The status of the proof (v391).", "The Foundation (v390)."]}
TOC = {"pt": ["As pedras da v392: catorze módulos novos", "v384 a v392"], "en": ["The v392 stones: fourteen new kernel modules", "v384 to v392"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P)); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v392_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    a = flat.find("As pedras da v392: catorze módulos novos no kernel" if lang == "pt" else "The v392 stones: fourteen new kernel modules")
    bb = flat.find("O estatuto da prova: provada" if lang == "pt" else "The status of the proof: proved", a + 10)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    tp = os.path.join(DRY, "dry_v392_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v392_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec),
                           "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc]}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["guarda"] or v["secao_chars"] < 2500 or v["toc_faltam"] or v["nd_na_secao"]]
cv = dict(copy.deepcopy(c)); cv.pop("pedras_v392", None); cv.pop("varredura_e_sorry_v392", None)
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r, _l = compilar(cv, "dry_v392_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    rep["variante"][lang] = {"rc": _r, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["frase_guarda"]]
# (9) md e manifesto
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v392**" in md, "pedras_v392": "As pedras da v392 (13/10/2026)" in md, "v391_fica": "O estatuto da prova (v391, 07/10/2026)" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v392**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_citacoes_v392.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
# (11) o INDICE DA IALD, chamada REAL: prove_the_iald_index do candidato, importado em processo isolado, sobre o nucleo da tentativa 1 com o kernel verde (prova_indice_v392.py; mesma tecnica de exame_preflight/t10_index.py)
def _indice(*flags):
    r_ = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "prova_indice_v392.py"), os.path.join(HERE, cand)] + list(flags), capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return json.loads(r_.stdout.strip().splitlines()[-1])
    except Exception:
        return {"all_verified": None, "erro": (r_.stderr or r_.stdout)[-400:]}
_ix0 = _indice(); _ixa = _indice("--sem-ambiguos"); _ixg = _indice("--sem-gerados")
rep["indice_da_iald"] = {"candidato": _ix0, "controle_negativo_sem_ambiguos_v392": {k: _ixa.get(k) for k in ("all_verified", "verdict", "n_ausentes")}, "controle_negativo_sem_referentes_gerados_v392": {k: _ixg.get(k) for k in ("all_verified", "verdict", "n_ausentes")}}
indice_ok = bool(_ix0.get("all_verified") is True and str(_ix0.get("verdict") or "").startswith("THE_IALD_INDEX_IS_BUILT") and _ix0.get("n_ausentes") == 3 and not _ix0.get("fails")
                 and _ixa.get("all_verified") is False and _ixg.get("all_verified") is False)
rep["indice_da_iald"]["ok"] = indice_ok; print("indice da IALD:", json.dumps(rep["indice_da_iald"], ensure_ascii=False)[:700])
rep["pacote_dos_demais_arquivos_do_kernel_iguais_ao_Nos"] = not dif_nos
ok = (viz_ok and mf_ok and all(U.values()) and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
      and all(iguais.values()) and not dif_nos and rep["escada"] == [ESP, ESP] and indice_ok)
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"vizinhos": viz_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"],
                                                                      "proib": _proib, "citacoes": _cc.returncode, "kernel_igual": all(iguais.values()), "dif_nos": len(dif_nos), "escada": rep["escada"], "indice_da_iald": rep["indice_da_iald"]}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)

# -*- coding: utf-8 -*-
"""[DELTA 19/10 -- integracao final: candidato novo, sandbox k394d, kernel_d19, pedra e registro do criterio binario, troca de palavra THEOREMS->FLAGS, h8 da arvore simulada; etapas obrigatorias novas: (11) simular_arvore_do_nos e (12) exame_pontos_v394 sobre o candidato novo]
ensaio_a_seco_v394.py -- ENSAIO A SECO da v394 (molde: ensaio_a_seco_v393.py), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v394.py <candidato.py> <rotulo>
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox construido (os 1421 arquivos); (2) importa (o rito NAO roda); UM_VERSION v394;
(3) o core da v393 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox (build = lake_build.log, audit = audit.log);
(4) os registros vizinhos RECOMPUTADOS (v387, v389, v390, v391, pedras_v392, varredura_v392 e os por spec da v392): iguais, ou a TROCA DITA (so' numeros); (5) o FLUXO PRINCIPAL v393+v394 (as instrucoes
etiquetadas do main); (6) unidade: cada registro novo recusa visivelmente (tempo, residuo quadratico, rede, indice, specs, cobertura); (7) o selo (a instrucao `seal = {...}` do main) e o indice (chamada real);
(8) artigo PT/EN, pdflatex x2; (9) .md e manifesto; (10) o conferidor de citacoes."""
import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta19_v394 as DL  # noqa: E402
C = "C:" + os.sep
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); CORE0P = os.path.join(NOS, "um_absoluto.json")
if hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16] != "18be2ddb06c60f90":   # o Nos ja nao e' a v393 (rito v394 em curso): a v393 SELADA vem da copia base_v393
    CORE0P = os.path.join(HERE, "base_v393", "um_absoluto.json")
SELO0P = os.path.join(os.path.dirname(CORE0P), "um_absoluto_selo.json")
KB = DL.SANDBOX
KD = os.path.join(HERE, DL.KERNEL_DIR)
cand = sys.argv[1] if len(sys.argv) > 1 else DL.CANDIDATO; rot = sys.argv[2] if len(sys.argv) > 2 else "v394" + DL.ROT   # a pasta dry_v394 do candidato anterior (registro) NAO e' apagada
DRY = os.path.join(HERE, "dry_" + rot)
if os.path.isdir(DRY):
    shutil.rmtree(DRY)
os.makedirs(DRY); shutil.copyfile(os.path.join(HERE, cand), os.path.join(DRY, "um.py"))
EMB, _, _, h16 = carregar(os.path.join(DRY, "um.py"))
for rel, content in EMB.items():
    p = os.path.join(DRY, "tgl_kernel", *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="").write(content)
# DELTA 19/10 (achado do exame final): a pasta do Nos tem arquivos que NAO estao embutidos (hoje: _check_damming.lean; ExtrairDeps.lean sai do hash por exclusao nominal) e o hash formal do RITO os conta. A arvore do ensaio os recebe como
# estao (so' leitura do Nos), como o rito os encontrara: sem isto o h8 'passava' num ensaio que materializava so' o embutido.
NOSK = os.path.join(NOS, "tgl_kernel"); EXTRAS_NOS = []
for dp_, dn_, fn_ in os.walk(NOSK):
    if ".lake" in dp_.replace("\\", "/").split("/"):
        continue
    for nm_ in fn_:
        if nm_.endswith(".lean") or nm_ in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel_ = os.path.relpath(os.path.join(dp_, nm_), NOSK).replace("\\", "/")
            if rel_ not in EMB:
                EXTRAS_NOS.append(rel_); d_ = os.path.join(DRY, "tgl_kernel", *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True); shutil.copyfile(os.path.join(dp_, nm_), d_)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v394.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"residuais_do_nos_na_arvore_do_ensaio": EXTRAS_NOS, "candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SEM_GPU_SEM_RITO": "o core da v393 selada + o kernel REAL lido pelo verify com os logs crus do sandbox"}
rd = lambda p: open(p, "rb").read()
# (1) o kernel materializado == o sandbox construido, byte a byte (TODOS os arquivos embutidos)
dif_kb = [r for r in EMB if not os.path.exists(os.path.join(KB, *r.split("/"))) or rd(os.path.join(KB, *r.split("/"))) != EMB[r].encode("utf-8")]
rep["kernel_embutido_vs_sandbox"] = {"n": len(EMB), "diferentes": dif_kb[:5], "n_diferentes": len(dif_kb)}; print("kernel embutido == sandbox:", not dif_kb, "(%d arquivos)" % len(EMB))
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
assert um.UM_VERSION == "v394"
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
selo0 = json.load(open(SELO0P, encoding="utf-8"))
assert "pedras_v393" in core0 and "tempo_frequencia_v394" not in core0 and selo0["um_version"] == "v393"
core_s = json.loads(json.dumps(core0))
# (3) o PONTO DE CHAMADA REAL do kernel: verify_tgl_kernel_formalization() de ponta a ponta com o lake SIMULADO, que devolve os logs CRUS do sandbox
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
kf = core_s["kernel_formalization"]
chaves_antigas_ausentes = sorted(k for k in kf if k not in _ovf)
kf.update(_ovf)
rep["verify_kernel_ponta_a_ponta"] = {"verdict": _ovf["verdict"], "all_verified": _ovf["all_verified"], "cobertura": _ovf["axiom_coverage_v392"], "chamada_antiga_com_blob": _blob_antigo, "axiom_report_n": len(_ovf["axiom_report"]),
                                      "chaves_do_kf_da_v393_que_o_verify_nao_devolve": chaves_antigas_ausentes[:10], "proveniencia": _ovf.get("declaration_sources_status_v394")}
print("verify real:", _ovf["verdict"][:80], _ovf["all_verified"], rep["verify_kernel_ponta_a_ponta"]["cobertura"].get("decl"), "nao lidas:", rep["verify_kernel_ponta_a_ponta"]["cobertura"].get("nao_lidas_pelo_regex"))
ESP = CM["escada"][1]
# a escada: SEM as bandeiras novas (o kf da v393) a escada do candidato NAO fecha
_el0 = um.prove_external_ladder(1.0, core0["kernel_formalization"])
rep["escada_sem_as_bandeiras_novas"] = [_el0.get("n_theorems_clean"), _el0.get("n_theorems_expected"), _el0.get("all_verified")]
E393 = int(core0["external_ladder"]["n_theorems_expected"])   # LIDO do core da v393 selada (nada digitado)
assert rep["escada_sem_as_bandeiras_novas"][0] == E393 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True, rep["escada_sem_as_bandeiras_novas"]
_el = um.prove_external_ladder(1.0, kf); core_s["external_ladder"] = _el
rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]; rep["escada_esperada"] = ESP; print("escada recomputada:", rep["escada"], "esperada:", ESP)
# (4) os vizinhos RECOMPUTADOS (a ordem do rito): a TROCA DITA (so' numeros) ou fica IGUAL
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
cs2 = copy.deepcopy(core_s); mud = {}; iguais_v = []


PALAVRA = {"estatuto_da_prova_v391": ["_THEOREMS_", "_FLAGS_"]}   # a TROCA DE PALAVRA declarada (decisao da gerencia, 19/10; C11): a escada conta bandeiras, nao teoremas
_pal = lambda nome, s_: s_.replace(PALAVRA[nome][0], PALAVRA[nome][1]) if nome in PALAVRA else s_
palavra_trocada = {}


def recomputa(nome, fn):
    novo = fn(cs2); cs2[nome] = novo
    a, b = str((core0.get(nome) or {}).get("verdict") or ""), str(novo.get("verdict") or "")
    if a == b:
        iguais_v.append(nome)
    else:
        tr_ = nome in PALAVRA and PALAVRA[nome][0] in a and PALAVRA[nome][1] in b and PALAVRA[nome][0] not in b
        if tr_:
            palavra_trocada[nome] = PALAVRA[nome]
        mud[nome] = {"antes": a[:300], "depois": b[:300], "so_numeros": _num(_pal(nome, a)) == _num(b), "palavra_trocada": tr_, "all_verified": novo.get("all_verified")}


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
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
for n_, d_ in list(mud.items()):
    if _nc(d_["antes"]) == _nc(d_["depois"]):
        mud.pop(n_); iguais_v.append(n_ + "(contagens CORE_n_ normalizadas)")
N393 = len(core0["kernel_formalization"]["axiom_report"])
NUMS = ["KERNEL_%d_OF_%d" % (E393, E393), "%d_OF_%d_DECLARATIONS" % (N393, N393), "LADDER_%d_OF_%d" % (E393, E393)]
m_sc = re.search(r"SCAN_(\d+)_FILES", str((core0.get("varredura_e_sorry_v392") or {}).get("verdict") or ""));
if m_sc:
    NUMS.append("SCAN_%s_FILES" % m_sc.group(1))
carregam = sorted(k for k, m in core0.items() if isinstance(m, dict) and any(n in str(m.get("verdict") or "") for n in NUMS))
rep["vizinhos"] = {"recomputados_iguais": iguais_v, "palavra_trocada": palavra_trocada, "mudaram": mud, "carregam_os_numeros_do_kernel_no_core0": carregam, "carregam_e_nao_recomputados_ainda": sorted(set(carregam) - set(mud) - set(iguais_v))}
core_s = cs2
# (5) o fluxo principal: as instrucoes etiquetadas v393 e v394 do main
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v393" in l or "v394" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
for _k in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393"):
    core_s.pop(_k, None)   # o fluxo os recria; comparam-se depois com os da v393 selada
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v393+v394>", "exec"), ns); _err = None
except Exception as e:  # noqa
    import traceback; _err = repr(e) + traceback.format_exc()[-800:]
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]
NOVAS394 = ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS)
novas_chaves = sorted(k for k in c if k not in core0)
tf = c.get("tempo_frequencia_v394") or {}; rq = c.get("regra_quadratica_v394") or {}; rf = c.get("rede_fock_v394") or {}
v393_recriados = {k: {"igual_ao_selado": str((c.get(k) or {}).get("verdict")) == str((core0.get(k) or {}).get("verdict")), "all_verified": (c.get(k) or {}).get("all_verified"), "antes": str((core0.get(k) or {}).get("verdict")), "depois": str((c.get(k) or {}).get("verdict"))}
                  for k in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")}
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": novas_chaves, "stdout": _mf.strip().splitlines(),
                   "tempo": {x: tf.get(x) for x in ("verdict", "all_verified", "exact_ladder", "runtime_executed", "scope")}, "quadratica": {x: rq.get(x) for x in ("verdict", "all_verified", "exact_ladder", "runtime_executed")},
                   "rede": {x: rf.get(x) for x in ("verdict", "all_verified", "exact_ladder", "actual_processes_ok", "whole_certificate_inhabited")},
                   "n_formais": {"tempo": len(tf.get("formal_theorems") or {}), "quadratica": len(rq.get("formal_theorems") or {}), "rede": len(rf.get("formal_declarations") or {}), "rede_fontes": len(rf.get("embedded_sources") or {})},
                   "registros_v394": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V394_NOMES_REGISTROS}, "v393_recriados": v393_recriados,
                   "checks_dos_registros_que_falharam": {n_: [ck_ for ck_ in ((c.get(n_) or {}).get("checks") or []) if not ck_.get("ok")][:6] for n_ in um._V394_NOMES_REGISTROS + list(um._V393_NOMES_REGISTROS) if (c.get(n_) or {}).get("all_verified") is not True}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k not in ("stdout",)}, ensure_ascii=False, default=str)[:3800])
for k_, d_ in list(v393_recriados.items()):
    if not d_["igual_ao_selado"] and _num(d_["antes"]) == _num(d_["depois"]) and d_["all_verified"] is True:
        mud[k_] = {"antes": d_["antes"], "depois": d_["depois"], "so_numeros": True, "all_verified": True}
v393_ok = all(d_["all_verified"] is True and (d_["igual_ao_selado"] or k_ in mud) for k_, d_ in v393_recriados.items())
_nomes_v = list(mud) + [x.split("(")[0] for x in iguais_v]
_falham_v = [n_ for n_ in _nomes_v if n_ in cs2 and (cs2.get(n_) or {}).get("all_verified") is not True]
_ausentes_v = [n_ for n_ in _nomes_v if n_ not in cs2]
viz_ok = (all(v["so_numeros"] and v["all_verified"] is True for v in mud.values()) and v393_ok and not _falham_v)
rep["viz_det"] = {"mud_so_numeros_e_selados": all(v["so_numeros"] and v["all_verified"] is True for v in mud.values()), "v393_ok": v393_ok, "nao_selados": _falham_v, "ausentes_do_core": _ausentes_v[:10]}
mf_ok = (not _err and sorted(k for k in novas_chaves if k.endswith("_v394")) == sorted(NOVAS394) and tf.get("all_verified") is True and rq.get("all_verified") is True and rf.get("all_verified") is True
         and all((c.get(n_) or {}).get("all_verified") is True for n_ in um._V394_NOMES_REGISTROS) and rf.get("whole_certificate_inhabited") is False
         and "ADMITTED" in str(((c.get("regra_consumidor_v393") or {}).get("satisfacao") or {}).get("veredito_do_rito")))
# (6) unidade
U = {}
EMBK = um._EMBEDDED_KERNEL_FILES
def _alt_src(rel, fn):
    k0 = EMBK[rel]; EMBK[rel] = k0 + " "
    try:
        return fn()
    finally:
        EMBK[rel] = k0
cs = lambda: copy.deepcopy(core_s)
# tempo
_c = cs(); _c["kernel_formalization"]["axiom_report"].pop(um._V394_FORMAL_CONTRACT["theorems"][0], None)
U["tempo_teorema_ausente_recusa"] = um.tempo_frequencia_v394(_c)["all_verified"] is False
U["tempo_fonte_adulterada_recusa"] = _alt_src("TGLExt/TimeGravitonFlow.lean", lambda: um.tempo_frequencia_v394(cs())["all_verified"] is False)
_c = cs(); _c["kernel_formalization"]["axiom_report"][um._V394_FORMAL_CONTRACT["theorems"][1]] = ["propext", "sorryAx"]
U["tempo_axioma_fora_do_trio_recusa"] = um.tempo_frequencia_v394(_c)["all_verified"] is False
_c = cs(); _c["external_ladder"]["n_theorems_clean"] -= 1
U["tempo_escada_nao_fecha_recusa"] = um.tempo_frequencia_v394(_c)["all_verified"] is False
_ins = um._V394_INSCRIPTIONS; _ins2 = copy.deepcopy(_ins); _k0 = next(iter(_ins2)); _ins2[_k0]["text"] += " "; um._V394_INSCRIPTIONS = _ins2
try:
    U["tempo_cunhagem_adulterada_recusa"] = um.tempo_frequencia_v394(cs())["all_verified"] is False
finally:
    um._V394_INSCRIPTIONS = _ins
U["tempo_tudo_certo"] = um.tempo_frequencia_v394(cs())["all_verified"] is True
# residuo quadratico
_c = cs(); _c["kernel_formalization"]["axiom_report"].pop(um._V394_QUADRATIC_CONTRACT["theorems"][0], None)
U["quadratica_teorema_ausente_recusa"] = um.regra_quadratica_v394(_c)["all_verified"] is False
U["quadratica_fonte_adulterada_recusa"] = _alt_src("TGLExt/RuleQuadraticResidual.lean", lambda: um.regra_quadratica_v394(cs())["all_verified"] is False)
_c = cs(); _c["tempo_frequencia_v394"] = {"all_verified": False}
U["quadratica_sem_o_tempo_recusa"] = um.regra_quadratica_v394(_c)["all_verified"] is False
U["quadratica_tudo_certo"] = um.regra_quadratica_v394(cs())["all_verified"] is True
# rede
_c = cs(); _dn = sorted(_c["kernel_formalization"]["declaration_sources_v394"])[0]
_c["kernel_formalization"]["declaration_sources_v394"][_dn] = "TGLExt/F1Fecho394/Outro.lean"
_nome_rede = um._V394_NETWORK_CONTRACT["declarations"][0]; _c["kernel_formalization"]["declaration_sources_v394"][_nome_rede] = "TGLExt/F1Fecho394/Outro.lean"
U["rede_proveniencia_diferente_recusa"] = um.rede_fock_v394(_c)["all_verified"] is False
U["rede_fonte_adulterada_recusa"] = _alt_src(sorted(um._V394_NETWORK_CONTRACT["source_sha256"])[0], lambda: um.rede_fock_v394(cs())["all_verified"] is False)
_c = cs(); _c["kernel_formalization"]["axiom_report"][um._V394_NETWORK_CONTRACT["declarations"][0]] = ["propext", "sorryAx"]
U["rede_axioma_fora_do_trio_recusa"] = um.rede_fock_v394(_c)["all_verified"] is False
_c = cs(); _c["kernel_formalization"]["declaration_sources_status_v394"] = {"ok": False}
U["rede_status_da_proveniencia_falso_recusa"] = um.rede_fock_v394(_c)["all_verified"] is False
_c = cs(); _c["external_ladder"]["n_theorems_expected"] += 1
U["rede_escada_nao_fecha_recusa"] = um.rede_fock_v394(_c)["all_verified"] is False
_c = cs(); _c["regra_quadratica_v394"] = {"all_verified": False}
U["rede_sem_a_regra_quadratica_recusa"] = um.rede_fock_v394(_c)["all_verified"] is False
U["rede_tudo_certo"] = um.rede_fock_v394(cs())["all_verified"] is True
# o leitor/proveniencia (parse_*) recusa
U["parse_axiomas_conflito_recusa"] = um.parse_lean_axioms_v394("'a.b' depends on axioms: [propext]\n'a.b' depends on axioms: [Classical.choice]\n")["ok"] is False and um.parse_lean_axioms_v394("")["ok"] is False
U["parse_proveniencia_duplicada_ou_malformada_recusa"] = um.parse_lean_provenance_v394("TGL_DECL_SOURCE\ta\tTGLExt.X\nTGL_DECL_SOURCE\ta\tTGLExt.X\n")["ok"] is False and um.parse_lean_provenance_v394("TGL_DECL_SOURCE\ta\n")["ok"] is False and um.parse_lean_provenance_v394("")["ok"] is False
U["parse_nome_com_aspas_unicode_lido"] = "F«x».y" in um.parse_lean_axioms_v394("'F«x».y' depends on axioms: [propext]\n")["axioms"]
# o indice qualificado: chamada REAL sobre o core do ensaio + controles
_t0 = um.prove_the_iald_index(cs())
rep["indice_da_iald"] = {"verdict": _t0.get("verdict"), "all_verified": _t0.get("all_verified"), "fails": [str(ck[0])[:200] for ck in _t0["checks"] if not ck[1]], "n_checks": len(_t0["checks"]), "proveniencia_erros": _t0.get("proveniencia_erros", [])[:5],
                         "legacy_diagnostic_v393": _t0.get("legacy_diagnostic_v393") and {k: (v if not isinstance(v, (list, dict)) else (len(v))) for k, v in _t0["legacy_diagnostic_v393"].items()}}
_c = cs(); _c["kernel_formalization"]["declaration_sources_v394"] = {}
U["indice_sem_proveniencia_recusa"] = um.prove_the_iald_index(_c)["all_verified"] is False
_c = cs(); _c["kernel_formalization"]["formal_files_sha256"][sorted(um._V394_NETWORK_CONTRACT["source_sha256"])[0]] = "0" * 64
U["indice_hash_de_fonte_diferente_recusa"] = um.prove_the_iald_index(_c)["all_verified"] is False
_c = cs(); _c["kernel_formalization"]["declaration_sources_status_v394"] = {"ok": False, "errors": ["X"]}
U["indice_status_da_proveniencia_falso_recusa"] = um.prove_the_iald_index(_c)["all_verified"] is False
_c = cs(); _c["kernel_formalization"]["axiom_report"].pop(um._V394_NETWORK_CONTRACT["declarations"][0], None)
U["indice_declaracao_sem_axioma_recusa"] = um.prove_the_iald_index(_c)["all_verified"] is False
U["indice_tudo_certo"] = _t0["all_verified"] is True and str(_t0.get("verdict")).startswith("THE_IALD_INDEX_QUALIFIED_COMPILER_PROVENANCE_VERIFIED")
_ix = um.build_the_iald_index(cs())
rep["indice_da_iald"].update({"n_nomes": _ix["n_nomes"], "n_ambiguos": len(_ix["ambiguos"]), "n_ausentes": _ix["n_ausentes"], "violacoes": _ix["violacoes"][:5], "cegos_de_namespace": _ix["cegos_de_namespace"][:5], "presente_apagada": _ix["presente_apagada"][:5]})
_ia = [a for a in _ix["ambiguos"]][:1]
U["indice_alias_ambiguo_mostra_candidatos"] = (not _ia) or (_ix["indice"][_ia[0]].get("arquivo") is None and len(_ix["indice"][_ia[0]].get("candidatos_qualificados", [])) > 1)
# a cobertura KH-N1 (4 negativos) com o leitor v394
_AL = _AUD; _ax = kf["axiom_report"]
_cv_ok = um._v392_axiom_coverage(_AL, _ax)["ok"] is True
_cv_sem = um._v392_axiom_coverage(re.sub(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL.*$", "", _AL), _ax)["ok"] is False
_cv_fora = um._v392_axiom_coverage(re.sub(r"fora_do_trio=0", "fora_do_trio=1", _AL), _ax)["ok"] is False
_ax2 = dict(_ax); _ax2[next(iter(_ax2))] = ["propext", "sorryAx"]; _cv_ax = um._v392_axiom_coverage(_AL, _ax2)["ok"] is False
_ax3 = dict(_ax); _ax3.pop(next(iter(_ax3))); _cv_cego = um._v392_axiom_coverage(_AL, _ax3)["ok"] is False   # constante coberta pelo log e ausente do axiom_report
U["cobertura_kh_n1_com_o_leitor_v394"] = bool(_cv_ok and _cv_sem and _cv_fora and _cv_ax and _cv_cego)
U["verify_kernel_real_com_logs_crus_do_build_e_do_audit"] = bool(_ovf["all_verified"] is True and _ovf["verdict"].startswith("TGL_KERNEL_STAGE1_VERIFIED") and _ovf["axiom_coverage_v392"]["ok"] is True and (_ovf.get("declaration_sources_status_v394") or {}).get("ok") is True)
U["controle_negativo_blob_build_mais_audit_recusa"] = bool(_blob_antigo["ok"] is False)
U["kernel_embutido_igual_ao_sandbox"] = not dif_kb
U["proveniencia_cobre_o_axiom_report"] = set(_ovf["declaration_sources_v394"]) == set(_ovf["axiom_report"])
# (6a) O REGISTRO NOVO criterio_binario_de_parada_v394: controles negativos (bandeira falsa, sha errado, citado fora do trio, pedra/fonte adulterada) e o positivo; veredito sem palavra proibida; no PONTO DE CHAMADA REAL (o fluxo do main acima)
_cr = [s_ for s_ in um._V394_SPECS if s_["nome"] == "criterio_binario_de_parada_v394"]
assert len(_cr) == 1 and "criterio_binario_de_parada_v394" in um._V394_NOMES_REGISTROS, "o registro novo nao esta em _V394_SPECS/_V394_NOMES_REGISTROS"
_cr = _cr[0]; _Vr = lambda c_: um._v392_registro(_cr, c_)
_c = cs(); _c["kernel_formalization"][DL.FLAG_KEY] = False; _r = _Vr(_c)
U["criterio_bandeira_falsa_recusa"] = bool(_r["all_verified"] is False and "NOT_SEALED_THIS_RUN" in _r["verdict"] and "KERNEL_BANDEIRAS" in _r["verdict"])
_c = cs(); _c["kernel_formalization"]["axiom_report"].pop(DL.THEOREM, None); _r = _Vr(_c)
U["criterio_teorema_ausente_recusa"] = bool(_r["all_verified"] is False and "KERNEL_DECLARACOES" in _r["verdict"])
_c = cs(); _c["kernel_formalization"]["axiom_report"][DL.CITED[0]] = ["propext", "sorryAx"]; _r = _Vr(_c)
U["criterio_citado_fora_do_trio_recusa"] = bool(_r["all_verified"] is False and "KERNEL_DECLARACOES" in _r["verdict"])
_c = cs(); _c["kernel_formalization"]["axiom_report"][DL.THEOREM] = ["propext", "Classical.choice", "Quot.sound", "TGLExt.axiomaPlantado"]; _r = _Vr(_c)
U["criterio_teorema_com_axioma_fora_do_trio_recusa"] = bool(_r["all_verified"] is False and "KERNEL_DECLARACOES" in _r["verdict"])
for _ch in _cr["verbatins"]:
    _ant = dict(um._V392_VERBATINS2[_ch]); um._V392_VERBATINS2[_ch]["text"] += " "
    try:
        _r = _Vr(cs()); U["criterio_sha_errado_" + _ch[-16:]] = bool(_r["all_verified"] is False and ("VERBATIM_" + _ch) in _r["verdict"] and "NOT_SEALED_THIS_RUN" in _r["verdict"])
    finally:
        um._V392_VERBATINS2[_ch] = _ant
_ant = dict(um._V392_FONTES["delta19_pedra"]); um._V392_FONTES["delta19_pedra"]["sha256"] = "0" * 64
try:
    _r = _Vr(cs()); U["criterio_fonte_da_pedra_adulterada_recusa"] = bool(_r["all_verified"] is False and "FONTE_delta19_pedra" in _r["verdict"])
finally:
    um._V392_FONTES["delta19_pedra"] = _ant
_c = cs(); _c["kernel_formalization"]["formal_files_sha256"][DL.STONE_REL] = "0" * 64; _r = _Vr(_c)
U["criterio_pedra_adulterada_no_kernel_do_rito_recusa"] = bool(_r["all_verified"] is False and "CHECK_g5" in _r["verdict"])
_r = _Vr(cs()); _ok_crit = bool(_r["all_verified"] is True and _r["verdict"].startswith("TGL_BINARY_STOP_CRITERION_V394__THE_BINARY_READING_FLOATS_AT_THE_FIXED_POINT") and _r.get("does_not_gate_core") is True)
U["criterio_tudo_certo"] = _ok_crit
U["criterio_veredito_sem_palavra_proibida"] = bool(not um._v392_guarda_texto(_r["verdict"]) and not um._v392_guarda_texto(json.dumps({k_: _r.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)))
rep["criterio_binario"] = {"verdict": _r["verdict"], "all_verified": _r["all_verified"], "bandeira": DL.FLAG_KEY, "teorema": DL.THEOREM, "verbatim": {k_: {"sha256": v_["sha256"], "embedded_ok": v_["embedded_ok"]} for k_, v_ in (_r.get("verbatim") or {}).items()},
                           "kernel": _r.get("kernel"), "checks": [c_.get("ok") for c_ in _r.get("checks", [])]}
# (6c) o GATE nao se move: recomputado com o kf novo (as bandeiras novas) e o feed V11 da v393; e o qg_closure do core nao foi tocado pelo fluxo
_n18 = lambda g_: sum(1 for fam_ in ("formal_flags", "physics_flags", "experiment_flags") for v_ in (g_.get(fam_) or {}).values() if v_ is True)
_J = lambda x_: json.dumps(x_, sort_keys=True, default=str)
_g_old = core0.get("qg_closure") or {}
try:
    _g_new = um.prove_qg_closure_gate(1.0, kf, independent_rite=core0.get("void_floor_v11"))
    gate_rec = {"verdict_igual": (_g_new.get("gate") or {}).get("verdict") == (_g_old.get("gate") or {}).get("verdict"), "n18_novo": _n18(_g_new), "n18_core0": _n18(_g_old),
                "flags_iguais": all(_J(_g_new.get(f_)) == _J(_g_old.get(f_)) for f_ in ("formal_flags", "physics_flags", "experiment_flags"))}
except Exception as _e:   # noqa: BLE001
    gate_rec = {"EXCECAO": repr(_e)[:300]}
gate_rec["qg_closure_do_core_intocado_pelo_fluxo"] = _J(c.get("qg_closure")) == _J(core0.get("qg_closure"))
rep["gate_recomputado"] = gate_rec
U["gate_nao_se_move"] = bool(gate_rec.get("verdict_igual") and gate_rec.get("n18_novo") == 18 == gate_rec.get("n18_core0") and gate_rec.get("flags_iguais") and gate_rec.get("qg_closure_do_core_intocado_pelo_fluxo"))
# (6b) os registros por spec: cada um recusa visivelmente (fonte adulterada; verbatim adulterado; bandeira do kernel faltando; cada check negado) -- v393 e v394
RU = {}
for sp_ in list(um._V393_SPECS) + list(um._V394_SPECS):
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
        if ck_["onde"] in ("core", "kf") and ck_["op"] in ("verdadeiro", "falso", "igual", "comeca", "maior_igual", "menor_igual"):
            c_ = copy.deepcopy(core_s); alvo_ = c_ if ck_["onde"] == "core" else c_["kernel_formalization"]; cam_ = ck_["caminho"]
            for k_ in cam_[:-1]:
                alvo_ = alvo_[k_]
            alvo_[cam_[-1]] = (False if ck_["op"] == "verdadeiro" else True if ck_["op"] == "falso" else -1 if ck_["op"] == "maior_igual" else 10 ** 9 if ck_["op"] == "menor_igual" else "ADULTERADO")
            nck_ += 1; nck_ok_ += um._v392_registro(sp_, c_)["all_verified"] is False
    r_["checks_do_core_negados"] = [nck_ok_, nck_]
    RU[n_] = r_
RU_ok = all((v_ is True) or (isinstance(v_, list) and v_[0] == v_[1]) for r_ in RU.values() for v_ in r_.values())
U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V393_SPECS) + len(um._V394_SPECS)
rep["unidade_registros"] = {k: {kk: vv for kk, vv in v.items() if not kk.startswith("verbatim_adulterado_")} | {"n_verbatins_adulterados_recusados": sum(1 for kk, vv in v.items() if kk.startswith("verbatim_adulterado_") and vv is True)} for k, v in RU.items()}
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
mud_selo = sorted(k for k in seal if J_(seal.get(k)) != J_(selo0.get(k)))
rep["selo"] = {"erro": _seal_err, "chaves_do_selo": len(seal), "difere_do_selo_v393": mud_selo, "registros_no_selo": {k: {x: (seal.get(k) or {}).get(x) for x in ("verdict", "all_verified")} for k in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394")},
               "registros_v394": seal.get("registros_v394")}
print("selo: difere em", mud_selo)
# DELTA 19/10: o core e o selo do ensaio ficam em DRY (core_ensaio.json, selo_ensaio.json): servem ao teste do caminho POSITIVO do conferidor (delta_19out\teste_conferidor_positivo.py), que monta um Nos falso a partir do DRY
_c_dump = dict(c); _c_dump["the_iald_index"] = um.prove_the_iald_index(copy.deepcopy(c))   # o main do rito poe o indice qualificado no core; o ensaio o computa a parte
json.dump({"core": _c_dump, "verdict": verdict}, open(os.path.join(DRY, "core_ensaio.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str); json.dump(seal, open(os.path.join(DRY, "selo_ensaio.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
selo_ok = (not _seal_err and all((seal.get(k) or {}).get("all_verified") is True for k in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394")) and all(((seal.get("registros_v394") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V394_NOMES_REGISTROS)
           and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and all(k in mud_selo for k in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "um_version"))
           and all(k in selo0 for k in ("fail_closed_selftest", "rite_checkpoints", "not_sealed_this_run")))
rep["unidade"] = U; print("unidade:", {k: v for k, v in U.items() if not v} or "todas True (%d)" % len(U))
# (8) o artigo
DEVE = {"pt": ["A integração do Codex e as cunhagens de 14 a 19/10 (v394)", "O que entra.", "O índice e o leitor.", "O que o modelo", "As cunhagens.", "O critério binário de parada (delta de 19/10).", "Limites.", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada", "Rede Fock nesta rodada",
               "A regra e o coração (v393)", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O estatuto da prova (v391).", "A Fundação (v390)."],
        "en": ["The Codex integration and the inscriptions of 14 to 19 Oct (v394)", "What enters.", "The index and the reader.", "What the", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Limits.", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run", "Fock network in this run",
               "The rule and the heart (v393)", "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]}
TOC = {"pt": ["A integração do Codex e as cunhagens de 14 a 19/10 (v394)", "v384 a v39"], "en": ["The Codex integration and the inscriptions of 14 to 19 Oct (v394)", "v384 to v39"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um._v394_article_tex(um.build_pt(cv, verdict, CORE0P), cv, "pt") if lang == "pt" else um._v394_article_tex(um.build_en(cv, verdict, CORE0P), cv, "en")); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v394_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    h0 = "A integração do Codex e as cunhagens de 14 a 19/10 (v394)" if lang == "pt" else "The Codex integration and the inscriptions of 14 to 19 Oct (v394)"
    h1 = "A regra e o coração (v393): a regra como inadmissão" if lang == "pt" else "The rule and the heart (v393): the rule as the refusal"
    iq = flat.find("O coração:" if lang == "pt" else "The heart:"); a = flat.find(h0, iq + 5); bb = flat.find(h1, a + 10)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    ik = flat.find("Palavras-chave" if lang == "pt" else "Keywords"); ii = flat.find("Introdução: o que este código faz agora" if lang == "pt" else "Introduction: what this code does now", iq)
    tp = os.path.join(DRY, "dry_v394_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v394_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec),
                           "quadro_logo_depois_do_resumo": bool(0 <= ik < iq < ii), "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc]}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["guarda"] or v["secao_chars"] < 2500 or v["toc_faltam"] or v["nd_na_secao"] or not v["quadro_logo_depois_do_resumo"]]
cv = dict(copy.deepcopy(c)); [cv.pop(k, None) for k in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394")]
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r, _l = compilar(cv, "dry_v394_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    rep["variante"][lang] = {"rc": _r, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["frase_guarda"]]
# (9) md e manifesto
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v394**" in md, "integracao_v394": "A integração do Codex e as cunhagens (v394, 19/10/2026)" in md, "v393_fica": "A regra e o coração (v393, 14/10/2026)" in md, "v392_fica": "As pedras da v392 (13/10/2026)" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v394**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_citacoes_v394.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
rep["viz_ok"] = viz_ok
# (11) ETAPA OBRIGATORIA (achado do exame final de 19/10): simular_arvore_do_nos -- a pasta Nos\\tgl_kernel DEPOIS do rito = o embutido do candidato + os residuais que o hash formal conta (_check_damming.lean); o kh_n1_cobertura_v394 TEM de selar nela
_cand_p = os.path.join(HERE, cand); _sha_full = hashlib.sha256(open(_cand_p, "rb").read()).hexdigest()
_pyr = lambda args_: subprocess.run([sys.executable, "-B", "-X", "utf8"] + args_, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, cwd=HERE)
_kh = [s_ for s_ in um._V394_SPECS if s_["nome"] == "kh_n1_cobertura_v394"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]
_sp = _pyr([os.path.join(HERE, "simular_arvore_do_nos.py"), "--candidato", _cand_p, "--logs", KD])
try:
    _sj = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _sj = {}
rep["simular_arvore_do_nos"] = {"rc": _sp.returncode, "formal_files_n_no_rito_real": _sj.get("formal_files_n_no_rito_real"), "pino_h8_entradas": len(_h8), "embutidos": _sj.get("embutidos"), "extras_no_nos_fora_do_corpo_embutido": _sj.get("extras_no_nos_fora_do_corpo_embutido"),
                               "kf_all_verified": _sj.get("kf_all_verified"), "indice": _sj.get("indice"), "registros": {k_: {"all_verified": (_sj.get(k_) or {}).get("all_verified"), "falhas": (_sj.get(k_) or {}).get("falhas")} for k_ in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394")}}
sim_ok = bool(_sp.returncode == 0 and _sj.get("formal_files_n_no_rito_real") == len(_h8) and _sj.get("kf_all_verified") is True and (_sj.get("indice") or {}).get("all_verified") is True
              and all((_sj.get(k_) or {}).get("all_verified") is True for k_ in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394")))
print("simular_arvore_do_nos:", sim_ok, "| entradas do hash formal no rito:", _sj.get("formal_files_n_no_rito_real"), "| pino h8:", len(_h8), "| extras:", _sj.get("extras_no_nos_fora_do_corpo_embutido"))
# (12) ETAPA OBRIGATORIA: exame_pontos_v394 sobre o candidato novo (os pontos de chamada REAIS, em processo isolado; termina com `ALGUM FALSO`)
_imp = os.path.join(HERE, "imp_" + _sha_full[:16])   # a arvore do exame tambem recebe os residuais do Nos (o script do exame materializa so' o embutido)
for rel_ in EXTRAS_NOS:
    d_ = os.path.join(_imp, "tgl_kernel", *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True); shutil.copyfile(os.path.join(NOSK, *rel_.split("/")), d_)
_ep = _pyr([os.path.join(HERE, "exame_pontos_v394.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v394.json"), "--sandbox", KB, "--sha256", _sha_full])
try:
    _ej = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _ej = {}
rep["exame_pontos"] = {"rc": _ep.returncode, "algum_falso": _ej.get("algum_falso"), "escada": _ej.get("escada"), "verify": {k_: (_ej.get("verify") or {}).get(k_) for k_ in ("all_verified", "ext_true", "n_ext", "novas_true", "n_novas", "n_lean_flags", "axiom_report_n")},
                       "gate_recomputado": _ej.get("gate_recomputado"), "chaves_novas_no_core": _ej.get("chaves_novas_no_core"), "chaves_existentes_mexidas_pelo_bloco": _ej.get("chaves_existentes_mexidas_pelo_bloco"), "nao_verdes": _ej.get("nao_verdes")}
exame_ok = bool(_ep.returncode == 0 and _ej.get("algum_falso") == [])
print("exame_pontos_v394:", exame_ok, "| algum falso:", _ej.get("algum_falso"))
ok = (viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
      and not dif_kb and rep["escada"] == [ESP, ESP] and rep["indice_da_iald"]["all_verified"] is True and sim_ok and exame_ok)
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"vizinhos": viz_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "selo": selo_ok, "indice": rep["indice_da_iald"]["all_verified"], "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"],
                                                                      "proib": _proib, "citacoes": _cc.returncode, "kernel_igual": not dif_kb, "escada": rep["escada"], "simular_arvore_do_nos": sim_ok, "exame_pontos": exame_ok}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)

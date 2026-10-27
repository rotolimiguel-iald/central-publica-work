# -*- coding: utf-8 -*-
"""ensaio_a_seco_v402.py -- ENSAIO A SECO da v402 (molde: ensaio_a_seco_v401.py FINAL, que rodou na cadeia da v401, com as licoes da v399, v400 e v401), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v402.py <candidato.py> <rotulo>
A v402 e' uma versao de CONTEUDO: TRES modulos novos de kernel (TGLExt/PonteDaEscalaDual, do Codex, ORDEM 025; TGLExt/QuedaSemGeometria; TGLExt/EsperancaCondicional: nomes provisorios), os registros com FUNCAO ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 e os registros por spec cunhagens_v402 e kh_n1_cobertura_v402.
A base e' a v401 SELADA (core e selo em base_v401), o kernel e' o da v401 + as tres pedras (sandbox C:/t/k402c); os registros de v393 a v399 E OS DA V401 (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) sao RECRIADOS e comparados com os da v401 selada
(os rotulos 'v401' dos nomes de relatorio herdados da subida de versao significam a base selada). Etapas:
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v402; (3) o core da v401 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: iguais, ou a TROCA DITA (so' numeros: a escada e a cobertura crescem com as pedras); (5) o FLUXO PRINCIPAL v393 a v399, v401 e v402 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as cinco da v402;
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os TRES registros com funcao da v402 (cada elo recusa), os registros por spec, a cobertura, o sidecar;
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, a secao v402 (antes da v401) e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos;
(13) [LICAO DA v400, mantida] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v402 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402   # (copia do quadro da v397, intocada pela v401 e pela v402)
NOS = DL.NOS
BASE = os.path.join(HERE, DL.BASE_DIR); CORE0P = os.path.join(BASE, "um_absoluto.json"); SELO0P = os.path.join(BASE, "um_absoluto_selo.json")   # a v401 SELADA (copia de bytes; identica ao Nos antes da instalacao)
KB = DL.SANDBOX
KD = os.path.join(HERE, DL.KERNEL_DIR)
cand = sys.argv[1] if len(sys.argv) > 1 else DL.CANDIDATO; rot = sys.argv[2] if len(sys.argv) > 2 else "v402"
DRY = os.path.join(HERE, "dry_" + rot)
if os.path.isdir(DRY):
    shutil.rmtree(DRY)
os.makedirs(DRY); shutil.copyfile(os.path.join(HERE, cand), os.path.join(DRY, "um.py"))
EMB, _, _, h16 = carregar(os.path.join(DRY, "um.py"))
for rel, content in EMB.items():
    p = os.path.join(DRY, "tgl_kernel", *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="").write(content)
# a pasta do Nos tem arquivos que NAO estao embutidos (hoje: _check_damming.lean; ExtrairDeps.lean sai do hash por exclusao nominal) e o hash formal do RITO os conta: a arvore do ensaio os recebe como estao (so' leitura do Nos)
NOSK = os.path.join(NOS, "tgl_kernel"); EXTRAS_NOS = []
for dp_, dn_, fn_ in os.walk(NOSK):
    if ".lake" in dp_.replace("\\", "/").split("/"):
        continue
    for nm_ in fn_:
        if nm_.endswith(".lean") or nm_ in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel_ = os.path.relpath(os.path.join(dp_, nm_), NOSK).replace("\\", "/")
            if rel_ not in EMB:
                EXTRAS_NOS.append(rel_); d_ = os.path.join(DRY, "tgl_kernel", *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True); shutil.copyfile(os.path.join(dp_, nm_), d_)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v402.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"residuais_do_nos_na_arvore_do_ensaio": EXTRAS_NOS, "candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SEM_GPU_SEM_RITO": "o core da v401 selada + o kernel REAL lido pelo verify com os logs crus do sandbox"}
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
assert um.UM_VERSION == "v402"
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
selo0 = json.load(open(SELO0P, encoding="utf-8"))
assert "teste_de_veracidade_fase9_v397" in core0 and "sonico_v398" in core0 and "afinacao_das_cordas_v398" in core0 and "selo_pela_propria_tecnologia_v399" in core0 and "declaracao_do_operador_v399" in core0 and "cunhagens_v399" in core0 and "kh_n1_cobertura_v399" in core0 and selo0["um_version"] == "v401"
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
                                      "chaves_do_kf_da_v401_que_o_verify_nao_devolve": chaves_antigas_ausentes[:10], "proveniencia": _ovf.get("declaration_sources_status_v394")}
print("verify real:", _ovf["verdict"][:80], _ovf["all_verified"], rep["verify_kernel_ponta_a_ponta"]["cobertura"].get("decl"), "nao lidas:", rep["verify_kernel_ponta_a_ponta"]["cobertura"].get("nao_lidas_pelo_regex"))
ESP = CM["escada"][1]
# a escada: SEM as bandeiras novas (o kf da v401) a escada do candidato NAO fecha
_el0 = um.prove_external_ladder(1.0, core0["kernel_formalization"])
rep["escada_sem_as_bandeiras_novas"] = [_el0.get("n_theorems_clean"), _el0.get("n_theorems_expected"), _el0.get("all_verified")]
E401 = int(core0["external_ladder"]["n_theorems_expected"])   # LIDO do core da v401 selada (nada digitado)
assert rep["escada_sem_as_bandeiras_novas"][0] == E401 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True and ESP == E401 + CM["n_bandeiras"], rep["escada_sem_as_bandeiras_novas"]
_el = um.prove_external_ladder(1.0, kf); core_s["external_ladder"] = _el
rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]; rep["escada_esperada"] = ESP; print("escada recomputada:", rep["escada"], "esperada:", ESP)
# (4) os vizinhos RECOMPUTADOS (a ordem do rito): a TROCA DITA (so' numeros) ou fica IGUAL
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
cs2 = copy.deepcopy(core_s); mud = {}; iguais_v = []; restauradas_contagens = []


def recomputa(nome, fn):
    novo = fn(cs2); cs2[nome] = novo
    a, b = str((core0.get(nome) or {}).get("verdict") or ""), str(novo.get("verdict") or "")
    if a == b:
        iguais_v.append(nome)
    else:
        mud[nome] = {"antes": a, "depois": b, "so_numeros": _num(a) == _num(b), "all_verified": novo.get("all_verified")}


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
        mud[n_] = {"antes": a, "depois": b, "so_numeros": _num(a) == _num(b), "all_verified": (cs2.get(n_) or {}).get("all_verified")}
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
for n_, d_ in list(mud.items()):
    if _nc(d_["antes"]) == _nc(d_["depois"]):
        mud.pop(n_); iguais_v.append(n_ + "(contagens CORE_n_ normalizadas)"); cs2[n_] = copy.deepcopy(core0[n_]); restauradas_contagens.append(n_)   # o rito computa este registro no ponto do main (o valor da v401 selada: o main e' o mesmo); o ensaio o recomputa sobre o core inteiro: so' as CONTAGENS diferem
# [v400] a UNICA troca esperada: o veredito do estatuto da prova (v391) carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash): o do candidato no lugar do da v401; so' isso (e as contagens CORE_n_, normalizadas acima) pode mudar
_HA, _HD = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest(), hashlib.sha256(open(os.path.join(DRY, "um.py"), "rb").read()).hexdigest()
troca_esperada = {}
for n_, d_ in list(mud.items()):
    if n_ == "estatuto_da_prova_v391" and d_.get("all_verified") is True and d_["antes"] != d_["depois"] and _nc(d_["antes"]).replace(_HA[:16], _HD[:16]) == _nc(d_["depois"]):
        troca_esperada[n_] = mud.pop(n_)
for d_ in mud.values():   # o relatorio guarda so' o comeco; a comparacao acima foi sobre a string INTEIRA
    d_["antes"], d_["depois"] = d_["antes"][:300], d_["depois"][:300]
N401 = len(core0["kernel_formalization"]["axiom_report"])
NUMS = ["KERNEL_%d_OF_%d" % (E401, E401), "%d_OF_%d_DECLARATIONS" % (N401, N401), "LADDER_%d_OF_%d" % (E401, E401)]
m_sc = re.search(r"SCAN_(\d+)_FILES", str((core0.get("varredura_e_sorry_v392") or {}).get("verdict") or ""))
if m_sc:
    NUMS.append("SCAN_%s_FILES" % m_sc.group(1))
carregam = sorted(k for k, m in core0.items() if isinstance(m, dict) and any(n in str(m.get("verdict") or "") for n in NUMS))
rep["vizinhos"] = {"recomputados_iguais": iguais_v, "mudaram": mud, "troca_esperada_so_o_hash_proprio": troca_esperada, "contagens_do_instante_restauradas_ao_da_v401": restauradas_contagens, "carregam_os_numeros_do_kernel_no_core0": carregam, "carregam_e_nao_recomputados_ainda": sorted(set(carregam) - set(mud) - set(iguais_v))}
core_s = cs2
# (5) o fluxo principal: as instrucoes etiquetadas v393, v394, v395, v396, v397, v401 e v402 do main (a ordem do arquivo)
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v393" in l or "v394" in l or "v395" in l or "v396" in l or "v397" in l or "v398" in l or "v399" in l or "v401" in l or "v402" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
V393N = ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393"]
V394N = ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS)
V395N = ["psibit_v395"] + list(um._V395_NOMES_REGISTROS)
V396N = ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS)
V397N = ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS)
V398N = ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS)
V401N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)   # (os registros das v399 e v401, recriados e comparados com os da v401 selada; o rotulo V401N e' herdado da subida de versao)
V402N = ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS)   # os registros NOVOS da v402 (nao existem no core da base)
for _k in V393N + V394N + V395N + V396N + V397N + V398N + V401N + V402N:
    core_s.pop(_k, None)   # o fluxo os recria; comparam-se depois com os da v401 selada
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v393+v394+v395+v396+v397+v398+v399+v402>", "exec"), ns); _err = None
except Exception as e:  # noqa
    import traceback; _err = repr(e) + traceback.format_exc()[-800:]
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]
NOVAS402 = sorted(V402N)   # a v402 cria CINCO chaves no core (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402, cunhagens_v402, kh_n1_cobertura_v402); os registros das v399 e v401 sao RECRIADOS e comparados com os da v401 selada
novas_chaves = sorted(k for k in c if k not in core0)
tv0 = c.get("teste_de_veracidade_fase9_v397") or {}
recriados = {k: {"igual_ao_selado": str((c.get(k) or {}).get("verdict")) == str((core0.get(k) or {}).get("verdict")), "all_verified": (c.get(k) or {}).get("all_verified"), "antes": str((core0.get(k) or {}).get("verdict")), "depois": str((c.get(k) or {}).get("verdict"))} for k in V393N + V394N + V395N + V396N + V397N + V398N + V401N}   # (os de V402N sao novos: nao ha o que comparar)
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": novas_chaves, "stdout": _mf.strip().splitlines(),
                   "veracidade": {x: tv0.get(x) for x in ("verdict", "all_verified", "lido", "does_not_gate_core")}, "veracidade_n_checks": len(tv0.get("checks") or []), "veracidade_checks_falhos": [ck_["descricao"] for ck_ in (tv0.get("checks") or []) if not ck_.get("ok")],
                   "veracidade_fontes": [{"chave": f_["chave"], "sha256": f_["sha256"], "ok": f_["ok"]} for f_ in (tv0.get("fontes") or [])],
                   "registros_v397": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V397_NOMES_REGISTROS}, "registros_v398": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V398_NOMES_REGISTROS}, "sonico_v398": {x: (c.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified", "beta_ok")}, "afinacao_das_cordas_v398": {x: (c.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v399": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V399_NOMES_REGISTROS}, "selo_pela_propria_tecnologia_v399": {x: (c.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified")}, "declaracao_do_operador_v399": {x: (c.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified")}, "recriados_v393_a_v401": recriados, "registros_novos_v402": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V402N},
                   "registros_v401": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)},
                   "checks_dos_registros_que_falharam": {n_: [ck_ for ck_ in ((c.get(n_) or {}).get("checks") or []) if not ck_.get("ok")][:6] for n_ in list(um._V399_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + um._V397_NOMES_REGISTROS + um._V396_NOMES_REGISTROS + um._V395_NOMES_REGISTROS + um._V394_NOMES_REGISTROS + list(um._V393_NOMES_REGISTROS) if (c.get(n_) or {}).get("all_verified") is not True}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k not in ("stdout", "recriados_v393_a_v401", "veracidade")}, ensure_ascii=False, default=str)[:3800])
for k_, d_ in list(recriados.items()):
    if not d_["igual_ao_selado"] and _num(d_["antes"]) == _num(d_["depois"]) and d_["all_verified"] is True:
        mud[k_] = {"antes": d_["antes"], "depois": d_["depois"], "so_numeros": True, "all_verified": True}
rec_ok = all(d_["all_verified"] is True and (d_["igual_ao_selado"] or k_ in mud) for k_, d_ in recriados.items())
_nomes_v = list(mud) + [x.split("(")[0] for x in iguais_v]
_falham_v = [n_ for n_ in _nomes_v if n_ in cs2 and (cs2.get(n_) or {}).get("all_verified") is not True]
_ausentes_v = [n_ for n_ in _nomes_v if n_ not in cs2]
viz_ok = (all(v["so_numeros"] and v["all_verified"] is True for v in mud.values()) and rec_ok and not _falham_v)
rep["viz_det"] = {"mud_so_numeros_e_selados": all(v["so_numeros"] and v["all_verified"] is True for v in mud.values()), "v393_a_v401_recriados_ok": rec_ok, "nao_selados": _falham_v, "ausentes_do_core": _ausentes_v[:10]}
mf_ok = (not _err and novas_chaves == sorted(NOVAS402) and tv0.get("all_verified") is True and all((c.get(n_) or {}).get("all_verified") is True for n_ in list(um._V397_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + list(um._V399_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + V401N + V402N)
         and (c.get("testemunha_estatica_v396") or {}).get("all_verified") is True and (c.get("psibit_v395") or {}).get("all_verified") is True and (c.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is False
         and "ADMITTED" in str(((c.get("regra_consumidor_v393") or {}).get("satisfacao") or {}).get("veredito_do_rito")))
# (6) unidade
U = {}
EMBK = um._EMBEDDED_KERNEL_FILES
cs = lambda: copy.deepcopy(core_s)
VER = um._V397_VERACIDADE_SPEC
RES_P = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RES_P, encoding="utf-8"))
RUN_V = lambda c_: um._v392_registro(VER, c_)
guarda_txt = lambda r_: um._v392_guarda_texto(json.dumps({k_: r_.get(k_) for k_ in ("limites", "diz", "nao_diz", "leituras_do_operador", "erratas", "extras")}, ensure_ascii=False)) + um._v392_guarda_texto(str(r_.get("verdict")))


def com_fonte_alterada(chave, mutador, repin=True):
    """Cria uma copia ADULTERADA do JSON pinado em `chave`, repina sha256/bytes/arquivo em _V392_FONTES (o ataque mais forte: o hash NAO acusa) e roda o registro; restaura no fim."""
    f0 = dict(um._V392_FONTES[chave]); d = json.loads(rd(f0["arquivo"]).decode("utf-8")); mutador(d)
    nb = json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8"); td = tempfile.mkdtemp(prefix="v402_ens_"); p = os.path.join(td, os.path.basename(f0["arquivo"])); open(p, "wb").write(nb)
    um._V392_FONTES[chave] = dict(f0, arquivo=p, sha256=hashlib.sha256(nb).hexdigest() if repin else f0["sha256"], bytes=len(nb) if repin else f0["bytes"])
    try:
        return RUN_V(cs())
    finally:
        um._V392_FONTES[chave] = f0; shutil.rmtree(td, ignore_errors=True)


def mult(d, caminho, f):
    cur = d
    for k in caminho[:-1]:
        cur = cur[k]
    cur[caminho[-1]] = cur[caminho[-1]] * f


_r = RUN_V(cs())
U["veracidade_tudo_certo"] = bool(_r["all_verified"] is True and _r["verdict"].startswith("TGL_FASE9_VERACIDADE_V397__THE_UNIQUE_WORD_TEST_OPENED_ONCE_READ_BY_HASH") and _r.get("does_not_gate_core") is True and len(_r["checks"]) == len(VER["checks"])
                                  and all(_r["lido"].get(k_) == DL.lido(res9, c_) for k_, c_ in DL.F9_CAMINHOS.items()))
U["veracidade_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(_r))
U["veracidade_z_disc_abaixo_de_5_e_poder_acima_de_5_nos_numeros_lidos"] = bool(_r["lido"]["z_disc_calibrado"] < 5.0 < _r["lido"]["poder_previo"] and _r["lido"]["lnB_lcdm"] > _r["lido"]["lnB_beta_livre"] > 0)
U["veracidade_diz_que_a_discriminacao_a_5_sigma_nao_foi_alcancada_e_nao_cego"] = bool("BELOW_5SIGMA_NOT_DISCRIMINATED" in _r["verdict"] and "NOT_BLIND_TO_DATA_STATED" in _r["verdict"] and "NOT_BLIND_TO_DATA_STATED" in str(_r["lido"].get("f9_veredito")))
for _ch in ("f9v2_resultado", "f9v2_congelamento", "f9v2_abertura", "f9v2_consumida"):
    _a0 = dict(um._V392_FONTES[_ch]); um._V392_FONTES[_ch] = dict(_a0, sha256="0" * 64)
    try:
        _r1 = RUN_V(cs())
    finally:
        um._V392_FONTES[_ch] = dict(_a0)
    U["veracidade_sha_errado_de_%s_recusa" % _ch] = bool(_r1["all_verified"] is False and ("FONTE_" + _ch) in _r1["verdict"])
    um._V392_FONTES[_ch] = dict(_a0, arquivo=os.path.join(DRY, "nao_existe", os.path.basename(_a0["arquivo"])))
    try:
        _r2 = RUN_V(cs())
    finally:
        um._V392_FONTES[_ch] = dict(_a0)
    U["veracidade_arquivo_ausente_de_%s_recusa" % _ch] = bool(_r2["all_verified"] is False and ("FONTE_" + _ch) in _r2["verdict"])
U["veracidade_z_disc_adulterado_com_sha_repinado_recusa"] = com_fonte_alterada("f9v2_resultado", lambda d: mult(d, DL.F9_CAMINHOS["z_disc_calibrado"], 1.0001))["all_verified"] is False
U["veracidade_z_delta_adulterado_com_sha_repinado_recusa"] = com_fonte_alterada("f9v2_resultado", lambda d: mult(d, DL.F9_CAMINHOS["z_delta_calibrado"], 1.0001))["all_verified"] is False
U["veracidade_lnB_adulterado_com_sha_repinado_recusa"] = com_fonte_alterada("f9v2_resultado", lambda d: mult(d, DL.F9_CAMINHOS["lnB_lcdm"], 1.0001))["all_verified"] is False
U["veracidade_p_adulterado_com_sha_repinado_recusa"] = com_fonte_alterada("f9v2_resultado", lambda d: mult(d, DL.F9_CAMINHOS["p_disc_unilateral"], 1.01))["all_verified"] is False
_rb = com_fonte_alterada("f9v2_resultado", lambda d: mult(d, DL.F9_CAMINHOS["beta_do_resultado"], 1.001))
U["veracidade_beta_do_resultado_adulterado_recusa"] = bool(_rb["all_verified"] is False and "CHECK_b1" in _rb["verdict"])
_a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
try:
    _ra = RUN_V(cs()); U["veracidade_alfa_do_um_adulterado_recusa"] = bool(_ra["all_verified"] is False and "CHECK_b1" in _ra["verdict"])
finally:
    um.SEALED_CODATA_ALPHA = _a0
U["veracidade_veredito_adulterado_recusa"] = com_fonte_alterada("f9v2_resultado", lambda d: d.__setitem__("veredito", d["veredito"].replace("NOT_FALSIFIED_POWERED", "FALSIFIED_AT_5SIGMA")))["all_verified"] is False
U["veracidade_cadeia_dos_recibos_pino_do_congelamento_adulterado_recusa"] = com_fonte_alterada("f9v2_resultado", lambda d: d["pinos"].__setitem__("recibo_de_congelamento_sha256", "0" * 64))["all_verified"] is False
U["veracidade_recibo_de_abertura_com_schema_adulterado_recusa"] = com_fonte_alterada("f9v2_abertura", lambda d: d.__setitem__("schema", "OUTRO"))["all_verified"] is False
U["veracidade_recibo_de_abertura_com_pino_do_congelamento_adulterado_recusa"] = com_fonte_alterada("f9v2_abertura", lambda d: d.__setitem__("freeze_receipt_sha256", "0" * 64))["all_verified"] is False
U["veracidade_marcador_de_abertura_consumida_adulterado_recusa"] = com_fonte_alterada("f9v2_consumida", lambda d: d.__setitem__("recibo_de_abertura_sha256", "0" * 64))["all_verified"] is False
for _ch in (CH_ for CH_ in VER["verbatins"]):
    _ant = um._V397_VERBATINS2[_ch]["text"]; um._V397_VERBATINS2[_ch]["text"] += " "   # [v402-patch-b] restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
    try:
        _rv = RUN_V(cs()); U["veracidade_fala_adulterada_" + _ch[-16:]] = bool(_rv["all_verified"] is False and _rv["verbatim"][_ch]["embedded_ok"] is False)
    finally:
        um._V397_VERBATINS2[_ch]["text"] = _ant
# o QUADRO: regra da ordem (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO item); frase VERBATIM; "NAO selou" quando o registro nao sela
_tv = copy.deepcopy(c["teste_de_veracidade_fase9_v397"])
for _lang in ("pt", "en"):
    _tex = "\n".join(um._v397_quadro_tex(_tv, _lang)); _its = [x for x in re.split(r"\\item ", _tex)[1:]]
    _a = QV.esperados(res9, _lang)[0]
    U["quadro_tex_%s_regra_da_ordem_e_frase_verbatim" % _lang] = bool(not QV._regra_da_ordem(_its, QV.normaliza(_a["z_disc"]["tex"]), _lang) and len(_its) == 5 and um._V397_FRASE_444 in _tex and ("NÃO selou" not in _tex and "did NOT seal" not in _tex))
_md = "\n".join(um._v397_quadro_md(_tv)); _its = re.split(r"(?m)^>\s*-\s+", _md)[1:]
U["quadro_md_regra_da_ordem_e_frase_verbatim"] = bool(not QV._regra_da_ordem(_its, QV.normaliza(QV.esperados(res9, "pt")[0]["z_disc"]["md"]), "pt") and len(_its) == 5 and um._V397_FRASE_444 in _md and QV.paragrafo_pronto_readme(_tv).count("> - ") == 5)
_ts = copy.deepcopy(_tv); _ts["all_verified"] = False
U["quadro_registro_nao_selado_diz_que_nao_selou"] = bool("NÃO selou" in "\n".join(um._v397_quadro_tex(_ts, "pt")) and "did NOT seal" in "\n".join(um._v397_quadro_tex(_ts, "en")) and "NÃO selou" in "\n".join(um._v397_quadro_md(_ts)))
_tn = {"all_verified": False, "lido": {}, "fontes": []}
U["quadro_sem_numeros_mostra_n_d_e_nao_levanta"] = bool("n/d" in "\n".join(um._v397_quadro_tex(_tn, "pt")) and "n/a" in "\n".join(um._v397_quadro_tex(_tn, "en")) and "n/d" in "\n".join(um._v397_quadro_md(_tn)))
rep["veracidade_registro"] = {"verdict": _r["verdict"], "all_verified": _r["all_verified"], "n_checks": len(_r["checks"]), "lido": _r["lido"], "fontes": [{"chave": f_["chave"], "sha256": f_["sha256"], "ok": f_["ok"]} for f_ in _r["fontes"]]}
# (6c) [v398] os DOIS registros com FUNCAO: tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos)
import math as _math
from fractions import Fraction as _Fr
_FN = {"sonico": um.sonico_v398, "afinacao": um.afinacao_das_cordas_v398}
_CT = {"sonico": um._V398_SONICO_CONTRACT, "afinacao": um._V398_AFINACAO_CONTRACT}
_TX = {"sonico": um._V398_SONICO_TEXT, "afinacao": um._V398_AFINACAO_TEXT}
_GUARDA98 = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
RF = {}
for k_ in ("sonico", "afinacao"):
    fn_, ct_, tx_ = _FN[k_], _CT[k_], _TX[k_]
    r_ = fn_(cs()); RF[k_] = r_
    U[k_ + "_tudo_certo"] = bool(r_["all_verified"] is True and r_["verdict"] == tx_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] >= 7
                                 and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values()) and all(r_["inscriptions"].values()))
    U[k_ + "_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in ct_["theorems"].items():   # bandeira falsa de CADA teorema do contrato
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U[k_ + "_bandeira_falsa_de_cada_teorema_do_contrato_recusa"] = bool(ok_)
    ok_ = True
    for th_ in list(ct_["theorems"]) + list(ct_["support"]) + list(ct_["cited_outside"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U[k_ + "_axioma_fora_do_trio_em_cada_termo_lido_recusa"] = bool(ok_)
    ok_ = True
    for th_ in [ct_["unconditional"]["theorem"]] + list(ct_["support"]):   # proveniencia errada (o compilador diz outro modulo)
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U[k_ + "_proveniencia_errada_recusa"] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][ct_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[ct_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U[k_ + "_fonte_da_pedra_adulterada_recusa"] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U[k_ + "_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in ct_["verbatins"]:
        _ant = um._V398_VERBATINS2[ch_]["text"]; um._V398_VERBATINS2[ch_]["text"] += " "   # [v402-patch-b] restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V398_VERBATINS2[ch_]["text"] = _ant
    U[k_ + "_inscricao_adulterada_recusa"] = bool(ok_)
# o SONICO: beta e numero adulterado
_rs = RF["sonico"]; _v = _rs["values"]
_b = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e); _th = _math.asin(_math.sqrt(_b)); _c2 = _math.cos(_th) ** 2; _s2 = _math.sin(_th) ** 2; _hn = -(_c2 * _math.log(_c2) + _s2 * _math.log(_s2))
U["sonico_numeros_recalculados_aqui"] = bool(abs(_v["beta"] - _b) <= 1e-15 and abs(_v["theta_M_rad"] - _th) <= 1e-15 and abs(_v["collapse_entropy_theta_M_nats"] - _hn) <= 1e-15 and abs(_v["collapse_entropy_theta_M_octaves"] - _hn / _math.log(2.0)) <= 1e-15
                                  and 0.0 < _hn < _math.log(2.0) and abs(_v["ln2"] - _math.log(2.0)) == 0.0 and abs(_v["exp_ln2"] - 2.0) <= 1e-15 and abs(_v["fair_bit_entropy"] - _math.log(2.0)) <= 1e-15 and _v["pin_minus_half_nat"] > 0.19)
c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = um.sonico_v398(c_)
_a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
try:
    _ra = um.sonico_v398(cs())
finally:
    um.SEALED_CODATA_ALPHA = _a0
U["sonico_beta_adulterado_recusa"] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
_h20 = um._v398_h2; um._v398_h2 = lambda p_: _h20(p_) * 1.001
try:
    _rn = um.sonico_v398(cs())
finally:
    um._v398_h2 = _h20
U["sonico_numero_adulterado_recusa"] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
# a AFINACAO: a aritmetica recalculada aqui por outro caminho, a hipotese e a geometria ditas, o kappa do core, e o numero adulterado
_ra_ = RF["afinacao"]; _w = _ra_["values"]
U["afinacao_aritmetica_recalculada_aqui"] = bool(_w["zeta_minus_one"] == str(_Fr(-1, 12)) and _w["hurwitz_zeta_minus_one_half"] == str(_Fr(1, 24)) and _w["bosonic_critical_dimension"] == 26 and _w["superstring_critical_dimension"] == 10 and _w["wrong_fermion_sign_dimension"] == 26
                                                 and _w["house_spatial_dimension"] == 9 and _w["boson_direction"] == str(_Fr(-1, 24)) and _w["ns_fermion_direction"] == str(_Fr(-1, 48)) and _w["ns_direction_sum"] == str(_Fr(-1, 16))
                                                 and [d_ for d_ in range(200) if _Fr(-(d_ - 2), 24) == -1] == [26] and [d_ for d_ in range(200) if _Fr(-(d_ - 2), 16) == _Fr(-1, 2)] == [10])
U["afinacao_hipotese_geometria_e_kappa_ditos"] = bool((_ra_["hypothesis"] == {"name": "MasslessFirstLevel", "status": "KNOWN", "named_not_proved": True}) and _ra_["geometry"] == "OPEN" and _ra_["derives_strings_from_the_axiom"] is False and _w["kappa_from_core"] is None
                                                      and "kappa_is_input" in " ".join(_ra_["limites"]) and "MasslessFirstLevel" in _ra_["estatuto"] and "[KNOWN]" in _ra_["estatuto"] and "[OPEN]" in _ra_["estatuto"] and "nada aqui deriva a teoria das cordas do axioma" in " ".join(_ra_["limites"])
                                                      and len(_ra_["auxiliaries_outside_the_composition"]) == 5 and all(_ra_["auxiliaries_outside_the_composition"].values()))
_bn0 = um._v398_bernoulli
def _bern_ruim(n_):
    b_ = _bn0(n_); b_[2] = _Fr(1, 5); return b_
um._v398_bernoulli = _bern_ruim
try:
    _rz = um.afinacao_das_cordas_v398(cs())
finally:
    um._v398_bernoulli = _bn0
U["afinacao_numero_adulterado_recusa"] = bool(_rz["all_verified"] is False and "ARITHMETIC_CHECK_FAILED" in _rz["verdict"] and any(not ck_["ok"] for ck_ in _rz["mechanics"]["checks"]))
rep["sonico_registro"] = {"verdict": RF["sonico"]["verdict"], "all_verified": RF["sonico"]["all_verified"], "n_checks": RF["sonico"]["mechanics"]["n_checks"], "values": RF["sonico"]["values"], "unconditional": RF["sonico"]["unconditional"]}
rep["afinacao_registro"] = {"verdict": RF["afinacao"]["verdict"], "all_verified": RF["afinacao"]["all_verified"], "n_checks": RF["afinacao"]["mechanics"]["n_checks"], "values": RF["afinacao"]["values"], "unconditional": RF["afinacao"]["unconditional"],
                            "hypothesis": RF["afinacao"]["hypothesis"], "geometry": RF["afinacao"]["geometry"]}
# (6d) [v399] os DOIS registros com FUNCAO da v402 (selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399): tudo certo, o round trip RECALCULADO aqui por outro caminho, a direcao do testemunho, e cada elo recusa visivelmente (controles negativos)
import time as _tm, tempfile as _tf, numpy as _np
import acom_conferencias_v402 as AC  # noqa: E402
_UMB = open(os.path.join(DRY, "um.py"), "rb").read(); _UMH = hashlib.sha256(_UMB).hexdigest()
_t0 = _tm.perf_counter(); r9s = um.selo_acom_v399(cs()); t_selo9 = _tm.perf_counter() - _t0
_s9 = r9s["selo"]; _a9 = _s9["acom"]; _ct9 = r9s["controles_negativos"]
U["selo_acom_tudo_certo"] = bool(r9s["all_verified"] is True and r9s["verdict"].startswith("TGL_SELO_PELA_PROPRIA_TECNOLOGIA_V399__") and r9s["does_not_gate_core"] is True and r9s["values"]["perfil"] == "ACOM-INT-C96-Q8" and _ct9["n_controles"] == 13 and _ct9["todos_recusados"] is True
                                and _s9["sha256"] == _UMH and _s9["bytes"] == len(_UMB) and _a9["prova_de_reconstrucao"]["igual_ao_objeto_byte_a_byte"] is True and _a9["prova_de_reconstrucao"]["bytes_divergentes"] == 0 and len(r9s["checks"]) == 6 and all(v_ for _, v_ in r9s["checks"]))
# o round trip RECALCULADO aqui, so' das tres partes cruas (a formula da Dobra + o arredondamento ao reticulado inteiro + o centro), sem as funcoes de reconstrucao do selo
_sl, _pp = um.selar(_UMB, "um.py", devolver_partes=True); _kp = _sl["acom"]["kappa"]["campos"]; _n9 = _kp["n_elements"]; _m9 = _kp["m_max_abs"]
_st9 = um._unpack2bits(_pp["psi_raw"], _n9); _th9 = _np.frombuffer(_pp["theta_raw"], dtype=_np.uint8)
_real9 = (_math.sqrt(_m9) * _np.sin(_th9.astype(_np.float64) / 255 * (_math.pi / 2))) ** 2
_rec9 = (_np.where(_st9 >= 2, -1, 1) * _np.rint(_real9).astype(_np.int64) + 96).astype(_np.uint8).tobytes()
U["selo_acom_round_trip_recalculado_aqui_so_das_tres_partes_cruas"] = bool(_rec9 == _UMB and _sl["acom"]["psi"]["sha256"] == _a9["psi"]["sha256"] and _sl["acom"]["theta"]["sha256"] == _a9["theta"]["sha256"] and _sl["acom"]["kappa"]["sha256"] == _a9["kappa"]["sha256"])
_erro_dobra9 = float(_np.abs(_real9 - _np.abs(_np.frombuffer(_UMB, dtype=_np.uint8).astype(_np.int64) - 96)).max())
U["selo_acom_dobra_pura_nao_e_exata_e_o_rint_e_dito"] = bool(0.0 < _erro_dobra9 < 0.5 and "rint" in _a9["prova_de_reconstrucao"]["metodo"] and "NAO e' da patente" in " ".join(r9s["statuses"].values()))
del _real9, _rec9, _st9, _th9
U["selo_acom_orcamento_de_tempo"] = bool(t_selo9 <= 10.0)   # medido ~1,4 s com os 13 controles; o limite folgado evita falso negativo em maquina ocupada
U["selo_acom_os_13_controles_recusados_na_ordem"] = bool([c_["id"] for c_ in _ct9["controles"]] == ["N%d" % i_ for i_ in range(1, 14)] and all(c_["ok"] and c_["obtido"].startswith("RECUSOU:") for c_ in _ct9["controles"])
                                                         and any("A_SEGUNDA_TESTEMUNHA_DETECTA_SOZINHA" in c_["obtido"] for c_ in _ct9["controles"] if c_["id"] == "N9") and next(c_.get("sem_hash_a_reconstrucao_nao_muda") for c_ in _ct9["controles"] if c_["id"] == "N5") is True)
_txt9 = json.dumps({k_: r9s.get(k_) for k_ in ("theorem", "direcao_do_testemunho", "statuses", "verdict")}, ensure_ascii=False)
U["selo_acom_textos_sem_palavra_proibida_e_sem_alegar_confidencialidade"] = bool(not um._v392_guarda_texto(_txt9) and not _GUARDA98.search(r9s["verdict"]) and "NAO alegada" in r9s["statuses"]["confidencialidade"] and not re.search(r"(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)", _txt9))
U["selo_acom_direcao_do_testemunho_dita"] = bool("o operador testifica DA IALD" in r9s["direcao_do_testemunho"] and "a IALD nao testifica do operador" in r9s["direcao_do_testemunho"] and "Jo 8,18" in r9s["direcao_do_testemunho"])
# [v402, BAIXA B1 do exame da v401] a checagem «beta do runtime» NAO e' mais tautologica: confronta com o beta do CORE do rito (que o main calcula por outro caminho) a 1e-9
_vb = r9s["values"]; _b_core = cs()["beta"]
U["selo_acom_beta_confronta_com_o_beta_do_core_a_1e_9"] = bool(_vb["beta_core"] == _b_core and _vb["rel_beta_vs_core"] is not None and _vb["rel_beta_vs_core"] < 1e-9 and r9s["checks"][5][0].startswith("beta do runtime (jamais literal) == o beta do core do rito") and r9s["checks"][5][1] is True)
_c1 = cs(); _c1["beta"] = _c1["beta"] * (1 + 1e-6); _rbc = um.selo_acom_v399(_c1)
U["selo_acom_beta_do_core_diferente_recusa"] = bool(_rbc["all_verified"] is False and _rbc["checks"][5][1] is False and _rbc["verdict"].endswith("_NOT_SEALED_THIS_RUN") and all(v_ for _, v_ in _rbc["checks"][:5]))
_c2 = cs(); _c2.pop("beta"); _rbs = um.selo_acom_v399(_c2)
U["selo_acom_sem_o_beta_do_core_recusa_fail_closed"] = bool(_rbs["all_verified"] is False and _rbs["checks"][5][1] is False)
_a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
try:
    _rba = um.selo_acom_v399(cs())
finally:
    um.SEALED_CODATA_ALPHA = _a0
U["selo_acom_alfa_do_programa_adulterado_agora_e_pego_pela_checagem_do_beta"] = bool(_rba["all_verified"] is False and _rba["checks"][5][1] is False)   # com a checagem tautologica da v401 isto NAO seria pego
_RXB = AC.regexes_da_bancada(os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"); _txt_um = _UMB.decode("utf-8")
U["alfa_unico_no_programa_a_secao_nao_redeclara_e_le_o_do_programa"] = bool("ALPHA_FINE_CODATA_2018" not in vars(um) and hasattr(um, "SEALED_CODATA_ALPHA") and len(_RXB["RE_ALPHA_LINHAS"].findall(_txt_um)) == 1 and not _RXB["RE_ALPHA_INDENTADA"].search(_txt_um)
                                                                          and len(_RXB["RE_VERSAO_LINHAS"].findall(_txt_um)) == 1 and not _RXB["RE_VERSAO_INDENTADA"].search(_txt_um) and um._beta_runtime() == um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e))
# controles negativos do registro do selo: SHA-256 do codigo diferente; bloco embutido adulterado; a recusa so' REGISTRA (e o rito nao cai)
_rr = um.registro_core_v399(_UMB[:300000], sha256_do_codigo="0" * 64, amostra=1 << 16)
U["selo_acom_sha256_do_codigo_diferente_recusa"] = bool(_rr["all_verified"] is False and _rr["verdict"].endswith("_NOT_SEALED_THIS_RUN") and any((not v_) for _, v_ in _rr["checks"]))
_ap0 = um.ACOM_PROVENIENCIA["bloco_embutido_sha256"]; um.ACOM_PROVENIENCIA["bloco_embutido_sha256"] = "0" * 64
try:
    _rb = um.registro_core_v399(_UMB[:300000], amostra=1 << 16); _cbe = um.conferir_bloco_embutido()
finally:
    um.ACOM_PROVENIENCIA["bloco_embutido_sha256"] = _ap0
U["selo_acom_bloco_embutido_adulterado_recusa"] = bool(_rb["all_verified"] is False and _cbe["confere"] is False)
_sel0 = um.selar


def _selar_recusa(*a_, **k_):
    raise um.SeloRecusado("RECONSTRUCAO_DIVERGE")


um.selar = _selar_recusa
try:
    _rz = um.selo_acom_v399(cs()); _sc0 = um.sidecar([("x", b"abc" * 100)], quem="ensaio")
finally:
    um.selar = _sel0
U["selo_acom_recusa_so_registra_e_nao_derruba"] = bool(_rz["all_verified"] is False and _rz["selo"] is None and _rz["erro"] and _rz["verdict"].endswith("_NOT_SEALED_THIS_RUN") and _sc0["recusas"] and "REFUSED" in _sc0["veredito"] and not _sc0["objetos"])
_ns_stmts = [st_ for st_ in main.body if isinstance(st_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id in ("_not_sealed", "_recusas", "_formais", "_computacao") for t_ in st_.targets)]
_gns = dict(vars(um)); _gns["core"] = dict(cs(), selo_pela_propria_tecnologia_v399=_rz)
exec(compile(ast.fix_missing_locations(ast.Module(body=_ns_stmts, type_ignores=[])), "<not_sealed>", "exec"), _gns)
U["selo_acom_recusado_entra_em_not_sealed_this_run_formais"] = bool(len(_ns_stmts) >= 5 and "selo_pela_propria_tecnologia_v399" in _gns["_formais"] and "selo_pela_propria_tecnologia_v399" not in _gns["_recusas"])
# a DECLARACAO DO OPERADOR
d9 = um.declaracao_do_operador_v399(cs())
_dtxt = open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read()
U["declaracao_tudo_certo"] = bool(d9["all_verified"] is True and d9["verdict"].startswith("TGL_OPERATOR_DECLARATION_OF_24OCT_REGISTERED__") and d9["does_not_gate_core"] is True and d9["declaration"]["statement_verbatim"].encode("utf-8") == _dtxt and d9["declaration"]["verbatim_sha256"] == hashlib.sha256(_dtxt).hexdigest()
                                  and len(d9["declaration"]["kernel_anchors_REAL"]) == 10 and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] for a_ in d9["declaration"]["kernel_anchors_REAL"]) and len(d9["declaration"]["pedra_instalada"]) == 2
                                  and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] for a_ in d9["declaration"]["pedra_instalada"]) and "[DECLARACAO DO OPERADOR / INPUT]" in d9["declaration"]["status_of_statement"] and len(d9["declaration"]["not_declared"]) == 4)
_anc = [a_["termo"] for a_ in d9["declaration"]["kernel_anchors_REAL"]]; _ped = [a_["termo"] for a_ in d9["declaration"]["pedra_instalada"]]
ok_ = True
for t_ in _anc + _ped:   # ancora ou declaracao da pedra AUSENTE do axiom_report do rito: recusa
    c_ = cs(); c_["kernel_formalization"]["axiom_report"].pop(t_); rr_ = um.declaracao_do_operador_v399(c_)
    ok_ = ok_ and rr_["all_verified"] is False and rr_["verdict"].startswith("OPERATOR_DECLARATION_V399_NOT_SEALED")
U["declaracao_ancora_ou_pedra_ausente_do_kernel_recusa"] = bool(ok_)
ok_ = True
for t_ in _anc + _ped:   # axioma fora do trio em cada termo lido
    c_ = cs(); c_["kernel_formalization"]["axiom_report"][t_] = ["propext", "sorryAx"]; ok_ = ok_ and um.declaracao_do_operador_v399(c_)["all_verified"] is False
U["declaracao_axioma_fora_do_trio_em_cada_termo_recusa"] = bool(ok_)
_t0_ = um._V399_DECLARACAO_TXT; um._V399_DECLARACAO_TXT = _t0_ + " "
try:
    rr_ = um.declaracao_do_operador_v399(cs())
finally:
    um._V399_DECLARACAO_TXT = _t0_
_s0_ = um._V399_DECLARACAO_SHA256; um._V399_DECLARACAO_SHA256 = "0" * 64
try:
    rr2_ = um.declaracao_do_operador_v399(cs())
finally:
    um._V399_DECLARACAO_SHA256 = _s0_
U["declaracao_fala_adulterada_ou_sha256_pinado_errado_recusa"] = bool(rr_["all_verified"] is False and rr2_["all_verified"] is False)
_f0_ = um.__file__; _tmpf_ = os.path.join(DRY, "sem_trava.txt"); open(_tmpf_, "w", encoding="utf-8").write("nada aqui\n"); um.__file__ = _tmpf_
try:
    rr3_ = um.declaracao_do_operador_v399(cs())
finally:
    um.__file__ = _f0_
U["declaracao_sem_a_trava_EXECUTION_LOCKED_NOT_ONE_recusa"] = bool(rr3_["all_verified"] is False)
_txtd = json.dumps({k_: d9.get(k_) for k_ in ("declaration", "statuses", "verdict")}, ensure_ascii=False)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")


def _tem_inversao(txt_):
    """a IALD no papel de quem testifica DO operador, fora da citacao em que ele a RECUSA («eu nao podia dizer que IALD testifica a mim»)."""
    for m_ in _RX_INV.finditer(txt_):
        ant_ = txt_[max(0, m_.start() - 40):m_.start()].lower()
        if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
            return True
    return False


U["declaracao_texto_sem_palavra_proibida_e_sem_inverter_a_direcao"] = bool(not um._v392_guarda_texto(_txtd) and not _GUARDA98.search(d9["verdict"]) and not _tem_inversao(_txtd) and not _tem_inversao(_txt9)
                                                                          and d9["declaration"]["direcao_do_testemunho"]["a_IALD"].startswith("NAO testifica do operador") and d9["declaration"]["direcao_do_testemunho"]["o_um_py"].startswith("testifica EM HASH"))
U["declaracao_diz_o_que_nao_declara"] = bool(any("o kernel prove a declaracao" in x_ for x_ in d9["declaration"]["not_declared"]) and any("diagFlow" in x_ for x_ in d9["declaration"]["not_declared"]) and any("creditado" in x_ for x_ in d9["declaration"]["not_declared"]) and any("gate" in x_ for x_ in d9["declaration"]["not_declared"]))
_rs9 = um.resumos_do_selo_v399(dict(cs(), selo_pela_propria_tecnologia_v399=r9s, declaracao_do_operador_v399=d9))
U["selo_resumos_so_veredito_bandeira_e_hashes_sem_o_selo_acom_inteiro"] = bool(set(_rs9) == {"selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"} and _rs9["selo_pela_propria_tecnologia_v399"]["all_verified"] is True and _rs9["declaracao_do_operador_v399"]["all_verified"] is True
                                                                            and "acom" not in _rs9["selo_pela_propria_tecnologia_v399"] and _rs9["selo_pela_propria_tecnologia_v399"]["sha256_do_um_py"] == _UMH and _rs9["declaracao_do_operador_v399"]["verbatim_sha256"] == hashlib.sha256(_dtxt).hexdigest())
_blk9 = AC.extrair_bloco(open(os.path.join(DRY, "um.py"), "rb").read().decode("utf-8")); _emb9, _hemb9, _ = AC.bloco_das_fontes()
_prov9 = um.ACOM_PROVENIENCIA; _fo9 = os.path.join(DL.V400, "insumos", "acom", "fontes_operador")
_pins9 = {"acom_mirror.py": _prov9["codigo_embutido_de"][0]["sha256"], "acom_crypto.py": _prov9["codigo_embutido_de"][1]["sha256"], "Acom_v17_mirror_crypto.py": _prov9["origem_funcional_do_operador"]["sha256"], "run_tests.py": _prov9["testes_do_operador"]["sha256"], "tgl_core.py": _prov9["tgl_core"]["sha256"], "ACOM_Mirror_Crypto_PI_INPI.tex": _prov9["patentes"][1]["sha256"]}
U["C1_bloco_embutido_do_um_py_igual_ao_refeito_das_fontes_do_operador"] = bool(_blk9 == _emb9 and _hemb9 == _prov9["bloco_embutido_sha256"] and _cbe["calculado"] != "0" * 64)
U["C2_pinos_das_seis_fontes_do_operador_igual_ao_disco"] = bool(all(hashlib.sha256(open(os.path.join(_fo9, n_), "rb").read()).hexdigest() == h_ for n_, h_ in _pins9.items()))
rep["selo_acom_registro"] = {"verdict": r9s["verdict"], "all_verified": r9s["all_verified"], "perfil": r9s["values"]["perfil"], "bloco_embutido_sha256": r9s["values"]["bloco_embutido_sha256"], "tempo_total_s": r9s["values"]["tempo_total_s"], "beta_core": r9s["values"]["beta_core"], "rel_beta_vs_core": r9s["values"]["rel_beta_vs_core"], "selagem_total_s": t_selo9, "sha256_do_um_py": _s9["sha256"], "bytes": _s9["bytes"],
                             "psi": _a9["psi"], "theta": _a9["theta"], "kappa": {"sha256": _a9["kappa"]["sha256"], "bytes": _a9["kappa"]["bytes"]}, "lut_sha256": _a9["kappa"]["campos"]["lut_sha256"], "m_max_abs": _a9["kappa"]["campos"]["m_max_abs"], "f_exp": _a9["estrutura"]["f_exp"], "entropia_dos_estados_bits": _a9["estrutura"]["entropia_dos_estados_bits"],
                             "erro_real_maximo_antes_do_rint": _a9["prova_de_reconstrucao"]["erro_real_maximo_antes_do_rint"], "erro_dobra_pura_recalculado_aqui": _erro_dobra9, "controles": [[c_["id"], c_["obtido"]] for c_ in _ct9["controles"]], "checks": [[d_, v_] for d_, v_ in r9s["checks"]], "auditoria_de_separacao": {k_: _a9["auditoria_de_separacao"][k_] for k_ in ("fracao_de_L_negativo", "psi_redundante", "basta")}}
rep["declaracao_registro"] = {"verdict": d9["verdict"], "all_verified": d9["all_verified"], "verbatim_sha256": d9["declaration"]["verbatim_sha256"], "checks": [[d_, v_] for d_, v_ in d9["checks"]], "ancoras": _anc, "pedra": _ped, "linhas_da_trava": d9["declaration"]["termos_para_a_leitura"]["EXECUTION_LOCKED_NOT_ONE"]}
# o indice qualificado: chamada REAL sobre o core do ensaio
_t0 = um.prove_the_iald_index(cs())
rep["indice_da_iald"] = {"verdict": _t0.get("verdict"), "all_verified": _t0.get("all_verified"), "fails": [str(ck[0])[:200] for ck in _t0["checks"] if not ck[1]], "n_checks": len(_t0["checks"]), "proveniencia_erros": _t0.get("proveniencia_erros", [])[:5]}
_c = cs(); _c["kernel_formalization"]["declaration_sources_v394"] = {}
U["indice_sem_proveniencia_recusa"] = um.prove_the_iald_index(_c)["all_verified"] is False
U["indice_tudo_certo"] = _t0["all_verified"] is True and str(_t0.get("verdict")).startswith("THE_IALD_INDEX_QUALIFIED_COMPILER_PROVENANCE_VERIFIED")
_ix = um.build_the_iald_index(cs())
rep["indice_da_iald"].update({"n_nomes": _ix["n_nomes"], "n_ambiguos": len(_ix["ambiguos"]), "n_ausentes": _ix["n_ausentes"], "violacoes": _ix["violacoes"][:5], "cegos_de_namespace": _ix["cegos_de_namespace"][:5], "presente_apagada": _ix["presente_apagada"][:5]})
# a cobertura KH-N1 (4 negativos) com o leitor v394
_AL = _AUD; _ax = kf["axiom_report"]
_cv_ok = um._v392_axiom_coverage(_AL, _ax)["ok"] is True
_cv_sem = um._v392_axiom_coverage(re.sub(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL.*$", "", _AL), _ax)["ok"] is False
_cv_fora = um._v392_axiom_coverage(re.sub(r"fora_do_trio=0", "fora_do_trio=1", _AL), _ax)["ok"] is False
_ax2 = dict(_ax); _ax2[next(iter(_ax2))] = ["propext", "sorryAx"]; _cv_ax = um._v392_axiom_coverage(_AL, _ax2)["ok"] is False
_ax3 = dict(_ax); _ax3.pop(next(iter(_ax3))); _cv_cego = um._v392_axiom_coverage(_AL, _ax3)["ok"] is False
U["cobertura_kh_n1_com_o_leitor_v394"] = bool(_cv_ok and _cv_sem and _cv_fora and _cv_ax and _cv_cego)
U["verify_kernel_real_com_logs_crus_do_build_e_do_audit"] = bool(_ovf["all_verified"] is True and _ovf["verdict"].startswith("TGL_KERNEL_STAGE1_VERIFIED") and _ovf["axiom_coverage_v392"]["ok"] is True and (_ovf.get("declaration_sources_status_v394") or {}).get("ok") is True)
U["controle_negativo_blob_build_mais_audit_recusa"] = bool(_blob_antigo["ok"] is False)
U["kernel_embutido_igual_ao_sandbox"] = not dif_kb
U["proveniencia_cobre_o_axiom_report"] = set(_ovf["declaration_sources_v394"]) == set(_ovf["axiom_report"])
# o GATE nao se move: recomputado com o kf novo (a bandeira nova) e o feed V11 da v401; e o qg_closure do core nao foi tocado pelo fluxo
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
# (6b) os registros por spec: cada um recusa visivelmente (fonte adulterada; verbatim adulterado; bandeira do kernel faltando; cada check negado) -- v394, v395, v396, v397, v401 e v402 (mais o spec de veracidade)
RU = {}
for sp_ in list(um._V394_SPECS) + list(um._V395_SPECS) + list(um._V396_SPECS) + [VER] + list(um._V397_SPECS) + list(um._V398_SPECS) + list(um._V399_SPECS) + list(um._V401_SPECS) + list(um._V402_SPECS):
    n_ = sp_["nome"]; r_ = {}
    ch_ = sp_["fontes"][0]; ant_ = dict(um._V392_FONTES[ch_]); um._V392_FONTES[ch_]["sha256"] = "0" * 64
    try:
        r_["fonte_adulterada"] = um._v392_registro(sp_, core_s)["all_verified"] is False
    finally:
        um._V392_FONTES[ch_] = ant_
    for vch_ in sp_.get("verbatins", []):
        ant_ = um._V392_VERBATINS2[vch_]["text"]; um._V392_VERBATINS2[vch_]["text"] += " "   # [v402-patch-b] restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            r_["verbatim_adulterado_" + vch_] = um._v392_registro(sp_, core_s)["all_verified"] is False
        finally:
            um._V392_VERBATINS2[vch_]["text"] = ant_
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
U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V394_SPECS) + len(um._V395_SPECS) + len(um._V396_SPECS) + 1 + len(um._V397_SPECS) + len(um._V398_SPECS) + len(um._V399_SPECS) + len(um._V401_SPECS) + len(um._V402_SPECS)
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
seal.update(um.resumos_do_selo_v399(c))   # v399/v402: o resumo da segunda testemunha e da declaracao do operador (a instrucao seal.update do main, que o ensaio nao executa por ser fora do fluxo etiquetado)
J_ = lambda x: json.dumps(x, sort_keys=True, default=str)
mud_selo = sorted(k for k in seal if J_(seal.get(k)) != J_(selo0.get(k)))
rep["selo"] = {"erro": _seal_err, "chaves_do_selo": len(seal), "difere_do_selo_v401": mud_selo, "teste_de_veracidade_fase9_v397_no_selo": {x: (seal.get("teste_de_veracidade_fase9_v397") or {}).get(x) for x in ("verdict", "all_verified", "lido")}, "registros_v397": seal.get("registros_v397"), "sonico_v401_no_selo": {x: (seal.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "afinacao_v401_no_selo": {x: (seal.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v398": seal.get("registros_v398"), "selo_pela_propria_tecnologia_v402_no_selo": {x: (seal.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified", "perfil", "controles_negativos")}, "declaracao_do_operador_v402_no_selo": {x: (seal.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified", "verbatim_sha256")}, "registros_v399": seal.get("registros_v399"), "falsidade_da_inercia_v402_no_selo": {x: (seal.get("falsidade_da_inercia_v401") or {}).get(x) for x in ("verdict", "all_verified", "unconditional", "key_theorem", "costless")}, "registros_v401": seal.get("registros_v401")}
print("selo: difere em", mud_selo)
_c_dump = dict(c); _c_dump["the_iald_index"] = um.prove_the_iald_index(copy.deepcopy(c))   # o main do rito poe o indice qualificado no core; o ensaio o computa a parte
json.dump({"core": _c_dump, "verdict": verdict}, open(os.path.join(DRY, "core_ensaio.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str); json.dump(seal, open(os.path.join(DRY, "selo_ensaio.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
# [v400] o que pode diferir do selo da v401 SELADA: (i) selo_pela_propria_tecnologia_v399, um_version e sha256 (os hashes do novo um.py -- o proprio proposito da versao); (ii) UMA chave que carrega o hash do proprio programa:
#   estatuto_da_prova_v391 (a certificacao pelo proprio hash: o UNICO campo que muda e' o hash do um.py, o do candidato no lugar do da v401)
_H_ANTES = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest(); _H_DEPOIS = hashlib.sha256(_UMB).hexdigest()


def _selo_explica(k_):   # [v402-patch-d]
    a_, b_ = selo0.get(k_), seal.get(k_)
    if k_ in ("estatuto_da_prova_v391", "pedras_v392", "pedras_v393", "varredura_e_sorry_v392", "three_stress_tests_v387"):
        # so' o VEREDITO muda, e so' em numeros (a escada, as declaracoes, a contagem de arquivos e de vereditos) e no hash do proprio um.py; o registro segue selado
        va, vb = str((a_ or {}).get("verdict")), str((b_ or {}).get("verdict"))
        va = va.replace(_H_ANTES, _H_DEPOIS).replace(_H_ANTES[:16], _H_DEPOIS[:16])
        return bool(va != str((a_ or {}).get("verdict")) or va != vb) and _num(_nc(va)) == _num(_nc(vb)) and (b_ or {}).get("all_verified") is True
    # o hash das fontes formais: o do kf do rito simulado (o kernel embutido do candidato + os residuais do Nos), diferente do da base porque o kernel ganhou o arquivo da pedra
    if k_ == "formal_source_hash":
        return bool(isinstance(b_, str) and len(b_) == 64 and a_ != b_ and b_ == kf.get("formal_source_hash"))
    return False


_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402") and not _selo_explica(k_))
rep["selo"]["difere_e_nao_e_so_o_esperado"] = _selo_inexplicado
selo_ok = (not _seal_err and (seal.get("teste_de_veracidade_fase9_v397") or {}).get("all_verified") is True and all(((seal.get("registros_v397") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V397_NOMES_REGISTROS)
           and (seal.get("sonico_v398") or {}).get("all_verified") is True and (seal.get("afinacao_das_cordas_v398") or {}).get("all_verified") is True and all(((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V398_NOMES_REGISTROS)
           and (seal.get("falsidade_da_inercia_v401") or {}).get("all_verified") is True and all(((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V401_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402")) and all(((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V402_NOMES_REGISTROS)
           and (seal.get("selo_pela_propria_tecnologia_v399") or {}).get("all_verified") is True and (seal.get("declaracao_do_operador_v399") or {}).get("all_verified") is True and all(((seal.get("registros_v399") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V399_NOMES_REGISTROS)
           and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and ({"selo_pela_propria_tecnologia_v399", "um_version", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402"} <= set(mud_selo) and not _selo_inexplicado)
           and all(k in selo0 for k in ("fail_closed_selftest", "rite_checkpoints", "not_sealed_this_run")))
# (6e) [v399] o SIDECAR um_absoluto_selo_acom.json sobre o core e o selo DESTE ensaio (as copias de dry): os tres objetos selados e verificados, o SHA-256 ao lado, deterministico (dois ritos seguidos), a honestidade e o tempo
_td = tempfile.mkdtemp(prefix="v402_sidecar_"); _oo = um.OUT
try:
    shutil.copyfile(os.path.join(DRY, "core_ensaio.json"), os.path.join(_td, "um_absoluto.json")); shutil.copyfile(os.path.join(DRY, "selo_ensaio.json"), os.path.join(_td, "um_absoluto_selo.json"))
    um.OUT = _td
    _t0 = _tm.perf_counter(); _sc1 = um.selo_acom_sidecar_v399(); t_side = _tm.perf_counter() - _t0
    _b1 = open(os.path.join(_td, "um_absoluto_selo_acom.json"), "rb").read()
    _sc2 = um.selo_acom_sidecar_v399(); _b2 = open(os.path.join(_td, "um_absoluto_selo_acom.json"), "rb").read()
    _sj9 = json.loads(_b1.decode("utf-8"))
    _bytes_obj = {"um.py": _UMB, "um_absoluto.json": open(os.path.join(_td, "um_absoluto.json"), "rb").read(), "um_absoluto_selo.json": open(os.path.join(_td, "um_absoluto_selo.json"), "rb").read()}
    _ver9 = {o_["nome"]: um.verificar(_bytes_obj[o_["nome"]], o_) for o_ in _sj9["objetos"]}
finally:
    um.OUT = _oo; shutil.rmtree(_td, ignore_errors=True)
U["sidecar_tres_objetos_selados_e_verificados_com_o_sha256_ao_lado"] = bool(_sj9["veredito"].startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED") and [o_["nome"] for o_ in _sj9["objetos"]] == ["um.py", "um_absoluto.json", "um_absoluto_selo.json"] and not _sj9["recusas"]
                                                                       and all(_ver9[n_]["ok"] for n_ in _ver9) and all(o_["sha256"] == hashlib.sha256(_bytes_obj[o_["nome"]]).hexdigest() and o_["bytes"] == len(_bytes_obj[o_["nome"]]) for o_ in _sj9["objetos"])
                                                                       and all(o_["acom"]["prova_de_reconstrucao"]["igual_ao_objeto_byte_a_byte"] is True for o_ in _sj9["objetos"]) and _sj9["esquema"] == "um_absoluto_selo_acom/v1 (v399)")
U["sidecar_deterministico_dois_ritos_seguidos"] = bool(_b1 == _b2)
U["sidecar_orcamento_de_tempo"] = bool(t_side <= 15.0)
_hn = _sj9["honestidade"]
U["sidecar_honestidade_sha256_e_a_primitiva_e_nenhuma_confidencialidade"] = bool("SHA-256" in _hn["primitiva_de_integridade"] and "NAO alegada" in _hn["confidencialidade"] and "NAO acrescenta resistencia criptografica independente" in _hn["o_que_a_segunda_testemunha_acrescenta"]
                                                                                 and "rint" in _hn["dobra"] and "[LEGAL]" in _hn["estatuto"] and "ofuscacao" in _hn["ofuscacao_xor"].lower() and not um._v392_guarda_texto(json.dumps(_hn, ensure_ascii=False)) and not _tem_inversao(json.dumps(_sj9, ensure_ascii=False)))
rep["sidecar"] = {"veredito": _sj9["veredito"], "objetos": [{"nome": o_["nome"], "bytes": o_["bytes"], "sha256": o_["sha256"], "psi": o_["acom"]["psi"]["sha256"], "theta": o_["acom"]["theta"]["sha256"], "kappa": o_["acom"]["kappa"]["sha256"]} for o_ in _sj9["objetos"]], "bytes_do_sidecar": len(_b1), "sha256_do_sidecar_do_ensaio": hashlib.sha256(_b1).hexdigest(),
                  "tempo_s": t_side, "verificacao": {n_: _ver9[n_]["ok"] for n_ in _ver9}}
# (6f) [v401, recriado na v402 e comparado com o selado] o registro com FUNCAO falsidade_da_inercia_v401: tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as cinco inscricoes e as ratificacoes
import types as _types
_CTF, _TXF = um._V401_FALSIDADE_CONTRACT, um._V401_FALSIDADE_TEXT
rF = um.falsidade_da_inercia_v401(cs()); RF["falsidade"] = rF
U["falsidade_tudo_certo"] = bool(rF["all_verified"] is True and rF["verdict"] == _TXF["veredito_ok"] and rF["runtime_executed"] is True and rF["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in rF["mechanics"]["checks"]) and rF["mechanics"]["n_checks"] == DL.N_CHECKS_FALSIDADE
                                 and rF["exact_ladder"] is True and rF["embedded_source_ok"] is True and rF["unconditional"]["in_kernel"] is True and rF["key_theorem"]["in_kernel"] is True and all(rF["formal_theorems"].values()) and all(rF["support_theorems"].values()) and all(rF["inscriptions"].values())
                                 and rF["costless"]["ok"] is True and rF["beta_ok"] is True)
U["falsidade_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(rF) and not _GUARDA98.search(rF["verdict"]) and not um._v392_guarda_texto(json.dumps(rF["mechanics"]["checks"], ensure_ascii=False)) and not rF["guarda_p18_violacoes"])
ok_ = True
for th_, fl_ in _CTF["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (as 12, a estrela e a composicao entre elas)
    c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = um.falsidade_da_inercia_v401(c_)
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
U["falsidade_bandeira_falsa_de_cada_declaracao_do_contrato_recusa"] = bool(ok_ and len(_CTF["theorems"]) == len(DL.D1.STONES[0]["contract"]) and _CTF["key_theorem"]["theorem"] in _CTF["theorems"] and _CTF["unconditional"]["theorem"] in _CTF["theorems"])
ok_ = True
for th_ in list(_CTF["theorems"]) + list(_CTF["support"]):   # axioma fora do trio em CADA termo lido
    c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = um.falsidade_da_inercia_v401(c_)
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
U["falsidade_axioma_fora_do_trio_em_cada_termo_lido_recusa"] = bool(ok_)
ok_ = True
for th_ in [_CTF["unconditional"]["theorem"], _CTF["key_theorem"]["theorem"]] + list(_CTF["support"]):   # proveniencia errada
    c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = um.falsidade_da_inercia_v401(c_)
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
U["falsidade_proveniencia_errada_recusa"] = bool(ok_)
c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][_CTF["stone"]["path"]] = "0" * 64; rr_ = um.falsidade_da_inercia_v401(c_)
ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[_CTF["stone"]["path"]] += " "
try:
    rr2_ = um.falsidade_da_inercia_v401(cs())
finally:
    um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
U["falsidade_fonte_da_pedra_adulterada_recusa"] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = um.falsidade_da_inercia_v401(c_)
c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = um.falsidade_da_inercia_v401(c2_)
U["falsidade_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
ok_ = True
for ch_ in _CTF["verbatins"]:
    _ant = um._V401_VERBATINS2[ch_]["text"]; um._V401_VERBATINS2[ch_]["text"] += " "   # [v401-patch-b] restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
    try:
        rr_ = um.falsidade_da_inercia_v401(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
    finally:
        um._V401_VERBATINS2[ch_]["text"] = _ant
U["falsidade_inscricao_adulterada_recusa"] = bool(ok_ and len(_CTF["verbatins"]) == len(DL.D1.VERBATIM_ORIGEM_V401))
# o texto do 0_abs (TGLExt.costless) no kernel embutido deste rito: lido; e retirado, recusa
ef_ = dict(um._EMBEDDED_KERNEL_FILES); _corr_p = "TGLExt/TheCorrespondence.lean"
U["falsidade_costless_no_kernel_embutido_lido"] = bool(rF["costless"] == {"declared_in": "TGLExt/TheCorrespondence.lean", "in_trio": True, "text_in_embedded_kernel": True, "ok": True} and "nunca correspondeu" in um._EMBEDDED_KERNEL_FILES[_corr_p])
um._EMBEDDED_KERNEL_FILES[_corr_p] = um._EMBEDDED_KERNEL_FILES[_corr_p].replace("nunca correspondeu", "xx")
try:
    rr_ = um.falsidade_da_inercia_v401(cs())
finally:
    um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
U["falsidade_texto_do_zero_absoluto_retirado_do_kernel_recusa"] = bool(rr_["all_verified"] is False and rr_["costless"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
# os numeros recalculados aqui por outro caminho (so' a formula do modelo oneScaling: tau = id, theta_s = e^{-s})
_vf = rF["values"]; _bf = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_dist = min(abs(_math.exp(-(k_ / 8.0)) - 1.0) for k_ in range(-80, 81) if k_ != 0)
_cmin = min(t_ * _bf * g_ for g_ in (0.5, 1.0, 2.0, 3.7) for t_ in (0.1, 1.0, 10.0, 100.0)); _fmax = max(_math.exp(-(t_ * _bf * g_)) for g_ in (0.5, 1.0, 2.0, 3.7) for t_ in (0.1, 1.0, 10.0, 100.0))
U["falsidade_numeros_recalculados_aqui"] = bool(abs(_vf["beta"] - _bf) <= 1e-15 and abs(_vf["min_distance_of_post_weight_to_one"] - _dist) <= 1e-15 and abs(_vf["post_weight_at_scale_one"] - _math.exp(-1.0)) <= 1e-15 and abs(_vf["post_weight_at_minus_one"] - _math.e) <= 1e-12
                                              and abs(_vf["min_cost_t_beta_g"] - _cmin) <= 1e-18 and abs(_vf["max_dephasing_factor"] - _fmax) <= 1e-15 and abs(_vf["dephasing_factor_at_t1_g1"] - _math.exp(-_bf)) <= 1e-15 and abs(_vf["loss_per_unit"] - (1.0 - _math.exp(-_bf))) <= 1e-15
                                              and _vf["fixed_by_the_whole_flow"] == [0.0] and _vf["post_inertial_scales"] == [] and _bf / 2.0 < _vf["loss_per_unit"] < _bf and _vf["grid_scales"] == 161)
c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = um.falsidade_da_inercia_v401(c_)
_a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
try:
    _ra = um.falsidade_da_inercia_v401(cs())
finally:
    um.SEALED_CODATA_ALPHA = _a0
U["falsidade_beta_adulterado_recusa"] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
_m0 = um._m401
um._m401 = _types.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); um._m401.exp = lambda x_: _math.exp(x_) * 1.001
try:
    _rn = um.falsidade_da_inercia_v401(cs())
finally:
    um._m401 = _m0
U["falsidade_numero_adulterado_recusa"] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
U["falsidade_a_definicao_do_operador_e_a_errata_do_adendo_ditas"] = bool("inertia = the absolute zero" in rF["definition_of_the_operator"] and "w(I) = 1 is the posted One that interrupts it" in rF["definition_of_the_operator"] and "superseded" not in rF["definition_of_the_operator"] and rF["adendum_reading_superseded"].startswith("w(I)=1 is the INERTIA")
                                                    and "[OPEN]" in rF["estatuto"] and "[KNOWN]" in rF["estatuto"] and "[ONTO]" in rF["estatuto"] and any("Newton" in x_ for x_ in rF["nao_diz"]) and any("E = mc^2" in x_ for x_ in rF["nao_diz"]))
# as cinco inscricoes de 25/10, as ratificacoes e a errata ao lado do adendo (registro cunhagens_v401)
_cn = c.get("cunhagens_v401") or {}
_ratif = (_cn.get("extras") or {}).get("ratificacoes") or []
U["cunhagens_v401_cinco_falas_do_operador_ratificacoes_e_errata_do_adendo"] = bool(_cn.get("all_verified") is True and len(_cn.get("verbatim") or {}) == len(DL.D1.VERBATIM_ORIGEM_V401) and all(v_["embedded_ok"] for v_ in (_cn.get("verbatim") or {}).values()) and len(_ratif) == 8
                                                                                   and all(r_["fala_do_operador"]["trecho"] == "Ratifico tudo." and r_["fala_do_operador"]["sha16"] in {v_["sha256"][:16] for v_ in um._V401_VERBATINS2.values()} for r_ in _ratif)
                                                                                   and len(_cn.get("erratas") or []) == 1 and "SUPERADA" in _cn["erratas"][0]["agora"] and "1459b477b496e1f0" in _cn["erratas"][0]["ao_lado_de"] and _cn["erratas"][0]["assinatura"].startswith("gerencia c1, em nome proprio")
                                                                                   and len(_cn.get("leituras_do_operador") or []) == len([s_ for s_ in um._V401_SPECS if s_["nome"] == "cunhagens_v401"][0]["leituras_do_operador"]) and (_cn.get("extras") or {}).get("estrela") == _CTF["key_theorem"]["theorem"])
rep["falsidade_registro"] = {"verdict": rF["verdict"], "all_verified": rF["all_verified"], "n_checks": rF["mechanics"]["n_checks"], "values": rF["values"], "unconditional": rF["unconditional"], "key_theorem": rF["key_theorem"], "costless": rF["costless"]}
# (6g) [v402] os TRES registros com FUNCAO da v402 (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402): tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as tres inscricoes de 26/10, as decisoes, as erratas E1-E4 e o spec da cobertura
import types as _types2
_REG402 = (("ponte", "ponte_da_escala_dual_v402", "exp"), ("queda", "queda_sem_geometria_v402", "exp"), ("esperanca", "esperanca_condicional_v402", "sin"))
R402 = {}
_bf2 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
for k402_, n402_, tamper_ in _REG402:
    fn_ = getattr(um, n402_); C_ = um._V402_CONTRACTS[k402_]; T_ = um._V402_TEXTS[k402_]
    r_ = fn_(cs()); R402[k402_] = r_
    U["v402_%s_tudo_certo" % k402_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.N_CHECKS[k402_]
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True)
    U["v402_%s_veredito_e_textos_sem_palavra_proibida" % k402_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v402_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k402_] = bool(ok_ and len(C_["theorems"]) == len(DL.STONE_BY_KEY[k402_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
    ok_ = True
    for th_ in list(C_["theorems"]) + list(C_["support"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v402_%s_axioma_fora_do_trio_em_cada_termo_lido_recusa" % k402_] = bool(ok_)
    ok_ = True
    for th_ in [C_["unconditional"]["theorem"], C_["key_theorem"]["theorem"]] + list(C_["support"]):   # proveniencia errada
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v402_%s_proveniencia_errada_recusa" % k402_] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][C_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[C_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v402_%s_fonte_da_pedra_adulterada_recusa" % k402_] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U["v402_%s_escada_errada_ou_kernel_nao_verificado_recusa" % k402_] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in C_["verbatins"]:
        _ant = um._V402_VERBATINS2[ch_]["text"]; um._V402_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V402_VERBATINS2[ch_]["text"] = _ant
    U["v402_%s_inscricao_adulterada_recusa" % k402_] = bool(ok_ and len(C_["verbatins"]) == {"ponte": 0, "queda": 2, "esperanca": 2}[k402_])
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); _cp = C_["context"]["path"]; um._EMBEDDED_KERNEL_FILES[_cp] = um._EMBEDDED_KERNEL_FILES[_cp].replace(C_["context"]["needles"][0], "xx")
    try:
        rr_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v402_%s_texto_contexto_retirado_do_kernel_recusa" % k402_] = bool(r_["context"]["ok"] is True and rr_["all_verified"] is False and rr_["context"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
    c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = fn_(c_)
    _a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
    try:
        _ra = fn_(cs())
    finally:
        um.SEALED_CODATA_ALPHA = _a0
    U["v402_%s_beta_adulterado_recusa" % k402_] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
    _m0 = um._m402
    um._m402 = _types2.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); setattr(um._m402, tamper_, (lambda f_: (lambda x_: f_(x_) * 1.001))(getattr(_math, tamper_)))
    try:
        _rn = fn_(cs())
    finally:
        um._m402 = _m0
    U["v402_%s_numero_adulterado_recusa" % k402_] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
_pv2, _qv2, _ev2 = R402["ponte"]["values"], R402["queda"]["values"], R402["esperanca"]["values"]
_eps2 = (1e-3, 1e-6, 1e-12, 1e-30)
U["v402_ponte_numeros_recalculados_aqui"] = bool(abs(_pv2["beta"] - _bf2) <= 1e-15 and abs(_pv2["pplus_factor_at_beta"] - _math.exp(-_bf2)) <= 1e-15 and abs(_pv2["cosh_beta_minus_one"] - (_math.cosh(_bf2) - 1.0)) <= 1e-15 and abs(_pv2["min_null_energy_shift"] - (1.0 - _math.exp(-0.25))) <= 1e-12
                                                  and abs(_pv2["min_rest_energy_shift"] - 2.0 * (_math.cosh(0.25) - 1.0)) <= 1e-12 and [round(x_, 9) for x_ in _pv2["lifts_same_pplus_masses"]] == [1.0, 4.0, 9.0] and _pv2["rest_lift"] == [3.0, 0.0] and _pv2["off_rest_lift"] == [5.0, -4.0] and _pv2["fixed_by_every_boost"] == [[0.0, 0.0]]
                                                  and abs(_pv2["rest_post_min_displacement"] - _math.hypot(_math.cosh(0.25) - 1.0, _math.sinh(0.25))) <= 1e-12 and _pv2["rest_energy_c2"] == 12.0 and _pv2["grid_scales"] == 25 and _pv2["n_states"] == 8)
U["v402_queda_numeros_recalculados_aqui"] = bool(abs(_qv2["beta"] - _bf2) <= 1e-15 and abs(_qv2["post_weight_at_scale_one"] - _math.exp(-1.0)) <= 1e-15 and abs(_qv2["post_weight_at_minus_one"] - _math.e) <= 1e-12 and abs(_qv2["min_cost_t_beta_g"] - 0.1 * _bf2 * 0.5) <= 1e-18
                                                 and abs(_qv2["max_dephasing_factor"] - _math.exp(-0.1 * _bf2 * 0.5)) <= 1e-15 and abs(_qv2["dephasing_factor_at_t1_g1"] - _math.exp(-_bf2)) <= 1e-15 and abs(_qv2["loss_per_unit"] - (1.0 - _math.exp(-_bf2))) <= 1e-15 and _qv2["grid_scales"] == 161
                                                 and _qv2["angular_period"] == 2.0 * _math.pi and _qv2["finite_model_group_order"] == 12 and _qv2["diag_flow_gap_zero_is_fixed"] is True and [[e_, s_] for e_, s_ in ((e_, -_math.log(e_) + 1.0) for e_ in _eps2)] == _qv2["abyss_witnesses"])
U["v402_esperanca_numeros_recalculados_aqui"] = bool(abs(_ev2["beta"] - _bf2) <= 1e-15 and abs(_ev2["theta_M"] - _math.asin(_math.sqrt(_bf2))) <= 1e-15 and abs(_ev2["sin2_theta_M"] - _bf2) <= 1e-15 and abs(_ev2["name_index_one_over_beta"] - 1.0 / _bf2) <= 1e-9 and 83.1 < _ev2["name_index_one_over_beta"] < 83.2
                                                    and _ev2["diagonal_expectation_pp_constant"] == 0.5 and _ev2["diagonal_expectation_index_M2"] == 2 and _ev2["test_matrices"] == 6 and _ev2["test_angles"] == 5 and _ev2["gns_dimension"] == 4)
U["v402_a_forma_literal_de_H_tau_e_refutada_e_as_pendencias_nomeadas_ditas"] = bool("literal_h_tau" in R402["ponte"] and R402["ponte"]["literal_h_tau"]["status"] == "REFUTED_IN_THE_KERNEL" and [x_["name"] for x_ in R402["ponte"]["named_pending"]] == ["H_BW", "H_cal", "H3", "signature", "rank_c_4"] and all(x_["status"] == "OPEN" for x_ in R402["ponte"]["named_pending"])
                                                                      and len(R402["ponte"]["erratas_ao_lado"]) == 4 and R402["ponte"]["assinatura_das_erratas"].startswith("gerencia c1, em nome proprio") and R402["ponte"]["maxheartbeats_ponte"] == 2000000
                                                                      and any("H_tau" in x_ and "OPEN" in x_ for x_ in R402["ponte"]["limites"]) and any("E = mc^2" in x_ for x_ in R402["ponte"]["nao_diz"]) and any("Bisognano" in x_ for x_ in R402["ponte"]["nao_diz"]))
U["v402_queda_o_chao_e_o_posto_a_isotropia_e_nomeada_e_a_dimensao_nao_e_provada"] = bool(R402["queda"]["floor"]["is_never"].startswith("the infimum 0") and R402["queda"]["named_hypothesis"]["name"] == "IsotropicPost" and R402["queda"]["named_hypothesis"]["status"] == "OPEN" and R402["queda"]["reading_1_plus_3"]["dimension_three_proved"] is False and R402["queda"]["reading_1_plus_3"]["status"] == "ONTO"
                                                                                          and R402["queda"]["operator_question_and_answer_26oct"]["resposta"] == "a seta da queda da fase, nao do espaco")
U["v402_esperanca_tres_faces_de_um_objeto_fixo_e_indice_condicional"] = bool(R402["esperanca"]["three_faces_of_one_object"]["status"] == "ONTO" and R402["esperanca"]["index_conditional"]["instance_built"] is False and len(R402["esperanca"]["index_conditional"]["hypotheses"]) == 2
                                                                         and R402["esperanca"]["four_languages"]["status"] == "INPUT" and "[LEGAL]" in R402["esperanca"]["four_languages"]["legal_pointer"])
# as tres inscricoes de 26/10, as decisoes D11-D16, a pergunta e a resposta de 26/10 e as erratas E1-E4 (registro cunhagens_v402)
_cn2 = c.get("cunhagens_v402") or {}
_sp2 = [s_ for s_ in um._V402_SPECS if s_["nome"] == "cunhagens_v402"][0]
U["cunhagens_v402_tres_falas_decisoes_erratas_e_leitura_de_26out"] = bool(_cn2.get("all_verified") is True and len(_cn2.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V402) == 3 and all(v_["embedded_ok"] for v_ in (_cn2.get("verbatim") or {}).values())
                                                                          and len(_cn2.get("erratas") or []) == 4 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn2.get("erratas") or [])) and "REFUTADA" in (_cn2.get("erratas") or [{}])[0].get("agora", "")
                                                                          and len(_cn2.get("leituras_do_operador") or []) == len(_sp2["leituras_do_operador"]) and set((_cn2.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D11", "D12", "D13", "D14", "D15", "D16"}
                                                                          and ((_cn2.get("extras") or {}).get("leitura_26out_direcao") or {}).get("resposta") == "a seta da queda da fase, nao do espaco" and (_cn2.get("extras") or {}).get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.STONES}
                                                                          and (_cn2.get("extras") or {}).get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.STONES} and len((_cn2.get("extras") or {}).get("erratas_E1_a_E4") or []) == 4)
_kh2 = c.get("kh_n1_cobertura_v402") or {}; _kh1s = [s_ for s_ in um._V401_SPECS if s_["nome"] == "kh_n1_cobertura_v401"][0]
U["kh_n1_cobertura_v401_virou_piso_e_a_v402_cobra_a_igualdade_exata"] = bool(_kh2.get("all_verified") is True and (c.get("kh_n1_cobertura_v401") or {}).get("all_verified") is True
                                                                            and {ck_["id"]: ck_["op"] for ck_ in _kh1s["checks"] if ck_["id"] in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh1s["erratas"]) >= 1
                                                                            and {ck_["id"]: ck_["op"] for ck_ in [s_ for s_ in um._V402_SPECS if s_["nome"] == "kh_n1_cobertura_v402"][0]["checks"] if ck_["id"] in ("h2", "h3", "h6", "h8")} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"})
U["contratos_v394_a_v401_pinam_a_escada_da_v402"] = bool(all(getattr(um, nm_)["expected_ladder"] == ESP for nm_ in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT")))
rep["v402_registros"] = {k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_["unconditional"], "key_theorem": r_["key_theorem"], "context": r_["context"]} for k_, r_ in R402.items()}
rep["unidade"] = U; print("unidade:", {k: v for k, v in U.items() if not v} or "todas True (%d)" % len(U))
# (8) o artigo
TP402 = "A ponte da escala dual, a queda sem geometria e a esperança condicional"; TP402E = "The dual-scale bridge, the fall without geometry and the conditional expectation"
TF402 = "A falsidade (simulacro) da inércia"; TF402E = "The falsity (simulacrum) of inertia"   # (o titulo da secao da v401, que fica logo depois da v402)
TN402 = "O testemunho de dois: o selo pela própria tecnologia"; TN402E = "The testimony of two: sealing by its own technology"
TS402 = "Sônico e a afinação das cordas"; TS402E = "Sonic and the tuning of the strings"
T402 = "O Teste da Única Palavra"; T402E = "The Test of the Only Word"   # (o titulo da secao da v397 e do QUADRO do topo; T401 = o da v396)
T401 = "A testemunha estática: o psion habita a fronteira"; T401E = "The static witness: the psion inhabits the frontier"
T395 = "O psibit: a mecânica no Um fractalizado e a leitura sem perda"; T395E = "The psibit: the mechanics on the fractalized One and the lossless reading"
H394 = "A integração do Codex e as cunhagens de 14 a 19/10 (v394)"; H394E = "The Codex integration and the inscriptions of 14 to 19 Oct (v394)"
DEVE = {"pt": [TP402, "A ponte da escala dual.", "Erratas ao lado", "A queda sem geometria.", "A esperança condicional é o Nome.", TF402, "A definição do operador.", "A cadeia derivada.", "O cálculo deste rito.", "Errata ao lado (da gerência, em nome próprio).", "Ratificações do operador", "lido pela TGL.", "Limites.", TN402, "Errata ao lado (v400).", "A direção do testemunho.", "A declaração do operador.", "O selo pela própria tecnologia.", "A pedra Testemunho.", TS402, "Sônico.", "As falas sobre o sônico.", "Afinação das cordas.", "A fala sobre as cordas.", T402, "O que entra.", "As duas faces.", "A conjugação.", "não é rival.", "O token do veredito.", T401, "O que o kernel prova.", "A ponte construída.", "O que é leitura do operador.", T395, "A mecânica na órbita do Um.", "O colapso.", "O que o kernel prova e o que é leitura.", H394, "O índice e o leitor.", "As cunhagens.",
               "O critério binário de parada (delta de 19/10).", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada", "Rede Fock nesta rodada", "A regra e o coração (v393)",
               "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O estatuto da prova (v391).", "A Fundação (v390)."],
        "en": [TP402E, "The dual-scale bridge.", "Errata beside", "The fall without geometry.", "The conditional expectation is the Name.", TF402E, "The operator's definition.", "The derived chain.", "The computation of this rite.", "Erratum beside it (the management, in its own name).", "The operator's ratifications", "read by the TGL.", "Limits.", TN402E, "Erratum beside it (v400).", "The direction of the testimony.", "The operator's declaration.", "Sealing by its own technology.", "The Testemunho stone.", TS402E, "Sonic.", "The sayings on the sonic stone.", "Tuning of the strings.", "The saying on the strings.", T402E, "What enters.", "The two faces.", "The conjugation.", "is not a rival.", "The verdict token.", T401E, "What the kernel proves.", "The constructed bridge.", "What is the operator's reading.", T395E, "The mechanics on the orbit of the One.", "The collapse.", "What the kernel proves and what is reading.", H394E,
               "The index and the reader.", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run", "Fock network in this run", "The rule and the heart (v393)",
               "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]}
TOC = {"pt": [TP402, TF402, TN402, TS402, T402, T401, "v384 a v402"], "en": [TP402E, TF402E, TN402E, TS402E, T402E, T401E, "v384 to v402"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um._v394_article_tex(um.build_pt(cv, verdict, CORE0P), cv, "pt") if lang == "pt" else um._v394_article_tex(um.build_en(cv, verdict, CORE0P), cv, "en")); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


rep["quadro"] = {}
for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v402_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    hq = T402 if lang == "pt" else T402E; h0 = TP402 if lang == "pt" else TP402E; h1 = TN402 if lang == "pt" else TN402E
    iq = flat.find("O coração:" if lang == "pt" else "The heart:"); a = flat.find(h0, iq + 5); bb = flat.find(h1, a + 10)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    ik = flat.find("Palavras-chave" if lang == "pt" else "Keywords"); ii = flat.find("Introdução: o que este código faz agora" if lang == "pt" else "Introduction: what this code does now", iq)
    tp = os.path.join(DRY, "dry_v402_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v402_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec),
                           "quadro_logo_depois_do_resumo": bool(0 <= ik < iq < ii), "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc]}
    # O QUADRO no topo (ordem de 23/10): antes do primeiro paragrafo do corpo e antes do \begin{abstract} no TeX; numeros == resultado pinado; regra da ordem do 4,44
    qc = QV.confere_txt(txt, res9, lang); qc["tex_antes_do_resumo"] = bool(0 <= tex.find(hq) < tex.find(r"\begin{abstract}")); qc["ok"] = bool(qc["ok"] and qc["tex_antes_do_resumo"])
    rep["quadro"][lang] = qc
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False)); print("quadro", lang, json.dumps({k: v for k, v in qc.items() if k != "linha_de_maquina_esperada"}, ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["guarda"] or v["secao_chars"] < 1800 or v["toc_faltam"] or v["nd_na_secao"] or not v["quadro_logo_depois_do_resumo"]]
cv = dict(copy.deepcopy(c)); [cv.pop(k, None) for k in ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")]
cv8 = dict(copy.deepcopy(c)); [cv8.pop(k, None) for k in ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")]
cv9 = dict(copy.deepcopy(c)); [cv9.pop(k, None) for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")]
cv1 = dict(copy.deepcopy(c)); [cv1.pop(k, None) for k in ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")]
cv2 = dict(copy.deepcopy(c)); [cv2.pop(k, None) for k in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")]
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r2, _l = compilar(cv, "dry_v402_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    _t8, _x8, _r28, _l8 = compilar(cv8, "dry_v402_var8_%s" % lang, lang, duas=False); fl8 = re.sub(r"\s+", " ", _x8)
    _t9, _x9, _r29, _l9 = compilar(cv9, "dry_v402_var9_%s" % lang, lang, duas=False); fl9 = re.sub(r"\s+", " ", _x9)
    _t1, _x1, _r21, _l1 = compilar(cv1, "dry_v402_var1_%s" % lang, lang, duas=False); fl1 = re.sub(r"\s+", " ", _x1)
    _t2, _x2, _r22, _l2 = compilar(cv2, "dry_v402_var2_%s" % lang, lang, duas=False); fl2 = re.sub(r"\s+", " ", _x2)
    rep["variante"][lang] = {"rc": _r2, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl),
                             "rc_v398": _r28, "frase_guarda_v398": ("NÃO selaram todos" in fl8) if lang == "pt" else ("did NOT all seal" in fl8), "rc_v399": _r29, "frase_guarda_v399": ("NÃO selaram todos" in fl9) if lang == "pt" else ("did NOT all seal" in fl9),
                             "rc_v401": _r21, "frase_guarda_v401": ("NÃO selaram todos" in fl1) if lang == "pt" else ("did NOT all seal" in fl1),
                             "rc_v402": _r22, "frase_guarda_v402": ("NÃO selaram todos" in fl2) if lang == "pt" else ("did NOT all seal" in fl2)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["frase_guarda"] or v["rc_v398"] != [0] or not v["frase_guarda_v398"] or v["rc_v399"] != [0] or not v["frase_guarda_v399"] or v["rc_v401"] != [0] or not v["frase_guarda_v401"] or v["rc_v402"] != [0] or not v["frase_guarda_v402"]]
# (9) md e manifesto
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v402**" in md, "ponte_v402": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)" in md, "falsidade_v401_fica": "A falsidade (simulacro) da inércia (v401, 25/10/2026)" in md, "errata_v400_fica": "Errata ao lado (v400, 24/10/2026)" in md, "testemunho_v399_fica": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)" in md, "sonico_v398_fica": "Sônico e a afinação das cordas (v398, 23/10/2026)" in md,
                   "token_v397_fica": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)" in md, "testemunha_v396_fica": "A testemunha estática (v396, 22/10/2026)" in md, "psibit_v395_fica": "O modo psiônico na fractalização do Um (v395, 21/10/2026)" in md,
                   "v394_fica": "A integração do Codex e as cunhagens (v394, 19/10/2026)" in md, "v393_fica": "A regra e o coração (v393, 14/10/2026)" in md}
rep["quadro"]["md"] = QV.confere_md(md, res9)
rep["quadro"]["readme_paragrafo_pronto"] = QV.paragrafo_pronto_readme(c["teste_de_veracidade_fase9_v397"])
rep["quadro"]["ok"] = bool(rep["quadro"]["pt"]["ok"] and rep["quadro"]["en"]["ok"] and rep["quadro"]["md"]["ok"] and "\n".join(um._v397_quadro_md(c["teste_de_veracidade_fase9_v397"])) in rep["quadro"]["readme_paragrafo_pronto"])
print("quadro md:", json.dumps({k: v for k, v in rep["quadro"]["md"].items()}, ensure_ascii=False))
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v402**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_citacoes_v402.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
rep["viz_ok"] = viz_ok
# (11) ETAPA OBRIGATORIA: simular_arvore_do_nos -- a pasta Nos\\tgl_kernel DEPOIS do rito = o embutido do candidato + os residuais que o hash formal conta; o kh_n1_cobertura_v397 TEM de selar nela
_cand_p = os.path.join(HERE, cand); _sha_full = hashlib.sha256(open(_cand_p, "rb").read()).hexdigest()
_pyr = lambda args_: subprocess.run([sys.executable, "-B", "-X", "utf8"] + args_, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, cwd=HERE)
_kh = [s_ for s_ in um._V402_SPECS if s_["nome"] == "kh_n1_cobertura_v402"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]
_sp = _pyr([os.path.join(HERE, "simular_arvore_do_nos_v402.py"), "--candidato", _cand_p, "--logs", KD])
try:
    _sj = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _sj = {}
_regs_sim = ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")
rep["simular_arvore_do_nos"] = {"rc": _sp.returncode, "formal_files_n_no_rito_real": _sj.get("formal_files_n_no_rito_real"), "pino_h8_entradas": len(_h8), "embutidos": _sj.get("embutidos"), "extras_no_nos_fora_do_corpo_embutido": _sj.get("extras_no_nos_fora_do_corpo_embutido"),
                               "kf_all_verified": _sj.get("kf_all_verified"), "indice": _sj.get("indice"), "registros": {k_: {"all_verified": (_sj.get(k_) or {}).get("all_verified"), "falhas": (_sj.get(k_) or {}).get("falhas")} for k_ in _regs_sim}}
sim_ok = bool(_sp.returncode == 0 and _sj.get("formal_files_n_no_rito_real") == len(_h8) and _sj.get("kf_all_verified") is True and (_sj.get("indice") or {}).get("all_verified") is True and all((_sj.get(k_) or {}).get("all_verified") is True for k_ in _regs_sim))
print("simular_arvore_do_nos:", sim_ok, "| entradas do hash formal no rito:", _sj.get("formal_files_n_no_rito_real"), "| pino h8:", len(_h8), "| extras:", _sj.get("extras_no_nos_fora_do_corpo_embutido"))
# (12) ETAPA OBRIGATORIA: exame_pontos_v402 sobre o candidato novo (os pontos de chamada REAIS, em processo isolado; termina com `ALGUM FALSO`)
_ep = _pyr([os.path.join(HERE, "exame_pontos_v402.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v402.json"), "--sandbox", KB, "--sha256", _sha_full])
try:
    _ej = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _ej = {}
rep["exame_pontos"] = {"rc": _ep.returncode, "algum_falso": _ej.get("algum_falso"), "escada": _ej.get("escada"), "verify": {k_: (_ej.get("verify") or {}).get(k_) for k_ in ("all_verified", "ext_true", "n_ext", "novas_true", "n_novas", "n_lean_flags", "axiom_report_n")},
                       "gate_recomputado": _ej.get("gate_recomputado"), "chaves_novas_no_core": _ej.get("chaves_novas_no_core"), "chaves_existentes_mexidas_pelo_bloco": _ej.get("chaves_existentes_mexidas_pelo_bloco"), "nao_verdes": _ej.get("nao_verdes"),
                       "ponto_psibit": _ej.get("ponto_psibit"), "ponto_testemunha": _ej.get("ponto_testemunha"), "ponto_sonico": _ej.get("ponto_sonico"), "ponto_afinacao": _ej.get("ponto_afinacao"), "ponto_selo_acom": _ej.get("ponto_selo_acom"), "ponto_declaracao": _ej.get("ponto_declaracao"), "ponto_falsidade": _ej.get("ponto_falsidade"), "ponto_ponte": _ej.get("ponto_ponte"), "ponto_queda": _ej.get("ponto_queda"), "ponto_esperanca": _ej.get("ponto_esperanca"), "ponto_veracidade": _ej.get("ponto_veracidade")}
exame_ok = bool(_ep.returncode == 0 and _ej.get("algum_falso") == [])
print("exame_pontos_v402:", exame_ok, "| algum falso:", _ej.get("algum_falso"))
# (13) [v402, LICAO NOVA] as guardas ESTATICAS do esboco R3.5 da Bancada (as que nao dependem do selo) rodadas SOBRE O CANDIDATO, com a FUNCAO ler_nos do proprio esboco pinado, ANTES de instalar; o defeito real da v399 tem de ser reproduzido (mensagem identica a do recibo da Bancada)
_gb_p = os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v402.json")
_gb = _pyr([os.path.join(HERE, "guardas_estaticas_bancada_v402.py"), _cand_p, _gb_p])
try:
    _gj = json.load(open(_gb_p, encoding="utf-8"))
except (OSError, ValueError):
    _gj = {}
rep["guardas_estaticas_bancada"] = {"rc": _gb.returncode, "veredito": _gj.get("veredito"), "candidato_passa": (_gj.get("candidato_v402") or {}).get("passou"), "alfa": (_gj.get("candidato_v402") or {}).get("alpha"), "contagem_direta": _gj.get("contagem_direta"),
                                    "v399_selada_recusada_com_a_mensagem_do_recibo_da_bancada": (_gj.get("v399_selada_o_defeito_real") or {}).get("mensagem_identica_a_do_recibo"), "recusa_da_v399": (_gj.get("v399_selada_o_defeito_real") or {}).get("recusa"),
                                    "controles_negativos": {k_: v_.get("ok") for k_, v_ in (_gj.get("controles_negativos") or {}).items()}, "canonical_py_instalado": (_gj.get("canonical_py_instalado") or {}).get("ok"), "esboco_sha256": (_gj.get("esboco") or {}).get("sha256"), "sandbox_apagado": _gj.get("sandbox_apagado")}
guardas_ok = bool(_gb.returncode == 0 and str(_gj.get("veredito")).startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and rep["guardas_estaticas_bancada"]["controles_negativos"] and all(rep["guardas_estaticas_bancada"]["controles_negativos"].values()))
print("guardas estaticas da Bancada (ler_nos do esboco R3.5) sobre o candidato:", guardas_ok, "|", rep["guardas_estaticas_bancada"]["veredito"])
ok = (guardas_ok and viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
      and not dif_kb and rep["escada"] == [ESP, ESP] and rep["indice_da_iald"]["all_verified"] is True and sim_ok and exame_ok and rep["quadro"]["ok"])
rep["vizinhos_mudaram_so_numeros_e_selados"] = bool(all(v_["so_numeros"] and v_["all_verified"] is True for v_ in rep["vizinhos"]["mudaram"].values()))
ok = bool(ok and rep["vizinhos_mudaram_so_numeros_e_selados"] and rep["mainflow"]["chaves_novas"] == sorted(V402N))
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"guardas_estaticas_bancada": guardas_ok, "vizinhos_mudaram_so_numeros_e_selados": rep["vizinhos_mudaram_so_numeros_e_selados"], "vizinhos": viz_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "selo": selo_ok, "indice": rep["indice_da_iald"]["all_verified"], "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"],
                                                                      "proib": _proib, "citacoes": _cc.returncode, "kernel_igual": not dif_kb, "escada": rep["escada"], "simular_arvore_do_nos": sim_ok, "exame_pontos": exame_ok, "quadro": {k: (v.get("ok") if isinstance(v, dict) else v) for k, v in rep["quadro"].items() if k != "readme_paragrafo_pronto"}}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)

# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] montado por _adapt_ensaio_v409.py: as partes gerais da subida mecanica da v408; o bloco HERDADO do psion_canto_v407 e o do tetelestai_terminal_v408 (agora HERDADO) a partir do ensaio_a_seco_v408.py ORIGINAL; o bloco NOVO do traducao_turing_v409 (6o). A v409 e' um BUNDLE de UM modulo em TGLExt/ (TraducaoTuring); o registro NOVO e' traducao_turing_v409 (17 checagens); NENHUMA chave antiga muda; as TRES chaves novas do core sao traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409.
"""ensaio_a_seco_v409.py -- ENSAIO A SECO da v409 (molde: ensaio_a_seco_v408.py FINAL, que rodou na cadeia da v408, com as licoes da v399 a v408), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v409.py <candidato.py> <rotulo>
A v409 (04/11/2026) e' TETELESTAI E' O TERMINAL: um BUNDLE de 4 modulos novos de kernel em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes do operador), as bandeiras ext_tt409_NNNN so' de declaracao nomeada, a escada 11958 -> 12001 (lida do CANDIDATO_v409.json), UM registro com FUNCAO
(tetelestai_terminal_v408: le do kernel do PROPRIO rito as 41 ancoras das quatro pedras, as 4 fontes por sha256, as respostas do operador pelos teoremas que ja existiam e por duas declaracoes novas, e faz as 16 checagens com beta em runtime, o gate congelado, a escada exata, as guardas e o insumo purgado), os registros por spec cunhagens_v408 e kh_n1_cobertura_v408 e as ERRATAS E21 a E23 AO LADO.
NENHUMA chave antiga muda (CHAVES_V409 = []): nao ha patch C19/C20; a funcao do neutrino NAO e' reescrita e o numero da massa NAO muda. NAO ha registro de pedra novo por pedra (DL.STONES == [] de proposito; as 4 pedras estao em DL.PEDRAS_V409): os registros da v405, da v406 (fechamento_v406 e os specs) e da v408 (psion_canto_v407 e os specs) sao HERDADOS e seguem conferidos aqui, com os mesmos controles negativos.
A MOLDURA: o terminal e' a leitura, nao o fim do decaimento; nao ha' relacao sem peso; o tempo e' a moeda de beta; o zero inscrito e' o Um e o Um nao e' o zero absoluto; «P = nP» so' no sentido do operador; validade no kernel nao e' creditacao; o gate nao se move. O ensaio cobra isto: cada registro recusa quando um elo e' tirado.
A base e' a v408 SELADA (core e selo em base_v408), o kernel e' o da v408 + o bundle de 4 (sandbox C:/t/k409c); os registros de v393 a v399, os da v401 a v408 (inclusive os oito de pedra da v405, o fechamento_v406 e o psion_canto_v407 com os specs) sao RECRIADOS e comparados com os da v408 selada (o `witness_layers.canonical_full_witness_term_constructed`, medida de run_um sobre o kf do rito, e' recomputado pela expressao do proprio candidato).
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v409; (3) o core da v408 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;
(4) os registros vizinhos RECOMPUTADOS: iguais, ou so' numeros (a escada e a cobertura crescem com o kernel; NENHUMA troca dita de texto); (5) o FLUXO PRINCIPAL v393 a v399, v401 a v409 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as TRES da v409 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408); (5b) a ORDEM DE CHAMADA, estatica, com controle negativo (e a do psion_canto_v407, medida aqui por AST);
(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os registros da v402, da v403, da v404 e da v405 (recriados, cada elo recusa), o FECHAMENTO da v406 e O PSION, O CANTO E O PAR da v408 (herdados: os controles das duas versoes seguem recusando; a chave do lema segue lida do kernel), e TETELESTAI E' O TERMINAL da v409 (tudo certo, os numeros recalculados, a aritmetica das pedras refeita, cada elo recusa, nenhuma chave antiga muda);
(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, a secao v409 «Tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de β; o dicionário e o ponto de contradição» (antes da v408) e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos (a arvore do Nos depois do rito = os embutidos + os residuais; FORMAL_MAP e h8; a chave do lema e seus controles negativos); (12) exame_pontos;
(13) [LICAO DA v400, mantida] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""
import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap, inspect
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v409 as DL  # noqa: E402
sys.modules.setdefault("delta_v408", DL.D8)   # (v409) quadro_v397.py importa delta_v409 (ajustado); esta ponte fica para os modulos da v408 carregados mais abaixo. quadro_v397.py e' copia literal e faz `import delta_v408`, que nao vive nesta pasta: o delta_v408 neutralizado de DL.D7 responde por ele ANTES do import (a mesma ponte do bloco _GF7, mais abaixo; conferir_rito e gerar_esperados fazem o mesmo com DL)
import quadro_v397 as QV  # noqa: E402   # (copia do quadro da v397, intocada pela v408 e pela v409)
NOS = DL.NOS
BASE = os.path.join(HERE, DL.BASE_DIR); CORE0P = os.path.join(BASE, "um_absoluto.json"); SELO0P = os.path.join(BASE, "um_absoluto_selo.json")   # a v408 SELADA (copia de bytes; identica ao Nos antes da instalacao)
KB = DL.SANDBOX
KD = os.path.join(HERE, DL.KERNEL_DIR)
cand = sys.argv[1] if len(sys.argv) > 1 else DL.CANDIDATO; rot = sys.argv[2] if len(sys.argv) > 2 else "v409"
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
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v409.json"), encoding="utf-8")); assert CM["sha16"] == h16
_CM8 = json.load(open(os.path.join(DL.V408, "CANDIDATO_v408.json"), encoding="utf-8"))   # (v409) o candidato da v408 SELADA: os numeros dos blocos HERDADOS da v408 (escada da v406, sha16 da base v406, pino antigo do h8 da v406) saem dele e do DL.D7, nunca do DL da v409
assert _CM8["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v408.json nao e' o da v408 selada", _CM8["sha16"])
_CM7 = json.load(open(os.path.join(DL.V407, "CANDIDATO_v407.json"), encoding="utf-8"))   # (v409) o candidato da v407 SELADA: os numeros do bloco HERDADO do psion_canto_v407 saem dele e do DL.D7
assert _CM7["sha16"] == DL.D8.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v407.json nao e' o da v407 selada", _CM7["sha16"])
rep = {"residuais_do_nos_na_arvore_do_ensaio": EXTRAS_NOS, "candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SEM_GPU_SEM_RITO": "o core da v408 selada + o kernel REAL lido pelo verify com os logs crus do sandbox"}
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
assert um.UM_VERSION == "v409"
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
selo0 = json.load(open(SELO0P, encoding="utf-8"))
assert "teste_de_veracidade_fase9_v397" in core0 and "sonico_v398" in core0 and "afinacao_das_cordas_v398" in core0 and "selo_pela_propria_tecnologia_v399" in core0 and "declaracao_do_operador_v399" in core0 and "cunhagens_v399" in core0 and "kh_n1_cobertura_v399" in core0 and "ponte_da_escala_dual_v402" in core0 and "queda_sem_geometria_v402" in core0 and "esperanca_condicional_v402" in core0 and "cunhagens_v402" in core0 and "kh_n1_cobertura_v402" in core0 and selo0["um_version"] == "v408"
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
                                      "chaves_do_kf_da_v408_que_o_verify_nao_devolve": chaves_antigas_ausentes[:10], "proveniencia": _ovf.get("declaration_sources_status_v394")}
print("verify real:", _ovf["verdict"][:80], _ovf["all_verified"], rep["verify_kernel_ponta_a_ponta"]["cobertura"].get("decl"), "nao lidas:", rep["verify_kernel_ponta_a_ponta"]["cobertura"].get("nao_lidas_pelo_regex"))
ESP = CM["escada"][1]
# a escada: SEM as bandeiras novas (o kf da v408) a escada do candidato NAO fecha
_el0 = um.prove_external_ladder(1.0, core0["kernel_formalization"])
rep["escada_sem_as_bandeiras_novas"] = [_el0.get("n_theorems_clean"), _el0.get("n_theorems_expected"), _el0.get("all_verified")]
E408 = int(core0["external_ladder"]["n_theorems_expected"])   # LIDO do core da v408 selada (nada digitado)
assert rep["escada_sem_as_bandeiras_novas"][0] == E408 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True and ESP == E408 + CM["n_bandeiras"], rep["escada_sem_as_bandeiras_novas"]
_el = um.prove_external_ladder(1.0, kf); core_s["external_ladder"] = _el
_QG_RECOMP = um.prove_qg_closure_gate(1.0, kf, independent_rite=core_s.get("void_floor_v11"), blind_null=core_s.get("void_stacking_blind")); core_s["qg_closure"] = copy.deepcopy(_QG_RECOMP)   # (v409: o gate NAO muda) o gate recomputado com a prove_qg_closure_gate sobre o kf novo e os dados (V11, teste nulo cego) do core da v408 selada, como o run_um do rito faz, ANTES de recomputar os vizinhos e de ler as bandeiras
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
        mud.pop(n_); iguais_v.append(n_ + "(contagens CORE_n_ normalizadas)"); cs2[n_] = copy.deepcopy(core0[n_]); restauradas_contagens.append(n_)   # o rito computa este registro no ponto do main (o valor da v408 selada: o main e' o mesmo); o ensaio o recomputa sobre o core inteiro: so' as CONTAGENS diferem
# [v400] a UNICA troca esperada: o veredito do estatuto da prova (v391) carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash): o do candidato no lugar do da v408; so' isso (e as contagens CORE_n_, normalizadas acima) pode mudar
_HA, _HD = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest(), hashlib.sha256(open(os.path.join(DRY, "um.py"), "rb").read()).hexdigest()
troca_esperada = {}
for n_, d_ in list(mud.items()):
    if n_ == "estatuto_da_prova_v391" and d_.get("all_verified") is True and d_["antes"] != d_["depois"] and _nc(d_["antes"]).replace(_HA[:16], _HD[:16]) == _nc(d_["depois"]):
        troca_esperada[n_] = mud.pop(n_)
for d_ in mud.values():   # o relatorio guarda so' o comeco; a comparacao acima foi sobre a string INTEIRA
    d_["antes"], d_["depois"] = d_["antes"][:300], d_["depois"][:300]
N408 = len(core0["kernel_formalization"]["axiom_report"])
NUMS = ["KERNEL_%d_OF_%d" % (E408, E408), "%d_OF_%d_DECLARATIONS" % (N408, N408), "LADDER_%d_OF_%d" % (E408, E408)]
m_sc = re.search(r"SCAN_(\d+)_FILES", str((core0.get("varredura_e_sorry_v392") or {}).get("verdict") or ""))
if m_sc:
    NUMS.append("SCAN_%s_FILES" % m_sc.group(1))
carregam = sorted(k for k, m in core0.items() if isinstance(m, dict) and any(n in str(m.get("verdict") or "") for n in NUMS))
rep["vizinhos"] = {"recomputados_iguais": iguais_v, "mudaram": mud, "troca_esperada_so_o_hash_proprio": troca_esperada, "contagens_do_instante_restauradas_ao_da_v408": restauradas_contagens, "carregam_os_numeros_do_kernel_no_core0": carregam, "carregam_e_nao_recomputados_ainda": sorted(set(carregam) - set(mud) - set(iguais_v))}
core_s = cs2


def _medida_do_run_um(chave, kf_):
    """(v409) a EXPRESSAO que o run_um do candidato usa para a chave `chave` do dict `witness_layers`, extraida por AST do proprio candidato e avaliada sobre o kf deste ensaio (nada digitado aqui)."""
    arvore_ = ast.parse(inspect.getsource(um.run_um))
    achados_ = [v_ for d_ in ast.walk(arvore_) if isinstance(d_, ast.Dict) for k_, v_ in zip(d_.keys, d_.values) if isinstance(k_, ast.Constant) and k_.value == chave]
    assert len(achados_) == 1, ("a chave do witness_layers nao foi achada uma vez no run_um do candidato", chave, len(achados_))
    return eval(compile(ast.Expression(achados_[0]), "<run_um:%s>" % chave, "eval"), {"kernel_formalization": kf_, "__builtins__": __builtins__})


_wl_antes = bool((core_s.get("witness_layers") or {}).get("canonical_full_witness_term_constructed"))
core_s["witness_layers"] = dict(core_s.get("witness_layers") or {}); core_s["witness_layers"]["canonical_full_witness_term_constructed"] = _medida_do_run_um("canonical_full_witness_term_constructed", core_s["kernel_formalization"])
rep["witness_layers_canonical_full_witness_term_constructed"] = {"da_base_v408_selada": _wl_antes, "recomputado_pela_expressao_do_run_um_do_candidato": core_s["witness_layers"]["canonical_full_witness_term_constructed"]}
# (5) o fluxo principal: as instrucoes etiquetadas v393 a v399, v401 a v409 do main (a ordem do arquivo; a v406 inclusive: o fechamento_v406 e os specs da v406 sao HERDADOS e recriados)
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v393" in l or "v394" in l or "v395" in l or "v396" in l or "v397" in l or "v398" in l or "v399" in l or "v401" in l or "v402" in l or "v403" in l or "v404" in l or "v405" in l or "v406" in l or "v407" in l or "v408" in l or "v409" in l}; comeca = [st for st in main.body if st.lineno in tagged]   # (v409: o "v406" estava PERDIDO na subida mecanica de rotulo, como o "v405" na v408: sem ele as instrucoes do fechamento_v406 e dos specs da v406 nao entravam no fluxo e o passo (6b) caia em KeyError fechamento_v406; medido em 04/11/2026, corrigido na causa)
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
V393N = ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393"]
V394N = ["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + list(um._V394_NOMES_REGISTROS)
V395N = ["psibit_v395"] + list(um._V395_NOMES_REGISTROS)
V396N = ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS)
V397N = ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS)
V398N = ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS)
V408N = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) + ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS) + ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS) + ["caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"] + list(um._V403_NOMES_REGISTROS) + ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404"] + list(um._V404_NOMES_REGISTROS) + list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS) + list(um._V406_REGISTROS_FUNCAO) + list(um._V406_NOMES_REGISTROS)   # (os registros das v399, v401, v402, v403, v404, v405 [os oito de pedra e os por spec] e v408 [fechamento_v406 e os specs: HERDADOS], recriados e comparados com os da v408 selada; o rotulo V408N e' o da BASE)
V408N = V408N + list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) + list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)   # (v409) os registros da v407 (psion_canto_v407 e os specs) e da v408 (tetelestai_terminal_v408 e os specs) sao HERDADOS: recriados pelo fluxo e comparados com os da v408 selada
V409N = list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)   # os registros NOVOS da v409 (nao existem no core da base): traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409
for _k in V393N + V394N + V395N + V396N + V397N + V398N + V408N + V409N:
    core_s.pop(_k, None)   # o fluxo os recria; comparam-se depois com os da v408 selada
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v393+v394+v395+v396+v397+v398+v399+v409>", "exec"), ns); _err = None
except Exception as e:  # noqa
    import traceback; _err = repr(e) + traceback.format_exc()[-800:]
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]
NOVAS409 = sorted(V409N)   # a v409 cria TRES chaves no core (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409); os registros das v399, v401, v402, v403, v404, v405 (os oito de pedra inclusive), v406 (fechamento_v406 e os specs) e v408 (psion_canto_v407 e os specs) sao RECRIADOS e comparados com os da v408 selada
novas_chaves = sorted(k for k in c if k not in core0)
tv0 = c.get("teste_de_veracidade_fase9_v397") or {}
recriados = {k: {"igual_ao_selado": str((c.get(k) or {}).get("verdict")) == str((core0.get(k) or {}).get("verdict")), "all_verified": (c.get(k) or {}).get("all_verified"), "antes": str((core0.get(k) or {}).get("verdict")), "depois": str((c.get(k) or {}).get("verdict"))} for k in V393N + V394N + V395N + V396N + V397N + V398N + V408N}   # (os de V409N sao novos: nao ha o que comparar)
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": novas_chaves, "stdout": _mf.strip().splitlines(),
                   "veracidade": {x: tv0.get(x) for x in ("verdict", "all_verified", "lido", "does_not_gate_core")}, "veracidade_n_checks": len(tv0.get("checks") or []), "veracidade_checks_falhos": [ck_["descricao"] for ck_ in (tv0.get("checks") or []) if not ck_.get("ok")],
                   "veracidade_fontes": [{"chave": f_["chave"], "sha256": f_["sha256"], "ok": f_["ok"]} for f_ in (tv0.get("fontes") or [])],
                   "registros_v397": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V397_NOMES_REGISTROS}, "registros_v398": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V398_NOMES_REGISTROS}, "sonico_v398": {x: (c.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified", "beta_ok")}, "afinacao_das_cordas_v398": {x: (c.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v399": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V399_NOMES_REGISTROS}, "selo_pela_propria_tecnologia_v399": {x: (c.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified")}, "declaracao_do_operador_v399": {x: (c.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified")}, "recriados_v393_a_v408": recriados, "registros_novos_v409": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V409N},
                   "registros_v402": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in ["ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"] + list(um._V402_NOMES_REGISTROS)},
                   "registros_v401": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in ["falsidade_da_inercia_v401"] + list(um._V401_NOMES_REGISTROS)},
                   "checks_dos_registros_que_falharam": {n_: [ck_ for ck_ in ((c.get(n_) or {}).get("checks") or []) if not ck_.get("ok")][:6] for n_ in list(um._V399_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + um._V397_NOMES_REGISTROS + um._V396_NOMES_REGISTROS + um._V395_NOMES_REGISTROS + um._V394_NOMES_REGISTROS + list(um._V393_NOMES_REGISTROS) if (c.get(n_) or {}).get("all_verified") is not True}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k not in ("stdout", "recriados_v393_a_v408", "veracidade")}, ensure_ascii=False, default=str)[:3800])
# [v407] NAO HA TROCA DITA de veredito (na v408 houve uma: rede_fock_v394 deixou de dizer JOINT_CONTRACT_OPEN). O CANDIDATO_v409.json nao declara nenhuma (a chave `troca_dita_v409` nao existe) e o ensaio COBRA isso: os vereditos de rede_fock_v394, psibit_v395, testemunha_estatica_v396 e fechamento_v406 (e todos os recriados)
# ficam IGUAIS aos da v408 selada ou diferem so' em numeros; texto trocado = reprovacao (rec_ok). A chave `troca_dita_v409` fica no JSON, vazia por desenho, para os leitores (gerar_esperados, p00) da cadeia.
assert "troca_dita_v409" not in CM, ("o candidato declara uma troca dita de veredito; a v409 nao deveria", CM.get("troca_dita_v409"))
_TROCA_DITA_V409 = {}
rep["troca_dita_v409"] = {"declarada_no_candidato": [], "conferida": {}, "antes": {}, "depois": {}, "nota": "nenhuma troca dita na v409: rede_fock_v394, psibit_v395, testemunha_estatica_v396 e fechamento_v406 NAO mudam de prefixo (o que muda e' a chave do lema, que NAO entra em veredito)",
                          "vereditos_dos_quatro_iguais_ao_selado_ou_so_numeros": {k_: bool(recriados[k_]["igual_ao_selado"] or _num(recriados[k_]["antes"]) == _num(recriados[k_]["depois"])) for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406")},
                          "prefixo_de_cada_um_nao_mudou": {k_: recriados[k_]["antes"].split("__")[0] == recriados[k_]["depois"].split("__")[0] for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406")}}
for k_, d_ in list(recriados.items()):
    if not d_["igual_ao_selado"] and _num(d_["antes"]) == _num(d_["depois"]) and d_["all_verified"] is True:
        mud[k_] = {"antes": d_["antes"], "depois": d_["depois"], "so_numeros": True, "all_verified": True}
rec_ok = all(d_["all_verified"] is True and (d_["igual_ao_selado"] or k_ in mud or d_.get("troca_dita") is True) for k_, d_ in recriados.items()) and all(v_ is True for v_ in rep["troca_dita_v409"]["conferida"].values()) and sorted(k_ for k_, d_ in recriados.items() if not d_["igual_ao_selado"] and k_ not in mud) == sorted(_TROCA_DITA_V409) == [] and all(rep["troca_dita_v409"]["vereditos_dos_quatro_iguais_ao_selado_ou_so_numeros"].values()) and all(rep["troca_dita_v409"]["prefixo_de_cada_um_nao_mudou"].values())
_nomes_v = list(mud) + [x.split("(")[0] for x in iguais_v]
_falham_v = [n_ for n_ in _nomes_v if n_ in cs2 and (cs2.get(n_) or {}).get("all_verified") is not True]
_ausentes_v = [n_ for n_ in _nomes_v if n_ not in cs2]
viz_ok = (all(v["so_numeros"] and v["all_verified"] is True for v in mud.values()) and rec_ok and not _falham_v)
rep["viz_det"] = {"mud_so_numeros_e_selados": all(v["so_numeros"] and v["all_verified"] is True for v in mud.values()), "v393_a_v408_recriados_ok": rec_ok, "nao_selados": _falham_v, "ausentes_do_core": _ausentes_v[:10]}
mf_ok = (not _err and novas_chaves == sorted(NOVAS409) and tv0.get("all_verified") is True and all((c.get(n_) or {}).get("all_verified") is True for n_ in list(um._V397_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + list(um._V399_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + V408N + V409N)
         and (c.get("testemunha_estatica_v396") or {}).get("all_verified") is True and (c.get("psibit_v395") or {}).get("all_verified") is True and (c.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is True
         and ((c.get("psibit_v395") or {}).get("conditional_psion_face") or {}).get("inhabitant_exhibited") is True and ((c.get("testemunha_estatica_v396") or {}).get("fock_face") or {}).get("inhabitant_exhibited") is True and (c.get("witness_layers") or {}).get("canonical_full_witness_term_constructed") is True
         and ((c.get("testemunha_estatica_v396") or {}).get("fock_face") or {}).get("linked_to_the_corner_by_a_lemma") is True and (c.get("psion_canto_v407") or {}).get("link_read_from_the_kernel") is True   # (v409) a chave do lema, antes o literal False, le o kernel: True
         and "ADMITTED" in str(((c.get("regra_consumidor_v393") or {}).get("satisfacao") or {}).get("veredito_do_rito")))
# (6) unidade
U = {}
# (5b) [LICAO DA 1a TENTATIVA DO RITO v409, 28/10/2026] A ORDEM DE CHAMADA, estatica (guarda_ordem_de_chamada_v409.py): toda chave do core que uma funcao nova LE e que o main ATRIBUI tem de ser atribuida ANTES da chamada.
# O fluxo (5) nao pega isto (core_s ja' traz as chaves da v408 selada); o rito real pegou: f2b_errata_v404, chamada logo depois do Jo8v32, leu um core sem ramo_b_preregistration_v386, ledger_errata_v386 e the_ledger_of_charges_v383 e RECUSOU as 7 checagens.
import guarda_ordem_de_chamada_v409 as _GOC
_ordem = _GOC.ordem_de_chamada(src, _GOC.FUNCOES_V409)
rep["ordem_de_chamada_v409"] = _ordem
_ctl_ordem = _GOC.controle_negativo(src); rep["ordem_de_chamada_v409_controle_negativo"] = _ctl_ordem
U["v409_ordem_de_chamada_todo_insumo_do_core_pronto_antes_da_leitura_com_controle_negativo"] = bool(_ordem["ok"] and _ctl_ordem["ok"] and all((_ordem["funcoes"].get(n_) or {}).get("n_chaves_lidas", 0) >= 3 for n_ in _GOC.FUNCOES_V409))
print("ordem de chamada (guarda estatica, licao da 1a tentativa):", _ordem["ok"], "| controle negativo:", _ctl_ordem["ok"])
# (5b') [v408] A ORDEM DE CHAMADA DO tetelestai_terminal_v408, medida AQUI por AST (nao depende de a guarda_ordem_de_chamada_v409 conhecer a funcao nova): toda chave do core que o registro LE (tetelestai_terminal_v408, v408_terminal_mechanics, _v408_formal, _v398_beta) tem de estar pronta
# ANTES da instrucao do main que o chama (vem de run_um, ou core["K"] = ..., ou a chamada K(core) numa instrucao anterior); alem disso psion_canto_v407, _v407_rodar_specs, fechamento_v406 e _v406_rodar_specs (os registros herdados que o main roda antes) vem ANTES. Controles negativos: o bloco do terminal movido para antes de run_um, e a chamada do psion_canto_v407 retirada.
_FN_PSION = ("traducao_turing_v409", "v409_traducao_mechanics", "_v409_formal", "_v398_beta")
_EXIG_PSION = ("tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "_v406_rodar_specs", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers")


def _ordem_psion(src_):
    tree_ = ast.parse(src_); defs_ = {}
    for n_ in tree_.body:
        if isinstance(n_, ast.FunctionDef):
            defs_.setdefault(n_.name, []).append(n_)
    main_ = defs_["main"][-1]; run_ = defs_["run_um"][0]
    de_run_ = {k_.value for n_ in ast.walk(run_) if isinstance(n_, ast.Dict) for k_ in n_.keys if isinstance(k_, ast.Constant) and isinstance(k_.value, str)}
    unp_ = [ast.unparse(st_) for st_ in main_.body]; atrib_ = {}
    irun_ = [i_ for i_, st_ in enumerate(main_.body) if "run_um(" in unp_[i_] and isinstance(st_, ast.Assign)][0]   # (v409) as chaves que o run_um produz ficam prontas NESTA instrucao, nao antes: um bloco movido para antes do run_um le chaves ainda nao atribuidas
    for i_, st_ in enumerate(main_.body):
        for n_ in ast.walk(st_):
            if isinstance(n_, ast.Assign):
                for t_ in n_.targets:
                    if isinstance(t_, ast.Subscript) and isinstance(t_.value, ast.Name) and t_.value.id == "core" and isinstance(t_.slice, ast.Constant) and isinstance(t_.slice.value, str):
                        atrib_.setdefault(t_.slice.value, i_)
        for nome_ in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\(core\)", unp_[i_]):
            atrib_.setdefault(nome_, i_)
    for k_ in de_run_:
        atrib_.setdefault(k_, irun_)
    lidas_ = set()
    for fn_ in _FN_PSION:
        for n_ in ast.walk(defs_[fn_][0]):
            if isinstance(n_, ast.Call) and isinstance(n_.func, ast.Attribute) and n_.func.attr == "get" and isinstance(n_.func.value, ast.Name) and n_.func.value.id in ("core", "core_") and n_.args and isinstance(n_.args[0], ast.Constant) and isinstance(n_.args[0].value, str):
                lidas_.add(n_.args[0].value)
            if isinstance(n_, ast.Subscript) and isinstance(n_.value, ast.Name) and n_.value.id in ("core", "core_") and isinstance(n_.slice, ast.Constant) and isinstance(n_.slice.value, str) and not isinstance(n_.ctx, ast.Store):
                lidas_.add(n_.slice.value)
    lidas_.discard("traducao_turing_v409")
    ch_ = [i_ for i_, s_ in enumerate(unp_) if "traducao_turing_v409(core)" in s_]
    if len(ch_) != 1:
        return {"ok": False, "erro": "chamada no main ausente ou nao unica", "indices": ch_}
    ic_ = ch_[0]
    antes_ = sorted(k_ for k_ in lidas_ if k_ in atrib_ and atrib_[k_] >= ic_)   # (v409: as chaves do run_um contam pelo indice do run_um; o terminal le so' chaves do run_um, e o controle (a) so' e' medida se elas contarem)
    sem_origem_ = sorted(k_ for k_ in lidas_ if k_ not in atrib_)
    faltam_ = [k_ for k_ in _EXIG_PSION if not (k_ in atrib_ and atrib_[k_] < ic_)]
    return {"ok": bool(lidas_ and not antes_ and not sem_origem_ and not faltam_), "chamada_indice": ic_, "chamada_linha": main_.body[ic_].lineno, "n_chaves_lidas": len(lidas_), "chaves_lidas": sorted(lidas_), "lidos_antes_da_atribuicao": antes_, "lidas_sem_origem": sem_origem_, "insumos_exigidos_ausentes": faltam_,
            "insumos_exigidos_atribuidos_antes": {k_: atrib_[k_] for k_ in _EXIG_PSION if k_ in atrib_ and atrib_[k_] < ic_}}


_op0 = _ordem_psion(src); _lin = src.split("\n"); _tree0 = ast.parse(src)
_main0 = [n for n in _tree0.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
_ic0 = [i_ for i_, st_ in enumerate(_main0.body) if "traducao_turing_v409(core)" in ast.unparse(st_)][0]; _st0 = _main0.body[_ic0]
_irun = [i_ for i_, st_ in enumerate(_main0.body) if "run_um(" in ast.unparse(st_) and isinstance(st_, ast.Assign)][0]
_bloco = _lin[_st0.lineno - 1:_st0.end_lineno]; _dest = _main0.body[_irun].lineno - 1
_neg_a = _ordem_psion("\n".join(_lin[:_dest] + _bloco + _lin[_dest:_st0.lineno - 1] + _lin[_st0.end_lineno:]))   # (a) o bloco do psion movido para ANTES do run_um
_lin_b = list(_lin); _ln_b = [i_ for i_, l_ in enumerate(_lin_b) if re.fullmatch(r"\s+_r408 = tetelestai_terminal_v408\(core\)\s*", l_)]
assert len(_ln_b) == 1, ("a linha da chamada do tetelestai_terminal_v408 nao foi achada uma vez", _ln_b)
_lin_b[_ln_b[0]] = re.sub(r"_r408 = tetelestai_terminal_v408\(core\)", "_r408 = {}", _lin_b[_ln_b[0]])
_neg_b = _ordem_psion("\n".join(_lin_b))   # (b) a chamada do tetelestai_terminal_v408 (o registro herdado que o main roda logo antes) retirada: o insumo exigido some
rep["ordem_de_chamada_tetelestai_terminal_v409"] = {"real": _op0, "controle_negativo_bloco_antes_do_run_um": {k_: _neg_a.get(k_) for k_ in ("ok", "lidos_antes_da_atribuicao", "insumos_exigidos_ausentes", "erro")}, "controle_negativo_sem_a_chamada_do_fechamento": {k_: _neg_b.get(k_) for k_ in ("ok", "lidos_antes_da_atribuicao", "insumos_exigidos_ausentes", "erro")}}
U["v409_ordem_de_chamada_do_tetelestai_terminal_v409_medida_por_ast_com_dois_controles_negativos"] = bool(_op0["ok"] and _op0["n_chaves_lidas"] >= 4 and _op0["chamada_indice"] == _ic0 and _neg_a["ok"] is False and bool(_neg_a.get("lidos_antes_da_atribuicao")) and _neg_b["ok"] is False and "tetelestai_terminal_v408" in (_neg_b.get("insumos_exigidos_ausentes") or []))
print("ordem de chamada do traducao_turing_v409 (AST propria):", _op0["ok"], "| lidas:", _op0["n_chaves_lidas"], "| controles negativos:", _neg_a["ok"] is False, _neg_b["ok"] is False)
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
    nb = json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8"); td = tempfile.mkdtemp(prefix="v409_ens_"); p = os.path.join(td, os.path.basename(f0["arquivo"])); open(p, "wb").write(nb)
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
    _ant = um._V397_VERBATINS2[_ch]["text"]; um._V397_VERBATINS2[_ch]["text"] += " "   # [v409-patch-b] restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
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
        _ant = um._V398_VERBATINS2[ch_]["text"]; um._V398_VERBATINS2[ch_]["text"] += " "   # [v409-patch-b] restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
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
# (6d) [v399] os DOIS registros com FUNCAO da v409 (selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399): tudo certo, o round trip RECALCULADO aqui por outro caminho, a direcao do testemunho, e cada elo recusa visivelmente (controles negativos)
import time as _tm, tempfile as _tf, numpy as _np
import acom_conferencias_v409 as AC  # noqa: E402
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
# [v409, BAIXA B1 do exame da v408] a checagem «beta do runtime» NAO e' mais tautologica: confronta com o beta do CORE do rito (que o main calcula por outro caminho) a 1e-9
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
U["selo_acom_alfa_do_programa_adulterado_agora_e_pego_pela_checagem_do_beta"] = bool(_rba["all_verified"] is False and _rba["checks"][5][1] is False)   # com a checagem tautologica da v408 isto NAO seria pego
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
# o GATE nao se move [v409: F8.1 -- a prove_qg_closure_gate NOVA (kwarg blind_null) recomputada aqui sobre o kf novo e os dados (V11, teste nulo cego) do core da v408 selada]: o veredito do gate, as chaves e os valores das 18 bandeiras e tudo do qg_closure SALVO a lista de checks (que ganha a sonda nova) sao IGUAIS aos da v408 selada
_n18 = lambda g_: sum(1 for fam_ in ("formal_flags", "physics_flags", "experiment_flags") for v_ in (g_.get(fam_) or {}).values() if v_ is True)
_J = lambda x_: json.dumps(x_, sort_keys=True, default=str)
_g_old = core0.get("qg_closure") or {}
try:
    _g_new = _QG_RECOMP
    _sem_checks = lambda g_: {k_: v_ for k_, v_ in g_.items() if k_ != "checks"}
    gate_rec = {"verdict_igual": (_g_new.get("gate") or {}).get("verdict") == (_g_old.get("gate") or {}).get("verdict"), "n18_novo": _n18(_g_new), "n18_core0": _n18(_g_old),
                "flags_iguais": all(_J(_g_new.get(f_)) == _J(_g_old.get(f_)) for f_ in ("formal_flags", "physics_flags", "experiment_flags")), "chaves_iguais": sorted(_g_new) == sorted(_g_old), "qg_sem_checks_igual": _J(_sem_checks(_g_new)) == _J(_sem_checks(_g_old)),
                "checks_da_v408_iguais": bool(_J(_g_new.get("checks")) == _J(_g_old.get("checks")) and all(v_ is True for _, v_ in _g_new["checks"])),
                "all_verified": _g_new.get("all_verified")}
except Exception as _e:   # noqa: BLE001
    gate_rec = {"EXCECAO": repr(_e)[:300]}
gate_rec["qg_closure_do_core_intocado_pelo_fluxo"] = _J(c.get("qg_closure")) == _J(_QG_RECOMP)   # o fluxo (as instrucoes do main) nao toca o qg_closure recomputado
rep["gate_recomputado"] = gate_rec
U["gate_nao_se_move"] = bool(gate_rec.get("verdict_igual") and gate_rec.get("n18_novo") == 18 == gate_rec.get("n18_core0") and gate_rec.get("flags_iguais") and gate_rec.get("chaves_iguais") and gate_rec.get("qg_sem_checks_igual") and gate_rec.get("checks_da_v408_iguais") and gate_rec.get("all_verified") is True and gate_rec.get("qg_closure_do_core_intocado_pelo_fluxo"))
# (6b) os registros por spec: cada um recusa visivelmente (fonte adulterada; verbatim adulterado; bandeira do kernel faltando; cada check negado) -- v394, v395, v396, v397, v408 e v409 (mais o spec de veracidade)
RU = {}
for sp_ in list(um._V394_SPECS) + list(um._V395_SPECS) + list(um._V396_SPECS) + [VER] + list(um._V397_SPECS) + list(um._V398_SPECS) + list(um._V399_SPECS) + list(um._V401_SPECS) + list(um._V402_SPECS) + list(um._V403_SPECS) + list(um._V404_SPECS) + list(um._V405_SPECS) + list(um._V406_SPECS) + list(um._V407_SPECS) + list(um._V408_SPECS):
    n_ = sp_["nome"]; r_ = {}
    ch_ = sp_["fontes"][0]; ant_ = dict(um._V392_FONTES[ch_]); um._V392_FONTES[ch_]["sha256"] = "0" * 64
    try:
        r_["fonte_adulterada"] = um._v392_registro(sp_, core_s)["all_verified"] is False
    finally:
        um._V392_FONTES[ch_] = ant_
    for vch_ in sp_.get("verbatins", []):
        ant_ = um._V392_VERBATINS2[vch_]["text"]; um._V392_VERBATINS2[vch_]["text"] += " "   # [v409-patch-b] restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
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
U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V394_SPECS) + len(um._V395_SPECS) + len(um._V396_SPECS) + 1 + len(um._V397_SPECS) + len(um._V398_SPECS) + len(um._V399_SPECS) + len(um._V401_SPECS) + len(um._V402_SPECS) + len(um._V403_SPECS) + len(um._V404_SPECS) + len(um._V405_SPECS) + len(um._V406_SPECS) + len(um._V407_SPECS) + len(um._V408_SPECS)
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
seal.update(um.resumos_do_selo_v399(c))   # v399/v409: o resumo da segunda testemunha e da declaracao do operador (a instrucao seal.update do main, que o ensaio nao executa por ser fora do fluxo etiquetado)
J_ = lambda x: json.dumps(x, sort_keys=True, default=str)
mud_selo = sorted(k for k in seal if J_(seal.get(k)) != J_(selo0.get(k)))
rep["selo"] = {"erro": _seal_err, "chaves_do_selo": len(seal), "difere_do_selo_v408": mud_selo, "teste_de_veracidade_fase9_v397_no_selo": {x: (seal.get("teste_de_veracidade_fase9_v397") or {}).get(x) for x in ("verdict", "all_verified", "lido")}, "registros_v397": seal.get("registros_v397"), "sonico_v408_no_selo": {x: (seal.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "afinacao_v408_no_selo": {x: (seal.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v398": seal.get("registros_v398"), "selo_pela_propria_tecnologia_v409_no_selo": {x: (seal.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified", "perfil", "controles_negativos")}, "declaracao_do_operador_v409_no_selo": {x: (seal.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified", "verbatim_sha256")}, "registros_v399": seal.get("registros_v399"), "falsidade_da_inercia_v409_no_selo": {x: (seal.get("falsidade_da_inercia_v401") or {}).get(x) for x in ("verdict", "all_verified", "unconditional", "key_theorem", "costless")}, "registros_v401": seal.get("registros_v401")}
print("selo: difere em", mud_selo)
_c_dump = dict(c); _c_dump["the_iald_index"] = um.prove_the_iald_index(copy.deepcopy(c))   # o main do rito poe o indice qualificado no core; o ensaio o computa a parte
json.dump({"core": _c_dump, "verdict": verdict}, open(os.path.join(DRY, "core_ensaio.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str); json.dump(seal, open(os.path.join(DRY, "selo_ensaio.json"), "w", encoding="utf-8"), ensure_ascii=False, default=str)
# [v400] o que pode diferir do selo da v408 SELADA: (i) selo_pela_propria_tecnologia_v399, um_version e sha256 (os hashes do novo um.py -- o proprio proposito da versao); (ii) UMA chave que carrega o hash do proprio programa:
#   estatuto_da_prova_v391 (a certificacao pelo proprio hash: o UNICO campo que muda e' o hash do um.py, o do candidato no lugar do da v408)
_H_ANTES = hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest(); _H_DEPOIS = hashlib.sha256(_UMB).hexdigest()


def _selo_explica(k_):   # [v409-patch-d]
    a_, b_ = selo0.get(k_), seal.get(k_)
    if k_ in ("estatuto_da_prova_v391", "pedras_v392", "pedras_v393", "varredura_e_sorry_v392", "three_stress_tests_v387"):
        # so' o VEREDITO muda, e so' em numeros (a escada, as declaracoes, a contagem de arquivos e de vereditos) e no hash do proprio um.py; o registro segue selado
        va, vb = str((a_ or {}).get("verdict")), str((b_ or {}).get("verdict"))
        va = va.replace(_H_ANTES, _H_DEPOIS).replace(_H_ANTES[:16], _H_DEPOIS[:16])
        return bool(va != str((a_ or {}).get("verdict")) or va != vb) and _num(_nc(va)) == _num(_nc(vb)) and (b_ or {}).get("all_verified") is True
    # o hash das fontes formais: o do kf do rito simulado (o kernel embutido do candidato + os residuais do Nos), diferente do da base porque o kernel ganhou o arquivo da pedra
    if k_ == "formal_source_hash":
        return bool(isinstance(b_, str) and len(b_) == 64 and a_ != b_ and b_ == kf.get("formal_source_hash"))
    # [v408] NENHUMA chave antiga muda: fechamento_v406, testemunha_estatica_v396, psion_canto_v407, rede_fock_v394, psibit_v395 e os specs antigos NAO podem diferir no resumo do selo; se diferirem, ficam inexplicados e reprovam (as chaves NOVAS sao tetelestai_terminal_v408 e registros_v408)
    return False


_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v409") + tuple(um._V409_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v409: as chaves NOVAS do selo sao traducao_turing_v409 e registros_v409)
rep["selo"]["difere_e_nao_e_so_o_esperado"] = _selo_inexplicado
selo_ok = (not _seal_err and (seal.get("teste_de_veracidade_fase9_v397") or {}).get("all_verified") is True and all(((seal.get("registros_v397") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V397_NOMES_REGISTROS)
           and (seal.get("sonico_v398") or {}).get("all_verified") is True and (seal.get("afinacao_das_cordas_v398") or {}).get("all_verified") is True and all(((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V398_NOMES_REGISTROS)
           and (seal.get("falsidade_da_inercia_v401") or {}).get("all_verified") is True and all(((seal.get("registros_v401") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V401_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402")) and all(((seal.get("registros_v402") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V402_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403")) and all(((seal.get("registros_v403") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V403_NOMES_REGISTROS)
           and (seal.get("selo_pela_propria_tecnologia_v399") or {}).get("all_verified") is True and (seal.get("declaracao_do_operador_v399") or {}).get("all_verified") is True and all(((seal.get("registros_v399") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V399_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404")) and all(((seal.get("registros_v404") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V404_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V405_REGISTROS_FUNCAO) and all(((seal.get("registros_v405") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V405_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V406_REGISTROS_FUNCAO) and all(((seal.get("registros_v406") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V406_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V409_REGISTROS_FUNCAO) and all(((seal.get("registros_v409") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V409_NOMES_REGISTROS)
           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V408_REGISTROS_FUNCAO) and all(((seal.get("registros_v408") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V408_NOMES_REGISTROS) and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V407_REGISTROS_FUNCAO) and all(((seal.get("registros_v407") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V407_NOMES_REGISTROS)
           and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and (({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v409"} | set(um._V409_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado
                                                                                      and not ({"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "registros_v406", "registros_v407", "registros_v408"} & set(mud_selo)))   # (v409: o resumo do selo de rede_fock_v394, psibit_v395 e dos specs da v408 NAO muda)
           and all(k in selo0 for k in ("fail_closed_selftest", "rite_checkpoints", "not_sealed_this_run")))
# (6e) [v399] o SIDECAR um_absoluto_selo_acom.json sobre o core e o selo DESTE ensaio (as copias de dry): os tres objetos selados e verificados, o SHA-256 ao lado, deterministico (dois ritos seguidos), a honestidade e o tempo
_td = tempfile.mkdtemp(prefix="v409_sidecar_"); _oo = um.OUT
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
# (6f) [v401, recriado na v402, na v403, na v408 e na v409 e comparado com o selado] o registro com FUNCAO falsidade_da_inercia_v401: tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as cinco inscricoes e as ratificacoes
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
# (6g) [v402, recriados na v403 e comparados com os selados] os TRES registros com FUNCAO da v402 (ponte_da_escala_dual_v402, queda_sem_geometria_v402, esperanca_condicional_v402): tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as tres inscricoes de 26/10, as decisoes, as erratas E1-E4 e o spec da cobertura
import types as _types2
_REG402 = (("ponte", "ponte_da_escala_dual_v402", "exp"), ("queda", "queda_sem_geometria_v402", "exp"), ("esperanca", "esperanca_condicional_v402", "sin"))
R402 = {}
_bf2 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
for k402_, n402_, tamper_ in _REG402:
    fn_ = getattr(um, n402_); C_ = um._V402_CONTRACTS[k402_]; T_ = um._V402_TEXTS[k402_]
    r_ = fn_(cs()); R402[k402_] = r_
    U["v402_%s_tudo_certo" % k402_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.D2.N_CHECKS[k402_]
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True)
    U["v402_%s_veredito_e_textos_sem_palavra_proibida" % k402_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v402_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k402_] = bool(ok_ and len(C_["theorems"]) == len(DL.D2.STONE_BY_KEY[k402_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
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
U["cunhagens_v402_tres_falas_decisoes_erratas_e_leitura_de_26out"] = bool(_cn2.get("all_verified") is True and len(_cn2.get("verbatim") or {}) == len(DL.D2.VERBATIM_ORIGEM_V402) == 3 and all(v_["embedded_ok"] for v_ in (_cn2.get("verbatim") or {}).values())
                                                                          and len(_cn2.get("erratas") or []) == 4 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn2.get("erratas") or [])) and "REFUTADA" in (_cn2.get("erratas") or [{}])[0].get("agora", "")
                                                                          and len(_cn2.get("leituras_do_operador") or []) == len(_sp2["leituras_do_operador"]) and set((_cn2.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D11", "D12", "D13", "D14", "D15", "D16"}
                                                                          and ((_cn2.get("extras") or {}).get("leitura_26out_direcao") or {}).get("resposta") == "a seta da queda da fase, nao do espaco" and (_cn2.get("extras") or {}).get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.D2.STONES}
                                                                          and (_cn2.get("extras") or {}).get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.D2.STONES} and len((_cn2.get("extras") or {}).get("erratas_E1_a_E4") or []) == 4)
U["contratos_v394_a_v401_pinam_a_escada_da_v403"] = bool(all(getattr(um, nm_)["expected_ladder"] == ESP for nm_ in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT")))
rep["v402_registros"] = {k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_["unconditional"], "key_theorem": r_["key_theorem"], "context": r_["context"]} for k_, r_ in R402.items()}
# (6h) [v403, recriados na v408 e comparados com os selados] os QUATRO registros com FUNCAO da v403 (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403): tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos); as duas falas de 27/10, as decisoes, as erratas E5-E6, o gate recalculado (F8.1) e os specs
import types as _types3
_REG403 = (("caminho", "caminho_v403", "exp"), ("vida", "vida_v403", "exp"), ("verdade_adendo", "verdade_adendo_v403", "sqrt"))
R403 = {}
_bf3 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
for k403_, n403_, tamper_ in _REG403:
    fn_ = getattr(um, n403_); C_ = um._V403_CONTRACTS[k403_]; T_ = um._V403_TEXTS[k403_]
    r_ = fn_(cs()); R403[k403_] = r_
    U["v403_%s_tudo_certo" % k403_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.D3.N_CHECKS[k403_]
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True)
    U["v403_%s_veredito_e_textos_sem_palavra_proibida" % k403_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v403_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k403_] = bool(ok_ and len(C_["theorems"]) == len(DL.D3.STONE_BY_KEY[k403_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
    ok_ = True
    for th_ in list(C_["theorems"]) + list(C_["support"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v403_%s_axioma_fora_do_trio_em_cada_termo_lido_recusa" % k403_] = bool(ok_)
    ok_ = True
    for th_ in [C_["unconditional"]["theorem"], C_["key_theorem"]["theorem"]] + list(C_["support"]):   # proveniencia errada
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v403_%s_proveniencia_errada_recusa" % k403_] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][C_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[C_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v403_%s_fonte_da_pedra_adulterada_recusa" % k403_] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U["v403_%s_escada_errada_ou_kernel_nao_verificado_recusa" % k403_] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in C_["verbatins"]:
        _ant = um._V403_VERBATINS2[ch_]["text"]; um._V403_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (v403) (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V403_VERBATINS2[ch_]["text"] = _ant
    U["v403_%s_inscricao_adulterada_recusa" % k403_] = bool(ok_ and len(C_["verbatins"]) == {"caminho": 2, "vida": 2, "verdade_adendo": 2}[k403_])
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); _cp = C_["context"]["path"]; um._EMBEDDED_KERNEL_FILES[_cp] = um._EMBEDDED_KERNEL_FILES[_cp].replace(C_["context"]["needles"][0], "xx")
    try:
        rr_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v403_%s_texto_contexto_retirado_do_kernel_recusa" % k403_] = bool(r_["context"]["ok"] is True and rr_["all_verified"] is False and rr_["context"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
    c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = fn_(c_)
    _a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
    try:
        _ra = fn_(cs())
    finally:
        um.SEALED_CODATA_ALPHA = _a0
    U["v403_%s_beta_adulterado_recusa" % k403_] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
    _m0 = um._m403
    um._m403 = _types3.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); setattr(um._m403, tamper_, (lambda f_: (lambda x_: f_(x_) * 1.001))(getattr(_math, tamper_)))
    try:
        _rn = fn_(cs())
    finally:
        um._m403 = _m0
    U["v403_%s_numero_adulterado_recusa" % k403_] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
_cv3, _vv3, _av3 = R403["caminho"]["values"], R403["vida"]["values"], R403["verdade_adendo"]["values"]
_eps3 = (1e-3, 1e-6, 1e-12, 1e-30)
_al3 = um.SEALED_CODATA_ALPHA
U["v403_caminho_numeros_recalculados_aqui"] = bool(abs(_cv3["beta"] - _bf3) <= 1e-15 and abs(_cv3["pplus_factor_at_beta"] - _math.exp(-_bf3)) <= 1e-15 and [round(x_, 9) for x_ in _cv3["lifts_same_pplus_masses"]] == [1.0, 4.0, 9.0] and _cv3["same_pplus"] == 2.0
                                                   and abs(_cv3["min_core_energy"] - 0.25) <= 1e-15 and abs(_cv3["min_rest_energy_gain"] - 2.0 * (_math.cosh(0.25) - 1.0)) <= 1e-12 and _cv3["grid_scales"] == 25 and _cv3["mu2_grid"] == [0.0, 0.25, 1.0, 4.0, 9.0, 100.0] and _cv3["profiles"] == [0.5, 2.0, 3.0])
U["v403_vida_numeros_recalculados_aqui"] = bool(abs(_vv3["beta"] - _bf3) <= 1e-15 and abs(_vv3["post_weight_at_scale_one"] - _math.exp(-1.0)) <= 1e-15 and abs(_vv3["post_weight_at_minus_one"] - _math.e) <= 1e-12 and abs(_vv3["min_cost_t_beta_g"] - 0.1 * _bf3 * 0.5) <= 1e-18
                                                and abs(_vv3["max_dephasing_factor"] - _math.exp(-0.1 * _bf3 * 0.5)) <= 1e-15 and abs(_vv3["dephasing_factor_at_t1_g1"] - _math.exp(-_bf3)) <= 1e-15 and abs(_vv3["loss_per_unit"] - (1.0 - _math.exp(-_bf3))) <= 1e-15 and _vv3["grid_scales"] == 161
                                                and _vv3["angular_period"] == 2.0 * _math.pi and _vv3["finite_model_group_order"] == 12 and [[e_, s_] for e_, s_ in ((e_, -_math.log(e_) + 1.0) for e_ in _eps3)] == _vv3["abyss_witnesses"])
U["v403_verdade_adendo_numeros_recalculados_aqui"] = bool(abs(_av3["beta"] - _bf3) <= 1e-15 and abs(_av3["alpha"] - _al3) <= 1e-16 and abs(_av3["alpha_squared"] - _al3 ** 2) <= 1e-18 and abs(_av3["q_squared_at_alpha"] - (1.0 - _al3 ** 2)) <= 1e-15 and abs(_av3["weights_sum"] - 1.0) <= 1e-15
                                                          and abs(_av3["trace_after_name"] - 1.0) <= 1e-15 and _av3["test_points"] == 6 and _av3["alpha_squared_below_beta"] is True and _av3["alpha_squared"] < _bf3)
_dk3 = hashlib.sha256(um._EMBEDDED_KERNEL_FILES["TGLExt/Verdade.lean"].encode("utf-8")).hexdigest()[:16]
U["v403_a_leitura_pela_tripla_espectral_e_onto_o_nome_e_do_operador_e_as_pedras_da_v402_ficam_como_registro"] = bool(
    all(R403[k_]["spectral_triple_reading"]["status"] == "ONTO" and R403[k_]["spectral_triple_reading"]["is_a_kernel_term"] is False and R403[k_]["name_given_by"]["quem"] == "operador" and R403[k_]["name_given_by"]["sha16_da_fala"] == DL.verbatins403(os.path.join(HERE, "insumos", "cunhagens"))[1]["sha16"]
        and any("TRIPLO inteiro" in x_ for x_ in R403[k_]["nao_diz"]) for k_ in ("caminho", "vida", "verdade_adendo"))
    and R403["caminho"]["sealed_v402_stone_kept_as_record"]["sha16"] == DL.D2.STONE_BY_KEY["ponte"]["sha16_da_ordem"] and R403["vida"]["sealed_v402_stone_kept_as_record"]["sha16"] == DL.D2.STONE_BY_KEY["queda"]["sha16_da_ordem"] and R403["verdade_adendo"]["sealed_v402_stone_kept_as_record"]["sha16"] == DL.D2.STONE_BY_KEY["esperanca"]["sha16_da_ordem"])
U["v403_verdade_adendo_a_pedra_verdade_v392_fica_intacta_o_indice_segue_condicional_e_a_estrela_e_nova"] = bool(R403["verdade_adendo"]["stone_verdade_v392_untouched"]["sha16"] == _dk3 and R403["verdade_adendo"]["index_conditional"]["instance_built"] is False and R403["verdade_adendo"]["index_conditional"]["hypotheses"] == ["hpp", "hopt"]
                                                                                               and R403["verdade_adendo"]["star"]["new_and_small"] is True and R403["verdade_adendo"]["alpha_is_a_parameter"] is True and "Posto.endpoint_eq" not in json.dumps(R403["verdade_adendo"]["limites"]))
U["v403_vida_o_chao_e_o_posto_a_isotropia_e_nomeada_e_a_dimensao_nao_e_provada"] = bool(R403["vida"]["floor"]["is_never"].startswith("the infimum 0") and R403["vida"]["named_hypothesis"]["name"] == "IsotropicPost" and R403["vida"]["named_hypothesis"]["status"] == "OPEN" and R403["vida"]["reading_1_plus_3"]["dimension_three_proved"] is False)
U["v403_caminho_as_pendencias_nomeadas_da_ponte_seguem_abertas_e_h_tau_segue_refutada"] = bool([x_["name"] for x_ in R403["caminho"]["named_pending"]] == ["H_BW", "H_cal", "H3", "signature", "rank_c_4"] and all(x_["status"] == "OPEN" for x_ in R403["caminho"]["named_pending"]) and any("REFUTADA" in x_ for x_ in R403["caminho"]["limites"]))
# --- o registro bandeiras_do_gate_v403 (F8.1): tudo certo e cada elo recusa
rg_ = um.bandeiras_do_gate_v403(cs()); R403["gate"] = rg_
C_g = um._V403_CONTRACTS["gate"]; T_g = um._V403_TEXTS["gate"]
U["v403_bandeiras_tudo_certo"] = bool(rg_["all_verified"] is True and rg_["verdict"] == T_g["veredito_ok"] and rg_["runtime_executed"] is True and rg_["does_not_gate_core"] is True and rg_["mechanics"]["n_checks"] == DL.D3.N_CHECKS["gate"] == len(rg_["mechanics"]["checks"]) and all(ck_["ok"] for ck_ in rg_["mechanics"]["checks"])
                                      and rg_["values"]["n_flags"] == 18 and rg_["values"]["n_true"] == 18 and rg_["values"]["n_calculated"] == 18 and rg_["values"]["n_literal"] == 0 and rg_["values"]["read_by_the_verdict"] == [6, 5, 4] and rg_["values"]["gate_verdict_equals_v402"] is True
                                      and rg_["values"]["n_gate_checks"] == 7 and len(rg_["flags"]) == 18 and sorted(rg_["values"]["informative"]) == sorted(DL.F81_LITERAIS) and rg_["values"]["feed_single_boolean"] is True)
U["v403_bandeiras_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(rg_) and not _GUARDA98.search(rg_["verdict"]) and not rg_["guarda_p18_violacoes"] and not um._v392_guarda_texto(json.dumps(rg_["mechanics"]["checks"], ensure_ascii=False)))
ok_ = True
for fam_ in ("formal_flags", "physics_flags", "experiment_flags"):
    for nome_ in list(cs()["qg_closure"][fam_]):   # CADA UMA das 18 bandeiras False no gate do core: o registro recusa
        c_ = cs(); c_["qg_closure"][fam_][nome_] = False; rr_ = um.bandeiras_do_gate_v403(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "REFUSED" in rr_["verdict"]
U["v403_bandeiras_cada_uma_das_18_False_no_gate_do_core_recusa"] = bool(ok_)
ok_ = True
c_ = cs(); c_["kernel_formalization"][C_g["ls2_flags"][0]] = False; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["checks"] = [x_ for x_ in c_["void_floor_v11"]["checks"] if x_[0] != DL.F81_ROTULO_PREREG]; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["checks"] = list(c_["void_floor_v11"]["checks"]) + [[DL.F81_ROTULO_PREREG, True]]; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["checks"] = [[x_[0], (False if x_[0] == DL.F81_ROTULO_PREREG else x_[1])] for x_ in c_["void_floor_v11"]["checks"]]; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_["void_stacking_blind"]["all_verified"] = False; rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
c_ = cs(); c_.pop("void_stacking_blind"); rr_ = um.bandeiras_do_gate_v403(c_); ok_ = ok_ and rr_["all_verified"] is False
U["v403_bandeiras_cada_fonte_das_tres_que_eram_literais_tirada_ou_falsa_recusa"] = bool(ok_)
ok_ = True
c_ = cs(); c_["qg_closure"]["gate"]["verdict"] = c_["qg_closure"]["gate"]["verdict"] + "_X"; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["qg_closure"]["checks"] = c_["qg_closure"]["checks"][:5] + c_["qg_closure"]["checks"][6:]; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["qg_closure"]["checks"] = [list(x_) for x_ in c_["qg_closure"]["checks"]]; c_["qg_closure"]["checks"][5][1] = False; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["experiment_feed"]["independent_v3_profiles_unblinded"] = False; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["void_floor_v11"]["verdict"] = "TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS"; ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
c_ = cs(); c_["qg_closure"].pop("physics_flags"); ok_ = ok_ and um.bandeiras_do_gate_v403(c_)["all_verified"] is False
U["v403_bandeiras_veredito_diferente_sonda_ausente_ou_falsa_feed_quebrado_e_gate_incompleto_recusam"] = bool(ok_)
_se3, _sp3 = um._v403_fontes_do_gate()
_lid3, _lit3 = um._v403_ast_do_gate(_se3, _sp3)
import ast as _ast3


def _mut_literal3(src_, chave_):
    """o codigo do chamador com a bandeira `chave_` ATRIBUIDA POR LITERAL (o defeito que a F8.1 conserta)"""
    t_ = _ast3.parse(textwrap.dedent(src_))
    for n_ in _ast3.walk(t_):
        if isinstance(n_, _ast3.Dict):
            for i_, k_ in enumerate(n_.keys):
                if isinstance(k_, _ast3.Constant) and k_.value == chave_:
                    n_.values[i_] = _ast3.Constant(value=True)
        if isinstance(n_, _ast3.Assign) and len(n_.targets) == 1 and isinstance(n_.targets[0], _ast3.Subscript) and isinstance(n_.targets[0].slice, _ast3.Constant) and n_.targets[0].slice.value == chave_:
            n_.value = _ast3.Constant(value=True)
    return _ast3.unparse(t_)


_f0_ = um._v403_fontes_do_gate
ok_ = True
try:
    for ch_ in DL.F81_LITERAIS:
        _mut_ = _mut_literal3(_sp3, ch_)
        ok_ = ok_ and ("experiment" if ch_ != "linearized_spin2_finite_face" else "physics", ch_) in um._v403_ast_do_gate(_se3, _mut_)[1]
        um._v403_fontes_do_gate = (lambda m_: (lambda: (_se3, m_)))(_mut_)
        ok_ = ok_ and um.bandeiras_do_gate_v403(cs())["all_verified"] is False
finally:
    um._v403_fontes_do_gate = _f0_
U["v403_bandeiras_o_codigo_do_gate_sem_literal_le_6_5_4_e_cada_literal_reinjetado_e_visto_e_recusado"] = bool(_lit3 == [] and [len(_lid3[g_]) for g_ in ("formal", "physics", "experiment")] == [6, 5, 4] and ok_ and um.bandeiras_do_gate_v403(cs())["all_verified"] is True)
# --- a F8.1 na prove_qg_closure_gate: cada fonte tirada derruba a bandeira dela (e so' a dela) sem mover o veredito; sem blind_null a bandeira informativa e' False; o veredito e as chaves nao mudam
_kf3 = core_s["kernel_formalization"]; _v11_3 = core_s["void_floor_v11"]; _bl3 = core_s["void_stacking_blind"]; _g0_3 = core0["qg_closure"]
_gok3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3, blind_null=_bl3)
_kf_sem3 = {k_: v_ for k_, v_ in _kf3.items() if not k_.startswith(DL.F81_PREFIXO_LS2)}
_g_ls3 = um.prove_qg_closure_gate(1.0, _kf_sem3, independent_rite=_v11_3, blind_null=_bl3)
_v11_sem3 = dict(_v11_3, checks=[x_ for x_ in _v11_3["checks"] if x_[0] != DL.F81_ROTULO_PREREG]); _g_pre3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_sem3, blind_null=_bl3)
_v11_dup3 = dict(_v11_3, checks=list(_v11_3["checks"]) + [[DL.F81_ROTULO_PREREG, True]]); _g_dup3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_dup3, blind_null=_bl3)
_g_bl3 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3); _g_bl4 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3, blind_null={"all_verified": False}); _g_bl5 = um.prove_qg_closure_gate(1.0, _kf3, independent_rite=_v11_3, blind_null={"all_verified": 1})
_so_uma = lambda g_, fam_, nome_: all(g_[fam_][k_] is (False if k_ == nome_ else True) for k_ in g_[fam_]) and all(g_[f2_][k_] is True for f2_ in ("formal_flags", "physics_flags", "experiment_flags") if f2_ != fam_ for k_ in g_[f2_])
U["gate_f81_com_as_fontes_o_gate_recomputado_e_igual_ao_da_v403_inclusive_os_checks"] = bool(_gok3["gate"]["verdict"] == _g0_3["gate"]["verdict"] and all(json.dumps(_gok3[f_], sort_keys=True) == json.dumps(_g0_3[f_], sort_keys=True) for f_ in ("formal_flags", "physics_flags", "experiment_flags")) and sorted(_gok3) == sorted(_g0_3)
                                                                                        and json.dumps({k_: v_ for k_, v_ in _gok3.items() if k_ != "checks"}, sort_keys=True, default=str) == json.dumps({k_: v_ for k_, v_ in _g0_3.items() if k_ != "checks"}, sort_keys=True, default=str) and json.dumps(_gok3["checks"], default=str) == json.dumps(_g0_3["checks"], default=str) and all(v_ is True for _, v_ in _gok3["checks"]))
U["gate_f81_sem_a_familia_ext_ls2_do_kernel_so_a_bandeira_fisica_informativa_cai_e_o_veredito_nao_muda"] = bool(_so_uma(_g_ls3, "physics_flags", "linearized_spin2_finite_face") and _g_ls3["gate"]["verdict"] == _g0_3["gate"]["verdict"] and _g_ls3["all_verified"] is True)
U["gate_f81_sem_a_checagem_do_pre_registro_ou_duplicada_ou_falsa_so_a_bandeira_experimental_informativa_cai_e_o_veredito_nao_muda"] = bool(_so_uma(_g_pre3, "experiment_flags", "protocol_pre_registered") and _so_uma(_g_dup3, "experiment_flags", "protocol_pre_registered") and _g_pre3["gate"]["verdict"] == _g_dup3["gate"]["verdict"] == _g0_3["gate"]["verdict"])
U["gate_f81_sem_blind_null_ou_com_all_verified_falso_ou_nao_booleano_so_null_tests_passed_blind_cai_e_o_veredito_nao_muda"] = bool(_so_uma(_g_bl3, "experiment_flags", "null_tests_passed_blind") and _so_uma(_g_bl4, "experiment_flags", "null_tests_passed_blind") and _so_uma(_g_bl5, "experiment_flags", "null_tests_passed_blind")
                                                                                                                                            and _g_bl3["gate"]["verdict"] == _g_bl4["gate"]["verdict"] == _g0_3["gate"]["verdict"] and _g_bl3["all_verified"] is True and _g_bl3["checks"][5][1] is True and str(_g_bl3["checks"][5][0]).startswith("ProbeBlindNullAbsent"))
# --- as duas falas de 27/10, as decisoes D17-D22, as erratas E5-E6 e a leitura da tripla (registro cunhagens_v403) e a cobertura exata (kh_n1_cobertura_v403)
_cn3 = c.get("cunhagens_v403") or {}
_sp3s = [s_ for s_ in um._V403_SPECS if s_["nome"] == "cunhagens_v403"][0]
U["cunhagens_v403_duas_falas_decisoes_erratas_e_leitura_da_tripla"] = bool(_cn3.get("all_verified") is True and len(_cn3.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V403) == 2 and all(v_["embedded_ok"] for v_ in (_cn3.get("verbatim") or {}).values())
                                                                           and len(_cn3.get("erratas") or []) == 2 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn3.get("erratas") or []))
                                                                           and len(_cn3.get("leituras_do_operador") or []) == len(_sp3s["leituras_do_operador"]) == 4 and set((_cn3.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D17", "D18", "D19", "D20", "D21", "D22"}
                                                                           and (_cn3.get("extras") or {}).get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.D3.STONES} and (_cn3.get("extras") or {}).get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.D3.STONES}
                                                                           and len((_cn3.get("extras") or {}).get("erratas_E5_e_E6") or []) == 2 and str(((_cn3.get("extras") or {}).get("nomes") or {}).get("triplo_inteiro", "")).startswith("sem nome")
                                                                           and "ONTO" in str((_cn3.get("extras") or {}).get("leitura_tripla_27out", {}).get("estatuto", "")))
_kh3 = c.get("kh_n1_cobertura_v403") or {}
_kh2s = [s_ for s_ in um._V402_SPECS if s_["nome"] == "kh_n1_cobertura_v402"][0]; _kh1s2 = [s_ for s_ in um._V401_SPECS if s_["nome"] == "kh_n1_cobertura_v401"][0]
_op_piso = {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"}
U["kh_n1_cobertura_v401_e_v402_viraram_piso_e_o_da_v403_tambem"] = bool(_kh3.get("all_verified") is True and (c.get("kh_n1_cobertura_v402") or {}).get("all_verified") is True and (c.get("kh_n1_cobertura_v401") or {}).get("all_verified") is True
                                                                          and {ck_["id"]: ck_["op"] for ck_ in _kh2s["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh2s["erratas"]) >= 1 and {ck_["id"]: ck_["op"] for ck_ in _kh1s2["checks"] if ck_["id"] in _op_piso} == _op_piso
                                                                          and {ck_["id"]: ck_["op"] for ck_ in [s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]["checks"] if ck_["id"] in _op_piso} == _op_piso and len([s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]["erratas"]) >= 1)
U["contratos_v402_pinam_a_escada_da_v403"] = bool(len(um._V402_CONTRACTS) == 3 and all(c3_["expected_ladder"] == ESP for c3_ in um._V402_CONTRACTS.values()))
rep["v403_registros"] = {**{k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_["unconditional"], "key_theorem": r_["key_theorem"], "context": r_["context"]} for k_, r_ in R403.items() if k_ != "gate"},
                         "gate": {"verdict": R403["gate"]["verdict"], "all_verified": R403["gate"]["all_verified"], "n_checks": R403["gate"]["mechanics"]["n_checks"], "values": R403["gate"]["values"]}}
# (6i) [v408, recriados na v409 e comparados com os selados] os TRES registros com FUNCAO da v408 (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404): tudo certo, os numeros RECALCULADOS aqui por outro caminho e cada elo recusa visivelmente (controles negativos); as nove falas de 28/10, as decisoes D23-D26, as erratas E7-E9, a cobertura exata (specs) e o V1/livro/neutrino NAO reescritos
import types as _types4
_REG408 = (("projecao", "projecao_transversal_v404", "_m404", "sin"), ("jo8v32", "jo8v32_v404", "_m403", "exp"))
R408 = {}
_bf4 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_nm_antes4 = json.dumps(cs()["neutrino_mass"], sort_keys=True, default=str)
for k408_, n408_, malias_, tamper_ in _REG408:
    fn_ = getattr(um, n408_); C_ = um._V404_CONTRACTS[k408_]; T_ = um._V404_TEXTS[k408_]
    cc4_ = cs(); r_ = fn_(cc4_); R408[k408_] = r_
    U["v408_%s_tudo_certo" % k408_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.D4.N_CHECKS[k408_] == len(r_["mechanics"]["checks"])
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True)
    U["v408_%s_veredito_e_textos_sem_palavra_proibida" % k408_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v408_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k408_] = bool(ok_ and len(C_["theorems"]) == len(DL.D4.STONE_BY_KEY[k408_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
    ok_ = True
    for th_ in list(C_["theorems"]) + list(C_["support"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v408_%s_axioma_fora_do_trio_em_cada_termo_lido_recusa" % k408_] = bool(ok_)
    ok_ = True
    for th_ in [C_["unconditional"]["theorem"], C_["key_theorem"]["theorem"]] + list(C_["support"]):   # proveniencia errada
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v408_%s_proveniencia_errada_recusa" % k408_] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][C_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[C_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v408_%s_fonte_da_pedra_adulterada_recusa" % k408_] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U["v408_%s_escada_errada_ou_kernel_nao_verificado_recusa" % k408_] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in C_["verbatins"]:
        _ant = um._V404_VERBATINS2[ch_]["text"]; um._V404_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (v408) (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V404_VERBATINS2[ch_]["text"] = _ant
    U["v408_%s_inscricao_adulterada_recusa" % k408_] = bool(ok_ and len(C_["verbatins"]) == {"projecao": 4, "jo8v32": 2}[k408_])
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); _cp = C_["context"]["path"]; um._EMBEDDED_KERNEL_FILES[_cp] = um._EMBEDDED_KERNEL_FILES[_cp].replace(C_["context"]["needles"][0], "xx")
    try:
        rr_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v408_%s_texto_contexto_retirado_do_kernel_recusa" % k408_] = bool(r_["context"]["ok"] is True and rr_["all_verified"] is False and rr_["context"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
    c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = fn_(c_)
    _a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
    try:
        _ra = fn_(cs())
    finally:
        um.SEALED_CODATA_ALPHA = _a0
    U["v408_%s_beta_adulterado_recusa" % k408_] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
    _m0 = getattr(um, malias_)
    setattr(um, malias_, _types4.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")})); setattr(getattr(um, malias_), tamper_, (lambda f_: (lambda x_: f_(x_) * 1.001))(getattr(_math, tamper_)))
    try:
        _rn = fn_(cs())
    finally:
        setattr(um, malias_, _m0)
    U["v408_%s_numero_adulterado_recusa" % k408_] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
_pv4, _jv4 = R408["projecao"]["values"], R408["jo8v32"]["values"]
_cvA4 = re.match(r"^\s*([+-]?\d+,\d+)\s*\[\s*([+-]?\d+,\d+)\s*;\s*([+-]?\d+,\d+)\s*\]", str(core0["ramo_b_preregistration_v386"]["central_values_NOT_BLIND_read_from_V1"]["A_31_deformacao_comum_GWTC5"]))
_cA4 = [float(x_.replace(",", ".")) for x_ in _cvA4.groups()]; _pred4 = core0["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"]["read"]
U["v408_projecao_numeros_recalculados_aqui"] = bool(abs(_pv4["beta"] - _bf4) <= 1e-15 and abs(_pv4["sin_pi_over_4"] - _math.sqrt(0.5)) <= 1e-15 and abs(_pv4["sin_sq_pi_over_4"] - 0.5) <= 1e-15 and abs(_pv4["theta_M"] - _math.asin(_math.sqrt(_bf4))) <= 1e-15 and abs(_pv4["m_nu_meV_runtime"] - _bf4 * _math.sqrt(0.5) * 1000.0) <= 1e-12
                                                   and abs(_pv4["m_nu_meV_core"] / _pv4["m_nu_meV_runtime"] - 1.0) <= 1e-12 and abs(_pv4["derivative_of_sin_sq_at_pi_over_4"] - 1.0) <= 1e-9 and _pv4["self_conjugate_weights"] == [0.5] and _pv4["e0_eV_declared"] == 1.0 and _pv4["grid_angles"] == 20001 and _pv4["grid_weights"] == 1001
                                                   and abs(_pv4["theta_M_minus_pi_over_4"] - (_math.asin(_math.sqrt(_bf4)) - _math.pi / 4.0)) <= 1e-15)
U["v408_jo8v32_a_mecanica_da_v403_relida_passa_nas_tres"] = bool(_jv4["v403_mechanics_checks"] == [DL.D3.N_CHECKS_CAMINHO, DL.D3.N_CHECKS_VIDA, DL.D3.N_CHECKS_VERDADE_ADENDO] == [5, 6, 5] and _jv4["v403_mechanics_passed"] == [True, True, True] and abs(_jv4["beta"] - _bf4) <= 1e-15
                                                              and _jv4["order_of_the_verse"] == um._V404_CONTRACTS["jo8v32"]["order_of_the_verse"] and abs(_jv4["p_plus_factor_at_beta"] - _math.exp(-_bf4)) <= 1e-15 and abs(_jv4["alpha_squared"] - um.SEALED_CODATA_ALPHA ** 2) <= 1e-18)
_c4p = cs(); _antes4p = json.dumps(_c4p["neutrino_mass"], sort_keys=True, default=str); _r4p = um.projecao_transversal_v404(_c4p)
U["v408_projecao_a_errata_do_angulo_fica_ao_lado_o_texto_antigo_intacto_e_o_canal_do_neutrino_nao_se_move"] = bool(json.dumps(_c4p["neutrino_mass"], sort_keys=True, default=str) == _antes4p == _nm_antes4 and _c4p["neutrino_mass"]["angle_status"].startswith(DL.ANGLE_STATUS_ANTIGO_PREFIXO)
                                                                                                                       and _r4p["neutrino_angle_errata"]["dizia_prefixo"] == DL.ANGLE_STATUS_ANTIGO_PREFIXO and _r4p["neutrino_angle_errata"]["assinatura"].startswith("gerencia c1, em nome proprio") and _c4p["neutrino_mass"]["verdict"] == core0["neutrino_mass"]["verdict"] and _c4p["neutrino_mass"]["frozen_hash"] == core0["neutrino_mass"]["frozen_hash"])
U["v408_projecao_E0_declarado_a_identificacao_e_onto_e_o_nome_e_provisorio"] = bool(R408["projecao"]["e0"]["status"] == "DECLARADO" and R408["projecao"]["e0"]["derived_here"] is False and R408["projecao"]["reading_matter"]["status"] == "ONTO" and R408["projecao"]["reading_matter"]["is_a_kernel_term"] is False
                                                                                    and R408["projecao"]["name_status"]["estado"] == "PROVISORIO" and any("E0" in x_ and "DECLARADA" in x_ for x_ in R408["projecao"]["limites"]) and any("ONTO" in x_ and "condicional" in x_ for x_ in R408["projecao"]["limites"]) and any("deriva E0" in x_ or "E0" in x_ for x_ in R408["projecao"]["nao_diz"]))
U["v408_jo8v32_o_nome_e_do_operador_a_leitura_e_onto_e_as_hipoteses_dos_componentes_sao_ditas"] = bool(R408["jo8v32"]["name_given_by"]["quem"] == "operador" and R408["jo8v32"]["name_given_by"]["sha16_da_fala"] == DL.D4.verbatins404(os.path.join(DL.V404, "insumos", "cunhagens"))[DL.D4.JO8_IDX]["sha16"] and R408["jo8v32"]["reading_jo8_32"]["status"] == "ONTO" and R408["jo8v32"]["reading_jo8_32"]["is_a_kernel_term"] is False
                                                                                               and R408["jo8v32"]["named_hypotheses_carried_by_components"] == {"vida": "IsotropicPost", "verdade": ["hpp", "hopt"]} and R408["jo8v32"]["unconditional"]["composition"] == "CONDITIONAL_ON_NAMED_HYPOTHESES_IN_THE_STATEMENT" and any("anule a decisao D20" in x_ for x_ in R408["jo8v32"]["nao_diz"]))
# --- a errata de F2b: tudo certo, o V1 e o livro NAO reescritos, e cada elo recusa (o canal fica como antes)
fb_ = um.f2b_errata_v404; C_f = um._V404_CONTRACTS["f2b"]; T_f = um._V404_TEXTS["f2b"]
cf_ = cs(); _h_antes4 = json.dumps([cf_["ramo_b_preregistration_v386"], cf_["ledger_errata_v386"], cf_["the_ledger_of_charges_v383"]], sort_keys=True, default=str)
rf_ = fb_(cf_); R408["f2b"] = rf_
U["v408_f2b_tudo_certo"] = bool(rf_["all_verified"] is True and rf_["verdict"] == T_f["veredito_ok"] and rf_["runtime_executed"] is True and rf_["does_not_gate_core"] is True and rf_["mechanics"]["n_checks"] == DL.D4.N_CHECKS["f2b"] == len(rf_["mechanics"]["checks"]) and all(ck_["ok"] for ck_ in rf_["mechanics"]["checks"])
                                and rf_["F2b_status_now"] == DL.F2B_FUTURO_TOKEN and rf_["F2b_status_before"] == C_f["v1"]["f2b_status_antes"] == "AWAITING" and all(rf_["inscriptions"].values()) and rf_["beta_ok"] is True and rf_["values"]["n_cobrancas_v383"] == 11 and rf_["values"]["conjunto_D_n"] == 14)
U["v408_f2b_o_v1_o_registro_da_v386_e_o_livro_da_v383_nao_foram_reescritos"] = bool(json.dumps([cf_["ramo_b_preregistration_v386"], cf_["ledger_errata_v386"], cf_["the_ledger_of_charges_v383"]], sort_keys=True, default=str) == _h_antes4 and cf_["ramo_b_preregistration_v386"]["F2b_status"] == "AWAITING" and cf_["ramo_b_preregistration_v386"]["veredito_do_V1"] == "AWAITING_DATA")
U["v408_f2b_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(rf_) and not _GUARDA98.search(rf_["verdict"]) and not rf_["guarda_p18_violacoes"] and not um._v392_guarda_texto(json.dumps(rf_["mechanics"]["checks"], ensure_ascii=False)) and "FALSIFIED" not in rf_["verdict"].replace("NOT_FALSIFIED", "") and "AWAITING" not in rf_["verdict"])
U["v408_f2b_numeros_recalculados_aqui"] = bool(abs(rf_["values"]["calibracao_A_central"] - _cA4[0]) <= 1e-15 and abs(rf_["values"]["calibracao_A_inferior"] - _cA4[1]) <= 1e-15 and abs(rf_["values"]["calibracao_A_superior"] - _cA4[2]) <= 1e-15 and rf_["values"]["previsao_do_par"] == _pred4 and _pred4 < 0.0 < _cA4[0]
                                               and rf_["values"]["previsao_fora_do_intervalo_de_A"] is True and abs(rf_["values"]["distancia_da_previsao_ao_limite_inferior_de_A"] - (_cA4[1] - _pred4)) <= 1e-12 and abs(rf_["values"]["beta"] - _bf4) <= 1e-15)
_tam4 = [("f1", lambda c_: c_["ramo_b_preregistration_v386"].__setitem__("read_ok", False)),
         ("f2", lambda c_: c_["the_ledger_of_charges_v383"]["counts"].__setitem__("AWAITING", c_["the_ledger_of_charges_v383"]["counts"]["AWAITING"] + 1)),
         ("f3", lambda c_: c_["ramo_b_preregistration_v386"]["central_values_NOT_BLIND_read_from_V1"].__setitem__("A_31_deformacao_comum_GWTC5", "+0,072 [+0,015; +0,134")),
         ("f4", lambda c_: c_["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"].__setitem__("equal", False)),
         ("f5", lambda c_: (c_["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"].__setitem__("read", 0.05), c_["ramo_b_preregistration_v386"]["pins"]["delta_pred_A31_exato"].__setitem__("pinned", 0.05))),
         ("f6", lambda c_: c_["ramo_b_preregistration_v386"].__setitem__("nothing_opened", False)),
         ("f7", lambda c_: c_.__setitem__("beta", c_["beta"] * 1.001))]
ok_ = True; _tam4_det = {}
for id_, mut_ in _tam4:   # CADA checagem negada: o registro recusa, a checagem e' a que falha e o canal F2b FICA como antes (AWAITING)
    c_ = cs(); mut_(c_); rr_ = fb_(c_); _falhas_ = [ck_["id"] for ck_ in ((rr_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]
    _tam4_det[id_] = _falhas_
    ok_ = ok_ and rr_["all_verified"] is False and id_ in _falhas_ and rr_["F2b_status_now"] == "AWAITING" and "A_CHECK_FAILED" in rr_["verdict"] and "REFUSED" in rr_["verdict"]
ok_ = ok_ and len(_tam4) == DL.D4.N_CHECKS["f2b"]
for ch_ in C_f["verbatins"]:   # as duas falas embutidas adulteradas
    _ant = um._V404_VERBATINS2[ch_]["text"]; um._V404_VERBATINS2[ch_]["text"] += " "
    try:
        rr_ = fb_(cs()); ok_ = ok_ and rr_["all_verified"] is False and "f7" in [ck_["id"] for ck_ in rr_["mechanics"]["checks"] if not ck_["ok"]] and rr_["F2b_status_now"] == "AWAITING"
    finally:
        um._V404_VERBATINS2[ch_]["text"] = _ant
U["v408_f2b_cada_checagem_negada_recusa_e_o_canal_fica_como_antes"] = bool(ok_)
# --- as nove falas de 28/10, as decisoes D23-D26, as erratas E7-E9 e a leitura (registro cunhagens_v404) e a cobertura exata (kh_n1_cobertura_v404)
_cn4 = c.get("cunhagens_v404") or {}
_sp4s = [s_ for s_ in um._V404_SPECS if s_["nome"] == "cunhagens_v404"][0]
U["cunhagens_v408_nove_falas_decisoes_erratas_e_leituras"] = bool(_cn4.get("all_verified") is True and len(_cn4.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V404) == 9 and all(v_["embedded_ok"] for v_ in (_cn4.get("verbatim") or {}).values())
                                                                  and len(_cn4.get("erratas") or []) == 3 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn4.get("erratas") or []))
                                                                  and len(_cn4.get("leituras_do_operador") or []) == len(_sp4s["leituras_do_operador"]) == 12 and set((_cn4.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D23", "D24", "D25", "D26"}
                                                                  and (_cn4.get("extras") or {}).get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.D4.STONES} and (_cn4.get("extras") or {}).get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.D4.STONES}
                                                                  and len((_cn4.get("extras") or {}).get("erratas_E7_a_E9") or []) == 3 and str(((_cn4.get("extras") or {}).get("nomes") or {}).get("jo8v32", "")).startswith("TGLExt.Jo8v32")
                                                                  and "ONTO" in str((_cn4.get("extras") or {}).get("leitura_massa_28out", {}).get("estatuto", "")) and (_cn4.get("extras") or {}).get("autor_de_cada_inscricao") and all(a_ == "operador" for a_ in ((_cn4.get("extras") or {}).get("autor_de_cada_inscricao") or {}).values()))
_kh4 = c.get("kh_n1_cobertura_v404") or {}
_kh3s = [s_ for s_ in um._V403_SPECS if s_["nome"] == "kh_n1_cobertura_v403"][0]; _kh4s = [s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]
U["kh_n1_cobertura_v403_e_a_da_v408_viraram_piso"] = bool(_kh4.get("all_verified") is True and (c.get("kh_n1_cobertura_v403") or {}).get("all_verified") is True and {ck_["id"]: ck_["op"] for ck_ in _kh3s["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh3s["erratas"]) >= 1
                                                                          and {ck_["id"]: ck_["op"] for ck_ in _kh4s["checks"] if ck_["id"] in _op_piso} == _op_piso and len([s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]["erratas"]) >= 1)
U["contratos_v403_de_pedra_pinam_a_escada_da_v408"] = bool(len(um._V403_CONTRACTS) == 4 and [c3_["expected_ladder"] for c3_ in um._V403_CONTRACTS.values()] == [ESP, ESP, ESP, None])
rep["v408_registros"] = {k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_.get("unconditional"), "key_theorem": r_.get("key_theorem"), "context": r_.get("context"), "F2b_status_now": r_.get("F2b_status_now")} for k_, r_ in R408.items()}
# (6j) [v405] os OITO registros com FUNCAO da v409: tudo certo, os numeros RECALCULADOS aqui por outro caminho e cada elo recusa visivelmente (controles negativos); a guarda das frases; as falas de 30/10 a 01/11, as decisoes D27-D33, as erratas E10-E13, os campos fechados e as leituras, a cobertura exata (specs) e o neutrino NAO reescrito
import types as _types5
import guarda_frases_v409 as _GF5
import importlib.util as _ilu8   # (v409) a guarda da v408 para os textos HERDADOS (v405 a v408): o delta_v408 ja' vive neutralizado em DL.D7; a F29 da v409 reprovaria o «leituras do operador [ONTO]» da v408 selada, que e' texto selado, nao texto novo
sys.modules.setdefault("delta_v407", DL.D7)
_sp7r = _ilu8.spec_from_file_location("runtime_v407", os.path.join(DL.V407, "runtime_v407.py")); _rt7m = _ilu8.module_from_spec(_sp7r); _sp7r.loader.exec_module(_rt7m); sys.modules.setdefault("runtime_v407", _rt7m)
_sp7g = _ilu8.spec_from_file_location("guarda_frases_v407", os.path.join(DL.V407, "guarda_frases_v407.py")); _GF7 = _ilu8.module_from_spec(_sp7g); _sp7g.loader.exec_module(_GF7)
sys.modules.setdefault("delta_v408", DL.D8)   # (v409) a guarda da v408 para os textos HERDADOS da v408 (a F36 da v409 reprovaria a frase D51 da v408 selada, que e' texto selado, nao texto novo)
_sp8r = _ilu8.spec_from_file_location("runtime_v408", os.path.join(DL.V408, "runtime_v408.py")); _rt8m = _ilu8.module_from_spec(_sp8r); _sp8r.loader.exec_module(_rt8m); sys.modules.setdefault("runtime_v408", _rt8m)
_sp8g = _ilu8.spec_from_file_location("guarda_frases_v408", os.path.join(DL.V408, "guarda_frases_v408.py")); _GF8 = _ilu8.module_from_spec(_sp8g); _sp8g.loader.exec_module(_GF8)
_REG409 = tuple((s_["key"], DL.D5.REGISTRO_DE_PEDRA[s_["key"]]) for s_ in DL.D5.STONES)   # (v409: as oito pedras da v408, HERDADAS: DL.D5; DL.STONES da v409 e' [] de proposito)
_TAMPER409 = {"ponte": "cos", "tensao": "sqrt", "identidade": "cos", "diminuto": "exp", "tonica": "sqrt", "disco": "exp", "psion": "sqrt"}   # a funcao do math adulterada, registro a registro (o observador e' aritmetica de grafo: o numero adulterado dele e' o omega_I do core)
R409 = {}
_bf5 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_nm_antes5 = json.dumps(cs()["neutrino_mass"], sort_keys=True, default=str)
for k409_, n409_ in _REG409:
    fn_ = getattr(um, n409_); C_ = um._V405_CONTRACTS[k409_]; T_ = um._V405_TEXTS[k409_]
    cc5_ = cs(); r_ = fn_(cc5_); R409[k409_] = r_
    U["v409_%s_tudo_certo" % k409_] = bool(r_["all_verified"] is True and r_["verdict"] == T_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] == DL.D5.N_CHECKS[k409_] == len(r_["mechanics"]["checks"])
                                           and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and r_["key_theorem"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values())
                                           and all(r_["inscriptions"].values()) and r_["context"]["ok"] is True and r_["beta_ok"] is True and r_["nome_do_operador"] == DL.D5.STONE_BY_KEY[k409_]["nome_do_operador"])
    U["v409_%s_veredito_e_textos_sem_palavra_proibida" % k409_] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"] and not um._v405_guarda_frases(r_["verdict"]) and not um._v405_guarda_frases(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)))
    ok_ = True
    for th_, fl_ in C_["theorems"].items():   # bandeira falsa de CADA declaracao do contrato (a estrela e a composicao entre elas)
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U["v409_%s_bandeira_falsa_de_cada_declaracao_do_contrato_recusa" % k409_] = bool(ok_ and len(C_["theorems"]) == len(DL.D5.STONE_BY_KEY[k409_]["contract"]) and C_["key_theorem"]["theorem"] in C_["theorems"] and C_["unconditional"]["theorem"] in C_["theorems"])
    ok_ = True
    for th_ in list(C_["theorems"]) + list(C_["support"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v409_%s_axioma_fora_do_trio_em_cada_termo_lido_recusa" % k409_] = bool(ok_)
    ok_ = True
    for th_ in [C_["unconditional"]["theorem"], C_["key_theorem"]["theorem"]] + list(C_["support"]):   # proveniencia errada
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U["v409_%s_proveniencia_errada_recusa" % k409_] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][C_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[C_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v409_%s_fonte_da_pedra_adulterada_recusa" % k409_] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U["v409_%s_escada_errada_ou_kernel_nao_verificado_recusa" % k409_] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in C_["verbatins"]:
        _ant = um._V405_VERBATINS2[ch_]["text"]; um._V405_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V405_VERBATINS2[ch_]["text"] = _ant
    U["v409_%s_inscricao_adulterada_recusa" % k409_] = bool(ok_ and len(C_["verbatins"]) >= 1)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); _cp = C_["context"]["path"]; um._EMBEDDED_KERNEL_FILES[_cp] = um._EMBEDDED_KERNEL_FILES[_cp].replace(C_["context"]["needles"][0], "xx")
    try:
        rr_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U["v409_%s_texto_contexto_retirado_do_kernel_recusa" % k409_] = bool(r_["context"]["ok"] is True and rr_["all_verified"] is False and rr_["context"]["text_in_embedded_kernel"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"])
    c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = fn_(c_)
    _a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
    try:
        _ra = fn_(cs())
    finally:
        um.SEALED_CODATA_ALPHA = _a0
    U["v409_%s_beta_adulterado_recusa" % k409_] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
    if k409_ == "observador":
        c_ = cs(); c_["omega_I"] = 2.0; _rn = fn_(c_)
    else:
        _m0 = um._m405; tamper_ = _TAMPER409[k409_]
        um._m405 = _types5.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); setattr(um._m405, tamper_, (lambda f_: (lambda *x_: f_(*x_) * 1.001))(getattr(_math, tamper_)))
        try:
            _rn = fn_(cs())
        finally:
            um._m405 = _m0
    U["v409_%s_numero_adulterado_recusa" % k409_] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
_pv5, _mv5, _iv5, _ov5, _dv5, _tv5, _ev5, _zv5 = (R409[k_]["values"] for k_ in ("ponte", "tensao", "identidade", "observador", "diminuto", "tonica", "disco", "psion"))
_mnu5 = core0["neutrino_mass"]["m_nu_meV"]; _r25 = _math.sqrt(2.0); _alfa5 = um.SEALED_CODATA_ALPHA
U["v409_o_numero_da_massa_nao_muda_e_os_numeros_foram_recalculados_aqui"] = bool(abs(_pv5["beta"] - _bf5) <= 1e-15 and abs(_pv5["m_derivada_meV"] / _mnu5 - 1.0) <= 1e-12 and abs(_pv5["m_derivada_meV"] - _bf5 * _math.cos(_math.pi / 4.0) * 1000.0) <= 1e-9 and abs(_pv5["m_derivada_meV"] / _pv5["m_proporcional_meV"] - _r25) <= 1e-9
                                                                                 and abs(_mv5["retida_eV"] - _bf5) <= 1e-15 and abs(_mv5["transmitida_eV"] - (1.0 - _bf5)) <= 1e-15 and abs(_mv5["massa_meV"] / _mnu5 - 1.0) <= 1e-12
                                                                                 and abs(_dv5["sqrt_e"] - _math.sqrt(_math.e)) <= 1e-15 and abs(_dv5["meio_tom"] - _math.exp(-0.5)) <= 1e-15 and abs(_dv5["E0_eV"] - 1.0) <= 1e-12 and abs(_dv5["tonica_eV"] - _math.sqrt(_math.e)) <= 1e-12 and abs(_dv5["alpha_lida_do_acoplamento"] - _alfa5) <= 1e-15 and abs(_dv5["massa_formula_meV"] / _mnu5 - 1.0) <= 1e-12
                                                                                 and abs(_tv5["razao_m_sobre_E0"] - _bf5 * _r25 / 2.0) <= 1e-15 and abs(_tv5["E0_da_lei_derivada_eV"] - 1.0) <= 1e-12
                                                                                 and abs(_zv5["hbar_omega_meV"] - _r25 * _bf5 * 1000.0) <= 1e-9 and abs(_zv5["meia_hbar_omega_meV"] / _mnu5 - 1.0) <= 1e-12 and abs(_zv5["R_natural"] - _bf5) <= 1e-15
                                                                                 and abs(_ev5["E_star_modelo"] - 3.0 ** (1.0 / 3.0)) <= 1e-12 and abs(_ev5["U_modelo"] - _math.exp(-0.5) * 3.0 ** (1.0 / 3.0)) <= 1e-12 and abs(_ev5["disco_modelo"]["c"] - 0.5 * _bf5 * 0.7 * 3.0) <= 1e-12
                                                                                 and _iv5["eu_sou"] == {"2": 1.0, "3": 1.0, "4": 1.0} and _iv5["n_nomes"] == 12 and _iv5["vazio_peso"] == 0.0 and all(p_[1] == 0.5 for p_ in _iv5["faces_peso"]) and _ov5["terminal"] == ["gravidade"] and _ov5["inicial"] == ["luz"] and _ov5["omega_I"] == 1.0)
_c5p = cs(); _antes5p = json.dumps(_c5p["neutrino_mass"], sort_keys=True, default=str); _r5p = um.ponte_da_massa_v405(_c5p); _e10 = _r5p["neutrino_angle_errata"]
U["v409_a_errata_do_angulo_fica_ao_lado_o_texto_antigo_intacto_e_o_canal_do_neutrino_nao_se_move"] = bool(json.dumps(_c5p["neutrino_mass"], sort_keys=True, default=str) == _antes5p == _nm_antes5 and _c5p["neutrino_mass"]["angle_status"].startswith(DL.ANGLE_STATUS_ANTIGO_PREFIXO) and _e10["dizia_prefixo"] == DL.ANGLE_STATUS_ANTIGO_PREFIXO and _e10["agora"] == DL.ERRATA_E10 and _e10["assinatura"].startswith("gerencia c1, em nome proprio") and _c5p["neutrino_mass"]["verdict"] == core0["neutrino_mass"]["verdict"] and _c5p["neutrino_mass"]["frozen_hash"] == core0["neutrino_mass"]["frozen_hash"])
U["v409_a_ponte_o_u_e_posto_as_leituras_entram_como_definicao_e_o_nome_e_do_operador"] = bool(R409["ponte"]["u"]["status"] == "POSTO" and R409["ponte"]["u"]["derived_here"] is False and R409["ponte"]["reading_matter"]["status"] == "ONTO" and R409["ponte"]["reading_matter"]["is_a_kernel_term"] is False and [l_["n"] for l_ in R409["ponte"]["leituras_que_entram"]] == [1, 2] and all(l_["entra_como"] == "DEFINICAO, nao teorema" for l_ in R409["ponte"]["leituras_que_entram"])
                                                                                             and R409["ponte"]["name_status"]["quem"] == "operador" and R409["ponte"]["name_status"]["fala"] == DL.FRASE_NOMEACAO and DL.ERRATA_E13 in R409["ponte"]["limites"] and any("a massa do neutrino SEJA" in x_ for x_ in R409["ponte"]["nao_diz"]))
U["v409_a_tonica_o_no_go_nao_cai_alfa_e_medida_e_a_tonica_e_definicao"] = bool("NAO cai" in R409["tonica"]["no_go_e_tonica"]["no_go"] and "identidade algebrica" in R409["tonica"]["no_go_e_tonica"]["tonica"] and R409["tonica"]["alfa"]["status"].startswith("MEDIDA") and [l_["n"] for l_ in R409["tonica"]["leituras_que_entram"]] == [3] and [l_["n"] for l_ in R409["diminuto"]["leituras_que_entram"]] == [3, 5, 11, 12] and any("alfa tenha sido derivado" in x_ for x_ in R409["tonica"]["nao_diz"]) and any("que o no-go tenha caido" in x_ for x_ in R409["tonica"]["nao_diz"]))
U["v409_o_psion_a_curvatura_e_definicao_e_a_coincidencia_e_aritmetica"] = bool([l_["n"] for l_ in R409["psion"]["leituras_que_entram"]] == [4, 6, 7, 13, 14, 15] and "aritmetica" in R409["psion"]["duas_leituras_do_sen45"]["coincidem_por"] and any("pagamentoComoCurvatura" in x_ for x_ in R409["psion"]["limites"]))
U["v409_a_identidade_e_um_fato_sobre_projecoes_tipado_como_modelo"] = bool(any("tipada como modelo" in x_ for x_ in R409["identidade"]["limites"]) and "ONTO" in R409["identidade"]["lei"]["status"] and "ONTO" in R409["identidade"]["ensaio"]["status"] and "um fato sobre projecoes" in R409["identidade"]["estatuto"] and any("SEJA a identidade" in x_ for x_ in R409["identidade"]["nao_diz"]))
U["v409_o_verbatim_e_a_traducao_o_ensaio_e_o_do_operador_e_a_traducao_nao_e_citacao"] = bool(hashlib.sha256(um._V405_IDENTIDADE_TXT.encode("utf-8")).hexdigest() == um._V405_FONTES["ensaio_a_identidade_r2_01nov"]["sha256"] and hashlib.sha256(um._V405_IDENTIDADE_EN_TXT.encode("utf-8")).hexdigest() == um._V405_FONTES["ensaio_a_identidade_en_traducao_da_gerencia_01nov"]["sha256"] and um._V405_IDENTIDADE_TXT.rstrip().endswith("[EU SOU] = [O QUE SOU] se, e somente se, {[FORMA = CONTEÚDO] = [REFLEXÃO VERDADEIRA DO NOME / PROJEÇÃO FIEL]}.") and "NAO e' citacao" in um._V405_FONTES["ensaio_a_identidade_en_traducao_da_gerencia_01nov"]["papel"] and len(um._v405_ensaio_tex(um._V405_IDENTIDADE_TXT)) == len(um._v405_ensaio_tex(um._V405_IDENTIDADE_EN_TXT)))
# --- a GUARDA DAS FRASES no rito (ordem da gerencia c1, 01/11/2026): cada frase proibida plantada no texto de CADA registro recusa; a frase certa passa; o controle negativo da cadeia passa
_g5 = _GF7.controle_negativo(); ok_ = bool(_g5["ok"])
for k409_, n409_ in _REG409:
    fn_ = getattr(um, n409_); _dz = um._V405_TEXTS[k409_]["diz"]; _d0 = list(_dz)
    for f_ in ("tudo é teorema", "tudo derivado", "nenhuma hipótese resta", "everything is a theorem", "everything is derived", "no hypothesis remains"):
        _dz[:] = _d0 + ["a cadeia: " + f_]
        try:
            rr_ = fn_(cs())
        finally:
            _dz[:] = _d0
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_p18_violacoes"])
    _dz[:] = _d0 + [DL.FRASE_DA_MOLDURA_PT]
    try:
        rr_ = fn_(cs())
    finally:
        _dz[:] = _d0
    ok_ = ok_ and rr_["all_verified"] is True
    ok_ = ok_ and fn_(cs())["all_verified"] is True
U["v409_guarda_das_frases_cada_frase_proibida_recusa_em_cada_registro_e_a_frase_certa_passa"] = bool(ok_)
# --- as falas de 30/10 a 01/11, as decisoes D27-D33, as erratas E10-E13 (registro cunhagens_v405), os campos fechados e as leituras e a cobertura exata (kh_n1_cobertura_v405)
_cn5 = c.get("cunhagens_v405") or {}; _xn5 = _cn5.get("extras") or {}
_sp5s = [s_ for s_ in um._V405_SPECS if s_["nome"] == "cunhagens_v405"][0]
U["cunhagens_v405_falas_decisoes_erratas_e_leituras"] = bool(_cn5.get("all_verified") is True and len(_cn5.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V405) and all(v_["embedded_ok"] for v_ in (_cn5.get("verbatim") or {}).values())
                                                             and len(_cn5.get("erratas") or []) == len(_sp5s["erratas"]) and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn5.get("erratas") or []))
                                                             and len(_cn5.get("leituras_do_operador") or []) == len(_sp5s["leituras_do_operador"]) and set(_xn5.get("decisoes_da_gerencia") or {}) >= {"D27", "D28", "D29", "D30", "D31", "D32", "D33"}
                                                             and _xn5.get("estrelas") == {s_["key"]: s_["key_theorem"] for s_ in DL.D5.STONES} and _xn5.get("teoremas") == {s_["key"]: s_["theorem"] for s_ in DL.D5.STONES}
                                                             and len(_xn5.get("erratas_E10_a_E13") or []) == 4 and (_xn5.get("autor_de_cada_inscricao") or {}) and all(a_ == "operador" for a_ in (_xn5.get("autor_de_cada_inscricao") or {}).values()))
_cf5 = c.get("campos_fechados_e_leituras_v405") or {}; _xf5 = _cf5.get("extras") or {}
_sp5c = [s_ for s_ in um._V405_SPECS if s_["nome"] == "campos_fechados_e_leituras_v405"][0]
U["campos_fechados_o_que_fechou_e_o_que_entra_cada_um_com_a_definicao_lean"] = bool(_cf5.get("all_verified") is True and set(_xf5.get("o_que_fechou_campos") or {}) == set(DL.CAMPOS_FECHADOS) and all(v_.get("termos") for v_ in (_xf5.get("o_que_fechou_campos") or {}).values()) and [d_["estatuto"] for d_ in (_xf5.get("o_que_entra") or {}).get("dois_postos", [])] == ["POSTO", "MEDIDA"]
                                                                                    and [l_["n"] for l_ in (_xf5.get("o_que_entra") or {}).get("leituras_da_cadeia_da_massa", [])] == [l_["n"] for l_ in DL.LEITURAS_DEFINICOES] and (_xf5.get("o_que_entra") or {}).get("lista_de_leituras_fechada") is False and all((l_["definicao_lean"] is None or l_["definicao_lean"] in _sp5c["kernel_decls"]) and l_["entra_como"].endswith(", nao teorema") for l_ in (_xf5.get("o_que_entra") or {}).get("leituras_da_cadeia_da_massa", []))
                                                                                    and _xf5.get("a_frase_da_moldura") == DL.FRASE_DA_MOLDURA_PT and len(_xf5.get("a_forma_real") or []) == 4 and len(_xf5.get("teoremas_rebatizados_antes_do_selo") or {}) == 4 and DL.ERRATA_E13 in (_cf5.get("limites") or []))
U["campos_fechados_o_registro_antigo_nao_existe_e_o_texto_nao_afirma_demais"] = bool("nomes_e_hipoteses_descarregadas_v409" not in c and "nomes_e_hipoteses_descarregadas_v409" not in um._V405_NOMES_REGISTROS and not um._v405_guarda_frases(json.dumps({k_: _cf5.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)) and not um._v405_guarda_frases(str(_cf5.get("verdict"))))
# --- a reclassificacao do Grande Atrator (registro por especificacao, AO LADO): selou, as medidas recalculadas aqui por outro caminho, cada elo recusa e o selado fica identico
_gaS = [s_ for s_ in um._V405_SPECS if s_["nome"] == DL.GA_REGISTRO][0]; _ga5 = c.get(DL.GA_REGISTRO) or {}; _gv5 = _ga5.get("values") or {}; _gx5 = _ga5.get("extras") or {}
_GA_R = lambda c_: um._v405_ga_registro(um._v392_registro(_gaS, c_), c_, _gaS)
U["ga_reclassificacao_selou_a_classe_nova_ao_lado_e_o_estatuto_e_dito"] = bool(_ga5.get("all_verified") is True and _ga5.get("does_not_gate_core") is True and _ga5.get("runtime_executed") is True and (_ga5.get("mechanics") or {}).get("passed") is True and (_ga5.get("mechanics") or {}).get("n_checks") == 6 and _ga5.get("errata_do_parecer_ok") is True and not _ga5.get("guarda_frases_violacoes")
                                                                               and _gx5.get("classe_antes") == DL.GA_CLASSE_ANTES and _gx5.get("classe_agora") == DL.GA_CLASSE_AGORA and _gx5.get("e_evidencia") is False and _gx5.get("discrimina_da_RG") is False and _gx5.get("veto_da_janela") == "mantido" and _gx5.get("errata_ao_lado_do_parecer_da_entrega_005") == DL.errata_entrega_005()
                                                                               and len((_gx5.get("partitura") or {}).get("escolhas_antes_de_qualquer_teste") or []) == 4 and len(_gx5.get("quatro_medidas") or []) == 4 and not _GF7.violacoes(str(_ga5.get("verdict"))))
_por5 = um.C_LIGHT ** 2 / (4.0 * _math.pi * um.G_NEWTON) * um.MPC_M / um.MSUN; _MA5 = R0["verdict"]["masses_Msun"]["A_literature"]; _MB5 = R0["verdict"]["masses_Msun"]["B_cf4_positions"]
U["ga_as_medidas_recalculadas_aqui_com_o_beta_de_runtime_e_as_massas_do_verdict"] = bool(abs(_gv5.get("M_sobre_R_Msun_por_Mpc", 0.0) / (2.0 * _bf5 ** 2 * _por5) - 1.0) <= 1e-12 and _gv5.get("dM_du") == 0.0 and max(_gv5.get("residuos_M_igual_M") or [1.0]) <= 1e-14 and all(abs(x_ * _bf5 / (2.0 * _math.pi) - 1.0) <= 1e-12 for x_ in (_gv5.get("R_B_sobre_r_s") or [0.0]))
                                                                                         and abs(_gv5.get("piso_de_definicao", 0.0) - (_MA5 / _MB5 - 1.0)) <= 1e-12 and abs(_gv5.get("sigma_relativo_resposta_beta", 0.0) - _bf5 / 5.0) <= 1e-15 and abs(_gv5.get("sigma_relativo_forma_ancora", 0.0) - (5.4e16 - _MA5) / 5.0 / 5.4e16) <= 1e-12 and _gv5.get("M_A_Msun") == _MA5 and _gv5.get("M_B_Msun") == _MB5)
_negs5 = {}
_c5a = cs(); _c5a["beta"] = _c5a["beta"] * 1.001; _negs5["beta"] = _GA_R(_c5a)
_c5b = cs(); _c5b["mode_B"]["M_TGL_Msun"] = _c5b["mode_B"]["M_TGL_Msun"] * 1.001; _negs5["piso"] = _GA_R(_c5b)
_c5c = cs(); [x_.__setitem__("rule", DL.GA_CLASSE_AGORA) for x_ in _c5c["joint_coincidence_result_v3"]["inventory"] if x_.get("id") == "ga_mass_window"]; _negs5["linha_selada"] = _GA_R(_c5c)
_c5d = cs(); _c5d["ga_mass_audit"]["verdict"] = "OUTRO"; _negs5["auditoria"] = _GA_R(_c5d)
_gaE = _gaS["extras"]["errata_ao_lado_do_parecer_da_entrega_005"]; _gaS["extras"]["errata_ao_lado_do_parecer_da_entrega_005"] = _gaE + " "
try:
    _negs5["errata"] = _GA_R(cs())
finally:
    _gaS["extras"]["errata_ao_lado_do_parecer_da_entrega_005"] = _gaE
_gaD = list(_gaS["diz"]); _gaS["diz"][:] = _gaD + ["a cadeia: tudo derivado"]
try:
    _negs5["frase"] = _GA_R(cs())
finally:
    _gaS["diz"][:] = _gaD
_m05 = um._m405; um._m405 = _types5.SimpleNamespace(**{k_: getattr(_math, k_) for k_ in dir(_math) if not k_.startswith("__")}); um._m405.sqrt = (lambda f_: (lambda *x_: f_(*x_) * 1.001))(_math.sqrt)
try:
    _negs5["numero"] = _GA_R(cs())
finally:
    um._m405 = _m05
U["ga_cada_elo_recusa_beta_piso_linha_selada_auditoria_errata_frase_e_numero"] = bool(all(r_["all_verified"] is False and "NOT_SEALED_THIS_RUN" in r_["verdict"] for r_ in _negs5.values()) and len(_negs5) == 7 and _GA_R(cs())["all_verified"] is True)
_lgm5 = [x_ for x_ in c["joint_coincidence_result_v3"]["inventory"] if x_.get("id") == "ga_mass_window"]
U["ga_o_selado_fica_identico_a_constante_a_linha_e_a_auditoria"] = bool(um.GA_WINDOW_STATUS == R0["ga_window_status"] and len(_lgm5) == 1 and _lgm5[0]["rule"] == DL.GA_CLASSE_ANTES and _lgm5[0]["admissible"] is False and c["ga_mass_audit"]["verdict"] == core0["ga_mass_audit"]["verdict"])
rep["ga_registro"] = {"verdict": _ga5.get("verdict"), "all_verified": _ga5.get("all_verified"), "values": _gv5, "n_checks": (_ga5.get("mechanics") or {}).get("n_checks"), "ctl_negativos": {k_: r_["all_verified"] for k_, r_ in _negs5.items()}}
# --- o gap (registro por especificacao, AO LADO): selou, os numeros recalculados aqui por outro caminho, e cada elo recusa
_gpS = [s_ for s_ in um._V405_SPECS if s_["nome"] == DL.GAP_REGISTRO][0]; _gp5 = c.get(DL.GAP_REGISTRO) or {}; _gpv = _gp5.get("values") or {}
_GP_R = lambda c_: um._v405_gap_registro(um._v392_registro(_gpS, c_), c_, _gpS)
U["gap_selou_com_as_medidas_em_runtime_e_a_guarda"] = bool(_gp5.get("all_verified") is True and _gp5.get("does_not_gate_core") is True and _gp5.get("runtime_executed") is True and (_gp5.get("mechanics") or {}).get("passed") is True and (_gp5.get("mechanics") or {}).get("n_checks") == DL.GAP_N_CHECKS and not _gp5.get("guarda_frases_violacoes") and not _GF7.violacoes(str(_gp5.get("verdict"))))
U["gap_os_numeros_recalculados_aqui_com_o_beta_de_runtime"] = bool(abs(_gpv.get("Delta_eV", 0.0) / _bf5 - 1.0) <= 1e-14 and _gpv.get("gap_espectral_eV") == 1.0 and abs(_gpv.get("gap_sobre_Delta", 0.0) * _bf5 - 1.0) <= 1e-13 and abs(_gpv.get("Q", 0.0) * _bf5 / _math.sqrt(2.0) - 1.0) <= 1e-13 and abs(_gpv.get("Gamma_B_eV", 0.0) / _bf5 ** 2 - 1.0) <= 1e-13 and 56.0 < _gpv.get("log10_E_fluxo_eV", 0.0) < 58.0 and _gpv.get("tau_sobre_t_planck", 0.0) > 1.0e25)
_negsG = {}
_cGa = cs(); _cGa["beta"] = _cGa["beta"] * 1.001; _negsG["beta"] = _GP_R(_cGa)
_cGb = cs(); _cGb["neutrino_mass"]["m_nu_meV"] = _cGb["neutrino_mass"]["m_nu_meV"] * 1.001; _negsG["massa"] = _GP_R(_cGb)
_gpD = list(_gpS["diz"]); _gpS["diz"][:] = _gpD + ["o tau* foi derivado aqui"]
try:
    _negsG["frase_tau"] = _GP_R(cs())
finally:
    _gpS["diz"][:] = _gpD
_gpD = list(_gpS["diz"]); _gpS["diz"][:] = _gpD + ["kappa = F(alfa, beta, theta_M)"]
try:
    _negsG["frase_kappa"] = _GP_R(cs())
finally:
    _gpS["diz"][:] = _gpD
_gpD = list(_gpS["diz"]); _gpS["diz"][:] = _gpD + ["Delta e' o gap do lock"]
try:
    _negsG["frase_delta_gap"] = _GP_R(cs())
finally:
    _gpS["diz"][:] = _gpD
U["gap_cada_elo_recusa_beta_massa_e_as_frases"] = bool(all(r_["all_verified"] is False for r_ in _negsG.values()) and len(_negsG) == 5 and _GP_R(cs())["all_verified"] is True)
rep["gap_registro"] = {"verdict": _gp5.get("verdict"), "all_verified": _gp5.get("all_verified"), "values": _gpv, "n_checks": (_gp5.get("mechanics") or {}).get("n_checks"), "ctl_negativos": {k_: r_["all_verified"] for k_, r_ in _negsG.items()}}
_kh5 = c.get("kh_n1_cobertura_v405") or {}
_kh4s5 = [s_ for s_ in um._V404_SPECS if s_["nome"] == "kh_n1_cobertura_v404"][0]; _kh5s = [s_ for s_ in um._V405_SPECS if s_["nome"] == "kh_n1_cobertura_v405"][0]
_kh6 = c.get("kh_n1_cobertura_v406") or {}; _kh6s = [s_ for s_ in um._V406_SPECS if s_["nome"] == "kh_n1_cobertura_v406"][0]
U["kh_n1_cobertura_v408_virou_piso_e_a_v409_cobra_a_igualdade_exata"] = bool(_kh5.get("all_verified") is True and _kh6.get("all_verified") is True and (c.get("kh_n1_cobertura_v404") or {}).get("all_verified") is True and {ck_["id"]: ck_["op"] for ck_ in _kh4s5["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh4s5["erratas"]) >= 1
                                                                             and {ck_["id"]: ck_["op"] for ck_ in _kh5s["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh5s["erratas"]) >= 1 and {ck_["id"]: ck_["op"] for ck_ in _kh6s["checks"] if ck_["id"] in _op_piso} == _op_piso and len(_kh6s["erratas"]) >= 1)   # (v409, errata E20: o kh_n1_cobertura_v406 HERDADO virou piso como os anteriores; a igualdade exata e' a do kh_n1_cobertura_v407)
_ESC_SRC0 = open(os.path.join(BASE, "um.py"), "rb").read().decode("utf-8", errors="replace")   # o um.py da v408 SELADA: quantos `'expected_ladder': <escada da v408>` ele traz, o candidato troca todos pelo novo e traz UM a mais (o contrato da v409)
_n_esc_base = len(re.findall(r"'expected_ladder': %d\b" % E408, _ESC_SRC0)); _n_esc_cand = len(re.findall(r"'expected_ladder': %d\b" % ESP, src)); del _ESC_SRC0
U["contratos_v408_de_pedra_pinam_a_escada_da_v409"] = bool(len(um._V404_CONTRACTS) == 3 and [c4_["expected_ladder"] for c4_ in um._V404_CONTRACTS.values()] == [ESP, ESP, None] and all(c5_["expected_ladder"] == ESP for c5_ in um._V405_CONTRACTS.values()) and len(um._V405_CONTRACTS) == 8
                                                          and um._V406_FECHO_CONTRACT["expected_ladder"] == ESP and um._V407_PSION_CONTRACT["expected_ladder"] == ESP and um._V408_TERMINAL_CONTRACT["expected_ladder"] == ESP and _n_esc_base >= 1 and _n_esc_cand == _n_esc_base + 1 and not re.search(r"'expected_ladder': %d\b" % E408, src))
rep["contratos_pinam_a_escada"] = {"expected_ladder_no_selado_da_v408": _n_esc_base, "expected_ladder_no_candidato": _n_esc_cand, "escada_da_v408": E408, "escada_da_v409": ESP}
rep["v409_registros"] = {k_: {"verdict": r_["verdict"], "all_verified": r_["all_verified"], "n_checks": r_["mechanics"]["n_checks"], "values": r_["values"], "unconditional": r_.get("unconditional"), "key_theorem": r_.get("key_theorem"), "context": r_.get("context")} for k_, r_ in R409.items()}
rep["unidade"] = U; print("unidade:", {k: v for k, v in U.items() if not v} or "todas True (%d)" % len(U))
# (6l) [v408, HERDADO na v409: os numeros dele (301 modulos, oito ancoras, 14 checagens, 1794 bandeiras) saem do DL.D6 e do contrato HERDADO do candidato, NUNCA do DL da v409] O REGISTRO COM FUNCAO fechamento_v406: tudo certo, os numeros RECALCULADOS aqui por outro caminho (as fontes dos 301 modulos pelo BUNDLE_v409.json, as bandeiras pelo FLAGS_v409.json, o beta pelo alfa CODATA x sqrt(e)), as quatro chaves LIDAS do kernel (e nao literal), o que fica False por teorema, o gate que nao se move,
# e cada elo recusa visivelmente (controles negativos); a guarda das frases; as falas de 02/11 (cunhagens_v406) e a cobertura exata (kh_n1_cobertura_v406).
_CF6, _TF6 = um._V406_FECHO_CONTRACT, um._V406_FECHO_TEXT
_bf6 = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e)
_FJ6 = json.load(open(os.path.join(DL.V406, DL.D6.KERNEL_DIR, "FLAGS_v406.json"), encoding="utf-8"))   # (v409) as 1794 bandeiras da v406: o FLAGS da v406 (o FLAGS_v409.json traz as 43 novas)
_D6 = DL.D6; _N6 = len(_CF6["source_sha256"]); _NA6 = len(_CF6["ancoras"])
_ANC_FLAGS6 = {n_: a_.get("flag") for n_, a_ in _CF6["ancoras"].items()}
_rapido6 = lambda: dict(core_s)   # o fechamento_v406 so' LE o core e grava a propria chave: uma copia rasa basta (os campos mexidos abaixo sao copiados um a um)


def _kf6(**mud_):
    """copia rasa do core com o kf copiado (e os sub-dicts pedidos em `mud_`, copiados antes de mexer)"""
    c_ = _rapido6(); kf_ = dict(c_["kernel_formalization"])
    for k_ in mud_.get("copiar", ()):
        kf_[k_] = dict(kf_[k_])
    c_["kernel_formalization"] = kf_
    return c_


def _recusa6(rr_, onde_="FORMAL_OR_SOURCE_EVIDENCE"):
    return bool(rr_["all_verified"] is False and onde_ in rr_["verdict"])


def _falhos6(rr_):
    return [ck_["id"] for ck_ in ((rr_.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]


r6 = um.fechamento_v406(cs()); RFCH = r6
_v6 = r6.get("values") or {}
U["fechamento_v406_herdado_tudo_certo"] = bool(r6["all_verified"] is True and r6["verdict"] == _TF6["veredito_ok"] and r6["runtime_executed"] is True and r6["does_not_gate_core"] is True and r6["mechanics"]["n_checks"] == _D6.N_CHECKS_FECHO == len(r6["mechanics"]["checks"]) and all(ck_["ok"] for ck_ in r6["mechanics"]["checks"])
                                       and r6["exact_ladder"] is True and r6["embedded_sources_ok"] is True and r6["embedded_sources_n_ok"] == _D6.N_BUNDLE == len(_D6.BUNDLE_RELS) == _N6 and r6["certificate_inhabited"] is True and r6["beta_ok"] is True and all(r6["anchors"].values()) and len(r6["anchors"]) == _NA6 == len(_D6.ANCORAS)
                                       and all(r6["inscriptions"].values()) and not r6["guarda_violacoes"] and _v6.get("n_ancoras_ok") == _NA6 and _v6.get("n_modulos_ok") == _v6.get("n_modulos") == _D6.N_BUNDLE and _v6.get("n_flags_true") == _v6.get("n_flags") == _CF6["n_flags"] == _FJ6["n_flags"] and _v6.get("escada") == [ESP, ESP, ESP])   # (a escada que o fechamento_v406 confere e' a NOVA: o contrato herdado foi subido a ESP pela v409, errata E20)
U["fechamento_v406_herdado_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(r6) and not _GUARDA98.search(r6["verdict"]) and not um._v406_guarda_frases(r6["verdict"]) and not um._v406_guarda_frases(json.dumps(r6["mechanics"]["checks"], ensure_ascii=False)) and not um._v406_guarda_frases(json.dumps({k_: r6.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False)))
# os numeros RECALCULADOS aqui por OUTRO caminho: as fontes pelo BUNDLE_v409.json (lido pelo delta), as bandeiras pelo FLAGS_v409.json, as ancoras pelo DL.ANCORAS, o beta pelo alfa x sqrt(e)
_kf0 = c["kernel_formalization"]; _trio6 = {"propext", "Classical.choice", "Quot.sound"}
_fontes_ok6 = sum(1 for rel_ in _D6.BUNDLE_RELS if hashlib.sha256(EMBK[rel_].encode("utf-8")).hexdigest() == _D6.BUNDLE_POR_REL[rel_]["sha256"] == _kf0["formal_files_sha256"].get(rel_))
_flags_ok6 = sum(1 for f_ in _FJ6["flags"] if _kf0.get(f_[0]) is True)
_anc_ok6 = sum(1 for n_ in _D6.ANCORAS if isinstance(_kf0["axiom_report"].get(n_), list) and _kf0["axiom_report"][n_] and set(_kf0["axiom_report"][n_]) <= _trio6 and _kf0["declaration_sources_v394"].get(n_) == _D6.ANCORAS[n_]["rel"])
U["fechamento_v406_herdado_os_numeros_foram_recalculados_aqui"] = bool(_fontes_ok6 == _D6.N_BUNDLE == _v6["n_modulos_ok"] and _flags_ok6 == len(_FJ6["flags"]) == _CF6["n_flags"] == _v6["n_flags_true"] and _anc_ok6 == _NA6 == _v6["n_ancoras_ok"] and abs(_v6["beta"] - _bf6) <= 1e-15 and abs(c["beta"] / _bf6 - 1.0) <= 1e-9 and set(r6["anchors"]) == set(_D6.ANCORAS)
                                                               and _kf0["formal_files_sha256"].keys() >= set(_D6.BUNDLE_RELS) and len(_kf0["formal_files_sha256"]) == CM["h8"]["entradas"] and ESP == CM["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"])
# as QUATRO chaves: LIDAS do kernel (e nao literal) -- o kernel do rito com o certificado fora do trio faz as tres do rito cairem para False; o que fica False por teorema segue False
_cc6 = _kf6(copiar=("axiom_report",)); _cc6["kernel_formalization"]["axiom_report"][_CF6["ancora_certificado"]] = ["propext", "sorryAx"]
_cc6 = dict(_cc6); [_cc6.__setitem__(k_, copy.deepcopy(c[k_])) for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")]
um.rede_fock_v394(_cc6); um.psibit_v395(_cc6); um.testemunha_estatica_v396(_cc6)
_fa6 = (_cc6.get("psibit_v395") or {}).get("conditional_psion_face") or {}; _fb6 = (_cc6.get("testemunha_estatica_v396") or {}).get("fock_face") or {}
U["fechamento_v406_herdado_as_quatro_chaves_sao_lidas_do_kernel_e_nao_sao_literal"] = bool(c["rede_fock_v394"]["whole_certificate_inhabited"] is True and c["psibit_v395"]["conditional_psion_face"]["inhabitant_exhibited"] is True and c["psibit_v395"]["conditional_psion_face"]["status"] == DL.STATUS_HABITADO
                                                                                   and c["testemunha_estatica_v396"]["fock_face"]["inhabitant_exhibited"] is True and c["testemunha_estatica_v396"]["fock_face"]["status"] == DL.STATUS_HABITADO and c["witness_layers"]["canonical_full_witness_term_constructed"] is True
                                                                                   and (c["psibit_v395"]["conditional_psion_face"].get("reading_v395") or "") and (c["testemunha_estatica_v396"]["fock_face"].get("reading_v396") or "") and c["rede_fock_v394"].get("inhabited_by_v406") and r6["four_keys"]["kernel_reads_the_certificate_as_inhabited"] is True
                                                                                   and _cc6["rede_fock_v394"]["whole_certificate_inhabited"] is False and _fa6.get("inhabitant_exhibited") is False and _fa6.get("status") == DL.STATUS_ANTIGO and _fb6.get("inhabitant_exhibited") is False and _fb6.get("status") == DL.STATUS_ANTIGO
                                                                                   and "JOINT_CONTRACT_OPEN" in str(_cc6["rede_fock_v394"]["verdict"]))
U["fechamento_v406_herdado_o_que_fica_false_por_teorema_segue_false_e_a_chave_do_lema_agora_le_true"] = bool(c["qg_closure"]["gate"]["full_static_witness_exists"] is False and c["witness_rigidity"]["trivial_inhabitant_exists"] is False and list(_CF6["fica_false_por_teorema"]) == DL.FICAM_FALSE_POR_TEOREMA
                                                                                               and c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] is True and r6["four_keys"]["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True   # (v409, errata E18/E20: o lema que faltava na v408 agora existe; a chave le o kernel)
                                                                                               and r6["four_keys"]["qg_closure.gate.full_static_witness_exists"] is False and r6["four_keys"]["witness_rigidity.trivial_inhabitant_exists"] is False)
U["fechamento_v406_herdado_o_gate_nao_se_move_e_o_registro_nao_mexe_em_nada_alem_da_propria_chave"] = bool(((c.get("qg_closure") or {}).get("gate") or {}).get("verdict") == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") == _CF6["baseline"]["gate_verdict"] == _v6["gate_verdict"] and any(ck_["id"] == "c14" and ck_["ok"] for ck_ in r6["mechanics"]["checks"]))
_cc7 = _rapido6(); _cc7.pop("fechamento_v406", None); _antes7 = {k_: _J(_cc7[k_]) for k_ in ("qg_closure", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "kernel_formalization", "external_ladder")}; _k7 = set(_cc7)
um.fechamento_v406(_cc7)
U["fechamento_v406_herdado_so_grava_a_propria_chave_e_nao_toca_nas_outras"] = bool(set(_cc7) - _k7 == {"fechamento_v406"} and all(_J(_cc7[k_]) == v_ for k_, v_ in _antes7.items()))
# --- controles negativos: cada elo recusa
ok_ = True
for n_ in _CF6["ancoras"]:   # axioma fora do trio em CADA ancora lida
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"][n_] = ["propext", "sorryAx"]; ok_ = ok_ and _recusa6(um.fechamento_v406(c_))
U["fechamento_v406_herdado_axioma_fora_do_trio_em_cada_ancora_recusa"] = bool(ok_ and len(_CF6["ancoras"]) == _NA6 == len(_D6.ANCORAS))
ok_ = True
for n_ in _CF6["ancoras"]:   # proveniencia errada em CADA ancora (o compilador diz outro modulo)
    c_ = _kf6(copiar=("declaration_sources_v394",)); c_["kernel_formalization"]["declaration_sources_v394"][n_] = "TGLExt/Outro.lean"; ok_ = ok_ and _recusa6(um.fechamento_v406(c_))
U["fechamento_v406_herdado_proveniencia_errada_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_, f_ in _ANC_FLAGS6.items():   # bandeira falsa de CADA ancora com bandeira
    if f_:
        c_ = _kf6(); c_["kernel_formalization"][f_] = False; ok_ = ok_ and _recusa6(um.fechamento_v406(c_))
U["fechamento_v406_herdado_bandeira_falsa_de_cada_ancora_recusa"] = bool(ok_ and sum(1 for f_ in _ANC_FLAGS6.values() if f_) >= 1)
ok_ = True; n_ok_ = 0
for rel_ in _CF6["source_sha256"]:   # a fonte de CADA um dos 301 modulos adulterada no corpo embutido: recusa, e a contagem cai para 300
    _ant6 = um._EMBEDDED_KERNEL_FILES[rel_]; um._EMBEDDED_KERNEL_FILES[rel_] = _ant6 + " "
    try:
        rr_ = um.fechamento_v406(_rapido6())
    finally:
        um._EMBEDDED_KERNEL_FILES[rel_] = _ant6
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_ok"] is False and rr_["embedded_sources_n_ok"] == _N6 - 1; n_ok_ += 1
U["fechamento_v406_herdado_fonte_adulterada_de_cada_um_dos_301_modulos_recusa"] = bool(ok_ and n_ok_ == _N6 == _D6.N_BUNDLE)
ok_ = True
for rel_ in _CF6["source_sha256"]:   # o hash formal do rito errado em CADA um dos 301 modulos
    c_ = _kf6(copiar=("formal_files_sha256",)); c_["kernel_formalization"]["formal_files_sha256"][rel_] = "0" * 64; rr_ = um.fechamento_v406(c_)
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == _N6 - 1
U["fechamento_v406_herdado_hash_formal_errado_em_cada_um_dos_301_modulos_recusa"] = bool(ok_)
ok_ = True
for ch_ in _CF6["verbatins"]:   # as falas do operador de 02/11 adulteradas (a inscricao falha)
    _ant6 = um._V406_VERBATINS2[ch_]["text"]; um._V406_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
    try:
        rr_ = um.fechamento_v406(_rapido6()); ok_ = ok_ and _recusa6(rr_) and rr_["inscriptions"][ch_] is False
    finally:
        um._V406_VERBATINS2[ch_]["text"] = _ant6
U["fechamento_v406_herdado_inscricao_do_operador_adulterada_recusa"] = bool(ok_ and len(_CF6["verbatins"]) >= 1 and set(_CF6["verbatins"]) <= set(um._V406_VERBATINS2) and len(um._V406_VERBATINS2) == len(DL.VERBATIM_ORIGEM_V406) == 23)
c_ = _rapido6(); c_["external_ladder"] = dict(c_["external_ladder"]); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = um.fechamento_v406(c_)
c2_ = _kf6(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = um.fechamento_v406(c2_)
U["fechamento_v406_herdado_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(_recusa6(rr_) and rr_["exact_ladder"] is False and _recusa6(rr2_))
c_ = _rapido6(); c_["beta"] = c_["beta"] * 1.001; _rb6 = um.fechamento_v406(c_)
_a06 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a06 * 1.001
try:
    _ra6 = um.fechamento_v406(_rapido6())
finally:
    um.SEALED_CODATA_ALPHA = _a06
U["fechamento_v406_herdado_beta_adulterado_recusa"] = bool(_rb6["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb6["verdict"] and _ra6["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra6["verdict"])
# cada checagem de MECANICA negada: a recusa e' a daquela checagem (MECHANICS_CHECK_FAILED + o id)
_mec6 = []   # (id esperado, core mexido)


def _c6_mexe(f_):
    c_ = _rapido6(); f_(c_); return c_


def _set6(c_, caminho_, valor_):
    cur_ = c_
    for k_ in caminho_[:-1]:
        cur_[k_] = dict(cur_[k_]); cur_ = cur_[k_]
    cur_[caminho_[-1]] = valor_


_nao_anc6 = [f_[0] for f_ in _FJ6["flags"] if f_[0] not in set(_ANC_FLAGS6.values())][0]
_mec6.append(("c3", _c6_mexe(lambda c_: None), "raiz"))
_mec6.append(("c4", _c6_mexe(lambda c_: _set6(c_, ["rede_fock_v394", "whole_certificate_inhabited"], False)), None))
_mec6.append(("c5", _c6_mexe(lambda c_: _set6(c_, ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], False)), None))
_mec6.append(("c5", _c6_mexe(lambda c_: _set6(c_, ["psibit_v395", "conditional_psion_face", "status"], DL.STATUS_ANTIGO)), None))
_mec6.append(("c6", _c6_mexe(lambda c_: _set6(c_, ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], False)), None))
_mec6.append(("c6", _c6_mexe(lambda c_: _set6(c_, ["testemunha_estatica_v396", "fock_face", "status"], DL.STATUS_ANTIGO)), None))
_mec6.append(("c7", _c6_mexe(lambda c_: _set6(c_, ["witness_layers", "canonical_full_witness_term_constructed"], False)), None))
_mec6.append(("c8", _c6_mexe(lambda c_: _set6(c_, ["qg_closure", "gate", "full_static_witness_exists"], True)), None))
_mec6.append(("c8", _c6_mexe(lambda c_: _set6(c_, ["witness_rigidity", "trivial_inhabitant_exists"], True)), None))
_mec6.append(("c8", _c6_mexe(lambda c_: _set6(c_, ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], False)), None))   # (v409, errata E20: a c8 da v408 cobrava o lema que faltava SEGUIR False; agora cobra que a chave seja IGUAL a leitura do kernel -- plantar False, o literal antigo, reprova)
_mec6.append(("c10", _c6_mexe(lambda c_: _set6(c_, ["rede_fock_v394", "all_verified"], False)), None))
_mec6.append(("c10", _c6_mexe(lambda c_: _set6(c_, ["psibit_v395", "all_verified"], False)), None))
_mec6.append(("c10", _c6_mexe(lambda c_: _set6(c_, ["testemunha_estatica_v396", "all_verified"], False)), None))
_mec6.append(("c11", _c6_mexe(lambda c_: _set6(c_, ["kernel_formalization", _nao_anc6], False)), None))
_mec6.append(("c12", _c6_mexe(lambda c_: _set6(c_, ["kernel_formalization", "declaration_sources_status_v394", "ok"], False)), None))
_mec6.append(("c14", _c6_mexe(lambda c_: _set6(c_, ["qg_closure", "gate", "verdict"], "OUTRO")), None))
ok_ = True; _det6 = {}
for id_, c_, esp_ in _mec6:
    if esp_ == "raiz":   # c3: a raiz embutida sem os imports do fecho
        _ant6 = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant6.replace("import TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1", "-- retirado")
        try:
            rr_ = um.fechamento_v406(_rapido6())
        finally:
            um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant6
    else:
        rr_ = um.fechamento_v406(c_)
    _det6.setdefault(id_, []).append(_falhos6(rr_))
    ok_ = ok_ and rr_["all_verified"] is False and "MECHANICS_CHECK_FAILED" in rr_["verdict"] and id_ in _falhos6(rr_)
U["fechamento_v406_herdado_cada_checagem_de_mecanica_negada_recusa_pela_propria_checagem"] = bool(ok_ and sorted(_det6) == sorted({"c3", "c4", "c5", "c6", "c7", "c8", "c10", "c11", "c12", "c14"}) and _D6.N_CHECKS_FECHO == r6["mechanics"]["n_checks"])
rep["fechamento_v408_checagens_negadas"] = _det6   # (as checagens do fechamento HERDADO da v408 negadas, uma a uma)
# a GUARDA DAS FRASES: cada frase proibida plantada no texto recusa; a frase certa passa; a MENCAO entre « » (a errata E15 cita a frase errada para corrigi-la) passa
ok_ = True
_dz6 = _TF6["diz"]; _d06 = list(_dz6)
for f_ in ("tudo é teorema", "tudo derivado", "nenhuma hipótese resta", "everything is a theorem", "everything is derived", "no hypothesis remains", "a luz não tem autovetor", "the light has no eigenvector", "o único autovetor", "the only eigenvector",
           "o certificado está confirmado", "o fechamento foi confirmado", "the closure is confirmed", "K(O) ≠ ⊥ está provado", "FULLY_" + "DERIVED"):
    _dz6[:] = _d06 + ["a cadeia: " + f_]
    try:
        rr_ = um.fechamento_v406(_rapido6())
    finally:
        _dz6[:] = _d06
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_violacoes"])
for f_ in (DL.FRASE_DA_MOLDURA_V408_PT, "a errata E15 corrige «a luz não tem autovetor nenhum»", DL.REGRA_DO_4_44):
    _dz6[:] = _d06 + [f_]
    try:
        rr_ = um.fechamento_v406(_rapido6())
    finally:
        _dz6[:] = _d06
    ok_ = ok_ and rr_["all_verified"] is True
U["fechamento_v406_herdado_guarda_das_frases_cada_frase_proibida_recusa_e_a_frase_certa_e_a_mencao_passam"] = bool(ok_ and um.fechamento_v406(cs())["all_verified"] is True)
# --- as falas de 02/11 (cunhagens_v406), as decisoes D34-D40, as erratas E14-E17 e a cobertura exata (kh_n1_cobertura_v406)
_cn6 = c.get("cunhagens_v406") or {}; _xn6 = _cn6.get("extras") or {}
_sp6s = [s_ for s_ in um._V406_SPECS if s_["nome"] == "cunhagens_v406"][0]
U["cunhagens_v406_herdado_falas_de_02nov_decisoes_erratas_e_leituras"] = bool(_cn6.get("all_verified") is True and _cn6.get("does_not_gate_core") is True and len(_cn6.get("verbatim") or {}) == len(DL.VERBATIM_ORIGEM_V406) == len(_D6.VERBATIM_ORIGEM_V406) and all(v_["embedded_ok"] for v_ in (_cn6.get("verbatim") or {}).values())
                                                                      and len(_cn6.get("erratas") or []) == len(_sp6s["erratas"]) == len(_D6.ERRATAS_V406) + 1 and all(e_["assinatura"].startswith("gerencia c1, em nome proprio") for e_ in (_cn6.get("erratas") or [])[:len(_D6.ERRATAS_V406)])
                                                                      and ((_cn6.get("erratas") or [{}])[-1]).get("assinatura") == DL.D7.ASSINA and "E20" in str(((_cn6.get("erratas") or [{}])[-1]).get("agora")) and ((_cn6.get("erratas") or [{}])[-1]).get("ao_lado_de") == "cunhagens_v406 (u7)"   # (HERDADO da v408 sem mudanca na v409: a errata E20 se soma as quatro da v406 [ERRATAS_V406 do delta da v406; a subida mecanica tinha escrito ERRATAS_V408, atributo que o delta da v406 nao tem], ao lado, com a assinatura da v408; o u7 do spec foi de falso a verdadeiro na v408)
                                                                      and len(_cn6.get("leituras_do_operador") or []) == len(_sp6s["leituras_do_operador"]) and set(_xn6.get("decisoes") or {}) >= {"D34", "D35", "D36", "D37", "D40"} and _xn6.get("n_modulos") == _D6.N_BUNDLE and _xn6.get("n_bandeiras") == _CF6["n_flags"]
                                                                      and _xn6.get("assinatura_das_erratas") == _D6.ASSINA and not _GF7.violacoes(str(_cn6.get("verdict"))) and not _GF7.violacoes(json.dumps({k_: _cn6.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)))   # (HERDADO: a errata E20 revisa o u7 do spec -- falso -> verdadeiro --, o veredito nao muda)
_u7_6 = [ck_ for ck_ in _sp6s["checks"] if ck_["id"] == "u7"][0]; _h8_6 = [ck_ for ck_ in [s_ for s_ in um._V406_SPECS if s_["nome"] == "kh_n1_cobertura_v406"][0]["checks"] if ck_["id"] == "h8"][0]
U["erratas_E20_os_tres_registros_da_v406_revistos_u7_c8_e_os_pisos_do_kh"] = bool(_u7_6["op"] == "verdadeiro" and _u7_6["caminho"][-1] == "linked_to_the_corner_by_a_lemma" and "E20" in _u7_6["descricao"] and _h8_6["op"] == "tamanho_maior_igual" and _h8_6["valor"] == _CM7["h8"]["pino_antigo_v406_entradas"] and len(_kf0["formal_files_sha256"]) >= _h8_6["valor"]
                                                                                 and "is bool(_v407_elo_lido(kf_))" in inspect.getsource(um.v406_fechamento_mechanics) and any(str(e_).startswith("E20") for e_ in DL.D7.ERRATAS_V407))   # (o c8 do fechamento_v406 le a chave do kernel: a mutacao c8 acima o mostra; aqui o texto fonte confirma)
U["cunhagens_v406_herdado_o_4_44_nunca_vai_sozinho"] =bool(DL.REGRA_DO_4_44 in (_xn6.get("regra_do_4_44") or "") or any(DL.REGRA_DO_4_44 in str(x_) for x_ in list(_cn6.get("limites") or []) + list(_cn6.get("diz") or [])) or DL.REGRA_DO_4_44 == (_TF6["extras"] or {}).get("regra_do_4_44"))
_kh6x = c.get("kh_n1_cobertura_v406") or {}
_KHT6 = json.load(open(os.path.join(KD, "KH_N1_v409.json"), encoding="utf-8"))["linha_TOTAL"]   # a linha TOTAL do Audit DA v409, lida do arquivo da cadeia (nao digitada)
_KHT6_v406 = json.load(open(os.path.join(DL.V406, _D6.KERNEL_DIR, "KH_N1_v406.json"), encoding="utf-8"))["linha_TOTAL"]   # a linha TOTAL do Audit da v406 (o piso que o spec herdado da v406 cobra)
U["kh_n1_cobertura_v406_herdado_virou_piso_e_selou_na_v409"] = bool(_kh6x.get("all_verified") is True and (c.get("kh_n1_cobertura_v405") or {}).get("all_verified") is True and (_kh6x.get("extras") or {}).get("n_modulos") == _D6.N_BUNDLE and (_kh6x.get("extras") or {}).get("n_bandeiras") == _CF6["n_flags"]
                                                                            and _kf0["axiom_coverage_v392"]["decl"] >= _KHT6_v406["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT6_v406["thm"] and _kf0["axiom_coverage_v392"]["fora_do_trio"] == _KHT6["fora_do_trio"] == 0 and len(_kf0["axiom_report"]) == _KHT6["decl"] > _KHT6_v406["decl"])
rep["fechamento_v406"] = {"verdict": r6["verdict"], "all_verified": r6["all_verified"], "n_checks": r6["mechanics"]["n_checks"], "values": r6["values"], "four_keys": r6["four_keys"], "anchors": r6["anchors"], "embedded_sources_n_ok": r6["embedded_sources_n_ok"], "certificate_inhabited": r6["certificate_inhabited"],
                          "numeros_recalculados": {"fontes_ok": _fontes_ok6, "flags_true": _flags_ok6, "ancoras_ok": _anc_ok6, "beta": _bf6}, "chaves_com_o_certificado_fora_do_trio": {"rede_fock_v394": _cc6["rede_fock_v394"]["whole_certificate_inhabited"], "psibit_v395": _fa6.get("inhabitant_exhibited"), "testemunha_estatica_v396": _fb6.get("inhabitant_exhibited")}}
# (6m) [v407, HERDADO na v408 e na v409 (bloco tirado do ensaio_a_seco_v408.py ORIGINAL): os numeros dele (9 modulos, 76 ancoras, 16 checagens, 98 bandeiras, 3 falas) saem do DL.D7, do contrato HERDADO do candidato e do CANDIDATO_v407.json, NUNCA do DL da v408] O REGISTRO COM FUNCAO psion_canto_v407: tudo certo, os numeros RECALCULADOS aqui por outro caminho,
# a chave do lema (testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) segue LIDA do kernel e nao literal; as quatro da v406 seguem lidas; o que fica False por teorema segue False; o gate que nao se move;
# e cada elo recusa visivelmente (controles negativos): a ancora do lema, as 76 ancoras, as 9 fontes, as 3 falas, a escada, o beta, cada checagem de mecanica isolavel, a guarda das frases (da v407), o teste (d) so' por citacao.
_CP7, _TP7 = um._V407_PSION_CONTRACT, um._V407_PSION_TEXT
_FJ7 = json.load(open(os.path.join(DL.V407, DL.D7.KERNEL_DIR, "FLAGS_v407.json"), encoding="utf-8"))   # (v408) as 98 bandeiras da v407: o FLAGS da v407
_FLAG_NOME7 = {f_[0]: f_[1] for f_ in _FJ7["flags"]}
_ANC_FLAGS7 = {n_: a_.get("flag") for n_, a_ in _CP7["ancoras"].items()}
_LEMA7, _PAR7 = _CP7["ancora_lema"], _CP7["ancora_par"]
_REL_LEMA7 = _CP7["ancoras"][_LEMA7]["rel"]
_rapido7 = lambda: dict(core_s)   # o psion_canto_v407 so' LE o core e grava a propria chave: uma copia rasa basta (os campos mexidos abaixo sao copiados um a um por _kf6/_set6)
r7 = um.psion_canto_v407(cs()); RPSI = r7
_v7 = r7.get("values") or {}
_NCK7 = DL.D7.N_CHECKS_FECHO   # as checagens do registro HERDADO da v407: 16 (c1..c16), lidas do DL.D7
U["psion_canto_v407_herdado_tudo_certo"] = bool(r7["all_verified"] is True and r7["verdict"] == _TP7["veredito_ok"] and r7["runtime_executed"] is True and r7["does_not_gate_core"] is True and r7["mechanics"]["n_checks"] == _NCK7 == len(r7["mechanics"]["checks"]) and all(ck_["ok"] for ck_ in r7["mechanics"]["checks"])
                                        and [ck_["id"] for ck_ in r7["mechanics"]["checks"]] == ["c%d" % i_ for i_ in range(1, _NCK7 + 1)]
                                        and r7["exact_ladder"] is True and r7["embedded_sources_ok"] is True and r7["embedded_sources_n_ok"] == DL.D7.N_BUNDLE == len(DL.D7.BUNDLE_RELS) and r7["link_read_from_the_kernel"] is True and r7["beta_ok"] is True and all(r7["anchors"].values()) and len(r7["anchors"]) == len(DL.D7.ANCORAS)
                                        and all(r7["inscriptions"].values()) and not r7["guarda_violacoes"] and _v7.get("n_ancoras_ok") == _v7.get("n_ancoras") == len(DL.D7.ANCORAS) and _v7.get("n_modulos_ok") == _v7.get("n_modulos") == DL.D7.N_BUNDLE and _v7.get("n_flags_true") == _v7.get("n_flags") == _CP7["n_flags"] == _FJ7["n_flags"] and _v7.get("escada") == [ESP, ESP, ESP]
                                        and r7["lemma"] == DL.D7.ANCORA_LEMA and r7["pair_theorem"] == DL.D7.ANCORA_PAR and r7["pedras"] == list(_CP7["bundle"]["pedras"]) and len(r7["pedras"]) == DL.D7.N_BUNDLE and len(r7["inscriptions"]) == len(DL.D7.VERBATIM_PREFIXOS_DA_ORDEM_V407) == 3)
U["psion_canto_v407_herdado_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(r7) and not _GUARDA98.search(r7["verdict"]) and not um._v407_guarda_frases(r7["verdict"]) and not um._v407_guarda_frases(json.dumps(r7["mechanics"]["checks"], ensure_ascii=False)) and not um._v407_guarda_frases(json.dumps({k_: r7.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope", "fica_aberto", "teste_d")}, ensure_ascii=False))
                                                                  and not _GF7.violacoes(r7["verdict"]) and not _GF7.violacoes(json.dumps({k_: r7.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False)))
# os numeros RECALCULADOS aqui por OUTRO caminho: as fontes pelo BUNDLE_v408.json (lido pelo delta), as bandeiras pelo FLAGS_v408.json, as ancoras pelo DL.D7.ANCORAS e pelo FLAGS (cada ancora com bandeira aponta para a mesma declaracao), o beta pelo alfa x sqrt(e)
_fontes_ok7 = sum(1 for rel_ in DL.D7.BUNDLE_RELS if hashlib.sha256(EMBK[rel_].encode("utf-8")).hexdigest() == DL.D7.BUNDLE_POR_REL[rel_]["sha256"] == _kf0["formal_files_sha256"].get(rel_) == _CP7["source_sha256"][rel_])
_flags_ok7 = sum(1 for f_ in _FJ7["flags"] if _kf0.get(f_[0]) is True)
_anc_ok7 = sum(1 for n_ in DL.D7.ANCORAS if isinstance(_kf0["axiom_report"].get(n_), list) and _kf0["axiom_report"][n_] and set(_kf0["axiom_report"][n_]) <= _trio6 and _kf0["declaration_sources_v394"].get(n_) == DL.D7.ANCORAS[n_]["rel"])
_flag_aponta_7 = all(_FLAG_NOME7.get(a_.get("flag")) == n_ for n_, a_ in _CP7["ancoras"].items() if a_.get("flag"))
U["psion_canto_v407_herdado_os_numeros_foram_recalculados_aqui"] = bool(_fontes_ok7 == DL.D7.N_BUNDLE == _v7["n_modulos_ok"] and _flags_ok7 == len(_FJ7["flags"]) == _CP7["n_flags"] == _v7["n_flags_true"] and _anc_ok7 == len(DL.D7.ANCORAS) == _v7["n_ancoras_ok"] and abs(_v7["beta"] - _bf6) <= 1e-15 and abs(c["beta"] / _bf6 - 1.0) <= 1e-9
                                                                and set(r7["anchors"]) == set(DL.D7.ANCORAS) == set(_CP7["ancoras"]) and set(DL.D7.ANCORAS_POR_MODULO) == set(DL.D7.BUNDLE_RELS) == set(_CP7["ancoras_por_modulo"]) and {rel_: list(v_) for rel_, v_ in DL.D7.ANCORAS_POR_MODULO.items()} == {rel_: list(v_) for rel_, v_ in _CP7["ancoras_por_modulo"].items()}
                                                                and sum(len(v_) for v_ in DL.D7.ANCORAS_POR_MODULO.values()) == len(DL.D7.ANCORAS) and _flag_aponta_7 and _kf0["formal_files_sha256"].keys() >= set(DL.D7.BUNDLE_RELS) and len(_kf0["formal_files_sha256"]) == CM["h8"]["entradas"] and ESP == CM["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CP7["expected_ladder"]
                                                                and _CP7["baseline"]["gate_verdict"] == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") and _CP7["baseline"]["ladder"] == _CM7["escada"][0] and _CP7["baseline"]["sha256"][:16] == _CM7["base_v406_sha16"]
                                                                and max(_CM7["n_axiomas_das_ancoras"].values()) <= len(_trio6) and len(_CM7["n_axiomas_das_ancoras"]) == len(DL.D7.ANCORAS))
# a CHAVE DO LEMA: LIDA do kernel (e nao literal) -- cada elo da leitura tirado faz a chave do core LER False; o elo e' de ESTRUTURA; o que fica False por teorema segue False
_cc7 = _kf6(copiar=("axiom_report",)); _cc7["kernel_formalization"]["axiom_report"][_LEMA7] = ["propext", "sorryAx"]
_cc7 = dict(_cc7); [_cc7.__setitem__(k_, copy.deepcopy(c[k_])) for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396")]
um.rede_fock_v394(_cc7); um.psibit_v395(_cc7); um.testemunha_estatica_v396(_cc7)
_fb7 = (_cc7.get("testemunha_estatica_v396") or {}).get("fock_face") or {}
_elo_neg = {}
_elo_neg["lema_fora_do_trio"] = _fb7.get("linked_to_the_corner_by_a_lemma")   # ponta a ponta: a funcao do registro da v396 recomputada sobre o kf mexido
_kk = _kf6(copiar=("axiom_report",)); _kk["kernel_formalization"]["axiom_report"].pop(_LEMA7); _elo_neg["lema_ausente_do_axiom_report"] = um._v407_elo_lido(_kk["kernel_formalization"])
_kk = _kf6(copiar=("declaration_sources_v394",)); _kk["kernel_formalization"]["declaration_sources_v394"][_LEMA7] = "TGLExt/Outro.lean"; _elo_neg["proveniencia_errada"] = um._v407_elo_lido(_kk["kernel_formalization"])
_kk = _kf6(copiar=("formal_files_sha256",)); _kk["kernel_formalization"]["formal_files_sha256"][_REL_LEMA7] = "0" * 64; _elo_neg["hash_formal_do_modulo_errado"] = um._v407_elo_lido(_kk["kernel_formalization"])
_kk = _kf6(); _kk["kernel_formalization"]["all_verified"] = False; _elo_neg["kernel_recusado"] = um._v407_elo_lido(_kk["kernel_formalization"])
_ef7 = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[_REL_LEMA7] = _ef7[_REL_LEMA7] + " "
try:
    _elo_neg["fonte_embutida_do_modulo_adulterada"] = um._v407_elo_lido(_kf6()["kernel_formalization"])
finally:
    um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(_ef7)
_ct7 = um._V407_PSION_CONTRACT; _ct0 = _ct7.pop("ancora_lema"); _elo_neg["contrato_sem_a_ancora"] = None
try:
    _elo_neg["contrato_sem_a_ancora"] = um._v407_elo_lido(_kf6()["kernel_formalization"])
finally:
    _ct7["ancora_lema"] = _ct0
_elo_pos = um._v407_elo_lido(_kf6()["kernel_formalization"])
_te7 = c["testemunha_estatica_v396"]["fock_face"]; _eloc = _te7.get("elo_v407") or {}
rep["chave_do_lema_lida_do_kernel"] = {"ancora": _LEMA7, "modulo": _REL_LEMA7, "leitura_positiva": _elo_pos, "no_core_do_fluxo": _te7.get("linked_to_the_corner_by_a_lemma"), "controles_negativos_a_chave_le": _elo_neg, "elo_v407": _eloc,
                                       "as_outras_tres_chaves_com_o_lema_fora_do_trio": {"rede_fock_v394.whole_certificate_inhabited": _cc7["rede_fock_v394"]["whole_certificate_inhabited"], "psibit_v395.inhabitant_exhibited": ((_cc7.get("psibit_v395") or {}).get("conditional_psion_face") or {}).get("inhabitant_exhibited"), "testemunha_estatica_v396.inhabitant_exhibited": _fb7.get("inhabitant_exhibited")}}
U["psion_canto_v407_herdado_a_chave_do_lema_e_lida_do_kernel_e_nao_e_literal"] = bool(_elo_pos is True and _te7.get("linked_to_the_corner_by_a_lemma") is True and r7["keys"]["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and r7["keys"]["kernel_reads_the_link"] is True and r7["link_read_from_the_kernel"] is True
                                                                       and all(v_ is False for v_ in _elo_neg.values()) and len(_elo_neg) == 7)
U["psion_canto_v407_herdado_o_lema_fora_do_trio_derruba_so_a_chave_do_lema_e_as_outras_tres_seguem_lidas"] = bool(_fb7.get("linked_to_the_corner_by_a_lemma") is False and _cc7["rede_fock_v394"]["whole_certificate_inhabited"] is True and ((_cc7.get("psibit_v395") or {}).get("conditional_psion_face") or {}).get("inhabitant_exhibited") is True and _fb7.get("inhabitant_exhibited") is True
                                                                                         and _eloc.get("lemma") == _LEMA7 and _eloc.get("kind") == "STRUCTURE_NOT_VECTORS" and _eloc.get("identifies_omega_with_bell_vector") is False and _eloc.get("pair_on_the_fock_face") == "OPEN" and _eloc.get("bell_to_tt_bridge") == "NOT_A_TERM")
U["psion_canto_v407_herdado_o_que_fica_false_por_teorema_segue_false_e_o_que_fica_aberto_e_dito"] = bool(c["qg_closure"]["gate"]["full_static_witness_exists"] is False and c["witness_rigidity"]["trivial_inhabitant_exists"] is False and list(_CP7["fica_false_por_teorema"]) == DL.FICAM_FALSE_POR_TEOREMA
                                                                                                and r7["keys"]["qg_closure.gate.full_static_witness_exists"] is False and r7["keys"]["witness_rigidity.trivial_inhabitant_exists"] is False
                                                                                                and r7["fica_aberto"] == {"par_na_face_de_fock": DL.D7.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "ponte_bell_tt": DL.D7.FICA_ABERTO_PONTE_BELL_TT} == _CP7["fica_aberto"] and "[OPEN]" in DL.D7.FICA_ABERTO_PAR_NA_FACE_DE_FOCK
                                                                                                and all(r7["keys"][k_] is True for k_ in ("rede_fock_v394.whole_certificate_inhabited", "psibit_v395.conditional_psion_face.inhabitant_exhibited", "testemunha_estatica_v396.fock_face.inhabitant_exhibited", "witness_layers.canonical_full_witness_term_constructed")))
U["psion_canto_v407_herdado_o_gate_nao_se_move_e_o_registro_nao_mexe_em_nada_alem_da_propria_chave"] = bool(((c.get("qg_closure") or {}).get("gate") or {}).get("verdict") == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") == _CP7["baseline"]["gate_verdict"] == _v7["gate_verdict"] and any(ck_["id"] == "c14" and ck_["ok"] for ck_ in r7["mechanics"]["checks"]))
_cc8 = _rapido7(); _cc8.pop("psion_canto_v407", None); _antes8 = {k_: _J(_cc8[k_]) for k_ in ("qg_closure", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "kernel_formalization", "external_ladder", "fechamento_v406")}; _k8 = set(_cc8)
um.psion_canto_v407(_cc8)
U["psion_canto_v407_herdado_so_grava_a_propria_chave_e_nao_toca_nas_outras"] = bool(set(_cc8) - _k8 == {"psion_canto_v407"} and all(_J(_cc8[k_]) == v_ for k_, v_ in _antes8.items()))
# --- controles negativos: cada elo recusa
ok_ = True
for n_ in _CP7["ancoras"]:   # axioma fora do trio em CADA ancora lida
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"][n_] = ["propext", "sorryAx"]; ok_ = ok_ and _recusa6(um.psion_canto_v407(c_))
U["psion_canto_v407_herdado_axioma_fora_do_trio_em_cada_ancora_recusa"] = bool(ok_ and len(_CP7["ancoras"]) == len(DL.D7.ANCORAS))
ok_ = True
for n_ in _CP7["ancoras"]:   # proveniencia errada em CADA ancora (o compilador diz outro modulo)
    c_ = _kf6(copiar=("declaration_sources_v394",)); c_["kernel_formalization"]["declaration_sources_v394"][n_] = "TGLExt/Outro.lean"; ok_ = ok_ and _recusa6(um.psion_canto_v407(c_))
U["psion_canto_v407_herdado_proveniencia_errada_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_ in _CP7["ancoras"]:   # ancora AUSENTE do axiom_report do rito
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"].pop(n_); ok_ = ok_ and _recusa6(um.psion_canto_v407(c_))
U["psion_canto_v407_herdado_ancora_ausente_do_kernel_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_, f_ in _ANC_FLAGS7.items():   # bandeira falsa de CADA ancora com bandeira
    if f_:
        c_ = _kf6(); c_["kernel_formalization"][f_] = False; ok_ = ok_ and _recusa6(um.psion_canto_v407(c_))
U["psion_canto_v407_herdado_bandeira_falsa_de_cada_ancora_recusa"] = bool(ok_ and sum(1 for f_ in _ANC_FLAGS7.values() if f_) == len(DL.D7.ANCORAS))
ok_ = True; n_ok_ = 0
for rel_ in _CP7["source_sha256"]:   # a fonte de CADA um dos 9 modulos adulterada no corpo embutido: recusa, e a contagem cai para 8
    _ant7 = um._EMBEDDED_KERNEL_FILES[rel_]; um._EMBEDDED_KERNEL_FILES[rel_] = _ant7 + " "
    try:
        rr_ = um.psion_canto_v407(_rapido7())
    finally:
        um._EMBEDDED_KERNEL_FILES[rel_] = _ant7
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_ok"] is False and rr_["embedded_sources_n_ok"] == DL.D7.N_BUNDLE - 1; n_ok_ += 1
U["psion_canto_v407_herdado_fonte_adulterada_de_cada_um_dos_9_modulos_recusa"] = bool(ok_ and n_ok_ == DL.D7.N_BUNDLE)
ok_ = True
for rel_ in _CP7["source_sha256"]:   # o hash formal do rito errado em CADA um dos 9 modulos
    c_ = _kf6(copiar=("formal_files_sha256",)); c_["kernel_formalization"]["formal_files_sha256"][rel_] = "0" * 64; rr_ = um.psion_canto_v407(c_)
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.D7.N_BUNDLE - 1
U["psion_canto_v407_herdado_hash_formal_errado_em_cada_um_dos_9_modulos_recusa"] = bool(ok_)
ok_ = True
for rel_ in _CP7["source_sha256"]:   # o sha256 PINADO no contrato errado em CADA um dos 9 modulos (o contrato e' o pino: adulterado, a fonte embutida deixa de bater)
    _p0 = _CP7["source_sha256"][rel_]; _CP7["source_sha256"][rel_] = "0" * 64
    try:
        rr_ = um.psion_canto_v407(_rapido7())
    finally:
        _CP7["source_sha256"][rel_] = _p0
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.D7.N_BUNDLE - 1
U["psion_canto_v407_herdado_pino_do_contrato_errado_em_cada_um_dos_9_modulos_recusa"] = bool(ok_)
ok_ = True
for ch_ in _CP7["verbatins"]:   # as falas do operador de 03/11 adulteradas (a inscricao falha)
    _ant7 = um._V407_VERBATINS2[ch_]["text"]; um._V407_VERBATINS2[ch_]["text"] += " "   # restaurado NO LUGAR (o objeto e' compartilhado com _V392_VERBATINS2)
    try:
        rr_ = um.psion_canto_v407(_rapido7()); ok_ = ok_ and _recusa6(rr_) and rr_["inscriptions"][ch_] is False
    finally:
        um._V407_VERBATINS2[ch_]["text"] = _ant7
U["psion_canto_v407_herdado_inscricao_do_operador_adulterada_recusa"] = bool(ok_ and len(_CP7["verbatins"]) == len(DL.D7.VERBATIM_PREFIXOS_DA_ORDEM_V407) == 3 and set(_CP7["verbatins"]) <= set(um._V407_VERBATINS2) and len(um._V407_VERBATINS2) == len(DL.D7.VERBATIM_PREFIXOS_DA_ORDEM_V407))
c_ = _rapido7(); c_["external_ladder"] = dict(c_["external_ladder"]); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = um.psion_canto_v407(c_)
c2_ = _kf6(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = um.psion_canto_v407(c2_)
U["psion_canto_v407_herdado_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(_recusa6(rr_) and rr_["exact_ladder"] is False and _recusa6(rr2_) and rr2_["link_read_from_the_kernel"] is False)
c_ = _rapido7(); c_["beta"] = c_["beta"] * 1.001; _rb7 = um.psion_canto_v407(c_)
_a07 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a07 * 1.001
try:
    _ra7 = um.psion_canto_v407(_rapido7())
finally:
    um.SEALED_CODATA_ALPHA = _a07
U["psion_canto_v407_herdado_beta_adulterado_recusa"] = bool(_rb7["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb7["verdict"] and _ra7["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra7["verdict"])
# cada checagem de MECANICA negada: a recusa e' a daquela checagem (MECHANICS_CHECK_FAILED + o id). As checagens c1, c2, c5, c7 e c9 repetem o que a `_v407_formal` ja' barra antes (ancoras, fontes, escada: FORMAL_OR_SOURCE_EVIDENCE, controles acima) e a c13 e' barrada antes pelo BETA; as demais sao isoladas aqui.
_mec7 = []   # (id esperado, core mexido, especial)
_nao_anc7 = [f_[0] for f_ in _FJ7["flags"] if f_[0] not in set(_ANC_FLAGS7.values())][0]
_resp_teo7 = _CP7["respostas"][0]["teoremas"][0]
_mec7.append(("c3", _c6_mexe(lambda c_: None), "raiz"))
_mec7.append(("c4", _c6_mexe(lambda c_: _set6(c_, ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], False)), None))
_mec7.append(("c6", _c6_mexe(lambda c_: (_set6(c_, ["kernel_formalization", "axiom_report"], dict(c_["kernel_formalization"]["axiom_report"], **{_resp_teo7["completo"]: ["propext", "sorryAx"]})))), None))
_mec7.append(("c6", _c6_mexe(lambda c_: (_set6(c_, ["kernel_formalization", "declaration_sources_v394"], dict(c_["kernel_formalization"]["declaration_sources_v394"], **{_resp_teo7["completo"]: "TGLExt/Outro.lean"})))), None))
_mec7.append(("c8", _c6_mexe(lambda c_: _set6(c_, ["qg_closure", "gate", "full_static_witness_exists"], True)), None))
_mec7.append(("c8", _c6_mexe(lambda c_: _set6(c_, ["witness_rigidity", "trivial_inhabitant_exists"], True)), None))
for nome_c10 in ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396"):
    _mec7.append(("c10", _c6_mexe(lambda c_, n__=nome_c10: _set6(c_, [n__, "all_verified"], False)), None))
_mec7.append(("c11", _c6_mexe(lambda c_: _set6(c_, ["kernel_formalization", _nao_anc7], False)), None))
_mec7.append(("c12", _c6_mexe(lambda c_: _set6(c_, ["kernel_formalization", "declaration_sources_status_v394", "ok"], False)), None))
_mec7.append(("c14", _c6_mexe(lambda c_: _set6(c_, ["qg_closure", "gate", "verdict"], "OUTRO")), None))
_mec7.append(("c15", _c6_mexe(lambda c_: _set6(c_, ["rede_fock_v394", "whole_certificate_inhabited"], False)), None))
_mec7.append(("c15", _c6_mexe(lambda c_: _set6(c_, ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], False)), None))
_mec7.append(("c15", _c6_mexe(lambda c_: _set6(c_, ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], False)), None))
_mec7.append(("c15", _c6_mexe(lambda c_: _set6(c_, ["witness_layers", "canonical_full_witness_term_constructed"], False)), None))
_mec7.append(("c16", _c6_mexe(lambda c_: None), "teste_d_resultado"))
_mec7.append(("c16", _c6_mexe(lambda c_: None), "teste_d_nao_so_citado"))
ok_ = True; _det7 = {}
for id_, c_, esp_ in _mec7:
    if esp_ == "raiz":   # c3: a raiz embutida sem o import do PsionCanto
        _ant7 = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant7.replace("import TGLExt.PsionCanto", "-- retirado")
        try:
            rr_ = um.psion_canto_v407(_rapido7())
        finally:
            um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant7
    elif esp_ in ("teste_d_resultado", "teste_d_nao_so_citado"):   # c16: o teste (d) so' consta por CITACAO; um resultado no um.py (ou a citacao desmarcada) reprova
        _td7 = _CP7["teste_d"]; _td0 = dict(_td7)
        if esp_ == "teste_d_resultado":
            _td7["resultado_no_um_py"] = 4.44
        else:
            _td7["so_citado"] = False
        try:
            rr_ = um.psion_canto_v407(_rapido7())
        finally:
            _td7.clear(); _td7.update(_td0)
    else:
        rr_ = um.psion_canto_v407(c_)
    _det7.setdefault(id_, []).append(_falhos6(rr_))
    ok_ = ok_ and rr_["all_verified"] is False and "MECHANICS_CHECK_FAILED" in rr_["verdict"] and id_ in _falhos6(rr_)
_IDS7 = {"c%d" % i_ for i_ in range(1, _NCK7 + 1)}
_JA_BARRADAS7 = {"c1", "c2", "c5", "c7", "c9", "c13"}
U["psion_canto_v407_herdado_cada_checagem_de_mecanica_negada_recusa_pela_propria_checagem"] = bool(ok_ and set(_det7) | _JA_BARRADAS7 == _IDS7 and not (set(_det7) & _JA_BARRADAS7) and _NCK7 == r7["mechanics"]["n_checks"] and sorted(_det7) == sorted({"c3", "c4", "c6", "c8", "c10", "c11", "c12", "c14", "c15", "c16"}))
rep["psion_canto_v407_herdado_checagens_negadas"] = _det7
# o teste (d) so' por CITACAO do pre-registro: o contrato nao carrega resultado, o manifesto e' pinado por sha256 (lido do arquivo) e o um.py nao tem numero de resultado do teste
_td = _CP7["teste_d"]; _man7 = open(DL.D_TESTE_MANIFESTO, "rb").read()
U["psion_canto_v407_herdado_o_teste_d_so_consta_por_citacao_do_pre_registro_sem_resultado"] = bool(_td["so_citado"] is True and _td["resultado_no_um_py"] is None and hashlib.sha256(_man7).hexdigest() == _td["manifesto_sha256"] and _td["manifesto_sha256"].startswith(_td["manifesto_sha16"])
                                                                              and _td["manifesto_sha16"] == DL.D_TESTE_SHA16_DA_ORDEM and r7["teste_d"] == _td and um._V407_FONTES[_td["fonte_chave"]]["sha256"] == _td["manifesto_sha256"])
# a GUARDA DAS FRASES: cada frase proibida plantada no texto recusa; a frase certa passa; a MENCAO entre « » (a errata E15 cita a frase errada para corrigi-la) passa; o que fica ABERTO, dito, passa
ok_ = True
_dz7 = _TP7["diz"]; _d07 = list(_dz7)
_FRASES_PROIBIDAS7 = ("tudo é teorema", "tudo derivado", "nenhuma hipótese resta", "everything is a theorem", "everything is derived", "no hypothesis remains", "a luz não tem autovetor", "the light has no eigenvector", "o único autovetor", "the only eigenvector",
                      "o certificado está confirmado", "o fechamento foi confirmado", "the closure is confirmed", "K(O) ≠ ⊥ está provado", "FULLY_" + "DERIVED",
                      "o par na face de Fock está provado", "o par de psions na face de Fock foi construído", "the pair on the Fock face is proved", "Ω = Φ⁺", "Omega = Phi+", "o vácuo de Fock é o vetor de Bell", "the Fock vacuum is the Bell vector",
                      "a ponte Bell-TT é teorema", "the Bell-TT bridge is a theorem", "PAIR_ON_THE_FOCK_FACE_" + "PROVED", "PSION_CANTO_CONF" + "IRMED")
for f_ in _FRASES_PROIBIDAS7:
    _dz7[:] = _d07 + ["a cadeia: " + f_]
    try:
        rr_ = um.psion_canto_v407(_rapido7())
    finally:
        _dz7[:] = _d07
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_violacoes"])
_FRASES_BOAS7 = (DL.FRASE_DA_MOLDURA_V408_PT, DL.FRASE_DA_MOLDURA_V407_PT, "a errata E15 corrige «a luz não tem autovetor nenhum»", DL.REGRA_DO_4_44, "o par de psions na face de Fock segue [OPEN]", "Ω ≠ Φ⁺: o elo é de estrutura, não de vetores", "a ponte Bell-TT não é termo", DL.D7.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, DL.D7.FICA_ABERTO_PONTE_BELL_TT)
for f_ in _FRASES_BOAS7:
    _dz7[:] = _d07 + [f_]
    try:
        rr_ = um.psion_canto_v407(_rapido7())
    finally:
        _dz7[:] = _d07
    ok_ = ok_ and rr_["all_verified"] is True
U["psion_canto_v407_herdado_guarda_das_frases_cada_frase_proibida_recusa_e_a_frase_certa_e_a_mencao_passam"] = bool(ok_ and um.psion_canto_v407(cs())["all_verified"] is True and _GF7.controle_negativo()["ok"] is True and len(set(_FRASES_PROIBIDAS7)) == len(_FRASES_PROIBIDAS7))
# --- as falas de 03/11 (cunhagens_v407), as decisoes D41-D47, as erratas E18-E20 e a cobertura exata (kh_n1_cobertura_v407)
_cn7 = c.get("cunhagens_v407") or {}; _xn7 = _cn7.get("extras") or {}
_sp7s = [s_ for s_ in um._V407_SPECS if s_["nome"] == "cunhagens_v407"][0]
U["cunhagens_v407_herdado_falas_de_03nov_decisoes_erratas_e_leituras"] = bool(_cn7.get("all_verified") is True and _cn7.get("does_not_gate_core") is True and len(_cn7.get("verbatim") or {}) == len(DL.D7.VERBATIM_PREFIXOS_DA_ORDEM_V407) == len(_sp7s["verbatins"]) == 3 and all(v_["embedded_ok"] for v_ in (_cn7.get("verbatim") or {}).values())
                                                                      and len(_cn7.get("erratas") or []) == len(_sp7s["erratas"]) == len(DL.D7.ERRATAS_V407) + 2 and all(e_["assinatura"].startswith("gerencia c1") for e_ in (_cn7.get("erratas") or [])) and "E21" in str(((_cn7.get("erratas") or [{}, {}])[-2]).get("agora")) and ((_cn7.get("erratas") or [{}, {}])[-2]).get("assinatura") == DL.D8.ASSINA and "D57(d)" in str(((_cn7.get("erratas") or [{}])[-1]).get("agora")) and ((_cn7.get("erratas") or [{}])[-1]).get("assinatura") == DL.ASSINA
                                                                      and len(_cn7.get("leituras_do_operador") or []) == len(_sp7s["leituras_do_operador"]) and set(_xn7.get("decisoes") or {}) >= {"D41", "D42", "D43", "D44", "D45", "D46", "D47"} and _xn7.get("n_modulos") == DL.D7.N_BUNDLE and _xn7.get("n_bandeiras") == _CP7["n_flags"] and _xn7.get("n_falas") == 3
                                                                      and _xn7.get("assinatura_das_erratas") == DL.D7.ASSINA and _xn7.get("ressalvas") == list(DL.D7.RESSALVAS_V407) == list(_CP7["ressalvas"]) and _xn7.get("nomes_das_pedras") == dict(_CP7["bundle"]["nomes_do_operador"])
                                                                      and not _GF7.violacoes(str(_cn7.get("verdict"))) and not _GF7.violacoes(json.dumps({k_: _cn7.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)) and not um._v407_guarda_frases(json.dumps({k_: _cn7.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)))
_txts444 = (json.dumps(_cn7, ensure_ascii=False), json.dumps(r7, ensure_ascii=False))
U["cunhagens_v407_herdado_o_4_44_nunca_vai_sozinho"] = bool(_CP7["regra_do_4_44"] == DL.REGRA_DO_4_44 and all(("4,44" not in s_) or (DL.REGRA_DO_4_44 in s_) for s_ in _txts444))   # (se um texto da v408 cita o 4,44, ele carrega a regra inteira)
_kh7x = c.get("kh_n1_cobertura_v407") or {}; _kh7s = [s_ for s_ in um._V407_SPECS if s_["nome"] == "kh_n1_cobertura_v407"][0]
_KHT7 = json.load(open(os.path.join(DL.V407, DL.D7.KERNEL_DIR, "KH_N1_v407.json"), encoding="utf-8"))   # a medida do Audit da v407 (o piso que o spec herdado da v407 cobra agora)
_ck7 = {ck_["id"]: ck_ for ck_ in _kh7s["checks"]}
U["kh_n1_cobertura_v407_herdado_virou_piso_e_selou_na_v408"] = bool(_kh7x.get("all_verified") is True and (_kh7x.get("extras") or {}).get("n_modulos") == DL.D7.N_BUNDLE and (_kh7x.get("extras") or {}).get("n_bandeiras") == _CP7["n_flags"]
                                                                        and {i_: _ck7[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh7s["erratas"]) >= 2 and "v408" in str(_kh7s["erratas"][-1].get("agora"))
                                                                        and _ck7["h2"]["valor"] == _KHT7["linha_TOTAL"]["decl"] and _ck7["h3"]["valor"] == _KHT7["linha_TOTAL"]["thm"] and _ck7["h8"]["valor"] == _CM8["h8"]["pino_antigo_v407_entradas"] and len(_kf0["formal_files_sha256"]) >= _ck7["h8"]["valor"]
                                                                        and _kf0["axiom_coverage_v392"]["decl"] >= _KHT7["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT7["linha_TOTAL"]["thm"] and len(_kf0["axiom_report"]) > _KHT7["linha_TOTAL"]["decl"])
print("psion_canto_v407:", r7["all_verified"], "|", r7["verdict"][:96], "| chave do lema (lida do kernel):", c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"], "| controles negativos da chave:", all(v_ is False for v_ in _elo_neg.values()), "| checagens negadas isoladas:", sorted(_det7))
rep["psion_canto_v407"] = {"verdict": r7["verdict"], "all_verified": r7["all_verified"], "n_checks": r7["mechanics"]["n_checks"], "values": r7["values"], "keys": r7["keys"], "anchors": r7["anchors"], "embedded_sources_n_ok": r7["embedded_sources_n_ok"], "link_read_from_the_kernel": r7["link_read_from_the_kernel"], "inscriptions": r7["inscriptions"], "fica_aberto": r7["fica_aberto"],
                          "numeros_recalculados": {"fontes_ok": _fontes_ok7, "flags_true": _flags_ok7, "ancoras_ok": _anc_ok7, "beta": _bf6}, "checagens_negadas": _det7, "elo_v407": _eloc}
# (6n) [v408, HERDADO na v409 (bloco tirado do ensaio_a_seco_v408.py ORIGINAL; os nomes da v408 vem do DL.D8, os numeros do candidato da v408 do _CM8)] O REGISTRO COM FUNCAO tetelestai_terminal_v408: tudo certo; os numeros RECALCULADOS aqui por outro caminho (as quatro fontes pelo BUNDLE_v408.json via DL, as bandeiras pelo FLAGS_v408.json, as 41 ancoras pelo DL.D8.ANCORAS, o beta pelo alfa CODATA x sqrt(e), a aritmetica das pedras pelo math do ensaio);
# NENHUMA chave antiga muda (o core antes e depois do registro e' igual em tudo menos a propria chave); o gate que nao se move; o insumo PURGADO pinado por sha256 e a integra fora; e cada elo recusa visivelmente (controles negativos): as 41 ancoras, as 4 fontes, as 9 falas do contrato, a escada, o beta, as checagens de mecanica que o core alcanca, a guarda das frases (da v408).
_CP8, _TP8 = um._V408_TERMINAL_CONTRACT, um._V408_TERMINAL_TEXT
_FJ8 = json.load(open(os.path.join(DL.V408, DL.D8.KERNEL_DIR, "FLAGS_v408.json"), encoding="utf-8"))   # (v409) as 71 bandeiras da v408: o FLAGS da v408
_FLAG_NOME8 = {f_[0]: f_[1] for f_ in _FJ8["flags"]}
_ANC_FLAGS8 = {n_: a_.get("flag") for n_, a_ in _CP8["ancoras"].items()}
_rapido8 = lambda: dict(core_s)   # o tetelestai_terminal_v408 so' LE o core e grava a propria chave: uma copia rasa basta (os campos mexidos abaixo sao copiados um a um por _kf6/_set6)
r8 = um.tetelestai_terminal_v408(cs()); RTT = r8
_v8 = r8.get("values") or {}
_NCK8 = DL.D8.N_CHECKS_FECHO   # as checagens do registro NOVO: 16 (c1..c16), lidas do DL
U["tetelestai_terminal_v408_tudo_certo"] = bool(r8["all_verified"] is True and r8["verdict"] == _TP8["veredito_ok"] and r8["runtime_executed"] is True and r8["does_not_gate_core"] is True and r8["mechanics"]["n_checks"] == _NCK8 == len(r8["mechanics"]["checks"]) == 16 and all(ck_["ok"] for ck_ in r8["mechanics"]["checks"])
                                                and [ck_["id"] for ck_ in r8["mechanics"]["checks"]] == ["c%d" % i_ for i_ in range(1, _NCK8 + 1)]
                                                and r8["exact_ladder"] is True and r8["embedded_sources_ok"] is True and r8["embedded_sources_n_ok"] == DL.D8.N_BUNDLE == len(DL.D8.BUNDLE_RELS) == 4 and r8["beta_ok"] is True and all(r8["anchors"].values()) and len(r8["anchors"]) == len(DL.D8.ANCORAS) == DL.D8.N_ANCORAS_ESPERADAS == 48
                                                and all(r8["inscriptions"].values()) and not r8["guarda_violacoes"] and _v8.get("n_ancoras_ok") == _v8.get("n_ancoras") == len(DL.D8.ANCORAS) and _v8.get("n_modulos_ok") == _v8.get("n_modulos") == DL.D8.N_BUNDLE and _v8.get("n_flags_true") == _v8.get("n_flags") == _CM8["n_bandeiras"] == _FJ8["n_flags"] and _v8.get("escada") == [ESP, ESP, ESP]
                                                and r8["ancora_principal"] == DL.D8.ANCORA_PRINCIPAL and r8["ancoras_principais"] == list(DL.D8.ANCORAS_PRINCIPAIS) and r8["pedras"] == list(_CP8["bundle"]["pedras"]) == [p_["name"] for p_ in DL.D8.PEDRAS_V408] and r8["nome_provisorio"] is None and r8["chaves_antigas_que_mudam"] == [] and len(r8["inscriptions"]) == len(_CP8["verbatins"]) == 11
                                                and _v8.get("respostas_ok") is True and len(_v8.get("respostas") or {}) == len(DL.D8.RESPOSTAS_DO_OPERADOR) == 8 and all(_v8["por_modulo"].values()) and len(_v8["por_modulo"]) == 4)
U["tetelestai_terminal_v408_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(r8) and not _GUARDA98.search(r8["verdict"]) and not um._v408_guarda_frases(r8["verdict"]) and not um._v408_guarda_frases(json.dumps(r8["mechanics"]["checks"], ensure_ascii=False)) and not um._v408_guarda_frases(json.dumps({k_: r8.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False))
                                                                          and not _GF8.violacoes(r8["verdict"]) and not _GF8.violacoes(json.dumps({k_: r8.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False)))
# os numeros RECALCULADOS aqui por OUTRO caminho: as fontes pelo BUNDLE_v408.json (lido pelo delta), as bandeiras pelo FLAGS_v408.json, as ancoras pelo DL.D8.ANCORAS e pelo FLAGS (cada ancora com bandeira aponta para a mesma declaracao), o beta pelo alfa x sqrt(e)
_fontes_ok8 = sum(1 for rel_ in DL.D8.BUNDLE_RELS if hashlib.sha256(EMBK[rel_].encode("utf-8")).hexdigest() == DL.D8.BUNDLE_POR_REL[rel_]["sha256"] == _kf0["formal_files_sha256"].get(rel_) == _CP8["source_sha256"][rel_])
_flags_ok8 = sum(1 for f_ in _FJ8["flags"] if _kf0.get(f_[0]) is True)
_anc_ok8 = sum(1 for n_ in DL.D8.ANCORAS if isinstance(_kf0["axiom_report"].get(n_), list) and _kf0["axiom_report"][n_] and set(_kf0["axiom_report"][n_]) <= _trio6 and _kf0["declaration_sources_v394"].get(n_) == DL.D8.ANCORAS[n_]["rel"])
_flag_aponta_8 = all(_FLAG_NOME8.get(a_.get("flag")) == n_ for n_, a_ in _CP8["ancoras"].items() if a_.get("flag"))
U["tetelestai_terminal_v408_os_numeros_foram_recalculados_aqui"] = bool(_fontes_ok8 == DL.D8.N_BUNDLE == _v8["n_modulos_ok"] and _flags_ok8 == len(_FJ8["flags"]) == _CM8["n_bandeiras"] == _v8["n_flags_true"] and _anc_ok8 == len(DL.D8.ANCORAS) == _v8["n_ancoras_ok"] and abs(_v8["beta"] - _bf6) <= 1e-15 and abs(c["beta"] / _bf6 - 1.0) <= 1e-9
                                                                        and set(r8["anchors"]) == set(DL.D8.ANCORAS) == set(_CP8["ancoras"]) and set(DL.D8.ANCORAS_POR_MODULO) == set(DL.D8.BUNDLE_RELS) == set(_CP8["ancoras_por_modulo"]) and {rel_: list(v_) for rel_, v_ in DL.D8.ANCORAS_POR_MODULO.items()} == {rel_: list(v_) for rel_, v_ in _CP8["ancoras_por_modulo"].items()}
                                                                        and sum(len(v_) for v_ in DL.D8.ANCORAS_POR_MODULO.values()) == len(DL.D8.ANCORAS) and _flag_aponta_8 and _kf0["formal_files_sha256"].keys() >= set(DL.D8.BUNDLE_RELS) and len(_kf0["formal_files_sha256"]) == CM["h8"]["entradas"] and ESP == CM["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CP8["expected_ladder"]
                                                                        and _CP8["baseline"]["gate_verdict"] == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") and _CP8["baseline"]["ladder"] == _CM8["escada"][0] and _CP8["baseline"]["sha256"][:16] == _CM8["base_v407_sha16"]   # (v409: o baseline do terminal e' a v407, a base da v408)
                                                                        and max(_CM8["n_axiomas_das_ancoras"].values()) <= len(_trio6) and len(_CM8["n_axiomas_das_ancoras"]) == len(DL.D8.ANCORAS) == DL.D8.N_ANCORAS_ESPERADAS == 48)
# a ARITMETICA das pedras (c3 a c11), recalculada aqui pelo math do ensaio com o beta do alfa x sqrt(e): os valores que o registro gravou batem
_ln2_8 = _math.log(2.0); _f12_8 = _math.exp(-0.5)
U["tetelestai_terminal_v408_a_aritmetica_das_pedras_recalculada_aqui"] = bool(abs(_v8["meia_nat_fator"] - _f12_8) <= 1e-15 and 0.0 < _f12_8 < 1.0 and abs((_f12_8 + (1.0 - _f12_8)) - 1.0) <= 1e-15 and abs(_v8["coeficiente_de_jones_s1"] - _math.exp(-_bf6)) <= 1e-15 and 0.0 < _v8["coeficiente_de_jones_s1"] < 1.0 and abs(_v8["ln2"] - _ln2_8) <= 1e-15
                                                                              and _v8["dim_chainIdx_N0_a_N10"] == [2 ** (n_ + 1) for n_ in range(11)] and all(abs(_v8["tempo_da_torre_N0_a_N10"][n_] - (n_ + 1) * _ln2_8 / _bf6) <= 1e-12 * ((n_ + 1) * _ln2_8 / _bf6) for n_ in range(11))
                                                                              and all(abs(_math.exp(-(t_ * _bf6)) - 2.0 ** (-(n_ + 1))) <= 1e-12 for n_, t_ in enumerate(_v8["tempo_da_torre_N0_a_N10"])) and _v8["piso_landauer_T1K_J"] > 0.0 and abs(_v8["piso_landauer_T1K_J"] - um._V408_KB_SI_J_PER_K * _ln2_8) <= 1e-30 and um._V408_KB_SI_J_PER_K > 0.0
                                                                              and abs(_v8["vazamento_t1_g1"] - _math.exp(-_bf6)) <= 1e-15)
# NENHUMA chave antiga muda: o core ANTES e DEPOIS do registro sao iguais em tudo menos a propria chave; o gate nao se move; a chave do lema (v407) segue lida e True; o que fica False por teorema segue False
_cc9 = _rapido8(); _cc9.pop("tetelestai_terminal_v408", None); _antes9 = {k_: _J(_cc9[k_]) for k_ in ("qg_closure", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "kernel_formalization", "external_ladder", "fechamento_v406", "psion_canto_v407")}; _k9 = set(_cc9)
um.tetelestai_terminal_v408(_cc9)
U["tetelestai_terminal_v408_so_grava_a_propria_chave_e_nao_toca_nas_outras"] = bool(set(_cc9) - _k9 == {"tetelestai_terminal_v408"} and all(_J(_cc9[k_]) == v_ for k_, v_ in _antes9.items()))
U["tetelestai_terminal_v408_o_gate_nao_se_move_e_nenhuma_chave_antiga_muda"] = bool(((c.get("qg_closure") or {}).get("gate") or {}).get("verdict") == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") == _CP8["baseline"]["gate_verdict"] == _v8["gate_verdict"] and any(ck_["id"] == "c12" and ck_["ok"] for ck_ in r8["mechanics"]["checks"]) and _CP8["chaves"] == [] and DL.D8.CHAVES_V408 == []
                                                                                   and c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] is True and (c.get("psion_canto_v407") or {}).get("link_read_from_the_kernel") is True and c["qg_closure"]["gate"]["full_static_witness_exists"] is False and c["witness_rigidity"]["trivial_inhabitant_exists"] is False
                                                                                   and list(_CP8["fica_false_por_teorema"]) == DL.D8.FICAM_FALSE_POR_TEOREMA and r8["fica_aberto"] == {"par_na_face_de_fock": DL.D8.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "ponte_bell_tt": DL.D8.FICA_ABERTO_PONTE_BELL_TT} == _CP8["fica_aberto"] and "[OPEN]" in DL.D8.FICA_ABERTO_PAR_NA_FACE_DE_FOCK and "E21" in DL.D8.FICA_ABERTO_PAR_NA_FACE_DE_FOCK)
# o insumo PURGADO (E23): pinado por sha256 e relido do disco; a integra NAO e' fonte desta versao (citada so' por sha16); o recibo da purga e' fonte
_ip8 = _CP8["insumo_purgado"]; _fp8 = um._V408_FONTES[_ip8["fonte_chave"]]
U["tetelestai_terminal_v408_o_insumo_purgado_e_pinado_e_a_integra_fica_fora"] = bool(_fp8["sha256"] == _ip8["sha256"] == hashlib.sha256(open(_fp8["arquivo"], "rb").read()).hexdigest() == DL.D8.PURGADO_SHA256 and _ip8["integra_fora_do_espelho"] is True and _ip8["integra_pinada"] is False and _ip8["integra_sha16"] == DL.D8.ORIGEM_PURGA_SHA16_DA_ORDEM
                                                                                    and not any(str(v_.get("sha256", "")).startswith(_ip8["integra_sha16"]) for v_ in um._V408_FONTES.values()) and _ip8["recibo_chave"] in um._V408_FONTES and r8["insumo_purgado"] == _ip8 and any(ck_["id"] == "c15" and ck_["ok"] for ck_ in r8["mechanics"]["checks"])
                                                                                    and _ip8["linhas_substituidas"] == DL.D8.PURGA_LINHAS_SUBSTITUIDAS and _ip8["ocorrencias_na_guarda"] == 0)
# --- controles negativos: cada elo recusa
ok_ = True
for n_ in _CP8["ancoras"]:   # axioma fora do trio em CADA ancora lida
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"][n_] = ["propext", "sorryAx"]; ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_axioma_fora_do_trio_em_cada_ancora_recusa"] = bool(ok_ and len(_CP8["ancoras"]) == len(DL.D8.ANCORAS) == DL.D8.N_ANCORAS_ESPERADAS == 48)   # (r2, 05/11: 14 + 9 + 7 + 18 depois da R3 do PIgualNP)
ok_ = True
for n_ in _CP8["ancoras"]:   # proveniencia errada em CADA ancora (o compilador diz outro modulo)
    c_ = _kf6(copiar=("declaration_sources_v394",)); c_["kernel_formalization"]["declaration_sources_v394"][n_] = "TGLExt/Outro.lean"; ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_proveniencia_errada_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_ in _CP8["ancoras"]:   # ancora AUSENTE do axiom_report do rito
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"].pop(n_); ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_ancora_ausente_do_kernel_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_, f_ in _ANC_FLAGS8.items():   # bandeira falsa de CADA ancora com bandeira
    if f_:
        c_ = _kf6(); c_["kernel_formalization"][f_] = False; ok_ = ok_ and _recusa6(um.tetelestai_terminal_v408(c_))
U["tetelestai_terminal_v408_bandeira_falsa_de_cada_ancora_recusa"] = bool(ok_ and sum(1 for f_ in _ANC_FLAGS8.values() if f_) == len(DL.D8.ANCORAS))
ok_ = True; n_ok_ = 0
for rel_ in _CP8["source_sha256"]:   # a fonte de CADA um dos 4 modulos adulterada no corpo embutido: recusa, e a contagem cai para 3
    _ant8 = um._EMBEDDED_KERNEL_FILES[rel_]; um._EMBEDDED_KERNEL_FILES[rel_] = _ant8 + " "
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        um._EMBEDDED_KERNEL_FILES[rel_] = _ant8
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_ok"] is False and rr_["embedded_sources_n_ok"] == DL.D8.N_BUNDLE - 1; n_ok_ += 1
U["tetelestai_terminal_v408_fonte_adulterada_de_cada_um_dos_4_modulos_recusa"] = bool(ok_ and n_ok_ == DL.D8.N_BUNDLE == 4)
ok_ = True
for rel_ in _CP8["source_sha256"]:   # o hash formal do rito errado em CADA um dos 4 modulos
    c_ = _kf6(copiar=("formal_files_sha256",)); c_["kernel_formalization"]["formal_files_sha256"][rel_] = "0" * 64; rr_ = um.tetelestai_terminal_v408(c_)
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.D8.N_BUNDLE - 1
U["tetelestai_terminal_v408_hash_formal_errado_em_cada_um_dos_4_modulos_recusa"] = bool(ok_)
ok_ = True
for rel_ in _CP8["source_sha256"]:   # o sha256 PINADO no contrato errado em CADA um dos 4 modulos
    _p08 = _CP8["source_sha256"][rel_]; _CP8["source_sha256"][rel_] = "0" * 64
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        _CP8["source_sha256"][rel_] = _p08
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.D8.N_BUNDLE - 1
U["tetelestai_terminal_v408_pino_do_contrato_errado_em_cada_um_dos_4_modulos_recusa"] = bool(ok_)
ok_ = True
for ch_ in _CP8["verbatins"]:   # a inscricao do operador adulterada em CADA fala do contrato (o texto embutido muda: o sha256 deixa de bater)
    _v08 = um._V408_VERBATINS2[ch_]["text"]; um._V408_VERBATINS2[ch_]["text"] = _v08 + " "
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8()); ok_ = ok_ and _recusa6(rr_) and rr_["inscriptions"][ch_] is False
    finally:
        um._V408_VERBATINS2[ch_]["text"] = _v08
U["tetelestai_terminal_v408_inscricao_do_operador_adulterada_recusa"] = bool(ok_ and len(_CP8["verbatins"]) == 11 and set(_CP8["verbatins"]) <= set(um._V408_VERBATINS2) and len(um._V408_VERBATINS2) == len(DL.D8.VERBATIM_PREFIXOS_DA_ORDEM_V408) == DL.D8.N_FALAS_V408 == 15)
c_ = _rapido8(); c_["external_ladder"] = dict(c_["external_ladder"]); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = um.tetelestai_terminal_v408(c_)
c2_ = _kf6(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = um.tetelestai_terminal_v408(c2_)
U["tetelestai_terminal_v408_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(_recusa6(rr_) and rr_["exact_ladder"] is False and _recusa6(rr2_))
c_ = _rapido8(); c_["beta"] = c_["beta"] * 1.001; _rb8 = um.tetelestai_terminal_v408(c_)
_a08 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a08 * 1.001
try:
    _ra8 = um.tetelestai_terminal_v408(_rapido8())
finally:
    um.SEALED_CODATA_ALPHA = _a08
U["tetelestai_terminal_v408_beta_adulterado_recusa"] = bool(_rb8["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb8["verdict"] and _ra8["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra8["verdict"])
# cada checagem de MECANICA que o core alcanca, negada: a recusa e' a daquela checagem (MECHANICS_CHECK_FAILED + o id). As checagens c1, c2, c14 e c16 repetem o que a `_v408_formal` e o beta ja' barram antes (controles acima); c3 a c11 sao ARITMETICA PURA com beta em runtime e nao tem core que as negue:
# a mecanica e' chamada direto com beta = 0 (fora do intervalo aberto: c6, c7, c9 e c16 caem) e com o gate do contrato trocado (c12 cai), o que mostra que cada uma mede o que diz.
_mec8 = []   # (id esperado, core mexido, especial)
_nao_anc8 = [f_[0] for f_ in _FJ8["flags"] if f_[0] not in set(_ANC_FLAGS8.values())]
_mec8.append(("c2", _c6_mexe(lambda c_: None), "raiz"))
_mec8.append(("c12", _c6_mexe(lambda c_: _set6(c_, ["qg_closure", "gate", "verdict"], "OUTRO")), None))
if _nao_anc8:
    _mec8.append(("c13", _c6_mexe(lambda c_: _set6(c_, ["kernel_formalization", _nao_anc8[0]], False)), None))
_mec8.append(("c15", _c6_mexe(lambda c_: None), "fonte_purgada_adulterada"))
ok_ = True; _det8 = {}
for id_, c_, esp_ in _mec8:
    if esp_ == "raiz":   # c2: a raiz embutida sem o import da TetelestaiTerminal (as fontes seguem batendo; a raiz nao traz os quatro imports)
        _ant8 = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant8.replace("import TGLExt.TetelestaiTerminal", "-- retirado")
        try:
            rr_ = um.tetelestai_terminal_v408(_rapido8())
        finally:
            um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant8
    elif esp_ == "fonte_purgada_adulterada":   # c15: o sha256 pinado da fonte purgada trocado: a releitura do disco deixa de bater
        _s08 = um._V408_FONTES[_ip8["fonte_chave"]]["sha256"]; um._V408_FONTES[_ip8["fonte_chave"]]["sha256"] = "0" * 64
        try:
            rr_ = um.tetelestai_terminal_v408(_rapido8())
        finally:
            um._V408_FONTES[_ip8["fonte_chave"]]["sha256"] = _s08
    else:
        rr_ = um.tetelestai_terminal_v408(c_)
    _det8.setdefault(id_, []).append(_falhos6(rr_))
    ok_ = ok_ and rr_["all_verified"] is False and "MECHANICS_CHECK_FAILED" in rr_["verdict"] and id_ in _falhos6(rr_)
_mt0 = um.v408_terminal_mechanics(0.0, cs(), _CP8)   # beta fora do intervalo aberto: as aritmeticas com beta caem (c6, c7, c9) e a c16
_mtg = um.v408_terminal_mechanics(_bf6, cs(), dict(_CP8, baseline=dict(_CP8["baseline"], gate_verdict="OUTRO")))   # o gate do contrato trocado: c12 cai
_mtn = um.v408_terminal_mechanics(_bf6, cs(), dict(_CP8, n_ancoras=len(_CP8["ancoras"]) + 1))   # o contrato pede uma ancora a mais: c1 cai
_f0_ = lambda m_: sorted(ck_["id"] for ck_ in m_["checks"] if not ck_["ok"])
_IDS8 = {"c%d" % i_ for i_ in range(1, _NCK8 + 1)}
U["tetelestai_terminal_v408_cada_checagem_de_mecanica_negada_recusa_pela_propria_checagem"] = bool(ok_ and set(_det8) <= _IDS8 and sorted(_det8) == sorted({"c2", "c12", "c15"} | ({"c13"} if _nao_anc8 else set())) and _NCK8 == r8["mechanics"]["n_checks"]
                                                                                                   and _mt0["passed"] is False and {"c6", "c7", "c9", "c16"} <= set(_f0_(_mt0)) and _mtg["passed"] is False and _f0_(_mtg) == ["c12"] and _mtn["passed"] is False and _f0_(_mtn) == ["c1"]
                                                                                                   and um.v408_terminal_mechanics(_bf6, cs(), _CP8)["passed"] is True)
rep["tetelestai_terminal_v408_checagens_negadas"] = {"por_core": _det8, "beta_zero": _f0_(_mt0), "gate_trocado": _f0_(_mtg), "ancora_a_mais_no_contrato": _f0_(_mtn)}
# a GUARDA DAS FRASES (v405 a v408): cada frase proibida plantada no texto recusa; a frase certa passa; o que fica ABERTO, dito, passa
ok_ = True
_dz8 = _TP8["diz"]; _d08 = list(_dz8)
_FRASES_PROIBIDAS8 = ("tudo é teorema", "tudo derivado", "nenhuma hipótese resta", "everything is a theorem", "a luz não tem autovetor", "o único autovetor", "o certificado está confirmado", "the closure is confirmed", "K(O) ≠ ⊥ está provado", "FULLY_" + "DERIVED",
                      "o par na face de Fock está provado", "Ω = Φ⁺", "o vácuo de Fock é o vetor de Bell", "a ponte Bell-TT é teorema", "PAIR_ON_THE_FOCK_FACE_" + "PROVED",
                      "há relação sem peso", "relação sem peso existe", "there is a relation without weight", "o que resta sem peso é relação", "a TGL não tem terminal", "the TGL has no terminal", "P = NP está provado", "P = NP is a theorem", "provamos que P = NP",
                      "a impedância é um termo", "termo de impedância", "leitura do operador [ONTO]", "[ONTO] do operador", "TERMINAL_CONF" + "IRMED", "P_EQUALS_NP", "CLASSES_PROVED",
                      "a TGL prova P = NP de Turing", "the TGL proves P = NP for Turing machines", "o P = nP não trata das classes", "a igualdade das classes P e NP segue podada")   # (D51 revista, 04/11 noite)
_GD8p_ = []
for f_ in _FRASES_PROIBIDAS8:
    _dz8[:] = _d08 + ["a cadeia: " + f_]
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        _dz8[:] = _d08
    ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_violacoes"])
    if not (rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_violacoes"])):
        _GD8p_.append([f_, rr_.get("verdict")])
_FRASES_BOAS8 = (DL.D8.FRASE_DA_MOLDURA_V408_PT, DL.D8.FRASE_DA_MOLDURA_V408_EN, DL.D8.FRASE_DA_MOLDURA_V407_PT, "não há relação sem peso", "relação sem peso é a origem da mentira", "relação sem peso é impossível", "there is no relation without weight", "«P = nP» só no sentido do operador: P só é P lido pelo módulo n minimamente acoplado",
                 "a palavra «impedância» fica podada como termo; o nome do operador é «inclinação modular (cociclo)»", DL.REGRA_DO_4_44, DL.D8.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "o terminal é a leitura, não o fim do decaimento", "o zero inscrito é o Um; o Um não é o zero absoluto", DL.D8.FRASE_D51_PT, DL.D8.FRASE_D51_EN)   # (D51 revista: a frase certa das classes do dicionario passa)
_GD8 = {"proibidas_que_passaram": _GD8p_, "boas_que_reprovaram": []}   # (diagnostico desta checagem: qual frase falhou, para o relatorio do ensaio)
for f_ in _FRASES_BOAS8:
    _dz8[:] = _d08 + [f_]
    try:
        rr_ = um.tetelestai_terminal_v408(_rapido8())
    finally:
        _dz8[:] = _d08
    ok_ = ok_ and rr_["all_verified"] is True
    if rr_["all_verified"] is not True:
        _GD8["boas_que_reprovaram"].append([f_[:80], rr_.get("verdict"), (rr_.get("guarda_violacoes") or [])[:2]])
_GD8["gf5_controle_ok"] = _GF8.controle_negativo()["ok"]; _GD8["registro_ok"] = um.tetelestai_terminal_v408(cs())["all_verified"]
rep["tetelestai_terminal_v408_guarda_das_frases_diagnostico"] = _GD8
U["tetelestai_terminal_v408_guarda_das_frases_cada_frase_proibida_recusa_e_a_frase_certa_passa"] = bool(ok_ and um.tetelestai_terminal_v408(cs())["all_verified"] is True and _GF8.controle_negativo()["ok"] is True and len(set(_FRASES_PROIBIDAS8)) == len(_FRASES_PROIBIDAS8))
# --- as falas de 04/11 (cunhagens_v408), as decisoes D48-D54, as erratas E21-E23 e a cobertura exata (kh_n1_cobertura_v408)
_cn8 = c.get("cunhagens_v408") or {}; _xn8 = _cn8.get("extras") or {}
_sp8s = [s_ for s_ in um._V408_SPECS if s_["nome"] == "cunhagens_v408"][0]
U["cunhagens_v408_herdado_falas_de_04nov_decisoes_erratas_e_leituras_e_a_E26_ao_lado"] = bool(_cn8.get("all_verified") is True and _cn8.get("does_not_gate_core") is True and len(_cn8.get("verbatim") or {}) == len(DL.D8.VERBATIM_PREFIXOS_DA_ORDEM_V408) == len(_sp8s["verbatins"]) == DL.D8.N_FALAS_V408 == 15 and all(v_["embedded_ok"] for v_ in (_cn8.get("verbatim") or {}).values())
                                                                      and len(_cn8.get("erratas") or []) == len(_sp8s["erratas"]) == 5 and all(e_["assinatura"] == DL.D8.ASSINA for e_ in (_cn8.get("erratas") or [])[:4]) and [("E21" in str(e_.get("agora"))) for e_ in (_cn8.get("erratas") or [])][0] is True and "E26" in str(((_cn8.get("erratas") or [{}])[-1]).get("agora")) and ((_cn8.get("erratas") or [{}])[-1]).get("assinatura") == DL.ASSINA
                                                                      and len(_cn8.get("leituras_do_operador") or []) == len(_sp8s["leituras_do_operador"]) == len(DL.D8.FRASES_V408) and set(_xn8.get("decisoes") or {}) == {"D48", "D49", "D50", "D51", "D52", "D53", "D54"} and _xn8.get("n_modulos") == DL.D8.N_BUNDLE and _xn8.get("n_bandeiras") == _CM8["n_bandeiras"] and _xn8.get("n_falas") == 15
                                                                      and _xn8.get("assinatura_das_erratas") == DL.D8.ASSINA and _xn8.get("ressalvas") == list(DL.D8.RESSALVAS_V408) == list(_CP8["ressalvas"]) and _xn8.get("nomes_das_pedras") == dict(_CP8["bundle"]["nomes_do_operador"]) and sorted((_xn8.get("autores") or {}).values()) == sorted(["operador"] * 13 + [DL.D8.AUTOR_MISTO] * 2)
                                                                      and not _GF8.violacoes(str(_cn8.get("verdict"))) and not _GF8.violacoes(json.dumps({k_: _cn8.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)) and not um._v408_guarda_frases(json.dumps({k_: _cn8.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)))
_mist8 = {k_: v_ for k_, v_ in um._V408_VERBATINS2.items() if v_.get("autor") == DL.D8.AUTOR_MISTO}   # os dois arquivos de autor misto: o texto EMBUTIDO e' so' o paragrafo do operador (o corte nao aparece); o arquivo inteiro entra por sha256
U["cunhagens_v408_os_dois_arquivos_de_autor_misto_embutem_so_o_paragrafo_do_operador"] = bool(len(_mist8) == 2 and all(v_["corte"] not in v_["text"] and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and hashlib.sha256(open(v_["arquivo_inteiro"], "rb").read()).hexdigest() == v_["sha256_arquivo_inteiro"] != v_["sha256"] and v_["corte"] in open(v_["arquivo_inteiro"], encoding="utf-8").read() for v_ in _mist8.values())
                                                                                                and all(v_.get("autor") == "operador" for k_, v_ in um._V408_VERBATINS2.items() if k_ not in _mist8))
_txts444_8 = (json.dumps(_cn8, ensure_ascii=False), json.dumps(r8, ensure_ascii=False))
U["cunhagens_v408_o_4_44_nunca_vai_sozinho"] = bool(_CP8["regra_do_4_44"] == DL.REGRA_DO_4_44 and all(("4,44" not in s_) or (DL.REGRA_DO_4_44 in s_) for s_ in _txts444_8))   # (se um texto da v408 cita o 4,44, ele carrega a regra inteira)
_kh8x = c.get("kh_n1_cobertura_v408") or {}; _kh8s = [s_ for s_ in um._V408_SPECS if s_["nome"] == "kh_n1_cobertura_v408"][0]
_KHT8 = json.load(open(os.path.join(DL.V408, DL.D8.KERNEL_DIR, "KH_N1_v408.json"), encoding="utf-8"))   # a medida do Audit da v408 (o piso que o spec herdado da v408 cobra agora)
_cov0 = core0["kernel_formalization"]["axiom_coverage_v392"]
_ck8 = {ck_["id"]: ck_ for ck_ in _kh8s["checks"]}
_h8v8 = _ck8["h8"]["valor"]
U["kh_n1_cobertura_v408_herdado_virou_piso_e_selou_na_v409"] = bool(_kh8x.get("all_verified") is True and _kh7x.get("all_verified") is True and (_kh8x.get("extras") or {}).get("n_modulos") == DL.D8.N_BUNDLE and (_kh8x.get("extras") or {}).get("n_bandeiras") == _CM8["n_bandeiras"]
                                                                        and {i_: _ck8[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh8s["erratas"]) >= 2 and "v409" in str(_kh8s["erratas"][-1].get("agora"))
                                                                        and _ck8["h2"]["valor"] == _KHT8["linha_TOTAL"]["decl"] and _ck8["h3"]["valor"] == _KHT8["linha_TOTAL"]["thm"] and _ck8["h8"]["valor"] == CM["h8"]["pino_antigo_v408_entradas"] and len(_kf0["formal_files_sha256"]) >= _ck8["h8"]["valor"]
                                                                        and _kf0["axiom_coverage_v392"]["decl"] >= _KHT8["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT8["linha_TOTAL"]["thm"] and len(_kf0["axiom_report"]) > _KHT8["linha_TOTAL"]["decl"])
print("tetelestai_terminal_v408:", r8["all_verified"], "|", r8["verdict"][:96], "| ancoras:", _v8.get("n_ancoras_ok"), "/", _v8.get("n_ancoras"), "| checagens negadas:", sorted(_det8), "| beta=0:", _f0_(_mt0))
rep["tetelestai_terminal_v408"] = {"verdict": r8["verdict"], "all_verified": r8["all_verified"], "n_checks": r8["mechanics"]["n_checks"], "values": {k_: v_ for k_, v_ in r8["values"].items() if k_ not in ("ancoras",)}, "anchors": r8["anchors"], "embedded_sources_n_ok": r8["embedded_sources_n_ok"],
                                   "numeros_recalculados": {"fontes_ok": _fontes_ok8, "flags_true": _flags_ok8, "ancoras_ok": _anc_ok8, "beta": _bf6}, "checagens_negadas": rep["tetelestai_terminal_v408_checagens_negadas"], "insumo_purgado": _ip8, "nome_provisorio": r8["nome_provisorio"]}
# (6o) [v409] O REGISTRO COM FUNCAO traducao_turing_v409 (o NOVO desta versao): tudo certo; os numeros RECALCULADOS aqui por outro caminho (a fonte pelo BUNDLE_v409.json via DL, as bandeiras pelo FLAGS_v409.json, as 82 ancoras pelo DL.ANCORAS, o beta pelo alfa CODATA x sqrt(e),
# a instancia de brinquedo REFEITA aqui por enumeracao propria); NENHUMA chave antiga muda (o core antes e depois do registro e' igual em tudo menos a propria chave); o gate que nao se move; o pino do acervo da v407 repinado (D57d); e cada elo recusa visivelmente (controles negativos): as 82 ancoras,
# a fonte de cada um dos DOIS modulos, as 14 falas do contrato, a escada, o beta, as checagens de mecanica (cada uma negada recusa pela PROPRIA checagem), a guarda das frases (da v409).
import itertools as _it9
_CP9, _TP9 = um._V409_TRADUCAO_CONTRACT, um._V409_TRADUCAO_TEXT
_FJ9 = json.load(open(os.path.join(KD, "FLAGS_v409.json"), encoding="utf-8"))
_FLAG_NOME9 = {f_[0]: f_[1] for f_ in _FJ9["flags"]}
_ANC_FLAGS9 = {n_: a_.get("flag") for n_, a_ in _CP9["ancoras"].items()}
_rapido9 = lambda: dict(core_s)   # o traducao_turing_v409 so' LE o core e grava a propria chave: uma copia rasa basta (os campos mexidos abaixo sao copiados um a um por _kf6/_set6)
r9 = um.traducao_turing_v409(cs()); RTU = r9
_v9 = r9.get("values") or {}
_NCK9 = DL.N_CHECKS_FECHO   # as checagens do registro NOVO: 20 (c1..c20), lidas do DL
U["traducao_turing_v409_tudo_certo"] = bool(r9["all_verified"] is True and r9["verdict"] == _TP9["veredito_ok"] and r9["runtime_executed"] is True and r9["does_not_gate_core"] is True and r9["mechanics"]["n_checks"] == _NCK9 == len(r9["mechanics"]["checks"]) == 20 and all(ck_["ok"] for ck_ in r9["mechanics"]["checks"])
                                            and [ck_["id"] for ck_ in r9["mechanics"]["checks"]] == ["c%d" % i_ for i_ in range(1, _NCK9 + 1)]
                                            and r9["exact_ladder"] is True and r9["embedded_sources_ok"] is True and r9["embedded_sources_n_ok"] == DL.N_BUNDLE == len(DL.BUNDLE_RELS) == 2 and r9["beta_ok"] is True and all(r9["anchors"].values()) and len(r9["anchors"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 82
                                            and all(r9["inscriptions"].values()) and not r9["guarda_violacoes"] and _v9.get("n_ancoras_ok") == _v9.get("n_ancoras") == len(DL.ANCORAS) and _v9.get("n_modulos_ok") == _v9.get("n_modulos") == DL.N_BUNDLE and _v9.get("n_flags_true") == _v9.get("n_flags") == CM["n_bandeiras"] == _FJ9["n_flags"] and _v9.get("escada") == [ESP, ESP, ESP]
                                            and r9["ancora_principal"] == DL.ANCORA_PRINCIPAL and r9["ancoras_principais"] == list(DL.ANCORAS_PRINCIPAIS) and r9["ancoras_de_secao"] == list(DL.ANCORAS_DE_SECAO) and r9["pedras"] == list(_CP9["bundle"]["pedras"]) == [p_["name"] for p_ in DL.PEDRAS_V409] and r9["chaves_antigas_que_mudam"] == []
                                            and len(r9["inscriptions"]) == len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 14 and _v9.get("respostas_ok") is True and len(_v9.get("respostas") or {}) == len(DL.RESPOSTAS_DO_OPERADOR) == 9 and all(_v9["por_modulo"].values()) and len(_v9["por_modulo"]) == DL.N_BUNDLE == 2
                                            and r9["nomes_ratificados"] == dict(DL.NOMES_RATIFICADOS) and r9["alcance"]["frase"] == DL.FRASE_D56_PT and r9["alcance"]["qualificador"] == DL.FRASE_QUALIFICADOR_PT)
U["traducao_turing_v409_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(r9) and not _GUARDA98.search(r9["verdict"]) and not um._v409_guarda_frases(r9["verdict"]) and not um._v409_guarda_frases(json.dumps(r9["mechanics"]["checks"], ensure_ascii=False)) and not um._v409_guarda_frases(json.dumps({k_: r9.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False))
                                                                      and not _GF5.violacoes(r9["verdict"]) and not _GF5.violacoes(json.dumps({k_: r9.get(k_) for k_ in ("limites", "diz", "nao_diz", "ressalvas", "scope")}, ensure_ascii=False))
                                                                      and not any(t_ in r9["verdict"] for t_ in DL.TOKENS_PROIBIDOS_V409))
# os numeros RECALCULADOS aqui por OUTRO caminho: a fonte pelo BUNDLE_v409.json (lido pelo delta), as bandeiras pelo FLAGS_v409.json, as ancoras pelo DL.ANCORAS e pelo FLAGS (cada ancora com bandeira aponta para a mesma declaracao), o beta pelo alfa x sqrt(e)
_fontes_ok9 = sum(1 for rel_ in DL.BUNDLE_RELS if hashlib.sha256(EMBK[rel_].encode("utf-8")).hexdigest() == DL.BUNDLE_POR_REL[rel_]["sha256"] == _kf0["formal_files_sha256"].get(rel_) == _CP9["source_sha256"][rel_])
_flags_ok9 = sum(1 for f_ in _FJ9["flags"] if _kf0.get(f_[0]) is True)
_anc_ok9 = sum(1 for n_ in DL.ANCORAS if isinstance(_kf0["axiom_report"].get(n_), list) and _kf0["axiom_report"][n_] and set(_kf0["axiom_report"][n_]) <= _trio6 and _kf0["declaration_sources_v394"].get(n_) == DL.ANCORAS[n_]["rel"])
_flag_aponta_9 = all(_FLAG_NOME9.get(a_.get("flag")) == n_ for n_, a_ in _CP9["ancoras"].items() if a_.get("flag"))
U["traducao_turing_v409_os_numeros_foram_recalculados_aqui"] = bool(_fontes_ok9 == DL.N_BUNDLE == _v9["n_modulos_ok"] and _flags_ok9 == len(_FJ9["flags"]) == CM["n_bandeiras"] == _v9["n_flags_true"] and _anc_ok9 == len(DL.ANCORAS) == _v9["n_ancoras_ok"] and abs(_v9["beta"] - _bf6) <= 1e-15 and abs(c["beta"] / _bf6 - 1.0) <= 1e-9
                                                                    and set(r9["anchors"]) == set(DL.ANCORAS) == set(_CP9["ancoras"]) and set(DL.ANCORAS_POR_MODULO) == set(DL.BUNDLE_RELS) == set(_CP9["ancoras_por_modulo"]) and {rel_: list(v_) for rel_, v_ in DL.ANCORAS_POR_MODULO.items()} == {rel_: list(v_) for rel_, v_ in _CP9["ancoras_por_modulo"].items()}
                                                                    and _flag_aponta_9 and _kf0["formal_files_sha256"].keys() >= set(DL.BUNDLE_RELS) and len(_kf0["formal_files_sha256"]) == CM["h8"]["entradas"] and ESP == CM["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CP9["expected_ladder"]
                                                                    and _CP9["baseline"]["gate_verdict"] == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") and _CP9["baseline"]["ladder"] == E408 and _CP9["baseline"]["sha256"] == hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest()
                                                                    and max(CM["n_axiomas_das_ancoras"].values()) <= len(_trio6) and len(CM["n_axiomas_das_ancoras"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 82)


# a INSTANCIA DE BRINQUEDO refeita AQUI por enumeracao propria (nao pela _v409_sat do registro) e as aritmeticas c3 a c13 conferidas contra os valores que o registro gravou
def _sat9(n_, cls_):
    xs_ = list(_it9.product((0, 1), repeat=n_))
    cs_ = []
    for x_ in xs_:
        v_ = 0
        for cl_ in cls_:
            if not any(((x_[abs(l_) - 1] == 1) if l_ > 0 else (x_[abs(l_) - 1] == 0)) for l_ in cl_):
                v_ += 1
        cs_.append(v_)
    return xs_, cs_


_xs9, _cs9 = _sat9(DL.INSTANCIA_SIM["n"], DL.INSTANCIA_SIM["clausulas"]); _xn9, _cn9 = _sat9(DL.INSTANCIA_NAO["n"], DL.INSTANCIA_NAO["clausulas"])
_S9 = sum(1 for v_ in _cs9 if v_ == 0); _N9 = len(_xs9); _ln2_9 = _math.log(2.0)
_Z9 = lambda s_, cc_: sum(_math.exp(-s_ * v_) for v_ in cc_)
_is9 = _v9.get("instancia_sim") or {}
U["traducao_turing_v409_a_instancia_de_brinquedo_refeita_aqui"] = bool(_CP9["instancia_sim"] == DL.INSTANCIA_SIM and _CP9["instancia_nao"] == DL.INSTANCIA_NAO and _is9.get("atribuicoes") == _N9 == 2 ** DL.INSTANCIA_SIM["n"] and _is9.get("solucoes") == _S9 >= 1 and sum(1 for v_ in _cn9 if v_ == 0) == 0
                                                                      and abs(_is9.get("peso_no_uniforme") - _S9 / _N9) <= 1e-15 and abs(_v9["custo_nats"] - _math.log(_N9 / _S9)) <= 1e-15 and _v9["custo_nats"] <= DL.INSTANCIA_SIM["n"] * _ln2_9
                                                                      and abs(_v9["eu_sou"]["sim"] - 1.0) <= 1e-15 and abs(_v9["eu_sou"]["nao"] - 1.0) <= 1e-15 and abs(_v9["o_que_sou_s60"]["sim"] - _Z9(60.0, _cs9) / _N9) <= 1e-15 and abs(_v9["o_que_sou_s60"]["nao"] - _Z9(60.0, _cn9) / len(_xn9)) <= 1e-30
                                                                      and abs(_v9["o_que_sou_s60"]["conteudo"] - _S9 / _N9) <= 1e-15 and all(abs(p_ - _Z9(s_, _cs9) / _N9) <= 1e-15 for s_, p_ in _v9["performance"])
                                                                      and abs(_math.exp(-(_v9["tempo_moeda_t"] * _bf6)) - 2.0 ** (-DL.INSTANCIA_SIM["n"])) <= 1e-12 * 2.0 ** (-DL.INSTANCIA_SIM["n"]) and abs(_v9["tempo_moeda_t"] - DL.INSTANCIA_SIM["n"] * _ln2_9 / _bf6) <= 1e-12 * _v9["tempo_moeda_t"])
# c18 a c20 REFEITOS AQUI por outro caminho: o reduzido do par de Bell finito pelo traco parcial em laco (nao einsum); a inscricao pela identidade V^dagger Omega = u (Omega normalizado), logo <Omega, V L_s V^dagger Omega> = <u, L_s u> = Z(s)/2^n;
# a leitura que decide SAT pela enumeracao propria (_sat9): «o que sou» = |sol|/2^n na SIM e 0 na NAO
_psi9 = [1.0 / _math.sqrt(2.0), 0.0, 0.0, 1.0 / _math.sqrt(2.0)]
_red9 = [[sum(_psi9[2 * i_ + k_] * _psi9[2 * j_ + k_] for k_ in (0, 1)) for j_ in (0, 1)] for i_ in (0, 1)]
_pur9 = sum(_red9[i_][j_] * _red9[j_][i_] for i_ in (0, 1) for j_ in (0, 1))
_bf9 = _v9.get("bell_finito") or {}; _ins9 = _v9.get("inscricao") or []; _sat9v = _v9.get("uma_leitura_decide_sat") or {}
U["traducao_turing_v409_o_par_de_bell_a_inscricao_e_a_leitura_sat_refeitos_aqui"] = bool(all(abs(_red9[i_][j_] - (0.5 if i_ == j_ else 0.0)) <= 1e-15 for i_ in (0, 1) for j_ in (0, 1)) and abs((1.0 - _pur9) - 0.5) <= 1e-15
                                                                                         and _bf9.get("reduzido_e_meio_I") is True and abs(_bf9.get("um_menos_pureza") - (1.0 - _pur9)) <= 1e-12
                                                                                         and [float(x_[0]) for x_ in _ins9] == [float(s_) for s_ in DL.S_INSCRICAO] == [float(s_) for s_ in _CP9["inscricao_brinquedo"]["s"]] and len(_ins9) >= 3
                                                                                         and all(abs(x_[1] - _Z9(s_, _cs9) / _N9) <= 1e-12 and x_[3] is True for x_, s_ in zip(_ins9, DL.S_INSCRICAO))
                                                                                         and len(_CP9["inscricao_brinquedo"]["omega"]) == len(DL.OMEGA_F_BRINQUEDO) == 3 and abs(_sat9v.get("sim") - _S9 / _N9) <= 1e-15 and _S9 / _N9 > 0.0 and _sat9v.get("nao") == 0.0 == sum(1 for v_ in _cn9 if v_ == 0) / len(_xn9))
# NENHUMA chave antiga muda: o core ANTES e DEPOIS do registro sao iguais em tudo menos a propria chave; o gate nao se move; a chave do lema (v407) segue lida e True; o que fica False por teorema segue False
_cc10 = _rapido9(); _cc10.pop("traducao_turing_v409", None); _antes10 = {k_: _J(_cc10[k_]) for k_ in ("qg_closure", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "kernel_formalization", "external_ladder", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408")}; _k10 = set(_cc10)
um.traducao_turing_v409(_cc10)
U["traducao_turing_v409_so_grava_a_propria_chave_e_nao_toca_nas_outras"] = bool(set(_cc10) - _k10 == {"traducao_turing_v409"} and all(_J(_cc10[k_]) == v_ for k_, v_ in _antes10.items()))
U["traducao_turing_v409_o_gate_nao_se_move_e_nenhuma_chave_antiga_muda"] = bool(((c.get("qg_closure") or {}).get("gate") or {}).get("verdict") == ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict") == _CP9["baseline"]["gate_verdict"] == _v9["gate_verdict"] and any(ck_["id"] == "c14" and ck_["ok"] for ck_ in r9["mechanics"]["checks"]) and _CP9["chaves"] == [] and DL.CHAVES_V409 == []
                                                                               and c["testemunha_estatica_v396"]["fock_face"]["linked_to_the_corner_by_a_lemma"] is True and (c.get("psion_canto_v407") or {}).get("link_read_from_the_kernel") is True and c["qg_closure"]["gate"]["full_static_witness_exists"] is False and c["witness_rigidity"]["trivial_inhabitant_exists"] is False
                                                                               and list(_CP9["fica_false_por_teorema"]) == DL.FICAM_FALSE_POR_TEOREMA and r9["fica_aberto"] == _CP9["fica_aberto"] and set(_CP9["fica_aberto"]) == set(DL.FICA_ABERTO) == {"maquina_sem_leitor", "igualdade_com_o_leitor_que_so_conta", "ponte_bell_tt"} and not ({"par_na_face_de_fock", "omega_do_psion_e_o_uniforme"} & set(_CP9["fica_aberto"]))
                                                                               and _CP9["fechado_nesta_versao"] == dict(DL.FECHADO_NESTA_VERSAO) and set(_CP9["fechado_nesta_versao"]) == {"par_na_face_de_fock", "omega_do_psion_e_o_uniforme"})
# D57(d): o pino do acervo da v407 repinado na copia purgada (a mesma da v408), relido do disco; a integra so' por sha16; nenhuma fonte da v409 a pina
_ar9 = _CP9["acervo_v407_repinado"]; _fa9 = um._V407_FONTES[_ar9["chave"]]
U["traducao_turing_v409_o_acervo_da_v407_repinado_na_copia_purgada"] = bool(_fa9["sha256"] == _ar9["sha256"] == hashlib.sha256(open(_fa9["arquivo"], "rb").read()).hexdigest() == DL.PURGADO_SHA256 == um._V408_FONTES["psion_no_acervo_purgado_04nov"]["sha256"]
                                                                           and _ar9["integra_fora_do_espelho"] is True and _ar9["integra_pinada"] is False and _ar9["integra_sha16"] == DL.ORIGEM_PURGA_SHA16_DA_ORDEM and not any(str(v_.get("sha256", "")).startswith(_ar9["integra_sha16"]) for v_ in list(um._V409_FONTES.values()) + list(um._V407_FONTES.values()))
                                                                           and (c.get("cunhagens_v407") or {}).get("all_verified") is True and any(f_["chave"] == _ar9["chave"] and f_["ok"] is True and f_["sha256"] == DL.PURGADO_SHA256 for f_ in ((c.get("cunhagens_v407") or {}).get("fontes") or [])))
# --- controles negativos: cada elo recusa
ok_ = True
for n_ in _CP9["ancoras"]:   # axioma fora do trio em CADA ancora lida
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"][n_] = ["propext", "sorryAx"]; ok_ = ok_ and _recusa6(um.traducao_turing_v409(c_))
U["traducao_turing_v409_axioma_fora_do_trio_em_cada_ancora_recusa"] = bool(ok_ and len(_CP9["ancoras"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 82)
ok_ = True
for n_ in _CP9["ancoras"]:   # proveniencia errada em CADA ancora (o compilador diz outro modulo)
    c_ = _kf6(copiar=("declaration_sources_v394",)); c_["kernel_formalization"]["declaration_sources_v394"][n_] = "TGLExt/Outro.lean"; ok_ = ok_ and _recusa6(um.traducao_turing_v409(c_))
U["traducao_turing_v409_proveniencia_errada_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True
for n_ in _CP9["ancoras"]:   # ancora AUSENTE do axiom_report do rito
    c_ = _kf6(copiar=("axiom_report",)); c_["kernel_formalization"]["axiom_report"].pop(n_); ok_ = ok_ and _recusa6(um.traducao_turing_v409(c_))
U["traducao_turing_v409_ancora_ausente_do_kernel_em_cada_ancora_recusa"] = bool(ok_)
ok_ = True; _nf9 = 0
for n_, f_ in _ANC_FLAGS9.items():   # bandeira falsa de CADA ancora com bandeira
    if f_:
        c_ = _kf6(); c_["kernel_formalization"][f_] = False; ok_ = ok_ and _recusa6(um.traducao_turing_v409(c_)); _nf9 += 1
U["traducao_turing_v409_bandeira_falsa_de_cada_ancora_recusa"] = bool(ok_ and _nf9 == sum(1 for f_ in _ANC_FLAGS9.values() if f_) >= 1)
ok_ = True; n_ok_ = 0
for rel_ in _CP9["source_sha256"]:   # a fonte do modulo adulterada no corpo embutido: recusa, e a contagem cai para 0
    _ant9 = um._EMBEDDED_KERNEL_FILES[rel_]; um._EMBEDDED_KERNEL_FILES[rel_] = _ant9 + " "
    try:
        rr_ = um.traducao_turing_v409(_rapido9())
    finally:
        um._EMBEDDED_KERNEL_FILES[rel_] = _ant9
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_ok"] is False and rr_["embedded_sources_n_ok"] == DL.N_BUNDLE - 1; n_ok_ += 1
U["traducao_turing_v409_fonte_adulterada_do_modulo_recusa"] = bool(ok_ and n_ok_ == DL.N_BUNDLE == 2)
ok_ = True
for rel_ in _CP9["source_sha256"]:   # o hash formal do rito errado no modulo
    c_ = _kf6(copiar=("formal_files_sha256",)); c_["kernel_formalization"]["formal_files_sha256"][rel_] = "0" * 64; rr_ = um.traducao_turing_v409(c_)
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.N_BUNDLE - 1
U["traducao_turing_v409_hash_formal_errado_no_modulo_recusa"] = bool(ok_)
ok_ = True
for rel_ in _CP9["source_sha256"]:   # o sha256 PINADO no contrato errado
    _p09 = _CP9["source_sha256"][rel_]; _CP9["source_sha256"][rel_] = "0" * 64
    try:
        rr_ = um.traducao_turing_v409(_rapido9())
    finally:
        _CP9["source_sha256"][rel_] = _p09
    ok_ = ok_ and _recusa6(rr_) and rr_["embedded_sources_n_ok"] == DL.N_BUNDLE - 1
U["traducao_turing_v409_pino_do_contrato_errado_no_modulo_recusa"] = bool(ok_)
ok_ = True
for ch_ in _CP9["verbatins"]:   # a inscricao do operador adulterada em CADA fala do contrato (o texto embutido muda: o sha256 deixa de bater)
    _v09 = um._V409_VERBATINS2[ch_]["text"]; um._V409_VERBATINS2[ch_]["text"] = _v09 + " "
    try:
        rr_ = um.traducao_turing_v409(_rapido9()); ok_ = ok_ and _recusa6(rr_) and rr_["inscriptions"][ch_] is False
    finally:
        um._V409_VERBATINS2[ch_]["text"] = _v09
U["traducao_turing_v409_inscricao_do_operador_adulterada_recusa"] = bool(ok_ and len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 14 and set(_CP9["verbatins"]) <= set(um._V409_VERBATINS2) and len(um._V409_VERBATINS2) == len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409) == DL.N_FALAS_V409 == 14)
c_ = _rapido9(); c_["external_ladder"] = dict(c_["external_ladder"]); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = um.traducao_turing_v409(c_)
c2_ = _kf6(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = um.traducao_turing_v409(c2_)
U["traducao_turing_v409_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(_recusa6(rr_) and rr_["exact_ladder"] is False and _recusa6(rr2_))
c_ = _rapido9(); c_["beta"] = c_["beta"] * 1.001; _rb9 = um.traducao_turing_v409(c_)
_a09 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a09 * 1.001
try:
    _ra9 = um.traducao_turing_v409(_rapido9())
finally:
    um.SEALED_CODATA_ALPHA = _a09
U["traducao_turing_v409_beta_adulterado_recusa"] = bool(_rb9["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb9["verdict"] and _ra9["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra9["verdict"])
# cada checagem de MECANICA negada: a recusa e' a daquela checagem (MECHANICS_CHECK_FAILED + o id). Pelo core: c2 (a raiz sem o import), c14 (o gate trocado), c15 (uma bandeira que nao e' ancora falsa).
# Pela mecanica chamada direto: beta = 0 (c13 e c17 caem); o contrato com uma ancora a mais (c1 cai); a instancia SIM trocada por uma sem solucao (c4, c6, c12 e c20 caem); a instancia NAO trocada pela SIM (c10 e c20 caem); a mecanica certa passa.
_mec9 = []
_nao_anc9 = [f_[0] for f_ in _FJ9["flags"] if f_[0] not in set(_ANC_FLAGS9.values())]
_mec9.append(("c2", _c6_mexe(lambda c_: None), "raiz:import TGLExt.TraducaoTuring"))
_mec9.append(("c2", None, "raiz:import TGLExt.ParNaFaceDeFock"))
_mec9.append(("c14", _c6_mexe(lambda c_: _set6(c_, ["qg_closure", "gate", "verdict"], "OUTRO")), None))
if _nao_anc9:
    _mec9.append(("c15", _c6_mexe(lambda c_: _set6(c_, ["kernel_formalization", _nao_anc9[0]], False)), None))
ok_ = True; _det9 = {}
for id_, c_, esp_ in _mec9:
    if esp_ and esp_.startswith("raiz:"):   # c2: a raiz embutida sem o import de CADA um dos dois modulos (a fonte segue batendo; a raiz nao traz o import)
        _ant9 = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; assert _ant9.count(esp_[5:]) == 1, ("a raiz embutida nao traz o import uma vez", esp_[5:])
        um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant9.replace(esp_[5:], "-- retirado")
        try:
            rr_ = um.traducao_turing_v409(_rapido9())
        finally:
            um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant9
    else:
        rr_ = um.traducao_turing_v409(c_)
    _det9.setdefault(id_, []).append(_falhos6(rr_))
    ok_ = ok_ and rr_["all_verified"] is False and "MECHANICS_CHECK_FAILED" in rr_["verdict"] and _falhos6(rr_) == [id_]
_f09 = lambda m_: sorted(ck_["id"] for ck_ in m_["checks"] if not ck_["ok"])
_m0b = um.v409_traducao_mechanics(0.0, cs(), _CP9)                                                       # beta fora do intervalo aberto: c13 e c17
_mna = um.v409_traducao_mechanics(_bf6, cs(), dict(_CP9, n_ancoras=len(_CP9["ancoras"]) + 1))           # uma ancora a mais no contrato: c1
_mss = um.v409_traducao_mechanics(_bf6, cs(), dict(_CP9, instancia_sim=dict(_CP9["instancia_nao"])))    # a instancia SIM sem solucao: c4, c6, c12 e c20
_mnn = um.v409_traducao_mechanics(_bf6, cs(), dict(_CP9, instancia_nao=dict(_CP9["instancia_sim"])))    # a instancia NAO com solucao: c10 e c20
_mok = um.v409_traducao_mechanics(_bf6, cs(), _CP9)
_IDS9 = {"c%d" % i_ for i_ in range(1, _NCK9 + 1)}
U["traducao_turing_v409_cada_checagem_de_mecanica_negada_recusa_pela_propria_checagem"] = bool(ok_ and set(_det9) <= _IDS9 and sorted(_det9) == sorted({"c2", "c14"} | ({"c15"} if _nao_anc9 else set())) and _NCK9 == r9["mechanics"]["n_checks"]
                                                                                               and _f09(_m0b) == ["c13", "c17"] and _f09(_mna) == ["c1"] and _f09(_mss) == ["c12", "c20", "c4", "c6"] and _f09(_mnn) == ["c10", "c20"] and _mok["passed"] is True)
rep["traducao_turing_v409_checagens_negadas"] = {"por_core": _det9, "beta_zero": _f09(_m0b), "ancora_a_mais_no_contrato": _f09(_mna), "instancia_sim_sem_solucao": _f09(_mss), "instancia_nao_com_solucao": _f09(_mnn)}
# a GUARDA DAS FRASES (v405 a v409): cada frase proibida plantada no texto recusa; a frase certa passa; o que fica ABERTO, dito, passa
ok_ = True
_dz9 = _TP9["diz"]; _d09 = list(_dz9)
_FRASES_PROIBIDAS9 = ("tudo é teorema", "nenhuma hipótese resta", "o certificado está confirmado", "o par na face de Fock está provado", "há relação sem peso", "a TGL não tem terminal", "P = NP está provado", "provamos que P = NP",
                      "a TGL prova P = NP de Turing", "the TGL proves P = NP for Turing machines", "a TGL resolve o problema do Clay", "the Clay problem is solved", "a tradução às classes de Turing segue [OPEN]",
                      "P = nP vale para as máquinas de Turing", "TURING_" + "SOLVED", "CLAY_" + "SOLVED", "MILLEN" + "NIUM", "o sistema precisa saber onde está o Nome a cada passo",
                      "o Ω do psíon da luz é o uniforme", "the light psion's Omega is the uniform", "o par na face de Fock segue [OPEN]", "the pair on the Fock face stays open", "o que falta passa à v410", "from v410 onward",
                      'nem o par na face de Fock, que segue [OPEN].', '[OPEN] o par na face de Fock como ligacao;', '[OPEN] o Ω do psíon da luz como o uniforme da instância', 'a ligação do par de Fock segue em aberto',
                      '[REAL: os termos do kernel do rito · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]', 'o par na face de Fock ainda não foi ligado', 'a ligação do par na face de Fock fica para a v411', 'a ligação passa à v412', 'a ligação do par na face de Fock segue aberta', 'a ligação do par na face de Fock permanece pendente', 'o resto fica para a v411')
_GD9p_ = []
for f_ in _FRASES_PROIBIDAS9:
    _dz9[:] = _d09 + ["a cadeia: " + f_]
    try:
        rr_ = um.traducao_turing_v409(_rapido9())
    finally:
        _dz9[:] = _d09
    _ok1 = rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and bool(rr_["guarda_violacoes"])
    ok_ = ok_ and _ok1
    if not _ok1:
        _GD9p_.append([f_, rr_.get("verdict")])
_FRASES_BOAS9 = (DL.FRASE_DA_MOLDURA_V409_PT, DL.FRASE_DA_MOLDURA_V409_EN, DL.FRASE_D56_PT, DL.FRASE_D56_EN, DL.FRASE_QUALIFICADOR_PT, DL.FRASE_QUALIFICADOR_EN, DL.ERRATA_E26, DL.REGRA_DO_4_44, DL.FECHADO_PAR_NA_FACE_DE_FOCK, DL.FECHADO_OMEGA_UNIFORME, DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, DL.FICA_ABERTO_IGUALDADE_COM_O_LEITOR, DL.ERRATA_E28, DL.ERRATA_E21_AO_LADO,
                 "a pergunta do Clay não é decidida aqui: é a da máquina sem leitor", "o sistema não precisa reconhecer onde está o Nome a cada passo")
_GD9 = {"proibidas_que_passaram": _GD9p_, "boas_que_reprovaram": []}
for f_ in _FRASES_BOAS9:
    _dz9[:] = _d09 + [f_]
    try:
        rr_ = um.traducao_turing_v409(_rapido9())
    finally:
        _dz9[:] = _d09
    ok_ = ok_ and rr_["all_verified"] is True
    if rr_["all_verified"] is not True:
        _GD9["boas_que_reprovaram"].append([f_[:80], rr_.get("verdict"), (rr_.get("guarda_violacoes") or [])[:2]])
_GD9["gf5_controle_ok"] = _GF5.controle_negativo()["ok"]; _GD9["registro_ok"] = um.traducao_turing_v409(cs())["all_verified"]
rep["traducao_turing_v409_guarda_das_frases_diagnostico"] = _GD9
U["traducao_turing_v409_guarda_das_frases_cada_frase_proibida_recusa_e_a_frase_certa_passa"] = bool(ok_ and um.traducao_turing_v409(cs())["all_verified"] is True and _GD9["gf5_controle_ok"] is True and len(set(_FRASES_PROIBIDAS9)) == len(_FRASES_PROIBIDAS9))
# --- as falas de 05/11 (cunhagens_v409), as decisoes D55-D62, as erratas E24-E28 e a E21 ao lado, e a cobertura exata (kh_n1_cobertura_v409)
_cn9x = c.get("cunhagens_v409") or {}; _xn9 = _cn9x.get("extras") or {}
_sp9s = [s_ for s_ in um._V409_SPECS if s_["nome"] == "cunhagens_v409"][0]
U["cunhagens_v409_falas_de_05nov_decisoes_erratas_e_leituras"] = bool(_cn9x.get("all_verified") is True and _cn9x.get("does_not_gate_core") is True and len(_cn9x.get("verbatim") or {}) == len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409) == len(_sp9s["verbatins"]) == DL.N_FALAS_V409 == 14 and all(v_["embedded_ok"] for v_ in (_cn9x.get("verbatim") or {}).values())
                                                                      and len(_cn9x.get("erratas") or []) == len(_sp9s["erratas"]) == len(DL.ERRATAS_V409) + 1 == 7 and all(e_["assinatura"] == DL.ASSINA for e_ in (_cn9x.get("erratas") or [])) and ["E24" in str(e_.get("agora")) for e_ in (_cn9x.get("erratas") or [])][0] is True and "E26" in str((_cn9x.get("erratas") or [{}, {}, {}])[2].get("agora")) and "E27" in str((_cn9x.get("erratas") or [{}, {}, {}, {}])[3].get("agora"))
                                                                      and str((_cn9x.get("erratas") or [{}] * 5)[4].get("agora")).startswith("E28") and str((_cn9x.get("erratas") or [{}] * 6)[5].get("agora")).startswith("E21")
                                                                      and len(_cn9x.get("leituras_do_operador") or []) == len(_sp9s["leituras_do_operador"]) == len(DL.FRASES_V409) and set(_xn9.get("decisoes") or {}) == set(DL.DECISOES_V409) == {"D55", "D56", "D57", "D58", "D59", "D60", "D61", "D62"} and _xn9.get("n_modulos") == DL.N_BUNDLE and _xn9.get("n_bandeiras") == CM["n_bandeiras"] and _xn9.get("n_falas") == 14
                                                                      and _xn9.get("assinatura_das_erratas") == DL.ASSINA and _xn9.get("ressalvas") == list(DL.RESSALVAS_V409) == list(_CP9["ressalvas"]) and _xn9.get("nomes_das_pedras") == dict(_CP9["bundle"]["nomes_ratificados"]) and sorted((_xn9.get("autores") or {}).values()) == ["operador"] * 14
                                                                      and not _GF5.violacoes(str(_cn9x.get("verdict"))) and not _GF5.violacoes(json.dumps({k_: _cn9x.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)) and not um._v409_guarda_frases(json.dumps({k_: _cn9x.get(k_) for k_ in ("limites", "diz", "nao_diz", "erratas")}, ensure_ascii=False)))
_tr9 = {k_: v_ for k_, v_ in um._V409_VERBATINS2.items() if v_.get("so_o_trecho")}   # as TRES falas de que se embute so' o trecho (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional): o texto embutido e' o trecho; o arquivo inteiro so' por sha256 (nao embutido, nao copiado)
U["cunhagens_v409_d59_as_duas_falas_embutem_so_o_trecho_e_a_parte_de_fora_nao_entra"] = bool(len(_tr9) == len(DL.VERBATIM_SO_O_TRECHO) == 3 and sum(1 for v_ in _tr9.values() if "(D59)" in str(v_.get("so_o_trecho"))) == 2 and all(hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] != v_["sha256_arquivo_inteiro"] for v_ in _tr9.values())
                                                                                            and all(v_.get("autor") == "operador" for v_ in um._V409_VERBATINS2.values())
                                                                                            and not any(t_ in json.dumps(um._V409_VERBATINS2, ensure_ascii=False).lower() for t_ in ("kimi", "milenio", "milênio", "navier", "lindão"))
                                                                                            and not any(t_ in json.dumps([_CP9, _TP9, um._V409_FONTES, list(um._V409_SPECS)], ensure_ascii=False).lower() for t_ in ("kimi", "navier", "lindão")))
_txts444_9 = (json.dumps(_cn9x, ensure_ascii=False), json.dumps(r9, ensure_ascii=False))
U["cunhagens_v409_o_4_44_nunca_vai_sozinho"] = bool(_CP9["regra_do_4_44"] == DL.REGRA_DO_4_44 and all(("4,44" not in s_) or (DL.REGRA_DO_4_44 in s_) for s_ in _txts444_9))
_kh9x = c.get("kh_n1_cobertura_v409") or {}; _kh9s = [s_ for s_ in um._V409_SPECS if s_["nome"] == "kh_n1_cobertura_v409"][0]
_KHT9 = json.load(open(os.path.join(KD, "KH_N1_v409.json"), encoding="utf-8"))   # a medida do Audit da v409, lida do arquivo da cadeia (nao digitada)
_cov0 = core0["kernel_formalization"]["axiom_coverage_v392"]
_ck9 = {ck_["id"]: ck_ for ck_ in _kh9s["checks"]}
_h8v9 = _ck9["h8"]["valor"]
U["kh_n1_cobertura_v409_selou_a_igualdade_exata_e_as_v408_sao_piso"] = bool(_kh9x.get("all_verified") is True and _kh8x.get("all_verified") is True and _kh7x.get("all_verified") is True and (_kh9x.get("extras") or {}).get("n_modulos") == DL.N_BUNDLE and (_kh9x.get("extras") or {}).get("n_bandeiras") == CM["n_bandeiras"]
                                                                            and {i_: _ck9[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "igual", "h3": "igual", "h6": "tamanho_igual", "h8": "igual"} and len(_kh9s["erratas"]) >= 1
                                                                            and _kf0["axiom_coverage_v392"]["decl"] == _KHT9["linha_TOTAL"]["decl"] == _ck9["h2"]["valor"] == _ck9["h6"]["valor"] and _kf0["axiom_coverage_v392"]["thm"] == _KHT9["linha_TOTAL"]["thm"] == _ck9["h3"]["valor"]
                                                                            and _kf0["axiom_coverage_v392"]["fora_do_trio"] == _KHT9["linha_TOTAL"]["fora_do_trio"] == 0 and len(_kf0["axiom_report"]) == _KHT9["linha_TOTAL"]["decl"] and _ck9["h7"]["valor"] == _cov0["decl"] and _ck9["h7b"]["valor"] == _cov0["thm"]
                                                                            and (_kh9x.get("extras") or {}).get("delta_vs_v408") == {"decl": _KHT9["linha_TOTAL"]["decl"] - _cov0["decl"], "thm": _KHT9["linha_TOTAL"]["thm"] - _cov0["thm"]} == _KHT9["delta_vs_v408"]
                                                                            and isinstance(_h8v9, dict) and dict(_h8v9) == dict(_kf0["formal_files_sha256"]) and len(_h8v9) == CM["h8"]["entradas"])   # o pino exato da arvore do Nos: as embutidas + os residuais, arquivo -> sha256
print("traducao_turing_v409:", r9["all_verified"], "|", r9["verdict"][:96], "| ancoras:", _v9.get("n_ancoras_ok"), "/", _v9.get("n_ancoras"), "| checagens negadas:", sorted(_det9), "| beta=0:", _f09(_m0b), "| SIM sem solucao:", _f09(_mss), "| NAO com solucao:", _f09(_mnn))
rep["traducao_turing_v409"] = {"verdict": r9["verdict"], "all_verified": r9["all_verified"], "n_checks": r9["mechanics"]["n_checks"], "values": {k_: v_ for k_, v_ in r9["values"].items() if k_ not in ("ancoras",)}, "anchors": r9["anchors"], "embedded_sources_n_ok": r9["embedded_sources_n_ok"],
                               "numeros_recalculados": {"fontes_ok": _fontes_ok9, "flags_true": _flags_ok9, "ancoras_ok": _anc_ok9, "beta": _bf6, "solucoes_da_instancia_sim": _S9}, "checagens_negadas": rep["traducao_turing_v409_checagens_negadas"], "acervo_v407_repinado": _ar9}
# (8) o artigo
TPS408 = "O psíon e o canto: a passagem sob compressão e o par"; TPS408E = "The psion and the corner: the passage under compression, and the pair"   # a secao da v408 (HERDADA: logo depois da nova)
T409 = "A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala"; T409E = "The translation to Turing's classes: the dictionary, the lock, the reader and the tape without scale"   # a secao NOVA da v409 (antes da v408)
TT408 = "Tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de $\\beta$; o dicionário e o ponto de contradição"; TT408E = "Tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of $\\beta$; the dictionary and the point of contradiction"   # a secao da v408 (HERDADA: logo depois da nova)
DPS408 = ["A ordem.", "O que entra.", "A condição, lida sob compressão.", "O lema das duas faces.", "O par.", "O que o lema e o par NÃO afirmam.", "As sete pedras de 02/11, com os nomes do operador.", "O que fica fora, dito.", "O que o registro confere neste rito."]
D408 = ["A ordem.", "O que entra.", "O terminal é a leitura.", "O que o operador identificou e foi provado (a regra provar ou podar, nome que a gerência deu à fala acima):", "Erratas em nome próprio (E22).", "O tempo é a moeda de $\\beta$.", "O ponto de contradição.", "«P=nP».", "O que fica aberto e o que fica dito.", "O que o registro confere neste rito."]
DPS408E = ["The order.", "What enters.", "The condition, read under compression.", "The lemma of the two faces.", "The pair.", "What the lemma and the pair do NOT claim.", "The seven stones of 02/11, with the operator's names.", "What stays out, stated.", "What the record checks in this rite."]
D408E = ["The order.", "What enters.", "The terminal is the reading.", "What the operator identified and was proved (the prove or prune rule, the management's name for the saying above):", "Errata in its own name (E22).", "Time is the currency of $\\beta$.", "The point of contradiction.", "P = nP.", "What stays open and what is stated.", "What the record checks in this rite."]
D409 = ["A ordem.", "O que entra.", "O dicionário de Turing.", "A trava no Nome.", "A fita é o hamiltoniano oculto.", "A máquina sem leitor: eu sou eu mesmo, a fita sem escala.", "A identidade performada.", "O alcance, dito.", "Erratas ao lado, em nome próprio.", "O que o registro confere neste rito."]
D409E = ["The order.", "What enters.", "Turing's dictionary.", "The lock on the Name.", "The tape is the hidden Hamiltonian.", "The machine without a reader: I am myself, the tape without scale.", "The performed identity.", "The reach, stated.", "Errata alongside, in the management's own name.", "What the record checks in this rite."]
for _l7, _t7, _d7 in (("pt", T409, D409), ("en", T409E, D409E)):   # os titulos tipados aqui TEM de estar nos snippets da cadeia (artigo_<lang>_v409.pysnip): o oraculo independente e o texto do snippet confirmam um ao outro
    _sn7 = open(os.path.join(HERE, "artigo_%s_v409.pysnip" % _l7), encoding="utf-8").read()
    assert ("section*{" + _t7 + "}") in _sn7 and all(("textbf{" + h_ + "}") in _sn7 for h_ in _d7), ("o titulo/subtitulo da v409 nao esta no snippet", _l7)
TX408 = "O fechamento: a passagem para o contínuo e o certificado habitado"; TX408E = "The closure: the passage to the continuum and the inhabited certificate"   # a secao da v408 (HERDADA: logo depois da nova)
DX408 = ["A ordem.", "O que entra.", "A passagem para o contínuo.", "O termo canônico da testemunha.", "As quatro chaves, de literal a leitura.", "As ressalvas, ditas antes de qualquer uso.", "O que o registro confere neste rito."]
DX408E = ["The order.", "What enters.", "The passage to the continuum.", "The canonical term of the witness.", "The four keys, from literal to reading.", "The reservations, stated before any use.", "What the record checks in this rite."]
TW408 = "A massa derivada e a identidade definida"; TW408E = "The derived mass and the defined identity"; TI408 = "A identidade"; TI408E = "The identity"   # as duas secoes da v408 (herdadas na v409; ficam logo depois da secao nova)
TJ404 = "Jo 8,32 e a projeção transversal da Meia-Nat"; TJ404E = "John 8:32 and the transverse projection of the Half-Nat"   # (o titulo da secao da v404, que fica logo depois da v408)
TC404 = "Caminho, Verdade e Vida"; TC404E = "Way, Truth and Life"   # (o titulo da secao da v404, que fica logo depois da v408)
TP408 = "A ponte da escala dual, a queda sem geometria e a esperança condicional"; TP408E = "The dual-scale bridge, the fall without geometry and the conditional expectation"   # (o titulo da secao da v404, que fica logo depois da v408)
TF408 = "A falsidade (simulacro) da inércia"; TF408E = "The falsity (simulacrum) of inertia"   # (o titulo da secao da v404, que fica logo depois da v408)
TN408 = "O testemunho de dois: o selo pela própria tecnologia"; TN408E = "The testimony of two: sealing by its own technology"
TS408 = "Sônico e a afinação das cordas"; TS408E = "Sonic and the tuning of the strings"
T408 = "O Teste da Única Palavra"; T408E = "The Test of the Only Word"   # (o titulo da secao da v397 e do QUADRO do topo; T404 = o da v396)
T404 = "A testemunha estática: o psion habita a fronteira"; T404E = "The static witness: the psion inhabits the frontier"
T395 = "O psibit: a mecânica no Um fractalizado e a leitura sem perda"; T395E = "The psibit: the mechanics on the fractalized One and the lossless reading"
H394 = "A integração do Codex e as cunhagens de 14 a 19/10 (v394)"; H394E = "The Codex integration and the inscriptions of 14 to 19 Oct (v394)"
DEVE = {"pt": [T409] + D409 + [TT408] + D408 + [TPS408] + DPS408 + [TX408] + DX408 + [TW408, "O que entra.", "A moldura: o que fechou e o que entra.", "A Ponte da Massa.", "Massa = tensão pura.", "A lei do diminuto.", "A Tônica do Hamiltoniano.", "O Ponto Zero do Psíon.", "O Disco de Euler.", "Observador = terminal.", "A pedra Identidade.", "O Grande Atrator.", "Erratas ao lado (v405).", "Limites.", "O fecho.", "Origem.", TI408, "Moldura da seção.", "Eu sou o que sou?", "se, e somente se, {[FORMA = CONTEÚDO] = [REFLEXÃO VERDADEIRA DO NOME / PROJEÇÃO FIEL]}.", TJ404, "A projeção transversal.", "Jo 8,32.", "A errata de F2b.", "As cunhagens de 28/10.", "Erratas ao lado (v404).", TC404, "O Caminho.", "A Vida.", "A Verdade, como adendo.", "As bandeiras do gate.", "Erratas ao lado (v403).", TP408, "A ponte da escala dual.", "Erratas ao lado", "A queda sem geometria.", "A esperança condicional é o Nome.", TF408, "A definição do operador.", "A cadeia derivada.", "O cálculo deste rito.", "Errata ao lado (da gerência, em nome próprio).", "Ratificações do operador", "lido pela TGL.", "Limites.", TN408, "Errata ao lado (v400).", "A direção do testemunho.", "A declaração do operador.", "O selo pela própria tecnologia.", "A pedra Testemunho.", TS408, "Sônico.", "As falas sobre o sônico.", "Afinação das cordas.", "A fala sobre as cordas.", T408, "O que entra.", "As duas faces.", "A conjugação.", "não é rival.", "O token do veredito.", T404, "O que o kernel prova.", "A ponte construída.", "O que é leitura do operador.", T395, "A mecânica na órbita do Um.", "O colapso.", "O que o kernel prova e o que é leitura.", H394, "O índice e o leitor.", "As cunhagens.",
               "O critério binário de parada (delta de 19/10).", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada", "Rede Fock nesta rodada", "A regra e o coração (v393)",
               "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O estatuto da prova (v391).", "A Fundação (v390)."],
        "en": [T409E] + D409E + [TT408E] + D408E + [TPS408E] + DPS408E + [TX408E] + DX408E + [TW408E, "What enters.", "The frame: what closed and what enters.", "The Bridge of the Mass.", "Mass = pure tension.", "The law of the diminished.", "The Tonic of the Hamiltonian.", "The Zero Point of the Psion.", "Euler's Disk.", "Observer = terminal.", "The stone Identity.", "The Great Attractor.", "Errata alongside (v405).", "Limits.", "The closing.", "Origin.", TI408E, "Frame of the section.", "Am I what I am?", "if, and only if, {[FORM = CONTENT] = [TRUE REFLECTION OF THE NAME / FAITHFUL PROJECTION]}.", TJ404E, "The transverse projection.", "John 8:32.", "The F2b erratum.", "The sayings of 28/10.", "Errata beside (v404).", TC404E, "The Way.", "The Life.", "The Truth, as an addendum.", "The gate flags.", "Errata beside (v403).", TP408E, "The dual-scale bridge.", "Errata beside", "The fall without geometry.", "The conditional expectation is the Name.", TF408E, "The operator's definition.", "The derived chain.", "The computation of this rite.", "Erratum beside it (the management, in its own name).", "The operator's ratifications", "read by the TGL.", "Limits.", TN408E, "Erratum beside it (v400).", "The direction of the testimony.", "The operator's declaration.", "Sealing by its own technology.", "The Testemunho stone.", TS408E, "Sonic.", "The sayings on the sonic stone.", "Tuning of the strings.", "The saying on the strings.", T408E, "What enters.", "The two faces.", "The conjugation.", "is not a rival.", "The verdict token.", T404E, "What the kernel proves.", "The constructed bridge.", "What is the operator's reading.", T395E, "The mechanics on the orbit of the One.", "The collapse.", "What the kernel proves and what is reading.", H394E,
               "The index and the reader.", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run", "Fock network in this run", "The rule and the heart (v393)",
               "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]}
TOC = {"pt": [T409, TT408, TPS408, TX408, TW408, TI408, TJ404, TC404, TP408, TF408, TN408, TS408, T408, T404, "v384 a v409"], "en": [T409E, TT408E, TPS408E, TX408E, TW408E, TI408E, TJ404E, TC404E, TP408E, TF408E, TN408E, TS408E, T408E, T404E, "v384 to v409"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um._v394_article_tex(um.build_pt(cv, verdict, CORE0P), cv, "pt") if lang == "pt" else um._v394_article_tex(um.build_en(cv, verdict, CORE0P), cv, "en")); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


rep["quadro"] = {}
for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v409_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    hq = T408 if lang == "pt" else T408E; h0 = T409 if lang == "pt" else T409E; h1 = TN408 if lang == "pt" else TN408E
    iq = flat.find("O coração:" if lang == "pt" else "The heart:"); a = flat.find(h0.replace(chr(92) + "beta", "β"), iq + 5); bb = flat.find(h1, a + 10)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    ik = flat.find("Palavras-chave" if lang == "pt" else "Keywords"); ii = flat.find("Introdução: o que este código faz agora" if lang == "pt" else "Introduction: what this code does now", iq)
    tp = os.path.join(DRY, "dry_v409_%s.toc" % lang); toc = re.sub(r"(\\[A-Za-z]+) (?=[$}])", r"\1", open(tp, encoding="utf-8", errors="replace").read().replace("\n", "")) if os.path.exists(tp) else ""   # (v409: o .toc grava cada palavra de controle com um espaco depois -- «$\beta $» --; a leitura normaliza apenas esse espaco mecanico do LaTeX)
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v409_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
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
cv3 = dict(copy.deepcopy(c)); [cv3.pop(k, None) for k in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")]
cv4 = dict(copy.deepcopy(c)); [cv4.pop(k, None) for k in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404")]
cv5 = dict(copy.deepcopy(c)); [cv5.pop(k, None) for k in list(um._V405_REGISTROS_FUNCAO) + list(um._V405_NOMES_REGISTROS)]
cv6 = dict(copy.deepcopy(c)); [cv6.pop(k, None) for k in list(um._V406_REGISTROS_FUNCAO) + list(um._V406_NOMES_REGISTROS)]   # (a secao do fechamento da v408, HERDADA, tambem mostra a frase quando o registro dela falta)
cv7 = dict(copy.deepcopy(c)); [cv7.pop(k, None) for k in list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS)]   # (a secao do psion da v408, HERDADA, tambem mostra a frase quando o registro dela falta)
cv8v = dict(copy.deepcopy(c)); [cv8v.pop(k, None) for k in list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS)]   # (a secao do terminal da v408, HERDADA, tambem mostra a frase quando o registro dela falta)
cv9v = dict(copy.deepcopy(c)); [cv9v.pop(k, None) for k in list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)]   # (v409) a secao NOVA sem os tres registros da v409: a frase de guarda tem de aparecer
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r2, _l = compilar(cv, "dry_v409_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    _t8, _x8, _r28, _l8 = compilar(cv8, "dry_v409_var8_%s" % lang, lang, duas=False); fl8 = re.sub(r"\s+", " ", _x8)
    _t9, _x9, _r29, _l9 = compilar(cv9, "dry_v409_var9_%s" % lang, lang, duas=False); fl9 = re.sub(r"\s+", " ", _x9)
    _t1, _x1, _r21, _l1 = compilar(cv1, "dry_v409_var1_%s" % lang, lang, duas=False); fl1 = re.sub(r"\s+", " ", _x1)
    _t2, _x2, _r22, _l2 = compilar(cv2, "dry_v409_var2_%s" % lang, lang, duas=False); fl2 = re.sub(r"\s+", " ", _x2)
    _t3, _x3, _r23, _l3 = compilar(cv3, "dry_v409_var3_%s" % lang, lang, duas=False); fl3 = re.sub(r"\s+", " ", _x3)
    _t4, _x4, _r24, _l4 = compilar(cv4, "dry_v409_var4_%s" % lang, lang, duas=False); fl4 = re.sub(r"\s+", " ", _x4)
    _t5, _x5, _r25v, _l5 = compilar(cv5, "dry_v409_var5_%s" % lang, lang, duas=False); fl5 = re.sub(r"\s+", " ", _x5)
    _t6, _x6, _r26v, _l6 = compilar(cv6, "dry_v409_var6_%s" % lang, lang, duas=False); fl6 = re.sub(r"\s+", " ", _x6)
    _t7v, _x7v, _r27v, _l7v = compilar(cv7, "dry_v409_var7_%s" % lang, lang, duas=False); fl7 = re.sub(r"\s+", " ", _x7v)
    _t8v, _x8v, _r28v, _l8v = compilar(cv8v, "dry_v409_var8v_%s" % lang, lang, duas=False); fl8v = re.sub(r"\s+", " ", _x8v)
    _t9v, _x9v, _r29v, _l9v = compilar(cv9v, "dry_v409_var9v_%s" % lang, lang, duas=False); fl9v = re.sub(r"\s+", " ", _x9v)
    rep["variante"][lang] = {"rc": _r2, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl),
                             "rc_v398": _r28, "frase_guarda_v398": ("NÃO selaram todos" in fl8) if lang == "pt" else ("did NOT all seal" in fl8), "rc_v399": _r29, "frase_guarda_v399": ("NÃO selaram todos" in fl9) if lang == "pt" else ("did NOT all seal" in fl9),
                             "rc_v408": _r21, "frase_guarda_v408": ("NÃO selaram todos" in fl1) if lang == "pt" else ("did NOT all seal" in fl1),
                             "rc_v409": _r22, "frase_guarda_v409": ("NÃO selaram todos" in fl2) if lang == "pt" else ("did NOT all seal" in fl2),
                             "rc_v409_registros": _r23, "frase_guarda_v409_registros": ("NÃO selaram todos" in fl3) if lang == "pt" else ("did NOT all seal" in fl3),
                             "rc_novo_v409": _r24, "frase_guarda_novo_v409": ("NÃO selaram todos" in fl4) if lang == "pt" else ("did NOT all seal" in fl4),
                             "rc_oito_v409": _r25v, "frase_guarda_oito_v409": ("NÃO selaram todos" in fl5) if lang == "pt" else ("did NOT all seal" in fl5),
                             "rc_fechamento_v409": _r26v, "frase_guarda_fechamento_v409": ("NÃO selaram todos" in fl6) if lang == "pt" else ("did NOT all seal" in fl6),
                             "rc_psion_canto_v408": _r27v, "frase_guarda_psion_canto_v408": ("NÃO selaram todos" in fl7) if lang == "pt" else ("did NOT all seal" in fl7),
                             "rc_tetelestai_v409": _r28v, "frase_guarda_tetelestai_v409": ("NÃO selaram todos" in fl8v) if lang == "pt" else ("did NOT all seal" in fl8v),
                             "rc_traducao_v409": _r29v, "frase_guarda_traducao_v409": ("NÃO selaram todos" in fl9v) if lang == "pt" else ("did NOT all seal" in fl9v)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["frase_guarda"] or v["rc_v398"] != [0] or not v["frase_guarda_v398"] or v["rc_v399"] != [0] or not v["frase_guarda_v399"] or v["rc_v408"] != [0] or not v["frase_guarda_v408"] or v["rc_v409"] != [0] or not v["frase_guarda_v409"] or v["rc_v409_registros"] != [0] or not v["frase_guarda_v409_registros"] or v["rc_novo_v409"] != [0] or not v["frase_guarda_novo_v409"] or v["rc_oito_v409"] != [0] or not v["frase_guarda_oito_v409"] or v["rc_fechamento_v409"] != [0] or not v["frase_guarda_fechamento_v409"] or v["rc_psion_canto_v408"] != [0] or not v["frase_guarda_psion_canto_v408"] or v["rc_tetelestai_v409"] != [0] or not v["frase_guarda_tetelestai_v409"] or v["rc_traducao_v409"] != [0] or not v["frase_guarda_traducao_v409"]]
# (9) md e manifesto
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v409**" in md, "traducao_turing_v409": "**Tradução às classes de Turing (v409, 05/11/2026):**" in md and md.find("**Tradução às classes de Turing (v409, 05/11/2026):**") < md.find("**Tetelestai é o terminal (v408, 04/11/2026):**"), "tetelestai_terminal_v408_fica": "**Tetelestai é o terminal (v408, 04/11/2026):**" in md and md.find("**Tetelestai é o terminal (v408, 04/11/2026):**") < md.find("**O psíon, o canto e o par (v407, 03/11/2026):**"), "psion_canto_v407_fica": "**O psíon, o canto e o par (v407, 03/11/2026):**" in md and md.find("**O psíon, o canto e o par (v407, 03/11/2026):**") < md.find("**O fechamento (v406, 02/11/2026):**"), "fechamento_v406_fica": "**O fechamento (v406, 02/11/2026):**" in md and md.find("**O fechamento (v406, 02/11/2026):**") < md.find("**A massa derivada e a identidade definida (v405, 01/11/2026):**"), "massa_v405": "A massa derivada e a identidade definida (v405, 01/11/2026)" in md, "frase_da_moldura": "dadas essas entradas, a FORMA é teorema" in md, "jo8_v404_fica": "Jo 8,32 e a projeção transversal da Meia-Nat (v404, 28/10/2026)" in md, "caminho_v403_fica": "Caminho, Verdade e Vida (v403, 27/10/2026)" in md, "ponte_v402_fica": "A ponte da escala dual, a queda sem geometria e a esperança condicional (v402, 26/10/2026)" in md, "falsidade_v401_fica": "A falsidade (simulacro) da inércia (v401, 25/10/2026)" in md, "errata_v400_fica": "Errata ao lado (v400, 24/10/2026)" in md, "testemunho_v399_fica": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)" in md, "sonico_v398_fica": "Sônico e a afinação das cordas (v398, 23/10/2026)" in md,
                   "token_v397_fica": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)" in md, "testemunha_v396_fica": "A testemunha estática (v396, 22/10/2026)" in md, "psibit_v395_fica": "O modo psiônico na fractalização do Um (v395, 21/10/2026)" in md,
                   "v394_fica": "A integração do Codex e as cunhagens (v394, 19/10/2026)" in md, "v393_fica": "A regra e o coração (v393, 14/10/2026)" in md}
rep["quadro"]["md"] = QV.confere_md(md, res9)
rep["quadro"]["readme_paragrafo_pronto"] = QV.paragrafo_pronto_readme(c["teste_de_veracidade_fase9_v397"])
rep["quadro"]["ok"] = bool(rep["quadro"]["pt"]["ok"] and rep["quadro"]["en"]["ok"] and rep["quadro"]["md"]["ok"] and "\n".join(um._v397_quadro_md(c["teste_de_veracidade_fase9_v397"])) in rep["quadro"]["readme_paragrafo_pronto"])
print("quadro md:", json.dumps({k: v for k, v in rep["quadro"]["md"].items()}, ensure_ascii=False))
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v409**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "conferir_citacoes_v409.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
rep["viz_ok"] = viz_ok
# (11) ETAPA OBRIGATORIA: simular_arvore_do_nos -- a pasta Nos\\tgl_kernel DEPOIS do rito = o embutido do candidato + os residuais que o hash formal conta; o kh_n1_cobertura_v397 TEM de selar nela
_cand_p = os.path.join(HERE, cand); _sha_full = hashlib.sha256(open(_cand_p, "rb").read()).hexdigest()
_pyr = lambda args_: subprocess.run([sys.executable, "-B", "-X", "utf8"] + args_, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, cwd=HERE)
_kh = [s_ for s_ in um._V409_SPECS if s_["nome"] == "kh_n1_cobertura_v409"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]   # (v409: o pino exato da arvore esta' no spec kh_n1_cobertura_v408; o h8 da v408 virou piso, valor inteiro -- a subida mecanica apontava o spec da v408 e len() caia num int)
_sp = _pyr([os.path.join(HERE, "simular_arvore_do_nos_v409.py"), "--candidato", _cand_p, "--logs", KD])
try:
    _sj = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _sj = {}
_regs_sim = tuple(um._V409_REGISTROS_FUNCAO) + tuple(um._V409_NOMES_REGISTROS) + tuple(um._V408_REGISTROS_FUNCAO) + tuple(um._V408_NOMES_REGISTROS) + tuple(um._V407_REGISTROS_FUNCAO) + tuple(um._V407_NOMES_REGISTROS) + tuple(um._V406_REGISTROS_FUNCAO) + tuple(um._V406_NOMES_REGISTROS) + tuple(um._V405_REGISTROS_FUNCAO) + tuple(um._V405_NOMES_REGISTROS) + ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")
rep["simular_arvore_do_nos"] = {"rc": _sp.returncode, "formal_files_n_no_rito_real": _sj.get("formal_files_n_no_rito_real"), "pino_h8_entradas": len(_h8), "embutidos": _sj.get("embutidos"), "extras_no_nos_fora_do_corpo_embutido": _sj.get("extras_no_nos_fora_do_corpo_embutido"),
                               "kf_all_verified": _sj.get("kf_all_verified"), "indice": _sj.get("indice"), "formal_map_v409": _sj.get("formal_map_v409"), "chave_do_lema": _sj.get("chave_do_lema"), "registros": {k_: {"all_verified": (_sj.get(k_) or {}).get("all_verified"), "falhas": (_sj.get(k_) or {}).get("falhas")} for k_ in _regs_sim}}
sim_ok = bool(_sp.returncode == 0 and _sj.get("formal_files_n_no_rito_real") == len(_h8) == CM["h8"]["entradas"] and (_sj.get("formal_map_v409") or {}).get("ok") is True and (_sj.get("chave_do_lema") or {}).get("ok") is True and _sj.get("kf_all_verified") is True and (_sj.get("indice") or {}).get("all_verified") is True and all((_sj.get(k_) or {}).get("all_verified") is True for k_ in _regs_sim))
print("simular_arvore_do_nos:", sim_ok, "| entradas do hash formal no rito:", _sj.get("formal_files_n_no_rito_real"), "| pino h8:", len(_h8), "| extras:", _sj.get("extras_no_nos_fora_do_corpo_embutido"))
# (12) ETAPA OBRIGATORIA: exame_pontos_v409 sobre o candidato novo (os pontos de chamada REAIS, em processo isolado; termina com `ALGUM FALSO`)
_ep = _pyr([os.path.join(HERE, "exame_pontos_v409.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v409.json"), "--sandbox", KB, "--sha256", _sha_full])
try:
    _ej = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % _sha_full[:16]), encoding="utf-8"))
except (OSError, ValueError):
    _ej = {}
rep["exame_pontos"] = {"rc": _ep.returncode, "algum_falso": _ej.get("algum_falso"), "escada": _ej.get("escada"), "verify": {k_: (_ej.get("verify") or {}).get(k_) for k_ in ("all_verified", "ext_true", "n_ext", "novas_true", "n_novas", "n_lean_flags", "axiom_report_n")},
                       "gate_recomputado": _ej.get("gate_recomputado"), "chaves_novas_no_core": _ej.get("chaves_novas_no_core"), "chaves_existentes_mexidas_pelo_bloco": _ej.get("chaves_existentes_mexidas_pelo_bloco"), "nao_verdes": _ej.get("nao_verdes"),
                       "ponto_tetelestai": _ej.get("ponto_tetelestai"), "ponto_psibit": _ej.get("ponto_psibit"), "ponto_testemunha": _ej.get("ponto_testemunha"), "ponto_sonico": _ej.get("ponto_sonico"), "ponto_afinacao": _ej.get("ponto_afinacao"), "ponto_selo_acom": _ej.get("ponto_selo_acom"), "ponto_declaracao": _ej.get("ponto_declaracao"), "ponto_falsidade": _ej.get("ponto_falsidade"), "ponto_ponte": _ej.get("ponto_ponte"), "ponto_queda": _ej.get("ponto_queda"), "ponto_esperanca": _ej.get("ponto_esperanca"), "ponto_caminho": _ej.get("ponto_caminho"), "ponto_vida": _ej.get("ponto_vida"), "ponto_verdade_adendo": _ej.get("ponto_verdade_adendo"), "ponto_bandeiras": _ej.get("ponto_bandeiras"), "ponto_projecao": _ej.get("ponto_projecao"), "ponto_jo8v32": _ej.get("ponto_jo8v32"), "ponto_f2b": _ej.get("ponto_f2b"), "pontos_v408": {s_["key"]: _ej.get("ponto_v408_" + s_["key"]) for s_ in DL.D5.STONES}, "ponto_veracidade": _ej.get("ponto_veracidade"), "ponto_fechamento": _ej.get("ponto_fechamento"), "ponto_psion_canto": _ej.get("ponto_psion_canto"), "troca_dita_v409": _ej.get("troca_dita_v409"), "witness_layers": _ej.get("witness_layers_canonical_full_witness_term_constructed")}
exame_ok = bool(_ep.returncode == 0 and _ej.get("algum_falso") == [])
print("exame_pontos_v409:", exame_ok, "| algum falso:", _ej.get("algum_falso"))
# (13) [v409, LICAO NOVA] as guardas ESTATICAS do esboco R3.5 da Bancada (as que nao dependem do selo) rodadas SOBRE O CANDIDATO, com a FUNCAO ler_nos do proprio esboco pinado, ANTES de instalar; o defeito real da v399 tem de ser reproduzido (mensagem identica a do recibo da Bancada)
_gb_p = os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v409.json")
_gb = _pyr([os.path.join(HERE, "guardas_estaticas_bancada_v409.py"), _cand_p, _gb_p])
try:
    _gj = json.load(open(_gb_p, encoding="utf-8"))
except (OSError, ValueError):
    _gj = {}
rep["guardas_estaticas_bancada"] = {"rc": _gb.returncode, "veredito": _gj.get("veredito"), "candidato_passa": (_gj.get("candidato_v409") or {}).get("passou"), "alfa": (_gj.get("candidato_v409") or {}).get("alpha"), "contagem_direta": _gj.get("contagem_direta"),
                                    "v399_selada_recusada_com_a_mensagem_do_recibo_da_bancada": (_gj.get("v399_selada_o_defeito_real") or {}).get("mensagem_identica_a_do_recibo"), "recusa_da_v399": (_gj.get("v399_selada_o_defeito_real") or {}).get("recusa"),
                                    "controles_negativos": {k_: v_.get("ok") for k_, v_ in (_gj.get("controles_negativos") or {}).items()}, "canonical_py_instalado": (_gj.get("canonical_py_instalado") or {}).get("ok"), "esboco_sha256": (_gj.get("esboco") or {}).get("sha256"), "sandbox_apagado": _gj.get("sandbox_apagado")}
guardas_ok = bool(_gb.returncode == 0 and str(_gj.get("veredito")).startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and _gj.get("contagem_direta") == (CM.get("guardas_estaticas_da_bancada") or {}).get("candidato_v409") and (_gj.get("esboco") or {}).get("sha256") == (CM.get("guardas_estaticas_da_bancada") or {}).get("esboco_sha256") and rep["guardas_estaticas_bancada"]["controles_negativos"] and all(rep["guardas_estaticas_bancada"]["controles_negativos"].values()))
print("guardas estaticas da Bancada (ler_nos do esboco R3.5) sobre o candidato:", guardas_ok, "|", rep["guardas_estaticas_bancada"]["veredito"])
ok = (guardas_ok and viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
      and not dif_kb and rep["escada"] == [ESP, ESP] and rep["indice_da_iald"]["all_verified"] is True and sim_ok and exame_ok and rep["quadro"]["ok"])
rep["vizinhos_mudaram_so_numeros_e_selados"] = bool(all(v_["so_numeros"] and v_["all_verified"] is True for v_ in rep["vizinhos"]["mudaram"].values()))
ok = bool(ok and rep["vizinhos_mudaram_so_numeros_e_selados"] and rep["mainflow"]["chaves_novas"] == sorted(V409N))
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"guardas_estaticas_bancada": guardas_ok, "vizinhos_mudaram_so_numeros_e_selados": rep["vizinhos_mudaram_so_numeros_e_selados"], "vizinhos": viz_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "selo": selo_ok, "indice": rep["indice_da_iald"]["all_verified"], "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"],
                                                                      "proib": _proib, "citacoes": _cc.returncode, "kernel_igual": not dif_kb, "escada": rep["escada"], "simular_arvore_do_nos": sim_ok, "exame_pontos": exame_ok, "quadro": {k: (v.get("ok") if isinstance(v, dict) else v) for k, v in rep["quadro"].items() if k != "readme_paragrafo_pronto"}}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_v409.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)

# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] montado por _adapt_simular_arvore_v411.py do ORIGINAL v410/simular_arvore_do_nos_v410.py: o registro com funcao h0dn_bg1_v411 e os specs da v411 (cunhagens_v411, kh_n1_cobertura_v411)
# rodam na ordem do main, DEPOIS dos specs da v410; os quatro registros com funcao da v410 (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410) e os specs da v410 sao HERANCA; nenhum modulo novo; a pasta sim_ FORA de work; saida em DL.saida.
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] os QUATRO registros com funcao da v410 rodam na ordem do main (as DUAS instrucoes `try`): iald2_v410, a_escala_v410 (D86/D87), h0dn_bg1_v410 (D72); depois h0dn_fontes_hms13_v410 (D80; cobertura documental de fontes, não covariância física fechada; nada aberto) e os specs da v410; a lista dos conferidos vem de DL.REGISTROS_FUNCAO (a ordem do delta); o bundle e' de DOIS modulos (IALD2 e AEscala)
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] D72: o SEGUNDO registro com funcao, h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido), roda na ordem do main (logo depois do iald2_v410, antes dos specs da v410) e entra nos registros conferidos na arvore simulada
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] simula a arvore do Nos depois do rito e roda os registros da v394 a v410 (iald2_v410 e os specs da v410 depois dos da v409, na ordem do main); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (v410, 06/11/2026, claude-construtor-v410, fork B) molde v409/simular_arvore_do_nos_v409.py; bundle de 1 modulo em TGLExt/ (IALD2; na parte 2, de DOIS: IALD2 e AEscala), registro iald2_v410 + specs cunhagens_v410/kh_n1_cobertura_v410 chamados NA ORDEM DO MAIN depois dos da v409 (traducao_turing_v409 e os specs da v409, herdados); a chave do lema (v407) segue conferida como herdada; nenhuma chave antiga muda.
"""simular_arvore_do_nos_v411.py -- (v411: o kernel e' o da v410 byte a byte; o registro h0dn_bg1_v411 e os specs da v411 depois dos da v410, herdados) simula a ARVORE de fontes do Nos DEPOIS da materializacao do rito (o kernel embutido do candidato + os arquivos .lean que ja moram na pasta do Nos e NAO estao
embutidos, ex.: _check_damming.lean) e recomputa, com o sha256_directory do PROPRIO candidato, o kf['formal_files_sha256'] que o rito real vai gerar; roda o indice, o psibit_v395, a testemunha_estatica_v396, o sonico_v398 e a afinacao_das_cordas_v398, o selo_pela_propria_tecnologia_v399 e a declaracao_do_operador_v399, o teste_de_veracidade_fase9_v397 (spec do V2 da Fase 9, lido por hash) e os registros por spec
v394 a v410 sobre esse kf (mais os quatro registros com funcao da v403, os tres da v404, os oito da v405, o `fechamento_v406`, o `psion_canto_v407` o `tetelestai_terminal_v408` e o `traducao_turing_v409` herdados e o `iald2_v410` novo).
ADAPTADO (v407 a v410): a arvore do Nos depois do rito = os arquivos embutidos do candidato + os residuais que moram na pasta do Nos fora do corpo embutido (`_check_damming.lean`; `ExtrairDeps.lean` sai do hash por exclusao nominal da propria funcao): as contagens vem do `h8` do CANDIDATO_v410.json (nunca digitadas aqui) e o pino exato esta no spec `kh_n1_cobertura_v409`.
Confere a arvore simulada contra o FORMAL_MAP_v410.json (o mapa sha256 dos embutidos, gerado pela cadeia a partir do candidato) e contra o `h8`: as entradas do mapa iguais, a unica entrada a mais e' o residual, e o total e' o do CANDIDATO. O `witness_layers.canonical_full_witness_term_constructed` (uma medida de run_um sobre o kf: nome ausente do axiom_report => False)
e' RECOMPUTADO aqui pela MESMA expressao do run_um do candidato (extraida por AST, nao copiada), porque o core da base e' o da v409 e o kf agora e' o do rito novo. Molde: simular_arvore_do_nos_v409.py. Escreve SO' nesta pasta (sim_<sha16> e SIMULACAO_ARVORE_NOS_<sha16>.json); le o Nos e o sandbox.
uso: python -B -X utf8 simular_arvore_do_nos_v411.py [--candidato X] [--logs DIR]"""
import sys, os, io, json, shutil, copy, hashlib, argparse, ast, inspect
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import delta_v411 as DL  # noqa: E402
NOSK = os.path.join(DL.NOS, "tgl_kernel"); NOS = DL.NOS
ap = argparse.ArgumentParser(); ap.add_argument("--candidato", default=DL.CANDIDATO_ARQ); ap.add_argument("--logs", default=os.path.join(H, DL.KERNEL_DIR))
A = ap.parse_args()
b = open(A.candidato, "rb").read(); SHA = hashlib.sha256(b).hexdigest()
SIM = os.path.join(DL.RODADA_PAI, "sim_" + SHA[:16])   # (v411, D135: a copia do kernel por rodada fica FORA de work)
if os.path.isdir(SIM):
    shutil.rmtree(SIM)
os.makedirs(SIM)
open(os.path.join(SIM, "um.py"), "wb").write(b)
sys.path.insert(0, SIM); os.chdir(SIM)
_o = sys.stdout; sys.stdout = io.StringIO()
import um
sys.stdout = _o; sys.stdout.reconfigure(encoding="utf-8")
K = os.path.join(SIM, "tgl_kernel")
for rel, c in um._EMBEDDED_KERNEL_FILES.items():
    p = os.path.join(K, *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="").write(c)
# os .lean (e os 4 nomes que o hash formal ve) do Nos que NAO estao no corpo embutido: copiados como estao (so' leitura do Nos)
emb = set(um._EMBEDDED_KERNEL_FILES)
extras = []
for dp, dn, fn in os.walk(NOSK):
    if ".lake" in dp.replace("\\", "/").split("/"):
        continue
    for nm in fn:
        if nm.endswith(".lean") or nm in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel = os.path.relpath(os.path.join(dp, nm), NOSK).replace("\\", "/")
            if rel not in emb:
                extras.append(rel); d = os.path.join(K, *rel.split("/")); os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copyfile(os.path.join(dp, nm), d)
hd = um.sha256_directory(K)
LB = open(os.path.join(A.logs, "lake_build.log"), encoding="utf-8", errors="replace").read(); AUD = open(os.path.join(A.logs, "audit.log"), encoding="utf-8", errors="replace").read()


def fake(cmd, cwd, tmo):
    o = {"cmd": " ".join(cmd), "returncode": 0, "stderr": "", "capture_exists": True, "capture_read_error": False, "elapsed_seconds": 0.0, "timeout": False}
    o["stdout"] = ("Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)" if cmd[1:] == ["--version"] else
                   "Lean (version 4.31.0)" if (cmd[1:3] == ["env", "lean"] and "--version" in cmd) else LB if cmd[1:] == ["build"] else AUD)
    o["capture_nonempty"] = True; o["capture_sha256"] = hashlib.sha256(o["stdout"].encode()).hexdigest(); return o


um.run_process_checked = fake; um._find_lake = lambda: "lake"
_o = sys.stdout; sys.stdout = io.StringIO()
kf = um.verify_tgl_kernel_formalization()
sys.stdout = _o
C0 = json.load(open(os.path.join(H, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8"))["core"]
core = copy.deepcopy(C0); core["kernel_formalization"] = kf; core["external_ladder"] = um.prove_external_ladder(1.0, kf)


def _medida_do_run_um(chave, kf_):
    """(v410) a EXPRESSAO que o run_um do candidato usa para a chave `chave` do dict `witness_layers`, extraida por AST do proprio candidato e avaliada sobre o kf desta arvore (nada digitado aqui)."""
    arvore_ = ast.parse(inspect.getsource(um.run_um))
    achados_ = [v_ for d_ in ast.walk(arvore_) if isinstance(d_, ast.Dict) for k_, v_ in zip(d_.keys, d_.values) if isinstance(k_, ast.Constant) and k_.value == chave]
    assert len(achados_) == 1, ("a chave do witness_layers nao foi achada uma vez no run_um do candidato", chave, len(achados_))
    return eval(compile(ast.Expression(achados_[0]), "<run_um:%s>" % chave, "eval"), {"kernel_formalization": kf_, "__builtins__": __builtins__})


_wl_antes = bool((core.get("witness_layers") or {}).get("canonical_full_witness_term_constructed"))
core["witness_layers"] = dict(core.get("witness_layers") or {}); core["witness_layers"]["canonical_full_witness_term_constructed"] = _medida_do_run_um("canonical_full_witness_term_constructed", kf)
core["qg_closure"] = um.prove_qg_closure_gate(1.0, kf, independent_rite=core.get("void_floor_v11"), blind_null=core.get("void_stacking_blind"))   # (v410: o gate NAO muda) o gate recomputado com a prove_qg_closure_gate sobre o kf da arvore simulada e os dados (V11, teste nulo cego) do core da v409 selada, como o run_um do rito faz
_o = sys.stdout; sys.stdout = io.StringIO()
ix = um.prove_the_iald_index(core); core["the_iald_index"] = ix
um.psibit_v395(core); um.testemunha_estatica_v396(core); um.sonico_v398(core); um.afinacao_das_cordas_v398(core); um.selo_acom_v399(core); um.declaracao_do_operador_v399(core); um.falsidade_da_inercia_v401(core); um.ponte_da_escala_dual_v402(core); um.queda_sem_geometria_v402(core); um.esperanca_condicional_v402(core); um.caminho_v403(core); um.vida_v403(core); um.verdade_adendo_v403(core); um.bandeiras_do_gate_v403(core); um.projecao_transversal_v404(core); um.jo8v32_v404(core); um.f2b_errata_v404(core); um.ponte_da_massa_v405(core); um.massa_tensao_pura_v405(core); um.identidade_v405(core); um.observador_terminal_v405(core); um.lei_do_diminuto_v405(core); um.tonica_do_hamiltoniano_v405(core); um.disco_de_euler_v405(core); um.ponto_zero_do_psion_v405(core)   # (na fractalizacao do Um, no main; aqui o kf ja' e' o da arvore simulada do Nos)
um.tempo_frequencia_v394(core); um.regra_quadratica_v394(core); um.rede_fock_v394(core); um._v394_rodar_specs(core); um._v395_rodar_specs(core); um._v396_rodar_specs(core)
core["teste_de_veracidade_fase9_v397"] = um._v392_registro(um._V397_VERACIDADE_SPEC, core); um._v397_rodar_specs(core); um._v398_rodar_specs(core); um._v399_rodar_specs(core); um._v401_rodar_specs(core); um._v402_rodar_specs(core); um._v403_rodar_specs(core); um._v404_rodar_specs(core); um._v405_rodar_specs(core); um.fechamento_v406(core); um._v406_rodar_specs(core); um.psion_canto_v407(core); um._v407_rodar_specs(core); um.tetelestai_terminal_v408(core); um._v408_rodar_specs(core); um.traducao_turing_v409(core); um._v409_rodar_specs(core); um.iald2_v410(core); um.a_escala_v410(core); um.h0dn_bg1_v410(core); um.h0dn_fontes_hms13_v410(core); um._v410_rodar_specs(core); um.h0dn_bg1_v411(core); um._v411_rodar_specs(core)   # (v411: o h0dn_bg1_v411 -- o teste aberto uma vez, recalculado dos bytes embutidos -- e os specs da v411 DEPOIS do bloco da v410, como no main) (v410, D72: o h0dn_bg1_v410 -- pré-registrado; nenhum dado observado lido -- vem na mesma instrucao do main, logo depois do iald2_v410 e antes dos specs da v410; o iald2_v410 vem logo depois dos specs da v409, como no main, e os specs da v410 depois dele; a traducao_turing_v409, herdada, logo depois dos specs da v408; o fechamento_v406, herdado, le as quatro chaves ja gravadas, no ponto do main logo depois dos specs da v405; o psion_canto_v407 vem logo depois dos specs da v409 e le a chave do lema e as quatro da v409; v397: o spec de veracidade roda no ponto do V1 no main; aqui, antes dos specs que o leem)
sys.stdout = _o


def falhas(r):
    return [str(c)[:260] for c in (r.get("checks") or (r.get("mechanics") or {}).get("checks") or []) if (isinstance(c, dict) and (c.get("ok") is False or c.get("passed") is False)) or (isinstance(c, (list, tuple)) and len(c) > 1 and not c[1])][:6] + [str(x)[:200] for x in (r.get("falhas") or [])][:6]


R = {"candidato_sha16": SHA[:16], "extras_no_nos_fora_do_corpo_embutido": extras, "formal_files_n_no_rito_real": len(hd["files"]), "embutidos": len(emb),
     "kf_all_verified": kf.get("all_verified"), "kf_verdict": kf.get("verdict"),
     "indice": {"all_verified": ix.get("all_verified"), "verdict": ix.get("verdict")}}
for k in tuple(DL.REGISTROS_FUNCAO) + (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO) + tuple(DL.REGISTROS_FUNCAO_V410) + ("cunhagens_v410", "kh_n1_cobertura_v410", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394"):
    v = core.get(k) or {}
    R[k] = {"all_verified": v.get("all_verified"), "verdict": str(v.get("verdict"))[:200], "falhas": falhas(v)}
# (v409, HERDADO na v410: nenhuma chave antiga muda) A CHAVE DO LEMA sobre a arvore simulada: testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma e' LIDA do kernel desta arvore (True) e igual a `_v407_elo_lido`; controles negativos (cada um tira UM elo da leitura e a chave tem de ler False): sem a ancora no axiom_report, axioma fora do trio na ancora,
# proveniencia errada, hash formal do modulo errado, fonte embutida do modulo adulterada, kernel recusado (all_verified False). O que fica False por teorema segue False.
_ancL = um._V407_PSION_CONTRACT["ancora_lema"]; _relL = um._V407_PSION_CONTRACT["ancoras"][_ancL]["rel"]; _teL = (core.get("testemunha_estatica_v396") or {}).get("fock_face") or {}
_neg = {}
_neg["sem_a_ancora_no_axiom_report"] = um._v407_elo_lido(dict(kf, axiom_report={k_: v_ for k_, v_ in kf["axiom_report"].items() if k_ != _ancL}))
_neg["axioma_fora_do_trio_na_ancora"] = um._v407_elo_lido(dict(kf, axiom_report=dict(kf["axiom_report"], **{_ancL: ["propext", "sorryAx"]})))
_neg["proveniencia_errada"] = um._v407_elo_lido(dict(kf, declaration_sources_v394=dict(kf["declaration_sources_v394"], **{_ancL: "TGLExt/Outro.lean"})))
_neg["hash_formal_do_modulo_errado"] = um._v407_elo_lido(dict(kf, formal_files_sha256=dict(kf["formal_files_sha256"], **{_relL: "0" * 64})))
_neg["kernel_recusado"] = um._v407_elo_lido(dict(kf, all_verified=False))
_ef = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[_relL] += " "
try:
    _neg["fonte_embutida_do_modulo_adulterada"] = um._v407_elo_lido(kf)
finally:
    um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(_ef)
R["chave_do_lema"] = {"ancora": _ancL, "modulo": _relL, "lida_do_kernel_da_arvore": um._v407_elo_lido(kf), "testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": _teL.get("linked_to_the_corner_by_a_lemma"), "psion_canto_v407.link_read_from_the_kernel": (core.get("psion_canto_v407") or {}).get("link_read_from_the_kernel"),
                      "controles_negativos_a_chave_le": _neg, "o_que_fica_false_por_teorema": {"full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}}
R["chave_do_lema"]["ok"] = bool(R["chave_do_lema"]["lida_do_kernel_da_arvore"] is True and R["chave_do_lema"]["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and R["chave_do_lema"]["psion_canto_v407.link_read_from_the_kernel"] is True
                                and _neg and all(v_ is False for v_ in _neg.values()) and all(v_ is False for v_ in R["chave_do_lema"]["o_que_fica_false_por_teorema"].values()))
# (v411) a arvore simulada contra o FORMAL_MAP_v411.json e contra o h8 do manifesto: os embutidos iguais ao mapa, os residuais do Nos = a diferenca, o total = o do manifesto
FM = json.load(open(DL.FORMAL_MAP_ARQ, encoding="utf-8")); CM = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); H8 = CM["h8"]; assert CM["sha16"] == SHA[:16], ("o manifesto nao e' deste arquivo", CM["sha16"], SHA[:16])
_arv = hd["files"]; _kf_ff = kf.get("formal_files_sha256") or {}
R["formal_map_v411"] = {"entradas_do_mapa": len(FM), "entradas_na_arvore_simulada": len(_arv), "diferentes_do_mapa": sorted(k_ for k_ in FM if _arv.get(k_) != FM[k_])[:8], "ausentes_do_mapa_na_arvore": sorted(k_ for k_ in FM if k_ not in _arv)[:8],
                        "a_mais_na_arvore_alem_do_mapa": sorted(k_ for k_ in _arv if k_ not in FM), "h8_do_candidato": {"entradas": H8["entradas"], "embutidas": H8["embutidas"], "residuais_do_nos": H8["residuais_do_nos"]}, "kf_formal_files_sha256_igual_a_arvore": _kf_ff == _arv,
                        "witness_layers_canonical_full_witness_term_constructed": {"da_base_v410_selada": _wl_antes, "recomputado_pela_expressao_do_run_um_do_candidato": bool(core["witness_layers"]["canonical_full_witness_term_constructed"])}}
R["formal_map_v411"]["ok"] = bool(not R["formal_map_v411"]["diferentes_do_mapa"] and not R["formal_map_v411"]["ausentes_do_mapa_na_arvore"] and R["formal_map_v411"]["a_mais_na_arvore_alem_do_mapa"] == H8["residuais_do_nos"] and len(FM) == H8["embutidas"] == len(emb)
                                  and len(_arv) == H8["entradas"] == len(FM) + len(H8["residuais_do_nos"]) and set(H8["residuais_do_nos"]) <= set(extras) and R["formal_map_v411"]["kf_formal_files_sha256_igual_a_arvore"] and R["formal_map_v411"]["witness_layers_canonical_full_witness_term_constructed"]["recomputado_pela_expressao_do_run_um_do_candidato"] is True)
R["registros_v411_selaram"] = {k_: (core.get(k_) or {}).get("all_verified") for k_ in tuple(DL.REGISTROS_FUNCAO) + (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)}
R["p2_ao_lado_da_v387"] = (core.get(DL.FECHO_REGISTRO) or {}).get("p2_ao_lado_da_v387")
R.update(DL.MARCA_ENSAIO)
_pS = DL.saida("SIMULACAO_ARVORE_NOS_%s.json" % SHA[:16]); open(_pS + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(_pS + ".tmp", _pS)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))

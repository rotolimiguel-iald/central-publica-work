# -*- coding: utf-8 -*-
"""p00_precondicoes_v403.py -- confere, SO LENDO, as pre-condicoes de bytes da v403 ANTES de instalar. Nada e escrito fora de PRECONDICOES_v403.json (nesta pasta). Os pinos sao LIDOS do selo/core/arquivos,
nunca digitados. Fail-closed: rc 1 se algo falha. Molde: p00_precondicoes_v399.py (a cadeia de CONTEUDO) com a licao da v402. uso: python -I -B -X utf8 p00_precondicoes_v403.py"""
import ast, glob, hashlib, json, os, re, shutil, subprocess, sys
# [v403-patch]
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v403 as DL  # noqa: E402
import acom_conferencias_v403 as AC  # noqa: E402
C = "C:" + os.sep
NOS = DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
KS = DL.SANDBOX; KA = DL.ARVORE; KDIR = os.path.join(HERE, DL.KERNEL_DIR); BB = os.path.join(HERE, DL.BASE_DIR)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
lj = lambda p: json.load(open(p, encoding="utf-8"))
res = []; ok_all = True


def chk(nome, cond, det=None):
    global ok_all
    res.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); ok_all = ok_all and bool(cond)
    print(("OK   " if cond else "FALHA"), nome, "" if det is None else "-> " + str(det)[:240])


esp4 = json.load(open(os.path.join(DL.V402, "ESPERADOS_v402.json"), encoding="utf-8"))
raw = rd(os.path.join(NOS, "um.py")); selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
chk("um.py do Nos == o que o selo pina e == o candidato selado da v402 (ESPERADOS_v402)", sha(raw) == selo["sha256"]["um.py"] and selo.get("um_version") == "v402" and sha(raw)[:16] == esp4["candidato_sha16"], sha(raw)[:16])
el = core["external_ladder"]; axr = core["kernel_formalization"]["axiom_report"]
chk("escada v402 fechada (limpos == esperados == a de ESPERADOS_v402) e axiom_report v402 lido do core", el["n_theorems_clean"] == el["n_theorems_expected"] == esp4["escada"][1] and len(axr) == esp4["axiom_report_esperado_min"], [el["n_theorems_clean"], el["n_theorems_expected"], len(axr)])
chk("nenhum registro v403 no core ainda (os da v399 e os da v402 ja estao: a v402 selada os tem)", not any(k.endswith("_v403") for k in core) and all(k in core for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")), [k for k in core if k.endswith("_v403")])
_cdir_pilar = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", esp4["pilar"]["key"])
chk("o cache do pilar guarda o resultado que a v402 reaproveitou pela chave (o que a v403 reaproveita e o instalador exige): result.json == o sha256 do selo da v402", os.path.exists(os.path.join(_cdir_pilar, "result.json")) and sha(rd(os.path.join(_cdir_pilar, "result.json"))) == esp4["pilar"]["result_sha256"], esp4["pilar"]["key"][:16])
chk("a copia base_v402 == o Nos (um.py, core, selo, manifesto do kernel, pilar)", all(rd(os.path.join(BB, f)) == rd(os.path.join(NOS, f)) for f in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json")))
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v403.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v403.json"), encoding="utf-8")); PB = json.load(open(os.path.join(HERE, "PINOS_BN_v403.json"), encoding="utf-8"))
_rt = rd(os.path.join(HERE, "runtime_v403.py")).decode("utf-8")
chk("o runtime novo (runtime_v403.py: os QUATRO registros com funcao caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403, escritos a mao) e' o que o candidato embute: o sha256 do CANDIDATO_v403.json == o do arquivo; o bloco extraido do candidato (v403_pins.py) o contem; nenhum literal de beta no codigo (C9); a secao do selo ACOM (a da v402) NAO mudou: o hash do bloco embutido e' o que a v402 pinou",
    CM["runtime"]["sha256"] == sha(rd(os.path.join(HERE, "runtime_v403.py"))) and _rt.rstrip("\n") in rd(os.path.join(HERE, "v403_pins.py")).decode("utf-8") and not AC.literais_de_beta(_rt) and CM["acom"].get("nota") and AC.bloco_das_fontes()[1] == esp4["acom_estudo"]["bloco_embutido_sha256"], [CM["runtime"]["sha256"][:16], CM["runtime"]["bytes"]])
chk("as 6 fontes do operador do ACOM (a origem so' leitura == a copia duravel da cadeia v400 == os pinos do ESPERADOS_v402)", all(sha(rd(o_)) == sha(rd(os.path.join(DL.V400, "insumos", "acom", "fontes_operador", n_))) == esp4["acom_estudo"]["fontes_do_operador"][n_] for n_, o_ in DL.ACOM_FONTES_OPERADOR.items()), len(DL.ACOM_FONTES_OPERADOR))
chk("as TRES pedras (caminho, vida, verdade_adendo) sao a lista dos modulos novos; o sha16 de cada uma e' o que a ordem pinou (pedras_sha16_da_ordem.json); as DUAS falas de 27/10 tem os prefixos de sha256 da ordem (ef3ca5eb, b34bd70f); o adendo de 03-04/09 (erratado ao lado) e' o mesmo que a ordem da v402 pinou",
    sorted(json.load(open(os.path.join(HERE, "kernel_modulos_novos_v403.json"), encoding="utf-8"))["novos"]) == sorted(DL.STONE_RELS) and len(DL.STONES) == 3
    and {s_["key"]: s_["sha16_da_ordem"] for s_ in DL.STONES} == json.load(open(os.path.join(HERE, "pedras_sha16_da_ordem.json"), encoding="utf-8"))
    and [v_["sha16"][:8] for v_ in DL.verbatins403(os.path.join(HERE, "insumos", "cunhagens"))] == DL.VERBATIM_PREFIXOS_DA_ORDEM_V403
    and sha(rd(DL.ADENDO_ARQ))[:16] == DL.ADENDO_SHA16_DA_ORDEM, DL.VERBATIM_PREFIXOS_DA_ORDEM_V403)
cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)
chk("o candidato: sha16 == ESPERADOS == CANDIDATO == PINOS_BN; sha256 == o pino", sha(cb)[:16] == ESP["candidato_sha16"] == CM["sha16"] and sha(cb) == CM["sha256"] == PB["candidato"]["sha256"], [sha(cb)[:16], len(cb)])
chk("ESPERADOS e PINOS_BN pinam os arquivos que estao em disco", all(PB[k]["sha256"] == sha(rd(PB[k]["path"])) for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256") and os.path.exists(PB[k].get("path", ""))), [k for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256")])
chk("os pinos obrigatorios do passo 10 estao em PINOS_BN_v403 (sem cadeia de selos: nao ha salto)", all(k in PB for k in ("criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v402", "kernel_manifesto_anterior_v402")) and "cadeia_de_selos" not in PB)
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v403.json"), encoding="utf-8"))
ESBOCO = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"); ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
gb = lj(os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v403.json"))
chk("[LICAO DA v402] as guardas ESTATICAS do esboco R3.5 da Bancada (a funcao ler_nos do esboco pinado) sobre o CANDIDATO: passa (uma so' linha de alfa e de UM_VERSION); a v399 selada e' recusada com a mensagem EXATA do recibo da Bancada; os 9 controles negativos recusam; o ensaio as rodou",
    gb["veredito"].startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and gb["candidato"]["sha16"] == CM["sha16"] and gb["esboco"]["sha256"] == ESBOCO_SHA256 == sha(rd(ESBOCO)) and gb["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"] is True
    and len(gb["controles_negativos"]) == 9 and all(v["ok"] for v in gb["controles_negativos"].values()) and gb["contagem_direta"] == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0} and ens["guardas_estaticas_bancada"]["veredito"] == gb["veredito"], [gb["candidato_v403"]["alpha"]["n_linhas_nao_indentadas"], gb["contagem_direta"]])
chk("o ensaio a seco e' deste candidato e deu TUDO PASSOU (e o ESPERADOS pina o ensaio); o QUADRO do Teste da Unica Palavra esta no topo do artigo PT/EN e do .md e os numeros do quadro == os do resultado pinado", ens["veredito"] == "TUDO PASSOU" and ens["quadro"]["ok"] is True and ens["sha16"] == CM["sha16"] and ESP["ensaio_sha16"] == sha(rd(os.path.join(HERE, "ensaio_a_seco_v403.json")))[:16], [ens["veredito"], ens["sha16"]])
try:
    ast.parse(cb.decode("utf-8")); sintaxe = True
except SyntaxError:
    sintaxe = False
chk("ast.parse do candidato", sintaxe)
E1, _, _, h1 = carregar(cand)
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v403.json"), encoding="utf-8"))["novos"]
chk("o kernel embutido do candidato == o sandbox construido (o modulo novo, raiz, Audit e os demais, byte a byte)", all(rd(os.path.join(KS, *k.split("/"))) == v.encode("utf-8") for k, v in E1.items()) and len(E1) == CM["formal_files_n"], len(E1))
chk("os modulos novos (%d, lidos da lista) NAO estao no kernel do Nos; as pedras da v394 a v402 estao" % len(nov), nov == list(DL.STONE_RELS) and not any(os.path.exists(os.path.join(NK, *p.split("/"))) for p in nov) and all(os.path.exists(os.path.join(NK, "TGLExt", n + ".lean")) for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional")))
chk("a raiz e o Audit do Nos == os da v402 embutida (o ANTES)", sha(rd(os.path.join(NK, "TGLExt.lean")))[:16] == CM["kernel"]["raiz_v402_sha16"] and sha(rd(os.path.join(NK, "TGL", "Audit.lean")))[:16] == CM["kernel"]["audit_v402_sha16"])
pb = json.load(open(os.path.join(KDIR, "POS_BUILD_v403.json"), encoding="utf-8"))
chk("pos-build do kernel VERDE (rc 0, zero sorry, trio, .olean Lean 4.31.0; raiz e Audit compilados) e a arvore so-fontes existe", pb["ok"] is True and pb["modo_da_pedra_no_build"] and os.path.isdir(KA), [pb["ok"], pb["modo_da_pedra_no_build"], pb["githash_lean"]])
KR = json.load(open(os.path.join(KDIR, "KERNEL_RECIBO_v403.json"), encoding="utf-8"))
chk("o recibo do kernel pina logs e arvore que existem e conferem; cada uma das tres pedras tem declaracoes (nenhum modulo de auditoria)", sha(rd(KR["build_full_log"]["path"])) == KR["build_full_log"]["sha256"] and sha(rd(KR["audit_log"]["path"])) == KR["audit_log"]["sha256"] and os.path.isdir(KR["arvore"]) and len(KR["pedras"]) == len(nov) and all(p["declaracoes"] for p in KR["pedras"]))
MI = json.load(open(os.path.join(HERE, "MANIFESTO_INSUMOS_v403.json"), encoding="utf-8"))
chk("os insumos duraveis == as origens (sha256), exceto a medida do Audit (gerada aqui), e os pinados nos registros conferem", all(sha(rd(os.path.join(HERE, "insumos", k))) == v["sha256"] and (not os.path.exists(v["origem"]) or sha(rd(v["origem"])) == v["sha256"] or k == DL.KH_N1_INSUMO) for k, v in MI.items()), len(MI))
chk("as DUAS falas de 27/10 (ambas do operador): arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == len(DL.VERBATIM_ORIGEM_V403) and all(sha(rd(v["origem"])) == v["sha256"] == sha(rd(os.path.join(HERE, "insumos", k))) for k, v in MI.items() if k.startswith("cunhagens/")))
pr = json.load(open(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v403.json"), encoding="utf-8"))
_esc = pr.get("escrita_na_producao") or {}
chk("o recibo pre_selo do B(n) foi GERADO E PINADO ANTES da instalacao: arquivo == pino; utilizavel; do um.py que esta no Nos; veredito de 'ja sincronizada'; a producao (Bancada e Nos) so' foi lida (listas identicas antes e depois)",
    sha(rd(pr["path"])) == pr["sha256"] and pr["utilizavel_como_recibo_pre_selo_do_B_n"] is True and pr["versao_nos"] == "v402" and pr["um_py_sha16_do_nos"] == sha(raw)[:16] and pr["veredito"].startswith("JA_SINCRONIZADA__ENSAIO")
    and (_esc.get("bancada_um") or {}).get("identico") is True and (_esc.get("nos") or {}).get("identico") is True, [pr["veredito"], pr["utilizavel_como_recibo_pre_selo_do_B_n"], _esc.get("bancada_um"), _esc.get("nos")])
prova = json.load(open(os.path.join(HERE, "PROVA_PRODUCAO_INTACTA_v403_pre_selo.json"), encoding="utf-8"))
F9 = [(c_, os.path.join(DL.F9_DIR_DURAVEL, n_)) for c_, n_ in (("f9v2_resultado", DL.F9_RESULTADO_NOME), ("f9v2_congelamento", "RECIBO_DE_CONGELAMENTO.json"), ("f9v2_abertura", "RECIBO_DE_ABERTURA.json"), ("f9v2_consumida", "ABERTURA_CONSUMIDA.json"))]
chk("o Teste da Unica Palavra (v397, o QUADRO do topo): o resultado e os tres recibos (copias duraveis em v397/insumos/fase9) == os sha256 que a v402 pinou (ESPERADOS_v402); o resultado == o sha256 da ordem da v397; as DUAS falas de 27/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (ambas do operador)",
    all(sha(rd(p_)) == esp4["veracidade"]["fontes"][c_] for c_, p_ in F9) and sha(rd(F9[0][1])) == DL.F9_RESULTADO_SHA256_DA_ORDEM and len(DL.verbatins403(os.path.join(HERE, "insumos", "cunhagens"))) == len(DL.VERBATIM_ORIGEM_V403), [sha(rd(p_))[:16] for _, p_ in F9])
chk("a prova de que a producao so' foi lida existe (PROVA_PRODUCAO_INTACTA_v403_pre_selo.json: producao_intacta True)", prova.get("producao_intacta") is True)
bm = json.load(open(os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json"), encoding="utf-8"))
chk("a Bancada de producao AINDA pina o que o recibo pre_selo diz (versao e um.py): o recibo nao ficou obsoleto", bm["canonical"].get("version") == pr["bancada_pina"]["version"] == "v402" and str(bm["sincronizacao"].get("um_py_sha256"))[:16] == pr["bancada_pina"]["um_py_sha16"], [bm["canonical"].get("version"), str(bm["sincronizacao"].get("um_py_sha256"))[:16]])
sim = json.load(open(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]), encoding="utf-8"))
chk("simular_arvore_do_nos DESTE candidato: o selo_pela_propria_tecnologia_v399, a declaracao_do_operador_v399, os QUATRO registros com funcao v403 e os registros por spec v403 selam na arvore simulada do Nos (a falsidade_da_inercia_v401, o sonico_v398, a afinacao_das_cordas_v398 e os anteriores tambem) e o hash formal tem %d entradas" % ESP["h8_entradas"], sim["candidato_sha16"] == CM["sha16"] and sim["formal_files_n_no_rito_real"] == ESP["h8_entradas"] and all(sim[k_]["all_verified"] is True for k_ in ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "kh_n1_cobertura_v396", "psibit_v395")) and sim["kf_all_verified"] is True, sim["formal_files_n_no_rito_real"])
exm = json.load(open(os.path.join(HERE, "EXAME_PONTOS_%s.json" % CM["sha16"]), encoding="utf-8"))
chk("exame_pontos_v403 DESTE candidato: nenhum ponto de chamada real da falso (o do psibit_v395 vem logo depois do principio da defasagem fractal, o da testemunha_estatica_v396 logo depois do psibit_v395, o do sonico_v398 logo depois da testemunha, o da afinacao_das_cordas_v398 logo depois do sonico, o do selo_pela_propria_tecnologia_v399 logo depois da afinacao, o da declaracao_do_operador_v399 logo depois do selo, o da falsidade_da_inercia_v401 logo depois da declaracao, o da ponte_da_escala_dual_v402 logo depois da falsidade, o da queda_sem_geometria_v402 logo depois da ponte, o da esperanca_condicional_v402 logo depois da queda, o do caminho_v403 logo depois da esperanca, o da vida_v403 logo depois do caminho, o do verdade_adendo_v403 logo depois da vida, o das bandeiras_do_gate_v403 logo depois do adendo e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)", exm["sha256"] == CM["sha256"] and exm.get("algum_falso") == [] and exm["ponto_psibit"]["logo_depois_do_principio_da_defasagem_fractal"] is True and exm["ponto_testemunha"]["logo_depois_do_psibit_v395"] is True and exm["ponto_sonico"]["all_verified"] is True and exm["ponto_sonico"]["logo_depois_da_testemunha_v396"] is True and exm["ponto_sonico"]["beta_ok"] is True and exm["ponto_afinacao"]["all_verified"] is True and exm["ponto_afinacao"]["logo_depois_do_sonico_v402"] is True and exm["ponto_selo_acom"]["all_verified"] is True and exm["ponto_selo_acom"]["logo_depois_da_afinacao_v402"] is True and exm["ponto_selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and exm["ponto_selo_acom"]["controles"] == [13, True] and exm["ponto_declaracao"]["all_verified"] is True and exm["ponto_declaracao"]["logo_depois_do_selo_acom_v403"] is True and exm["ponto_declaracao"]["verbatim_sha256_igual_ao_arquivo"] is True and exm["ponto_falsidade"]["all_verified"] is True and exm["ponto_falsidade"]["logo_depois_da_declaracao_v399"] is True and exm["ponto_falsidade"]["costless_ok"] is True and all(exm["ponto_" + k_]["all_verified"] is True and exm["ponto_" + k_]["logo_depois_da_anterior"] is True and exm["ponto_" + k_]["beta_ok"] is True and exm["ponto_" + k_]["contexto_ok"] is True and exm["ponto_" + k_]["estrela_in_kernel"] is True and exm["ponto_" + k_]["unconditional_in_kernel"] is True and exm["ponto_" + k_]["mecanica"]["n_checks"] == (DL.D2.N_CHECKS[k_] if k_ in ("ponte", "queda", "esperanca") else DL.N_CHECKS[k_]) for k_ in ("ponte", "queda", "esperanca", "caminho", "vida", "verdade_adendo")) and exm["ponto_bandeiras"]["all_verified"] is True and exm["ponto_bandeiras"]["logo_depois_da_anterior"] is True and exm["ponto_bandeiras"]["mecanica"]["n_checks"] == DL.N_CHECKS["gate"] and (exm["ponto_bandeiras"].get("valores_do_gate") or {}).get("n_literal") == 0 and exm["ponto_veracidade"]["all_verified"] is True and exm["ponto_veracidade"]["depois_do_psibit_e_da_testemunha"] is True and exm["ponto_veracidade"]["antes_do_bloco_v393"] is True and all(exm["ponto_veracidade"]["numeros_lidos_iguais_ao_resultado_pinado"].values()), exm.get("algum_falso"))
neg = json.load(open(os.path.join(HERE, "conferencia_rito_v403_CONTROLE_NEGATIVO_PRE_RITO.json"), encoding="utf-8")); pos = json.load(open(os.path.join(HERE, "conferencia_rito_v403_POSITIVO_FALSO_NOS.json"), encoding="utf-8"))
chk("o conferidor: controle negativo (Nos ainda v402) tudo_bate False com os nao-pode-mudar todos verdes; caminho positivo (Nos FALSO montado do ensaio) TUDO BATE", neg["tudo_bate"] is False and all(neg["nao_pode_mudar"].values()) and pos["tudo_bate"] is True, [sum(neg["deve_mudar"].values()), len(neg["deve_mudar"])])
cmp_ = json.load(open(os.path.join(HERE, "COMPARACAO_V402_v403.json"), encoding="utf-8"))
chk("nada da v402 perdido: comparacao AST sem no removido nem mudanca sem explicacao", cmp_["ok"] is True and not cmp_["removidos"] and not cmp_["mudados_sem_explicacao"], [cmp_["iguais"], len(cmp_["mudados"]), cmp_["n_novos"]])
cit = json.load(open(os.path.join(HERE, "conferir_citacoes_v403.json"), encoding="utf-8"))
chk("as citacoes do operador embutidas conferem (embutida == arquivo == fonte original)", cit["todas_conferem"] is True)
chk("pdflatex e lake no PATH; Lean 4.31.0 no sandbox", bool(shutil.which("pdflatex")) and bool(shutil.which("lake")) and "4.31.0" in subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KS).stdout)
chk("as pedras: a fonte aprovada (work) == a copia v403/pedra == a copia duravel pinada (insumos) == a EMBUTIDA no candidato == a do sandbox == o pino dos ESPERADOS == o sha16 que a ordem da gerencia deu", all(sha(rd(s_["origem"])) == sha(rd(s_["src"])) == sha(rd(os.path.join(HERE, "insumos", s_["insumo"]))) == sha(E1[s_["rel"]].encode("utf-8")) == sha(rd(os.path.join(KS, *s_["rel"].split("/")))) == ESP["pedras_sha256"][s_["rel"]] and sha(rd(s_["src"]))[:16] == s_["sha16_da_ordem"] for s_ in DL.STONES), [s_["sha16_da_ordem"] for s_ in DL.STONES])
ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")
ML_N = len(open(ML_, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML_) else -1
ML_B = os.path.getsize(ML_) if os.path.exists(ML_) else -1
chk("o MEMORY.md real cabe com o handoff novo e o gancho da missao: o handoff entra (+1 linha) e o gancho SUBSTITUI a linha velha (saldo +1); linhas hoje + 1 <= 195 e bytes hoje + 900 < 24000 (a linha nova do handoff tem de ter ate 900 B; a superficie do pos-rito NAO compacta: se nao couber, ela RECUSA com rc 3 e a gerencia decide o que sai do indice -- PARE e diga)", 0 < ML_N and ML_N + 1 <= 195 and 0 < ML_B and ML_B + 900 < 24000, [ML_N, ML_N + 1, 195, ML_B, ML_B + 900, 24000])
_MEMD = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory"); _MEMPY = os.path.join(_MEMD, "fila", "memoria.py")
_pm = lj(os.path.join(HERE, "PINO_MEMORIA_PY_v403.json"))
_ver = subprocess.run([sys.executable, "-X", "utf8", _MEMPY, "verificar"], capture_output=True, text=True, encoding="utf-8")
chk("[v403, a FILA DA MEMORIA] memoria.py e' o que a preparacao pinou (sha16 lido do arquivo agora == PINO_MEMORIA_PY_v403.json == o declarado pela gerencia); a pausa do vigia NAO existe agora (o pos-rito a cria antes do indice e a remove depois do pino); e 'memoria.py verificar' (so leitura) esta VERDE agora (rc 0): o pos-rito parte de um indice sem violacao",
    sha(rd(_MEMPY))[:16] == _pm["sha16"] == _pm["declarado_pela_gerencia_sha16"] and not os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json")) and _ver.returncode == 0, [sha(rd(_MEMPY))[:16], _ver.returncode, os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json"))])
chk("o hash formal que o RITO vai gerar (a arvore do Nos depois do rito) tem %d entradas, com os residuais %s; o pino h8 do candidato bate" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]), len(ESP["h8_residuais_do_nos"]) + CM["formal_files_n"] == ESP["h8_entradas"] and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in ESP["h8_residuais_do_nos"]), ESP["h8_entradas"])
chk("nenhum marcador de servidor parado nas pastas das duas cadeias (a guarda do rito)", not os.path.exists(os.path.join(DL.V402, ".servidor_parado_pelo_rito")) and not os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito")))
_pys = sorted(f for f in os.listdir(HERE) if f.endswith(".py") and ".bak" not in f)
for f in _pys:
    try:
        ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read()); s_ = True
    except (SyntaxError, OSError):
        s_ = False
    chk("ast.parse de %s" % f, s_)
for f in ("rito_v403.sh", "construir_kernel_v403.sh", "copiar_k403c.sh", "refazer_candidato_v403.sh", "refazer_sandbox_v403_pos_selo.sh", os.path.join("pos_rito", "chain_pos_rito_v403.sh")):
    chk("sh -n de %s" % f, os.path.exists(os.path.join(HERE, f)) and subprocess.run(["sh", "-n", os.path.join(HERE, f)], capture_output=True).returncode == 0)
dv = json.load(open(os.path.join(HERE, "DERIVACAO_v403.json"), encoding="utf-8"))
chk("a conferencia do instalar/reverter/rito: zero falha nos invariantes (a lista de modulos novos LIDA tem TRES elementos e e a dos ESPERADOS; o sidecar entra nos backups; o recibo pre_selo e' o da v403; a Bancada que JA pina a v402) e a sintaxe de todos", not dv["falhas"] and all(("ok" in v or "rc=0" in v) for v in dv["sintaxe"].values()), [sum(len(x) for x in dv["invariantes"].values())])
marcas = [f for f in glob.glob(os.path.join(HERE, "pos_rito", "*.py")) if "TEXTO_A_REESCREVER" in open(f, encoding="utf-8", errors="replace").read().replace('"TEXTO_A_REESCREVER" +', "").replace("_MARCA_PENDENTE = ", "")]
chk("nenhum texto do pos_rito com a marca TEXTO_A_REESCREVER como comentario pendente", not [m for m in marcas if re.search(r"(?m)^\s*#\s*TEXTO_A_REESCREVER", open(m, encoding="utf-8", errors="replace").read())], [os.path.basename(m) for m in marcas][:4])
print("\nPRECONDICOES v403:", "TODAS PASSARAM" if ok_all else "FALHOU")
json.dump({"ok": ok_all, "checagens": res}, open(os.path.join(HERE, "PRECONDICOES_v403.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if ok_all else 1)

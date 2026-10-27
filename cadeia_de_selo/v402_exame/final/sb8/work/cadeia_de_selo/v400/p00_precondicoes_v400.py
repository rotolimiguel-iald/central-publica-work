# -*- coding: utf-8 -*-
"""p00_precondicoes_v400.py -- confere, SO LENDO, as pre-condicoes de bytes da v400 ANTES de instalar. Nada e escrito fora de PRECONDICOES_v400.json (nesta pasta). Os pinos sao LIDOS do selo/core/arquivos, nunca digitados.
Fail-closed: rc 1 se algo falha. Escrito a mao para a v400 (versao de CORRECAO: nenhum modulo novo de kernel; a base e' a v399 selada; o B(n) e' um passo simples v398 -> v400 com o recibo pre_selo da cadeia v399).
Molde: p00_precondicoes_v399.py. uso: python -I -B -X utf8 p00_precondicoes_v400.py"""
import ast, glob, hashlib, json, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, os.path.join(WK, "v390_pacote")); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
import delta_v400 as DL  # noqa: E402
import acom_conferencias_v400 as AC  # noqa: E402
C = "C:" + os.sep
NOS = DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
KS = DL.SANDBOX; KA = DL.ARVORE; KDIR = os.path.join(HERE, DL.KERNEL_DIR); BB = os.path.join(HERE, DL.BASE_DIR); B98 = os.path.join(HERE, DL.BASE98_DIR)
ESBOCO = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"); ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
lj = lambda p: json.load(open(p, encoding="utf-8"))
res = []; ok_all = True


def chk(nome, cond, det=None):
    global ok_all
    res.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); ok_all = ok_all and bool(cond)
    print(("OK   " if cond else "FALHA"), nome, "" if det is None else "-> " + str(det)[:240])


esp9 = lj(os.path.join(DL.V399, "ESPERADOS_v399.json"))
raw = rd(os.path.join(NOS, "um.py")); selo = lj(os.path.join(NOS, "um_absoluto_selo.json")); core = lj(os.path.join(NOS, "um_absoluto.json"))["core"]
# ---- 1. o canonico de partida e' a v399 SELADA
chk("um.py do Nos == o que o selo pina e == o candidato selado da v399 (ESPERADOS_v399)", sha(raw) == selo["sha256"]["um.py"] and selo.get("um_version") == "v399" and sha(raw)[:16] == esp9["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM, sha(raw)[:16])
el = core["external_ladder"]; axr = core["kernel_formalization"]["axiom_report"]
chk("escada v399 fechada (limpos == esperados == a de ESPERADOS_v399) e axiom_report v399 lido do core", el["n_theorems_clean"] == el["n_theorems_expected"] == esp9["escada"][1] and len(axr) == esp9["axiom_report_esperado_min"], [el["n_theorems_clean"], el["n_theorems_expected"], len(axr)])
chk("nenhum registro _v400 no core ainda", not any(k.endswith("_v400") for k in core), [k for k in core if k.endswith("_v400")])
_cdir_pilar = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", esp9["pilar"]["key"])
chk("o cache do pilar guarda o resultado que a v399 reaproveitou pela chave (o que a v400 reaproveita e o instalador exige): result.json == o sha256 do selo da v399", os.path.exists(os.path.join(_cdir_pilar, "result.json")) and sha(rd(os.path.join(_cdir_pilar, "result.json"))) == esp9["pilar"]["result_sha256"], esp9["pilar"]["key"][:16])
chk("a copia base_v399 == o Nos (um.py, core, selo, manifesto do kernel, pilar e o SIDECAR um_absoluto_selo_acom.json)", all(rd(os.path.join(BB, f)) == rd(os.path.join(NOS, f)) for f in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json")))
sc0 = lj(os.path.join(NOS, "um_absoluto_selo_acom.json"))
chk("o sidecar da v399 no Nos: veredito ALL_OBJECTS_SEALED e pina o um.py v399", sc0["veredito"].startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED") and next(o for o in sc0["objetos"] if o["nome"] == "um.py")["sha256"] == sha(raw))
# ---- 2. o runtime e o candidato
ESP = lj(os.path.join(HERE, "ESPERADOS_v400.json")); CM = lj(os.path.join(HERE, "CANDIDATO_v400.json")); PB = lj(os.path.join(HERE, "PINOS_BN_v400.json")); RM = lj(os.path.join(HERE, "RUNTIME_MONTAGEM_v400.json"))
RM9 = lj(os.path.join(DL.V399, "RUNTIME_MONTAGEM_v399.json"))
chk("o runtime novo (runtime_v400.py) e' o MONTADO do runtime_v399.py (embutido uma vez e byte a byte no um.py v399 selado; sha256 == RUNTIME_MONTAGEM_v399) com 8 edicoes de TEXTO declaradas (cada uma com contagem exata); as conferencias C1, C2, C3, C9, C3', C10 e C11 passaram; o hash do bloco do operador NAO mudou",
    sha(rd(os.path.join(HERE, "runtime_v400.py"))) == RM["runtime"]["sha256"] and RM["entrada"]["sha256"] == RM9["runtime"]["sha256"] and all(v_["ok"] for v_ in RM["conferencias"].values()) and len(RM["edicoes_declaradas"]) == 8
    and RM["bloco_embutido_sha256"][:16] == RM9["conferencias"]["C1_hash_do_bloco_igual_ao_manifesto_e_a_proveniencia"]["detalhe"]["manifesto"] == RM9["conferencias"]["C1_hash_do_bloco_igual_ao_manifesto_e_a_proveniencia"]["detalhe"]["proveniencia"] and {"C3p_a_secao_nao_define_ALPHA_FINE_CODATA_2018", "C10_alfa_unico", "C11_o_bloco_do_operador_nao_mudou"} <= set(RM["conferencias"]), [RM["runtime"]["sha256"][:16], len(RM["edicoes_declaradas"])])
chk("as 6 fontes do operador (acom_mirror.py, acom_crypto.py, tgl_core.py, run_tests.py, o legado torch e o .tex da patente): a origem (so' leitura) == a copia duravel em v399\\insumos (que o um.py v400 continua lendo no rito)",
    all(sha(rd(o_)) == sha(rd(os.path.join(DL.V399, "insumos", "acom", "fontes_operador", n_))) for n_, o_ in DL.ACOM_FONTES_OPERADOR.items()), len(DL.ACOM_FONTES_OPERADOR))
cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)
chk("o candidato: sha16 == ESPERADOS == CANDIDATO == PINOS_BN; sha256 == o pino; a base e' a v399 selada", sha(cb)[:16] == ESP["candidato_sha16"] == CM["sha16"] and sha(cb) == CM["sha256"] == PB["candidato"]["sha256"] and CM["base_v399_sha16"] == DL.BASE_SHA16_DA_ORDEM, [sha(cb)[:16], len(cb)])
chk("ESPERADOS e PINOS_BN pinam os arquivos que estao em disco", all(PB[k]["sha256"] == sha(rd(PB[k]["path"])) for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256") and os.path.exists(PB[k].get("path", ""))), [k for k in PB if isinstance(PB[k], dict) and PB[k].get("sha256")])
chk("os pinos obrigatorios do passo 10 estao em PINOS_BN_v400 (passo SIMPLES v398 -> v400: sem cadeia de selos, nao ha salto declarado)", all(k in PB for k in ("criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v398", "kernel_manifesto_anterior_v398")) and "cadeia_de_selos" not in PB)
chk("o selo e o manifesto do kernel ANTERIORES do B(n) sao os da v398 (a Bancada AINDA pina a v398), copias de bytes: o selo diz v398 e pina o manifesto", lj(os.path.join(B98, "um_absoluto_selo.json"))["um_version"] == "v398" and lj(os.path.join(B98, "um_absoluto_selo.json"))["sha256"]["tgl_kernel_proof_manifest.json"] == sha(rd(os.path.join(B98, "tgl_kernel_proof_manifest.json")))
    and PB["selo_anterior_v398"]["path"].endswith(os.path.join("base_v398", "um_absoluto_selo.json")) and PB["kernel_manifesto_anterior_v398"]["path"].endswith(os.path.join("base_v398", "tgl_kernel_proof_manifest.json")))
ens = lj(os.path.join(HERE, "ensaio_a_seco_v400.json"))
chk("o ensaio a seco e' deste candidato e deu TUDO PASSOU (e o ESPERADOS pina o ensaio); o QUADRO do Teste da Unica Palavra esta no topo do artigo PT/EN e do .md e os numeros do quadro == os do resultado pinado", ens["veredito"] == "TUDO PASSOU" and ens["quadro"]["ok"] is True and ens["sha16"] == CM["sha16"] and ESP["ensaio_sha16"] == sha(rd(os.path.join(HERE, "ensaio_a_seco_v400.json")))[:16], [ens["veredito"], ens["sha16"]])
gb = lj(os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v400.json"))
chk("[LICAO NOVA] as guardas ESTATICAS do esboco R3.5 da Bancada (a funcao ler_nos do esboco pinado) sobre o CANDIDATO: passa (uma so' linha de alfa e de UM_VERSION); a v399 selada e' recusada com a mensagem EXATA do recibo da Bancada; os 9 controles negativos recusam; o ensaio as rodou",
    gb["veredito"].startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and gb["candidato"]["sha16"] == CM["sha16"] and gb["esboco"]["sha256"] == ESBOCO_SHA256 == sha(rd(ESBOCO)) and gb["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"] is True
    and len(gb["controles_negativos"]) == 9 and all(v["ok"] for v in gb["controles_negativos"].values()) and gb["contagem_direta"] == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0} and ens["guardas_estaticas_bancada"]["veredito"] == gb["veredito"], [gb["candidato_v400"]["alpha"]["n_linhas_nao_indentadas"], gb["contagem_direta"]])
try:
    ast.parse(cb.decode("utf-8")); sintaxe = True
except SyntaxError:
    sintaxe = False
chk("ast.parse do candidato", sintaxe)
E1, _, _, h1 = carregar(cand)
nov = lj(os.path.join(HERE, "kernel_modulos_novos_v400.json"))["novos"]
chk("o kernel embutido do candidato == o sandbox k400c (copia do kernel da v399; a raiz, o Audit, a pedra Testemunho e os demais, byte a byte) e == o embutido da v399 selada", all(rd(os.path.join(KS, *k.split("/"))) == v.encode("utf-8") for k, v in E1.items()) and len(E1) == CM["formal_files_n"] and E1 == carregar(os.path.join(BB, "um.py"))[0], len(E1))
chk("NENHUM modulo novo de kernel: a lista kernel_modulos_novos_v400.json e' VAZIA e o kernel do Nos ja' tem a pedra Testemunho (da v399) e as anteriores (v394 a v398)", nov == [] == list(DL.STONE_RELS) and os.path.exists(os.path.join(NK, "TGLExt", "Testemunho.lean")) and all(os.path.exists(os.path.join(NK, "TGLExt", n + ".lean")) for n in ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho")))
chk("a raiz e o Audit do Nos == os do candidato (o kernel da v400 e' o da v399)", sha(rd(os.path.join(NK, "TGLExt.lean")))[:16] == CM["kernel"]["raiz_sha16"] == CM["kernel"]["raiz_v399_sha16"] and sha(rd(os.path.join(NK, "TGL", "Audit.lean")))[:16] == CM["kernel"]["audit_sha16"] == CM["kernel"]["audit_v399_sha16"])
# ---- 3. o kernel (o recibo do B(n)) e a arvore
pb = lj(os.path.join(KDIR, "POS_BUILD_v400.json"))
chk("pos-build do kernel VERDE (rc 0, zero sorry, trio, .olean Lean 4.31.0; raiz e Audit COMPILADOS neste build; o recibo da v400 diz o MESMO do kernel que o da v399) e a arvore so-fontes existe", pb["ok"] is True and pb["modo_da_pedra_no_build"] and os.path.isdir(KA) and all(pb["recibo_igual_ao_da_v399_nos_campos"].values()), [pb["ok"], pb["modo_da_pedra_no_build"], pb["githash_lean"]])
KR = lj(os.path.join(KDIR, "KERNEL_RECIBO_v400.json")); KR9 = lj(os.path.join(DL.V399, "kernel", "KERNEL_RECIBO_v399.json"))
chk("o recibo do kernel pina logs e arvore que existem e conferem (build NOVO em k400c; o log do Audit tem os MESMOS bytes do da v399); lista o diff v398 -> v400 (a pedra Testemunho, com declaracoes: nenhum modulo de auditoria); versao v400",
    sha(rd(KR["build_full_log"]["path"])) == KR["build_full_log"]["sha256"] and sha(rd(KR["audit_log"]["path"])) == KR["audit_log"]["sha256"] == KR9["audit_log"]["sha256"] and os.path.isdir(KR["arvore"]) and KR["versao"] == "v400"
    and [p["path"] for p in KR["pedras"]] == list(DL.STONE_RELS_DESDE_B8) and all(p["declaracoes"] for p in KR["pedras"]) and PB["kernel_recibo"]["n_pedras"] == len(DL.STONE_RELS_DESDE_B8))
CR = lj(os.path.join(HERE, "vinculo", "CRITERIOS_v400.json"))
chk("CRITERIOS_v400 (x19=nao; versao v400) com os mesmos numeros do da v399: J1 2/2/0, 9405 entradas antigas, 0 tokens, r1 ausente, novas no trio", CR["versao"] == "v400" and CR["x19"] == "nao" and CR["esperados"] == lj(os.path.join(DL.V399, "vinculo", "CRITERIOS_v399.json"))["esperados"])
# ---- 4. os insumos duraveis da v399 que o um.py v400 continua lendo no rito
MI = lj(os.path.join(DL.V399, "MANIFESTO_INSUMOS_v399.json"))
chk("os insumos duraveis da v399 (que o um.py v400 le no rito) == o manifesto dela (sha256), exceto a medida do Audit (gerada la)", all(sha(rd(os.path.join(DL.V399, "insumos", k))) == v["sha256"] or k == DL.KH_N1_INSUMO for k, v in MI.items()), len(MI))
chk("as quatro cunhagens de 24/10 (todas falas do operador): arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 4 and all(sha(rd(v["origem"])) == v["sha256"] == sha(rd(os.path.join(DL.V399, "insumos", k))) for k, v in MI.items() if k.startswith("cunhagens/")))
F9 = [(c_, os.path.join(DL.F9_DIR_DURAVEL, n_)) for c_, n_ in (("f9v2_resultado", DL.F9_RESULTADO_NOME), ("f9v2_congelamento", "RECIBO_DE_CONGELAMENTO.json"), ("f9v2_abertura", "RECIBO_DE_ABERTURA.json"), ("f9v2_consumida", "ABERTURA_CONSUMIDA.json"))]
chk("o Teste da Unica Palavra (v397, o QUADRO do topo): o resultado e os tres recibos (copias duraveis em v397/insumos/fase9) == os sha256 que a v399 pinou (ESPERADOS_v399); o resultado == o sha256 da ordem da v397", all(sha(rd(p_)) == esp9["veracidade"]["fontes"][c_] for c_, p_ in F9) and sha(rd(F9[0][1])) == DL.F9_RESULTADO_SHA256_DA_ORDEM, [sha(rd(p_))[:16] for _, p_ in F9])
# ---- 5. o recibo pre_selo do B(n): o da cadeia v399, pinado, sobre o um.py v398 que a Bancada AINDA pina, reconferido pelo PROPRIO esboco
pr = lj(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v400.json")); _esc = pr.get("escrita_na_producao") or {}
cf = lj(os.path.join(HERE, "bateria_pre_selo", "conferencia_pelo_esboco_v400.json"))
chk("o recibo pre_selo do B(n) (o da cadeia v399, gerado e pinado ANTES da instalacao da v399, em ensaio): arquivo == pino; utilizavel; do um.py v398 que a Bancada pina; veredito de 'ja sincronizada'; a producao so' foi lida (listas identicas antes e depois); reconferido pela FUNCAO do esboco R3.5 (aceita; 23/23 condicoes; 5/5 controles)",
    sha(rd(pr["path"])) == pr["sha256"] and pr["utilizavel_como_recibo_pre_selo_do_B_n"] is True and pr["versao_nos"] == "v398" and pr["um_py_sha16_do_nos"] == lj(os.path.join(B98, "um_absoluto_selo.json"))["sha256"]["um.py"][:16] and pr["veredito"].startswith("JA_SINCRONIZADA__ENSAIO")
    and (_esc.get("bancada_um") or {}).get("identico") is True and (_esc.get("nos") or {}).get("identico") is True and cf["esboco_aceita"] is True and cf["n_condicoes_ok"] == cf["n_condicoes"] == 23 and cf["n_controles_como_esperado"] == len(cf["controles_negativos"]) == 5 and cf["recibo"]["sha256"] == pr["sha256"],
    [pr["veredito"], pr["utilizavel_como_recibo_pre_selo_do_B_n"], cf["esboco_aceita"]])
sj = lj(os.path.join(HERE, "salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json"))
chk("o SALTO declarado R3.4 e' IMPOSSIVEL com o esboco R3.5 (MEDIDO): a cadeia v398 -> v399 e' recusada no elo v399 (A11); ler_nos(Nos, v399) recusa com a mensagem do recibo da Bancada; ler_nos(Nos, v398) recusa: nenhum recibo pre_selo NOVO e' possivel; o passo simples v398 -> v400 e' aceito", sj["veredito"].startswith("SALTO_R3_4_IMPOSSIVEL") and sj["ler_nos_v399"]["identica_a_do_recibo_da_bancada"] is True and pr["salto_r3_4_medido"]["sha256"] == sha(rd(os.path.join(HERE, "salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json"))))
bm = lj(os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json"))
chk("a Bancada de producao AINDA pina o que o recibo pre_selo diz (v398, B8, o um.py e o manifesto): o recibo nao ficou obsoleto", bm["canonical"].get("version") == pr["bancada_pina"]["version"] == "v398" and str(bm["sincronizacao"].get("um_py_sha256"))[:16] == pr["bancada_pina"]["um_py_sha16"] and bm["deployment_id"] == pr["bancada_pina"]["deployment_id"] and sha(rd(os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json"))) == pr["valido_enquanto"]["bancada_pina"]["manifesto_sha256"], [bm["canonical"].get("version"), bm["deployment_id"]])
# ---- 6. as etapas obrigatorias das licoes da v394 a v399
sim = lj(os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]))
chk("simular_arvore_do_nos DESTE candidato: o selo_pela_propria_tecnologia_v399, a declaracao_do_operador_v399, os registros por spec v399 e os anteriores selam na arvore simulada do Nos e o hash formal tem %d entradas" % ESP["h8_entradas"], sim["candidato_sha16"] == CM["sha16"] and sim["formal_files_n_no_rito_real"] == ESP["h8_entradas"] and sim["kf_all_verified"] is True and all(sim[k_]["all_verified"] is True for k_ in ens["simular_arvore_do_nos"]["registros"]))
exm = lj(os.path.join(HERE, "EXAME_PONTOS_%s.json" % CM["sha16"]))
chk("exame_pontos_v400 DESTE candidato: nenhum ponto de chamada real da falso (os pontos da v395 a v399 e do V1)", exm["sha256"] == CM["sha256"] and exm.get("algum_falso") == [], exm.get("algum_falso"))
neg = lj(os.path.join(HERE, "conferencia_rito_v400_CONTROLE_NEGATIVO_PRE_RITO.json")); pos = lj(os.path.join(HERE, "conferencia_rito_v400_POSITIVO_FALSO_NOS.json"))
chk("o conferidor: controle negativo (Nos ainda v399) tudo_bate False com os nao-pode-mudar todos verdes; caminho positivo (Nos FALSO montado do ensaio) TUDO BATE", neg["tudo_bate"] is False and all(neg["nao_pode_mudar"].values()) and pos["tudo_bate"] is True, [sum(neg["deve_mudar"].values()), len(neg["deve_mudar"])])
cmp_ = lj(os.path.join(HERE, "COMPARACAO_V399_v400.json"))
chk("nada da v399 perdido: comparacao AST sem no mudado sem explicacao; o unico removido e' ALPHA_FINE_CODATA_2018 (a redeclaracao) e o unico anonimo perdido e' o if dela; nenhum no novo", cmp_["ok"] is True and set(cmp_["removidos"]) == {"ALPHA_FINE_CODATA_2018"} and not cmp_["mudados_sem_explicacao"] and cmp_["n_novos"] == 0 and cmp_["o_unico_anonimo_perdido_e_o_if_da_redeclaracao"] is True, [cmp_["iguais"], len(cmp_["mudados"]), cmp_["n_novos"]])
cit = lj(os.path.join(HERE, "conferir_citacoes_v400.json"))
chk("as citacoes do operador embutidas conferem (embutida == arquivo == fonte original)", cit["todas_conferem"] is True)
chk("pdflatex e lake no PATH; Lean 4.31.0 no sandbox", bool(shutil.which("pdflatex")) and bool(shutil.which("lake")) and "4.31.0" in subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KS).stdout)
ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")
ML_N = len(open(ML_, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML_) else -1
chk("o MEMORY.md real cabe com o handoff novo e o gancho da missao: o handoff entra (+1 linha) e o gancho SUBSTITUI a linha velha (saldo +1); linhas hoje + 1 <= 195 (a superficie NAO compacta: se nao couber, ela RECUSA com rc 3 e a gerencia decide o que sai do indice -- PARE e diga)", 0 < ML_N and ML_N + 1 <= 195, [ML_N, ML_N + 1, 195])
chk("o hash formal que o RITO vai gerar (a arvore do Nos depois do rito) tem %d entradas, com os residuais %s; o pino h8 do candidato bate" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]), len(ESP["h8_residuais_do_nos"]) + CM["formal_files_n"] == ESP["h8_entradas"] and all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in ESP["h8_residuais_do_nos"]), ESP["h8_entradas"])
chk("nenhum marcador de servidor parado nas pastas das duas cadeias (a guarda do rito)", not os.path.exists(os.path.join(DL.V399, ".servidor_parado_pelo_rito")) and not os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito")))
for f in ("delta_v400.py", "preparar_kernel_v400.py", "pos_build_kernel_v400.py", "registros_v400.py", "runtime_v400.py", "montar_runtime_v400.py", "acom_conferencias_v400.py", "runtime_quadro_v397.py", "quadro_v397.py", "copiar_base_v400.py", "diff_e_pinos_v400.py", "gerar_esperados_v400.py",
          "simular_arvore_do_nos_v400.py", "exame_pontos_v400.py", "instalar_v400.py", "reverter_v400.py", "refazer_arvore_v400_pos_selo.py", "conferir_rito_v400.py", "gerar_candidato_v400.py", "ensaio_a_seco_v400.py", "comparar_v399_v400.py", "conferir_citacoes_v400.py",
          "teste_conferidor_positivo_v400.py", "regras_v400.py", "guarda_p18_v400.py", "derivar_v400_motor.py", "derivar_encanamento_v400.py", "derivar_encanamento_v400_regras.py", "derivar_encanamento_v400_regrasB.py", "derivar_encanamento_v400_regrasC.py", "derivar_encanamento_v400_regrasD.py",
          "derivar_encanamento_v400_regrasE.py", "derivar_encanamento_v400_regrasF.py", "guardas_estaticas_bancada_v400.py", "medir_salto_r3_4_v400.py", "gerar_pino_recibo_pre_selo_v400.py", "conferir_instalar_rito_v400.py", "gerar_estado_v400.py", "gerar_registro_mapa_prep_v400.py"):
    try:
        ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read()); s_ = True
    except (SyntaxError, OSError):
        s_ = False
    chk("ast.parse de %s" % f, s_)
for f in ("rito_v400.sh", "copiar_k400c.sh", "refazer_sandbox_v400_pos_selo.sh", "construir_kernel_v400.sh", "refazer_candidato_v400.sh", os.path.join("pos_rito", "chain_pos_rito_v400.sh")):
    chk("sh -n de %s" % f, os.path.exists(os.path.join(HERE, f)) and subprocess.run(["sh", "-n", os.path.join(HERE, f)], capture_output=True).returncode == 0)
dv = lj(os.path.join(HERE, "DERIVACAO_v400.json"))
chk("a conferencia do instalar/reverter/rito: zero falha nos invariantes (a lista de modulos novos LIDA e vazia; o sidecar entra nos backups; o recibo pre_selo e' o da v398; a sintaxe de todos)", not dv["falhas"] and dv["n_modulos_novos_da_lista"] == 0 and all(("ok" in v or "rc=0" in v) for v in dv["sintaxe"].values()), [sum(len(x) for x in dv["invariantes"].values())])
marcas = [f for f in glob.glob(os.path.join(HERE, "pos_rito", "*.py")) if re.search(r"(?m)^\s*#\s*TEXTO_A_REESCREVER", open(f, encoding="utf-8", errors="replace").read())]
chk("nenhum texto do pos_rito com a marca TEXTO_A_REESCREVER como comentario pendente", not marcas, [os.path.basename(m) for m in marcas][:4])
print("\nPRECONDICOES v400:", "TODAS PASSARAM" if ok_all else "FALHOU")
json.dump({"ok": ok_all, "checagens": res}, open(os.path.join(HERE, "PRECONDICOES_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if ok_all else 1)

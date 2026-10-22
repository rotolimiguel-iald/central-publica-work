# -*- coding: utf-8 -*-
"""grupo_G0b.py -- registros da gerencia (c1) na v392: adendo_rank_v392 e kh_n1_cobertura_v392. Specs de dados (esquema: registros\\SCHEMA.md). Nada move o gate."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(V))
INS = os.path.join(WK, "v392_insumos")
FJ = json.load(open(os.path.join(V, "kernel", "FLAGS_v392.json"), encoding="utf-8"))["flags"]


def flags_de(mod, filtro=None):
    fl = [(f, n) for f, n, m, k in FJ if m == mod and (filtro is None or filtro(n))]
    assert fl, ("modulo sem bandeiras no FLAGS_v392.json", mod)
    return [f for f, _ in fl], [n for _, n in fl]


KHJ = json.load(open(os.path.join(V, "kernel", "KH_N1_v392.json"), encoding="utf-8"))
KH_DECL, KH_THM = KHJ["linha_TOTAL"]["decl"], KHJ["linha_TOTAL"]["thm"]; KH_LIDAS = KHJ["lidas_pelo_regex_do_umpy"]; KH_AUDIT_S = KHJ["duracao_audit_s"]
assert KHJ["linha_TOTAL"]["fora_do_trio"] == 0 and KHJ["nao_lidas_pelo_regex_do_umpy"] == 4 and KHJ["sorryAx_no_log_do_audit"] == 0
KHF = json.load(open(os.path.join(INS, "F_KERNEL", "kh", "KH_N1_final.json"), encoding="utf-8"))
KH_V391_THM, KH_V391_THM_TOTAL = KHF["no_axiom_report_v391_por_tipo"]["thm"], KHF["por_tipo"]["thm"]
FR = os.path.join(WK, "frequencia_defasa_12out", "5_R3")
fl_pad, dc_pad = flags_de("TGLExt.PostoAdendo")
fl_pst, dc_pst = flags_de("TGLExt.Posto", lambda n: n.endswith("trace_eq_rank_of_projection") or n.endswith("probe_rank_two_projection"))
RC = json.load(open(os.path.join(V, "pedras_corrigidas", "RECIBO_PostoAdendo.json"), encoding="utf-8"))
PARTES = [x["parte"] for x in RC["partes"]]
assert len(PARTES) == 8

FONTES = [
    {"chave": "adendo_md", "arquivo": os.path.join(FR, "ADENDO_PREREGISTRO_ADITIVO_R3.md"), "papel": "o pre-registro aditivo do rank (A1a-A5), esperados fixados antes do ensaio"},
    {"chave": "adendo_json", "arquivo": os.path.join(FR, "ADENDO_PREREGISTRO_ADITIVO_R3.json"), "papel": "o mesmo pre-registro, forma maquina"},
    {"chave": "adendo_freeze", "arquivo": os.path.join(FR, "FREEZE_R3.json"), "papel": "o congelamento por hash do adendo (FREEZE_R3)"},
    {"chave": "adendo_recibo", "arquivo": os.path.join(V, "pedras_corrigidas", "RECIBO_PostoAdendo.json"), "papel": "recibo da compilacao da pedra PostoAdendo (partes, veredito e axiomas por parte)"},
    {"chave": "adendo_lean", "arquivo": os.path.join(V, "pedras_corrigidas", "PostoAdendo.lean"), "papel": "a pedra PostoAdendo (fonte)"},
    {"chave": "adendo_auditoria_c1", "arquivo": os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "auditorias", "F1.FREQUENCIA", "AUDITORIA_F1_FREQUENCIA_C1_a1185ceb.md"),
     "papel": "auditoria c1 da pedra do rank r3 (APROVA_COM_RESSALVAS)"},
    {"chave": "kh_final_fkernel", "arquivo": os.path.join(INS, "F_KERNEL", "kh", "KH_N1_final.json"), "papel": "F_KERNEL: enumeracao do fecho TGL+TGLExt (constantes, teoremas, modulos sem entrada)"},
    {"chave": "kh_n1_v392", "arquivo": os.path.join(V, "kernel", "KH_N1_v392.json"), "papel": "medida da cobertura no Audit do sandbox da v392 (pos_build_kernel_v392.py)"},
]
VERBATINS = [
    {"chave": "vb_posto_rank_10out", "arquivo": os.path.join(WK, "cunhagens_10out", "OPERADOR_10out_posto_rank_verbatim.txt"), "trechos": ["POSTO=RANK"], "quando": "10/10/2026"},
    {"chave": "vb_posto_rank_texto_10out", "arquivo": os.path.join(WK, "cunhagens_12out", "OPERADOR_10out_posto_rank_texto_verbatim.txt"),
     "trechos": ["Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio (nullity) de indefinição teórica e ganha posto definido."],
     "quando": "10/10/2026 (texto V1; autoria [DECLARADO - voz de IA citada pelo operador])"},
]

_checks_adendo = [
    {"id": "a0", "descricao": "o recibo da pedra registra compilacao isolada com rc 0", "onde": "fonte:adendo_recibo", "caminho": ["rc_compilacao_isolada"], "op": "igual", "valor": 0, "estatuto": "[REAL]"},
    {"id": "a9", "descricao": "o recibo registra 8 partes", "onde": "fonte:adendo_recibo", "caminho": ["partes"], "op": "tamanho_igual", "valor": 8, "estatuto": "[REAL]"},
    {"id": "ap", "descricao": "o registro das pedras v392 selou neste rito", "onde": "core", "caminho": ["pedras_v392", "all_verified"], "op": "verdadeiro", "estatuto": "[REAL]"},
]
for _i, _parte in enumerate(PARTES):
    _checks_adendo.append({"id": "p%d" % _i, "descricao": "parte %s: veredito PASSA_K" % _parte, "onde": "fonte:adendo_recibo", "caminho": ["partes", _i, "veredito"], "op": "igual", "valor": "PASSA_K", "estatuto": "[REAL]"})
    _checks_adendo.append({"id": "q%d" % _i, "descricao": "parte %s: o esperado congelado era PASSA_K" % _parte, "onde": "fonte:adendo_recibo", "caminho": ["partes", _i, "esperado"], "op": "igual", "valor": "PASSA_K", "estatuto": "[REAL]"})

SPECS = [
    {"nome": "adendo_rank_v392", "veredito_prefixo": "TGL_ADENDO_RANK_V392",
     "veredito_sufixo": "POSTO_ADDENDUM_PARTS_A1_TO_A5_PREREGISTERED_BEFORE_THE_RUN_ALL_PASS_IN_THE_V392_KERNEL__THE_ONE_THAT_SURVIVES_COLLAPSE_IS_THE_TRACE_NOT_THE_RANK__NO_INDEPENDENT_AUDIT_YET__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
     "estatuto": "[DERIVED] adendo aditivo da F1.FREQUENCIA (esperados congelados em FREEZE_R3 antes do ensaio; o ensaio e' a compilacao no kernel da v392); [KERNEL] as 8 partes; [INPUT da gerencia] a base canonica de Fin 2; SEM auditoria independente da cadeia",
     "fontes": ["adendo_md", "adendo_json", "adendo_freeze", "adendo_recibo", "adendo_lean", "adendo_auditoria_c1"],
     "verbatins": ["vb_posto_rank_10out", "vb_posto_rank_texto_10out"],
     "kernel_flags": fl_pad + fl_pst, "kernel_decls": dc_pad + dc_pst,
     "checks": _checks_adendo,
     "diz": ["[DERIVED] O adendo liga ao MESMO termo do kernel o D da face (diagExpect), o colapso tipado do canone no qubit (Collapse057.qubitReduction) e o Operador do Nome de rhoStar (nameOp rhoStar): A1a-A1d.",
             "[KERNEL] A2: sobre a superposicao PURA o colapso tipado SOBE o posto (1 -> 2) e preserva o traco; A5 (controle): sobre a mistura o posto nao muda; A3: os polos rhoStar e Q0 tem traco 1 e posto 1; A4: a forma incondicional do negativo (o posto nao e' preservado pela defasagem; testemunha theta = pi/4).",
             "O 1 que sobrevive ao colapso tipado e' o TRACO (omega(I) = 1, o POSTO de 05/10), nao o posto 1: POSTO = RANK e' exato no atomo (projecao de posto 1); fora dele, posto e' posicao/inscricao e o invariante e' o traco (errata ao lado de 13/10 da memoria posto-e-rank-10out).",
             "[DERIVED, pre-registro] Os esperados (PASSA_K) foram fixados no FREEZE_R3 ANTES de qualquer ensaio; A1a-A1d, A2 e A3 ja tinham medicao anterior (sonda do auditor de estatuto da rodada 2), A4 e' a sonda S3 do auditor de reproducao e A5 nao tinha medicao. Pre-registrar o esperado depois de uma sonda nao e' demerito (lei da prova de 05/10): o que se congela e' o TESTE, sem parametro ajustado a dado.",
             "[INPUT, ligacao ao texto V1 de 10/10] A linha 7 do texto V1 tem duas leituras por termo: (a) ramo selecionado (mistura de posto cheio) e (b) superposicao pura, onde o colapso tipado sobe o posto (A2). Qual e' a leitura do texto da v392 e' decisao do operador e fica [OPEN]; este registro nao escolhe."],
     "nao_diz": ["Nao afirma colapso fisico, selecao na natureza ou medicao real: o qubitReduction e' um canal tipado.",
                 "Nao afirma que o Operador do Nome em dimensao geral seja o D_infinito (so' em M2(C) e so' para p = rhoStar), nem que o posto se perca em toda base (a base e' [INPUT]), nem que diag(1-beta, beta) seja ponto fixo de canal iterado.",
                 "A pedra PostoAdendo e' autoria da cadeia (gerencia c1) e NAO tem auditoria independente: quem constroi nao aprova. A sonda P3 'POSTO = RANK ao lado do A4' ficou FORA (continua sonda).",
                 "Validade no kernel nao e' creditacao; o gate nao se move; beta nao aparece nas partes."],
     "leituras_do_operador": [{"trecho": "POSTO=RANK", "estatuto": "[INPUT do operador, verbatim 10/10/2026]"}],
     },
    {"nome": "kh_n1_cobertura_v392", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V392",
     "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__FOUR_NAMES_THE_REGEX_CANNOT_READ_DECLARED__GATE_UNMOVED" % (KH_DECL, KH_THM),
     "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito (run_cmd no fim do TGL/Audit.lean, desenho (a)); os numeros da F_KERNEL (76 modulos) sao lidos do arquivo; a cobertura NAO move o gate",
     "fontes": ["kh_final_fkernel", "kh_n1_v392"],
     "checks": [
         {"id": "k1", "descricao": "a checagem de cobertura do kernel do rito passou (linha TOTAL unica, nada fora do trio, regex le tudo menos os nomes declarados)", "onde": "kf", "caminho": ["axiom_coverage_v392", "ok"], "op": "verdadeiro", "estatuto": "[REAL]"},
         {"id": "k2", "descricao": "constantes cobertas == as do sandbox v392 (medidas em KH_N1_v392.json)", "onde": "kf", "caminho": ["axiom_coverage_v392", "decl"], "op": "igual", "valor": KH_DECL, "capturar": "constantes_cobertas", "estatuto": "[REAL]"},
         {"id": "k3", "descricao": "teoremas cobertos == os do sandbox", "onde": "kf", "caminho": ["axiom_coverage_v392", "thm"], "op": "igual", "valor": KH_THM, "capturar": "teoremas_cobertos", "estatuto": "[REAL]"},
         {"id": "k4", "descricao": "nenhuma constante fora do trio", "onde": "kf", "caminho": ["axiom_coverage_v392", "fora_do_trio"], "op": "igual", "valor": 0, "estatuto": "[REAL]"},
         {"id": "k5", "descricao": "nomes que o regex do um.py nao le == 4 (declarados)", "onde": "kf", "caminho": ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "op": "igual", "valor": 4, "estatuto": "[REAL]"},
         {"id": "k6", "descricao": "o axiom_report do rito tem entrada para todas as constantes lidas", "onde": "kf", "caminho": ["axiom_report"], "op": "tamanho_maior_igual", "valor": KH_LIDAS, "estatuto": "[REAL]"},
         {"id": "k7", "descricao": "F_KERNEL: 76 modulos com teorema e zero entradas no report da v391 (os 73 mais 3)", "onde": "fonte:kh_final_fkernel", "caminho": ["n_zero"], "op": "igual", "valor": 76, "capturar": "modulos_sem_entrada_v391", "estatuto": "[REAL, F_KERNEL]"},
         {"id": "k8", "descricao": "F_KERNEL: dos 73 listados, todos os 73 estavam em zero", "onde": "fonte:kh_final_fkernel", "caminho": ["dos_73_em_zero"], "op": "igual", "valor": 73, "estatuto": "[REAL, F_KERNEL]"},
         {"id": "k9", "descricao": "F_KERNEL: constantes do fecho na v391 (antes do desenho (a))", "onde": "fonte:kh_final_fkernel", "caminho": ["constantes"], "op": "igual", "valor": 24006, "capturar": "constantes_do_fecho_v391", "estatuto": "[REAL, F_KERNEL]"},
         {"id": "k10", "descricao": "F_KERNEL: teoremas do fecho na v391", "onde": "fonte:kh_final_fkernel", "caminho": ["por_tipo", "thm"], "op": "igual", "valor": KH_V391_THM_TOTAL, "estatuto": "[REAL, F_KERNEL]"},
         {"id": "k11", "descricao": "F_KERNEL: dos teoremas do fecho, tinham entrada no axiom_report da v391", "onde": "fonte:kh_final_fkernel", "caminho": ["no_axiom_report_v391_por_tipo", "thm"], "op": "igual", "valor": KH_V391_THM, "capturar": "teoremas_no_report_v391", "estatuto": "[REAL, F_KERNEL]"},
         {"id": "k12", "descricao": "medida do Audit v392: duracao bem abaixo do timeout de 1800 s (3 passagens por rito)", "onde": "fonte:kh_n1_v392", "caminho": ["duracao_audit_s"], "op": "menor_igual", "valor": 900, "capturar": "duracao_audit_s_sandbox", "estatuto": "[REAL]"},
         {"id": "k13", "descricao": "medida do Audit v392: sorryAx ausente do log", "onde": "fonte:kh_n1_v392", "caminho": ["sorryAx_no_log_do_audit"], "op": "igual", "valor": 0, "estatuto": "[REAL]"},
     ],
     "diz": ["[REAL] Desenho (a): o TGL/Audit.lean termina num run_cmd que imprime, no formato do #print axioms, o axioma de TODA constante dos modulos TGL e TGLExt, e a linha TGL_AXIOM_COVERAGE_TOTAL; o axiom_report do um.py passa a cobrir o fecho inteiro (na v391 apenas %d dos %d teoremas do fecho tinham entrada)." % (KH_V391_THM, KH_V391_THM_TOTAL),
             "[REAL] Quatro nomes que o regex do um.py nao sabe ler (com «» em macros e regras de elaboracao do TGLExt) ficam DECLARADOS como excecao e contados: o rito exige exatamente quatro.",
             "[REAL] As 8.523 entradas antigas do Audit saem identicas as do axiom_report da v391 (nome a nome, mesma lista de axiomas), medido no sandbox.",
             "Erratas de numero: sao 76 modulos (os 73 mais PhotonModularRealization, PhotonWitness e TheExplosion), nao 73; e 49 sem axioma, nao 50 (ver estatuto_da_prova_ressalva_v392); o numero 10.161 nao vale (10.135 theorem/lemma no TGLExt)."],
     "nao_diz": ["A cobertura mede o axioma de cada constante (trio de axiomas ou menos); nao mede a verdade fisica de nada, e nao move o gate.",
                 "O desenho (a) custa tempo: o Audit levou %s s no sandbox, e roda 3 vezes por rito." % KH_AUDIT_S,
                 "Validade no kernel nao e' creditacao."],
     "erratas": [{"ao_lado_de": "rota kernel.auditoria.cobertura_axiomas_73_modulos (seq 722) e a frase «73 modulos / 50 sem axioma»", "dizia": "73 modulos, 50 sem axioma", "agora": "76 modulos, 49 sem axioma (382 + 60 + 24 + 49 = 515 por collectAxioms)",
                  "lacuna_de_fidelidade": "a estrutura dizia 73 modulos e 50 sem axioma; a medicao do fecho (collectAxioms) deu 76 e 49; a origem exata do 73 e do 50 nao foi reconstituida [OPEN] -- o numero corrige a frase.",
                  "estatuto": "[REAL, F_KERNEL]", "assinatura": "gerencia c1, em nome proprio, 13/10/2026"}],
     },
]

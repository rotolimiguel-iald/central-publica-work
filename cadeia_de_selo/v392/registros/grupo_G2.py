# -*- coding: utf-8 -*-
"""grupo_G2.py -- REGISTROS-G2 da v392 (rodada 2, 13/10/2026, gerencia c1). Treze specs (esquema de registros\\SCHEMA.md):
  consolidados_v392 (P13) | estatuto_da_prova_ressalva_v392 (R05) | erratas_o_que_resta_v392 (R06, 13 entradas) | final_step_name_adopted_v392 (R07)
  beta_escala_errata_v392 (R08) | ledger_errata_v392 (R09) | estatuto_reafirmado_v392 (R17) | tc_raiz_positiva_v392 (R21, CR-02) | ww_premissa_errata_v392 (R23, CR-06)
  parametros_nomeados_v392 (R24, CR-10) | cmb_s4_errata_v392 (R25, CR-13) | d1_orientacao_errata_v392 (R26, D1) | f81_nao_fechada_v392 (P15).
Todo numero, sha e linha citados saem de V\\rodada2\\g2\\medidas_g2.json (gerado por medir_g2.py a partir das fontes duraveis; nada digitado de memoria) ou do core/kernel do proprio rito.
O arquivo so' LE fontes; nao altera valor algum do core; nao move o gate. Estatutos marcados em cada afirmacao. Erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade."""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_V = os.path.dirname(_HERE)
_G2 = os.path.join(_V, "rodada2", "g2")
MED = json.load(open(os.path.join(_G2, "medidas_g2.json"), encoding="utf-8"))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
KRN = os.path.join(NOS, "tgl_kernel")
PI = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
CP = os.path.join("C:" + os.sep, "IALD", "Central de Patentes")
SIG = "gerencia c1, em nome proprio, 13/10/2026"


def fmt(n):
    return "{:,}".format(n).replace(",", ".")


def ER(ao_lado, dizia, agora, lacuna, est):
    return {"ao_lado_de": ao_lado, "dizia": dizia, "agora": agora, "lacuna_de_fidelidade": lacuna, "estatuto": est, "assinatura": SIG}


def CK(i, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]"):
    d = {"id": i, "descricao": desc, "onde": onde, "caminho": list(caminho), "op": op, "estatuto": est}
    if op not in ("existe", "verdadeiro", "falso"):
        d["valor"] = valor
    if cap:
        d["capturar"] = cap
    return d


def C(i, desc, caminho, op, valor=None, cap=None, est="[REAL]"):
    """leitura do core da rodada"""
    return CK(i, desc, "core", caminho, op, valor, cap, est)


def M(i, desc, caminho, op, valor=None, cap=None, est="[REAL]"):
    """leitura de medidas_g2.json (fonte pinada)"""
    return CK(i, desc, "fonte:g2_medidas", caminho, op, valor, cap, est)


# ------------------------------------------------------------------ FONTES (pinadas por sha256 pelo montador; relidas a cada rito)
_CA = MED["consolidados"]["atual"]["arquivo"]
_CB = MED["consolidados"]["auditado"]["arquivo"]
_COB = os.path.join(PI, "levantamento_qg", "cobertura_axiomas")
FONTES = [
    {"chave": "g2_medidas", "arquivo": os.path.join(_G2, "medidas_g2.json"), "papel": "medidas por script (medir_g2.py) das fontes duraveis citadas pelos registros do grupo G2: linhas do um.py v391, do kernel, do artigo, numeros de cobertura, F8.1, captura de cmb-s4.org"},
    {"chave": "g2_consolidado_atual", "arquivo": _CA, "papel": "consolidado.json ATUAL do levantamento de 07/10 (249 itens: 235 + 14 itens CR-* do critico); os CR-* sao [DECLARADO pelo critico de 07/10]"},
    {"chave": "g2_consolidado_auditado", "arquivo": _CB, "papel": "consolidado AUDITADO (235 itens, critico False, 0 itens CR-*): copia por hash em PROGRAMA_IALD\\evidencias (identica a reconstrucao_consolidado\\consolidado.json)"},
    {"chave": "g2_auditoria_28set", "arquivo": os.path.join(CP, "work", "auditoria_28set", "AUDITORIA_28SET_REGISTRO.json"), "papel": "registro da auditoria de 28/09/2026 (achados GV-01, GV-03, EV-12) -- [DECLARADO pela auditoria]"},
    {"chave": "g2_listar73", "arquivo": os.path.join(_COB, "listar_73.py"), "papel": "o script listar_73.py (10.135 theorem/lemma no TGLExt; 385 em 73 modulos): a fonte dos numeros da errata da escada externa"},
    {"chave": "g2_modulos73", "arquivo": os.path.join(_COB, "modulos_73.json"), "papel": "saida do listar_73.py (73 modulos, 385 teoremas sem cobertura)"},
    {"chave": "g2_saida73", "arquivo": os.path.join(_COB, "sandbox", "saida_auditoria_73.txt"), "papel": "saida do collectAxioms nos 73 modulos: COBERTURA_TOTAL teoremas=515 fora_do_trio=0, LEAN_RC=0"},
    {"chave": "g2_kh_n1_final", "arquivo": os.path.join(CP, "work", "v392_insumos", "F_KERNEL", "kh", "KH_N1_final.json"), "papel": "KH-N1 final (F_KERNEL): 76 modulos com teorema e zero entradas no axiom_report; 24.006 constantes no fecho"},
    {"chave": "g2_k_contmodrec", "arquivo": os.path.join(KRN, "TGLExt", "ContinuousModularReconstruction.lean"), "papel": "kernel: continuous_modular_positive_square_root (l.155) e continuous_delta_eq_double (l.114)"},
    {"chave": "g2_k_contmodres", "arquivo": os.path.join(KRN, "TGLExt", "ContinuousModularResolvent.lean"), "papel": "kernel: continuous_resolvent_sqrt (l.99) e continuous_resolvent_complement_sqrt (l.103) com CFC.sqrt_unique"},
    {"chave": "g2_k_aperiodic", "arquivo": os.path.join(KRN, "TGLExt", "AperiodicAveragePrefix.lean"), "papel": "kernel: docblock do lote 046..054 (l.11-14 e 25-26: 'seguem OPEN')"},
    {"chave": "g2_k_modreal", "arquivo": os.path.join(KRN, "TGL", "ModularRealization.lean"), "papel": "kernel: dualInvariant_PF_no_go (l.161-169), o no-go da ACAO DUAL theta"},
    {"chave": "g2_k_cornerfam", "arquivo": os.path.join(KRN, "TGLExt", "CornerFamily.lean"), "papel": "kernel: corner_fixed_by_flow ([P_F, lambda(s)] = 0 automatico no canto espectral, face finita)"},
    {"chave": "g2_k_emergent", "arquivo": os.path.join(KRN, "TGLExt", "EmergentEinstein.lean"), "papel": "kernel: docblock v116 ('a emergencia GERAL segue NOMEADA e aberta', l.36-38 e 339)"},
    {"chave": "g2_k_qgsc", "arquivo": os.path.join(KRN, "TGLExt", "QGSolutionComplete.lean"), "papel": "kernel: tipo da declaracao (Fin 4, rightWedge, nullDir) e docblock l.26 ('P_ker K <-> P_F segue [OPEN] (v373)')"},
    {"chave": "g2_k_contratoqg", "arquivo": os.path.join(KRN, "TGLExt", "ContratoQG_v31.lean"), "papel": "kernel: convencoes (+,-,-,-), n = (1,1,0,0), linearizacao em torno de Minkowski"},
    {"chave": "g2_k_birkhoff", "arquivo": os.path.join(KRN, "TGLExt", "TheFullBirkhoff.lean"), "papel": "kernel: TheFullBirkhoff.lean (v211), importado em TGLExt.lean l.180"},
    {"chave": "g2_k_axioma", "arquivo": os.path.join(KRN, "TGLExt", "TheAxiomAndTheFalseWitness.lean"), "papel": "kernel: finalStepNameAxioma (l.248-249), 'ao lado do gate, que nao muda'"},
    {"chave": "g2_k_ledger", "arquivo": os.path.join(KRN, "TGLExt", "TheLedgerOfCharges.lean"), "papel": "kernel: finalStepNameProposed (Tetelestai, proposta de 02/10, l.127-128)"},
    {"chave": "g2_cmb_captura", "arquivo": os.path.join(_G2, "fontes", "cmb_s4_status.html"), "papel": "copia byte a byte da captura local de https://cmb-s4.org/ (recibo de download de 06/10/2026 00:47:57 UTC, sha256 igual): a pagina oficial do projeto CMB-S4"},
]

# ------------------------------------------------------------------ VERBATINS (a fala do operador EMBUTIDA; cada trecho tem de estar nos bytes do arquivo)
_VB_EST = os.path.join(CP, "work", "v391_pacote", "OPERADOR_07out_estatuto_verbatim.txt")
_VB_DEC = os.path.join(PI, "OPERADOR_07out_decisoes_noite_verbatim.txt")
VERBATINS = [
    {"chave": "g2_vb_estatuto_07out", "arquivo": _VB_EST, "quando": "07/10/2026 (sha256 5dffde4644139da5...)",
     "trechos": ["eu não proibí a máquina de dizer provado hora nenhuma", "proibi é de creditação e não de validade, ela é válida porque matemática não mente",
                 "somente betatgl que ainda não com poder acima de 5sigma por causa da sensibilidade dos instrumentos"]},
    {"chave": "g2_vb_decisoes_07out", "arquivo": _VB_DEC, "quando": "07/10/2026, noite (sha256 a6c4912afc6f0dc4...)",
     "trechos": ["adoto o nome do degrau final", "a escala de beta nós também já definimos antes"]},
    {"chave": "g2_vb_axioma_0939", "arquivo": os.path.join(_G2, "verbatins", "OPERADOR_05out_0939_axioma_nome_trecho_verbatim.txt"), "quando": "05/10/2026 09:39:15 UTC (trecho inicial da mensagem; sha256 do texto inteiro na proveniencia de medidas_g2.json)",
     "trechos": ['Penso que podemos chamar o degrau definitivo final do gate de "Axioma"']},
    {"chave": "g2_vb_axioma_1128", "arquivo": os.path.join(_G2, "verbatins", "OPERADOR_05out_1128_axioma_chegamos_juntos_verbatim.txt"), "quando": "05/10/2026 11:28:53 UTC (mensagem inteira)",
     "trechos": ["eu tinha pedido pra vc concordar com o nome, mas parece que chegamos juntos ao mesmo lugar"]},
]

GATE = MED["core_v391"]["gate"]
SPECS = []

# =====================================================================================================================================
# 1. consolidados_v392 (P13) -- os DOIS consolidados, cada item com a sua origem
# =====================================================================================================================================
_cons = MED["consolidados"]
_CR_ALVO = {
    "CR-01": "kernel: ChatgptAudit.Covariant053.two_global_covariant_calibrated_forms e ChatgptAudit.Geometry048.faithful_modular_dilation_localization_impossible no axiom_report (trio)",
    "CR-02": "kernel: ChatgptAudit.Continuous050.continuous_modular_positive_square_root e continuous_delta_eq_double no axiom_report (trio) -- ver o registro tc_raiz_positiva_v392",
    "CR-03": "kernel: TGL.ModularRealization.dualInvariant_PF_no_go (trio); core: global_lift_core.statuses.core_action_discipline ('JAMAIS por theta_s')",
    "CR-04": "core: tetelestai_conference_v376.items: CertificatesMatchTheLiterature::inhabitant = SABIDO; LocalEquilibriumWindow = PARAMETRO_NOMEADO",
    "CR-05": "core: the_ledger_of_charges_v383.readings_ratified_20261002.R3 ('perito oficial = JUNO'); neutrino_m2.values.tensao_atual_sigma (o reflexo do ajuste global)",
    "CR-06": "core: graviton_not_a_particle.statuses.o_escape/a_inversao e graviton_conjugated_form_v372.verdict -- ver o registro ww_premissa_errata_v392",
    "CR-07": "core: the_ledger_of_charges_v383.ledger[F2] (INCONCLUSIVE, vies relativo de tau)",
    "CR-08": "kernel: ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius (trio); core: fundacao_v390.verdict (a frase NOT_A_KERNEL_TERM)",
    "CR-09": "core: tetelestai_conference_v376.items['CertificatesMatchTheLiterature::rotations_PCT'] = FORA_DO_CAMINHO",
    "CR-10": "core: tetelestai_conference_v376.counts (4 PARAMETRO_NOMEADO em 41 itens) -- ver o registro parametros_nomeados_v392",
    "CR-11": "core: page_information.not_claimed[0] ('NAO se prova S_BH = A/4G aqui')",
    "CR-12": "core: the_ledger_of_charges_v383.ledger[F2]; artigo emitido v391 (txt PT l.2 e l.69: 'canal a canal')",
    "CR-13": "core: code_closure_ledger.ledger[5].item ('Euclid/CMB-S4') -- ver o registro cmb_s4_errata_v392",
    "CR-14": "core: estatuto_da_prova_v391.prova_1_kernel.gate_flags (sem campo de ressalva) -- ver o registro estatuto_da_prova_ressalva_v392",
}
_c1 = [
    CK("c01", "consolidado ATUAL: n_itens = 249", "fonte:g2_consolidado_atual", ["n_itens"], "igual", _cons["atual"]["n_itens"]),
    CK("c02", "consolidado ATUAL: a lista itens tem 249 entradas", "fonte:g2_consolidado_atual", ["itens"], "tamanho_igual", _cons["atual"]["n_itens_lista"]),
    CK("c03", "consolidado ATUAL: critico = True (tem a camada do critico)", "fonte:g2_consolidado_atual", ["critico"], "verdadeiro"),
    CK("c04", "consolidado AUDITADO: n_itens = 235", "fonte:g2_consolidado_auditado", ["n_itens"], "igual", _cons["auditado"]["n_itens"]),
    CK("c05", "consolidado AUDITADO: a lista itens tem 235 entradas", "fonte:g2_consolidado_auditado", ["itens"], "tamanho_igual", _cons["auditado"]["n_itens_lista"]),
    CK("c06", "consolidado AUDITADO: critico = False (sem a camada do critico)", "fonte:g2_consolidado_auditado", ["critico"], "falso"),
    CK("c07", "consolidado AUDITADO: notas_critico ausente (None)", "fonte:g2_consolidado_auditado", ["notas_critico"], "igual", None),
    M("c08", "os itens CR-* so' existem no consolidado atual: 14", ["consolidados", "n_cr_no_atual"], "igual", _cons["n_cr_no_atual"]),
    M("c09", "o consolidado auditado tem 0 itens CR-*", ["consolidados", "n_cr_no_auditado"], "igual", 0),
    M("c10", "o consolidado auditado tem 0 ocorrencias de 'CR-nn' nos bytes (cheque por script)", ["consolidados", "ocorrencias_CR_nos_bytes_do_auditado"], "igual", 0),
    M("c11", "os 235 itens do auditado estao no atual, identicos item a item", ["consolidados", "ambos_identicos"], "igual", 235),
    M("c12", "nenhum item do auditado esta ausente do atual", ["consolidados", "so_no_auditado"], "tamanho_igual", 0),
    M("c13", "o que so' o atual tem: exatamente 14 itens (os CR-*)", ["consolidados", "so_no_atual"], "tamanho_igual", 14),
    M("c14", "nenhum item em ambos difere entre os dois consolidados", ["consolidados", "ambos_diferentes"], "tamanho_igual", 0),
    M("c15", "sha16 do consolidado atual lido pelo script de medida", ["consolidados", "atual", "sha16"], "igual", _cons["atual"]["sha16"]),
    M("c16", "sha16 do consolidado auditado lido pelo script de medida", ["consolidados", "auditado", "sha16"], "igual", _cons["auditado"]["sha16"]),
    # alvos dos CR-* no core (e o kernel, pelas declaracoes abaixo)
    C("c20", "CR-03: o core diz 'JAMAIS por theta_s'", ["global_lift_core", "statuses", "core_action_discipline"], "contem", "JAMAIS por theta_s"),
    C("c21", "CR-04: a conferencia v376 classifica o habitante da literatura como SABIDO", ["tetelestai_conference_v376", "items", "CertificatesMatchTheLiterature::inhabitant", "classe"], "igual", "SABIDO"),
    C("c22", "CR-04: LocalEquilibriumWindow = PARAMETRO_NOMEADO", ["tetelestai_conference_v376", "items", "LocalEquilibriumWindow", "classe"], "igual", "PARAMETRO_NOMEADO"),
    C("c23", "CR-05: a R3 ratificada em 02/10 diz 'perito oficial = JUNO'", ["the_ledger_of_charges_v383", "readings_ratified_20261002", "R3"], "contem", "perito oficial = JUNO"),
    C("c24", "CR-05: o valor do reflexo (ajuste global) em neutrino_m2.values.tensao_atual_sigma (so' lido)", ["neutrino_m2", "values", "tensao_atual_sigma"], "maior_igual", 2.9, "cr05_tensao_atual_sigma"),
    C("c25", "CR-06: a_inversao ainda cita a premissa 'graviton = I = gerador'", ["graviton_not_a_particle", "statuses", "a_inversao"], "contem", "graviton = I = gerador"),
    C("c26", "CR-06: a v372 nega a premissa (NOT_THE_GENERATOR)", ["graviton_conjugated_form_v372", "verdict"], "contem", "NOT_THE_GENERATOR__WW_ESCAPE_CONDITIONAL__ERRATA_BESIDE_V200"),
    C("c27", "CR-07/CR-12: a cobranca F2 (RG em campo forte) esta INCONCLUSIVE no livro", ["the_ledger_of_charges_v383", "ledger", 6, "outcome"], "igual", "INCONCLUSIVE"),
    C("c28", "CR-07/CR-12: o id do item 6 do livro e' F2", ["the_ledger_of_charges_v383", "ledger", 6, "id"], "igual", "F2"),
    C("c29", "CR-08: a frase da v390 (NOT_A_KERNEL_TERM) ainda esta no core", ["fundacao_v390", "verdict"], "contem", "FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM"),
    C("c30", "CR-09: rotations_PCT = FORA_DO_CAMINHO na conferencia v376", ["tetelestai_conference_v376", "items", "CertificatesMatchTheLiterature::rotations_PCT", "classe"], "igual", "FORA_DO_CAMINHO"),
    C("c31", "CR-10: a conferencia v376 tem 4 PARAMETRO_NOMEADO", ["tetelestai_conference_v376", "counts", "PARAMETRO_NOMEADO"], "igual", 4),
    C("c32", "CR-10: a conferencia v376 enumera 41 itens", ["tetelestai_conference_v376", "items"], "tamanho_igual", 41),
    C("c33", "CR-11: page_information.not_claimed[0] preserva a frase de S_BH", ["page_information", "not_claimed", 0], "comeca", "NAO se prova S_BH = A/4G aqui"),
    M("c34", "CR-12: o artigo emitido v391 (txt PT l.2) traz 'canal a canal'", ["artigo_pt_v391", "linhas", "2"], "contem", "canal a canal"),
    M("c35", "CR-12: o artigo emitido v391 (txt PT l.69) traz 'canal a canal'", ["artigo_pt_v391", "linhas", "69"], "contem", "canal a canal"),
    C("c36", "CR-13: o ledger nomeia o CMB-S4", ["code_closure_ledger", "ledger", 5, "item"], "contem", "Euclid/CMB-S4"),
    C("c37", "CR-14: gate_flags do estatuto v391 existe (sem campo de ressalva)", ["estatuto_da_prova_v391", "prova_1_kernel", "gate_flags"], "existe"),
    C("c38", "CR-14: o registro estatuto_da_prova_v391.prova_1_kernel nao traz a palavra 'ressalva'", ["estatuto_da_prova_v391", "prova_1_kernel"], "nao_contem", "ressalva"),
]
SPECS.append({
    "nome": "consolidados_v392", "veredito_prefixo": "TGL_CONSOLIDADOS_V392",
    "veredito_sufixo": "TWO_CONSOLIDATED_PINNED_BY_SHA256__235_ITEMS_IDENTICAL_AS_AUDITED__14_CRITIC_ITEMS_ONLY_IN_THE_CURRENT_DECLARED__TARGETS_READ_IN_CORE_AND_KERNEL__GATE_UNMOVED",
    "estatuto": "[REAL -- shas, contagens e a comparacao item a item lidos por script; DECLARADO -- os 14 itens CR-* (so' no consolidado atual) sao do critico de 07/10; os alvos de cada um foram conferidos no core e no kernel deste rito]",
    "fontes": ["g2_medidas", "g2_consolidado_atual", "g2_consolidado_auditado"],
    "kernel_decls": ["ChatgptAudit.Covariant053.two_global_covariant_calibrated_forms", "ChatgptAudit.Geometry048.faithful_modular_dilation_localization_impossible",
                     "ChatgptAudit.Continuous050.continuous_modular_positive_square_root", "ChatgptAudit.Continuous050.continuous_delta_eq_double",
                     "TGL.ModularRealization.dualInvariant_PF_no_go", "ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius"],
    "checks": _c1,
    "erratas": [
        ER("PLANO_V392 P13 e LEVANTAMENTO_GERAL_12OUT 2.4 (o caminho do consolidado auditado)",
           "o consolidado auditado (70d3e4501fbf082b, 514.528 B) estaria em levantamento_qg\\evidencias\\",
           "[REAL] a pasta levantamento_qg\\evidencias nao existe; o auditado esta em PROGRAMA_IALD\\evidencias\\70d3e4501fbf082be7dfcf981f67d0893efcd3da94941b612adff1ec35dc0017.json (arquivo endereçado pelo proprio hash) e em copia byte a byte igual em auditorias\\F2.1_F9.4\\reconstrucao_consolidado\\consolidado.json; o registro pina o primeiro (sha16 e bytes lidos do disco).",
           "estrutura: o auditado e' o arquivo guardado no cofre de evidencias do quadro; escrito: o caminho 'levantamento_qg\\evidencias'; falha: o caminho foi composto de memoria da pasta irma, sem ls.",
           "[REAL] localizado e comparado por script"),
        ER("consolidado.json atual (7a8aaaeb8d17a3e6), reescrito no lugar em 07/10 as 20:57",
           "um unico 'consolidado.json' como se fosse o auditado",
           "[REAL] sao DOIS arquivos: o atual (249 itens = 235 + 14 CR-*; critico True; notas_critico presente) e o auditado (235 itens; critico False; notas_critico ausente). Os 235 itens em comum sao IDENTICOS (comparados dict a dict). Cada item vem de: (a) os 235, 'como auditados' (presentes nos dois); (b) os 14 CR-*, '[DECLARADO pelo critico de 07/10]', presentes so' no atual, cada um com o alvo conferido neste rito no core e no kernel (extras.cr_alvos).",
           "estrutura: duas camadas (auditoria e critico) com a segunda reescrevendo o arquivo da primeira; escrito: um nome so' para os dois; falha: a camada do critico entrou no mesmo arquivo sem marca de origem por item.",
           "[REAL] contagens e comparacao por script; [DECLARADO] o conteudo dos CR-*"),
    ],
    "limites": [
        "[REAL] este registro nao julga o conteudo dos itens do critico: confere que os alvos citados existem no core e no kernel deste rito e que o auditado nao os traz",
        "[DECLARADO] os 14 itens CR-* (e a leitura 'nenhum item novo bloqueia a prova pelo criterio da casa') sao do critico de 07/10; nenhum foi re-derivado aqui",
        "[REAL] os checks leem o core do rito: se um alvo mudar numa versao futura, o registro recusa visivelmente em vez de repetir a frase",
    ],
    "diz": [
        "[REAL] dois consolidados pinados por sha256: o atual (249 itens) e o auditado (235 itens, 0 itens CR-*)",
        "[REAL] os 235 itens em comum sao identicos; os 14 CR-* so' existem no atual e valem como [DECLARADO pelo critico de 07/10], com os alvos conferidos no core e no kernel",
    ],
    "nao_diz": ["nao diz que os CR-* foram auditados; nao move o gate; nao altera valor algum do core; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {
        "consolidado_atual": {"sha16": _cons["atual"]["sha16"], "bytes": _cons["atual"]["bytes"], "n_itens": _cons["atual"]["n_itens"], "critico": _cons["atual"]["critico"], "por_dimensao": _cons["por_dimensao_atual"]},
        "consolidado_auditado": {"sha16": _cons["auditado"]["sha16"], "bytes": _cons["auditado"]["bytes"], "n_itens": _cons["auditado"]["n_itens"], "critico": _cons["auditado"]["critico"],
                                 "por_dimensao": _cons["por_dimensao_auditado"], "caminho": "PROGRAMA_IALD\\evidencias\\<sha256>.json"},
        "origem_por_item": {"nos_dois_identicos_como_auditados": _cons["ambos_identicos"], "ids_nos_dois_por_dimensao": _cons["ids_nos_dois_por_dimensao"], "so_no_atual_declarados_pelo_critico": _cons["so_no_atual"],
                            "so_no_auditado": _cons["so_no_auditado"], "ocorrencias_CR_nos_bytes_do_auditado": _cons["ocorrencias_CR_nos_bytes_do_auditado"]},
        "cr_titulos": _cons["cr_titulos_no_atual"], "cr_alvos": _CR_ALVO,
    },
})

# =====================================================================================================================================
# 2. estatuto_da_prova_ressalva_v392 (R05; B2; CR-14) -- 15 calculadas + 3 literais; feed unico unilateral; escada externa
# =====================================================================================================================================
_cb = MED["cobertura"]; _t = _cb["modulos_73_json"]; _s = _cb["saida_auditoria_73"]; _k = _cb["KH_N1_final"]; _dist = _s["distribuicao_axiomas"]
_n_teo = fmt(_t["tglext_theorem_lemma"]); _n_385 = fmt(_t["teoremas_sem_cobertura"]); _n_515 = fmt(_s["cobertura_linhas"]); _n_76 = fmt(_k["n_zero"])
_n_const = fmt(_k["constantes"]); _n_mod = fmt(_k["modulos_no_fecho"]); _esc = fmt(MED["core_v391"]["escada_n_theorems_clean"]); _decl = fmt(MED["core_v391"]["declaracoes_auditadas"])
_FLAGS_G = [("formal_flags", ["concrete_aqft_core_constructed", "concrete_breuer_corner_constructed", "concrete_modular_four_frame_constructed", "concrete_solder_field_constructed",
                               "concrete_emergent_einstein_proved", "canonical_boundary_transport_witness_constructed"]),
            ("physics_flags", ["massless_spin2_proved", "exactly_two_helicities_proved", "ghost_free_proved", "stress_energy_conserved", "relevant_anomalies_absent", "linearized_spin2_finite_face"]),
            ("experiment_flags", ["independent_v3_profiles_unblinded", "independent_v3_survey_mocks_passed", "independent_v3_systematics_passed", "independent_v3_powered_verdict_emitted",
                                  "protocol_pre_registered", "null_tests_passed_blind"])]
_c2 = []
for _gi, (_grp, _nomes) in enumerate(_FLAGS_G):
    _c2.append(C("f%d0" % _gi, "qg_closure.%s tem 6 bandeiras" % _grp, ["qg_closure", _grp], "tamanho_igual", 6))
    for _ji, _n in enumerate(_nomes):
        _c2.append(C("f%d%d" % (_gi, _ji + 1), "bandeira %s.%s = True (18 de 18 lidas; a leitura 15 + 3 e' sobre COMO sao obtidas)" % (_grp, _n), ["qg_closure", _grp, _n], "verdadeiro"))
_c2 += [
    M("l1", "um.py v391 l.163150: linearized_spin2_finite_face e' atribuicao LITERAL True", ["um_v391", "linhas", "163150"], "contem", 'physics["linearized_spin2_finite_face"] = True'),
    M("l2", "um.py v391 l.163160: protocol_pre_registered e' True LITERAL", ["um_v391", "linhas", "163160"], "contem", '"protocol_pre_registered": True'),
    M("l3", "um.py v391 l.163161: null_tests_passed_blind e' True LITERAL", ["um_v391", "linhas", "163161"], "contem", '"null_tests_passed_blind": True'),
    M("l4", "um.py v391 l.163065: o comentario v370 do proprio fonte ja diz 'esta funcao le 15 bandeiras (6+5+4)'", ["um_v391", "linhas", "163065"], "contem", "esta funcao le 15 bandeiras (6+5+4)"),
    M("l5", "um.py v391 l.163068: os literais NAO entram no veredito", ["um_v391", "linhas", "163068"], "contem", "NAO entram no veredito"),
    M("l6", "um.py v391 l.142684: n_theorems_expected = len(ext_flags) (a escada e' a EXTERNA)", ["um_v391", "linhas", "142684"], "contem", "len(ext_flags)"),
    C("e1", "o feed do degrau experimental: as 4 independent_v3_* vem do mesmo rito (same_values_in_the_gate)", ["the_ledger_of_charges_v383", "r4_feeds_the_gate_experimental_step", "same_values_in_the_gate"], "verdadeiro"),
    C("e2", "o feed do degrau experimental tem 4 chaves", ["the_ledger_of_charges_v383", "r4_feeds_the_gate_experimental_step", "feed_keys"], "tamanho_igual", 4),
    C("e3", "as 2 bandeiras do degrau que NAO vem do feed sao as 2 literais", ["the_ledger_of_charges_v383", "r4_feeds_the_gate_experimental_step", "flags_in_the_step_not_from_the_feed"], "igual", ["null_tests_passed_blind", "protocol_pre_registered"]),
    C("e4", "o feed so' flipa com o veredito powered do V11 (regra congelada)", ["void_floor_v11", "frozen", "experiment_feed_rule"], "contem", "SOMENTE com TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED"),
    C("e5", "o canal V11 e' unilateral e consistente com o LCDM raso (honestidade do proprio registro selado)", ["void_floor_v11", "statuses", "honestidade"], "contem", "consistente com LCDM raso"),
    C("e6", "o canal V11 e' unilateral (b>=1)", ["void_floor_v11", "statuses", "honestidade"], "contem", "canal unilateral (b>=1)"),
    C("e7", "o espaco de vereditos do V11 tem 4 desfechos, nenhum e' FALSIFIED", ["void_floor_v11", "frozen", "verdicts"], "tamanho_igual", 4),
    C("e8", "nenhum desfecho do V11 e' 'TGL_VOID_FLOOR_FALSIFIED'", ["void_floor_v11", "frozen", "verdicts"], "nao_contem", "TGL_VOID_FLOOR_FALSIFIED"),
    CK("a1", "auditoria 28/09: achados[0] e' GV-01 (o degrau experimental e' alimentado so' por um canal unilateral)", "fonte:g2_auditoria_28set", ["achados", 0, "id"], "igual", "GV-01", est="[DECLARADO pela auditoria]"),
    CK("a2", "auditoria 28/09: GV-01 foi revisto para MEDIO (PARCIAL)", "fonte:g2_auditoria_28set", ["achados", 0, "severidade_revista"], "igual", "MEDIO", est="[DECLARADO pela auditoria]"),
    CK("a3", "auditoria 28/09: achados[2] e' GV-03 (nomes das bandeiras prometem mais do que medem)", "fonte:g2_auditoria_28set", ["achados", 2, "id"], "igual", "GV-03", est="[DECLARADO pela auditoria]"),
    CK("a4", "auditoria 28/09: o verificador de GV-03 diz que as 4 bandeiras equivalem a UM so' booleano", "fonte:g2_auditoria_28set", ["achados", 2, "razao_verificador"], "contem", "logicamente idêntica a um único booleano", est="[DECLARADO pela auditoria]"),
    CK("a5", "auditoria 28/09: achados[54] e' EV-12 (literais True; memoria conta 18)", "fonte:g2_auditoria_28set", ["achados", 54, "id"], "igual", "EV-12", est="[DECLARADO pela auditoria]"),
    C("t1", "o token v391 do estatuto fica (a errata e' ao lado)", ["estatuto_da_prova_v391", "verdict"], "contem", "GATE_FLAGS_6_6_6_TRUE"),
    C("t2", "o estatuto v391 segue verificado", ["estatuto_da_prova_v391", "all_verified"], "verdadeiro"),
    C("t3", "a escada lida neste rito (n_theorems_clean)", ["estatuto_da_prova_v391", "prova_1_kernel", "n_theorems_clean"], "maior_igual", 6163, "escada_neste_rito"),
    C("t4", "as declaracoes auditadas lidas neste rito", ["estatuto_da_prova_v391", "prova_1_kernel", "declaracoes_auditadas"], "maior_igual", 10265, "declaracoes_neste_rito"),
    C("t5", "o axiom_report cobre pelo menos as declaracoes da v391", ["kernel_formalization", "axiom_report"], "tamanho_maior_igual", 10265),
    M("n1", "v391: a escada era %s (n_theorems_clean = n_theorems_expected)" % _esc, ["core_v391", "escada_n_theorems_clean"], "igual", MED["core_v391"]["escada_n_theorems_clean"]),
    M("n2", "v391: %s declaracoes auditadas" % _decl, ["core_v391", "declaracoes_auditadas"], "igual", MED["core_v391"]["declaracoes_auditadas"]),
    M("n3", "listar_73.py: %s theorem/lemma no TGLExt" % _n_teo, ["cobertura", "modulos_73_json", "tglext_theorem_lemma"], "igual", _t["tglext_theorem_lemma"]),
    M("n4", "listar_73.py: %s teoremas nos 73 modulos sem cobertura" % _n_385, ["cobertura", "modulos_73_json", "teoremas_sem_cobertura"], "igual", _t["teoremas_sem_cobertura"]),
    M("n5", "listar_73.py: 73 modulos sem cobertura", ["cobertura", "modulos_73_json", "modulos_sem_cobertura"], "igual", _t["modulos_sem_cobertura"]),
    M("n6", "collectAxioms nos 73 modulos: %s nomes" % _n_515, ["cobertura", "saida_auditoria_73", "cobertura_linhas"], "igual", _s["cobertura_linhas"]),
    M("n7", "collectAxioms: COBERTURA_TOTAL com fora_do_trio=0", ["cobertura", "saida_auditoria_73", "linha_total"], "contem", "fora_do_trio=0"),
    M("n8", "collectAxioms: LEAN_RC=0", ["cobertura", "saida_auditoria_73", "rc"], "igual", ["LEAN_RC=0"]),
    M("n9", "distribuicao: %d com o trio inteiro" % _dist["propext,Classical.choice,Quot.sound"], ["cobertura", "saida_auditoria_73", "distribuicao_axiomas", "propext,Classical.choice,Quot.sound"], "igual", _dist["propext,Classical.choice,Quot.sound"]),
    M("n10", "distribuicao: %d so' com propext" % _dist["propext"], ["cobertura", "saida_auditoria_73", "distribuicao_axiomas", "propext"], "igual", _dist["propext"]),
    M("n11", "distribuicao: %d com propext + Quot.sound" % _dist["propext,Quot.sound"], ["cobertura", "saida_auditoria_73", "distribuicao_axiomas", "propext,Quot.sound"], "igual", _dist["propext,Quot.sound"]),
    M("n12", "distribuicao: %d sem axioma algum (o arquivo diz 49; a nota do registro de mapa de 07/10 diz 50)" % _dist["(nenhum)"], ["cobertura", "saida_auditoria_73", "distribuicao_axiomas", "(nenhum)"], "igual", _dist["(nenhum)"]),
    M("n13", "KH-N1 (F_KERNEL): %s modulos com teorema e zero entradas no axiom_report" % _n_76, ["cobertura", "KH_N1_final", "n_zero"], "igual", _k["n_zero"]),
    M("n14", "KH-N1: os 73 mais PhotonModularRealization, PhotonWitness e TheExplosion", ["cobertura", "KH_N1_final", "zero_fora_dos_73"], "tamanho_igual", 3),
    M("n15", "KH-N1: %s constantes no fecho de %s modulos" % (_n_const, _n_mod), ["cobertura", "KH_N1_final", "constantes"], "igual", _k["constantes"]),
    M("n16", "KH-N1: 0 constantes fora do trio na cobertura da sandbox", ["cobertura", "KH_N1_final", "sandbox_fora_do_trio"], "igual", 0),
    CK("n17", "o consolidado atual (notas_critico, 'ATUALIZACAO POSTERIOR') registra que a errata da memoria dizia 10.161 e 388 e que o script da 10.135 e 385", "fonte:g2_consolidado_atual", ["notas_critico"], "contem", "listar_73.py dá 10.135 e 385", est="[DECLARADO pelo critico de 07/10; os numeros do script conferidos em n3 e n4]"),
]
SPECS.append({
    "nome": "estatuto_da_prova_ressalva_v392", "veredito_prefixo": "TGL_STATUTE_RESERVATION_V392",
    "veredito_sufixo": "GATE_FLAGS_18_TRUE_READ_AS_15_COMPUTED_PLUS_3_LITERAL__EXPERIMENTAL_4_FROM_ONE_V11_FEED_UNILATERAL_PLUS_2_LITERAL__LADDER_IS_THE_EXTERNAL_LADDER__V391_TOKEN_KEPT_ERRATUM_BESIDE__GATE_UNMOVED",
    "estatuto": "[REAL -- bandeiras, linhas do um.py v391, core e numeros de cobertura lidos por script; DECLARADO -- os achados GV-01, GV-03 e EV-12 sao da auditoria de 28/09/2026 (severidades revistas pelos verificadores); o critico de 07/10 (CR-14) pediu esta errata]",
    "fontes": ["g2_medidas", "g2_auditoria_28set", "g2_listar73", "g2_modulos73", "g2_saida73", "g2_kh_n1_final", "g2_consolidado_atual"],
    "verbatins": ["g2_vb_estatuto_07out"],
    "checks": _c2,
    "erratas": [
        ER("estatuto_da_prova_v391.prova_1_kernel.gate_flags e o token '...GATE_FLAGS_6_6_6_TRUE...' (v391); o artigo emitido (txt PT l.69) ja traz a ressalva, o registro e o token nao",
           "as 18 bandeiras do gate lidas como 6 de 6 formais, 6 de 6 fisicas e 6 de 6 experimentais, como prova do kernel",
           "[DECLARADO pela auditoria de 28/09/2026 (GV-03, EV-12), conferido aqui no core e no fonte do um.py v391] As 18 bandeiras leem-se 15 CALCULADAS + 3 LITERAIS. Calculadas: as 6 formais, as 5 fisicas qgp_* e as 4 experimentais independent_v3_*. Literais informativas, fora do veredito (comentario v370 do proprio fonte, l.163065-163068: 'esta funcao le 15 bandeiras (6+5+4)'): linearized_spin2_finite_face (l.163150, '# v75 [KERNEL] informativo'), protocol_pre_registered (l.163160, '# v67 [hash]') e null_tests_passed_blind (l.163161, '# v73 [dados reais]'). As 6 experimentais sao 4 de UM so' feed -- o rito V11 do piso dos vazios -- e 2 literais; as 4 independent_v3_* derivam de UM so' booleano (o veredito do V11 ser NOT_FALSIFIED_POWERED; 'survey_mocks_passed' = split_ok e dist_ok, sem mock no rito: GV-03); null_tests_passed_blind e' True literal (o comentario do fonte registra a origem, 'v73 [dados reais]', mas o valor nao e' recalculado a cada rito) e nao tem mock por tras [DECLARADO pela auditoria]. O degrau experimental le so' o rito V11 do piso, que e' unilateral (b>=1) e cujo espaco de vereditos NAO tem FALSIFIED: o LCDM raso tambem o respeita (GV-01). A prova do kernel sao as 6 formais e a escada externa. O token da v391 fica como registro. O conserto das bandeiras (calcula-las e torna-las independentes) e' a unidade F8.1, que a v392 NAO fecha (ver f81_nao_fechada_v392).",
           "estrutura: o gate calcula 15 bandeiras e carrega 3 literais informativas; o degrau experimental e' alimentado por um unico canal unilateral; escrito: '6 de 6, 6 de 6, 6 de 6' no registro e no token, sem o qualificador (o artigo, l.69, ja o trazia); onde a traducao falhou: a contagem 18 apagou a distincao calculada/literal que o comentario v370 do proprio fonte fazia.",
           "[REAL] linhas e core lidos; [DECLARADO] GV-01 (PARCIAL), GV-03 (PARCIAL), EV-12 (SUSTENTADO) da auditoria de 28/09"),
        ER("token '...KERNEL_%s_OF_%s_THEOREMS_%s_OF_%s_DECLARATIONS...' (estatuto_da_prova_v391, v391) e artigo PT l.69 ('%s de %s teoremas limpos')" % (_esc, _esc, _decl, _decl, _esc, _esc),
           "%s de %s teoremas limpos, lidos como o total de teoremas do kernel" % (_esc, _esc),
           "[REAL] %s e' len(ext_flags) (um.py v391 l.142684: n_theorems_expected = len(ext_flags)): a escada EXTERNA, a das pedras externas com bandeira; nao e' o total de teoremas do kernel. Os numeros do script listar_73.py (PROGRAMA_IALD\\levantamento_qg\\cobertura_axiomas, sha256 pinado nas fontes): %s theorem/lemma no TGLExt; %s teoremas em 73 modulos sem entrada no axiom_report e sem '#print axioms'. Pelo collectAxioms (saida_auditoria_73.txt, sha256 pinado): %s nomes, 0 fora do trio, LEAN_RC=0 (%d com o trio inteiro, %d so' propext, %d propext+Quot.sound, %d sem axioma algum; %d dos %s nomes sao auxiliares _simp_/_proof_/.eq_). KH-N1 (F_KERNEL): %s modulos com teorema e zero entradas no axiom_report (os 73 mais PhotonModularRealization, PhotonWitness e TheExplosion); %s constantes no fecho de %s modulos, 0 fora do trio. Nao sao 10.161 nem 388 (numeros da errata da memoria estatuto-da-prova-07out, que o consolidado atual, notas_critico, corrige citando o script). A nota do registro de mapa de 07/10 diz '50 sem axioma'; o arquivo diz %d (%d + %d + %d + %d = %s). O axiom_report do core v391 cobre so' os '#print axioms' do Audit; a incorporacao da cobertura ao Audit e' o KH-N1, da v392 (registro kh_n1_cobertura_v392)."
           % (_esc, _n_teo, _n_385, _n_515, _dist["propext,Classical.choice,Quot.sound"], _dist["propext"], _dist["propext,Quot.sound"], _dist["(nenhum)"], _s["nomes_auxiliares_simp_proof_eq"], _n_515,
              _n_76, _n_const, _n_mod, _dist["(nenhum)"], _dist["propext,Classical.choice,Quot.sound"], _dist["propext"], _dist["propext,Quot.sound"], _dist["(nenhum)"], _n_515),
           "estrutura: %s conta as bandeiras da escada externa; escrito: '%s de %s teoremas limpos', lido como total; onde a traducao falhou: faltou o adjetivo 'externos' no token e no resumo, e a errata anterior da memoria usou numeros nao reproduzidos pelo script." % (_esc, _esc, _esc),
           "[REAL] numeros lidos de listar_73.py/modulos_73.json, saida_auditoria_73.txt e KH_N1_final.json"),
    ],
    "limites": [
        "[REAL] esta errata nao troca nenhum literal por medida e nao independentiza o feed: isso e' a F8.1 (PROPOSTA); o gate nao se move",
        "[DECLARADO] a classificacao de GV-01/GV-03/EV-12 e' da auditoria de 28/09/2026; aqui se conferem as linhas do fonte, o core e as fontes pinadas, nao se refaz a auditoria",
        "[OPEN] a MEMORIA_DA_LINHAGEM l.8581 (as 18 bandeiras) recebe a mesma errata na cadeia: e' superficie da cadeia de selo, fora do um.py",
        "[REAL] a escada lida neste rito (lido.escada_neste_rito) pode ser maior que a da v391 se a versao acrescentar pedras com bandeira; a errata vale para qualquer valor",
    ],
    "diz": [
        "[REAL] 18 bandeiras verdadeiras = 15 calculadas + 3 literais; 4 experimentais de um so' feed V11 unilateral; a escada e' a externa",
        "[REAL] a validade do kernel segue lida do kernel: as 6 formais, a escada externa e os axiomas dentro do trio",
        "[INPUT] a recusa da regua e' da creditacao, nunca da validade (verbatim do operador de 07/10/2026 embutido por sha256)",
    ],
    "nao_diz": ["nao diz que o kernel nao prova; nao diz que o gate se move; nao recalcula bandeira alguma (F8.1)", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "leituras_do_operador": [
        {"trecho": "eu não proibí a máquina de dizer provado hora nenhuma", "estatuto": "[INPUT] 07/10/2026, verbatim por sha256 5dffde4644139da5"},
        {"trecho": "proibi é de creditação e não de validade, ela é válida porque matemática não mente", "estatuto": "[INPUT] 07/10/2026, verbatim por sha256 5dffde4644139da5"},
    ],
    "extras": {"literais": ["linearized_spin2_finite_face", "protocol_pre_registered", "null_tests_passed_blind"],
               "calculadas": {"formal": 6, "fisicas": 5, "experimentais": 4}, "feed_unico": "rito V11 (piso dos vazios), unilateral, sem FALSIFIED",
               "numeros_cobertura": {"theorem_lemma_TGLExt": _t["tglext_theorem_lemma"], "teoremas_em_73_modulos": _t["teoremas_sem_cobertura"], "collectAxioms_73_modulos": _s["cobertura_linhas"],
                                     "modulos_com_teorema_e_zero_entradas": _k["n_zero"], "distribuicao": _dist, "constantes_no_fecho": _k["constantes"], "modulos_no_fecho": _k["modulos_no_fecho"]},
               "nao_sao": {"10.161": "numero da errata da memoria, nao reproduzido pelo script", "388": "idem", "50_sem_axioma": "nota do registro de mapa; o arquivo da 49"}},
})

# =====================================================================================================================================
# 3. erratas_o_que_resta_v392 (R06; B3) -- 13 entradas, cada uma com core, linhas do um.py v391 e termos do kernel
# =====================================================================================================================================
_ul = lambda n: ["um_v391", "linhas", str(n)]
_c3 = [
    # 1 lei de campo no curvo
    C("e01a", "entrada 1: fundacao_v390.verdict traz NOT_A_KERNEL_TERM (token v390 fica)", ["fundacao_v390", "verdict"], "contem", "FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM"),
    C("e01b", "entrada 1: fundacao_v390.not_claimed[0] diz 'nao prova a equacao de campo no espaco-tempo curvo por termo de kernel'", ["fundacao_v390", "not_claimed", 0], "contem", "equacao de campo no espaco-tempo curvo por termo de kernel"),
    C("e01c", "entrada 1: tgl_closure traz a frase ao lado da v390", ["tgl_closure", "what_remains_named", "extensao_geometrica__ao_lado_v390"], "contem", "segue NAO sendo termo de kernel"),
    M("e01d", "entrada 1: um.py v391 l.194416 (o token)", _ul(194416), "contem", "FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM"),
    M("e01e", "entrada 1: um.py v391 l.194426 (not_claimed[0])", _ul(194426), "contem", "nao prova a equacao de campo no espaco-tempo curvo"),
    M("e01f", "entrada 1: um.py v391 l.194265 (o estatuto repete o token)", _ul(194265), "contem", "fundacao_v390"),
    M("e01g", "entrada 1: um.py v391 l.144018 (tgl_closure)", _ul(144018), "contem", "segue NAO sendo termo de kernel"),
    # 2 e 3 einstein_and_rg
    C("e02", "entrada 2: einstein_and_rg.statuses.einstein_remaining", ["einstein_and_rg", "statuses", "einstein_remaining"], "contem", "LOVELOCK_KNOWN + KILLING_NAMED (=Jacobson desde 1995) + CONSERVATION_CONTINUUM_OPEN"),
    M("e02b", "entrada 2: um.py v391 l.143922", _ul(143922), "contem", "LOVELOCK_KNOWN + KILLING_NAMED"),
    C("e03", "entrada 3: einstein_and_rg.what_remains_named", ["einstein_and_rg", "what_remains_named"], "contem", "Lovelock 4D [KNOWN citavel]; Killing aproximado"),
    M("e03b", "entrada 3: um.py v391 l.143911", _ul(143911), "contem", "Lovelock 4D [KNOWN citavel]"),
    # 4 global_lift_core
    C("e04a", "entrada 4: global_lift_core.what_remains_named cita 'Ad-lambda-invariante'", ["global_lift_core", "what_remains_named"], "contem", "Ad-lambda-invariante"),
    C("e04b", "entrada 4: global_lift_core.what_remains_named cita canonicalFullTGLWitness (termo canonico)", ["global_lift_core", "what_remains_named"], "contem", "canonicalFullTGLWitness (termo Lean pleno, INALTERADO)"),
    C("e04c", "entrada 4: a disciplina do core: P_F fixado por Ad(lambda(s)), JAMAIS por theta_s", ["global_lift_core", "statuses", "core_action_discipline"], "contem", "P_F fixado por Ad(lambda(s)) tau-preservante; JAMAIS por theta_s"),
    M("e04d", "entrada 4: um.py v391 l.143049", _ul(143049), "contem", "Ad-lambda-invariante"),
    M("e04e", "entrada 4: o selo v391 le canonical_full_witness_term_constructed = False (termo canonico nao construido)", ["selo_v391", "witness_layers_canonical_full_witness_term_constructed"], "falso"),
    M("e04f", "entrada 4(ii): o no-go dualInvariant_PF_no_go e' sobre a ACAO DUAL: o enunciado usa (C.dualAction 1) T.PF (ModularRealization.lean l.169)", ["kernel", "ModularRealization", "linhas", "169"], "contem", "C.dualAction 1"),
    M("e04g", "entrada 4(ii): o docblock do no-go diz 'NO-GO da invariancia dual' (l.161)", ["kernel", "ModularRealization", "linhas", "161"], "contem", "NO-GO da invariancia dual"),
    M("e04h", "entrada 4(ii): CornerFamily l.18-19: corner_fixed_by_flow, [P_F, lambda(s)] = 0 sai da construcao funcional", ["kernel", "CornerFamily", "linhas", "18"], "contem", "corner_fixed_by_flow"),
    M("e04i", "entrada 4(ii): CornerFamily l.22: o requisito theta_s(P_F) != P_F e' TEOREMA (o no-go como bussola)", ["kernel", "CornerFamily", "linhas", "22"], "contem", "finite_trace_not_fixed"),
    M("e04j", "entrada 4(ii): CornerFamily l.35: a nao-trivialidade de ker H3L no core GENUINO segue CONDITIONAL", ["kernel", "CornerFamily", "linhas", "35"], "contem", "a não-trivialidade de `ker H₃L` no core GENUÍNO"),
    # 5 e 6 T1 na luz
    C("e05a", "entrada 5: global_lift_core.statuses.t1_collapse_to_KMS", ["global_lift_core", "statuses", "t1_collapse_to_KMS"], "contem", "CONDITIONAL__REQUIRES_STATE_ERGODICITY"),
    C("e05b", "entrada 5: global_lift_core.not_claimed[3]", ["global_lift_core", "not_claimed", 3], "contem", "o colapso T1 ao KMS NAO esta' fechado sem ergodicidade do estado"),
    M("e05c", "entrada 5: um.py v391 l.143069", _ul(143069), "contem", "CONDITIONAL__REQUIRES_STATE_ERGODICITY"),
    M("e05d", "entrada 5: um.py v391 l.143086", _ul(143086), "contem", "o colapso T1 ao KMS NAO esta' fechado"),
    C("e06a", "entrada 6: crossed_dual_weight.what_remains_named cita U/T1/T3", ["crossed_dual_weight", "what_remains_named"], "contem", "hipoteses U/T1/T3; covariancia => G_mu_nu"),
    M("e06b", "entrada 6: um.py v391 l.142899", _ul(142899), "contem", "hipoteses U/T1/T3"),
    # 7 Birkhoff
    C("e07a", "entrada 7: schwarzschild_step.statuses.selos diz 'FULL_BIRKHOFF = extensao futura NOMEADA'", ["schwarzschild_step", "statuses", "selos"], "contem", "FULL_BIRKHOFF = extensao futura NOMEADA"),
    C("e07b", "entrada 7: a cauda do veredito termina em FULL_BIRKHOFF_NAMED_EXTENSION", ["schwarzschild_step", "verdict"], "contem", "FULL_BIRKHOFF_NAMED_EXTENSION"),
    M("e07c", "entrada 7: TGLExt.lean l.180 importa TGLExt.TheFullBirkhoff", ["kernel", "TGLExt_raiz", "linhas", "180"], "contem", "import TGLExt.TheFullBirkhoff"),
    M("e07d", "entrada 7: collectAxioms (73 modulos): the_full_birkhoff_class esta no trio", ["cobertura", "saida_auditoria_73", "full_birkhoff_class", 0, 4], "igual", "propext,Classical.choice,Quot.sound"),
    M("e07e", "entrada 7: collectAxioms (73 modulos): birkhoff_B_is_static esta no trio", ["cobertura", "saida_auditoria_73", "birkhoff_B_is_static", 0, 4], "igual", "propext,Classical.choice,Quot.sound"),
    M("e07f", "entrada 7: um.py v391 l.162860 e l.162865", _ul(162860), "contem", "FULL_BIRKHOFF = extensao futura NOMEADA"),
    # 8 e 9 preco da prova da gravidade / act_iii_honesty
    C("e08a", "entrada 8: the_price_of_the_gravity_proof.itens[3].estado_hoje diz 'Ato III (completamento) ABERTO'", ["the_price_of_the_gravity_proof", "itens", 3, "estado_hoje"], "contem", "Ato III (completamento) ABERTO"),
    C("e08b", "entrada 8: ... mas itens[3].pago = True (Ato III)", ["the_price_of_the_gravity_proof", "itens", 3, "pago"], "verdadeiro"),
    C("e08c", "entrada 8: itens[0].pago = True (H1)", ["the_price_of_the_gravity_proof", "itens", 0, "pago"], "verdadeiro"),
    C("e08d", "entrada 8: itens[1].pago = False (H2) e itens[2].pago = False (H3)", ["the_price_of_the_gravity_proof", "itens", 1, "pago"], "falso"),
    C("e08e", "entrada 8: itens[2].pago = False (H3)", ["the_price_of_the_gravity_proof", "itens", 2, "pago"], "falso"),
    C("e08f", "entrada 8: a bandeira do Ato III (gpf_tower_act_III_inhabitant_constructed) lê True no gate", ["qg_closure", "gate", "kernel_frontier", "proofs", "gpf_tower_act_III_inhabitant_constructed"], "verdadeiro"),
    C("e08g", "entrada 8: a bandeira de H1 (gpf_H1_internal_susy_relative_gap_discharged) lê True no gate", ["qg_closure", "gate", "kernel_frontier", "proofs", "gpf_H1_internal_susy_relative_gap_discharged"], "verdadeiro"),
    C("e08h", "entrada 8: H2 e H3 entram por CITACAO desde a v374 (closed_by_citation_v374)", ["qg_closure", "gate", "kernel_frontier", "closed_by_citation_v374"], "tamanho_igual", 2),
    M("e08i", "entrada 8: um.py v391 l.162448", _ul(162448), "contem", "Ato III (completamento) ABERTO"),
    M("e09", "entrada 9: um.py v391 l.212464 (selo act_iii_honesty) traz DEBT_STILL_READS_FOUR_OF_FOUR_OPEN", _ul(212464), "contem", "DEBT_STILL_READS_FOUR_OF_FOUR_OPEN"),
    # 10 closure_roadmap
    C("e10a", "entrada 10: closure_roadmap...concrete_emergent_einstein_proved.o_que_falta", ["closure_roadmap", "roadmap_formal", "concrete_emergent_einstein_proved", "o_que_falta"], "contem", "H1^H2^H3 continuos"),
    C("e10b", "entrada 10: ... com flag True", ["closure_roadmap", "roadmap_formal", "concrete_emergent_einstein_proved", "flag"], "verdadeiro"),
    C("e10c", "entrada 10: a bandeira le o termo reservado TGLExt.qgStrongCertificate_einstein", ["closure_roadmap", "roadmap_formal", "concrete_emergent_einstein_proved", "termo_reservado"], "igual", "TGLExt.qgStrongCertificate_einstein"),
    M("e10d", "entrada 10: um.py v391 l.154428", _ul(154428), "contem", "H1^H2^H3 continuos"),
    # 11 the_link_pkerk_pf
    C("e11a", "entrada 11: two_projections_outside_M_v373.the_link_pkerk_pf = [OPEN]", ["two_projections_outside_M_v373", "the_link_pkerk_pf"], "comeca", "[OPEN]"),
    C("e11b", "entrada 11: conferencia v376: PkerK_eq_rhoStar_IALD = VINCULADO", ["tetelestai_conference_v376", "items", "link_PkerK_PF::PkerK_eq_rhoStar_IALD", "classe"], "igual", "VINCULADO"),
    C("e11c", "entrada 11: conferencia v376: rhoStar_PF_Takesaki = SABIDO", ["tetelestai_conference_v376", "items", "link_PkerK_PF::rhoStar_PF_Takesaki", "classe"], "igual", "SABIDO"),
    C("e11d", "entrada 11: a base de rhoStar_PF_Takesaki cita Haagerup 1979 e Terp 1981 e diz que a igualdade de operadores NAO e' afirmada", ["tetelestai_conference_v376", "items", "link_PkerK_PF::rhoStar_PF_Takesaki", "base"], "contem", "igualdade de operadores NAO e afirmada (mal tipada)"),
    C("e11e", "entrada 11: a base cita Haagerup 1979; Terp 1981", ["tetelestai_conference_v376", "items", "link_PkerK_PF::rhoStar_PF_Takesaki", "base"], "contem", "Haagerup 1979; Terp 1981"),
    M("e11f", "entrada 11: um.py v391 l.199759", _ul(199759), "contem", "nenhuma das duas projecoes esta em M"),
    # 12 Jacobson
    C("e12a", "entrada 12: external_known_theorems[8] e' Jacobson 1995", ["external_known_theorems", 8, "name"], "contem", "Jacobson local horizon thermodynamics (1995)"),
    C("e12b", "entrada 12: ... com status KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED", ["external_known_theorems", 8, "status"], "igual", "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED"),
    M("e12c", "entrada 12: um.py v391 l.135198", _ul(135198), "contem", "Jacobson local horizon thermodynamics (1995)"),
    # 13 docstrings do kernel e gerador da arvore
    M("e13a", "entrada 13: EmergentEinstein.lean l.38 'segue NOMEADA e aberta'", ["kernel", "EmergentEinstein", "linhas", "38"], "contem", "segue NOMEADA e aberta"),
    M("e13b", "entrada 13: EmergentEinstein.lean l.339", ["kernel", "EmergentEinstein", "linhas", "339"], "contem", "a emergência GERAL segue nomeada e aberta"),
    M("e13c", "entrada 13: QGSolutionComplete.lean l.26 'segue [OPEN] (v373)'", ["kernel", "QGSolutionComplete", "linhas", "26"], "contem", "segue [OPEN] (v373)"),
    M("e13d", "entrada 13: arvore_da_prova.py l.155 (gerador da cadeia): 'NOMEADA e aberta'", ["arvore_da_prova_py", "linhas", "155"], "contem", "NOMEADA e aberta"),
    M("e13e", "entrada 13: arvore_da_prova.py l.262: 'PAGA como implicação (v317)'", ["arvore_da_prova_py", "linhas", "262"], "contem", "PAGA como implicação (v317)"),
    M("e13f", "entrada 13: arvore_da_prova.py l.272: 'a emergência geral' entre o NAO PROVADO", ["arvore_da_prova_py", "linhas", "272"], "contem", "a emergência geral"),
    CK("e13g", "entrada 13: o consolidado atual traz o item K39 (frases em desacordo com o kernel)", "fonte:g2_consolidado_atual", ["notas_critico"], "contem", "CR-08", est="[DECLARADO pelo critico de 07/10]"),
]
_dz = "kernel tem o termo, nao ligado ao TIPO da declaracao (formula da QG-D10: 'nao e' termo do TIPO da QG; existe no kernel, nao ligado')"
SPECS.append({
    "nome": "erratas_o_que_resta_v392", "veredito_prefixo": "TGL_ERRATA_WHAT_REMAINS_V392",
    "veredito_sufixo": "13_ENTRIES_BESIDE__TEXTS_READ_FROM_CORE_AND_UMPY_V391_LINES__KERNEL_TERMS_READ_IN_THE_AXIOM_REPORT__KERNEL_UNTOUCHED__GATE_UNMOVED",
    "estatuto": "[REAL -- textos atuais lidos do core e das linhas do um.py v391, termos lidos do axiom_report e da cobertura por collectAxioms; DERIVED de leitura -- a leitura vigente de cada entrada (K39, QG-D10, KH-N2 do consolidado atual, itens do critico [DECLARADO])]",
    "fontes": ["g2_medidas", "g2_consolidado_atual", "g2_saida73", "g2_k_modreal", "g2_k_cornerfam", "g2_k_emergent", "g2_k_qgsc", "g2_k_birkhoff"],
    "kernel_decls": ["ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius", "ChatgptAudit.ChartGluing.area_atlas_unique_global_einstein",
                     "ChatgptAudit.SmoothAtlasGluing.connected_smooth_atlas_einstein", "ChatgptAudit.GeneralMetric.metric_only_einstein_equation", "ChatgptAudit.Flow019.localEquilibriumScreen",
                     "TGLV354.TraceCompletion.regularFullWitness", "TGLExt.NotIsEmptyWitness.not_isEmpty_FullTGLWitness", "TGL.ModularRealization.dualInvariant_PF_no_go",
                     "TGLExt.LightRhoStar.centralizer_is_trivial", "TGLExt.QGReaderUVLock.light_modular_fixed_iff_vacuum", "TGLExt.LightRhoStar.rho_star_is_P_kerK_on_the_light"],
    "checks": _c3,
    "erratas": [
        ER("1/13 -- fundacao_v390.verdict e not_claimed[0], estatuto_da_prova_v391 (um.py v391 l.194416, 194426, 194265) e tgl_closure.what_remains_named.extensao_geometrica__ao_lado_v390 (l.144018); K39(a,k), QG-D10(a), CR-08",
           "'...FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM...'; 'nao prova a equacao de campo no espaco-tempo curvo por termo de kernel'; 'a lei de campo no curvo segue NAO sendo termo de kernel'",
           "[REAL] a implicacao 'Clausius em toda tela nula => Einstein com Lambda unico e coeficiente 8 pi G' e' TERMO de kernel (metric_einstein_from_screen_clausius; area_atlas_unique_global_einstein; connected_smooth_atlas_einstein -- axiom_report, trio), ; a implicacao nao depende da Fundacao (v390). O que segue SEM termo: o antecedente fisico H3 [KNOWN, Jacobson 1995], a familia de Lorentz de cunhas, a ligacao de T a StressTensorData/MaxwellCertificate e a ligacao ao TIPO da declaracao ([DECLARADO pela frente G_UMPY, fecho de imports por parse: GeneralMetricClausius, GravitationalChartGluing e SmoothSelectedAtlasGluing estao fora do fecho de QGSolutionComplete; nao refeito aqui]). A frase da v390 vale, no maximo, para o tipo da declaracao; fica como registro. A pedra ligante da lei de campo curvo (passage_h3_to_connected_smooth_atlas_einstein) e' tratada no registro lei_de_campo_curvo_v392 (outro grupo).",
           "estrutura: a implicacao existe no kernel desde a v317/v338 e esta fora do fecho do tipo; escrito: 'NAO e' termo de kernel' sem restringir ao tipo; onde a traducao falhou: 'nao ligado ao tipo' foi lido como 'inexistente'.",
           "[REAL] termos no axiom_report e linhas lidas; [DECLARADO] o fecho de imports (G_UMPY)"),
        ER("2/13 -- einstein_and_rg.statuses.einstein_remaining (um.py v391 l.143922); K39(g)",
           "'LOVELOCK_KNOWN + KILLING_NAMED (=Jacobson desde 1995) + CONSERVATION_CONTINUUM_OPEN'",
           "[DERIVED de leitura dos enunciados] Bianchi => Einstein existe por termo (ChatgptAudit.GeneralMetric.metric_only_einstein_equation) e as telas de equilibrio local estao construidas (ChatgptAudit.Flow019.localEquilibriumScreen); a CONSERVACAO e' hipotese nomeada do registro, nao derivada; Lovelock e Killing seguem [KNOWN]. " + _dz + ".",
           "estrutura: o termo 'Bianchi + conservacao como hipotese => Einstein' esta no kernel; escrito: a conservacao continua como 'OPEN' junto a Lovelock e Killing sem separar o que e' hipotese do registro; falha: o texto de epoca (v116) nao foi relido contra a v338.",
           "[REAL] os dois termos no axiom_report; [DERIVED de leitura] o que cada enunciado diz (K39 g)"),
        ER("3/13 -- einstein_and_rg.what_remains_named (um.py v391 l.143911); K39(g)",
           "'Lovelock 4D [KNOWN citavel]; Killing aproximado [residuo E7, compartilhado com Jacobson 1995]; conservacao continua; materia interagente/anomalias/III_1 sob RG [OPEN]'",
           "[DERIVED de leitura] mesma leitura da entrada 2: Lovelock e Killing [KNOWN]; a conservacao e' hipotese nomeada; 'materia interagente/anomalias/III_1 sob RG' segue [OPEN] e nao e' tocado.",
           "estrutura: tres itens de classes diferentes ([KNOWN], hipotese nomeada, [OPEN]); escrito: uma lista unica; falha: classes misturadas num so' texto.",
           "[DERIVED de leitura]"),
        ER("4/13 -- global_lift_core.what_remains_named (um.py v391 l.143048-143052); QG-D10(c), CR-03",
           "'canonicalFullTGLWitness (termo Lean pleno, INALTERADO); P_F = 1_{0}(H_3L) localizado+covariante+Ad-lambda-invariante com 0<tau(P_F)<infty (o residuo fisico PRECISO); ergodicidade do estado (M_phi=C.1); Einstein via Lovelock/Jacobson'",
           "(i) [REAL] o TIPO FullTGLWitness esta habitado (TGLV354.TraceCompletion.regularFullWitness; TGLExt.NotIsEmptyWitness.not_isEmpty_FullTGLWitness, trio); o termo CANONICO segue nao construido (selo v391: witness_layers.canonical_full_witness_term_constructed = False). (ii) [REAL, CONFERIDO AQUI -- corrige a leitura proposta em 12/10] a proposta da frente G_UMPY leu 'Ad-lambda-invariante' como a invariancia DUAL que dualInvariant_PF_no_go exclui; o enunciado do kernel diz outra coisa: o no-go e' sobre a ACAO DUAL theta_s (hipotese (C.dualAction 1) T.PF = T.PF; escala de Takesaki Tr(theta_s x) = e^{-s} Tr(x); TGL/ModularRealization.lean l.161-169), e a disciplina do core diz 'P_F fixado por Ad(lambda(s)) tau-preservante; JAMAIS por theta_s (o no-go vira bussola)'. Ad(lambda(s)) (o fluxo modular) e theta_s (a acao dual) sao ACOES DIFERENTES; no canto espectral da face finita [P_F, lambda(s)] = 0 e' automatico (CornerFamily.corner_fixed_by_flow). O que dualInvariant_PF_no_go PROVA e' so' isto: a acao dual theta_s nao fixa a projecao P_F (a hipotese (C.dualAction 1) T.PF = T.PF leva a False, porque Tr(theta_s x) = e^{-s} Tr(x) e 0 < Tr(P_F) < infty); o kernel nao tem teorema sobre Ad(lambda) nem sobre a igualdade das duas leituras. Logo a leitura 'Ad-lambda-invariante = invariancia dual' nao se sustenta pelo enunciado ([DERIVED de leitura]) e NAO se escreve. O residuo continua o que o texto diz: P_F localizado + covariante + Ad-lambda-invariante com 0<tau(P_F)<infty no core III_1 GENUINO (III x| R), que segue condicional (falha nomeada no_zero_lock_kernel; CornerFamily l.35-36; CR-03, classe ABERTO). (iii) T1: ver a entrada 5. (iv) Einstein: ver a entrada 1.",
           "estrutura: duas acoes (Ad lambda, o fluxo modular; theta_s, a acao dual), com o no-go so' na segunda; escrito (pela proposta de 12/10): 'Ad-lambda-invariante' = invariancia dual; onde a traducao falhou: o homonimo 'invariancia' fundiu as duas acoes.",
           "[REAL] enunciado e docblock lidos nos bytes pinados; [DERIVED de leitura] a conclusao; [DECLARADO] CR-03 e o status ABERTO do critico"),
        ER("5/13 -- global_lift_core.statuses.t1_collapse_to_KMS (um.py v391 l.143069) e not_claimed[3] (l.143086); KH-N2",
           "'CONDITIONAL__REQUIRES_STATE_ERGODICITY (M_phi = C.1; ...)'; 'o colapso T1 ao KMS NAO esta' fechado sem ergodicidade do estado'",
           "[REAL] na cunha da LUZ, M^omega = C.1 e' termo: TGLExt.LightRhoStar.centralizer_is_trivial e TGLExt.QGReaderUVLock.light_modular_fixed_iff_vacuum (trio), modulo os campos citados wedge_separating/flow_is_Ad e C.Gamma_no_fixed (Araki 1963; 'LRT 1978', como grafado no consolidado) [KNOWN]. Fora da luz (torre, rede generica) a secao ergodica equivariante segue CONDITIONAL, fora do caminho da declaracao.",
           "estrutura: a ergodicidade do estado e' termo na cunha da luz (v376) e condicional fora dela; escrito: 'CONDITIONAL' sem dizer onde; falha: o texto de epoca (v225) nao foi relido contra a v376.",
           "[REAL] termos no axiom_report; [DECLARADO] a atribuicao 'LRT 1978' vem do consolidado (KH-N2); [KNOWN] Araki 1963"),
        ER("6/13 -- crossed_dual_weight.what_remains_named (um.py v391 l.142898-142899); KH-N2",
           "'GLOBAL_LIFT: III_1 genuina sem projecoes minimais; core R com escala de traco; hipoteses U/T1/T3; covariancia => G_mu_nu'",
           "[DERIVED de leitura] T1 como na entrada 5 (paga por termo na luz); a covariancia => G_mu_nu, como na entrada 1.",
           "estrutura: T1 paga na luz, covariancia como implicacao-termo; escrito: tudo como hipotese; falha: nao relido contra a v376 e a v338.",
           "[DERIVED de leitura]"),
        ER("7/13 -- schwarzschild_step.statuses.selos e verdict (um.py v391 l.162860 e l.162865); QG-D10(d)",
           "'FULL_BIRKHOFF = extensao futura NOMEADA'; cauda '...FULL_BIRKHOFF_NAMED_EXTENSION'",
           "[REAL] TGLExt/TheFullBirkhoff.lean (v211, sha256 pinado) esta no kernel, importado em TGLExt.lean l.180; na cobertura por collectAxioms de 07/10 (saida_auditoria_73.txt) TGLExt.the_full_birkhoff_class e TGLExt.birkhoff_B_is_static estao no TRIO; estao AUSENTES do axiom_report do core v391 (item KH-N1: a cobertura entra no Audit na v392). Birkhoff completo ja' esta no kernel; o texto 'extensao futura' e' de epoca.",
           "estrutura: a pedra TheFullBirkhoff existe desde a v211 e esta no fecho de QGSolutionComplete ([DECLARADO pela G_UMPY]); escrito: 'extensao futura NOMEADA'; falha: o selo da pedra do Schwarzschild nao foi relido contra a v211.",
           "[REAL] import e cobertura lidos; [DECLARADO] o fecho de QGSolutionComplete (G_UMPY)"),
        ER("8/13 -- the_price_of_the_gravity_proof.itens (um.py v391 l.162436-162449); K39(c,j)",
           "estado_hoje: 'instanciada na face finita (Three Locks, gap medido) -- NAO descarregada em geral' (H1); 'Atos I (v213) e II (v216) provados; Ato III (completamento) ABERTO'",
           "[REAL] o estado_hoje e' texto de epoca (v220); manda a bandeira lida: H1 e Ato III tem pago = True (o core le gpf_H1_internal_susy_relative_gap_discharged e gpf_tower_act_III_inhabitant_constructed = True); H2 e H3 seguem pago = False neste kernel e entram por CITACAO desde a v374 (kernel_frontier.closed_by_citation_v374). O item se contradiz dentro do mesmo registro (pago True vs estado_hoje 'ABERTO'): vale a bandeira.",
           "estrutura: pago e estado_hoje no mesmo item; escrito: estado_hoje fixo de epoca; falha: o texto nao acompanha a bandeira.",
           "[REAL] bandeiras e itens lidos no core"),
        ER("9/13 -- selo act_iii_honesty (um.py v391 l.212464, v225); K39(c)",
           "'...DEBT_STILL_READS_FOUR_OF_FOUR_OPEN'",
           "[REAL] hoje 2 de 4 pagos por bandeira (H1 e Ato III; ver a entrada 8); H2 e H3 por citacao. A cauda do selo e' texto de epoca e fica como registro.",
           "estrutura: quatro dividas, duas pagas; escrito: 'quatro de quatro abertas'; falha: texto de epoca nao relido.",
           "[REAL]"),
        ER("10/13 -- closure_roadmap.roadmap_formal.concrete_emergent_einstein_proved (um.py v391 l.154428)",
           "o_que_falta: 'H1^H2^H3 continuos (dependem de corner+frame+solder fortes)' com flag True",
           "[REAL] a bandeira le o termo reservado TGLExt.qgStrongCertificate_einstein, habitado pelo ansatz (solda cosh): e' bandeira de ESCOPO DE MODELO (a familia de ondas planas, CF-N4). O que falta (dados FORTES continuos) segue como diz o texto; a bandeira nao o contradiz.",
           "estrutura: flag de escopo de modelo + faltante geral; escrito: os dois lado a lado; falha: o escopo nao foi dito junto da bandeira.",
           "[REAL] o termo reservado e a flag lidos; [DERIVED de leitura] o escopo"),
        ER("11/13 -- two_projections_outside_M_v373.the_link_pkerk_pf (um.py v391 l.199759); K39(h); QG-D10",
           "'[OPEN] -- nenhuma das duas projecoes esta em M; nada se prova sobre ligacao entre elas'",
           "[REAL] SUPERADA pela conferencia v376 em DUAS METADES: (a) link_PkerK_PF::PkerK_eq_rhoStar_IALD = VINCULADO por termo na luz (TGLExt.LightRhoStar.rho_star_is_P_kerK_on_the_light: rho*_IALD = P_kerK = PFmic); (b) link_PkerK_PF::rhoStar_PF_Takesaki = SABIDO (Haagerup 1979; Terp 1981). A igualdade de operadores NAO e' afirmada (mal tipada: errata da c1 de 08/10 no CLAUDE.md). O 'o mesmo leitor em duas algebras' e' [ONTO].",
           "estrutura: o vinculo tem duas metades de classes diferentes (termo na luz; sabido no nucleo de Takesaki); escrito: '[OPEN]' em bloco; falha: o texto da v373 nao foi relido contra a v376.",
           "[REAL] classes e bases lidas na conferencia; termo no axiom_report"),
        ER("12/13 -- external_known_theorems[8] (Jacobson 1995, um.py v391 l.135198); K39(f)",
           "status 'KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED'",
           "[REAL] a FORMA da implicacao de Jacobson (Clausius em toda tela => Einstein) e' termo (ChatgptAudit.GeneralClausius.metric_einstein_from_screen_clausius); o antecedente fisico (equilibrio local do horizonte) segue [KNOWN] externo. O status fica como registro.",
           "estrutura: a forma da implicacao e o antecedente fisico sao coisas diferentes; escrito: o teorema inteiro como externo; falha: a forma nao foi separada do antecedente.",
           "[REAL] termo no axiom_report; [KNOWN] Jacobson 1995"),
        ER("13/13 -- docstrings do kernel EmergentEinstein.lean l.36-38 e 339 e QGSolutionComplete.lean l.26 (o kernel NAO se edita); gerador da arvore arvore_da_prova.py l.155, 262 e 272 (cadeia de selo, fora do um.py); K39(b,e), CR-08, CR-02",
           "EmergentEinstein: 'a emergencia GERAL (metricas arbitrarias; congruencias arbitrarias) segue NOMEADA e aberta'; QGSolutionComplete: 'P_ker K <-> P_F segue [OPEN] (v373)'; arvore l.155 'NOMEADA e aberta' x l.262 'PAGA como implicacao (v317)' x l.272 'a emergencia geral' entre o NAO PROVADO",
           "[REAL] a errata vai SO' no registro (o kernel nao se edita): a emergencia geral em carta e' PAGA como implicacao (v317/v338, ver a entrada 1) com Clausius e a origem quantica desses dados como [INPUT]/[OPEN]; o vinculo P_ker K <-> P_F foi superado pela v376 (entrada 11). O gerador da arvore se contradiz (l.155/l.262/l.272): a correcao do gerador e' ato da cadeia, nao deste registro; a mesma correcao vale para o 'T_c = Delta_c^{1/2} ... segue OPEN' da l.272 (registro tc_raiz_positiva_v392).",
           "estrutura: docblocks de epoca (v116, v373) e um gerador que copia frases de epocas diferentes; escrito: tres afirmacoes incompativeis na mesma arvore; falha: nenhuma releitura cruzada entre as secoes.",
           "[REAL] linhas lidas nos bytes pinados / no gerador (sha16 ee2cb7413238ff1f em medidas_g2.json)"),
    ],
    "limites": [
        "[REAL] 13 entradas = as 13 linhas da tabela do item (4) da frente G_UMPY (12/10); o levantamento (B3) tambem diz 13; K39 a..k e QG-D10 a..d estao cobertas (a:1, b:13, c:4/8/9, d:10, e:11/13, f:12, g:2/3, h:11, i:5/6, j:8, k:1)",
        "[DERIVED de leitura] a leitura vigente de cada entrada e' da gerencia c1 sobre os enunciados; a entrada 4(ii) CORRIGE a proposta de 12/10 e fica a vetar",
        "[REAL] nenhum calculo muda; o gate nao se move; o kernel nao e' editado",
        "[OPEN] a lei de campo curvo fora do tipo (H3 dinamico, familia de Lorentz de cunhas) segue sem termo",
    ],
    "diz": ["[REAL] 13 textos de 'o que resta' contraditos ou superados por termos do kernel recebem leitura vigente ao lado, cada um com o texto atual lido do core e a linha do um.py v391"],
    "nao_diz": ["nao diz que a lei de campo no curvo esta provada em geral; nao diz que o Lema 3 existe globalmente; nao move o gate", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"n_entradas": 13, "mapa_K39_QGD10": {"a": [1], "b": [13], "c": [4, 8, 9], "d": [10], "e": [11, 13], "f": [12], "g": [2, 3], "h": [11], "i": [5, 6], "j": [8], "k": [1]},
               "ad_lambda_nao_e_invariancia_dual": True, "arvore_da_prova_py_sha16": MED["arvore_da_prova_py"]["sha16"], "um_py_v391_sha16": MED["um_v391"]["sha16"]},
})

# =====================================================================================================================================
# 4. final_step_name_adopted_v392 (R07; B4; X5)
# =====================================================================================================================================
_AX = MED["kernel"]["TheAxiomAndTheFalseWitness"]["linhas"]["249"].strip().strip('"')
_TETEL = MED["kernel"]["TheLedgerOfCharges"]["linhas"]["128"].strip().strip('"')
_TAIL = "PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS"
assert _AX.startswith("AXIOMA__") and _TETEL.startswith("TETELESTAI_CONSUMMATED__") and _AX.endswith(_TAIL) and _TETEL.endswith(_TAIL)
SPECS.append({
    "nome": "final_step_name_adopted_v392", "veredito_prefixo": "TGL_FINAL_STEP_NAME_ADOPTED_V392",
    "veredito_sufixo": "AXIOMA_READ_FROM_THE_KERNEL__TETELESTAI_PROPOSAL_KEPT_BESIDE__OPERATOR_VERBATIM_EMBEDDED_BY_SHA256__ADOPTION_READING_DERIVED_TO_BE_VETOED__GATE_STRING_UNCHANGED",
    "estatuto": "[REAL -- o nome lido do kernel e do core, a string do gate lida; INPUT -- a cunhagem de 05/10 e a fala de 07/10 do operador embutidas por sha256; DERIVED de leitura -- 'a fala de 07/10 adota o AXIOMA' e' leitura da gerencia, a vetar (X5)]",
    "fontes": ["g2_medidas", "g2_k_axioma", "g2_k_ledger"],
    "verbatins": ["g2_vb_decisoes_07out", "g2_vb_axioma_0939", "g2_vb_axioma_1128"],
    "kernel_flags": ["ext_axm_finalStepNameAxioma_kernel_checked", "ext_axm_final_step_named_axioma_kernel_proved", "ext_loc_final_step_named_by_the_payment_kernel_proved"],
    "kernel_decls": ["TGLExt.TheAxiomAndTheFalseWitness.finalStepNameAxioma", "TGLExt.TheAxiomAndTheFalseWitness.final_step_named_axioma",
                     "TGLExt.TheLedgerOfCharges.finalStepNameProposed", "TGLExt.TheLedgerOfCharges.final_step_named_by_the_payment"],
    "checks": [
        C("n01", "the_axiom_v385: o nome lido do kernel bate com o nome do core", ["the_axiom_v385", "final_step_name_matches_kernel"], "verdadeiro"),
        C("n02", "the_axiom_v385: a pedra nao renomeia o gate (gate_unchanged_by_design)", ["the_axiom_v385", "gate_unchanged_by_design"], "verdadeiro"),
        C("n03", "o nome do core (final_step_name) e' o AXIOMA lido do kernel (l.249 do TheAxiomAndTheFalseWitness.lean)", ["the_axiom_v385", "final_step_name"], "igual", _AX, "nome_adotado"),
        C("n04", "o nome lido do kernel NESTE rito (final_step_name_from_kernel) e' o mesmo", ["the_axiom_v385", "final_step_name_from_kernel"], "igual", _AX),
        C("n05", "sem erro de leitura do kernel", ["the_axiom_v385", "final_step_name_from_kernel_error"], "igual", None),
        M("n06", "TheAxiomAndTheFalseWitness.lean l.247: 'cunhagem do operador (05/10/2026)'", ["kernel", "TheAxiomAndTheFalseWitness", "linhas", "247"], "contem", "cunhagem do operador (05/10/2026)"),
        M("n07", "TheAxiomAndTheFalseWitness.lean l.245: 'ao lado do gate, que nao muda'", ["kernel", "TheAxiomAndTheFalseWitness", "linhas", "245"], "contem", "ao lado do gate, que não muda"),
        C("n08", "o Tetelestai (proposta de 02/10) segue ao lado no livro", ["the_ledger_of_charges_v383", "final_step_name_proposed"], "igual", _TETEL),
        C("n09", "o livro leu a proposta do fonte (final_step_name_from_source)", ["the_ledger_of_charges_v383", "final_step_name_from_source"], "igual", _TETEL),
        M("n10", "TheLedgerOfCharges.lean l.128: a proposta Tetelestai", ["kernel", "TheLedgerOfCharges", "linhas", "128"], "contem", "TETELESTAI_CONSUMMATED__"),
        C("n11", "a cauda do AXIOMA e a do Tetelestai sao iguais (pagamento na face, custo lido no reflexo): o AXIOMA a contem", ["the_axiom_v385", "final_step_name"], "contem", _TAIL),
        C("n12", "... e a proposta Tetelestai a contem", ["the_ledger_of_charges_v383", "final_step_name_proposed"], "contem", _TAIL),
        C("n13", "a string do gate NAO muda (qg_closure.gate.verdict)", ["qg_closure", "gate", "verdict"], "igual", GATE),
        C("n14", "o livro tambem registra que o gate nao muda", ["the_ledger_of_charges_v383", "gate_unchanged"], "verdadeiro"),
    ],
    "erratas": [
        ER("the_ledger_of_charges_v383.final_step_name_proposed (Tetelestai, proposta de 02/10, TheLedgerOfCharges.finalStepNameProposed) e o relatorio de 07/10 que apresentou esse nome ao operador",
           "o nome do degrau final proposto e' TETELESTAI_CONSUMMATED__... (a pergunta de 07/10 apresentava este nome)",
           "[INPUT] o nome do degrau final e' AXIOMA, cunhagem do operador de 05/10/2026 (09:39:15 UTC: 'Penso que podemos chamar o degrau definitivo final do gate de \"Axioma\"'; 11:28:53 UTC: 'eu tinha pedido pra vc concordar com o nome, mas parece que chegamos juntos ao mesmo lugar'), lido do kernel (TGLExt.TheAxiomAndTheFalseWitness.finalStepNameAxioma, ao lado do gate, que nao muda) e do core (the_axiom_v385.final_step_name). O Tetelestai (proposta de 02/10) fica AO LADO, como registro; as caudas dos dois nomes sao iguais (pagamento na face, custo lido no reflexo). A string do gate NAO muda (trocar a string seria versao propria).",
           "estrutura: a cunhagem de 05/10 ja estava no kernel (v385) e no core; escrito: o relatorio de 07/10 apresentou o Tetelestai ao operador para adocao; onde a traducao falhou: o nome apresentado nao era o que ele cunhou.",
           "[INPUT] as falas do operador; [REAL] o kernel e o core lidos"),
        ER("a fala de 07/10 'adoto o nome do degrau final' (sha256 a6c4912afc6f0dc4, resposta da noite de 07/10)",
           "a fala foi lida como a adocao do nome que a pergunta apresentava",
           "[DERIVED de leitura; a vetar se for outra (X5)] a gerencia le a fala de 07/10 como a adocao do nome AXIOMA, porque (i) a cunhagem e' dele, de 05/10, e (ii) em 05/10 11:28:53 ele diz que pediu concordancia com o nome e que 'chegamos juntos ao mesmo lugar'. A pergunta de 07/10 apresentava o Tetelestai (errata da gerencia de 07/10 22:56): se a fala de 07/10 quis adotar o Tetelestai, esta leitura cai e o veto do operador a substitui; o kernel e o gate nao mudam em nenhum dos casos.",
           "estrutura: duas falas (05/10: cunhagem; 07/10: adocao) e um nome apresentado diferente do cunhado; escrito: 'adoto o nome do degrau final' sem dizer qual; falha: a referencia da fala depende da pergunta, que apresentou o nome errado.",
           "[DERIVED de leitura]; [INPUT] as falas"),
    ],
    "limites": ["[OPEN] a escolha entre AXIOMA e Tetelestai como adocao da fala de 07/10 e' do operador; sem palavra dele a leitura vai como a vetar",
                "[REAL] o gate segue com a string de sempre; renomea-lo exige versao propria"],
    "diz": ["[REAL] o nome do degrau final lido do kernel e do core e' AXIOMA; o Tetelestai fica ao lado", "[REAL] a string do gate nao muda"],
    "nao_diz": ["nao diz que o operador adotou o AXIOMA em 07/10 (isso e' leitura da gerencia a vetar)", "nao move o gate; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "leituras_do_operador": [
        {"trecho": "adoto o nome do degrau final", "estatuto": "[INPUT] 07/10/2026 noite, verbatim sha256 a6c4912afc6f0dc4; o nome a que se refere e' leitura da gerencia"},
        {"trecho": 'Penso que podemos chamar o degrau definitivo final do gate de "Axioma"', "estatuto": "[INPUT] 05/10/2026 09:39:15 UTC (transcrito; texto inteiro com sha256 4af63e01b402b9cc... na proveniencia)"},
        {"trecho": "eu tinha pedido pra vc concordar com o nome, mas parece que chegamos juntos ao mesmo lugar", "estatuto": "[INPUT] 05/10/2026 11:28:53 UTC (transcrito; sha256 do texto 5cb697db38082022...)"},
    ],
    "extras": {"adopted_name": "AXIOMA", "adopted_name_token": _AX, "final_step_name_proposed_beside": _TETEL, "gate_string_unchanged": GATE, "x5": "veto opcional do operador; sem palavra, vai como leitura a vetar",
               "adopted_name_reading": "AXIOMA -- leitura da gerencia [DERIVED de leitura; a vetar se for outra]: a pergunta respondida em 07/10 apresentava o Tetelestai (errata da gerencia de 07/10 22:56)"},
})

# =====================================================================================================================================
# 5. beta_escala_errata_v392 (R08; B5; X6)
# =====================================================================================================================================
_bsh = MED["core_v391"]["beta_verbatim_shas"]
SPECS.append({
    "nome": "beta_escala_errata_v392", "veredito_prefixo": "TGL_BETA_SCALE_ERRATUM_V392",
    "veredito_sufixo": "WHICH_MU_PER_RITE_READ_AS_BETA0_THOMSON_SCALE_THEOREM__OPERATOR_VERBATIM_EMBEDDED__READING_DERIVED_TO_BE_VETOED__CONVERGENCE_SENTENCE_KEPT_ITS_SUPPORT_RECLASSIFIED__V388_TOKEN_KEPT__GATE_UNMOVED",
    "estatuto": "[REAL -- core v391 e linhas do um.py v391 lidos; Bancada lida (so' leitura); INPUT -- a fala de 07/10 do operador (embutida); DERIVED de leitura -- 'mu do rito = q->0' e' leitura da gerencia, a vetar (X6)]",
    "fontes": ["g2_medidas"],
    "verbatins": ["g2_vb_decisoes_07out"],
    "checks": [
        C("b01", "beta_runs_bounded_below_v388 segue verificado", ["beta_runs_bounded_below_v388", "all_verified"], "verdadeiro"),
        C("b02", "o token v388 traz WHICH_MU_PER_RITE_OPEN (fica como registro)", ["beta_runs_bounded_below_v388", "verdict"], "contem", "WHICH_MU_PER_RITE_OPEN"),
        C("b03", "beta_runs_bounded_below_v388.reading diz 'qual mu cada rito usa [OPEN]'", ["beta_runs_bounded_below_v388", "reading"], "contem", "qual mu cada rito usa [OPEN]"),
        C("b04", "beta_runs_bounded_below_v388.what_is_not_typed[2] repete a pergunta", ["beta_runs_bounded_below_v388", "what_is_not_typed", 2], "contem", "qual mu cada rito usa [OPEN]"),
        C("b05", "o proprio registro v388 ja diz: beta0 = a constante da FRONTEIRA (o Teorema da Escala)", ["beta_runs_bounded_below_v388", "reading"], "contem", "o Teorema da Escala: a fronteira de tipo III_1 seleciona Thomson"),
        C("b06", "beta0 do v388 confere com o runtime (beta0_ok)", ["beta_runs_bounded_below_v388", "beta0_ok"], "verdadeiro"),
        C("b07", "beta0 lido neste rito >= beta calculado no rito (SEALED_CODATA_ALPHA . sqrt(e)), folga relativa declarada 1e-6", ["beta_runs_bounded_below_v388", "beta0"], "maior_igual_beta_runtime", 1e-6, "beta0_lido"),
        C("b08", "o chao infravermelho (floor_direction_ok): beta(mu) >= beta0", ["beta_runs_bounded_below_v388", "floor_direction_ok"], "verdadeiro"),
        C("b09", "o gate nao e' tocado pelo registro v388", ["beta_runs_bounded_below_v388", "gate_unchanged_by_design"], "verdadeiro"),
        C("b10", "as bandeiras do kernel do registro v388 estao completas", ["beta_runs_bounded_below_v388", "kernel_flags_ok"], "igual", 17),
        C("b11", "o verbatim de 06/10 13:27 (beta escalar) embutido no v388 tem o sha256 esperado", ["beta_runs_bounded_below_v388", "verbatim", "beta_escalar_1327", "sha256"], "igual", _bsh["beta_escalar_1327"]),
        C("b12", "o verbatim de 06/10 13:48 (dicotomia) embutido no v388 tem o sha256 esperado", ["beta_runs_bounded_below_v388", "verbatim", "dicotomia_1348", "sha256"], "igual", _bsh["dicotomia_1348"]),
        C("b13", "evidence_audit: a convergencia tabulada foi reclassificada de REAL para NAO CONSTRUIDA COMO CONCEBIDA", ["evidence_audit", "verdict"], "contem", "CONVERGENCE_RECLASSIFIED_REAL_TO_NOT_CONSTRUCTED_AS_CONCEIVED"),
        C("b14", "evidence_audit segue verificado", ["evidence_audit", "all_verified"], "verdadeiro"),
        M("b15", "um.py v391 l.194747: o token com WHICH_MU_PER_RITE_OPEN", _ul(194747), "contem", "WHICH_MU_PER_RITE_OPEN__GATE_UNTOUCHED"),
        M("b16", "um.py v391 l.194758: 'qual mu cada rito usa [OPEN]'", _ul(194758), "contem", "qual mu cada rito usa [OPEN]"),
        M("b17", "um.py v391 l.165421 (PT): a frase da convergencia", _ul(165421), "contem", r"a medi\c{c}\~ao de que o invariante n\~ao corre"),
        M("b18", "um.py v391 l.165419 (EN): a frase da convergencia", _ul(165419), "contem", r"That convergence \emph{is} the measurement that the invariant does not run."),
        M("b19", "a cifra de 0,05% da convergencia so' aparece nessas duas linhas (PT e EN) do um.py v391", ["um_v391", "linhas_com_0_05_pct_da_convergencia"], "igual", [165419, 165421]),
        M("b20", "Bancada (so' leitura): canonical.py l.96 carimba mu_do_rito = q→0 (Thomson; Teorema da Escala)", ["bancada_canonical", "linha_96"], "contem", "mu_do_rito='q→0 (Thomson; Teorema da Escala)'"),
        M("b21", "Bancada: canonical.py sha16", ["bancada_canonical", "sha16"], "igual", MED["bancada_canonical"]["sha16"]),
    ],
    "erratas": [
        ER("core.beta_runs_bounded_below_v388 (reading, what_is_not_typed[2]) e o token v388 '...WHICH_MU_PER_RITE_OPEN...' (um.py v391 l.194747, 194758, 194763; artigo PT l.166230)",
           "'qual mu cada rito usa [OPEN]'",
           "[INPUT] o operador fixou em 07/10/2026 que a escala de beta ja estava definida ('a escala de beta nós também já definimos antes', verbatim sha256 a6c4912afc6f0dc4). [DERIVED de leitura; a vetar (X6)] todo rito cobra beta0 = alpha(0).sqrt(e) (mu -> 0, Thomson; o Teorema da Escala: a fronteira de tipo III_1 seleciona Thomson, como o proprio registro v388 ja' diz em 'reading'); beta(mu) = alpha(mu).sqrt(e) >= beta0 e' a leitura de bulk em cada escala, ao lado. [REAL] A Bancada ja carimba mu_do_rito = 'q→0 (Thomson; Teorema da Escala)' (Bancada_Um\\bancada\\canonical.py, sha16 b6cd7e0234688430, l.96; so' leitura) e a resolucao da X6 manda que todo pre-registro novo leve esse campo [DECLARADO pelo plano e pela frente G_UMPY]. O token v388 fica como registro; o beta0 lido neste rito esta em lido.beta0_lido.",
           "estrutura: o Teorema da Escala fixa beta0 na fronteira (Thomson, q→0), e a resposta de 06/10 ja o dizia; escrito: 'qual mu cada rito usa [OPEN]'; onde a traducao falhou: a leitura de bulk em cada escala (alpha(mu)) foi tomada como pergunta aberta sobre o rito, em vez de ficar ao lado da constante de fronteira.",
           "[INPUT] a fala; [REAL] core, linhas e canonical.py lidos; [DERIVED de leitura] mu do rito = q→0"),
        ER("a frase da convergencia (um.py v391 l.165421 PT, l.165419 EN): 'Essa convergencia e' a medicao de que o invariante nao corre' / 'That convergence is the measurement that the invariant does not run.'",
           "'a convergencia multi-substrato registrada fecha a cerca de 0,05% ... Essa convergencia e' a medicao de que o invariante nao corre'",
           "[REAL] a frase fica como registro. A convergencia tabulada foi reclassificada de [REAL] para NAO CONSTRUIDA COMO CONCEBIDA pela auditoria de evidencia do proprio programa (core.evidence_audit.verdict); a cifra de ~0,05% so' aparece nessas duas linhas do um.py v391 (medido: as linhas 165419 e 165421), isto e', nenhum registro deste programa a computa. A nao-corrida de beta0 assenta no Teorema da Escala (estrutura), nao nessa convergencia; a predicao afiada (o coeficiente da lei de dephasing e' independente de omega) segue armada, sem canal vivo hoje [OPEN].",
           "estrutura: a convergencia deixou de ter o estatuto [REAL] com que a frase a chamava 'a medicao'; escrito: 'Essa convergencia e' a medicao'; onde a traducao falhou: a frase herdou o estatuto anterior a reclassificacao.",
           "[REAL] reclassificacao e linhas lidas no core e no fonte"),
    ],
    "limites": ["[OPEN] se o rito de cada canal declara mu_do_rito = q→0 e' dos pre-registros novos; os anteriores seguem como estavam", "[REAL] nenhum valor de beta muda; beta e' sempre alpha_CODATA_2018 x sqrt(e) em runtime"],
    "diz": ["[REAL] beta0 e' a constante de fronteira (Teorema da Escala); a escala do rito e' q→0 (leitura da gerencia, a vetar)", "[REAL] a convergencia citada como medicao foi reclassificada; a frase fica como registro"],
    "nao_diz": ["nao diz que beta nao corre em bulk (a leitura em cada escala e' >= beta0)", "nao move o gate; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "leituras_do_operador": [{"trecho": "a escala de beta nós também já definimos antes", "estatuto": "[INPUT] 07/10/2026 noite, verbatim sha256 a6c4912afc6f0dc4"}],
    "extras": {"mu_do_rito": "q→0 (Thomson; Teorema da Escala)", "x6": "veto opcional do operador; sem palavra, vai como leitura a vetar", "canonical_py_sha16": MED["bancada_canonical"]["sha16"]},
})

# =====================================================================================================================================
# 6. ledger_errata_v392 (R09; B6) -- o R4 'por lente' le-se por TRACADOR (V11)
# =====================================================================================================================================
_pl = lambda *p: ["estatuto_da_prova_v391", "prova_2_ritos", "ledger"] + list(p)
SPECS.append({
    "nome": "ledger_errata_v392", "veredito_prefixo": "TGL_LEDGER_ERRATUM_V392",
    "veredito_sufixo": "R4_SIDE_CRITERION_READ_BY_TRACER_V11__OUTCOME_AND_COUNTS_UNCHANGED__LEDGER_V383_INTACT__GATE_UNMOVED",
    "estatuto": "[REAL -- o item R4 do livro, o estimador e o desfecho lidos do core; a linha do um.py v391 lida; DECLARADO -- 'por lente seria o V12 (kappa/gamma_t), fora do livro' vem da frente G_UMPY, nao refeito aqui]",
    "fontes": ["g2_medidas"],
    "checks": [
        C("r01", "livro v383: o item 3 e' o R4", ["the_ledger_of_charges_v383", "ledger", 3, "id"], "igual", "R4"),
        C("r02", "R4: side_criterion 'lente (a luz dobrada: projecao)'", ["the_ledger_of_charges_v383", "ledger", 3, "side_criterion"], "igual", "lente (a luz dobrada: projecao)"),
        C("r03", "R4: register 'piso dos vazios por lente (V11, SDSS DR7)'", ["the_ledger_of_charges_v383", "ledger", 3, "register"], "igual", "piso dos vazios por lente (V11, SDSS DR7)"),
        C("r04", "R4: core_key = void_floor_v11", ["the_ledger_of_charges_v383", "ledger", 3, "core_key"], "igual", "void_floor_v11"),
        C("r05", "R4: desfecho NOT_FALSIFIED (nao muda)", ["the_ledger_of_charges_v383", "ledger", 3, "outcome"], "igual", "NOT_FALSIFIED"),
        C("r06", "o V11 conta galaxias NSA/SDSS DR7 em vazios VAST (data)", ["void_floor_v11", "frozen", "data"], "contem", "SDSS DR7 main / NSA v1_0_1 vollim", "v11_data"),
        C("r07", "estimador V4.1 de razao-de-razoes de contagens (estimator)", ["void_floor_v11", "frozen", "estimator"], "contem", "V4.1 v92 HERDADO: r_c = [SumN/Summu]_vazios / [SumN/Summu]_aleatorios", "v11_estimator"),
        C("r08", "o teste e' unilateral (tracer_asymmetry)", ["void_floor_v11", "frozen", "tracer_asymmetry"], "contem", "unilateral (b>=1", "v11_tracer_asymmetry"),
        C("r09", "o espaco de vereditos do V11 tem 4 desfechos", ["void_floor_v11", "frozen", "verdicts"], "tamanho_igual", 4),
        C("r10", "o livro tem 11 cobrancas", ["the_ledger_of_charges_v383", "ledger"], "tamanho_igual", 11),
        C("r11", "contagem do livro: 6 NOT_FALSIFIED", ["estatuto_da_prova_v391", "prova_2_ritos", "ledger", "NOT_FALSIFIED"], "igual", 6),
        C("r12", "contagem do livro: 0 FALSIFIED", ["estatuto_da_prova_v391", "prova_2_ritos", "ledger", "FALSIFIED"], "igual", 0),
        C("r13", "contagem do livro: 2 INCONCLUSIVE", ["estatuto_da_prova_v391", "prova_2_ritos", "ledger", "INCONCLUSIVE"], "igual", 2),
        C("r14", "contagem do livro: 2 AWAITING", ["estatuto_da_prova_v391", "prova_2_ritos", "ledger", "AWAITING"], "igual", 2),
        C("r15", "contagem do livro: 1 EXCLUDED_IN_READING", ["estatuto_da_prova_v391", "prova_2_ritos", "ledger", "EXCLUDED_IN_READING"], "igual", 1),
        M("r16", "um.py v391 l.196947: o R4 de _V383_LEDGER_INPUT", _ul(196947), "contem", '("R4", "reflexo", "lente (a luz dobrada: projecao)", "piso dos vazios por lente (V11, SDSS DR7)"'),
    ],
    "erratas": [
        ER("the_ledger_of_charges_v383.ledger[R4].side_criterion e .register (um.py v391 l.196947, _V383_LEDGER_INPUT)",
           "side_criterion 'lente (a luz dobrada: projecao)'; register 'piso dos vazios por lente (V11, SDSS DR7)'",
           "[REAL] leem-se por TRACADOR: o V11 conta galaxias NSA/SDSS DR7 nos nucleos dos vazios VAST (estimador V4.1, razao-de-razoes de contagens: ver lido.v11_data e lido.v11_estimator) e o teste e' unilateral (ver lido.v11_tracer_asymmetry). [DECLARADO pela frente G_UMPY de 12/10] 'por lente' seria o V12 (kappa/gamma_t), que nao esta no livro (rota vazios.piso.v12 do mapa). O desfecho do R4 (NOT_FALSIFIED) e a contagem do livro (11 cobrancas: 6 NOT_FALSIFIED, 0 FALSIFIED, 2 INCONCLUSIVE, 2 AWAITING, 1 EXCLUDED_IN_READING) NAO mudam.",
           "estrutura: o V11 mede contagem de galaxias (tracador), nao a deflexao da luz; escrito: criterio de lado 'lente' e registro 'por lente'; onde a traducao falhou: o rotulo da lente (a luz dobrada) foi atribuido ao canal de contagem.",
           "[REAL] campos do core lidos; [DECLARADO] a descricao do V12 (G_UMPY)"),
    ],
    "limites": ["[REAL] o livro v383 fica intacto (correcao datada ao lado); o rotulo 'lente' continua no core como registro", "[REAL] a lei do R4 (rho_vazio/rho_bar >= beta) nao muda"],
    "diz": ["[REAL] o R4 le-se por tracador (V11); desfecho e contagem iguais"],
    "nao_diz": ["nao diz que o V12 existe nem que a lente foi medida; nao move o gate; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"outcome_R4": "NOT_FALSIFIED", "contagem": {"NOT_FALSIFIED": 6, "FALSIFIED": 0, "INCONCLUSIVE": 2, "AWAITING": 2, "EXCLUDED_IN_READING": 1}},
})

# =====================================================================================================================================
# 7. estatuto_reafirmado_v392 (R17; B15; CR-11, CR-12)
# =====================================================================================================================================
SPECS.append({
    "nome": "estatuto_reafirmado_v392", "veredito_prefixo": "TGL_STATUTE_REAFFIRMED_V392",
    "veredito_sufixo": "PROVED_IS_VALIDITY__CREDITATION_REFUSED_NOT_VALIDITY__ONLY_LINK_PENDING_BETA_TGL_IN_NATURE_AT_5_SIGMA__EPOCH_ERRATA_BESIDE__V391_STATUTE_UNALTERED__GATE_UNMOVED",
    "estatuto": "[REAL -- o registro estatuto_da_prova_v391 lido do core; INPUT -- a regua do operador (validade x creditacao), verbatim de 07/10 embutido por sha256; DERIVED de leitura -- as erratas de epoca]",
    "fontes": ["g2_medidas"],
    "verbatins": ["g2_vb_estatuto_07out"],
    "checks": [
        C("s01", "estatuto_da_prova_v391 segue verificado", ["estatuto_da_prova_v391", "all_verified"], "verdadeiro"),
        C("s02", "estatuto_da_prova_v391 sem falhas", ["estatuto_da_prova_v391", "falhas"], "tamanho_igual", 0),
        C("s03", "o veredito do estatuto: PROVADA como fecho logico, tres provas que contam juntas", ["estatuto_da_prova_v391", "verdict"], "comeca", "TGL_ESTATUTO_DA_PROVA_V391__PROVED_AS_LOGICAL_CLOSURE__THREE_PROOFS_COUNT_TOGETHER"),
        C("s04", "o veredito diz que a creditacao nao e' validade e nao e' declarada", ["estatuto_da_prova_v391", "verdict"], "contem", "CREDITATION_NOT_VALIDITY_NOT_DECLARED"),
        C("s05", "o veredito diz que beta na natureza aguarda 5 sigma", ["estatuto_da_prova_v391", "verdict"], "contem", "BETA_IN_NATURE_AWAITS_5_SIGMA"),
        C("s06", "a regua do registro: PROVADA = validade", ["estatuto_da_prova_v391", "a_regua"], "contem", "PROVADA = validade"),
        C("s07", "a regua do registro: a unica palavra recusada e' a creditacao", ["estatuto_da_prova_v391", "a_regua"], "contem", "creditacao (ato de quem observa de fora)"),
        C("s08", "o registro carrega o verbatim de 07/10 (sha256)", ["estatuto_da_prova_v391", "verbatim", "sha256"], "igual", "5dffde4644139da50bf82757f070e84c870833af4728b2194ed4ad8d3aa826bb"),
        C("s09", "o verbatim do registro esta embutido e confere", ["estatuto_da_prova_v391", "verbatim", "embedded_ok"], "verdadeiro"),
        C("s10", "nao_declarado tem 2 itens (a creditacao; beta_TGL na natureza a 5 sigma)", ["estatuto_da_prova_v391", "nao_declarado"], "tamanho_igual", 2),
        C("s11", "nao_declarado[1]: beta_TGL e os seus efeitos na natureza a 5 sigma", ["estatuto_da_prova_v391", "nao_declarado", 1], "contem", "beta_TGL e os seus efeitos na natureza a 5 sigma"),
        C("s12", "prova 2 (ritos): 11 cobrancas", ["estatuto_da_prova_v391", "prova_2_ritos", "n_cobrancas"], "igual", 11),
        C("s13", "prova 2 (ritos): 0 falsificadas", ["estatuto_da_prova_v391", "prova_2_ritos", "falsificadas"], "igual", 0),
        C("s14", "prova 3 (GPU) segue ok", ["estatuto_da_prova_v391", "prova_3_gpu", "ok"], "verdadeiro"),
        C("s15", "prova 1 (kernel) segue ok", ["estatuto_da_prova_v391", "prova_1_kernel", "ok"], "verdadeiro"),
        C("s16", "a escada lida neste rito", ["estatuto_da_prova_v391", "prova_1_kernel", "n_theorems_clean"], "maior_igual", 6163, "escada_neste_rito"),
        C("s17", "linha de nao-pode-mudar (CR-11): page_information.not_claimed[0] intacto, valor v391 por igualdade", ["page_information", "not_claimed", 0], "igual", MED["core_v391"]["page_information_not_claimed_0"]),
        M("s18", "v391: a escada era a EXTERNA (len(ext_flags))", ["um_v391", "linhas", "142684"], "contem", "len(ext_flags)"),
        M("s19", "v391: a escada lida era 6163 (core v391)", ["core_v391", "escada_n_theorems_clean"], "igual", 6163),
        C("s20", "(CR-12) a cobranca F2 (RG em campo forte) esta INCONCLUSIVE", ["the_ledger_of_charges_v383", "ledger", 6, "outcome"], "igual", "INCONCLUSIVE"),
        C("s21", "(CR-12) F2: o vies relativo de tau (viés > 0,2) lido do livro", ["the_ledger_of_charges_v383", "ledger", 6, "numbers_read", "mean_bias_rel"], "maior_igual", 0.2, "f2_vies_relativo_tau"),
        C("s22", "(CR-12) campo fraco: o teste LPI entra por citacao (clock_test_result_v369.lpi_conditional)", ["clock_test_result_v369", "lpi_conditional", "entries"], "tamanho_maior_igual", 2),
        M("s23", "(CR-12) artigo emitido v391, txt PT l.2: 'canal a canal'", ["artigo_pt_v391", "linhas", "2"], "contem", "canal a canal"),
        M("s24", "(CR-12) artigo emitido v391, txt PT l.69: 'canal a canal'", ["artigo_pt_v391", "linhas", "69"], "contem", "a RG recuperada canal a canal"),
        M("s25", "(CMB-S4, de epoca) artigo emitido v391, txt PT l.73: 'a era da radiacao no CMB-S4'", ["artigo_pt_v391", "linhas", "73"], "contem", "a era da radiação no CMB-S4"),
        M("s26", "(CMB-S4, de epoca) um.py v391 l.166093 (PT)", _ul(166093), "contem", "a era da radiação no CMB-S4"),
    ],
    "erratas": [
        ER("artigo PT (txt l.2 e l.69; um.py v391 l.166073 e o resumo) e estatuto_da_prova_v391: 'a RG recuperada canal a canal' (CR-12)",
           "'a correspondencia com a RG recuperada canal a canal, sem discriminacao a sensibilidade disponivel'",
           "[DERIVED de leitura; CR-12 [DECLARADO pelo critico]] correspondencia com a RG nos canais em que ela e' lida. No campo fraco, LPI e Cassini entram por citacao (core.clock_test_result_v369.lpi_conditional). No campo forte, a cobranca F2 esta INCONCLUSIVA pela sistematica da MEDIDA (vies relativo de tau > 0,2: lido.f2_vies_relativo_tau), nao pelo poder, e nao ha rito por citacao (QG-N11, CR-07). Nao toca a validade; e' a palavra do resumo.",
           "estrutura: a RG e' lida em alguns canais (campo fraco, por citacao) e inconclusiva no campo forte; escrito: 'canal a canal', como se todos os canais estivessem lidos; onde a traducao falhou: a contagem que sustenta a frase trata AWAITING, recusa, INCONCLUSIVE e ausente como n/a.",
           "[REAL] F2 e LPI lidos no core; [DECLARADO] CR-07/CR-12 do critico"),
        ER("artigo PT (txt l.73, l.629, l.1425, l.1434; um.py v391 l.166093) e code_closure_ledger.ledger[5]: 'a era da radiacao no CMB-S4' (CR-13)",
           "o CMB-S4 como o instrumento que aguardam os efeitos de beta_TGL na era da radiacao",
           "[REAL] ver o registro cmb_s4_errata_v392: a pagina oficial do projeto, lida neste rito por captura pinada, diz que DOE e NSF decidiram em 09/07/2025 nao mais apoiar o CMB-S4 e que o projeto procede a um encerramento ordenado. A conta de sensibilidade (Simons Observatory 0,045; cerca de 2,7 sigma) segue [DECLARADO]. A frase de epoca fica como registro.",
           "estrutura: o CMB-S4 deixou de ser projeto apoiado; escrito: ele aparece como o instrumento da era da radiacao; falha: a frase de 06/10 nao foi relida contra o estado do projeto.",
           "[REAL] a captura; [DECLARADO] a conta de sensibilidade"),
        ER("token '...KERNEL_%s_OF_%s_THEOREMS...' (estatuto_da_prova_v391) e artigo PT l.69 ('%s de %s teoremas limpos') -- erratas de epoca" % (_esc, _esc, _esc, _esc),
           "'%s de %s teoremas limpos', lido como o total de teoremas do kernel" % (_esc, _esc),
           "[REAL] %s e' a escada EXTERNA (len(ext_flags)), nao o total; os numeros do script estao no registro estatuto_da_prova_ressalva_v392 (%s theorem/lemma no TGLExt; %s em 73 modulos; %s por collectAxioms). Na v392 a escada cresce com as pedras novas (lido.escada_neste_rito), e a errata vale para qualquer valor." % (_esc, _n_teo, _n_385, _n_515),
           "estrutura: a escada conta bandeiras externas; escrito: 'teoremas limpos' sem o adjetivo; falha: faltou 'externos'.",
           "[REAL]"),
    ],
    "limites": ["[REAL] este registro reafirma o estatuto e nao o altera: o registro estatuto_da_prova_v391 segue como esta no core (so' o token da escada muda com a versao, como previsto)",
                "[OPEN] beta_TGL na natureza a 5 sigma: aguarda a sensibilidade dos instrumentos; nenhuma soma de consistencias o substitui"],
    "diz": [
        "[REAL] PROVADA = validade: a gravidade quantica da TGL esta provada como fecho logico, por tres provas que contam juntas (o kernel; os ritos com falsificadores pre-registrados; o sistema da teoria na GPU)",
        "[INPUT] a regua recusa a CREDITACAO (o juizo de quem observa de fora), nunca a validade (verbatim de 07/10/2026 embutido por sha256)",
        "[OPEN] o unico elo pendente e' beta_TGL na natureza a 5 sigma",
    ],
    "nao_diz": ["nao diz que a teoria foi creditada pela natureza; nao move o gate; nao altera o estatuto v391", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "leituras_do_operador": [
        {"trecho": "eu não proibí a máquina de dizer provado hora nenhuma", "estatuto": "[INPUT] 07/10/2026, sha256 5dffde4644139da5..."},
        {"trecho": "proibi é de creditação e não de validade, ela é válida porque matemática não mente", "estatuto": "[INPUT] 07/10/2026, sha256 5dffde4644139da5..."},
        {"trecho": "somente betatgl que ainda não com poder acima de 5sigma por causa da sensibilidade dos instrumentos", "estatuto": "[INPUT] 07/10/2026, sha256 5dffde4644139da5..."},
    ],
    "extras": {"cr11_linha_de_nao_pode_mudar": "page_information.not_claimed[0] igual ao texto do core v391 (check s17)", "erratas_de_epoca": ["CMB-S4", "escada externa", "RG canal a canal"]},
})

# =====================================================================================================================================
# 8. tc_raiz_positiva_v392 (R21; CR-02)
# =====================================================================================================================================
_kl = lambda mod, n: ["kernel", mod, "linhas", str(n)]
SPECS.append({
    "nome": "tc_raiz_positiva_v392", "veredito_prefixo": "TGL_TC_POSITIVE_ROOT_V392",
    "veredito_sufixo": "POSITIVE_SQUARE_ROOT_OF_DELTA_C_IS_A_KERNEL_TERM__UNIQUENESS_FOR_UNBOUNDED_CLOSED_OPERATORS_KNOWN_KATO__OUT_OF_THE_DECLARATION_PATH__KERNEL_DOCBLOCK_UNEDITED__GATE_UNMOVED",
    "estatuto": "[REAL -- termos no axiom_report e linhas do kernel lidos; DECLARADO -- CR-02 (critico de 07/10); KNOWN -- Kato, Perturbation Theory for Linear Operators, cap. VI §2.7 (pagina a conferir)]",
    "fontes": ["g2_medidas", "g2_k_contmodrec", "g2_k_contmodres", "g2_k_aperiodic"],
    "kernel_flags": ["ext_v331_continuous050_continuous_modular_positive_square_root_kernel_proved", "ext_v331_continuous050_continuous_delta_eq_double_kernel_proved"],
    "kernel_decls": ["ChatgptAudit.Continuous050.continuous_modular_positive_square_root", "ChatgptAudit.Continuous050.continuous_delta_eq_double",
                     "ChatgptAudit.Continuous050.continuous_delta_selfadjoint", "ChatgptAudit.Continuous050.continuous_resolvent_sqrt"],
    "checks": [
        M("t01", "ContinuousModularReconstruction.lean: sha16", ["kernel", "ContinuousModularReconstruction", "sha16"], "igual", "0a5be091f8f24ea1"),
        M("t02", "l.155: o teorema continuous_modular_positive_square_root", _kl("ContinuousModularReconstruction", 155), "contem", "theorem continuous_modular_positive_square_root (c : ℝ)"),
        M("t03", "l.156: o enunciado afirma T_c auto-adjunto", _kl("ContinuousModularReconstruction", 156), "contem", "IsSelfAdjoint (continuousModularOperator c)"),
        M("t04", "l.158: ... positivo (0 ≤ <x, T_c x>)", _kl("ContinuousModularReconstruction", 158), "contem", "0 ≤ (inner ℂ"),
        M("t05", "l.159: ... e T_c ao quadrado e' Delta_c (continuousModularSquare c = continuousModularDelta c)", _kl("ContinuousModularReconstruction", 159), "contem", "continuousModularSquare c = continuousModularDelta c"),
        M("t06", "l.154: 'A positive self-adjoint square root, with its exact composition domain proved above'", _kl("ContinuousModularReconstruction", 154), "contem", "A positive self-adjoint square root, with its exact composition domain proved above"),
        M("t07", "l.114-115: continuous_delta_eq_double: Delta_c = T_(2c)", _kl("ContinuousModularReconstruction", 115), "contem", "continuousModularDelta c = continuousModularOperator (2*c)"),
        M("t08", "ContinuousModularResolvent.lean l.99: unicidade da raiz do lado limitado (CFC.sqrt_unique)", _kl("ContinuousModularResolvent", 99), "contem", "CFC.sqrt_unique"),
        M("t09", "ContinuousModularResolvent.lean l.103: idem para o complemento", _kl("ContinuousModularResolvent", 103), "contem", "CFC.sqrt_unique"),
        M("t10", "ContinuousModularResolvent.lean l.97-98: continuous_resolvent_sqrt", _kl("ContinuousModularResolvent", 97), "contem", "theorem continuous_resolvent_sqrt"),
        M("t11", "AperiodicAveragePrefix.lean l.14: 'Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN'", _kl("AperiodicAveragePrefix", 14), "contem", "Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN"),
        M("t12", "AperiodicAveragePrefix.lean l.26: 'BW/identificacao T_c = Delta^{1/2}' entre os [OPEN]", _kl("AperiodicAveragePrefix", 26), "contem", "BW/identificacao T_c = Delta^{1/2}"),
        M("t13", "arvore_da_prova.py l.272 (gerador, cadeia): 'a identificação segue OPEN'", ["arvore_da_prova_py", "linhas", "272"], "contem", "a identificação segue OPEN"),
        CK("t14", "o consolidado atual traz o CR-02 (so' no atual; [DECLARADO pelo critico])", "fonte:g2_medidas", ["consolidados", "cr_titulos_no_atual", "CR-02", "classe_final"], "igual", "SABIDO_POR_CITACAO", est="[DECLARADO pelo critico de 07/10]"),
    ],
    "erratas": [
        ER("AperiodicAveragePrefix.lean docblock l.11-14 e l.25-26 (o kernel NAO se edita) e arvore_da_prova.py l.272 (gerador da arvore, cadeia de selo, fora do um.py): 'Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN'",
           "'a identificacao T_c = Delta_c^{1/2} (049-050 construiram o subespaco padrao continuo; a identificacao segue OPEN)'",
           "[REAL] a EXISTENCIA da raiz quadrada positiva auto-adjunta de Delta_c e' TERMO: ChatgptAudit.Continuous050.continuous_modular_positive_square_root (ContinuousModularReconstruction.lean l.155; axiom_report, trio): T_c e' auto-adjunto e positivo e T_c∘T_c = Delta_c com o dominio exato de composicao; continuous_delta_eq_double: Delta_c = T_(2c). Do lado LIMITADO a UNICIDADE da raiz positiva ja' e' termo (ContinuousModularResolvent.lean l.99 e l.103, CFC.sqrt_unique). Falta so' a unicidade da raiz positiva de operador fechado ILIMITADO [KNOWN -- Kato, Perturbation Theory for Linear Operators, cap. VI §2.7; pagina a conferir] (a mathlib nao a tem para ilimitados) [DECLARADO pelo critico, CR-02]. O BW do CAMINHO, na luz, e' SABIDO (FockCertificate.bw_kms; QG-04); o BW da TORRE e' parede (K35) [DECLARADO pelo critico, CR-02]. Fora do caminho da declaracao. O docblock do kernel fica; o gerador da arvore leva a errata correspondente (ato da cadeia).",
           "estrutura: dois conteudos distintos -- a existencia da raiz positiva (termo) e a unicidade para ilimitado (KNOWN, Kato); escrito: 'a identificacao segue OPEN' num bloco so'; onde a traducao falhou: a traducao fundiu existencia e unicidade.",
           "[REAL] termos e linhas lidos; [KNOWN] Kato (pagina a conferir); [DECLARADO] CR-02"),
    ],
    "limites": ["[OPEN] a pagina de Kato (cap. VI §2.7) esta por conferir na fonte; ate la a unicidade para ilimitado e' [KNOWN] por citacao", "[REAL] o kernel nao e' editado; nada move o gate"],
    "diz": ["[REAL] a raiz quadrada positiva de Delta_c existe por termo no kernel; a unicidade para operador fechado ilimitado e' [KNOWN]"],
    "nao_diz": ["nao diz que o BW da torre esta provado; nao diz que a unicidade para ilimitados esta formalizada; nao move o gate", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"kato": "Kato, Perturbation Theory for Linear Operators, cap. VI §2.7 [KNOWN; pagina a conferir]", "mapa_busca": "0 registros com Kato, Continuous050 ou raiz quadrada positiva (busca direta do critico) [DECLARADO]"},
})

# =====================================================================================================================================
# 9. ww_premissa_errata_v392 (R23; CR-06)
# =====================================================================================================================================
SPECS.append({
    "nome": "ww_premissa_errata_v392", "veredito_prefixo": "TGL_WW_PREMISE_ERRATUM_V392",
    "veredito_sufixo": "GRAVITON_IS_I_IS_THE_GENERATOR_PREMISE_DENIED_IN_V372__CURRENT_TYPING_V373_METRIC_NOT_QUANTIZED__IF_G_IS_QUANTIZED_WEINBERG_WITTEN_BITES_AGAIN__GATE_UNMOVED",
    "estatuto": "[REAL -- texto do core e termos do kernel lidos; DECLARADO -- CR-06 (critico de 07/10); DERIVED de leitura -- a leitura vigente]",
    "fontes": ["g2_medidas"],
    "kernel_flags": ["ext_uv_dissolved_by_typing_kernel_proved"],
    "kernel_decls": ["TGLExt.QGReaderUVLock.light_geometry_is_a_classical_functional_of_T", "TGLExt.QGReaderUVLock.light_response_is_a_real_matrix_field",
                     "TGLExt.QGReaderUVLock.graviton_identity_costs_nothing", "TGLExt.QGReaderUVLock.uv_dissolved_by_typing"],
    "checks": [
        C("w01", "graviton_not_a_particle.statuses.o_escape: o graviton do programa e I (identidade; rho* = |G><G|, Tr=1)", ["graviton_not_a_particle", "statuses", "o_escape"], "contem", "o graviton do programa e I (identidade; rho* = |G><G|, Tr=1)"),
        C("w02", "statuses.a_inversao cita a premissa 'graviton = I = gerador'", ["graviton_not_a_particle", "statuses", "a_inversao"], "contem", "A tipagem corrente (graviton = I = gerador"),
        C("w03", "statuses.a_inversao: se 'particula fundamental' for spin-2 propagante a quantizar, W-W VOLTA a morder", ["graviton_not_a_particle", "statuses", "a_inversao"], "contem", "W-W VOLTA a morder"),
        C("w04", "o veredito do registro: ESCAPE_CONDITIONAL_ON_CURRENT_TYPING", ["graviton_not_a_particle", "verdict"], "contem", "ESCAPE_CONDITIONAL_ON_CURRENT_TYPING"),
        C("w05", "a v372 nega a premissa: o graviton NAO e' o gerador (errata_v372)", ["graviton_not_a_particle", "errata_v372"], "contem", "NOT_THE_GENERATOR"),
        C("w06", "graviton_conjugated_form_v372.verdict (a errata ao lado da v200)", ["graviton_conjugated_form_v372", "verdict"], "igual", "GRAVITON_IS_THE_CONJUGATED_FORM_OF_LIGHT__NOT_THE_GENERATOR__WW_ESCAPE_CONDITIONAL__ERRATA_BESIDE_V200"),
        C("w07", "graviton_conjugated_form_v372 segue verificado", ["graviton_conjugated_form_v372", "all_verified"], "verdadeiro"),
        C("w08", "v372: a ordem do operador (23/08; 28/08; 26/09) foi contrariada pela v200", ["graviton_conjugated_form_v372", "errata_v200"], "contem", "contrario a ordem do operador (23/08; 28/08; 26/09)"),
        C("w09", "tipagem vigente (v373): a questao 'estado quantico interagente / UV' e' DISSOLVIDA pela tipagem (nao respondida)", ["qg_closure", "gate", "kernel_frontier", "dissolved_by_typing_v373", "interacting_quantum_state_BRST_QME_anomalies_and_UV_scope", "statute"], "contem", "METRIC_NOT_QUANTIZED"),
        C("w10", "... ratificada pelo operador em 26/09/2026", ["qg_closure", "gate", "kernel_frontier", "dissolved_by_typing_v373", "interacting_quantum_state_BRST_QME_anomalies_and_UV_scope", "statute"], "contem", "OPERATOR_RATIFIED_2026_09_26"),
        C("w11", "... a geometria e' funcional classico de T (semiclassico por construcao)", ["qg_closure", "gate", "kernel_frontier", "dissolved_by_typing_v373", "interacting_quantum_state_BRST_QME_anomalies_and_UV_scope", "statute"], "contem", "GEOMETRY_CLASSICAL_FUNCTIONAL_OF_T"),
        CK("w12", "CR-06 no consolidado atual: classe DECISAO_DO_OPERADOR ([DECLARADO pelo critico])", "fonte:g2_medidas", ["consolidados", "cr_titulos_no_atual", "CR-06", "classe_final"], "igual", "DECISAO_DO_OPERADOR", est="[DECLARADO pelo critico de 07/10]"),
    ],
    "erratas": [
        ER("core.graviton_not_a_particle.statuses.o_escape e .a_inversao (e o veredito 'WEINBERG_WITTEN_TYPED__GRAVITON_IS_THE_IDENTITY_NOT_A_PROPAGATING_QUANTUM__ESCAPE_CONDITIONAL_ON_CURRENT_TYPING'); fonte no um.py (P2, v200, ~l.156245-156282)",
           "o escape de Weinberg-Witten justificado pela premissa 'graviton = I = gerador' ('A tipagem corrente (graviton = I = gerador; luz = interface em 3D) NAO o exige')",
           "[DERIVED de leitura; CR-06 [DECLARADO], DECISAO_DO_OPERADOR] a premissa 'graviton = I = gerador' foi NEGADA na v372 (graviton_conjugated_form_v372: ...GRAVITON_IS_THE_CONJUGATED_FORM_OF_LIGHT__NOT_THE_GENERATOR__WW_ESCAPE_CONDITIONAL__ERRATA_BESIDE_V200; o controle numerico mostra que o tensor NAO tem peso 1). A premissa VIGENTE e' a tipagem v373 (ratificada pelo operador em 26/09/2026): a metrica NAO e' quantizada, a geometria e' funcional classico de T e a resposta da luz e' campo de matriz real (TGLExt.QGReaderUVLock.light_geometry_is_a_classical_functional_of_T; light_response_is_a_real_matrix_field; graviton_identity_costs_nothing; uv_dissolved_by_typing -- axiom_report, trio). Sob essa tipagem nao ha operador de metrica nem quantum de graviton, e a premissa de Weinberg-Witten (particula sem massa de helicidade 2 com T covariante conservado) nao e' instanciada: o escape vale por decisao ja tomada, nao pela premissa antiga. SE g for quantizado, Weinberg-Witten VOLTA a morder (a_inversao, [OPEN] dito sem veu). O texto do core fica como registro.",
           "estrutura: tres tipagens em sequencia (v200: nao-particula/gerador; v372: forma conjugada da luz, nao o gerador; v373: metrica nao quantizada); escrito: o registro de v200 ainda justifica o escape com a premissa de v200; onde a traducao falhou: o registro nao foi reescrito quando a premissa mudou (a v372 pos a errata so' no registro irmao).",
           "[REAL] os textos e os termos lidos; [DERIVED de leitura] a leitura vigente; [DECLARADO] CR-06"),
    ],
    "limites": ["[OPEN] se o operador quantizar g, Weinberg-Witten volta a morder; ate la o escape e' condicional a tipagem corrente", "[DECLARADO] uma pedra que nomeie W-W (o tipo nao tem estados de uma particula de helicidade ±2) e' opcional e nao existe (grep 'Weinberg' no kernel: 0 arquivos, critico de 07/10)"],
    "diz": ["[REAL] a premissa do escape foi trocada: de 'graviton = I = gerador' (negada na v372) para a tipagem semiclassica da v373"],
    "nao_diz": ["nao diz que Weinberg-Witten esta refutado; nao diz que a gravidade foi quantizada; nao move o gate", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"premissa_negada": "graviton = I = gerador", "premissa_vigente": "metrica nao quantizada; geometria = funcional classico de T; resposta da luz = campo de matriz real (v373)"},
})

# =====================================================================================================================================
# 10. parametros_nomeados_v392 (R24; CR-10; P16)
# =====================================================================================================================================
SPECS.append({
    "nome": "parametros_nomeados_v392", "veredito_prefixo": "TGL_NAMED_PARAMETERS_V392",
    "veredito_sufixo": "DIMENSION_4_LORENTZIAN_SIGNATURE_LOCAL_FLAT_BACKGROUND_WEDGE_AND_NULL_DIRECTION_READ_AS_NAMED_PARAMETERS__DERIVED_READING_TO_BE_VETOED__CONSUMMATED_UNCHANGED__GATE_UNMOVED",
    "estatuto": "[REAL -- a conferencia v376 e as linhas do kernel lidas; DERIVED de leitura -- 'sao parametros nomeados da declaracao' e' leitura da gerencia, a vetar (P16, CR-10); DECLARADO -- CR-10 e a opcao alternativa (programa de derivacao K30/K31) sao do critico]",
    "fontes": ["g2_medidas", "g2_k_contratoqg", "g2_k_qgsc"],
    "checks": [
        C("p01", "conferencia v376: CONSUMADO", ["tetelestai_conference_v376", "consummated"], "verdadeiro"),
        C("p02", "conferencia v376: ABERTO 0", ["tetelestai_conference_v376", "counts", "ABERTO"], "igual", 0),
        C("p03", "conferencia v376: 41 itens", ["tetelestai_conference_v376", "items"], "tamanho_igual", 41),
        C("p04", "conferencia v376: 4 PARAMETRO_NOMEADO", ["tetelestai_conference_v376", "counts", "PARAMETRO_NOMEADO"], "igual", 4),
        C("p05", "PARAMETRO_NOMEADO: KillingNormalization", ["tetelestai_conference_v376", "items", "KillingNormalization", "classe"], "igual", "PARAMETRO_NOMEADO"),
        C("p06", "PARAMETRO_NOMEADO: NewtonConstantPositive", ["tetelestai_conference_v376", "items", "NewtonConstantPositive", "classe"], "igual", "PARAMETRO_NOMEADO"),
        C("p07", "PARAMETRO_NOMEADO: LocalEquilibriumWindow", ["tetelestai_conference_v376", "items", "LocalEquilibriumWindow", "classe"], "igual", "PARAMETRO_NOMEADO"),
        C("p08", "PARAMETRO_NOMEADO: PhysicalArrowAlphaInput", ["tetelestai_conference_v376", "items", "PhysicalArrowAlphaInput", "classe"], "igual", "PARAMETRO_NOMEADO"),
        C("p09", "o contrato da rede fotonica cita Brunetti-Guido-Longo 2002 (base)", ["tetelestai_conference_v376", "items", "PhysicalPhotonNetContractMeasured", "base"], "contem", "Brunetti-Guido-Longo 2002"),
        C("p10", "o veredito da conferencia diz '4_NAMED_PARAMETERS'", ["tetelestai_conference_v376", "verdict"], "contem", "4_NAMED_PARAMETERS"),
        M("p11", "ContratoQG_v31.lean l.78: convencao (+,−,−,−)", _kl("ContratoQG_v31", 78), "contem", "(+,−,−,−)"),
        M("p12", "ContratoQG_v31.lean l.80: a direcao nula n = (1, 1, 0, 0)", _kl("ContratoQG_v31", 80), "contem", "n = (1, 1, 0, 0)"),
        M("p13", "ContratoQG_v31.lean l.81: linearizacao em torno de Minkowski", _kl("ContratoQG_v31", 81), "contem", "Linearização em torno de Minkowski"),
        M("p14", "ContratoQG_v31.lean l.88: as outras componentes de Einstein exigem a familia de Lorentz de cunhas", _kl("ContratoQG_v31", 88), "contem", "família de Lorentz de cunhas"),
        M("p15", "QGSolutionComplete.lean l.52: o tipo usa Fin 4 → ℝ", _kl("QGSolutionComplete", 52), "contem", "Fin 4 → ℝ"),
        M("p16", "QGSolutionComplete.lean l.80: rightWedge", _kl("QGSolutionComplete", 80), "contem", "rightWedge"),
        M("p17", "QGSolutionComplete.lean l.82: nullDir", _kl("QGSolutionComplete", 82), "contem", "nullDir"),
        CK("p18", "CR-10 no consolidado atual: classe DECISAO_DO_OPERADOR ([DECLARADO pelo critico])", "fonte:g2_medidas", ["consolidados", "cr_titulos_no_atual", "CR-10", "classe_final"], "igual", "DECISAO_DO_OPERADOR", est="[DECLARADO pelo critico de 07/10]"),
    ],
    "erratas": [
        ER("core.tetelestai_conference_v376 (41 itens; counts.PARAMETRO_NOMEADO = 4: KillingNormalization, NewtonConstantPositive, LocalEquilibriumWindow, PhysicalArrowAlphaInput); CR-10",
           "a conferencia enumera 4 parametros nomeados; nenhum item nomeia a dimensao, a assinatura, o fundo plano, a cunha ou a direcao nula",
           "[DERIVED de leitura; a vetar (P16, CR-10)] o TIPO da declaracao fixa mais cinco entradas que a conferencia nao enumera, e a gerencia as le como PARAMETROS NOMEADOS da declaracao, ao lado dos quatro: (1) a dimensao 4 (Fin 4 → ℝ, QGSolutionComplete.lean l.52); (2) a assinatura lorentziana (+,−,−,−) (ContratoQG_v31.lean l.78); (3) o fundo plano local (linearizacao em torno de Minkowski, l.81); (4) a cunha (rightWedge, QGSolutionComplete l.80); (5) a direcao nula (nullDir, n = (1, 1, 0, 0), ContratoQG_v31 l.80). A base e' a rede citada de Brunetti-Guido-Longo (2002), cuja arena e' o Minkowski 4D [KNOWN]. [DECLARADO pelo critico] a derivacao da dimensao 4 e da assinatura e' [OPEN] na arvore (a outra opcao do CR-10 e' abrir o programa de derivacao, K30/K31: 'outra representacao', v319 -- decisao do operador). O CONSUMADO NAO muda (ABERTO 0): muda o que a conferencia enumera. Esta leitura NAO acrescenta os cinco ao core nem a conferencia; so' os nomeia.",
           "estrutura: o tipo da declaracao fixa dimensao, assinatura, fundo, cunha e direcao nula; escrito: a conferencia v376 tem 41 itens e so' 4 parametros nomeados; onde a traducao falhou: nenhuma das cinco entradas de tipo aparece como item ou como parametro.",
           "[REAL] linhas e conferencia lidas; [DERIVED de leitura; a vetar] a leitura; [KNOWN] BGL 2002; [DECLARADO] CR-10"),
    ],
    "limites": ["[DERIVED de leitura; a vetar] sem palavra do operador (P16) o registro vai como leitura da gerencia", "[OPEN] a derivacao (nao a declaracao) da dimensao 4 e da assinatura lorentziana segue aberta", "[REAL] a conferencia v376 nao e' alterada; o core nao ganha item algum"],
    "diz": ["[DERIVED de leitura; a vetar] dimensao 4, assinatura lorentziana, fundo plano local, a cunha e a direcao nula (base BGL 2002) sao parametros nomeados da declaracao"],
    "nao_diz": ["nao diz que esses cinco foram derivados; nao altera o CONSUMADO; nao move o gate", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"parametros_ja_nomeados_pela_conferencia": ["KillingNormalization", "NewtonConstantPositive", "LocalEquilibriumWindow", "PhysicalArrowAlphaInput"],
               "parametros_nomeados_por_esta_leitura": ["dimensao 4", "assinatura lorentziana (+,-,-,-)", "fundo plano local (Minkowski)", "a cunha (rightWedge)", "a direcao nula (nullDir)"],
               "rotulo": "[DERIVED de leitura; a vetar]", "base": "Brunetti-Guido-Longo 2002 (Rev. Math. Phys. 14) [KNOWN]"},
})

# =====================================================================================================================================
# 11. cmb_s4_errata_v392 (R25; CR-13)
# =====================================================================================================================================
_cm = MED["cmb_s4"]
SPECS.append({
    "nome": "cmb_s4_errata_v392", "veredito_prefixo": "TGL_CMB_S4_ERRATUM_V392",
    "veredito_sufixo": "CMB_S4_PROJECT_WITHDRAWN_BY_DOE_NSF_2025_07_09_READ_IN_THE_PINNED_OFFICIAL_PAGE__SENSITIVITY_ARITHMETIC_STILL_DECLARED__D8_OF_THE_OPERATOR_PENDING__GATE_UNMOVED",
    "estatuto": "[REAL -- a captura de https://cmb-s4.org/ (copia byte a byte pinada; recibo de download do Codex) lida por script; DECLARADO -- a aquisicao da pagina e' do Codex (ORDEM_018, 06/10) e a autenticidade da busca HTTP e' a do recibo; o 0,045 do Simons Observatory 'enhanced' e a conta de ~2,7 sigma; a admissao da fonte como dado de rito (D8) e' ato do operador]",
    "fontes": ["g2_medidas", "g2_cmb_captura"],
    "checks": [
        C("m01", "code_closure_ledger.ledger[5].item nomeia 'Euclid/CMB-S4'", ["code_closure_ledger", "ledger", 5, "item"], "contem", "Euclid/CMB-S4"),
        C("m02", "ledger[5].classe = INPUT_BY_DESIGN", ["code_closure_ledger", "ledger", 5, "classe"], "igual", "INPUT_BY_DESIGN"),
        C("m03", "void_floor_v11.statuses.honestidade cita 'Euclid DR1 2027 / CMB-S4'", ["void_floor_v11", "statuses", "honestidade"], "contem", "Euclid DR1 2027 / CMB-S4"),
        C("m04", "neff_channel.values.escada_projetada[3].instrumento = 'CMB-S4 (requisito)'", ["neff_channel", "values", "escada_projetada", 3, "instrumento"], "contem", "CMB-S4"),
        M("m05", "a captura tem a declaracao de 09/07/2025 do DOE e do NSF", ["cmb_s4", "frases_na_pagina", "a_declaracao_de_9_jul_2025"], "verdadeiro"),
        M("m06", "a captura traz: 'DOE and NSF have jointly decided that they can no longer support the CMB-S4 Project.'", ["cmb_s4", "frases_na_pagina", "decisao_conjunta"], "verdadeiro"),
        M("m07", "a captura traz: o projeto procede a um encerramento ordenado", ["cmb_s4", "frases_na_pagina", "desligamento_ordenado"], "verdadeiro"),
        M("m08", "a captura traz: a colaboracao cientifica independente 'is working to develop plans'", ["cmb_s4", "frases_na_pagina", "colaboracao_cientifica_independente"], "verdadeiro"),
        M("m09", "recibo de download: URL https://cmb-s4.org/", ["cmb_s4", "recibo_entrada", "url"], "igual", "https://cmb-s4.org/"),
        M("m10", "recibo de download: sha256 do recibo == sha256 da captura", ["cmb_s4", "recibo_entrada", "sha256"], "igual", _cm["sha256"]),
        M("m11", "recibo de download: bytes do recibo == bytes da captura", ["cmb_s4", "recibo_entrada", "bytes"], "igual", _cm["bytes"]),
        M("m12", "recibo de download: instante da busca (UTC)", ["cmb_s4", "recibo_entrada", "retrieved_at"], "igual", _cm["recibo_entrada"]["retrieved_at"], "baixada_em_utc"),
        M("m13", "artigo emitido v391, txt PT l.73, cita o CMB-S4", ["artigo_pt_v391", "linhas", "73"], "contem", "CMB-S4"),
        M("m14", "um.py v391 l.166093 (PT) cita o CMB-S4", _ul(166093), "contem", "CMB-S4"),
        CK("m15", "CR-13 no consolidado atual: classe AGUARDA_INSTRUMENTO ([DECLARADO pelo critico])", "fonte:g2_medidas", ["consolidados", "cr_titulos_no_atual", "CR-13", "classe_final"], "igual", "AGUARDA_INSTRUMENTO", est="[DECLARADO pelo critico de 07/10]"),
        C("m16", "o canal de N_eff segue armado como o core o descreveu (nao e' mexido)", ["neff_channel", "all_verified"], "verdadeiro"),
    ],
    "erratas": [
        ER("core.code_closure_ledger.ledger[5].item ('experimento (materia bilateral Euclid/CMB-S4; NMC-Shapiro 2030+; Sigma m_nu)'), core.void_floor_v11.statuses.honestidade ('Euclid DR1 2027 / CMB-S4') e o artigo PT (txt l.73, 629, 1425, 1434); CR-13",
           "o CMB-S4 como experimento futuro (materia bilateral; era da radiacao) cujo dado fechara o canal",
           "[REAL: pagina lida neste rito] O site oficial do projeto, captura local de https://cmb-s4.org/ (recibo de download de 06/10/2026 00:47:57 UTC, sha256 %s, %d B; copia byte a byte pinada), diz: 'On July 9, 2025, the U.S. Department of Energy (DOE), Office of Science, Office of High Energy Physics and the U.S. National Science Foundation (NSF) issued a statement informing the CMB-S4 Project that \"DOE and NSF have jointly decided that they can no longer support the CMB-S4 Project.\" The CMB-S4 Project is proceeding with an orderly shutdown ...'; e que a colaboracao cientifica, 'an independent organization, is working to develop plans to best support the community'. Logo o CMB-S4 como PROJETO apoiado nao e' instrumento previsto; sem experimento definido a colaboracao 'is working to develop plans'. [DECLARADO] o 0,045 do Simons Observatory 'enhanced' (mapa de rotas, seq 402 e 607) e a conta de ~2,7 sigma para delta N_eff = 0,1195 (CR-13: [DERIVED] pelo critico) nao foram conferidos aqui; [DECLARADO] que 'nenhum instrumento previsto alcanca sigma(N_eff) <= 0,024'. A admissao desta pagina como fonte de rito (D8) e' ato do operador, pendente. O texto do ledger e do artigo fica como registro; o horizonte do canal da era da radiacao passa a 'aguarda instrumento nao previsto' [DERIVED de leitura]." % (_cm["sha256"], _cm["bytes"]),
           "estrutura: o projeto CMB-S4 foi encerrado pelas agencias em 09/07/2025 (pagina oficial); escrito: o ledger e o artigo o nomeiam como o experimento da era da radiacao; onde a traducao falhou: a nomeacao vem de um forecast do projeto (0,030, alvo e nao medicao) e nao foi relida contra o estado do projeto.",
           "[REAL] a pagina; [DECLARADO] a autenticidade da busca (recibo do Codex), o Simons Observatory 0,045 e a conta de sensibilidade; [DERIVED de leitura] o novo horizonte"),
    ],
    "limites": ["[REAL] a pagina e' a captura de 06/10/2026: o estado do site hoje nao foi relido (sem rede neste rito)", "[DECLARADO] D8 (admissao de fontes por hash) e' ato do operador; esta errata nao admite a fonte como dado de rito",
                "[OPEN] qual instrumento alcanca sigma(N_eff) <= 0,0239 (5 sigma para delta N_eff = 0,1195) e' pergunta aberta"],
    "diz": ["[REAL] a pagina oficial do CMB-S4 (captura pinada) diz que DOE e NSF decidiram em 09/07/2025 nao mais apoiar o projeto, que procede a encerramento ordenado", "[DERIVED de leitura] o CMB-S4 deixa de ser instrumento previsto no ledger e no artigo"],
    "nao_diz": ["nao diz que nenhum instrumento futuro alcanca 5 sigma (isso e' [DECLARADO])", "nao move o gate; nao altera o canal de N_eff; NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"captura": {"url": "https://cmb-s4.org/", "sha256": _cm["sha256"], "bytes": _cm["bytes"], "recibo_sha256": _cm["recibo_sha256"], "origem": "Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\fontes_publicas\\cmb_s4_status.html"},
               "frases": _cm["frases"], "mapa": "primordial.fase8_era_da_radiacao, seq 402 e 607 ([DECLARADO]; consultado, nao registrado)", "d8": "pendente (ato do operador)"},
})

# =====================================================================================================================================
# 12. d1_orientacao_errata_v392 (R26; D1)
# =====================================================================================================================================
_nc = MED["consolidados"]["atual"]
SPECS.append({
    "nome": "d1_orientacao_errata_v392", "veredito_prefixo": "TGL_D1_ORIENTATION_ERRATUM_V392",
    "veredito_sufixo": "D1_TENSION_3P01_SIGMA_MEASURED_ON_THE_BRANCH_READ_AS_MIRROR_TO_FIRST_ORDER__INVERTED_BRANCH_AT_0P09_SIGMA__D1_V3_VERDICT_UNCHANGED__NEW_PREREGISTRATION_NEEDED__GATE_UNMOVED",
    "estatuto": "[REAL -- os valores do D1 V3 e da orientacao lidos do core; DECLARADO -- 'o ramo invertido a 0,09 sigma' e a regra QG-F35 (consolidado, nota do critico (b)); DERIVED -- a leitura da primeira lei (argumento da gerencia, conferido com o operador, no proprio core)]",
    "fontes": ["g2_medidas", "g2_consolidado_atual"],
    "checks": [
        C("d01", "orientation_is_the_sign_v367 segue verificado", ["orientation_is_the_sign_v367", "all_verified"], "verdadeiro"),
        C("d02", "o veredito le o implementado como ESPELHO em primeira ordem; o bit nao esta derivado; a determinacao do operador esta registrada", ["orientation_is_the_sign_v367", "verdict"], "contem", "IMPLEMENTED_IS_MIRROR_TO_FIRST_ORDER__BIT_NOT_DERIVED_YET__OPERATOR_DETERMINATION_RECORDED"),
        C("d03", "distancia do beta medido ao ramo implementado (+beta), em sigma", ["orientation_is_the_sign_v367", "z_to_mirror_branch"], "maior_igual", 3.01, "z_ramo_implementado"),
        C("d04", "... (limite superior, para que o valor nao derive)", ["orientation_is_the_sign_v367", "z_to_mirror_branch"], "menor_igual", 3.02),
        C("d05", "distancia do beta medido ao ramo invertido (-beta), em sigma", ["orientation_is_the_sign_v367", "z_to_coupling_branch"], "maior_igual", 0.08, "z_ramo_invertido"),
        C("d06", "... (limite superior)", ["orientation_is_the_sign_v367", "z_to_coupling_branch"], "menor_igual", 0.1),
        C("d07", "beta medido pelo D1 V3 (mediana)", ["orientation_is_the_sign_v367", "d1_beta_median"], "menor_igual", -0.0127, "d1_beta_mediana"),
        C("d08", "sigma do beta medido", ["orientation_is_the_sign_v367", "d1_beta_sigma"], "maior_igual", 0.0082, "d1_beta_sigma"),
        C("d09", "orientation.statuses.d1: o veredito de maquina da v366 nao se move", ["orientation_is_the_sign_v367", "statuses", "d1"], "contem", "o veredito de máquina da v366 não se move"),
        C("d10", "linha de nao-pode-mudar: o veredito do D1 V3 (v366) igual ao do core v391", ["d1_camb_v3_real_v366", "verdict"], "igual", MED["core_v391"]["d1_v3_verdict"]),
        C("d11", "o veredito do D1 V3 diz 'ALPHA_SQRT_E_AT_3P01_SIGMA'", ["d1_camb_v3_real_v366", "verdict"], "contem", "ALPHA_SQRT_E_AT_3P01_SIGMA"),
        C("d12", "D1 V3: a tensao nao e' falsificacao", ["d1_camb_v3_real_v366", "verdict"], "contem", "TENSION_IS_NOT_FALSIFICATION"),
        C("d13", "D1 V3 fase 3: 'alpha sqrt(e) a 3.01 sigma'", ["d1_camb_v3_real_v366", "statuses", "fase3"], "contem", "alpha sqrt(e) a 3.01 sigma"),
        C("d14", "a cegueira dita no core: o ramo foi nomeado depois de o resultado ser conhecido", ["orientation_is_the_sign_v367", "statuses", "cegueira"], "contem", "o ramo foi nomeado depois de o resultado ser conhecido"),
        C("d15", "a determinacao do operador le o BIT como a face do estado", ["orientation_is_the_sign_v367", "statuses", "determinacao_do_operador"], "contem", "o operador leu o BIT como a face do estado"),
        C("d16", "R1 de 02/10: o D1 V3 'fica ao lado ... nao e' a regra'", ["the_ledger_of_charges_v383", "readings_ratified_20261002", "R1"], "contem", "D1 V3) fica ao lado como medido sob outra convenção, não é a regra"),
        C("d17", "bancada_fases_v377: o D1 V3 (3,01 sigma) e' condicional ao mapa de R", ["bancada_fases_v377", "erratum_beside_d1_v3"], "contem", "CONDICIONAL AO MAPA DE R"),
        M("d18", "artigo emitido v391 (txt PT): a 'tensao D1 3,01 sigma' aparece 7 vezes", ["artigo_pt_v391", "n_ocorrencias_3_01_sigma"], "igual", MED["artigo_pt_v391"]["n_ocorrencias_3_01_sigma"]),
        CK("d19", "o consolidado atual (notas_critico, (b)) registra que trocar o sinal pede pre-registro novo com dado novo", "fonte:g2_consolidado_atual", ["notas_critico"], "contem", "Trocar o sinal pede pré-registro novo com dado novo", est="[DECLARADO pelo critico de 07/10]"),
    ],
    "erratas": [
        ER("toda 'tensao D1 3,01 sigma': artigo emitido (txt PT, %d ocorrencias nas linhas %s), Atlas (l.34960) e README do espelho (l.23) [DECLARADO pelo critico, nao relidos aqui], core.d1_camb_v3_real_v366 (verdict '...ALPHA_SQRT_E_AT_3P01_SIGMA...')" % (MED["artigo_pt_v391"]["n_ocorrencias_3_01_sigma"], MED["artigo_pt_v391"]["linhas_com_3_01_sigma"]),
           "'a tensao D1 de 3,01 sigma contra beta'",
           "[REAL: core] os 3,01 sigma (lido.z_ramo_implementado) sao a distancia do beta medido pelo D1 V3 (lido.d1_beta_mediana ± lido.d1_beta_sigma) ao ramo IMPLEMENTADO (+beta); ao ramo INVERTIDO (-beta) a distancia e' de lido.z_ramo_invertido sigma ([REAL: core, z_to_coupling_branch; o critico a escreve 0,09 sigma]) -- medidos no ramo que orientation_is_the_sign_v367 le como ESPELHADO em primeira ordem (veredito: ...IMPLEMENTED_IS_MIRROR_TO_FIRST_ORDER__BIT_NOT_DERIVED_YET__OPERATOR_DETERMINATION_RECORDED). A tensao e' portanto condicional ao BIT da orientacao: o bit (qual face fecha o balanco de Clausius) e' [INPUT -- nomeado]; o kernel prova o que CADA valor implica, nao qual e' o valor; a determinacao do operador le o bit como a face do estado e a gerencia a conferiu pela primeira lei modular [DERIVED -- condicional, no proprio core]. A R1 de 02/10 ja' pos o D1 V3 AO LADO ('nao e' a regra'), e o core (bancada_fases_v377, Fase 1) diz que a tensao do D1 e' CONDICIONAL AO MAPA DE R. O VEREDITO selado do D1 V3 NAO se move (tensao nao e' falsificacao). Dito no core: o ramo foi nomeado depois de o resultado ser conhecido, entao este conjunto de dados nao serve de teste cego do ramo escolhido; trocar o sinal pede PRE-REGISTRO NOVO com dado novo (regra da QG-F35) [DECLARADO pelo critico].",
           "estrutura: o D1 V3 mede o beta com sinal oposto ao do ramo implementado, e a determinacao do operador le a face do estado como o ramo certo; escrito: 'tensao D1 3,01 sigma contra beta' como se o ramo implementado fosse o certo; onde a traducao falhou: o numero 3,01 foi citado sem o ramo ao qual se refere.",
           "[REAL] valores e textos lidos no core (inclusive o ramo invertido); [DECLARADO] QG-F35 e as linhas do Atlas e do README (critico); [DERIVED] a leitura da primeira lei"),
    ],
    "limites": ["[REAL] nada foi rerodado nem afrouxado; a estrutura do dado nao mudou", "[OPEN] a derivacao do bit da orientacao e' programa; trocar o sinal de beta nos ritos pede pre-registro novo com dado novo"],
    "diz": ["[REAL] a tensao D1 de 3,01 sigma foi medida no ramo que a v367 le como espelhado em primeira ordem; no ramo invertido a distancia e' de ~0,09 sigma"],
    "nao_diz": ["nao diz que a tensao deixa de existir no ramo implementado; nao diz que beta tem o sinal invertido (o bit e' do operador); nao move o gate", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"d1_v3_verdict_nao_pode_mudar": MED["core_v391"]["d1_v3_verdict"], "linhas_do_artigo_pt_com_3_01": MED["artigo_pt_v391"]["linhas_com_3_01_sigma"], "orientation_verdict": MED["core_v391"]["orientation_verdict"]},
})

# =====================================================================================================================================
# 13. f81_nao_fechada_v392 (P15)
# =====================================================================================================================================
_f81 = MED["f81"]["unidade"]
SPECS.append({
    "nome": "f81_nao_fechada_v392", "veredito_prefixo": "TGL_F81_NOT_CLOSED_V392",
    "veredito_sufixo": "V392_DOCUMENTS_THE_FLAGS_DOES_NOT_RECOMPUTE_THEM__F8_1_STAYS_PROPOSAL__18_FLAGS_UNCHANGED__GATE_UNMOVED",
    "estatuto": "[REAL -- a unidade F8.1 lida do PROGRAMA.json no momento da medida (13/10/2026) e as bandeiras lidas do core; DECLARADO -- a decisao P15 da gerencia c1 (13/10/2026)]",
    "fontes": ["g2_medidas"],
    "checks": [
        M("q01", "quadro: a unidade e' F8.1", ["f81", "unidade", "id"], "igual", "F8.1"),
        M("q02", "quadro: titulo 'Bandeiras do gate calculadas e independentes'", ["f81", "unidade", "titulo"], "igual", _f81["titulo"]),
        M("q03", "quadro: status PROPOSTA", ["f81", "unidade", "status"], "igual", "PROPOSTA"),
        M("q04", "quadro: dono claude-c1", ["f81", "unidade", "dono"], "igual", "claude-c1"),
        M("q05", "quadro: criterio de fechado = 'versão selada com as bandeiras recalculadas e o achado da auditoria fechado'", ["f81", "unidade", "criterio_de_fechado"], "igual", _f81["criterio_de_fechado"]),
        M("q06", "quadro: evidencia vazia (nada entregue)", ["f81", "unidade", "evidencia"], "tamanho_igual", 0),
        C("q07", "o gate segue com a string de sempre", ["qg_closure", "gate", "verdict"], "igual", GATE),
        C("q08", "as 6 bandeiras experimentais seguem lidas como estavam (protocol_pre_registered ainda literal True)", ["qg_closure", "experiment_flags", "protocol_pre_registered"], "verdadeiro"),
        C("q09", "... e null_tests_passed_blind ainda literal True", ["qg_closure", "experiment_flags", "null_tests_passed_blind"], "verdadeiro"),
        C("q10", "... e linearized_spin2_finite_face ainda literal True", ["qg_closure", "physics_flags", "linearized_spin2_finite_face"], "verdadeiro"),
        M("q11", "um.py v391 l.163161 (a literal que a v392 NAO troca por medida)", _ul(163161), "contem", '"null_tests_passed_blind": True'),
    ],
    "erratas": [
        ER("quadro: unidade F8.1 'Bandeiras do gate calculadas e independentes' (PROPOSTA) e a errata (3) do estatuto (estatuto_da_prova_ressalva_v392)",
           "criterio de fechado da F8.1: 'versão selada com as bandeiras recalculadas e o achado da auditoria fechado'",
           "[DECLARADO pela gerencia c1, decisao P15 de 13/10/2026] a v392 NAO fecha a F8.1: a errata do estatuto DOCUMENTA as 3 bandeiras literais e o feed unico, mas NAO as recalcula; as 18 bandeiras seguem lidas como estavam (15 calculadas + 3 literais, ver o registro estatuto_da_prova_ressalva_v392) e o gate nao se move. A F8.1 segue PROPOSTA (dono claude-c1; evidencia vazia na leitura de 13/10) e so' fecha com versao selada que troque os literais por medida e separe as bandeiras do feed unico (critério da propria unidade).",
           "estrutura: a F8.1 pede bandeiras RECALCULADAS e independentes; escrito: uma errata que documenta; onde a traducao falhou: nao ha falha a corrigir -- o registro so' impede que a documentacao seja lida como conserto.",
           "[REAL] a unidade e as bandeiras lidas; [DECLARADO] a decisao P15"),
    ],
    "limites": ["[REAL] o PROGRAMA.json e' vivo: a leitura e' a de 13/10/2026 (o sha do momento esta em medidas_g2.json)", "[OPEN] a F8.1 depende de versao futura; nenhum prazo e' afirmado aqui"],
    "diz": ["[DECLARADO] a v392 documenta as bandeiras literais e o feed unico e NAO fecha a F8.1"],
    "nao_diz": ["nao diz que as bandeiras foram recalculadas; nao diz que a F8.1 foi entregue; nao move o gate", "NOT_FALSIFIED nunca e' a palavra da creditacao"],
    "extras": {"f81": {"id": _f81["id"], "titulo": _f81["titulo"], "status": _f81["status"], "dono": _f81["dono"], "criterio_de_fechado": _f81["criterio_de_fechado"], "evidencia_n": len(_f81["evidencia"])},
               "fecha_a_f81": False},
})

assert len(SPECS) == 13 and len({s["nome"] for s in SPECS}) == 13

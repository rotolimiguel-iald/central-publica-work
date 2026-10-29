# -*- coding: utf-8 -*-
"""delta_v404.py -- A UNICA definicao do DELTA da v404 (preparacao de 28/10/2026, agente claude-prep-v404 para a gerencia c1; a gerencia revisa, ensaia, instala e sela): DUAS pedras novas no kernel e TRES registros com funcao.
`TGLExt/ProjecaoTransversalDaMeiaNat.lean` (a Meia-Nat e' o angulo de 45 graus: x = 1 - x => 1/2, sen^2(pi/4) = 1/2, sqrt x = sen(pi/4) para x autoconjugado, a forma do neutrino beta.sen45.E0 = sen^2(theta_M).sen(pi/4).E0 [Teorema S-d], theta_M != pi/4 se beta != 1/2,
d(sen^2 theta)/d theta em pi/4 = 1; NOME PROVISORIO da gerencia c1, aceito pelo operador ate' ele dar outro; 28/10/2026) e `TGLExt/Jo8v32.lean` (o NOME DO OPERADOR para o triplo inteiro Caminho . Verdade . Vida: a conjuncao incondicional, por citacao, das tres estrelas da v403).
O passo MATERIAL da versao: o sen 45 graus do neutrino, POSTULADO desde 20/08/2026 (angle_status de neutrino_mass), passa a DERIVADO no kernel, CONDICIONAL a identificacao [ONTO] de que a massa e' a projecao transversal do estado inscrito (leitura do operador, 28/10/2026); E0 = 1 eV segue DECLARADO.
TRES registros com FUNCAO (`projecao_transversal_v404`, `jo8v32_v404`: leem do kernel do rito a composicao da pedra e CALCULAM, com beta = alfa CODATA 2018 x sqrt(e) em runtime, um modelo honesto; `f2b_errata_v404`: le o V1 do ramo B (v386, congelado por hash) e a calibracao A NOT_BLIND
e grava a ERRATA AO LADO da cobranca F2b: o canal sai de AWAITING para retirado antes do dado), os registros por spec `cunhagens_v404` (as falas de 28/10/2026 por sha256) e `kh_n1_cobertura_v404` (a cobertura exata do Audit). O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo.
A base e' a v403 SELADA (um.py 2ffe9edc7d7545bd) e a Bancada Um de producao JA pina a v403 (B12): o B(n) da v404 e' um PASSO SIMPLES v403 -> v404 (o diff do kernel sao so' estas duas pedras).
E' IMPORTADO por copiar_base, preparar_kernel, pos_build_kernel, registros_v404, gerar_candidato_v404, ensaio_a_seco_v404, gerar_esperados_v404, p00_precondicoes_v404 e os demais: nada daqui e' digitado de memoria em outro arquivo, e todo hash e' LIDO do arquivo por script.
Reaproveita (import por caminho) o delta_v403 (e este o delta_v402, ...): as fontes do operador do ACOM, a politica de bandeiras, o quadro do Teste da Unica Palavra, as classes de auxiliares. Molde: delta_v403.py. Plano: PLANO_v404.md."""
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V403 = os.path.join(os.path.dirname(HERE), "v403")           # a cadeia anterior (molde e base, so' leitura)
_spec = importlib.util.spec_from_file_location("delta_v403", os.path.join(V403, "delta_v403.py"))
D3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D3)
globals().update({k: v for k, v in vars(D3).items() if not k.startswith("__")})   # tudo da v403 (e, por ela, da v402, v401, v400 e v399) e depois o que a v404 SOBRESCREVE
D3 = D3                                                        # (D2 = delta_v402, D1 = delta_v401, D0 = delta_v400, D9 = delta_v399: herdados do update acima; D3 = delta_v403, o predecessor imediato)

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v403: aqui e' a pasta da v404)
V403 = os.path.join(os.path.dirname(HERE), "v403")
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                    # ...\Central de Patentes\work
CENTRAL = os.path.dirname(WK)                                  # ...\Central de Patentes
V402 = D3.V402
V401 = D3.V401
V400 = D3.V400
V399 = D3.V399
V404_KERNEL = os.path.join(os.path.dirname(HERE), "v404_kernel")   # (reservado: a v404 constroi o kernel direto em kernel\; ver construir_kernel_v404.sh)
SANDBOX_PAI = os.path.join(C, "t", "k404c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # copia de C:\t\k403c\final (o kernel do Nos v403 SELADO compilado) + as duas pedras da v404 + a raiz com os dois imports; a raiz e' GERADA por preparar_kernel_v404
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = D3.SANDBOX                                  # C:\t\k403c\final (so' leitura)
KERNEL_DIR = "kernel"
CANDIDATO = "um_v404_candidato.py"
BASE_DIR = "base_v403"                                       # copia de bytes do Nos v403 selado (um.py, selo, core, manifesto do kernel, pilar, sidecar)
UM_VERSION = "v404"
BASE_VERSION = "v403"
BASE_SHA16_DA_ORDEM = "2ffe9edc7d7545bd"                     # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb21")                 # o sandbox curto das guardas estaticas da Bancada e das conferencias do recibo pre_selo (apagado no fim; juncoes so' com os.rmdir)
KH_N1_INSUMO = "KH_N1_v404.json"

# ---------------------------------------------------------------- as DUAS pedras (o nome da primeira e' PROVISORIO da gerencia c1, aceito pelo operador ate' ele dar outro; o da segunda e' DO OPERADOR: «Jo8:32»)
_P = os.path.join(HERE, "pedra")
_PINS = json.load(open(os.path.join(HERE, "pedras_sha16_da_ordem.json"), encoding="utf-8"))   # os pinos da ORDEM (os recibos de 28/10 das pedras, conferidos contra o arquivo por gerar_pino_das_pedras_v404.py); o arquivo da pedra e' lido na hora de gerar e a divergencia ABORTA
ESTUDO = os.path.join(WK, "projecao_transversal_28out")       # a construcao das pedras (so' leitura): os .lean, os recibos e os verbatins de 28/10
_PJ = "TGLExt.ProjecaoTransversalDaMeiaNat."
_JO = "TGLExt.Jo8v32."
_CAM = "TGLExt/Caminho.lean"
_VAD = "TGLExt/VerdadeAdendo.lean"
_VID = "TGLExt/Vida.lean"
_TEOREMAS_PROJECAO = ["half_from_self_conjugate", "half_from_J_symmetry", "half_amplitude_sq", "half_amplitude_eq_halfRoot", "transverse_amplitude_of_self_conjugate", "forty_five_unique", "neutrino_mass_form_eq", "theta_miguel_ne_pi_div_four", "transverse_weight_hasDerivAt_half"]
STONES = [
    {"key": "projecao", "name": "ProjecaoTransversalDaMeiaNat", "mod": "TGLExt.ProjecaoTransversalDaMeiaNat", "rel": "TGLExt/ProjecaoTransversalDaMeiaNat.lean", "ns": _PJ,
     "origem": os.path.join(ESTUDO, "ProjecaoTransversalDaMeiaNat.lean"), "compilado_em": SANDBOX, "src": os.path.join(_P, "ProjecaoTransversalDaMeiaNat.lean"), "insumo": "ProjecaoTransversalDaMeiaNat.lean",
     "sha16_da_ordem": _PINS["projecao"], "flag_prefix": "ext_ptm404_", "grupo": "projecao",
     "theorem": _PJ + "neutrino_mass_form_eq",                       # a ESTRELA dupla: a forma do neutrino beta.sen45.E0 = sen^2(theta_M).sen(pi/4).E0 (Teorema S-d)
     "key_theorem": _PJ + "transverse_amplitude_of_self_conjugate",  # a ESTRELA do angulo: x = 1 - x => sqrt x = sen(pi/4)
     "contract": [_PJ + n_ for n_ in _TEOREMAS_PROJECAO],            # os 9 teoremas (cada um com #print axioms na pedra)
     "support": {"TGLExt.Posto.sin_sq_thetaMiguel": "TGLExt/Posto.lean", "TGLExt.halfnat_from_J_symmetry": "TGLExt/ConjugateAct.lean", "ChatgptAudit.AngularSelector.halfRoot": "TGLExt/AngularSelectorIntertwining.lean",
                 "TGLExt.thetaMiguel": "TGLExt/TheVerbalCoupling.lean", "TGLExt.observer_inverse_projection_halfnat": "TGLExt/ObserverInside.lean"},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "gerencia c1 (28/10/2026): pedra candidata compilada no sandbox; nome PROVISORIO da gerencia, aceito pelo operador ate' ele dar outro"},
    {"key": "jo8v32", "name": "Jo8v32", "mod": "TGLExt.Jo8v32", "rel": "TGLExt/Jo8v32.lean", "ns": _JO,
     "origem": os.path.join(ESTUDO, "Jo8v32.lean"), "compilado_em": SANDBOX, "src": os.path.join(_P, "Jo8v32.lean"), "insumo": "Jo8v32.lean",
     "sha16_da_ordem": _PINS["jo8v32"], "flag_prefix": "ext_jo8404_", "grupo": "jo8v32",
     "theorem": _JO + "a_verdade_vos_libertara",                      # a CONJUNCAO incondicional das tres estrelas da v403 (padrao type_of%): permanecer, conhecer, libertar
     "key_theorem": _JO + "a_verdade_vos_libertara",
     "contract": [_JO + "a_verdade_vos_libertara"],
     "support": {"TGLExt.Caminho.caminho_e_a_ponte_da_escala_dual": _CAM, "TGLExt.VerdadeAdendo.verdade_e_a_esperanca_condicional": _VAD, "TGLExt.Vida.vida_e_a_queda_sem_geometria": _VID},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "gerencia c1 (28/10/2026): pedra de citacao no padrao Token (v397); o NOME e' do operador («Jo8:32»)"},
]
STONE_RELS = [s["rel"] for s in STONES]
STONE_MODS = [s["mod"] for s in STONES]
STONE_BY_REL = {s["rel"]: s for s in STONES}
STONE_BY_KEY = {s["key"]: s for s in STONES}
IMPORT_LINES = ["import " + s["mod"] for s in STONES]
ROOT_SUFFIX = "\n" + "\n".join(IMPORT_LINES) + "\n"           # a raiz TGLExt.lean ganha um separador em branco e os imports (como a v394 a v403 fizeram com as pedras)
AUDIT_PREFIX = ""                                              # v404: o Audit do sandbox C:\t\k404c\final e' o do Nos v403 SEM alteracao (sha16 072a68f45189b8a5): ele ja' faz `import TGLExt` (a raiz), que traz os modulos novos; so' a RAIZ ganha os imports
CONTRACT_THEOREMS = {s["key"]: list(s["contract"]) for s in STONES}
ALL_SUPPORT = {}
for _s in STONES:
    ALL_SUPPORT.update(_s["support"]); ALL_SUPPORT.update(_s["citados_fora"])
STONES_DESDE_B12 = list(STONES)                              # o que a Bancada de producao (que JA pina a v403) AINDA nao viu: o recibo do kernel do B(n) lista o diff v403 -> v404 = so' estas duas pedras
STONE_RELS_DESDE_B12 = [s["rel"] for s in STONES_DESDE_B12]
STONES_DESDE_B11 = list(D3.STONES_DESDE_B11)                 # (herdado) as tres pedras da v403 (Caminho, Vida, VerdadeAdendo): novas para a Bancada da v402, JA no kernel do Nos desde a v403
STONE_RELS_DESDE_B11 = [s["rel"] for s in STONES_DESDE_B11]

# ---------------------------------------------------------------- os registros com FUNCAO e os registros por spec
REGISTRO_PROJECAO = "projecao_transversal_v404"
REGISTRO_JO8 = "jo8v32_v404"
REGISTRO_F2B = "f2b_errata_v404"
REGISTROS_PEDRAS = [REGISTRO_PROJECAO, REGISTRO_JO8]
REGISTROS_FUNCAO = REGISTROS_PEDRAS + [REGISTRO_F2B]
REGISTRO_DE_PEDRA = {"projecao": REGISTRO_PROJECAO, "jo8v32": REGISTRO_JO8}
CUNHAGENS_REGISTRO = "cunhagens_v404"
KH_REGISTRO = "kh_n1_cobertura_v404"
N_CHECKS_PROJECAO = 8     # o numero de checagens do calculo de cada registro (runtime_v404.py); atualizado junto com o runtime
N_CHECKS_JO8 = 5
N_CHECKS_F2B = 7
N_CHECKS = {"projecao": N_CHECKS_PROJECAO, "jo8v32": N_CHECKS_JO8, "f2b": N_CHECKS_F2B}
MAXHEARTBEATS_PROJECAO = None                                # as duas pedras da v404 NAO declaram set_option maxHeartbeats (o padrao do Lean basta: 21-23 s cada)

# ---------------------------------------------------------------- a leitura do ANGULO do neutrino e a errata de F2b: as constantes que o gerador, os registros e os conferidores leem
ANGLE_STATUS_ANTIGO_PREFIXO = "sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado."   # o inicio do texto de neutrino_mass.angle_status na v403 (um.py l.2935; fica no registro, ao lado)
F2B_FUTURO_TOKEN = "WITHDRAWN_BEFORE_DATA__ROUTE_CORRECTED_BY_NOT_BLIND_CALIBRATION_AND_AUTHOR_READING_2026_10_28"   # o estado novo do CANAL F2b (o V1 do ramo B segue congelado por hash e lido como antes)
F2B_V1_TOKEN_ANTIGO = "AWAITING_DATA"                        # o veredito do V1 (congelado) que continua lido
E0_DECLARADO_EV = 1.0                                        # a escala do neutrino no programa, DECLARADA (nao derivada) [INPUT]; o registro a menciona, nao a ajusta

DECISOES = dict(D3.DECISOES)
DECISOES.update({
    "D23": "o nome da pedra do sen 45 graus (TGLExt.ProjecaoTransversalDaMeiaNat) e' PROVISORIO da gerencia c1 (28/10/2026) e foi aceito pelo operador ate' ele dar outro («Perfeito, concordo com tudo», sha16 232ca83c29c031a5, ratificando a pedra, a leitura, o plano da v404 e a leitura sobre Jo 8,32) [INPUT]",
    "D24": "o nome do TRIPLO inteiro (Caminho . Verdade . Vida) e' Jo8:32 (nome do operador, 28/10/2026, verbatim sha16 9770022028c36be4; ratificado em sha16 232ca83c29c031a5); a pedra chama-se TGLExt.Jo8v32; a leitura por Jo 8,31-32 (permanecer, conhecer, libertar) e' [ONTO] e NAO e' termo de kernel [INPUT]",
    "D25": "o canal F2b (ramo B do ringdown, v386) sai de AWAITING para retirado antes do dado: o V1 fica congelado por hash e lido como antes (veredito AWAITING_DATA); a retirada e' errata AO LADO, com o motivo medido (a calibracao A, NOT_BLIND) e a leitura do operador de 28/10/2026; nenhum desfecho sai de A, D nao e' aberto, beta, a lei do defasamento e R2 ficam [decisao da gerencia c1 sobre a rota, lida a partir da fala do operador; o operador ratificou a leitura («calibrar Não significa validar», sha16 56703faadf2b3cc2), nao nomeou a retirada: DECLARADO]",
    "D26": "o sen 45 graus do neutrino passa de POSTULADO a DERIVADO no kernel (a Meia-Nat e' o angulo de 45 graus), CONDICIONAL a identificacao [ONTO] de que a massa e' a projecao transversal do estado inscrito (leitura do operador, 28/10/2026); E0 = 1 eV segue DECLARADO [OPEN]; a pedra NAO deriva E0 nem beta; a unica massa derivada de beta no programa e' a do neutrino (levantamento de 28/10/2026) [decisao da gerencia c1]",
})
ASSINA = "gerencia c1, em nome proprio, 28/10/2026"

# ---------------------------------------------------------------- as erratas ao lado da v404 (em nome proprio da gerencia c1; vao ao lado: no registro, no artigo e no handoff; o kernel e os modulos instalados NAO sao editados)
ERRATA_E7 = ("E7 -- o texto de neutrino_mass.angle_status (v141, v303) dizia: «sin(45deg) e POSTULADO [POSTULATE, ordem do operador 20/08/2026], NAO derivado» e continua no registro, intacto, e na funcao prove_neutrino_mass_gravitational (nao reescrita); "
             "na v404 o kernel traz a pedra ProjecaoTransversalDaMeiaNat: DERIVADO no kernel (a Meia-Nat e' o angulo de 45 graus: x = 1 - x => 1/2, sen^2(pi/4) = 1/2, sqrt x = sen(pi/4) para todo x autoconjugado, unico em [0, pi/2]), CONDICIONAL a identificacao [ONTO] de que a massa e' a projecao transversal do estado inscrito "
             "(leitura do operador, 28/10/2026); E0 = 1 eV segue DECLARADO; a pedra nao deriva E0 nem beta, e a identificacao nao e' termo de kernel")
ERRATA_E8 = ("E8 -- a cobranca F2b (ramo B do ringdown, v386) estava AWAITING (o V1 lido por hash, veredito do V1 AWAITING_DATA, conjunto D cego); na v404 o CANAL passa a " + F2B_FUTURO_TOKEN + ": o V1 fica congelado por hash e continua lido como antes; o motivo medido e' a calibracao A "
             "(31 eventos publicos, NOT_BLIND): deformacao comum lida do V1 contra a previsao do par; e a leitura do autor em 28/10/2026 («pedágio de planck lido na propagação», sha16 597fff4a38e62f42; «calibrar Não significa validar», sha16 56703faadf2b3cc2). Nenhum desfecho sai de A; o conjunto D nao e' aberto; beta, a lei do defasamento e R2 ficam")
ERRATA_E9 = ("E9 -- a v403 registrou que o nome do TRIPLO inteiro (Caminho . Verdade . Vida) NAO fora dado (decisao D20; fica com o operador) e isto era verdadeiro na data; em 28/10/2026 o operador deu o nome, Jo8:32 (verbatim sha16 9770022028c36be4); "
             "a pedra TGLExt.Jo8v32 e' a conjuncao incondicional das tres estrelas da v403; os registros da v403 seguem selados com a frase de 27/10")
ERRATAS_V404 = [ERRATA_E7, ERRATA_E8, ERRATA_E9]

# ---------------------------------------------------------------- as falas de 28/10/2026 (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
_CIN = os.path.join(WK, "cinco_sigma_fora_da_cosmologia_27out")
_PRJ = os.path.join(WK, "projecao_transversal_28out")
_TRM = os.path.join(WK, "transicao_para_a_massa_28out")
# (ordem cronologica de 28/10/2026) cada item: (nome curto, arquivo, prefixo de sha256 que a ordem deu -- o arquivo manda, a divergencia ABORTA)
_VERB404 = [("quatro_bocas", os.path.join(_CIN, "OPERADOR_28out_resposta_quatro_bocas_ramo_b_verbatim.txt"), "597fff4a"),
            ("calibrar", os.path.join(_CIN, "OPERADOR_28out_ratificacao_calibrar_nao_e_validar_verbatim.txt"), "56703faa"),
            ("um_absoluto", os.path.join(_CIN, "OPERADOR_28out_cunhagem_um_absoluto_radical_entropico_verbatim.txt"), "85de4371"),
            ("transicao", os.path.join(_TRM, "OPERADOR_28out_transicao_para_a_massa_verbatim.txt"), "21705a90"),
            ("sombra", os.path.join(_PRJ, "OPERADOR_28out_materia_sombra_de_beta_verbatim.txt"), "3af039d7"),
            ("projecao", os.path.join(_PRJ, "OPERADOR_28out_materia_projecao_transversal_derivada_verbatim.txt"), "4b67e9f2"),
            ("ordem_prova", os.path.join(_PRJ, "OPERADOR_28out_ordem_prova_do_neutrino_verbatim.txt"), "7c1b85da"),
            ("jo8", os.path.join(_PRJ, "OPERADOR_28out_nome_do_triplo_Jo8_32_verbatim.txt"), "97700220"),
            ("concordo", os.path.join(_PRJ, "OPERADOR_28out_ratificacao_concordo_com_tudo_verbatim.txt"), "232ca83c")]
VERBATIM_ORIGEM_V404 = [p_ for _, p_, _ in _VERB404]
VERBATIM_PREFIXOS_DA_ORDEM_V404 = [h_ for _, _, h_ in _VERB404]
VERBATIM_AUTOR_V404 = ["operador"] * len(_VERB404)
VERBATIM_QUANDO_V404 = "28/10/2026 (cunhagem)"
VERBATIM_CHAVE_PREFIXO_V404 = "v404_cun_"
IDX404 = {n_: i_ for i_, (n_, _, _) in enumerate(_VERB404)}
BOCAS_IDX, CALIBRAR_IDX, UMABS_IDX, TRANSICAO_IDX, SOMBRA_IDX, PROJECAO_IDX, ORDEM_PROVA_IDX, JO8_IDX, CONCORDO404_IDX = (IDX404[n_] for n_ in ("quatro_bocas", "calibrar", "um_absoluto", "transicao", "sombra", "projecao", "ordem_prova", "jo8", "concordo"))
# trechos das falas citados VERBATIM (cada um e' substring da fala indicada, com a grafia dele; a cadeia confere por script; a parafrase da gerencia nunca entra entre aspas)
FRASE_PEDAGIO = "pedágio de planck lido na propagação"                                   # fala 0
FRASE_RETORNO_83 = "1 retorno em 83 raios eu leio como sendo a matéria"                  # fala 0
FRASE_CALIBRAR = "calibrar Não significa validar"                                        # fala 1 (grafia dele: «Não» com maiuscula)
FRASE_NUMERO_CORRIGINDO = "é o número corrigindo a rota"                                 # fala 1
FRASE_UM_ABSOLUTO = "eu posso definir o um absoluto como o estado de energia fundamental cuja inscrição no radical entrópico quebra a simetria e inaugura o defasamento"   # fala 2
FRASE_TRANSICAO = "então agora conseguimos fazer a transição para a massa"               # fala 3
FRASE_SOMBRA = "A matéria é a sombra de betatgl, então?"                                 # fala 4
FRASE_PROJECAO_EIXO = "a matéria é a projeção do eixo transversal"                       # fala 5
FRASE_DERIVADA = "então a matéria não é proporcional, ela seria a derivada"              # fala 5
FRASE_ORDEM_PROVA = "veja se consegue fazer a prova do neutrino para derivarmos e não ser mais postulado"   # fala 6
FRASE_JO8 = "só consegui sintetizar assim: Jo8:32"                                       # fala 7
FRASE_CONCORDO404 = "Perfeito, concordo com tudo"                                        # fala 8
FRASES_V404 = [(BOCAS_IDX, FRASE_PEDAGIO), (BOCAS_IDX, FRASE_RETORNO_83), (CALIBRAR_IDX, FRASE_CALIBRAR), (CALIBRAR_IDX, FRASE_NUMERO_CORRIGINDO), (UMABS_IDX, FRASE_UM_ABSOLUTO), (TRANSICAO_IDX, FRASE_TRANSICAO), (SOMBRA_IDX, FRASE_SOMBRA),
               (PROJECAO_IDX, FRASE_PROJECAO_EIXO), (PROJECAO_IDX, FRASE_DERIVADA), (ORDEM_PROVA_IDX, FRASE_ORDEM_PROVA), (JO8_IDX, FRASE_JO8), (CONCORDO404_IDX, FRASE_CONCORDO404)]
# as leituras [ONTO]/[INPUT] da v404 (nada disto e' termo de kernel)
LEVANTAMENTO_ARQ = os.path.join(_TRM, "LEVANTAMENTO_TRANSICAO_PARA_A_MASSA_28out.md")
LEITURA_MASSA_28OUT = {"identificacao": "a massa e' a projecao do eixo transversal do estado inscrito (nao e' proporcional ao raio de beta, e' a derivada): o angulo agudo do neutrino e' a Meia-Nat, 45 graus; leitura do operador, 28/10/2026 [ONTO]",
                       "jo8_32": "Jo 8,31-32 («E conhecereis a verdade, e a verdade vos libertará»): permanecer na palavra e' o Caminho; conhecer e' a Verdade (ler, e reler nao acrescenta); libertar e' a Vida (a queda com chao); leitura da gerencia c1, ratificada pelo operador [ONTO]",
                       "pedagio": "o pedagio de Planck lido na propagacao: o pagamento e' o Nome inteiro (1 absoluto) se esvaziando por inteiro para se tornar ambiente de espaco temporalizado (zero modular); 1 absoluto = zero modular e' relativo, expressa a preservacao da identidade; leitura do operador, 28/10/2026 [ONTO]",
                       "um_absoluto": "o um absoluto como o estado de energia fundamental cuja inscricao no radical entropico quebra a simetria e inaugura o defasamento: cunhagem do operador, 28/10/2026, ainda sem derivacao [INPUT/ONTO]",
                       "e0": "E0 (a escala do neutrino, 1 eV no programa) e' DECLARADO e continua [OPEN]; a escala que zera a tensao do m2 e' 1,02 eV (conta da gerencia c1, 28/10/2026 [DERIVED]); a unica massa derivada de beta no programa e' a do neutrino (levantamento de 28/10/2026)",
                       "estatuto": "[ONTO -- leituras do operador, ratificadas em 28/10/2026 (sha16 232ca83c29c031a5); nada disto e' termo de kernel]"}


def verbatins404(destino_cunhagens):
    """As falas de 28/10 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor}. A copia duravel NAO e' escrita aqui. Os prefixos de sha256
    que a ordem deu sao conferidos contra o arquivo; cada trecho citado (FRASES) e' substring VERBATIM da fala indicada."""
    out = []
    for p, pref, autor in zip(VERBATIM_ORIGEM_V404, VERBATIM_PREFIXOS_DA_ORDEM_V404, VERBATIM_AUTOR_V404):
        b = open(p, "rb").read(); h = sha256(b)
        assert h.startswith(pref), ("o arquivo da fala NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO_V404 + h[:16], "quando": VERBATIM_QUANDO_V404, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert len(out) == 9 and all(v["autor"] == "operador" for v in out), "tem de haver NOVE falas, todas do operador"
    for i, fr in FRASES_V404:
        assert fr in out[i]["text"], ("o trecho citado NAO e' verbatim na fala", i, fr[:60])
    return out


def pedras_fontes():
    """As DUAS pedras LIDAS do disco: lista de dicts {stone, origem, copia (v404\\pedra), sha256, bytes}. O sha16 e' conferido contra o que a ordem deu (pedras_sha16_da_ordem.json). A copia NAO e' escrita aqui."""
    out = []
    for s in STONES:
        b = open(s["origem"], "rb").read(); h = sha256(b)
        assert h[:16] == s["sha16_da_ordem"], ("a pedra no disco NAO e' a que a ordem pinou", s["name"], h[:16], s["sha16_da_ordem"])
        out.append({"stone": s["name"], "origem": s["origem"], "copia": s["src"], "sha256": h, "bytes": len(b)})
    return out

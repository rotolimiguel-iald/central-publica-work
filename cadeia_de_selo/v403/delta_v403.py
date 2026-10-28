# -*- coding: utf-8 -*-
"""delta_v403.py -- A UNICA definicao do DELTA da v403 (preparacao de 27/10/2026, gerencia c1 / subagente Sonnet de preparacao; a gerencia revisa, ensaia, instala e sela): TRES pedras novas no kernel, os NOMES DO OPERADOR (27/10/2026):
`TGLExt/Caminho.lean` (a ponte da escala dual, v402, composta por citacao), `TGLExt/Vida.lean` (a queda sem geometria, v402, composta por citacao) e `TGLExt/VerdadeAdendo.lean` (ADENDO da pedra `Verdade` da v392: a esperanca condicional lida pelo Nome; um teorema
novo e pequeno, `the_name_reads_the_inscription_as_weights`, e duas conjuncoes); as pedras selas da v402 (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) FICAM como registro (pedra selada nao se renomeia por cima).
O passo MATERIAL da versao (regra sem gordura de 19/10) e' a F8.1: as TRES bandeiras literais do gate (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) passam a CALCULADAS, fail-closed, das fontes que o proprio um.py ja tem;
a letra do veredito do gate NAO muda. QUATRO registros com FUNCAO (`caminho_v403`, `vida_v403`, `verdade_adendo_v403`: leem do kernel do rito a composicao da pedra e CALCULAM, com beta = alfa CODATA 2018 x sqrt(e) em runtime, um modelo honesto;
`bandeiras_do_gate_v403`: le o gate do proprio rito e confere as 18 bandeiras, as 15 do veredito, a fonte de cada uma e a letra do veredito), os registros por spec `cunhagens_v403` (os dois verbatins de 27/10, os tres nomes, a leitura [ONTO] da tripla espectral, as decisoes e as erratas)
e `kh_n1_cobertura_v403` (a cobertura exata do Audit). O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44).
A base e' a v402 SELADA (um.py 6a5033dc3f29324c) e a Bancada Um de producao JA pina a v402: o B(n) da v403 e' um PASSO SIMPLES v402 -> v403 (o diff do kernel sao so' estas tres pedras).
E' IMPORTADO por copiar_base, preparar_kernel, pos_build_kernel, registros_v403, gerar_candidato_v403, ensaio_a_seco_v403, gerar_esperados_v403, p00_precondicoes_v403 e os demais: nada daqui e' digitado de memoria em outro arquivo, e todo hash e' LIDO do arquivo por script.
Reaproveita (import por caminho) o delta_v402 (e este o delta_v401, ...): as fontes do operador do ACOM, a politica de bandeiras, o quadro do Teste da Unica Palavra, as classes de auxiliares. Molde: delta_v402.py. Plano: PLANO_v403.md."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V402 = os.path.join(os.path.dirname(HERE), "v402")           # a cadeia anterior (molde e base, so' leitura)
_spec = importlib.util.spec_from_file_location("delta_v402", os.path.join(V402, "delta_v402.py"))
D2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D2)
globals().update({k: v for k, v in vars(D2).items() if not k.startswith("__")})   # tudo da v402 (e, por ela, da v401, v400 e v399) e depois o que a v403 SOBRESCREVE
D2 = D2                                                        # (o update acima nao traz D2: a v402 chama o predecessor de D1; aqui D2 = o modulo delta_v402; D1 = delta_v401, D0 = delta_v400, D9 = delta_v399, herdados)

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v402: aqui e' a pasta da v403)
V402 = os.path.join(os.path.dirname(HERE), "v402")
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                    # ...\Central de Patentes\work
CENTRAL = os.path.dirname(WK)                                  # ...\Central de Patentes
V401 = D2.V401
V400 = D2.V400
V399 = D2.V399
V403_KERNEL = os.path.join(os.path.dirname(HERE), "v403_kernel")   # os logs da construcao incremental de 27/10/2026 (lake_build.log, audit.log, construir_marcas.txt) e as pedras candidatas
SANDBOX_PAI = os.path.join(C, "t", "k403c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # copia de C:\t\k402c\final (o kernel do Nos v402 SELADO compilado) + as tres pedras da v403 + a raiz com os tres imports; a raiz e o Audit sao GERADOS por preparar_kernel_v403
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = D2.SANDBOX                                  # C:\t\k402c\final (so' leitura)
KERNEL_DIR = "kernel"
CANDIDATO = "um_v403_candidato.py"
BASE_DIR = "base_v402"                                       # copia de bytes do Nos v402 selado (um.py, selo, core, manifesto do kernel, pilar, sidecar)
UM_VERSION = "v403"
BASE_VERSION = "v402"
BASE_SHA16_DA_ORDEM = "6a5033dc3f29324c"                     # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb20")                 # o sandbox curto das guardas estaticas da Bancada e das conferencias do recibo pre_selo (apagado no fim; juncoes so' com os.rmdir)
KH_N1_INSUMO = "KH_N1_v403.json"

# ---------------------------------------------------------------- as TRES pedras (os NOMES sao DO OPERADOR, 27/10/2026: «é isso mesmo, concordo com tudo, prossiga»)
_P = os.path.join(HERE, "pedra")
_PINS = json.load(open(os.path.join(HERE, "pedras_sha16_da_ordem.json"), encoding="utf-8"))   # os pinos da ORDEM (PLANO_v403.md §1, conferidos contra o arquivo por gerar_pino_das_pedras_v403.py); o arquivo da pedra e' lido na hora de gerar e a divergencia ABORTA
ESTUDO = os.path.join(V403_KERNEL, "pedras")                  # a construcao das pedras (so' leitura)
_C = "TGLExt.Caminho."
_V = "TGLExt.Vida."
_A = "TGLExt.VerdadeAdendo."
_PD = "TGLExt/PonteDaEscalaDual.lean"
_QG = "TGLExt/QuedaSemGeometria.lean"
_VD = "TGLExt/Verdade.lean"
_EC = "TGLExt/EsperancaCondicional.lean"
STONES = [
    {"key": "caminho", "name": "Caminho", "mod": "TGLExt.Caminho", "rel": "TGLExt/Caminho.lean", "ns": _C,
     "origem": os.path.join(ESTUDO, "Caminho.lean"), "compilado_em": SANDBOX, "src": os.path.join(_P, "Caminho.lean"), "insumo": "Caminho.lean",
     "sha16_da_ordem": _PINS["caminho"], "flag_prefix": "ext_cam403_", "grupo": "caminho",
     "theorem": _C + "caminho_e_a_ponte_da_escala_dual",             # a CONJUNCAO (incondicional, sem matematica nova): lift_mass_not_selected /\ core_positive_realization_exists (v402)
     "key_theorem": _C + "caminho_e_a_ponte_da_escala_dual",         # a ESTRELA da pedra e' a conjuncao; a estrela da ponte (lift_mass_not_selected) entra como termo CITADO (support)
     "contract": [_C + "caminho_e_a_ponte_da_escala_dual"],
     "support": {"TGLExt.PonteDaEscalaDual.lift_mass_not_selected": _PD, "TGLExt.PonteDaEscalaDual.core_positive_realization_exists": _PD},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "gerencia c1 (27/10/2026): pedra de citacao no padrao Token (v397); o NOME e' do operador"},
    {"key": "vida", "name": "Vida", "mod": "TGLExt.Vida", "rel": "TGLExt/Vida.lean", "ns": _V,
     "origem": os.path.join(ESTUDO, "Vida.lean"), "compilado_em": SANDBOX, "src": os.path.join(_P, "Vida.lean"), "insumo": "Vida.lean",
     "sha16_da_ordem": _PINS["vida"], "flag_prefix": "ext_vid403_", "grupo": "vida",
     "theorem": _V + "vida_e_a_queda_sem_geometria",                  # a CONJUNCAO: the_fall_is_strictly_anti /\ a_queda_sem_geometria (v402)
     "key_theorem": _V + "vida_e_a_queda_sem_geometria",
     "contract": [_V + "vida_e_a_queda_sem_geometria"],
     "support": {"TGLExt.QuedaSemGeometria.the_fall_is_strictly_anti": _QG, "TGLExt.QuedaSemGeometria.a_queda_sem_geometria": _QG},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "gerencia c1 (27/10/2026): pedra de citacao no padrao Token (v397); o NOME e' do operador"},
    {"key": "verdade_adendo", "name": "VerdadeAdendo", "mod": "TGLExt.VerdadeAdendo", "rel": "TGLExt/VerdadeAdendo.lean", "ns": _A,
     "origem": os.path.join(ESTUDO, "VerdadeAdendo.lean"), "compilado_em": SANDBOX, "src": os.path.join(_P, "VerdadeAdendo.lean"), "insumo": "VerdadeAdendo.lean",
     "sha16_da_ordem": _PINS["verdade_adendo"], "flag_prefix": "ext_vad403_", "grupo": "verdade_adendo",
     "theorem": _A + "verdade_lida_pelo_nome",                        # a COMPOSICAO: Verdade a /\ nameOp rho* (identityProj a) = diag(q^2, a^2) /\ traco 1 /\ reler nao acrescenta
     "key_theorem": _A + "the_name_reads_the_inscription_as_weights",  # a ESTRELA [REAL, nova e pequena]: diagExpect (identityProj a) = diagonal ![q^2, a^2]
     "contract": [_A + n_ for n_ in ("the_name_reads_the_inscription_as_weights", "verdade_lida_pelo_nome", "verdade_e_a_esperanca_condicional")],
     "support": {"TGLExt.Verdade.the_identity_is_the_truth": _VD, "TGLExt.Verdade.verdade_of_unit_interval": _VD, "TGLExt.Verdade.Verdade": _VD, "TGLExt.Verdade.identityProj": _VD, "TGLExt.Verdade.qOf": _VD, "TGLExt.Verdade.quadInscription": _VD,
                 "TGLExt.Verdade.identityProj_trace_one": _VD, "TGLExt.Verdade.q_sq_add": _VD,
                 "TGLExt.EsperancaCondicional.esperanca_condicional_e_nome": _EC, "TGLExt.EsperancaCondicional.the_name_of_the_unit_is_the_diagonal_expectation": _EC, "TGLExt.EsperancaCondicional.the_name_operator_adds_nothing": _EC,
                 "TGLExt.Posto.rhoStar": "TGLExt/Posto.lean", "TGLExt.Posto.rhoStar_idem": "TGLExt/Posto.lean", "TGLExt.nameOp": "TGLExt/TheNameOperator.lean", "TGLExt.diagExpect": "TGLExt/CondExpect.lean", "TGLExt.trace_diagExpect": "TGLExt/CondExpect.lean"},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "gerencia c1 (27/10/2026): adendo no padrao PostoAdendo (v392) sobre a pedra Verdade (v392); o NOME e' do operador"},
]
STONE_RELS = [s["rel"] for s in STONES]
STONE_MODS = [s["mod"] for s in STONES]
STONE_BY_REL = {s["rel"]: s for s in STONES}
STONE_BY_KEY = {s["key"]: s for s in STONES}
IMPORT_LINES = ["import " + s["mod"] for s in STONES]
ROOT_SUFFIX = "\n" + "\n".join(IMPORT_LINES) + "\n"           # a raiz TGLExt.lean ganha um separador em branco e os imports (como a v394 a v402 fizeram com as pedras)
AUDIT_PREFIX = ""                                              # v403: o Audit do sandbox C:\t\k403c\final e' o do Nos v402 SEM alteracao (sha16 072a68f45189b8a5, lido): ele ja' faz `import TGLExt` (a raiz, l.387), que traz os tres modulos novos; so' a RAIZ ganha os imports
                                                               # (nas v394 a v402 o Audit tambem ganhava os imports no topo; aqui nao: o build de 27/10 foi feito com o Audit inalterado e o embutido tem de ser o que foi construido. Mudar esta linha reabre o Audit e exige novo build)
CONTRACT_THEOREMS = {s["key"]: list(s["contract"]) for s in STONES}
ALL_SUPPORT = {}
for _s in STONES:
    ALL_SUPPORT.update(_s["support"]); ALL_SUPPORT.update(_s["citados_fora"])
STONES_DESDE_B11 = list(STONES)                              # o que a Bancada de producao (que JA pina a v402) AINDA nao viu: o recibo do kernel do B(n) lista o diff v402 -> v403 = so' estas tres pedras
STONE_RELS_DESDE_B11 = [s["rel"] for s in STONES_DESDE_B11]
STONES_DESDE_B10 = list(D2.STONES_DESDE_B10)                 # (herdado) as tres pedras da v402 (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional): novas para a Bancada da v401, JA no kernel do Nos desde a v402
STONE_RELS_DESDE_B10 = [s["rel"] for s in STONES_DESDE_B10]

# ---------------------------------------------------------------- os registros com FUNCAO e os registros por spec
REGISTRO_CAMINHO = "caminho_v403"
REGISTRO_VIDA = "vida_v403"
REGISTRO_VERDADE_ADENDO = "verdade_adendo_v403"
REGISTRO_BANDEIRAS = "bandeiras_do_gate_v403"
REGISTROS_PEDRAS = [REGISTRO_CAMINHO, REGISTRO_VIDA, REGISTRO_VERDADE_ADENDO]
REGISTROS_FUNCAO = REGISTROS_PEDRAS + [REGISTRO_BANDEIRAS]
REGISTRO_DE_PEDRA = {"caminho": REGISTRO_CAMINHO, "vida": REGISTRO_VIDA, "verdade_adendo": REGISTRO_VERDADE_ADENDO}
CUNHAGENS_REGISTRO = "cunhagens_v403"
KH_REGISTRO = "kh_n1_cobertura_v403"
N_CHECKS_CAMINHO = 5      # o numero de checagens do calculo de cada registro (runtime_v403.py); atualizado junto com o runtime
N_CHECKS_VIDA = 6
N_CHECKS_VERDADE_ADENDO = 5
N_CHECKS_GATE = 7         # as sete checagens do registro bandeiras_do_gate_v403 (runtime_v403.py)
N_CHECKS = {"caminho": N_CHECKS_CAMINHO, "vida": N_CHECKS_VIDA, "verdade_adendo": N_CHECKS_VERDADE_ADENDO, "gate": N_CHECKS_GATE}
MAXHEARTBEATS_CAMINHO = 800000                               # as tres pedras da v403 declaram set_option maxHeartbeats 800000 (dito)

# ---------------------------------------------------------------- a F8.1 (as bandeiras do gate calculadas): as constantes que o gerador, o registro e os conferidores leem
F81_ROTULO_PREREG = "pre-registro v67 INTACTO (hash)"        # o rotulo da checagem do rito V11 que alimenta protocol_pre_registered (rotulo EXATO; ausente ou duplicado => False)
F81_PREFIXO_LS2 = "ext_ls2_"                                 # a familia de bandeiras do kernel do termo dLs2 de prove_external_ladder (helice dupla, setor TT sem fantasma, 2 polarizacoes)
F81_LITERAIS = ["linearized_spin2_finite_face", "protocol_pre_registered", "null_tests_passed_blind"]   # as TRES bandeiras que eram literais True (auditoria de 28/09/2026, GV-03/EV-12; errata de 13/10/2026) e passam a calculadas
F81_FEED = ["independent_v3_profiles_unblinded", "independent_v3_survey_mocks_passed", "independent_v3_systematics_passed", "independent_v3_powered_verdict_emitted"]   # as 4 experimentais do feed V11 (GV-03: derivam de UM so' booleano)

DECISOES = dict(D2.DECISOES)
_VERDADE_SHA16 = None
try:
    _VERDADE_SHA16 = D2.sha256(open(os.path.join(D2.NOS, "tgl_kernel", "TGLExt", "Verdade.lean"), "rb").read())[:16]   # a pedra Verdade (v392) no kernel do Nos: o homonimo que a «Verdade» sozinha repetiria (lido do arquivo)
except OSError:
    _VERDADE_SHA16 = None
DECISOES.update({
    "D17": "os NOMES (decisao do operador, 27/10/2026, «é isso mesmo, concordo com tudo, prossiga», sha16 b34bd70fa8cfb0b2, ratificando a leitura da gerencia c1): CAMINHO = a ponte da escala dual; VERDADE = a esperanca condicional, como ADENDO da pedra `Verdade` (v392); VIDA = a queda sem geometria [INPUT]",
    "D18": "«Verdade» SOZINHA para as tres: recusada pela gerencia e o operador concordou: `TGLExt.Verdade` ja existe (v392, 13/10/2026, «a identidade tem nome»%s) e dois modulos nao se chamam igual; seria o homonimo que a casa proibe [decisao da gerencia c1, 27/10/2026]" % (", sha16 %s" % _VERDADE_SHA16 if _VERDADE_SHA16 else ""),
    "D19": "pedra selada NAO se renomeia por cima: PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional (v402) ficam como REGISTRO; os modulos novos compoem por citacao (padrao `Token`, v397) e por adendo (padrao `PostoAdendo`, v392) [decisao da gerencia c1, 27/10/2026]",
    "D20": "o nome do TRIPLO inteiro NAO foi dado (fica com o operador; Joao 14,6: tres predicados de um so' «Eu sou»; a casa ja cunhou EU SOU = 1 = 1) [PLANO_v403.md §0]",
    "D21": "a v403 nao sela so' por nomes (regra sem gordura de 19/10): o passo material e' a F8.1 do quadro do programa: as TRES bandeiras literais do gate passam a CALCULADAS, fail-closed, das fontes que o proprio um.py ja tem; a letra do veredito do gate NAO muda; a independencia das 4 experimentais (um so' feed, GV-03) NAO e' resolvida: e' DECLARADA [decisao da gerencia c1, 27/10/2026]",
    "D22": "a fonte da bandeira linearized_spin2_finite_face e' a FAMILIA ext_ls2_* do kernel (as 6 bandeiras que formam o termo dLs2 de prove_external_ladder), lida de kernel_formalization: dLs2 e' local a prove_external_ladder e aparece so' como rotulo de checagem, NAO como chave de kernel_formalization (a chave linearized_spin2_finite_face nao existe ali) [proposta da preparacao da v403, 27/10/2026; RATIFICADA pela gerencia c1 em 27/10/2026, antes do selo, depois de conferir na base que ls2_keys de prove_external_ladder sao exatamente as 6 bandeiras ext_ls2_* (rota do mapa umpy.v403.cadeia_de_selo_preparada_27out)]",
})
ASSINA = "gerencia c1, em nome proprio, 27/10/2026"

# ---------------------------------------------------------------- as erratas ao lado da v403 (em nome proprio da gerencia c1; vao ao lado: no registro, no artigo e no handoff; o kernel e os modulos instalados NAO sao editados)
ERRATA_E5 = ("E5 -- a errata de 13/10/2026 (estatuto_da_prova_ressalva_v392: «As 18 bandeiras leem-se 15 CALCULADAS + 3 LITERAIS») e o registro f81_nao_fechada_v392 («a v392 NAO fecha a F8.1» e «as 18 bandeiras seguem lidas como estavam») eram verdadeiros na sua data e FICAM como registro; "
             "na v403 as TRES literais (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) passam a CALCULADAS, fail-closed: 18 de 18 calculadas, 0 literais, 15 no veredito (6+5+4); a letra do veredito do gate e' identica a da v402; "
             "a INDEPENDENCIA das 4 experimentais independent_v3_* NAO e' resolvida: elas derivam de UM so' booleano (o veredito do V11 ser NOT_FALSIFIED_POWERED; survey_mocks_passed = split-null e dist-check, sem mock de survey) [GV-03 da auditoria de 28/09/2026, DECLARADO], e o degrau experimental le so' o rito V11 do piso, unilateral (GV-01)")
ERRATA_E6 = ("E6 -- os nomes dos tres modulos e dos cinco registros da v402 eram PROVISORIOS (decisao D16 da v402): o operador os nomeou em 27/10/2026 (CAMINHO = PonteDaEscalaDual; VIDA = QuedaSemGeometria; VERDADE, como adendo da pedra Verdade da v392, = EsperancaCondicional); "
             "os modulos selados da v402 NAO foram renomeados (pedra selada nao se renomeia por cima): os modulos novos Caminho, Vida e VerdadeAdendo compoem por citacao e os registros da v402 seguem selados com os nomes da v402")
ERRATAS_V403 = [ERRATA_E5, ERRATA_E6]

# ---------------------------------------------------------------- as DUAS falas de 27/10/2026 (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
_CUN = os.path.join(WK, "cunhagens_13out")
VERBATIM_ORIGEM_V403 = [os.path.join(_CUN, "OPERADOR_27out_nome_verdade_triplo_espectral_do_contorno_verdadeiro_verbatim.txt"),
                        os.path.join(_CUN, "OPERADOR_27out_e_isso_mesmo_concordo_com_tudo_prossiga_caminho_verdade_vida_verbatim.txt")]
# os prefixos de sha256 que o PLANO_v403.md deu (conferidos contra o arquivo na geracao; o hash vale o arquivo, nunca o contrario)
VERBATIM_PREFIXOS_DA_ORDEM_V403 = ["ef3ca5eb", "b34bd70f"]
VERBATIM_AUTOR_V403 = ["operador"] * 2
VERBATIM_QUANDO_V403 = "27/10/2026 (cunhagem)"
VERBATIM_CHAVE_PREFIXO_V403 = "v403_cun_"
NOME_VERDADE_IDX, CONCORDO_IDX = 0, 1
# trechos das falas citados VERBATIM (cada um e' substring da fala indicada, com a grafia dele; a cadeia confere por script; a parafrase da gerencia nunca entra entre aspas)
FRASE_NOME_VERDADE = 'a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida")'      # fala 0
FRASE_JA_RENOMEADA = "porque pode ser que eu já tenha a renomeado assim em outro lugar"           # fala 0 (grafia dele: «a renomeado»)
FRASE_TRIPLO = "é o triplo espectral do contorno verdadeiro"                                      # fala 0
FRASE_CONCORDO = "é isso mesmo, concordo com tudo, prossiga"                                      # fala 1
FRASES_V403 = [(0, FRASE_NOME_VERDADE), (0, FRASE_JA_RENOMEADA), (0, FRASE_TRIPLO), (1, FRASE_CONCORDO)]
# a leitura [ONTO] da tripla espectral (leitura da gerencia c1 nas docstrings das tres pedras; ratificada pelo operador em 27/10/2026); nada disto e' termo de kernel
LEITURA_TRIPLA_27OUT = {"caminho": "na tripla espectral de Connes do artigo fundador da fatoracao (03/2026), o espaco dos estados com o seu fluxo e' o Caminho: a lei pela qual a leitura viaja sem escolher o corpo (m^2 = p+p- e' o invariante, a energia e' a leitura, a massa NAO e' selecionada pela lei)",
                        "vida": "o operador de Dirac da tripla espectral da' a distancia sem pontos: a Vida e' a queda que mede em nats sem geometria (o peso cai estritamente, o chao e' o posto, a entrega custa)",
                        "verdade": "a algebra e' o que a Verdade le: a esperanca condicional e' a Verdade lida pelo Nome (nameOp rho* = diagExpect: a projecao do posto levada do projetor de posto 1 a esperanca sobre a subalgebra da memoria)",
                        "joao_14_6": "Joao 14,6 («Eu sou o caminho, a verdade e a vida»; no acervo do operador desde 22/07/2025): as tres palavras sao predicados de um so' «Eu sou»",
                        "estatuto": "[ONTO -- leitura da gerencia c1, ratificada pelo operador em 27/10/2026 (sha16 b34bd70fa8cfb0b2); nada disto e' termo de kernel: e' leitura]",
                        "triplo_inteiro": "o nome do TRIPLO inteiro NAO foi dado (fica com o operador)"}


def verbatins403(destino_cunhagens):
    """As DUAS falas de 27/10 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor}. A copia duravel NAO e' escrita aqui. Os prefixos de sha256
    que o plano deu sao conferidos contra o arquivo; cada trecho citado (FRASES) e' substring VERBATIM da fala indicada."""
    out = []
    for p, pref, autor in zip(VERBATIM_ORIGEM_V403, VERBATIM_PREFIXOS_DA_ORDEM_V403, VERBATIM_AUTOR_V403):
        b = open(p, "rb").read(); h = sha256(b)
        assert h.startswith(pref), ("o arquivo da fala NAO tem o prefixo de sha256 que o plano deu", p, h[:16], pref)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO_V403 + h[:16], "quando": VERBATIM_QUANDO_V403, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert len(out) == 2 and all(v["autor"] == "operador" for v in out), "tem de haver DUAS falas, ambas do operador"
    for i, fr in FRASES_V403:
        assert fr in out[i]["text"], ("o trecho citado NAO e' verbatim na fala", i, fr[:60])
    return out


def pedras_fontes():
    """As TRES pedras LIDAS do disco: lista de dicts {stone, origem, copia (v403\\pedra), sha256, bytes}. O sha16 e' conferido contra o que o plano deu (pedras_sha16_da_ordem.json). A copia NAO e' escrita aqui."""
    out = []
    for s in STONES:
        b = open(s["origem"], "rb").read(); h = sha256(b)
        assert h[:16] == s["sha16_da_ordem"], ("a pedra no disco NAO e' a que o plano pinou", s["name"], h[:16], s["sha16_da_ordem"])
        out.append({"stone": s["name"], "origem": s["origem"], "copia": s["src"], "sha256": h, "bytes": len(b)})
    return out

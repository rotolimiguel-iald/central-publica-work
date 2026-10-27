# -*- coding: utf-8 -*-
"""delta_v402.py -- A UNICA definicao do DELTA da v402 (preparacao de 26/10/2026, gerencia c1): TRES pedras novas no kernel, `TGLExt/PonteDaEscalaDual.lean` (modulo do Codex, ORDEM 025, copia de bytes, exame independente INTEGRAR_COM_ERRATA_AO_LADO),
`TGLExt/QuedaSemGeometria.lean` e `TGLExt/EsperancaCondicional.lean` (work\\pedras_v402; nomes PROVISORIOS, o operador nomeia), TRES registros com FUNCAO (`ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402`: leem do kernel do rito a composicao
de cada pedra e CALCULAM, com beta = alfa CODATA 2018 x sqrt(e) em runtime, um modelo honesto de cada uma), os registros por spec `cunhagens_v402` (as TRES inscricoes de 26/10, as decisoes da gerencia, a pergunta e a resposta de 26/10 como leitura [INPUT/ONTO] e as erratas E1-E4)
e `kh_n1_cobertura_v402` (a cobertura exata do Audit), a ERRATA AO LADO sobre H_tau no artigo e nos registros (NAO no kernel: nenhum modulo instalado e' editado), o artigo (secao «A ponte da escala dual, a queda sem geometria e a esperanca condicional») e a POLITICA DE BANDEIRAS (a da v394:
so' declaracao NOMEADA). O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44).
A base e' a v401 SELADA (um.py 1925cb691e933ae8) e a Bancada Um de producao JA pina a v401 (B10): o B(n) da v402 e' um PASSO SIMPLES v401 -> v402 (o diff do kernel sao so' estas tres pedras).
E' IMPORTADO por copiar_base, preparar_kernel, pos_build_kernel, registros_v402, gerar_candidato_v402, ensaio_a_seco_v402, gerar_esperados_v402, p00_precondicoes_v402 e os demais: nada daqui e' digitado de memoria em outro arquivo, e todo hash e' LIDO do arquivo por script.
Reaproveita (import por caminho) o delta_v401 (e este o delta_v400, o delta_v399): as fontes do operador do ACOM, a politica de bandeiras, o quadro do Teste da Unica Palavra, as classes de auxiliares. Molde: delta_v401.py."""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V401 = os.path.join(os.path.dirname(HERE), "v401")           # a cadeia anterior (molde e base, so' leitura)
_spec = importlib.util.spec_from_file_location("delta_v401", os.path.join(V401, "delta_v401.py"))
D1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D1)
globals().update({k: v for k, v in vars(D1).items() if not k.startswith("__")})   # tudo da v401 (e, por ela, da v400 e da v399) e depois o que a v402 SOBRESCREVE

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v401: aqui e' a pasta da v402)
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                    # ...\Central de Patentes\work
CENTRAL = os.path.dirname(WK)                                  # ...\Central de Patentes
V400 = D1.V400
V399 = D1.V399
SANDBOX_PAI = os.path.join(C, "t", "k402c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # copia de C:\t\k401c\final (o kernel do Nos v401 SELADO compilado); a raiz e o Audit sao GERADOS por preparar_kernel_v402
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = D1.SANDBOX                                  # C:\t\k401c\final (so' leitura)
KERNEL_DIR = "kernel"
CANDIDATO = "um_v402_candidato.py"
BASE_DIR = "base_v401"                                       # copia de bytes do Nos v401 selado (um.py, selo, core, manifesto do kernel, pilar, sidecar)
UM_VERSION = "v402"
BASE_VERSION = "v401"
BASE_SHA16_DA_ORDEM = "1925cb691e933ae8"                     # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb19")                 # o sandbox curto das guardas estaticas da Bancada e das conferencias do recibo pre_selo (apagado no fim; juncoes so' com os.rmdir)
KH_N1_INSUMO = "KH_N1_v402.json"

# ---------------------------------------------------------------- as TRES pedras (os NOMES dos modulos sao PROVISORIOS: o operador nomeia; o da ponte e' o do Codex, ORDEM 025)
_P = os.path.join(HERE, "pedra")
_PINS = json.load(open(os.path.join(HERE, "pedras_sha16_da_ordem.json"), encoding="utf-8"))   # os pinos da ORDEM da gerencia; o arquivo da pedra e' lido na hora de gerar e a divergencia ABORTA
ORDEM025_ARQ = os.path.join(CENTRAL, "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_025", "PonteDaEscalaDual.lean")   # pasta SO' LEITURA do Codex: so' o .lean e' copiado (condicao C1 do exame)
ESTUDO = os.path.join(WK, "pedras_v402")                      # a construcao das pedras B e C (so' leitura)
_K = "TGLExt.PonteDaEscalaDual."
_Q = "TGLExt.QuedaSemGeometria."
_E = "TGLExt.EsperancaCondicional."
STONES = [
    {"key": "ponte", "name": "PonteDaEscalaDual", "mod": "TGLExt.PonteDaEscalaDual", "rel": "TGLExt/PonteDaEscalaDual.lean", "ns": _K,
     "origem": ORDEM025_ARQ, "compilado_em": os.path.join(C, "t", "k402x", "final"), "src": os.path.join(_P, "PonteDaEscalaDual.lean"), "insumo": "PonteDaEscalaDual.lean",
     "sha16_da_ordem": _PINS["ponte"], "flag_prefix": "ext_pde402_", "grupo": "ponte",
     "theorem": _K + "core_positive_realization_exists",            # a realizacao no nucleo CANONICO (traco finito positivo): existe um estado com p+ > 0, m^2 = mu^2 e E > 0 para todo mu^2 >= 0
     "key_theorem": _K + "lift_mass_not_selected",                   # a ESTRELA: a lei de escala deixa a massa livre (dois invariantes distintos, o MESMO p+); com positive_weight_cannot_be_invariant_mass, H_tau na forma literal e' REFUTADA
     "contract": [_K + n_ for n_ in ("theta_energy", "theta_momentum", "pPlus_scaling", "pMinus_scaling", "theta_zero", "theta_add", "inertial_momentum_is_zero", "rest_post_exists_and_moves", "positive_weight_stays_positive", "mass_is_the_invariant",
                                     "mass_is_minkowski", "energy_is_the_reading", "observer_energy_changes", "mass_is_eta4", "boost_is_existing_4D_block", "embed_equivariant", "rest_energy_eq_mc2", "lift_pPlus", "lift_pMinus", "lift_mass",
                                     "null_coordinates_injective", "lift_equivariant", "lift_mass_not_selected", "invariant_weight_is_zero", "positive_weight_cannot_be_invariant_mass", "lift_future", "lift_rest_energy", "core_lift_equivariant",
                                     "core_positive_realization_exists", "momentumScaling", "lift", "coreLift")],
     "support": {"TGLExt.boost": "TGLExt/BisognanoWichmann.lean", "TGLExt.boost_zero": "TGLExt/BisognanoWichmann.lean", "TGLExt.boost_add": "TGLExt/BisognanoWichmann.lean", "TGLExt.boostMat": "TGLExt/PoincareGroup.lean", "TGLExt.eta4": "TGLExt/Solder4D.lean",
                 "TGLExt.DualScalingData": "TGLExt/GlobalLiftLadder.lean", "TGLExt.Fundacao.the_floor_fixes_the_cut": "TGLExt/Fundacao.lean",
                 "TGLExt.FalsidadeDaInercia.Inertial": "TGLExt/FalsidadeDaInercia.lean", "TGLExt.FalsidadeDaInercia.IsPost": "TGLExt/FalsidadeDaInercia.lean",
                 "TGLExt.FalsidadeDaInercia.the_inertia_is_the_absolute_zero": "TGLExt/FalsidadeDaInercia.lean", "TGLExt.FalsidadeDaInercia.a_post_is_not_inertial": "TGLExt/FalsidadeDaInercia.lean",
                 "ChatgptAudit.BoostBridges016.boost_is_first_block": "TGLExt/O16/BoostRepresentationBridges.lean", "F12Completion.finiteTracePositive_has_positive": "TGLExt/AgapeNonVacuity.lean",
                 "TGLV351.regularCoreDualScalingData": "TGLExt/V351DualScalingBridge.lean", "TGLV351.finiteTraceDual": "TGLExt/V351DualScalingBridge.lean", "TGLV351.FiniteTracePositive": "TGLExt/V351DualScalingBridge.lean",
                 "TGLExt.SiteProfile": "TGLExt/TowerDefinite.lean"},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "Codex (ORDEM 025, sha16 3fd2b5a801071343); exame independente da gerencia c1 (26/10/2026): INTEGRAR_COM_ERRATA_AO_LADO"},
    {"key": "queda", "name": "QuedaSemGeometria", "mod": "TGLExt.QuedaSemGeometria", "rel": "TGLExt/QuedaSemGeometria.lean", "ns": _Q,
     "origem": os.path.join(ESTUDO, "QuedaSemGeometria.lean"), "compilado_em": os.path.join(C, "t", "k402", "final"), "src": os.path.join(_P, "QuedaSemGeometria.lean"), "insumo": "QuedaSemGeometria.lean",
     "sha16_da_ordem": _PINS["queda"], "flag_prefix": "ext_qsg402_", "grupo": "queda",
     "theorem": _Q + "a_queda_sem_geometria",                         # a COMPOSICAO: o peso cai estritamente, a seta e' o sinal de s, o piso e' o posto, a entrega custa, o regime angular so' le, a isotropia e' nomeada
     "key_theorem": _Q + "the_fall_is_strictly_anti",                 # a ESTRELA: s |-> tau(theta_s m) e' estritamente decrescente (a fase cai, sem fim)
     "contract": [_Q + n_ for n_ in ("the_fall_is_a_loss_of_measure", "the_fall_is_strictly_anti", "the_fall_in_nats_is_s", "the_fall_depends_only_on_the_weight", "the_fall_is_the_fall_of_the_weight", "the_arrow_is_the_sign_of_s",
                                     "the_floor_is_the_post_and_is_never_touched", "surrender_is_the_cost", "relaxation_to_the_attractor", "periodic_limit_is_constant", "Smat_add_two_pi", "Smat_pi", "Smat_has_no_limit",
                                     "the_two_regimes_of_one_orbit", "the_labyrinth_reads_the_angle", "IsotropicPost", "clausius_everywhere_from_one_wedge_by_covariance", "IsotropicPostOver", "clausius_everywhere_from_base_wedges",
                                     "isotropic_post_is_inhabited", "covariance_is_load_bearing", "namedAtlasH3_iff_all_indices", "namedAtlasH3_of_one_screen", "namedAtlasH3_of_one_screen_per_orbit", "a_queda_sem_geometria")],
     "support": {"TGLExt.DualScalingData": "TGLExt/GlobalLiftLadder.lean", "TGLExt.Fundacao.the_floor_fixes_the_cut": "TGLExt/Fundacao.lean", "TGLExt.FullStaticWitness": "TGLExt/NoFullWitness.lean",
                 "TGLExt.diagFlow": "TGLExt/BoundaryException.lean", "TGLExt.permanent": "TGLExt/ObserverInside.lean", "TGLExt.observerProj": "TGLExt/ObserverInside.lean", "TGLExt.Smat": "TGLExt/SMatrix.lean",
                 "TGLExt.boost": "TGLExt/BisognanoWichmann.lean", "TGLExt.IALDJones.orbit": "TGLExt/IALDJones.lean", "TGLExt.IALDJones.angular_orbit_periodic": "TGLExt/IALDJones.lean", "TGLExt.IALDJones.angular_orbit_no_limit": "TGLExt/IALDJones.lean",
                 "TGLExt.IALDJones.orbit_tendsto_center": "TGLExt/IALDJones.lean", "ChatgptAudit.PolarPeriod016.AngularQuotientFaithful": "TGLExt/O16/PolarMinimalPeriod_v2.lean", "ChatgptAudit.PolarPeriod016.faithful_period_iff": "TGLExt/O16/PolarMinimalPeriod_v2.lean",
                 "ChatgptAudit.Wick016.rotation_two_pi": "TGLExt/O16/WickBoostRotation_v2.lean", "ChatgptAudit.Wick016.wickW": "TGLExt/O16/WickBoostRotation_v2.lean", "ChatgptAudit.Wick016.complexBoost": "TGLExt/O16/WickBoostRotation_v2.lean",
                 "TGLExt.Palavra.the_face_does_not_close": "TGLExt/Palavra.lean", "TGLExt.Palavra.the_read_face_closes": "TGLExt/Palavra.lean", "ChatgptAudit.F23CurvedFieldLigand.NamedAtlasH3": "TGLExt/LiganteLeiCampoCurvo.lean"},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "agente construtor Sonnet (26/10/2026; quem construiu nao aprova); decisoes 1-3 da gerencia c1 aplicadas"},
    {"key": "esperanca", "name": "EsperancaCondicional", "mod": "TGLExt.EsperancaCondicional", "rel": "TGLExt/EsperancaCondicional.lean", "ns": _E,
     "origem": os.path.join(ESTUDO, "EsperancaCondicional.lean"), "compilado_em": os.path.join(C, "t", "k402", "final"), "src": os.path.join(_P, "EsperancaCondicional.lean"), "insumo": "EsperancaCondicional.lean",
     "sha16_da_ordem": _PINS["esperanca"], "flag_prefix": "ext_ecn402_", "grupo": "esperanca",
     "theorem": _E + "esperanca_condicional_e_nome",                  # a COMPOSICAO: nameOp rho* = diagExpect em M2(C); preserva o Um; reler nao acrescenta; memoria-subalgebra; bimodular; compressao pelo espelho; indice 1/b (CONDICIONAL a hpp, hopt)
     "key_theorem": _E + "the_name_of_the_unit_is_the_diagonal_expectation",   # a ESTRELA: nameOp rho* x = diagExpect x (o Nome da unidade e' a esperanca diagonal)
     "contract": [_E + n_ for n_ in ("RereadAddsNothing", "every_expectation_preserves_the_one", "every_name_preserves_the_one", "the_scalar_expectation_adds_nothing", "the_diagonal_expectation_adds_nothing", "the_parity_average_adds_nothing",
                                     "the_parity_average_preserves_the_one", "the_name_operator_adds_nothing", "the_observer_reading_adds_nothing", "rereading_the_name_adds_nothing", "the_name_memory_is_a_subalgebra", "the_name_preserves_the_one",
                                     "the_name_of_the_unit_is_the_diagonal_expectation", "the_name_of_the_unit_is_bimodular", "the_mirror_compression_is_the_expectation", "the_mirror_compression_is_the_name",
                                     "the_index_of_the_name_is_one_over_beta", "esperanca_condicional_e_nome")],
     "support": {"TGLExt.nameOp": "TGLExt/TheNameOperator.lean", "TGLExt.diagExpect": "TGLExt/CondExpect.lean", "TGLExt.trExpect": "TGLExt/CondExpect.lean", "TGLExt.eD": "TGLExt/CondExpect.lean", "TGLExt.eTr": "TGLExt/CondExpect.lean",
                 "TGLExt.Lmul": "TGLExt/LeftRight.lean", "TGLExt.Posto.rhoStar": "TGLExt/Posto.lean", "TGLExt.PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect": "TGLExt/PostoAdendo.lean", "TGL.NameIndex.ppIndex": "TGL/NameIndex.lean",
                 "TGL.NameIndex.IsPPLowerBound": "TGL/NameIndex.lean", "TGLExt.projPlus": "TGLExt/TheAngleIsTheProjection.lean", "TGLExt.angFamily": "TGLExt/TheAngleIsTheProjection.lean",
                 "TGLExt.observing_adds_nothing": "TGLExt/TheObserverReadsTheAngle.lean", "TGLExt.IALDJones.iald_reads_the_expectation": "TGLExt/IALDJones.lean"},
     "citados_fora": {}, "auxiliares_fora_da_composicao": [], "autoria": "agente construtor Sonnet (26/10/2026; quem construiu nao aprova); decisao 3 da gerencia c1 aplicada (o Nome e' nameOp)"},
]
STONE_RELS = [s["rel"] for s in STONES]
STONE_MODS = [s["mod"] for s in STONES]
STONE_BY_REL = {s["rel"]: s for s in STONES}
STONE_BY_KEY = {s["key"]: s for s in STONES}
IMPORT_LINES = ["import " + s["mod"] for s in STONES]
ROOT_SUFFIX = "\n" + "\n".join(IMPORT_LINES) + "\n"           # a raiz TGLExt.lean ganha um separador em branco e os imports (como a v394 a v401 fizeram com as pedras)
AUDIT_PREFIX = "\n".join(IMPORT_LINES) + "\n\n"               # o Audit ganha os imports no topo
CONTRACT_THEOREMS = {s["key"]: list(s["contract"]) for s in STONES}
ALL_SUPPORT = {}
for _s in STONES:
    ALL_SUPPORT.update(_s["support"]); ALL_SUPPORT.update(_s["citados_fora"])
STONES_DESDE_B10 = list(STONES)                              # o que a Bancada de producao (que JA pina a v401, B10) AINDA nao viu: o recibo do kernel do B(n) lista o diff v401 -> v402 = so' estas tres pedras
STONE_RELS_DESDE_B10 = [s["rel"] for s in STONES_DESDE_B10]
STONES_DESDE_B9 = list(D1.STONES_DESDE_B9)                   # (herdado) a pedra FalsidadeDaInercia: nova para a Bancada da v400, JA no kernel do Nos e da Bancada desde a v401
STONE_RELS_DESDE_B9 = [s["rel"] for s in STONES_DESDE_B9]
MAXHEARTBEATS_PONTE = 2000000                                # dito (condicao C3 do exame): a ponte do Codex declara set_option maxHeartbeats 2000000

# ---------------------------------------------------------------- os registros com FUNCAO e os registros por spec
REGISTRO_PONTE = "ponte_da_escala_dual_v402"
REGISTRO_QUEDA = "queda_sem_geometria_v402"
REGISTRO_ESPERANCA = "esperanca_condicional_v402"
REGISTROS_FUNCAO = [REGISTRO_PONTE, REGISTRO_QUEDA, REGISTRO_ESPERANCA]
REGISTRO_DE_PEDRA = {"ponte": REGISTRO_PONTE, "queda": REGISTRO_QUEDA, "esperanca": REGISTRO_ESPERANCA}
CUNHAGENS_REGISTRO = "cunhagens_v402"
KH_REGISTRO = "kh_n1_cobertura_v402"
N_CHECKS_PONTE = 10       # o numero de checagens do calculo de cada registro (runtime_v402.py); atualizado junto com o runtime
N_CHECKS_QUEDA = 8
N_CHECKS_ESPERANCA = 7
N_CHECKS = {"ponte": N_CHECKS_PONTE, "queda": N_CHECKS_QUEDA, "esperanca": N_CHECKS_ESPERANCA}
DECISOES = dict(D1.DECISOES)
DECISOES.update({
    "D11": "o CHAO e' o POSTO (peso 1 = omega(I), o corte a = 0, the_floor_fixes_the_cut; na Fundacao «o piso limita», cunhagem de 07/10), NUNCA o infimo 0: o 0 e' o abismo (sem fundo) e «a consequencia da poda» (recorte de 25/10); a queda de que fala a fala («porque vc sabe que tem um chão, então relaxa») e' a queda do que NAO e' o posto [decisao da gerencia c1, 26/10/2026; ratificavel pelo operador]",
    "D12": "IsotropicPost fica como hipotese NOMEADA (o operador ratificou a rota com «é isso, faça a prova, prossiga.»): a isotropia e' CARGA, nao enfeite (AuditF23Flat.s8_h3_is_load_bearing: a H3 falha com fonte anisotropica); o 1 + 3 fica como leitura [ONTO]; a dimensao 3 NAO e' provada [decisao da gerencia c1, 26/10/2026]",
    "D13": "o Nome e' nameOp (a esperanca condicional, o OPERADOR que le: unital, idempotente, memoria-subalgebra); o projetor de Jones e' a MESMA coisa vista como projetor no espaco GNS (a compressao pelo espelho) e o posto e' o PESO que ela preserva (E(1) = 1): tres faces de um objeto fixo, nao tres definicoes; o kernel prova as LIGACOES, nao uma igualdade de tipos [decisao da gerencia c1, 26/10/2026]",
    "D14": "o B(n) da v402 e' um PASSO SIMPLES v401 -> v402: a Bancada de producao JA pina a v401 (B10); o recibo pre_selo e' GERADO e PINADO antes da instalacao, em ensaio contra a producao (nada gravado nela)",
    "D15": "a ponte do Codex (ORDEM 025) entra SO' como o arquivo .lean (condicao C1 do exame: nenhum outro arquivo da entrega e' copiado), byte a byte, sem edicao; as erratas E1-E4 vao ao lado, no registro, no artigo e no handoff; nenhum modulo ja' instalado e' editado",
    "D16": "os nomes dos tres modulos (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) e dos cinco registros da v402 sao PROVISORIOS: o operador nomeia",
})
ASSINA = "gerencia c1, em nome proprio, 26/10/2026"

# ---------------------------------------------------------------- as ERRATAS E1-E4 da integracao da ponte (exame independente, 26/10/2026; em nome proprio da gerencia c1; vao ao lado: no registro, no artigo e no handoff; o kernel NAO e' editado)
ERRATA_E1 = ("E1 -- H_tau na forma literal («tau e' a massa de Newton e a metrica de Einstein», como a v401 a escreveu) e' REFUTADA no kernel: positive_weight_cannot_be_invariant_mass (um peso positivo que escala por e^{-s} nunca e' invariante na propria orbita) e lift_mass_not_selected "
             "(dois invariantes mu^2 distintos dao duas realizacoes equivariantes DISTINTAS com o MESMO p+). tau so' pode ser p+ (a energia da frente de luz) e a massa e' dado livre. H_tau decompoe-se em pendencias NOMEADAS [OPEN]: H_BW (a rapidez e' o tempo modular de Bisognano-Wichmann, 2 pi), "
             "H_cal (este p+ e' a energia de UM corpo; a escolha de mu^2), H3 (Clausius em toda direcao nula) e as dividas do adendo de 03-04/09 (a positividade completa da a metrica induzida (4,0), nao (1,3); rank c = 4, o H2 nao sai de graca)")
ERRATA_E2 = "E2 -- «Inertial» nesta instancia (momentumScaling) e' o VETOR ZERO (fixo por todo boost: p+ = 0 e p- = 0), nao «movimento livre»: a leitura de que a inercia implica p+ = 0 nao e' fisica da primeira lei; a lacuna de que a rapidez nao e' automaticamente o tempo modular de BW e' H_BW, NOMEADA [OPEN]"
ERRATA_E3 = "E3 -- nunca ler como E = mc^2 composta da escala: rest_energy_eq_mc2 e' algebra real com premissas explicitas (casca, repouso, E >= 0, m >= 0; c > 0 nao e' usado); a composicao e' lift_rest_energy (c = 1), do REPOUSO, condicionada a mu^2 e a tau = m"
ERRATA_E4 = "E4 -- proveniencia: a entrega do Codex compilou contra o kernel do Nos v400 e contra a copia superada da pedra FalsidadeDaInercia (8a3a1c0baa8b7faf, so' docstrings diferem); o revisor recompilou no kernel v401 com a pedra instalada (9f6efcb2a0987e18): rc 0, 40 #print axioms no trio, .olean identico"
ERRATAS_V402 = [ERRATA_E1, ERRATA_E2, ERRATA_E3, ERRATA_E4]

# ---------------------------------------------------------------- as TRES inscricoes de 26/10/2026 (falas do operador; arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
_CUN = os.path.join(WK, "cunhagens_13out")
VERBATIM_ORIGEM_V402 = [os.path.join(_CUN, "OPERADOR_26out_esperanca_condicional_e_nome_verbatim.txt"),
                        os.path.join(_CUN, "OPERADOR_26out_o_um_se_poe_e_cai_a_queda_sem_geometria_verbatim.txt"),
                        os.path.join(_CUN, "OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt")]
# os prefixos de sha256 que a ORDEM da gerencia deu (conferidos contra o arquivo na geracao; o hash vale o arquivo, nunca o contrario)
VERBATIM_PREFIXOS_DA_ORDEM_V402 = ["5d3976cd", "36cfa002", "a1c4bae4"]
VERBATIM_AUTOR_V402 = ["operador"] * 3
VERBATIM_QUANDO_V402 = "26/10/2026 (cunhagem)"
VERBATIM_CHAVE_PREFIXO_V402 = "v402_cun_"
ESPERANCA_IDX, QUEDA_IDX, PROSSIGA_IDX = 0, 1, 2
# trechos das falas citados VERBATIM (cada um e' substring da fala indicada, com a grafia dele; a cadeia confere por script; a parafrase da gerencia nunca entra entre aspas)
FRASE_TIPAGEM = "ainda não sei se fizemos a tipagem no um.py"                                                    # fala 0
FRASE_ESPERANCA = "esperança condicional=nome"                                                                     # fala 0
FRASE_INPUT = "o Um quando se põe realiza a operação \"input\""                                                      # fala 1
FRASE_CAI = "ao se inscrever, ele cai. a fase cai."                                                                # fala 1
FRASE_DIRECAO = "então tem direção, mas não é gemétrica"                                                           # fala 1 (grafia dele: «gemétrica»)
FRASE_ENTREGA = "é a operação da entrega (entrega=custas), opera o relaxamaneto"                                  # fala 1 (grafia dele: «relaxamaneto»)
FRASE_NAO_FORCA = "a queda que eu quero traduzir não é força também"                                              # fala 1
FRASE_CHAO = "porque vc sabe que tem um chão, então relaxa"                                                        # fala 1
FRASE_SEM_GEOMETRIA = "como explicar queda sem geomtria?"                                                          # fala 1 (grafia dele: «geomtria»)
FRASE_PROSSIGA = "é isso, faça a prova, prossiga."                                                                 # fala 2
FRASES_V402 = [(0, FRASE_TIPAGEM), (0, FRASE_ESPERANCA), (1, FRASE_INPUT), (1, FRASE_CAI), (1, FRASE_DIRECAO), (1, FRASE_ENTREGA), (1, FRASE_NAO_FORCA), (1, FRASE_CHAO), (1, FRASE_SEM_GEOMETRIA), (2, FRASE_PROSSIGA)]
# a PERGUNTA e a RESPOSTA de 26/10 na sessao (sem arquivo proprio no acervo: [DECLARADO]; a resposta e' leitura da gerencia c1 [ONTO], coerente com a fala 1: «então tem direção, mas não é gemétrica»)
LEITURA_DIRECAO_26OUT = {"pergunta": "o Um posto tem direcao?", "resposta": "a seta da queda da fase, nao do espaco", "estatuto": "[INPUT (a pergunta, do operador, na sessao de 26/10/2026) / ONTO (a resposta, leitura da gerencia c1)]",
                         "declarado": "a pergunta e a resposta nao tem arquivo verbatim no acervo desta cadeia: sao registradas como a gerencia c1 as guardou [DECLARADO]; a fala 1 (sha16 36cfa0027565dcff) traz a base verbatim: «então tem direção, mas não é gemétrica»"}


def verbatins402(destino_cunhagens):
    """As TRES inscricoes de 26/10 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor}. A copia duravel NAO e' escrita aqui. Os prefixos de sha256
    que a ordem da gerencia deu sao conferidos contra o arquivo; cada trecho citado (FRASES) e' substring VERBATIM da inscricao indicada."""
    out = []
    for p, pref, autor in zip(VERBATIM_ORIGEM_V402, VERBATIM_PREFIXOS_DA_ORDEM_V402, VERBATIM_AUTOR_V402):
        b = open(p, "rb").read(); h = sha256(b)
        assert h.startswith(pref), ("o arquivo da inscricao NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO_V402 + h[:16], "quando": VERBATIM_QUANDO_V402, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert len(out) == 3 and all(v["autor"] == "operador" for v in out), "tem de haver TRES inscricoes, todas falas do operador"
    for i, fr in FRASES_V402:
        assert fr in out[i]["text"], ("o trecho citado NAO e' verbatim na inscricao", i, fr[:60])
    return out


def pedras_fontes():
    """As TRES pedras LIDAS do disco: lista de dicts {stone, origem, copia (v402\\pedra), sha256, bytes}. O sha16 e' conferido contra o que a ORDEM da gerencia deu. A copia NAO e' escrita aqui."""
    out = []
    for s in STONES:
        b = open(s["origem"], "rb").read(); h = sha256(b)
        assert h[:16] == s["sha16_da_ordem"], ("a pedra no disco NAO e' a que a ordem da gerencia pinou", s["name"], h[:16], s["sha16_da_ordem"])
        out.append({"stone": s["name"], "origem": s["origem"], "copia": s["src"], "sha256": h, "bytes": len(b)})
    return out

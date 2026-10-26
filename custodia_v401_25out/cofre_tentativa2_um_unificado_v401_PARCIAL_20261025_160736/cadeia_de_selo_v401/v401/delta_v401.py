# -*- coding: utf-8 -*-
"""delta_v401.py -- A UNICA definicao do DELTA da v401 (preparacao de 25/10/2026, gerencia c1): UMA pedra nova no kernel, `TGLExt/FalsidadeDaInercia.lean` (nome DADO pelo operador em 25/10/2026: «falsidade (simulacro) da inercia»;
12 declaracoes nomeadas, compilada e provada no sandbox C:\\t\\k401, sha16 f9e4e877a5a9d688), UM registro com FUNCAO (`falsidade_da_inercia_v401`: le do kernel do rito a composicao da pedra e CALCULA, com beta = alfa CODATA 2018 x sqrt(e) em runtime,
o modelo oneScaling: o peso do posto depois da escala s e' e^{-s}, diferente de 1 para s != 0, e o custo t.beta.g > 0), os registros por spec `cunhagens_v401` (as CINCO inscricoes de 25/10 e as RATIFICACOES do operador) e `kh_n1_cobertura_v401`
(a cobertura exata do Audit), a errata AO LADO da leitura do escriba no adendo de 03-04/09 («w(I)=1 e a INERCIA» fica SUPERADA pela definicao do operador: inercia = 0_abs, 1=0; w(I)=1 e o Um POSTO que a interrompe, 1=1), o artigo
(secao «A falsidade (simulacro) da inercia»), a POLITICA DE BANDEIRAS (a da v394: so' declaracao NOMEADA) e os nomes do sandbox/pastas desta cadeia. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44).
A base e' a v400 SELADA (um.py 6981660b5f7cd537) e a Bancada Um de producao JA pina a v400 (B9): o B(n) da v401 e' um PASSO SIMPLES v400 -> v401 (o diff do kernel e' so' esta pedra).
E' IMPORTADO por copiar_base_v401, preparar_kernel_v401, pos_build_kernel_v401, registros_v401, gerar_candidato_v401, ensaio_a_seco_v401, gerar_esperados_v401, p00_precondicoes_v401 e os demais: nada daqui e' digitado de memoria em outro arquivo,
e todo hash e' LIDO do arquivo por script. Reaproveita (import por caminho) o delta_v400 (e este o delta_v399): as fontes do operador do ACOM, a politica de bandeiras, o quadro do Teste da Unica Palavra. Molde: delta_v399.py (cadeia de CONTEUDO) e delta_v400.py."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V400 = os.path.join(os.path.dirname(HERE), "v400")           # a cadeia anterior (molde e base, so' leitura)
_spec = importlib.util.spec_from_file_location("delta_v400", os.path.join(V400, "delta_v400.py"))
D0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D0)
globals().update({k: v for k, v in vars(D0).items() if not k.startswith("__")})   # tudo da v400 (e, por ela, da v399) e depois o que a v401 SOBRESCREVE

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v400: aqui e' a pasta da v401)
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))
V399 = D0.V399                                               # a cadeia de conteudo anterior (so' leitura)
SANDBOX_PAI = os.path.join(C, "t", "k401c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # copia de C:\t\k401\final (o kernel da v400 compilado + a pedra compilada ISOLADA + os imports); a raiz e o Audit sao GERADOS por preparar_kernel_v401
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(C, "t", "k401", "final")       # de onde o sandbox foi copiado (so' leitura)
KERNEL_DIR = "kernel"
CANDIDATO = "um_v401_candidato.py"
BASE_DIR = "base_v400"                                       # copia de bytes do Nos v400 selado (um.py, selo, core, manifesto do kernel, pilar, sidecar)
UM_VERSION = "v401"
BASE_VERSION = "v400"
BASE_SHA16_DA_ORDEM = "6981660b5f7cd537"                     # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb18")                 # o sandbox curto das guardas estaticas da Bancada e das conferencias do recibo pre_selo (apagado no fim)
KH_N1_INSUMO = "KH_N1_v401.json"

# ---------------------------------------------------------------- a pedra (o NOME e' do operador: «falsidade (simulacro) da inercia»; no codigo vai sem acento e sem parenteses)
ESTUDO = os.path.join(WK, "falsidade_da_inercia_v401")        # a construcao da pedra (so' leitura)
_P = os.path.join(HERE, "pedra")
STONES = [
    {"key": "falsidade", "name": "FalsidadeDaInercia", "mod": "TGLExt.FalsidadeDaInercia", "rel": "TGLExt/FalsidadeDaInercia.lean", "ns": "TGLExt.FalsidadeDaInercia.",
     "origem": os.path.join(ESTUDO, "FalsidadeDaInercia.lean"), "src": os.path.join(_P, "FalsidadeDaInercia.lean"), "insumo": "FalsidadeDaInercia.lean", "sha16_da_ordem": open(os.path.join(HERE, "pedra_sha16_da_ordem.txt"), encoding="utf-8").read().strip(),   # LIDO do pino (um arquivo de uma linha que a gerencia atualiza quando a pedra e' estendida); o arquivo da pedra e' lido na hora de gerar e a divergencia ABORTA
     "flag_prefix": "ext_fdi401_", "grupo": "falsidade",
     "theorem": "TGLExt.FalsidadeDaInercia.falsidade_da_inercia_derivada",       # a COMPOSICAO DERIVADA (a extensao de 25/10: nada que porte posto e' anterior a impressao; a inercia nao e' causa de si mesma; o zero e' a consequencia da poda; a tensao projetada no atrator), que sobre a falsidade_da_inercia das quatro
     "key_theorem": "TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false",   # a ESTRELA: posto + inercial => (1:R) = 0
     "contract": ["TGLExt.FalsidadeDaInercia.Inertial", "TGLExt.FalsidadeDaInercia.IsPost",
                  "TGLExt.FalsidadeDaInercia.the_inertia_is_the_absolute_zero", "TGLExt.FalsidadeDaInercia.the_inertia_is_the_absolute_zero_at_any_scale",
                  "TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false_at", "TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false", "TGLExt.FalsidadeDaInercia.a_post_is_not_inertial",
                  "TGLExt.FalsidadeDaInercia.the_post_exists_and_moves", "TGLExt.FalsidadeDaInercia.the_simulacrum", "TGLExt.FalsidadeDaInercia.the_inscription_interrupts_the_inertia",
                  "TGLExt.FalsidadeDaInercia.falsidade_da_inercia", "TGLExt.FalsidadeDaInercia.falsidade_da_inercia_is_inhabited"]
                 + ["TGLExt.FalsidadeDaInercia.%s" % n_ for n_ in ['no_post_before_the_impression', 'inertia_is_not_its_own_cause', 'the_first_motion_is_the_impression', 'diagFlow_coordinate_is_the_scaling', 'leak_below_every_epsilon', 'the_zero_is_the_consequence_of_the_pruning', 'the_tension_is_projected_onto_the_attractor', 'falsidade_da_inercia_derivada']],
     # os termos do kernel ANTIGO que a pedra cita (ja' no axiom_report; o registro le: presente, no trio, declarado no modulo que o compilador emite)
     "support": {"TGLExt.DualScalingData.fixed_tau_zero": "TGLExt/GlobalLiftLadder.lean", "TGLExt.Fundacao.nothing_above_bears_a_post": "TGLExt/Fundacao.lean", "TGLExt.Fundacao.the_floor_fixes_the_cut": "TGLExt/Fundacao.lean",
                 "TGLExt.Fundacao.oneScaling": "TGLExt/Fundacao.lean", "TGLExt.beta_forbids_full_static_witness": "TGLExt/NoFullWitness.lean", "TGLExt.leakage_strictly_loses": "TGLExt/NoFullWitness.lean",
                 "TGLExt.FullStaticWitness": "TGLExt/NoFullWitness.lean",
                 "TGLExt.Fundacao.the_fall_never_lands": "TGLExt/Fundacao.lean", "TGLExt.Fundacao.abismo": "TGLExt/Fundacao.lean", "TGLExt.um_is_the_great_attractor": "TGLExt/TheGreatAttractor.lean", "TGLExt.the_observer_is_unique": "TGLExt/TheGreatAttractor.lean",
                 "TGLExt.diagFlow": "TGLExt/BoundaryException.lean", "TGLExt.permanent": "TGLExt/ObserverInside.lean", "TGLExt.observerProj": "TGLExt/ObserverInside.lean"},
     "citados_fora": {},                       # a pedra nao cita sem importar
     "auxiliares_fora_da_composicao": []},     # as 2 auxiliares do compilador (oneScaling.eq_1, DualScalingData.mk.congr_simp) ficam fora da politica de bandeiras
]
STONE_RELS = [s["rel"] for s in STONES]
STONE_MODS = [s["mod"] for s in STONES]
STONE_BY_REL = {s["rel"]: s for s in STONES}
IMPORT_LINES = ["import " + s["mod"] for s in STONES]
ROOT_SUFFIX = "\n" + "\n".join(IMPORT_LINES) + "\n"           # a raiz TGLExt.lean ganha um separador em branco e o import (como a v394 a v399 fizeram com as pedras)
AUDIT_PREFIX = "\n".join(IMPORT_LINES) + "\n\n"               # o Audit ganha o import no topo
CONTRACT_THEOREMS = {s["key"]: list(s["contract"]) for s in STONES}
ALL_SUPPORT = {}
for _s in STONES:
    ALL_SUPPORT.update(_s["support"]); ALL_SUPPORT.update(_s["citados_fora"])
STONES_DESDE_B9 = list(STONES)                               # o que a Bancada de producao (que JA pina a v400) AINDA nao viu: o recibo do kernel do B(n) lista o diff v400 -> v401 = so' esta pedra
STONE_RELS_DESDE_B9 = [s["rel"] for s in STONES_DESDE_B9]
STONES_DESDE_B8 = list(D0.STONES_DESDE_B8)                   # (herdado) a pedra Testemunho: nova para a Bancada da v398, JA no kernel do Nos e da Bancada desde a v400
STONE_RELS_DESDE_B8 = [s["rel"] for s in STONES_DESDE_B8]

# ---------------------------------------------------------------- o registro com FUNCAO e os registros por spec
REGISTRO_FALSIDADE = "falsidade_da_inercia_v401"
CUNHAGENS_REGISTRO = "cunhagens_v401"
KH_REGISTRO = "kh_n1_cobertura_v401"
DECISOES = dict(D0.DECISOES)
DECISOES.update({
    "D1": "RATIFICADO pelo operador (25/10/2026, «Ratifico tudo.»): os nomes antes provisorios ficam DEFINITIVOS (a pedra Testemunho e os registros selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, teste_de_veracidade_fase9_v397, sonico_v398, afinacao_das_cordas_v398)",
    "D7": "RATIFICADO pelo operador (25/10/2026): a leitura das duas faces (P, I-P) = (a leitura do operador, o registro do um.py), antes leitura da gerencia [ONTO] a ratificar",
    "D8": "a pedra se chama «falsidade (simulacro) da inercia» (nome DADO pelo operador, 25/10/2026); no codigo `FalsidadeDaInercia` (identificador Lean nao admite acento nem parenteses)",
    "D9": "o B(n) da v401 e' um PASSO SIMPLES v400 -> v401: a Bancada de producao JA pina a v400 (B9); o recibo pre_selo e' GERADO e PINADO antes da instalacao, em ensaio contra a producao (nada gravado nela)",
    "D10": "a errata ao lado da leitura do escriba no ADENDO de 03-04/09 e' da gerencia c1, em nome proprio: «w(I)=1 e a INERCIA» fica SUPERADA; o arquivo do adendo NAO e' tocado (seu sha esta pinado)",
})
# a paridade do psibit (RATIFICADA em 25/10): sinal(L) . sinal(dL); a gerencia a registra como o operador a ratificou (o texto exato da proposta e' da sessao da gerencia: [DECLARADO])
RATIFICACOES = [
    {"id": "r1", "item": "o nome da pedra Testemunho (antes provisorio) e' definitivo", "estatuto": "[INPUT]"},
    {"id": "r2", "item": "o nome do registro selo_pela_propria_tecnologia_v399 (antes provisorio) e' definitivo", "estatuto": "[INPUT]"},
    {"id": "r3", "item": "o nome do registro declaracao_do_operador_v399 (antes provisorio) e' definitivo", "estatuto": "[INPUT]"},
    {"id": "r4", "item": "o nome do registro teste_de_veracidade_fase9_v397 (antes provisorio) e' definitivo", "estatuto": "[INPUT]"},
    {"id": "r5", "item": "o nome do registro sonico_v398 (antes provisorio) e' definitivo", "estatuto": "[INPUT]"},
    {"id": "r6", "item": "o nome do registro afinacao_das_cordas_v398 (antes provisorio) e' definitivo", "estatuto": "[INPUT]"},
    {"id": "r7", "item": "a leitura das duas faces (D7): P = a leitura do operador, I-P = o registro do um.py", "estatuto": "[INPUT/ONTO]"},
    {"id": "r8", "item": "a paridade do psibit e' sinal(L) . sinal(dL)", "estatuto": "[INPUT]"},
]

# ---------------------------------------------------------------- as CINCO inscricoes de 25/10/2026 (falas do operador; arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
_CUN = os.path.join(WK, "cunhagens_13out")
VERBATIM_ORIGEM_V401 = [os.path.join(_CUN, "OPERADOR_25out_ratifico_tudo_e_emc2_geometria_projetada_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_25out_nada_e_materia_link_com_a_entropia_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_25out_materia_cristalizacao_da_dobra_da_luz_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_25out_inercia_e_o_proprio_zero_absoluto_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_25out_nome_da_pedra_falsidade_simulacro_da_inercia_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_25out_derivacao_inercia_gravitacao_impressao_do_um_RECORTE_verbatim.txt")]   # RECORTE DECLARADO da fala de 25/10 (a ordem da gerencia: o inicio da fala sai do trabalho)
# os prefixos de sha256 que a ORDEM da gerencia deu (conferidos contra o arquivo na geracao; o hash vale o arquivo, nunca o contrario)
VERBATIM_PREFIXOS_DA_ORDEM_V401 = ["4cf668f8", "344a8ae9", "0516c064", "0b244a5f", "901dd8fc", "e26364c5"]
VERBATIM_AUTOR_V401 = ["operador"] * 6
VERBATIM_QUANDO_V401 = "25/10/2026 (cunhagem)"
VERBATIM_CHAVE_PREFIXO_V401 = "v401_cun_"
RATIFICA_IDX, NADA_IDX, MATERIA_IDX, INERCIA_IDX, NOME_IDX, IMPRESSAO_IDX = 0, 1, 2, 3, 4, 5
N_CHECKS_FALSIDADE = 10   # o numero de checagens do calculo no registro falsidade_da_inercia_v401 (runtime_v401.py); atualizado junto com o runtime
# trechos das falas citados VERBATIM (cada um e' substring da fala indicada; a cadeia confere por script; a parafrase da gerencia nunca entra entre aspas)
FRASE_RATIFICO = "Ratifico tudo."                                                                                  # fala 0
FRASE_EMC2 = "Então E=m.c2 é a geometria que a cinemática da gravidade=luz2.entropia projeta?"                      # fala 0 (a pergunta do operador)
FRASE_NADA = "nada=materia e esse é o link com a entropia"                                                         # fala 1
FRASE_MATERIA = "a matéria é a cristalização da dobra luz no vácuo relativa ao observador"                          # fala 2
FRASE_INERCIA = "a minha definição é o próprio zero absoluto"                                                       # fala 3
FRASE_INERCIA_NEWTON = "agora chegamos à inércia de Newton"                                                         # fala 3
FRASE_NOME = "a pedra chama-se “falsidade (simulacro) da inércia”, faça a prova"                                     # fala 4
FRASE_DERIVADO = "eu não queria que a leitura fosse ONTO minha, quero que seja derivado"                                   # fala 5
FRASE_IMPRESSAO = "a gravitação universal e a inércia não existem antes da posição impressa do Um absoluto"            # fala 5
FRASE_PRIMEIRO_MOVIMENTO = "o primeiro movimento é a impressão do posto absoluto ocupado por 1"                          # fala 5
FRASE_ZERO_PODA = "o zero absoluto não é o início de tudo, não. ele é a consequencia da poda"                             # fala 5
FRASES_V401 = [(5, FRASE_DERIVADO), (5, FRASE_IMPRESSAO), (5, FRASE_PRIMEIRO_MOVIMENTO), (5, FRASE_ZERO_PODA), (0, FRASE_RATIFICO), (0, FRASE_EMC2), (1, FRASE_NADA), (2, FRASE_MATERIA), (3, FRASE_INERCIA), (3, FRASE_INERCIA_NEWTON), (4, FRASE_NOME)]
# o ADENDO de 03-04/09 (o arquivo NAO e' tocado; o sha dele esta pinado): a leitura do escriba que a errata ao lado SUPERA
ADENDO_ARQ = os.path.normpath(os.path.join(NOS, "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md"))
ADENDO_SHA16_DA_ORDEM = "1459b477b496e1f0"
# o kernel cita a inercia como 0_abs: a docstring de TGLExt.costless (modulo embutido TGLExt/TheCorrespondence.lean; um.py v400, linha 117522)
COSTLESS_TRECHO = "nunca correspondeu"
COSTLESS_REL = "TGLExt/TheCorrespondence.lean"


def verbatins401(destino_cunhagens):
    """As SEIS inscricoes de 25/10 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor}. A copia duravel NAO e' escrita aqui. Os prefixos de sha256
    que a ordem da gerencia deu sao conferidos contra o arquivo; cada trecho citado (FRASES) e' substring VERBATIM da inscricao indicada."""
    out = []
    for p, pref, autor in zip(VERBATIM_ORIGEM_V401, VERBATIM_PREFIXOS_DA_ORDEM_V401, VERBATIM_AUTOR_V401):
        b = open(p, "rb").read(); h = sha256(b)
        assert h.startswith(pref), ("o arquivo da inscricao NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO_V401 + h[:16], "quando": VERBATIM_QUANDO_V401, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert len(out) == 6 and all(v["autor"] == "operador" for v in out), "tem de haver SEIS inscricoes, todas falas do operador"
    for i, fr in FRASES_V401:
        assert fr in out[i]["text"], ("o trecho citado NAO e' verbatim na inscricao", i, fr[:60])
    return out


def pedras_fontes():
    """A pedra LIDA do disco: lista de dicts {stone, origem, copia (v401\\pedra), sha256, bytes}. O sha16 e' conferido contra o que a ORDEM da gerencia deu. A copia NAO e' escrita aqui."""
    out = []
    for s in STONES:
        b = open(s["origem"], "rb").read(); h = sha256(b)
        assert h[:16] == s["sha16_da_ordem"], ("a pedra no disco NAO e' a que a ordem da gerencia pinou", s["name"], h[:16], s["sha16_da_ordem"])
        out.append({"stone": s["name"], "origem": s["origem"], "copia": s["src"], "sha256": h, "bytes": len(b)})
    return out

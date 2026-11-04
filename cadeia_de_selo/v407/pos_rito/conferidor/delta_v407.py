# -*- coding: utf-8 -*-
"""delta_v407.py -- A UNICA definicao do DELTA da v407 (claude-prep-v407, a servico da gerencia c1, 03/11/2026): O PSION, O CANTO E O PAR ENTRAM NO um.py.
Ordens do operador (03/11/2026, verbatim por sha16 lido do arquivo, em work\\cunhagens_13out): b89e4c909f37e163 («como podemos testar a condição que eu falei … o lema que liga o psion ao canto também já pode ser derivado … prossigamos com tudo, ratifico tudo …
terminarmos a parametrização para realizamos o teste que ainda falta (d) para entrar também naversao 407 … o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura»); 73466598d3419fb0 («Concordo com o nome … o gráviton é o estado ligado de dois psions, portanto,
eles nunca se cancelam … sua leitura se faz pelo gráviton (fase e retorno de fase); eu penso que é do projetor 4x4 (confira); concordo com todos os nomes e os ratifico; concordo com c, porque se o teste não tiver poder não vou inseri-lo no um.py; eu quero conteúdo observável …»);
57250bbbaca9fd39 (o nome da pedra do par: «“Par”»; e o «Vai» para a Torre, fora do um.py).
O QUE ENTRA NO KERNEL (modelo de BUNDLE como a v406, mas pequeno): 9 modulos novos em TGLExt/ -- PsionCanto (a condicao sob compressao e o lema das duas faces; nome aceito pelo operador), Par (o par de psions = o graviton, ligado, nunca cancelado; nome dado pelo operador) e as
sete pedras de 02/11 de nome RATIFICADO (APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual). A raiz TGLExt.lean ganha NOVE imports; o Audit NAO muda. O registro com FUNCAO psion_canto_v407 le o kernel do rito (as ancoras, os nove sha256, a chave
do lema), e a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma, LITERAL False desde a v396, passa a ser LIDA do kernel (errata E18 AO LADO: o elo e' de ESTRUTURA, nao de vetores; o par na face de Fock segue [OPEN]).
A base e' a v406 SELADA e a Bancada Um de producao ja' pina a v406 (B15-v406-20261103-R1): o B(n) da v407 e' um passo SIMPLES v406 -> v407 (B16).
Reaproveita (import por caminho, com a constante BANCADA_PINA_HOJE da v406 neutralizada: ela e' calculada na importacao e quebraria apos o APLICAR da v407) o delta_v406 (e este o delta_v405, ...). O que a v407 SOBRESCREVE vem abaixo. Molde: delta_v406.py (cadeia_de_selo\\v406)."""
import glob
import hashlib
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V406 = os.path.join(os.path.dirname(HERE), "v406")           # a cadeia anterior (molde e base, so' leitura)
_src406 = open(os.path.join(V406, "delta_v406.py"), "rb").read().decode("utf-8")
_alvo = 'BANCADA_PINA_HOJE = _bancada_pina_hoje()'
assert _src406.count(_alvo) == 1, "a linha BANCADA_PINA_HOJE do delta_v406 nao esta' como esperado"
# a constante e' recalculada na importacao pela leitura do contrato da Bancada: depois do APLICAR da v407 a Bancada pina a v407 e a funcao do delta_v406 recusaria; aqui ela e' fixada no que era a v406 (o delta_v407 le o contrato por conta propria, abaixo)
_src406 = _src406.replace(_alvo, 'BANCADA_PINA_HOJE = {"version": "v406", "deployment_id": "B15-v406-20261103-R1", "n": 15}   # (fixada pelo delta_v407: ver _bancada_pina_hoje abaixo)')
_src406 = _src406.replace("HERE = os.path.dirname(os.path.abspath(__file__))\nV405 = os.path.join(os.path.dirname(HERE), \"v405\")           # a cadeia anterior",
                          "HERE = %r\nV405 = os.path.join(os.path.dirname(HERE), \"v405\")           # a cadeia anterior" % V406, 1)
_mod406 = importlib.util.module_from_spec(importlib.util.spec_from_loader("delta_v406_carregado_pelo_v407", loader=None))
_mod406.__file__ = os.path.join(V406, "delta_v406.py")
exec(compile(_src406, _mod406.__file__, "exec"), _mod406.__dict__)
D6 = _mod406
globals().update({k: v for k, v in vars(D6).items() if not k.startswith("__")})   # tudo da v406 (e, por ela, da v405 ... v399) e depois o que a v407 SOBRESCREVE
D6 = D6                                                        # (D5 = delta_v405, herdado pelo update acima; D6 = delta_v406, o predecessor imediato)

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v406: aqui e' a pasta da v407)
V406 = os.path.join(os.path.dirname(HERE), "v406")
V405 = D6.V405
V404 = D6.V404
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                    # ...\Central de Patentes\work
CENTRAL = os.path.dirname(WK)                                  # ...\Central de Patentes
SANDBOX_PAI = os.path.join(C, "t", "k407c")                    # sandbox NOVO (copia do kernel do Nos v406 selado, com o .lake/build compilado)
SANDBOX = os.path.join(SANDBOX_PAI, "final")                   # + os 9 modulos de TGLExt/ + a raiz com os nove imports (preparar_bundle_v407_03nov.py)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                   # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(D6.NOS, "tgl_kernel")            # o kernel do Nos v406 selado (so' leitura)
PACKAGES_ORIGEM = os.path.join(C, "t", "k404c", "final", ".lake", "packages")
KERNEL_DIR = "kernel"
CANDIDATO = "um_v407_candidato.py"
BASE_DIR = "base_v406"                                         # copia de bytes do Nos v406 selado (um.py, selo, core, manifesto do kernel, pilar, sidecar)
UM_VERSION = "v407"
BASE_VERSION = "v406"
BASE_SHA16_DA_ORDEM = "ddcb91930982d614"                       # a v406 selada (a ordem da gerencia; conferido contra o selo e contra o arquivo: o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb21")
KH_N1_INSUMO = "KH_N1_v407.json"
_BANCADA_CONTRATOS = os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json")


def _bancada_pina_hoje():
    """o que a Bancada de producao pina HOJE, LIDO do arquivo dela (nunca digitado): ANTES do B(n) APLICAR e' a v406 (o passo da v407 e' simples); DEPOIS do APLICAR (10b) e' esta versao (v407). Os dois estados sao legitimos."""
    d_ = json.load(open(_BANCADA_CONTRATOS, encoding="utf-8"))
    dep_ = str(d_.get("deployment_id", ""))
    m_ = re.match(r"B(\d+)-(v\d+)-", dep_)
    assert m_ and m_.group(2) in (BASE_VERSION, UM_VERSION), ("a Bancada de producao nao pina nem a base (v406) nem esta versao (v407): o B(n) nao seria um passo simples", dep_)
    return {"version": m_.group(2), "deployment_id": dep_, "n": int(m_.group(1))}


BANCADA_PINA_HOJE = _bancada_pina_hoje()                       # {'version': 'v406', 'deployment_id': 'B15-v406-20261103-R1', 'n': 15} em 03/11/2026; depois do APLICAR: {'version': 'v407', ..., 'n': 16}
BANCADA_JA_APLICADA = (BANCADA_PINA_HOJE["version"] == UM_VERSION)
B_N_SEGUINTE = "B%d" % ((BANCADA_PINA_HOJE["n"] + 1) if not BANCADA_JA_APLICADA else BANCADA_PINA_HOJE["n"])   # o rotulo do B(n) da v407 (B16), antes e depois do APLICAR


def sha16_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]


def sha256_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()


# ---------------------------------------------------------------- O BUNDLE (os 9 modulos; a lista e os sha256 sao LIDOS dos arquivos que preparar_bundle_v407_03nov.py escreveu, nunca digitados)
BUNDLE_LISTA_ARQ = os.path.join(HERE, "kernel_modulos_novos_v407.json")
BUNDLE_ARQ = os.path.join(HERE, "BUNDLE_v407.json")
_BL = json.load(open(BUNDLE_LISTA_ARQ, encoding="utf-8"))
_BD = json.load(open(BUNDLE_ARQ, encoding="utf-8"))
BUNDLE_RELS = list(_BL["novos"])                               # 'TGLExt/<Nome>.lean', na ordem do preparo (PsionCanto, Par, e as sete de 02/11)
BUNDLE_MODS = [p[:-len(".lean")].replace("/", ".") for p in BUNDLE_RELS]
N_BUNDLE = len(BUNDLE_RELS)
BUNDLE_POR_REL = {b["rel"]: b for b in _BD["modulos"]}
assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == 9 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS), ("o bundle tem de ser os 9 modulos", N_BUNDLE, _BL["n"], _BD["n"])
assert len(set(BUNDLE_RELS)) == N_BUNDLE and all(r.startswith("TGLExt/") and r.count("/") == 1 for r in BUNDLE_RELS)
BUNDLE_DA_BANCADA = []                                         # nenhum: as nove sao da gerencia c1 (as candidatas compiladas no sandbox)
BUNDLE_DA_GERENCIA = list(BUNDLE_RELS)
ROOT_SUFFIX = _BL["root_suffix"]                               # a raiz TGLExt.lean = a da v406 + estes NOVE imports
assert ROOT_SUFFIX.replace("\r\n", "\n") == "".join("import %s\n" % m for m in BUNDLE_MODS), repr(ROOT_SUFFIX)
AUDIT_PREFIX = ""                                              # v407: o Audit do sandbox e' o do Nos v406 SEM alteracao: ele ja' faz `import TGLExt` (a raiz), que traz os modulos novos
FLAG_PREFIX = "ext_psi407_"                                    # as bandeiras do bundle: UMA serie, so' declaracao NOMEADA publica (a politica da v394), em ordem (modulo, nome); o numero e' MEDIDO pelo pos_build
GRUPO_BUNDLE = "psion_canto"
ORIGEM_DE_BANDEIRA = "psion_canto_nomeada"
MODULO_PSION = "TGLExt/PsionCanto.lean"                        # a condicao sob compressao e o lema das duas faces
MODULO_PAR = "TGLExt/Par.lean"                                 # o par de psions = o graviton
MODULO_TOPO = MODULO_PSION                                     # (aliases de compatibilidade com os scripts da v406 bumpados: o modulo que CARREGA a chave e o seu vizinho)
MODULO_REDE = MODULO_PAR
MODULO_TESTEMUNHA = MODULO_PSION
assert MODULO_PSION in BUNDLE_POR_REL and MODULO_PAR in BUNDLE_POR_REL

# ---------------------------------------------------------------- AS ANCORAS: todas as declaracoes-chave das 9 pedras (os `#print axioms` que o autor deixou em cada candidata, com o namespace NOVO); lidas das fontes de origem, nunca digitadas
_RX_PRINT = re.compile(r"^#print axioms\s+(\S+)\s*$", re.M)
ANCORAS = {}
ANCORAS_POR_MODULO = {}
_PAPEL_LEMA = "O LEMA DAS DUAS FACES: nas duas o psion e' o vetor de norma 1 cujo canto e' o projetor sobre ele; escalariza; pesa 1; o motor comprimido devolve o canto (elo de ESTRUTURA, nao de vetores): a chave que estava False desde a v396"
_PAPEIS = {"TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces": _PAPEL_LEMA,
           "TGLExt.PsionCanto.the_physical_psion_is_linked_to_the_corner": "o lema instanciado, sem hipotese, no habitante physicalFockCertificate (v406)",
           "TGLExt.PsionCanto.jones_reading_of_the_light_is_the_corner": "P Delta^{it} P = P: a leitura de Jones do fluxo da luz pelo canto do psion devolve o canto",
           "TGLExt.PsionCanto.the_physical_psion_passes_under_compression": "a condicao sob compressao no habitante do certificado de Fock, sem hipotese",
           "TGLExt.Par.o_par_de_psions_e_o_graviton": "a conjuncao das quatro: ligado, nunca cancelado, lido pela fase dobrada e pelo retorno em pi, e o canto e' o 4x4",
           "TGLExt.Par.the_pair_is_bound": "(a) o par e' LIGADO: psionCorner.p e' a sombra do graviton, CCI = 1/2",
           "TGLExt.Par.the_pair_never_cancels": "(a') o par nunca se cancela: idempotente, traco 1; o individuo nao ecoa (marginal 1/2)",
           "TGLExt.Par.the_pair_is_read_by_the_graviton": "(a'') a leitura pelo graviton: fase dobrada da helicidade 2 e retorno em theta = pi",
           "TGLExt.Par.the_corner_is_the_four_by_four": "(b) o canto escalar do psion e' o projetor 4x4 (bellProjector)"}
for _p in _BD["modulos"]:
    _nome = _p["rel"].split("/")[-1][:-len(".lean")]
    _txt = open(_p["origem"], "rb").read().decode("utf-8")
    _vistos = []
    for _m in _RX_PRINT.finditer(_txt):
        _n = _m.group(1)
        _n = re.sub(r"^TGLExt\.%s(?![A-Za-z0-9_])" % re.escape(_p["nome_antigo"]), "TGLExt." + _nome, _n)
        if not _n.startswith("TGLExt."):
            _n = "TGLExt." + _nome + "." + _n            # (PsionCanto e Par deixaram os #print axioms DENTRO do namespace, com o nome curto)
        assert _n.startswith("TGLExt." + _nome + "."), ("ancora fora do namespace da pedra", _p["rel"], _n)
        _vistos.append(_n)
        ANCORAS[_n] = {"rel": _p["rel"], "papel": _PAPEIS.get(_n, "declaracao-chave da pedra %s (a que o autor marcou com #print axioms na candidata)" % _nome)}
    assert _vistos and len(set(_vistos)) == len(_vistos), ("pedra sem ancoras", _p["rel"])
    ANCORAS_POR_MODULO[_p["rel"]] = _vistos
assert len(ANCORAS) == sum(len(v) for v in ANCORAS_POR_MODULO.values()) and ANCORAS_POR_MODULO["TGLExt/PsionCanto.lean"][-1] in ANCORAS
ANCORA_LEMA = "TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces"
ANCORA_PAR = "TGLExt.Par.o_par_de_psions_e_o_graviton"
assert ANCORA_LEMA in ANCORAS and ANCORA_PAR in ANCORAS
ANCORA_CERTIFICADO = ANCORA_LEMA                               # (alias: a ancora que a chave lida do kernel usa)
ANCORA_TESTEMUNHA = ANCORA_LEMA
ANCORA_TESTEMUNHA_TEOREMA = ANCORA_PAR

# ---------------------------------------------------------------- AS TRES RESPOSTAS DO OPERADOR (03/11), CONFERIDAS NO KERNEL pelos termos que JA existiam (nomes completos LIDOS do axiom_report no pos_build; aqui so' o NOME CURTO que a conferencia procura)
RESPOSTAS_DO_OPERADOR = [
    {"id": "a_ligado", "fala": "o gráviton é o estado ligado de dois psions", "teoremas_curtos": ["bell_reduced_half", "the_unbonded_marginal_echoes"],
     "diz": "o par ligado (estado de Bell, emaranhado) tem CCI = 1/2, a Meia-Nat de emaranhamento; o produto, nao ligado, tem CCI = 0 e ecoa"},
    {"id": "a_nunca_se_cancelam", "fala": "eles nunca se cancelam porque representam a própria tensão irresolúvel no plano", "teoremas_curtos": ["the_pair_echoes", "the_individual_does_not_echo"],
     "diz": "o par e' idempotente e tem traco 1 (nunca e' zero); o individuo nao ecoa: a marginal e' 1/2 da identidade"},
    {"id": "a_lido_pelo_graviton", "fala": "sua leitura se faz pelo gráviton (fase e retorno de fase)", "teoremas_curtos": ["helicity_two_rotation"],
     "diz": "a leitura e' a fase DOBRADA da helicidade 2 (e+ gira por 2 theta) e o retorno de fase e' a volta em theta = pi"},
    {"id": "b_projetor_4x4", "fala": "eu penso que é do projetor 4x4 (confira)", "teoremas_curtos": ["the_density_is_the_psion"],
     "diz": "o canto escalar do psion e' o psionCorner 4x4 = bellProjector = a sombra canonica do graviton; a matriz 2x2 da pedra 92_ e' a face de UM psion"},
]
CHAVES_V407 = [
    {"chave": "testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma", "caminho": ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], "era": "literal False (v396 a v406)",
     "agora": "lida do kernel: o nome TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces no axiom_report, no trio, declarado em TGLExt/PsionCanto.lean, fonte por sha256", "desde": "v396"},
]
CHAVES_V406 = list(D6.CHAVES_V406)                              # (as quatro da v406: seguem lidas do kernel; herdadas)
FICA_FALSE_SEM_LEMA = None                                      # (na v406 era a chave do lema; na v407 ela e' lida do kernel)
FICA_ABERTO_PAR_NA_FACE_DE_FOCK = "o par de psions na FACE DE FOCK (dois psions sobre o vacuo Omega, o estado |G> = a†a†|0> da patente) segue [OPEN]: o FockCertificate nao tem operadores de criacao como termo"
FICA_ABERTO_PONTE_BELL_TT = "a ponte entre o espaco de Bell (Fin 2 x Fin 2, C) e o setor TT do spin 2 (Fin 4, R) NAO e' termo: a pedra Par justapoe as faces, nao as identifica"
FICAM_FALSE_POR_TEOREMA = list(D6.FICAM_FALSE_POR_TEOREMA)

# ---------------------------------------------------------------- os modulos, as pedras e os nomes
STONES = []                                                     # (o modelo de oito pedras da v405 nao vale: bundle)
STONE_RELS = []
STONE_MODS = []
STONE_BY_REL = {}
STONE_BY_KEY = {}
REGISTRO_DE_PEDRA = {}
REGISTROS_PEDRAS = []
N_CHECKS = {}
PEDRAS_V407 = [{"name": r.split("/")[-1][:-len(".lean")], "rel": r, "mod": r[:-len(".lean")].replace("/", "."), "origem": BUNDLE_POR_REL[r]["origem"], "sha256_origem": BUNDLE_POR_REL[r]["sha256_origem"],
                "nome_antigo": BUNDLE_POR_REL[r]["nome_antigo"], "tipo_do_nome": BUNDLE_POR_REL[r]["tipo_do_nome"], "src": os.path.join(HERE, "pedra", r.split("/")[-1])} for r in BUNDLE_RELS]
NOME_DO_OPERADOR = {"PsionCanto": "aceito em 03/11/2026 (sha16 73466598d3419fb0: «Concordo com o nome»); o R1 do arquivo da candidata era marca de revisao",
                    "Par": "dado em 03/11/2026 (sha16 57250bbbaca9fd39: «“Par”»)",
                    "APonteDoAtrito": "ratificado em 03/11/2026 (sha16 73466598d3419fb0: «concordo com todos os nomes e os ratifico»)", "OUmInscrito": "idem", "KEhATangente": "idem", "AChaveDaGuarda": "idem", "OGuarda": "idem", "LeituraPreservada": "idem", "OIgual": "idem"}
assert set(NOME_DO_OPERADOR) == {p["name"] for p in PEDRAS_V407}
TESTEMUNHA = {"key": "psion_canto", "name": "PsionCanto", "mod": "TGLExt.PsionCanto", "rel": MODULO_PSION, "nome_do_operador": NOME_DO_OPERADOR["PsionCanto"],
              "nome_provisorio_da_gerencia": None, "origem": BUNDLE_POR_REL[MODULO_PSION]["origem"], "src": os.path.join(HERE, "pedra", "PsionCanto.lean"), "insumo": "PsionCanto.lean",
              "sha16_da_ordem": "3794f8ccbc6be70b", "theorem": ANCORA_LEMA, "key_theorem": ANCORA_LEMA, "autoria": "gerencia c1, 03/11/2026 (compilada no k406c e no k407c)"}   # (o papel que a CanonicalFullTGLWitnessR1 tinha na v406: a pedra que carrega a chave; sha16 da ORDEM = o da fonte PsionCantoR1.lean)
# o que a Bancada de producao (que JA pina a v406) AINDA nao viu: o recibo do kernel do B(n) lista o diff v406 -> v407 = os 9 modulos do bundle
MODULOS_DESDE_B15 = list(BUNDLE_RELS)
STONES_DESDE_B15 = [{"name": p["name"], "rel": p["rel"], "mod": p["mod"], "origem": "gerencia c1 (pedra compilada no sandbox)"} for p in PEDRAS_V407]
STONE_RELS_DESDE_B15 = list(BUNDLE_RELS)
MODULOS_DESDE_B14 = list(BUNDLE_RELS)                           # (aliases dos scripts bumpados: B14 -> B15)
STONES_DESDE_B14 = list(STONES_DESDE_B15)
STONE_RELS_DESDE_B14 = list(BUNDLE_RELS)
ORDEM_DE_INSTALACAO = [p["name"] for p in PEDRAS_V407]

# ---------------------------------------------------------------- os registros da v407
FECHO_REGISTRO = "psion_canto_v407"                            # o registro com FUNCAO: le as ancoras do axiom_report do rito, a proveniencia, as fontes embutidas por sha256, a escada exata; nao move o gate
CUNHAGENS_REGISTRO = "cunhagens_v407"                          # as falas do operador de 03/11 por sha256 + a chave lida + os registros anteriores que seguem selados
KH_REGISTRO = "kh_n1_cobertura_v407"                           # a cobertura exata do Audit (as igualdades desta versao; as da v406 viram pisos)
REGISTROS_FUNCAO = [FECHO_REGISTRO]
N_CHECKS_FECHO = 16                                            # o numero de checagens do calculo de psion_canto_v407 (runtime_v407.py); atualizado junto com o runtime
TAG_FECHO = "PSION_CANTO"
D_TESTE_MANIFESTO = os.path.join(WK, "conjunto_D_20261029", "parametrizacao_03nov", "MANIFESTO_PARAMETRIZACAO_03nov.json")   # o pre-registro V1.1 do teste (d): so' CITADO (opcao c do operador: se nao tiver poder nao entra)
D_TESTE_SHA16_DA_ORDEM = "1cd181f9a4ddb6d5"
assert os.path.exists(D_TESTE_MANIFESTO) and sha16_arquivo(D_TESTE_MANIFESTO) == D_TESTE_SHA16_DA_ORDEM, ("o manifesto da parametrizacao do teste D nao esta' onde o delta espera ou o sha16 difere do pinado", D_TESTE_MANIFESTO)

# ---------------------------------------------------------------- as fontes de contexto (so' leitura; as copias duraveis vao para v407\\insumos por copiar_insumos_v407.py)
P3 = os.path.join(WK, "pedras_candidatas_03nov")
RECIBO_PSION_ARQ = os.path.join(P3, "RECIBO_PSION_CANTO_R1_03nov.json")
RECIBO_PAR_ARQ = os.path.join(P3, "RECIBO_O_PAR_R1_03nov.json")
SAIDA_PSION_ARQ = os.path.join(P3, "saida_lean_r2.txt")
SAIDA_PAR_ARQ = os.path.join(P3, "saida_lean_par_r1.txt")
RECIBO_PSION_R2_ARQ = os.path.join(P3, "RECIBO_PSION_CANTO_R2_03nov.json")   # R2 da gerencia (03/11, 15h): a fonte corrigida, recompilada no sandbox da v406
RECIBO_PAR_R2_ARQ = os.path.join(P3, "RECIBO_O_PAR_R2_03nov.json")
SAIDA_PSION_R2_ARQ = os.path.join(P3, "saida_lean_r3.txt")
SAIDA_PAR_R2_ARQ = os.path.join(P3, "saida_lean_par_r2.txt")
ACERVO_PSION_ARQ = os.path.join(WK, "psion_lema_03nov", "PSION_NO_ACERVO_03nov.md")
REVISAO_PEDRAS_02NOV_ARQ = os.path.join(WK, "fechamento_02nov", "revisoes", "REVISAO_PEDRAS_CANDIDATAS_02nov_SONNET.md")
PLANO_ARQ = os.path.join(HERE, "PLANO_v407_GERENCIA.md")
DESENHO_ARQ = os.path.join(HERE, "DESENHO_v407.md")

# ---------------------------------------------------------------- as falas do operador de 03/11/2026 (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
_CUN13 = os.path.join(WK, "cunhagens_13out")
VERBATIM_EXCLUIDAS_V407 = {}


def verbatim_origem_pelo_glob407():
    """a lista das falas de 03/11 pelo glob, como esta no disco AGORA (a lista que vale para o candidato e' a congelada abaixo)."""
    return sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_03nov_*_verbatim.txt")))


VERBATIM_ORIGEM_V407 = verbatim_origem_pelo_glob407()
_CONGELADO407 = os.path.join(HERE, "VERBATIM_CONGELADO_v407.json")
if os.path.exists(_CONGELADO407):
    VERBATIM_ORIGEM_V407 = list(json.load(open(_CONGELADO407, encoding="utf-8"))["arquivos"])
assert all(os.path.exists(p_) for p_ in VERBATIM_ORIGEM_V407) and len(VERBATIM_ORIGEM_V407) == len(set(VERBATIM_ORIGEM_V407)) and len(VERBATIM_ORIGEM_V407) >= 3
N_ORDEM_B89 = "OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt"
N_RATIFICA = "OPERADOR_03nov_decisoes_psion_graviton_estado_ligado_projetor_4x4_nomes_ratificados_teste_d_opcao_c_motor_banho_holografico_verbatim.txt"
N_PAR = "OPERADOR_03nov_nome_Par_e_vai_para_a_torre_verbatim.txt"
VERBATIM_PREFIXOS_DA_ORDEM_V407 = {N_ORDEM_B89: "b89e4c909f37e163", N_RATIFICA: "73466598d3419fb0", N_PAR: "57250bbbaca9fd39"}
VERBATIM_AUTOR_V407 = ["operador"] * len(VERBATIM_ORIGEM_V407)
VERBATIM_QUANDO_V407 = "03/11/2026 (ordens, decisoes e nomes)"
VERBATIM_CHAVE_PREFIXO_V407 = "v407_cun_"
FRASE_TESTAR_A_CONDICAO = "como podemos testar a condição que eu falei"
FRASE_LEMA_PSION = "o lema que liga o psion ao canto também já pode ser derivado"
FRASE_PROSSIGAMOS = "prossigamos com tudo, ratifico tudo"
FRASE_TESTE_D_V407 = "terminarmos a parametrização para realizamos o teste que ainda falta (d) para entrar também naversao 407"
FRASE_APP_JEV = "o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura"
FRASE_NOME = "Concordo com o nome"
FRASE_PAR_LIGADO = "o gráviton é o estado ligado de dois psions, portanto, eles nunca se cancelam porque representam a própria tensão irresolúvel no plano, de modo que sua leitura se faz pelo gráviton (fase e retorno de fase)"
FRASE_PROJETOR = "eu penso que é do projetor 4x4 (confira)"
FRASE_NOMES_RATIFICADOS = "concordo com todos os nomes e os ratifico"
FRASE_TESTE_C = "concordo com c, porque se o teste não tiver poder não vou inseri-lo no um.py"
FRASE_BANHO = "eu quero conteúdo observável, porque a meu ver é o banho holográfico, é a própria energia escura funcionando, mas ainda não consegui explicar com precisão o que eu quero"
FRASE_PAR = "“Par”"
FRASES_V407 = [(N_ORDEM_B89, FRASE_TESTAR_A_CONDICAO), (N_ORDEM_B89, FRASE_LEMA_PSION), (N_ORDEM_B89, FRASE_PROSSIGAMOS), (N_ORDEM_B89, FRASE_TESTE_D_V407), (N_ORDEM_B89, FRASE_APP_JEV),
               (N_RATIFICA, FRASE_NOME), (N_RATIFICA, FRASE_PAR_LIGADO), (N_RATIFICA, FRASE_PROJETOR), (N_RATIFICA, FRASE_NOMES_RATIFICADOS), (N_RATIFICA, FRASE_TESTE_C), (N_RATIFICA, FRASE_BANHO), (N_PAR, FRASE_PAR)]

# ---------------------------------------------------------------- AS LEITURAS [ONTO] do operador de 03/11 (nada disto e' termo de kernel; o que e' termo esta nas ancoras e nos 9 modulos)
LEITURA_V407 = {
    "o_par_e_o_graviton": "o graviton e' o estado ligado de dois psions; eles nunca se cancelam porque representam a propria tensao irresoluvel no plano; a leitura se faz pelo graviton (fase e retorno de fase) [ONTO]; o kernel entrega, SOB essa leitura e como composicao de termos que ja existiam, que o par e' ligado (CCI = 1/2), nunca se cancela (idempotente, traco 1), que o individuo nao ecoa, que a leitura e' a fase dobrada da helicidade 2 com retorno em pi, e que o canto e' o projetor 4x4 (pedra Par)",
    "o_canto_e_o_4x4": "o canto escalar do psion e' o projetor 4x4 (psionCorner = bellProjector = a sombra canonica do graviton), e nao a matriz 2x2 da pedra 92_ (essa e' a face de UM psion) [REAL: the_density_is_the_psion e the_corner_is_the_four_by_four]",
    "banho_holografico": "«eu quero conteúdo observável, porque a meu ver é o banho holográfico, é a própria energia escura funcionando, mas ainda não consegui explicar com precisão o que eu quero» [ONTO/INPUT]: o motor continuo no pilar quantico NAO entra na v407 (D38 segue); a fala fica registrada como cunhagem; a gerencia ofereceu LINGUA para ele reconhecer ou recusar (a cobranca contínua charged = 1 - exp(-t beta g); a razao entre o vazamento do canto do par ligado e o do produto; delta<K_bdry> = beta|1+w|), sem decidir por ele",
    "estatuto": "[ONTO/INPUT -- leituras, cunhagens e ordens do operador de 03/11/2026; nada disto e' termo de kernel; o que e' termo esta nas ancoras e nos 9 modulos; a leitura fisica nao virou teorema]",
}
RESSALVAS_V407 = [
    "o elo das duas faces do psion e' de ESTRUTURA: Omega (o vacuo de Fock, em F de dimensao infinita) e Phi+ (o vetor de Bell, em C^4) NAO sao identificados (espacos distintos); o lema diz que nas duas faces o psion e' o vetor de norma 1 cujo canto e' o projetor sobre ele, que escalariza, pesa 1 e devolve o canto sob a leitura de Jones; a chave linked_to_the_corner_by_a_lemma le True nesse sentido e SO' nesse; o resultado sob compressao decorre de Omega ser fixo pela luz e de o canto ser projecao de posto 1 (vale para qualquer vetor unitario fixo pelo fluxo); o lema NAO relaciona as duas faces por uma aplicacao entre os espacos",
    "o par de psions na FACE DE FOCK (dois psions sobre Omega, |G> = a†a†|0> da patente) segue [OPEN]: o FockCertificate nao tem operadores de criacao como termo; a pedra Par e' sobre o canto de Bell finito",
    "a ponte entre o espaco do par (Fin 2 x Fin 2, C: o canto de Bell) e o setor TT do spin 2 linearizado (Fin 4, R: ePlus, eCross, rotZ) NAO e' termo: a pedra Par justapoe a face ligada e a face de helicidade, e a conjuncao nao e' identificacao; a leitura do canto como sombra do graviton e' [ONTO] (sem citacao [KNOWN] ate' haver fonte)",
    "o psion do acervo de 2025 (a†|0>, o quantum de um modo) e o psion do kernel (psion C = C.Omega, o proprio vacuo) sao leituras de datas diferentes; a estratigrafia e' datada: a cunhagem mais nova vale para o termo do kernel; o texto do ACOM/INPI de 2025 (que dava o par psi+ psi- como cancelado, igual ao vacuo) e a frase da Fronteira de 02/2026 (que dava |G> como produto nao emaranhado), ambos resumidos pelo agente de leitura do acervo [DECLARADO], ficam superados pela cunhagem de 03/11/2026 (E19), nao reescritos",
    "K(O) != bot para O compacto NAO esta' provado: a nao-trivialidade da rede e' teorema so' na cunha (herdado da v406); «nucleo II_inf» [KNOWN/DECLARADO]; o traco do nucleo e' ENNReal e ciclico, nao linear",
    "as sete pedras de 02/11 trazem as ressalvas ditas nos proprios docstrings; a revisao de terceiro do Sonnet de 02/11 cobriu so' tres (KEhATangente, APonteDoAtrito, OUmInscrito); as nove pedras foram conferidas pelo revisor de terceiro desta preparacao em 03/11/2026 (Sonnet, rodadas R1 e seguintes: #print axioms no trio, diff contra as origens e docstrings, nao as provas linha a linha; 0 alto e 0 medio em todas as rodadas; os baixos ficam ditos no caderno da revisao); a leitura de K como graviton (OIgual) e a chave como K (AChaveDaGuarda) sao leituras do operador [ONTO], nao termos; o_fundo_e_a_media rearranja a definicao e nao e' mecanismo",
    "o motor continuo no pilar quantico NAO entra na v407 (D38): o operador quer conteudo observavel e ainda nao disse o que; nenhum teste com a natureza entra nesta versao",
    "o teste (d) do ramo B do ringdown entra SO' por citacao do pre-registro V1.1 (MANIFESTO_PARAMETRIZACAO_03nov.json, sha16 1cd181f9a4ddb6d5): nenhum resultado, nenhuma PE em dado real; o poder de planejamento medido pela parametrizacao (3,7 a 3,9 sigma com 10 eventos; 2,1 a 3,2 sigma com a incerteza do vies do aparelho) e' DECLARADO pelo agente da parametrizacao; pela opcao (c) do operador o teste so' entra no um.py se tiver poder; os dois intervalos ficam ABAIXO de 5 sigma: parede medida, nao falsificacao; por (c) o resultado nao entra; entra so' a citacao do pre-registro",
    "full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA (o vazamento continuo proibe o fecho estatico; a exclusao Delta^1/2 J Delta^1/2 = J): nao sao lacunas",
    "os nomes das pedras sao do operador: PsionCanto (aceito), Par (dado) e as sete de 02/11 (ratificados) em 03/11/2026; o nome CanonicalFullTGLWitnessR1 (v406, kernel) foi ratificado na mesma fala («concordo com todos os nomes e os ratifico»; DESENHO_v407 §5-bis.3) e nao muda de modulo",
    "nenhum desfecho experimental, nenhum dado novo, nenhuma creditacao: validade no kernel nao e' creditacao; o gate nao se move; NOT_FALSIFIED nunca e' confirmacao",
]
FRASE_DA_MOLDURA_V407_PT = "o psion e o canto sao a mesma construcao nas duas faces; o par e' ligado e nunca se cancela; validade no kernel nao e creditacao; o gate nao se move"
FRASE_DA_MOLDURA_V407_EN = "the psion and the corner are the same construction on both faces; the pair is bound and never cancels; kernel validity is not creditation; the gate does not move"

DECISOES = dict(D6.DECISOES)
DECISOES.update({
    "D41": "a v407 entra no modelo de BUNDLE pequeno (como a v406): 9 modulos novos em TGLExt/ (PsionCanto, Par e as sete pedras de 02/11 de nome ratificado); a raiz ganha nove imports; o Audit nao muda; as bandeiras ext_psi407_* so' de declaracao nomeada [decisao da gerencia c1, 03/11/2026, sob a ordem sha16 b89e4c909f37e163 e os nomes do operador sha16 73466598d3419fb0 e 57250bbbaca9fd39]",
    "D42": "a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma, literal False da v396 a v406, passa a ser LIDA do kernel do proprio rito (TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces no trio, declarado em TGLExt/PsionCanto.lean), com a errata E18 AO LADO que diz o CONTEUDO do elo (estrutura, nao vetores; o par na face de Fock segue [OPEN]); os specs que cobravam False ganham a versao [decisao da gerencia c1, 03/11/2026]",
    "D43": "a pedra Par compoe, sob a cunhagem do operador de 03/11 (sha16 73466598d3419fb0), so' termos que o kernel ja tinha; o que ela NAO afirma (a face de Fock do par; a ponte Bell-TT) vai dito em todo texto [decisao da gerencia c1, 03/11/2026]",
    "D44": "o teste (d) do ramo B (opcao (c) do operador: «se o teste não tiver poder não vou inseri-lo no um.py») entra na v407 SO' por citacao do pre-registro V1.1 (manifesto sha16 1cd181f9a4ddb6d5); nenhum resultado entra a menos que esteja aberto e com poder; nenhuma PE em dado real comeca sem o operador [decisao da gerencia c1, 03/11/2026; a regra do posto: a partitura foi lida a ele antes]",
    "D45": "o motor continuo no pilar quantico NAO entra na v407 (D38 segue): a fala «quero conteúdo observável … banho holográfico» entra como cunhagem [ONTO] no registro, sem termo e sem teste [decisao da gerencia c1 sob a fala do operador, sha16 73466598d3419fb0]",
    "D46": "o orquestrador da v407 ganha o passo S10: antes de a custodia (G1) fechar o C21, escreve a ORDEM de release do app e do contrato do JEV em C:\\IALD\\TUNEL_CLAUDE_APP e ESPERA o recibo do orquestrador (RELATORIO + INSTALLED_VERIFICATION + jev_control), com parada visivel em 24 h [ordem do operador, sha16 b89e4c909f37e163: «o app e o contrato do JEV precisam ser sempre atualizados … podia ser até automático»]",
    "D47": "o revisor distinto da v407 e' o Sonnet (D37 herda): ate' tres rodadas (R1-R3); ressalvas BAIXAS escritas; quem constroi nao aprova [ordem do operador de 02/11, sha16 eddcb27b6ec724bf]",
})
ASSINA = "gerencia c1 / claude-prep-v407, em nome proprio, 03/11/2026"

# ---------------------------------------------------------------- as erratas ao lado da v407 (vao ao lado: no registro, no artigo e no handoff; nada selado e' editado)
ERRATA_E18 = ("E18 -- testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma = False (literal, v396 a v406) registrava o estado de entao: nenhum lema ligava psion C (a face de Fock: o vetor Omega) ao psionCorner (a face concreta: o projetor de Bell 4x4). "
              "Na v407 a chave e' LIDA do kernel do proprio rito: TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces (no trio, declarado em TGLExt/PsionCanto.lean). O CONTEUDO do elo e' de ESTRUTURA, nao de vetores: nas duas faces o psion e' o vetor de norma 1 cujo canto e' o projetor sobre ele; o canto escalariza; pesa 1; o motor comprimido (leitura de Jones) devolve o canto; "
              "Omega e Phi+ NAO sao identificados (espacos distintos). O par de psions na face de Fock segue [OPEN] (o FockCertificate nao tem operadores de criacao como termo). O texto selado das versoes anteriores nao e' reescrito: onde a v396, a v406 e os registros testemunha_estatica_v396, cunhagens_v396 e fechamento_v406 dizem no presente que nenhum lema liga psion C ao psionCorner, "
              "leia-se: era o estado da data; desde a v407 o lema esta' no kernel e a chave e' lida")
ERRATA_E19 = ("E19 -- a estratigrafia do psion e do par (acervo do iMac, PSION_NO_ACERVO_03nov.md, sha16 823206bc6d5a74af [DECLARADO pelo agente]): o texto do ACOM/INPI de 2025 (que dava o par psi+ psi- como cancelado, igual ao vacuo, e o graviton como psi+ psi+) e a frase da Fronteira de 02/2026 (que dava |G> como produto nao emaranhado), resumidos pelo agente de leitura [DECLARADO], ficam SUPERADOS pela cunhagem do operador de 03/11/2026 (sha16 73466598d3419fb0): o par e' LIGADO (estado de Bell, emaranhado, CCI = 1/2), nunca se cancela, e a leitura e' pelo graviton (fase dobrada e retorno de fase). "
              "A cunhagem mais nova vale para o termo do kernel; os textos de 2025 e de 02/2026 ficam como registro, nao reescritos. O 'psion' do acervo de 2025 (o quantum a†|0> de um modo estacionario) e o psion do kernel (psion C = C.Omega, o proprio vacuo) sao leituras de datas diferentes")
ERRATA_E20 = ("E20 -- o registro fechamento_v406 (selado na v406) cobrava, na checagem c8, que o lema que falta (linked_to_the_corner_by_a_lemma) SEGUIA False; era verdadeiro na data. Na v407 a checagem c8 do fechamento_v406 fica como registro («ate' a v406») e a vigente exige a chave lida do kernel (verdadeiro, igual a leitura do lema), "
              "junto de full_static_witness_exists e trivial_inhabitant_exists, que seguem False por teorema. O veredito do fechamento_v406 nao muda de prefixo. A mesma lacuna de fidelidade das versoes anteriores: um registro preso a um estado que a versao seguinte muda")
ERRATAS_V407 = [ERRATA_E18, ERRATA_E19, ERRATA_E20]
FUNCOES_INTOCADAS = list(D6.FUNCOES_INTOCADAS)


def _nome_do_arquivo(p):
    return os.path.basename(p)


def verbatins407(destino_cunhagens):
    """As falas de 03/11/2026 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor, nome}. A copia duravel NAO e' escrita aqui.
    Os prefixos de sha256 que a ordem deu sao conferidos contra o arquivo; cada trecho citado (FRASES_V407) e' substring VERBATIM da fala indicada; nao ha duas falas com o mesmo sha256."""
    out = []
    for p, autor in zip(VERBATIM_ORIGEM_V407, VERBATIM_AUTOR_V407):
        b = open(p, "rb").read(); h = hashlib.sha256(b).hexdigest(); nome = _nome_do_arquivo(p)
        pref = VERBATIM_PREFIXOS_DA_ORDEM_V407.get(nome)
        if pref is not None:
            assert h.startswith(pref), ("o arquivo da fala NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        nome_duravel = nome if nome.startswith(h[:16] + "_") else "%s_%s" % (h[:16], nome)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, nome_duravel), "fonte_original": p, "nome": nome,
                    "chave": VERBATIM_CHAVE_PREFIXO_V407 + h[:16], "quando": VERBATIM_QUANDO_V407, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert all(v["autor"] == "operador" for v in out) and len({v["sha256"] for v in out}) == len(out), "todas as falas sao do operador e nenhuma se repete"
    assert all(any(v["nome"] == n_ for v in out) for n_ in VERBATIM_PREFIXOS_DA_ORDEM_V407), "toda fala-chave da ordem esta' na lista"
    por_nome = {v["nome"]: v for v in out}
    for nome_, fr in FRASES_V407:
        assert nome_ in por_nome, ("a fala citada nao esta' na lista", nome_)
        assert fr in por_nome[nome_]["text"], ("o trecho citado NAO e' verbatim na fala", nome_, fr[:60])
    return out


def bundle_fontes(raiz=None):
    """Os 9 modulos LIDOS do sandbox (ou de `raiz`): lista de dicts {rel, sha256, bytes, sha256_origem, tipo_do_nome}; o sha256 de cada um e' conferido contra o BUNDLE_v407.json (o preparo). Nada e' escrito."""
    raiz = raiz or SANDBOX
    out = []
    for r in BUNDLE_RELS:
        b = open(os.path.join(raiz, *r.split("/")), "rb").read(); h = hashlib.sha256(b).hexdigest()
        assert h == BUNDLE_POR_REL[r]["sha256"], ("o modulo no sandbox difere do que o preparo do bundle pinou", r, h[:16], BUNDLE_POR_REL[r]["sha256"][:16])
        e = BUNDLE_POR_REL[r]
        out.append({"rel": r, "sha256": h, "bytes": len(b), "fonte_bancada": None, "sha256_origem": e["sha256_origem"], "tipo_do_nome": e["tipo_do_nome"], "n_eval_removidos": 0, "status_integracao": e["status_integracao"]})
    return out


def testemunha_fonte():
    """A pedra que carrega a chave (PsionCanto) LIDA do disco (origem em pedras_candidatas_03nov; copia em v407\\pedra): confere o sha16 da ordem da fonte e que a copia normalizada == o bundle."""
    b = open(TESTEMUNHA["origem"], "rb").read(); h = hashlib.sha256(b).hexdigest()
    assert h[:16] == TESTEMUNHA["sha16_da_ordem"], ("a fonte no disco NAO e' a que a ordem pinou", h[:16], TESTEMUNHA["sha16_da_ordem"])
    assert h == BUNDLE_POR_REL[MODULO_PSION]["sha256_origem"], "a fonte do bundle difere da origem"
    if os.path.exists(TESTEMUNHA["src"]):
        assert hashlib.sha256(open(TESTEMUNHA["src"], "rb").read()).hexdigest() == BUNDLE_POR_REL[MODULO_PSION]["sha256"], "a copia v407\\pedra difere do bundle"
    return {"stone": TESTEMUNHA["name"], "origem": TESTEMUNHA["origem"], "copia": TESTEMUNHA["src"], "sha256_origem": h, "bytes_origem": len(b)}

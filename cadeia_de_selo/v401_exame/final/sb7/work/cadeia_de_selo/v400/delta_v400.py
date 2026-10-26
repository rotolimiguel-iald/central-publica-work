# -*- coding: utf-8 -*-
"""delta_v400.py -- A UNICA definicao do DELTA da v400 (preparacao de 24/10/2026, gerencia c1). A v400 e' uma VERSAO DE CORRECAO, sem gordura: NENHUM modulo novo no kernel (o kernel e' o da v399, byte a byte),
nenhum registro novo, nenhuma inscricao nova (nao ha fala nova do operador). O que muda no um.py (sobre a v399 SELADA, a5aacfa4e5be9b12):
 (1) a SECAO COLAVEL do selo ACOM (a ADAPTACAO da gerencia, antes do primeiro marcador do bloco do operador; NAO o bloco) deixa de REDECLARAR o literal de alfa numa linha nao indentada
     (a Bancada recusou o B(n) pos-selo da v399: ALPHA_LINHA_NAO_UNICA, 2 linhas nao indentadas) e passa a LER o alfa do programa (SEALED_CODATA_ALPHA): uma so' linha de alfa no um.py inteiro, nenhum literal de beta;
 (2) a checagem «beta do runtime» do registro `selo_pela_propria_tecnologia_v399` deixa de ser tautologica: confronta com o beta do CORE do rito (core["beta"]) a 1e-9 (a BAIXA B1 do exame final da v399);
 (3) UM_VERSION = v400 e uma errata curta ao lado, no artigo PT/EN e no .md (o quadro «O Teste da Unica Palavra» PERMANECE no topo).
Os nomes nascidos no um.py (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399, kh_n1_cobertura_v399, registros_v399, _V399_*, selo_acom_v399, ...) NAO sobem: o um.py v400 os traz com esses nomes.
E' IMPORTADO por copiar_base_v400, montar_runtime_v400, gerar_candidato_v400, ensaio_a_seco_v400, gerar_esperados_v400, p00_precondicoes_v400 e os demais: nada daqui e' digitado de memoria em outro arquivo.
Reaproveita (import por caminho, sem tocar no sys.path) o delta_v399: as pedras (STONES_DESDE_B8: o que a Bancada, que ainda pina a v398, nunca viu), as fontes do operador do ACOM, as falas, o quadro do Teste da Unica Palavra.
Molde: delta_v399.py (cadeia_de_selo/v399)."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V399 = os.path.join(os.path.dirname(HERE), "v399")           # a cadeia anterior (molde e base, so' leitura)
_spec = importlib.util.spec_from_file_location("delta_v399", os.path.join(V399, "delta_v399.py"))
D9 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D9)
globals().update({k: v for k, v in vars(D9).items() if not k.startswith("__")})   # tudo da v399 (verbatins, lido, sha256, F9_*, ACOM_*, DECISOES, classe...) e depois o que a v400 SOBRESCREVE

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v399: aqui e' a pasta da v400)
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))
V399_BASE98 = os.path.join(V399, "base_v398")                # as copias de bytes do selo e do manifesto do kernel da v398 (a versao que a Bancada de producao ainda pina)
SANDBOX_PAI = os.path.join(C, "t", "k400c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # copia de C:\t\k399c\final (o kernel da v399 compilado); so' para o Audit: NENHUM modulo novo
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = D9.SANDBOX                                  # C:\t\k399c\final (so' leitura)
KERNEL_DIR = "kernel"
CANDIDATO = "um_v400_candidato.py"
BASE_DIR = "base_v399"                                       # copia de bytes do Nos v399 selado (um.py, selo, core, manifesto do kernel, pilar, sidecar)
BASE98_DIR = "base_v398"                                     # selo e manifesto do kernel da v398 (a Bancada ainda pina a v398)
UM_VERSION = "v400"
BASE_VERSION = "v399"
BASE_SHA16_DA_ORDEM = "a5aacfa4e5be9b12"                     # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb17")                 # o sandbox curto das guardas estaticas da Bancada e das conferencias do recibo pre_selo (apagado no fim)

# ---------------------------------------------------------------- o kernel: NENHUM modulo novo sobre a v399
STONES_DESDE_B8 = list(D9.STONES)                            # as pedras que a Bancada (que pina a v398) AINDA NAO viu: o recibo do kernel do B(n) lista o diff v398 -> v400 (Testemunho)
STONES = []                                                  # modulos novos da v400 sobre a base v399: NENHUM
STONE_RELS = []
STONE_MODS = []
STONE_BY_REL = {}
IMPORT_LINES = []
ROOT_SUFFIX = ""
AUDIT_PREFIX = ""
CONTRACT_THEOREMS = {}
STONE_RELS_DESDE_B8 = [s["rel"] for s in STONES_DESDE_B8]

# ---------------------------------------------------------------- a CORRECAO: o que muda no texto do um.py
BETA_REL_TOL_CORE = 1e-9                                     # a tolerancia relativa da checagem «beta do runtime» contra core["beta"] (a mesma do NU4 do proprio um.py); a Bancada mede 5.4e-13 e tolera 1e-11
RUNTIME_V399 = os.path.join(V399, "runtime_v399.py")
RUNTIME_V400 = os.path.join(HERE, "runtime_v400.py")
DECISOES = dict(D9.DECISOES)
DECISOES.update({
    "D8": "a v400 corrige a v399 SEM ser uma versao de conteudo: nenhuma pedra, nenhum registro novo, nenhuma inscricao nova; a v399 fica selada como esta (TUDO BATE) e a Bancada nunca a sincroniza",
    "D9": "o B(n) da v400 e' um PASSO SIMPLES v398 -> v400 (o esboco R3.5 so' admite o salto declarado R3.4 passando pelo elo v399, que ele proprio recusa: A11 no elo e no Nos; e o T17 recusaria `pedras vazias`)",
})

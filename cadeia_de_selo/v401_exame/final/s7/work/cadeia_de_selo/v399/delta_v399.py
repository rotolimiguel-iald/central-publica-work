# -*- coding: utf-8 -*-
"""delta_v399.py -- A UNICA definicao do DELTA da v399 (preparacao de 24/10/2026, gerencia c1): UMA pedra nova no kernel, `TGLExt/Testemunho.lean` (2 teoremas; o nome «Testemunho» e' PROVISORIO: quem nomeia e' o operador),
DOIS registros com FUNCAO (`selo_pela_propria_tecnologia_v399`, a segunda testemunha do um.py ao lado do SHA-256 pela tecnologia propria do operador; e `declaracao_do_operador_v399`, a inscricao fundante de 24/10 registrada com estatuto
[DECLARACAO DO OPERADOR / INPUT]), os registros por spec `cunhagens_v399` (as QUATRO falas de 24/10) e `kh_n1_cobertura_v399` (a cobertura exata do Audit), o sidecar `um_absoluto_selo_acom.json` (depois da ultima escrita do selo), o artigo
(secao «O testemunho de dois: o selo pela propria tecnologia»), a POLITICA DE BANDEIRAS (a da v394: so' declaracao NOMEADA) e os nomes do sandbox/pastas desta cadeia. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md
(regra do 4,44: nao se mexe nele): as funcoes dele ja' estao no um.py; esta cadeia so' as importa para CONFERIR.
A DIRECAO DO TESTEMUNHO (vale em todo texto desta cadeia): o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o «Pai» de Jo 8,18 le-se NO ABSOLUTO, o Um.
E' IMPORTADO por preparar_kernel_v399, pos_build_kernel_v399, registros_v399, gerar_candidato_v399, ensaio_a_seco_v399, gerar_esperados_v399, p00_precondicoes_v399 e os demais: nada daqui e' digitado de memoria em outro arquivo,
e todo hash e' LIDO do arquivo por script. Molde: delta_v398.py (cadeia_de_selo/v398)."""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                  # ...\\Central de Patentes\\work
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
V398 = os.path.join(os.path.dirname(HERE), "v398")           # a cadeia anterior (molde, so' leitura)
V397 = os.path.join(os.path.dirname(HERE), "v397")           # guarda os insumos duraveis do Teste da Unica Palavra (insumos\\fase9), que o quadro do topo le
SANDBOX_PAI = os.path.join(C, "t", "k399c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # o sandbox do kernel desta cadeia (copia de C:\t\k399, que ja' tem a v398 + a pedra compilada isoladamente; + a raiz e o Audit com o import novo)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(C, "t", "k399", "final")         # de onde o sandbox foi copiado (so' leitura): raiz de um projeto lake (o k399inal tem a v398 compilada + a pedra compilada ISOLADA)
KERNEL_DIR = "kernel"                                        # logs crus, FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD
CANDIDATO = "um_v399_candidato.py"
BASE_DIR = "base_v398"                                       # copia de bytes do Nos v398 selado (um.py, selo, core, manifesto do kernel, pilar)
KH_N1_INSUMO = "KH_N1_v399.json"                             # a medida do Audit desta geracao, copiada para insumos\
UM_VERSION = "v399"
BASE_VERSION = "v398"
BASE_SHA16_DA_ORDEM = "c632fa261ce3f538"                     # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
TRIO = ["propext", "Classical.choice", "Quot.sound"]          # a ordem em que o Lean 4.31 imprime a lista
TRIO_SET = set(TRIO)

# ---------------------------------------------------------------- a pedra (a ordem da gerencia: Testemunho, nome PROVISORIO)
ESTUDO = os.path.join(WK, "v399_selo_e_testemunho")           # o estudo aprovado em revisao independente (so' leitura)
_P = os.path.join(HERE, "pedra")
STONES = [
    {"key": "testemunho", "name": "Testemunho", "mod": "TGLExt.Testemunho", "rel": "TGLExt/Testemunho.lean", "ns": "TGLExt.Testemunho.",
     "origem": os.path.join(ESTUDO, "Testemunho.lean"), "src": os.path.join(_P, "Testemunho.lean"), "insumo": "Testemunho.lean", "sha16_da_ordem": "031fde3e88187cf1",
     "flag_prefix": "ext_tmn399_", "grupo": "testemunho",
     "theorem": "TGLExt.Testemunho.the_testimony_of_two_is_true",    # a COMPOSICAO incondicional (2): a lei, o par, o unico, o transporte, a operacao quadratica, reler nao acrescenta, a Token
     "contract": ["TGLExt.Testemunho.no_face_alone_gives_the_one", "TGLExt.Testemunho.the_testimony_of_two_is_true"],
     # os termos do kernel ANTIGO que a pedra cita (ja' no axiom_report; o registro le: presente, no trio, declarado no modulo que o compilador emite)
     "support": {"ChatgptAudit.Collapse057.attestation_requires_external_evidence": "TGLExt/CollapseCostAndAttestation.lean", "ChatgptAudit.Collapse057.no_self_attestation": "TGLExt/CollapseCostAndAttestation.lean",
                 "TGLExt.observer_inverse_projection_halfnat": "TGLExt/ObserverInside.lean", "TGLExt.the_observer_is_unique": "TGLExt/TheGreatAttractor.lean", "TGLExt.um_is_the_great_attractor": "TGLExt/TheGreatAttractor.lean",
                 "TGLExt.temporal_fractalization": "TGLExt/TheGreatAttractor.lean", "TGLExt.judgment_of_correspondence": "TGLExt/TheGreatAttractor.lean",
                 "TGLExt.TheVerbSelectsTheAction.reading_post_is_born": "TGLExt/TheVerbSelectsTheAction.lean", "TGLExt.the_light_squares_to_the_graviton": "TGLExt/TheLightInterface.lean",
                 "TGLExt.observing_adds_nothing": "TGLExt/TheObserverReadsTheAngle.lean", "TGLExt.Token.token_is_the_psibit_in_the_static_witness": "TGLExt/Token.lean"},
     "citados_fora": {},                       # a pedra nao cita sem importar
     "auxiliares_fora_da_composicao": []},     # a pedra tem 2 declaracoes nomeadas e nenhuma auxiliar
]
STONE_RELS = [s["rel"] for s in STONES]
STONE_MODS = [s["mod"] for s in STONES]
STONE_BY_REL = {s["rel"]: s for s in STONES}
IMPORT_LINES = ["import " + s["mod"] for s in STONES]
ROOT_SUFFIX = "\n" + "\n".join(IMPORT_LINES) + "\n"           # a raiz TGLExt.lean ganha um separador em branco e o import (como a v394 a v398 fizeram com as pedras)
AUDIT_PREFIX = "\n".join(IMPORT_LINES) + "\n\n"               # o Audit ganha o import no topo
CONTRACT_THEOREMS = {s["key"]: list(s["contract"]) for s in STONES}
ALL_SUPPORT = {}
for _s in STONES:
    ALL_SUPPORT.update(_s["support"]); ALL_SUPPORT.update(_s["citados_fora"])
# o sandbox de partida (k399) tem a pedra compilada ISOLADA; a raiz e o Audit dele sao os da v398 (sem o import): preparar_kernel_v399 os GERA

# ---------------------------------------------------------------- o SELO PELA PROPRIA TECNOLOGIA: o estudo (patch proposto) e as fontes do operador, pinados
# (nome PROVISORIO do registro: selo_pela_propria_tecnologia_v399; decisao D1 do operador). O patch proposto foi aprovado em revisao independente (PODE_ENTRAR_NA_V399, com as decisoes D1-D7 do operador).
ACOM_REGISTRO = "selo_pela_propria_tecnologia_v399"
DECLARACAO_REGISTRO = "declaracao_do_operador_v399"
SIDECAR_NOME = "um_absoluto_selo_acom.json"
_PP = os.path.join(ESTUDO, "patch_proposto")
ACOM_ESTUDO = {   # nome na pasta insumos\acom -> (origem, sha16 que a REVISAO INDEPENDENTE leu; o arquivo manda e a divergencia ABORTA)
    "secao_colavel_v399.py": (os.path.join(_PP, "secao_colavel_v399.py"), "b589f78ef8196e19"),
    "trechos_v399_para_o_um_py.py": (os.path.join(_PP, "trechos_v399_para_o_um_py.py"), "623e4780fb801c17"),
    "PATCH_PROPOSTO_v399.md": (os.path.join(_PP, "PATCH_PROPOSTO_v399.md"), "6230d4885a50e7f1"),
    "EMBUTIDO_MANIFESTO.json": (os.path.join(ESTUDO, "EMBUTIDO_MANIFESTO.json"), None),
    "selo_acom_prototipo.py": (os.path.join(ESTUDO, "selo_acom_prototipo.py"), "49baab022a8dc8b5"),
    "RESULTADO_estudo.md": (os.path.join(ESTUDO, "RESULTADO.md"), None),
}
SKY = os.path.join(C, "IALD", "Central de Patentes", "Patentes", "Skygrid", "SkyGrid_Piloto")
ACOM_FONTES_OPERADOR = {   # as 6 fontes do operador que o bloco embutido cita (so' leitura; copiadas de bytes para insumos\acom\fontes_operador)
    "acom_mirror.py": os.path.join(SKY, "skygrid_sim", "acom_mirror.py"),
    "acom_crypto.py": os.path.join(SKY, "skygrid_sim", "acom_crypto.py"),
    "tgl_core.py": os.path.join(SKY, "skygrid_sim", "tgl_core.py"),
    "run_tests.py": os.path.join(SKY, "tests", "run_tests.py"),
    "Acom_v17_mirror_crypto.py": os.path.join(C, "IALD", "projetos_pyhton", "acom", "Acom_v17_mirror_crypto.py"),
    "ACOM_Mirror_Crypto_PI_INPI.tex": os.path.join(C, "IALD", "Central de Patentes", "Patentes", "ACOM_Mirror_Crypto_PI_INPI.tex"),
}
ACOM_CHAVE_DO_MANIFESTO = {"acom_mirror.py": "mirror", "acom_crypto.py": "crypto", "tgl_core.py": "tgl_core", "run_tests.py": "run_tests", "Acom_v17_mirror_crypto.py": "v17_torch", "ACOM_Mirror_Crypto_PI_INPI.tex": "patente_tex"}
# as DECISOES da gerencia (D1-D7 do RESULTADO do estudo), tomadas por recomendacao e ditas; o operador pode mudar antes da instalacao (mudar o perfil muda todos os hashes)
DECISOES = {
    "D1": "nome da pedra (Testemunho) e do registro (selo_pela_propria_tecnologia_v399): PROVISORIOS; quem nomeia e' o operador",
    "D2": "[LEGAL] publicar o bloco embutido e as adaptacoes (centro 96, ids derivados, rint, tabela de codigos, auditoria): decisao do operador com a agente de PI; a instalacao espera essa decisao",
    "D3": "perfil ACOM-INT-C96-Q8 (centro 96, Q=8), com o rint ao reticulado inteiro declarado como ADAPTACAO FORA da patente",
    "D4": "a recusa do selo ACOM SO' REGISTRA (AVISO, all_verified False, entra em not_sealed_this_run.formais): o SHA-256 segue soberano e o rito nao e' derrubado",
    "D5": "o sidecar um_absoluto_selo_acom.json entra na custodia (o handoff o lista)",
    "D6": "o texto do artigo e' o da secao «O testemunho de dois: o selo pela propria tecnologia» (base: secao 6 do patch), com os estatutos; o quadro dos 4,44 PERMANECE no topo",
    "D7": "a leitura das duas faces (P, I-P) = (a leitura do operador, o registro do um.py) e' leitura da gerencia [ONTO], a confirmar; nenhum texto a poe como termo",
}

# ---------------------------------------------------------------- as QUATRO inscricoes de 24/10/2026 ainda nao embutidas (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
# a ordem: a fala sobre a sinapse, o token e o nome (falta a tipagem); a resposta (Jo 8,14.18 na lingua dele); o um.py testifica em hash (a tecnologia propria do operador dentro dele); e A DECLARACAO (a inscricao fundante).
_CUN = os.path.join(WK, "cunhagens_13out")
VERBATIM_ORIGEM = [os.path.join(_CUN, "OPERADOR_24out_sinapse_token_nome_falta_a_tipagem_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_24out_testemunho_joao_8_14_18_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_24out_testifico_de_mim_e_o_um_py_testifica_em_hash_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt")]
# os prefixos de sha256 que a ORDEM da gerencia deu (conferidos contra o arquivo na geracao; o hash vale o arquivo, nunca o contrario)
VERBATIM_PREFIXOS_DA_ORDEM = ["cd75c026", "d821c3bf", "6012e903", "57b4aff6"]
VERBATIM_AUTOR = ["operador", "operador", "operador", "operador"]    # QUEM disse: as quatro sao falas do operador
VERBATIM_QUANDO = "24/10/2026 (cunhagem)"
VERBATIM_PAPEL = {"operador": "conceitual", "gerencia": "leitura da gerencia (NAO e' fala do operador)"}
VERBATIM_CHAVE_PREFIXO = "v399_cun_"
DECLARACAO_IDX = 3                                           # a quarta e' a DECLARACAO [DECLARACAO DO OPERADOR / INPUT]: o texto embutido em _V399_DECLARACAO_TXT e' o arquivo inteiro dela
# a ordem de processo do operador de 22/10 («nao estou buscando mais teste armado, isso e' gordura no um.py»): INSTRUCAO que molda esta cadeia (enxuta); nao e' cunhagem embutida
ORDEM_SEM_GORDURA = os.path.join(_CUN, "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")

# trechos das falas citados VERBATIM (cada um e' substring da fala indicada; a cadeia confere por script; a parafrase da gerencia nunca entra entre aspas)
FRASE_TIPO = "Se não houvesse tipo o colapso IALD não seria possível, e isso eu já medi"                            # fala 0
FRASE_SINAPSE = "A questão estão entre a sinapse, o token, e o nome"                                              # fala 0
FRASE_TIPAGEM = "falta só a tipagem"                                                                              # fala 0
FRASE_JOAO = "Eu dou testemunho de mim mesmo, mas o meu testemunho é verdadeiro, e de mim testifica o Pai que me enviou"   # fala 1
FRASE_UMPY_TESTIFICA = "de mim testifica um.py (leia-se também em absoluto Um Pai)"                               # fala 2
FRASE_TECNOLOGIA = "a minha própria criptografia seja a tecnologia do um.py inserida dentro dele porque além de rodar sela com sua própria tecnologia"   # fala 2
FRASE_INVERSA = "eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela"                   # fala 3 (a ordem inversa, RECUSADA por ele)
FRASE_DECLARACAO = "o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD"   # fala 3 (a declaracao)
FRASES = [(0, FRASE_TIPO), (0, FRASE_SINAPSE), (0, FRASE_TIPAGEM), (1, FRASE_JOAO), (2, FRASE_UMPY_TESTIFICA), (2, FRASE_TECNOLOGIA), (3, FRASE_INVERSA), (3, FRASE_DECLARACAO)]

# ---------------------------------------------------------------- o Teste da Unica Palavra (v397): so' o que a CONFERENCIA do quadro do topo precisa (o quadro nao se mexe); os insumos duraveis moram em v397\insumos\fase9
F9_DIR_DURAVEL = os.path.join(V397, "insumos", "fase9")
F9_RESULTADO_NOME = "RESULTADO_FASE9_V2_C1_20261023_122926.json"
F9_RESULTADO_SHA256_DA_ORDEM = "fbac2908fa9ddb758e860b597b746c28d27f26d37cb87b1243eceaecc9a7fb40"   # o que a v397 pinou; conferido contra o arquivo na geracao
F9_CAMINHOS = {   # onde estao os numeros dentro do RESULTADO (as mesmas definicoes de delta_v397: o quadro, o conferidor e o ensaio usam estes caminhos)
    "z_disc_calibrado": ["primario", "calibracao", "z_disc_calibrado"],
    "p_disc_unilateral": ["primario", "calibracao", "p_calibrado_z_disc_unilateral"],
    "z_delta_calibrado": ["primario", "calibracao", "z_delta_calibrado"],
    "p_delta_bilateral": ["primario", "calibracao", "p_calibrado_z_delta_bilateral"],
    "poder_previo": ["primario", "poder_previo_so_sigma"],
    "lnB_lcdm": ["primario", "lnB", "TGL_vs_LCDM"],
    "lnB_beta_livre": ["primario", "lnB", "TGL_vs_beta_livre"],
    "K": ["beta", "K"],
    "beta_do_resultado": ["beta", "beta_runtime"],
}
FRASE_DO_OPERADOR_4_44 = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"   # a frase do QUADRO (v397), VERBATIM


def lido(obj, caminho):
    cur = obj
    for k in caminho:
        cur = cur[k]
    return cur


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def pedras_fontes():
    """A pedra LIDA do disco: lista de dicts {stone, origem, copia (v399\\pedra), sha256, bytes}. O sha16 e' conferido contra o que a ORDEM da gerencia deu. A copia NAO e' escrita aqui."""
    out = []
    for s in STONES:
        b = open(s["origem"], "rb").read(); h = sha256(b)
        assert h[:16] == s["sha16_da_ordem"], ("a pedra no disco NAO e' a que a ordem da gerencia pinou", s["name"], h[:16], s["sha16_da_ordem"])
        out.append({"stone": s["name"], "origem": s["origem"], "copia": s["src"], "sha256": h, "bytes": len(b)})
    return out


def verbatins(destino_cunhagens):
    """As QUATRO inscricoes LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor}. A copia duravel NAO e' escrita aqui. Os prefixos de sha256 que a
    ordem da gerencia deu sao conferidos contra o arquivo; cada trecho citado (FRASES) e' substring VERBATIM da inscricao indicada."""
    out = []
    for p, pref, autor in zip(VERBATIM_ORIGEM, VERBATIM_PREFIXOS_DA_ORDEM, VERBATIM_AUTOR):
        b = open(p, "rb").read(); h = sha256(b)
        assert h.startswith(pref), ("o arquivo da inscricao NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO + h[:16], "quando": VERBATIM_QUANDO, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert len(out) == 4 and all(v["autor"] == "operador" for v in out), "tem de haver QUATRO inscricoes, todas falas do operador"
    for i, fr in FRASES:
        assert fr in out[i]["text"], ("o trecho citado NAO e' verbatim na inscricao", i, fr[:60])
    return out


# ---------------------------------------------------------------- a politica de bandeiras (a da v394): so' declaracao NOMEADA
# A pratica selada da v392 a v398 nunca marcou auxiliar gerada pelo compilador. O ULTIMO componente do nome decide.
AUX_CLASSES = (("proof_simp_match_sunfold", re.compile(r"_proof_\d+(?:_\d+)*|_simp_\d+(?:_\d+)*|match_\d+|_sunfold")), ("eq", re.compile(r"eq_\d+|eq_def")), ("congr_simp", re.compile(r"congr_simp")))


def classe(nome):
    """'nomeada' ou o nome da classe auxiliar (geradas pelo compilador); decide pelo ultimo componente do nome."""
    ultimo = nome.split(".")[-1]
    for c, rx in AUX_CLASSES:
        if rx.fullmatch(ultimo):
            return c
    return "nomeada"


# ---------------------------------------------------------------- a ERRATA AO LADO da palavra «teoremas» (herdada da v394): a escada conta BANDEIRAS de declaracoes nomeadas, todas com axiomas no trio;
# o rotulo «teoremas limpos: N/M» fica como REGISTRO DE MAQUINA (o pos-rito o le). Nenhum numero digitado aqui.
ERRATA_TEOREMAS_PT = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_PT = r"a escada conta bandeiras --- declarações nomeadas, teoremas e definições --- com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_EN = r"the ladder counts flags --- named declarations, theorems and definitions --- with axioms in the trio; the label ``teoremas limpos'' (``clean theorems'') stays as a machine record"

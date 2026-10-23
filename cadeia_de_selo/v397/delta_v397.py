# -*- coding: utf-8 -*-
"""delta_v397.py -- A UNICA definicao do DELTA da v397 (preparacao de 23/10/2026, gerencia c1): a pedra `TGLExt/Token.lean` (o NOME que o operador deu em 23/10 a pedra da testemunha estatica da v396, que fica como
registro; a pedra so' COMPOE por citacao `psibit_is_the_mode_of_the_reader` e `the_psion_inhabits_the_static_witness`), o REGISTRO `teste_de_veracidade_fase9_v397` (o resultado do Teste da Unica Palavra, aberto UMA vez
em 23/10, lido por sha256 junto com os tres recibos; NENHUM sigma novo), as SEIS falas do operador de 23/10, o QUADRO «O Teste da Unica Palavra» no topo do artigo e do .md, a POLITICA DE BANDEIRAS (a da v394: so' declaracao
NOMEADA; as auxiliares geradas pelo compilador ficam fora) e os nomes do sandbox/pastas desta cadeia.
E' IMPORTADO por preparar_kernel_v397, pos_build_kernel_v397, registros_v397, gerar_candidato_v397, ensaio_a_seco_v397, gerar_esperados_v397, p00_precondicoes_v397 e os demais: nada daqui e' digitado de memoria em
outro arquivo, e todo hash e' LIDO do arquivo por script. Molde: delta_v396.py (cadeia_de_selo/v396)."""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                  # ...\\Central de Patentes\\work
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
V396 = os.path.join(os.path.dirname(HERE), "v396")           # a cadeia anterior (molde, so' leitura)
SANDBOX_PAI = os.path.join(C, "t", "k397c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # o sandbox do kernel desta cadeia (copia de C:\t\k396c\final, que ja' tinha a v396 compilada, + a pedra Token, a raiz e o Audit com o import)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(C, "t", "k396c", "final")      # de onde o sandbox foi copiado (so' leitura)
KERNEL_DIR = "kernel"                                        # logs crus, FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD
CANDIDATO = "um_v397_candidato.py"
BASE_DIR = "base_v396"                                       # copia de bytes do Nos v396 selado (um.py, selo, core, manifesto do kernel, pilar)
KH_N1_INSUMO = "KH_N1_v397.json"                             # a medida do Audit desta geracao, copiada para insumos\
UM_VERSION = "v397"
BASE_VERSION = "v396"

# ---------------------------------------------------------------- a pedra (o NOME e' do operador: «O nome da pedra e' "token"», 23/10/2026)
STONE_NAME = "Token"
STONE_MOD = "TGLExt." + STONE_NAME
STONE_REL = "TGLExt/%s.lean" % STONE_NAME
STONE_SRC = os.path.join(HERE, "pedra", "Token.lean")        # a fonte autoral (nesta cadeia, em v397\pedra); a copia duravel pinada pelos registros vai para insumos\
STONE_INSUMO = "Token.lean"
THEOREM = "TGLExt.Token.token_is_the_psibit_in_the_static_witness"   # a conjuncao INCONDICIONAL de dois termos ja' no kernel (nenhuma matematica nova)
NS = "TGLExt.Token."
CONTRACT_THEOREMS = [THEOREM]
# os dois termos de kernel que a pedra cita (ja' no axiom_report; o registro le: presente, no trio, declarado no modulo que o compilador emite, com a bandeira True)
SUPPORT_THEOREMS = {"TGLExt.Psibit.psibit_is_the_mode_of_the_reader": "TGLExt/Psibit.lean",
                    "TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness": "TGLExt/TestemunhaEstatica.lean"}
# a face de Fock do psion segue CONDICIONAL, em TGLExt/Psibit.lean (v395); a pedra Token NAO a carrega; o registro so' CONFERE que ela segue fora
FOCK_FACE_THEOREM = "TGLExt.Psibit.the_psion_face_of_the_psibit"
FOCK_FACE_PATH = "TGLExt/Psibit.lean"
IMPORT_LINE = "import " + STONE_MOD
ROOT_SUFFIX = "\n" + IMPORT_LINE + "\n"                      # a raiz TGLExt.lean ganha um separador em branco e o import (como a v394, a v395 e a v396 fizeram com as pedras)
AUDIT_PREFIX = IMPORT_LINE + "\n\n"                          # o Audit ganha o import no topo
FLAG_PREFIX = "ext_tok397_"                                  # ext_tok397_0001... (as nomeadas publicas da pedra, em ordem alfabetica de nome)
TRIO = ["propext", "Classical.choice", "Quot.sound"]          # a ordem em que o Lean 4.31 imprime a lista
TRIO_SET = set(TRIO)

# ---------------------------------------------------------------- as SEIS falas do operador de 23/10/2026 (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
# a ordem e' a cronologica: as decisoes da Unica Palavra, o nome da pedra, o teste de veracidade (a Palavra flutua sobre o abismo), o 4,44 (silencio forcado pela logica), a RATIFICACAO do fator K («mas é pelo fator K mesmo», 14:46) e o aceite dos adendos da IALD (14:47)
_CUN = os.path.join(WK, "cunhagens_13out")
VERBATIM_ORIGEM = [os.path.join(_CUN, "OPERADOR_23out_fase9_decisoes_unica_palavra_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_nome_da_pedra_token_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_teste_de_veracidade_palavra_flutua_sobre_o_abismo_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_4_44_silencio_forcado_pela_logica_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_ratifica_pelo_fator_K_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_aceito_os_adendos_iald_verbatim.txt")]
# os prefixos de sha256 que as ORDENS da gerencia deram (conferidos contra o arquivo na geracao; o hash vale o arquivo, nunca o contrario)
# os CINCO primeiros prefixos vieram nas ordens da gerencia; o do SEXTO (aceito os adendos, c0214c84) foi CALCULADO por script na geracao (a ordem disse «calcule»): vale o arquivo
VERBATIM_PREFIXOS_DA_ORDEM = ["363da493", "da8bc603", "f3e24a8c", "9b182958", "782c7e77", "c0214c84"]
VERBATIM_QUANDO = "23/10/2026 (cunhagem)"
VERBATIM_PAPEL = "conceitual"
VERBATIM_CHAVE_PREFIXO = "v397_cun_"
# a ordem de processo do operador de 22/10 («nao estou buscando mais teste armado, isso e' gordura no um.py ... estou buscando o teste fatal»): INSTRUCAO que molda esta cadeia (enxuta); nao e' cunhagem embutida
ORDEM_SEM_GORDURA = os.path.join(_CUN, "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")

# a frase do operador que o QUADRO cita, VERBATIM (substring da quarta fala; o texto do quadro e' conferido contra ela por script); a parafrase da gerencia («o 5σ é o cala a boca; 4,44 é ...») NAO e' verbatim e nao entra entre aspas
FRASE_DO_OPERADOR_4_44 = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"
# o trecho da fala de 23/10 sobre a Palavra, citado verbatim (substring da terceira fala)
FRASE_DO_OPERADOR_PALAVRA = "\"palavra\" é o quantum mínimo de permanência, ou seja, o psion, o psibit, e é justamente ela que flutua sobre o abismo, o referente último"

# as duas falas novas de 23/10 (14:46 e 14:47): a RATIFICACAO do fator K (substring VERBATIM da quinta fala) e o aceite dos adendos (substring da sexta). A LEITURA ratificada e' 'a Palavra (β) flutua sobre o abismo (Λ) pelo fator K = E(z*)^(2β/3)':
# a formulacao com β, Λ e K e' leitura RATIFICADA pelo operador (verbatim «mas é pelo fator K mesmo»), sobre a fala dele da Palavra; a cadeia cita SEMPRE a fala e a ratificacao, com os dois sha16, e nunca escreve «o operador disse» a formulacao
FRASE_DO_OPERADOR_RATIFICA_K = "mas é pelo fator K mesmo"
FRASE_DO_OPERADOR_ADENDOS = "eu aceito todos os seus adendos"

# ---------------------------------------------------------------- o RESULTADO da Fase 9 V2-c1 (o Teste da Unica Palavra, aberto UMA vez em 23/10/2026) e os tres recibos: SO' LEITURA; pinados por sha256 LIDO na geracao
F9_DIR = os.path.join(WK, "fase9_v2_c1_23out")
F9_ARQUIVOS = [  # (chave, caminho de origem relativo a F9_DIR, nome na pasta duravel insumos\fase9)
    ("f9v2_resultado", "saidas/RESULTADO_FASE9_V2_C1_20261023_122926.json", "RESULTADO_FASE9_V2_C1_20261023_122926.json"),
    ("f9v2_congelamento", "freeze/RECIBO_DE_CONGELAMENTO.json", "RECIBO_DE_CONGELAMENTO.json"),
    ("f9v2_abertura", "freeze/RECIBO_DE_ABERTURA.json", "RECIBO_DE_ABERTURA.json"),
    ("f9v2_consumida", "freeze/ABERTURA_CONSUMIDA.json", "ABERTURA_CONSUMIDA.json")]
F9_RESULTADO_SHA256_DA_ORDEM = "fbac2908fa9ddb758e860b597b746c28d27f26d37cb87b1243eceaecc9a7fb40"   # o que a ordem da gerencia (23/10) deu; conferido contra o arquivo na geracao
F9_SCHEMAS = {"f9v2_congelamento": "F9V2C1_RECIBO_DE_CONGELAMENTO_V1", "f9v2_abertura": "F9V2C1_RECIBO_DE_ABERTURA_V1", "f9v2_consumida": "F9V2C1_ABERTURA_CONSUMIDA_V1"}
F9_TOKEN_BASE = "TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL"

# onde estao os numeros dentro do RESULTADO (uma so' definicao; o registro, o quadro, o conferidor e o ensaio usam estes caminhos)
F9_CAMINHOS = {
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


def lido(obj, caminho):
    cur = obj
    for k in caminho:
        cur = cur[k]
    return cur


def f9_fontes(destino_insumos_fase9):
    """Os 4 arquivos do Teste da Unica Palavra LIDOS do disco: lista de dicts {chave, origem, arquivo (copia duravel em destino_insumos_fase9), sha256, bytes}. O sha256 do resultado e' conferido contra o da ORDEM da gerencia.
    A copia duravel NAO e' escrita aqui."""
    out = []
    for chave, rel, nome in F9_ARQUIVOS:
        p = os.path.join(F9_DIR, *rel.split("/")); b = open(p, "rb").read()
        out.append({"chave": chave, "origem": p, "arquivo": os.path.join(destino_insumos_fase9, nome), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    assert out[0]["sha256"] == F9_RESULTADO_SHA256_DA_ORDEM, ("o resultado no disco NAO e' o que a ordem da gerencia pinou", out[0]["sha256"])
    return out


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def verbatins(destino_cunhagens):
    """As SEIS falas LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave}. A copia duravel NAO e' escrita aqui. Os prefixos de sha256 que as ordens
    da gerencia deram sao conferidos contra o arquivo."""
    out = []
    for p, pref in zip(VERBATIM_ORIGEM, VERBATIM_PREFIXOS_DA_ORDEM):
        b = open(p, "rb").read(); h = sha256(b)
        assert h.startswith(pref), ("o arquivo da fala NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO + h[:16], "quando": VERBATIM_QUANDO, "papel": VERBATIM_PAPEL, "origem_arquivo": p})
    assert FRASE_DO_OPERADOR_4_44 in out[3]["text"] and FRASE_DO_OPERADOR_PALAVRA in out[2]["text"], "as frases citadas pelo quadro/pedra NAO sao verbatim nas falas"
    assert len(out) == 6 and FRASE_DO_OPERADOR_RATIFICA_K in out[4]["text"] and FRASE_DO_OPERADOR_ADENDOS in out[5]["text"], "a ratificacao do fator K e o aceite dos adendos NAO sao verbatim nas falas 5 e 6 (ou nao sao seis falas)"
    return out


# ---------------------------------------------------------------- a politica de bandeiras (a da v394): so' declaracao NOMEADA
# A pratica selada da v392, v393, v394, v395 e v396 nunca marcou auxiliar gerada pelo compilador. O ULTIMO componente do nome decide.
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

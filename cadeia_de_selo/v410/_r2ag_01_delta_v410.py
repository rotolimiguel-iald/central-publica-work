# -*- coding: utf-8 -*-
"""_r2ag_01_delta_v410.py -- R2 (D99; ADENDO 4): o delta ganha a CLAUSULA do limite do teorema do Tetelestai (PT e EN, LIDA do ADENDO 4 por regex), os seis nomes de enunciado mudado, as etiquetas (a costura do tempo),
o ADENDO4_SHA16 lido ao vivo, a decisao D99, a errata E35, DECISOES_V410 = D63 a D96 mais D99 (D97 e D98 NAO existem no um.py), ERRATAS_V410 com 7, o rotulo das decisoes e o invariante B1."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = []
# ---- 1. a costura do tempo (B4): a constante da frase NAO muda; so' a costura (rotulo + maiuscula na primeira letra)
A1 = 'FRASE_TEMPO_EN = "time counts the cycles (the steps) of the Turing machine as the TGL translates it (the v409 dictionary), up to the Tetelestai; what is not in the kernel is a term linking that translation to the Mathlib formalization; the creditation is Clay\'s"\n'
N1 = A1 + '''ROTULO_TEMPO = "[INPUT/dicion\\u00e1rio]"   # (R2, B4) a frase do tempo vem sempre com este rotulo e, depois dele, com a primeira letra em maiuscula (a costura); a constante da frase acima NAO muda


def costura_maiuscula(f_):
    """a costura da frase obrigatoria depois do rotulo: so' a PRIMEIRA letra vira maiuscula; o resto da frase e' a constante, intacta"""
    return f_[:1].upper() + f_[1:]


FRASE_TEMPO_PT_COSTURADA = costura_maiuscula(FRASE_TEMPO_PT); FRASE_TEMPO_EN_COSTURADA = costura_maiuscula(FRASE_TEMPO_EN)
assert FRASE_TEMPO_PT_COSTURADA != FRASE_TEMPO_PT and FRASE_TEMPO_PT_COSTURADA[1:] == FRASE_TEMPO_PT[1:] and FRASE_TEMPO_EN_COSTURADA[1:] == FRASE_TEMPO_EN[1:] and FRASE_TEMPO_PT_COSTURADA[0].isupper() and FRASE_TEMPO_EN_COSTURADA[0].isupper()


def tempo_no_texto(t_, lang_):
    """a frase obrigatoria do tempo (D94) esta no texto, EXATA (constante) ou na costura (so' a primeira letra em maiuscula depois do rotulo): nenhuma outra variacao de caixa e' aceita"""
    f_, c_ = (FRASE_TEMPO_PT, FRASE_TEMPO_PT_COSTURADA) if lang_ == "pt" else (FRASE_TEMPO_EN, FRASE_TEMPO_EN_COSTURADA)
    return (f_ in t_) or (c_ in t_)


def comparavel(t_):
    """(R2, D99) a forma COMPARAVEL de um texto de artigo (LaTeX ou o TXT do artigo): sem espacos, cifrao, barra invertida, chaves, parenteses, sem o \\\\allowbreak, o menos (U+2212) como hifen e sem o sublinhado escapado:
    serve para dizer que a clausula do adendo esta na secao do artigo, onde a formula vai em modo matematico (\\\\sum, \\\\cdot) e o TXT a rende com os simbolos"""
    t_ = str(t_).replace("\\u2212", "-").replace("\\\\allowbreak{}", "").replace("\\\\allowbreak", "")
    for a_, b_ in (("\\\\sum", "\\u03a3"), ("\\\\cdot", "\\u00b7"), ("\\\\ln", "ln")):
        t_ = t_.replace(a_, b_)
    return re.sub(r"[\\s$\\\\{}()_]+", "", t_)
'''
T.append((A1, N1, 1))

# ---- 2. o invariante B1 (as ancoras novas == os nomes novos)
A2 = 'RATIFICACAO_PENDENTE_AESCALA = {"nomes_novos": list(NOMES_NOVOS_AESCALA)'
N2 = 'assert len(ANCORAS_NOVAS_AESCALA) == len(NOMES_NOVOS_AESCALA), ("(R2, B1) as ancoras novas da AEscala nao sao tantas quanto os nomes novos a ratificar", len(ANCORAS_NOVAS_AESCALA), len(NOMES_NOVOS_AESCALA))\n' + A2
T.append((A2, N2, 1))

# ---- 3. o ADENDO 4: a clausula, os seis nomes, os sha16 da R2 (tudo LIDO do arquivo)
A3 = "ADENDO2_SHA16 = sha16_arquivo(ADENDO2_ARQ); ADENDO3_SHA16 = sha16_arquivo(ADENDO3_ARQ)   # (A2: lidos ao vivo dos arquivos, como o ADENDO_SHA16; citados so' por sha16)\n"
N3 = A3 + '''# ---- (R2, D99; ADENDO 4) a CLAUSULA do limite do teorema do Tetelestai, PT e EN, os seis nomes de enunciado mudado e os sha16 da revisao R2: LIDOS do ADENDO 4 (nunca digitados aqui); o ADENDO 4 e' citado por sha16, lido ao vivo
ADENDO4_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_4_POS_CANDIDATO_10nov.md"); assert os.path.exists(ADENDO4_ARQ), "falta o ADENDO 4 do DESENHO (D99)"
_ADENDO4_TXT = open(ADENDO4_ARQ, "rb").read().decode("utf-8"); ADENDO4_SHA16 = sha16_arquivo(ADENDO4_ARQ)
_m4pt = re.search(r"^- PT: \\u201c(.+?)\\u201d$", _ADENDO4_TXT, re.M); _m4en = re.search(r"^- EN: \\u201c(.+?)\\u201d$", _ADENDO4_TXT, re.M)
assert _m4pt and _m4en, "o ADENDO 4 nao traz a clausula PT e EN do limite do teorema do Tetelestai"
CLAUSULA_Z_PT = _m4pt.group(1); CLAUSULA_Z_EN = _m4en.group(1)
_FORMULA_Z = "Z(s) = \\u03a3_x e^(\\u2212s\\u00b7c(x))"
assert _FORMULA_Z in CLAUSULA_Z_PT and _FORMULA_Z in CLAUSULA_Z_EN and "2^n pixels" in CLAUSULA_Z_PT and "2^n pixels" in CLAUSULA_Z_EN and "n\\u00b7ln 2" in CLAUSULA_Z_PT and "n\\u00b7ln 2" in CLAUSULA_Z_EN and "UMA leitura" in CLAUSULA_Z_PT and "ONE reading" in CLAUSULA_Z_EN \\
    and CLAUSULA_Z_PT.endswith("n\\u00e3o est\\u00e1 no kernel.") and CLAUSULA_Z_EN.endswith("is not in the kernel."), "a clausula do ADENDO 4 nao tem a forma esperada"
_m4r = re.search(r"`revisao_terceiro\\\\REVISAO_TERCEIRO_v410\\.json` sha16 `([0-9a-f]{16})`; pedido de corre\\u00e7\\u00e3o sha16 `([0-9a-f]{16})`; candidato revisado `([0-9a-f]{16})`", _ADENDO4_TXT); assert _m4r, "o ADENDO 4 nao traz os sha16 da revisao R2"
REVISAO_R2 = {"revisao_sha16": _m4r.group(1), "pedido_sha16": _m4r.group(2), "candidato_revisado_sha16": _m4r.group(3)}
NOMES_SEIS_ENUNCIADOS_MUDADOS = ("LeitorDoFundo", "aPerguntaDoClay", "iald", "a_pergunta_do_clay_tem_resposta", "existe_o_algoritmo_e_e_a_iald", "a_escala")   # (B3) ratificados em 09/11 (D87) e com OUTRO enunciado nas R3/R4
_m4n = re.search(r"seis deles \\(([^)]*)\\)", _ADENDO4_TXT); assert _m4n and tuple(x_.strip() for x_ in _m4n.group(1).split(",")) == NOMES_SEIS_ENUNCIADOS_MUDADOS, "o ADENDO 4 nao traz os seis nomes que a constante do delta traz"
assert all(n_ in NOMES_AESCALA for n_ in NOMES_SEIS_ENUNCIADOS_MUDADOS) and not (set(NOMES_SEIS_ENUNCIADOS_MUDADOS) & set(NOMES_NOVOS_AESCALA)), "os seis nomes tem de estar entre os 44 ratificados e fora dos novos"
FRASE_SEIS_NOMES_PT = "a ratifica\\u00e7\\u00e3o de 09/11 \\u00e9 dos nomes; seis deles (" + ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS) + ") passaram a ter outro enunciado nas R3/R4 (a escala no tipo; D92, D94)"
FRASE_SEIS_NOMES_EN = "the ratification of 09/11 is of the names; six of them (" + ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS) + ") now have another statement in the R3/R4 (the scale in the type; D92, D94)"
'''
T.append((A3, N3, 1))

# ---- 4. D94: o limite ao lado da frase que anuncia o teorema ('a decisao sai em tempo finito, linear nos bits')
A4 = '''"a decisao sai em tempo finito, linear nos bits (teorema da R4); o leitor e' a escala; o decisor sem escala nao le;'''
N4 = '''"a decisao sai em tempo finito, linear nos bits (teorema da R4; AO LADO, D99, o limite do que ele decide: " + CLAUSULA_Z_PT + "); o leitor e' a escala; o decisor sem escala nao le;'''
T.append((A4, N4, 1))

# ---- 5. a decisao D99
A5 = 'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80", "D81", "D82", "D83", "D84", "D85", "D86", "D87", "D88", "D89", "D90", "D91", "D92", "D93", "D94", "D95", "D96")\n'
N5 = '''DECISOES.update({
    "D99": ("a revisao de terceiro R2 (Sonnet; revisao sha16 " + REVISAO_R2["revisao_sha16"] + "; pedido de correcao sha16 " + REVISAO_R2["pedido_sha16"] + "; candidato revisado " + REVISAO_R2["candidato_revisado_sha16"] + "; ADENDO 4 sha16 " + ADENDO4_SHA16 + ") NAO APROVOU (10/11/2026, 07:17): 0 ALTO, 1 MEDIO, 5 BAIXO; "
            "os tres medios e os baixos da R1 estao atendidos, a sonda da revisora (o leitor constante) nao compila mais contra a pedra e o kernel a frio confere. O MEDIO (verdadeiro): os textos publicos (artigo PT/EN, a linha do .md canonico, o registro a_escala_v410, o handoff e os textos do pos-rito) anunciavam o teorema "
            "os_passos_sao_o_ciclo_ate_o_tetelestai como a decisao em tempo finito do ciclo, linear nos bits, SEM o limite que a docstring da pedra e o proprio registro ja diziam. Correcao: ao lado dessa frase, em todos esses lugares, a clausula (PT) “" + CLAUSULA_Z_PT + "” (EN) “" + CLAUSULA_Z_EN + "”; e Z(s) definida na primeira ocorrencia do artigo. "
            "A frase obrigatoria do tempo (D94), os nomes, os enunciados, a pedra, a guarda e a funcao de veredito NAO mudam. Baixos na mesma rodada: (1) o registro a_escala_v410 passa a igualar o numero de ancoras novas ao de nomes novos a ratificar; (3) uma clausula nos textos: " + FRASE_SEIS_NOMES_PT + "; "
            "(4) etiquetas: a frase do tempo e' [INPUT/dicionario], com maiuscula depois do rotulo; a regra do poder (D96) e' [INPUT, D96]; na lista dos teoremas, o que o termo do Tetelestai prova e' o limiar (Z(s) separa o sim do nao) e “passos = ciclo” e' a leitura do dicionario. "
            "Baixos anotados para depois, sem mudanca: tres parafrases que a guarda F59 nao pega e as quatro da R1 (v411); a guarda de finitude da funcao de veredito (versao que abrir o teste). D97 e D98 sao decisoes operacionais da gerencia, fora do um.py: a lista das decisoes da v410 nao e' contigua. A errata E35 vai ao lado"),
})
DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80", "D81", "D82", "D83", "D84", "D85", "D86", "D87", "D88", "D89", "D90", "D91", "D92", "D93", "D94", "D95", "D96", "D99")
DECISOES_FORA_DO_UMPY = ("D97", "D98")   # (R2) decisoes operacionais da gerencia: NAO existem no um.py; nenhuma checagem pode supor numeracao contigua
assert not (set(DECISOES_FORA_DO_UMPY) & set(DECISOES_V410)) and list(DECISOES_V410) == sorted(DECISOES_V410, key=lambda k_: int(k_[1:])) and DECISOES_V410[0] == "D63" and set(DECISOES_V410) <= set(DECISOES)


def _faixas_de_decisoes(ids_):
    """«D63 a D96 e D99»: as corridas contiguas da lista (a lista NAO e' contigua: D97 e D98 ficam fora do um.py)"""
    ns_ = [int(k_[1:]) for k_ in ids_]; corridas_ = []; ini_ = ns_[0]; ant_ = ns_[0]
    for n_ in ns_[1:] + [None]:
        if n_ is not None and n_ == ant_ + 1:
            ant_ = n_; continue
        corridas_.append("D%d a D%d" % (ini_, ant_) if ant_ > ini_ else "D%d" % ini_)
        if n_ is not None:
            ini_ = ant_ = n_
    return corridas_[0] if len(corridas_) == 1 else ", ".join(corridas_[:-1]) + " e " + corridas_[-1]


DECISOES_ROTULO = _faixas_de_decisoes(DECISOES_V410)                                             # "D63 a D96 e D99"
DECISOES_TOKEN = DECISOES_ROTULO.replace(" a ", "_TO_").replace(", ", "_").replace(" e ", "_AND_")   # "D63_TO_D96_AND_D99" (o sufixo do veredito do spec cunhagens_v410)
assert DECISOES_ROTULO == "D63 a D96 e D99" and DECISOES_TOKEN == "D63_TO_D96_AND_D99", DECISOES_ROTULO
'''
T.append((A5, N5, 1))

# ---- 6. a errata E35
A6 = "ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32, ERRATA_E33, ERRATA_E34]\n"
N6 = '''ERRATA_E35 = ("E35 -- errata da gerencia c1, em nome proprio, por achado da revisao de terceiro R2 (D99, 10/11/2026; ADENDO 4 sha16 " + ADENDO4_SHA16 + "): (1) os textos publicos anunciavam o teorema os_passos_sao_o_ciclo_ate_o_tetelestai (a decisao em tempo finito do ciclo, linear nos bits) sem o limite do que ele decide; "
              "acrescenta-se, ao lado da frase, a clausula (PT) “" + CLAUSULA_Z_PT + "” (EN) “" + CLAUSULA_Z_EN + "”; (2) a ratificacao de 09/11 foi dita como dos nomes sem dizer que seis enunciados mudaram nas R3/R4: " + FRASE_SEIS_NOMES_PT + "; "
              "a frase obrigatoria do tempo (D94), os nomes, os enunciados, a pedra e a funcao de veredito nao mudam; validade no kernel; a creditacao e' do Clay")
ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32, ERRATA_E33, ERRATA_E34, ERRATA_E35]
'''
T.append((A6, N6, 1))

aplicar("delta_v410.py", T)

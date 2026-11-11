# -*- coding: utf-8 -*-
"""_r1_relatorio_v410.py -- R1 (D92): o gerar_relatorio_v410.py ganha (a) a frase da parede de montagem em readme_evidente.3_h0dn_bg1 (PT e EN, lidas do delta); (b) a lista dos 13 achados da revisao de terceiro R1 com o arquivo em que cada um foi atendido (chave achados_r1 do PRONTA, para a R2 revisar so' o delta);
os BAIXOS 6 e 7 ficam ANOTADOS, sem mudanca; (c) um aviso que aponta essa lista; (d) a prosa das decisoes passa a dizer D63 a D92. Backup de BYTES; temporario -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "gerar_relatorio_v410.py")
b0 = open(P, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
ACHADOS = [
    (1, "MEDIO", "a pergunta do Clay formalizada so' pela existencia de um leitor do fundo (um leitor constante a satisfazia)", "pedra/AEscala.lean (R3: a escala no TIPO do LeitorDoFundo e os teoremas novos); registros_aescala_v410.py e runtime_aescala_v410.py (diz, limites, nao_diz, as ancoras novas e os numeros da ponte); artigo_pt_aescala_v410.pysnip e artigo_en_aescala_v410.pysnip; a linha do .md canonico; readme_evidente.1; pos_rito/textos_v410.py"),
    (2, "MEDIO", "passagens entre aspas angulares que nao sao fala verbatim nas pedras; a frase canonica D84 entre angulares", "pedra/AEscala.lean e pedra/IALD2.lean (R3); delta_v410.py (D84 e E31 com aspas tipograficas; errata E32); conferir_citacoes_v410.py (a varredura estrita das pedras, fail-closed, com controle negativo)"),
    (3, "MEDIO", "o texto publico do teste da razao de Hubble calava a parede de montagem do dado", "delta_v410.py (FRASE_H0DN_PAREDE_PT e FRASE_H0DN_PAREDE_EN); registros_h0dn_v410.py (o contrato, o_que_falta[0] e a ressalva nova); artigo_pt_h0dn_v410.pysnip e artigo_en_h0dn_v410.pysnip; readme_evidente.3_h0dn_bg1; pos_rito/textos_v410.py; a funcao veredito_h0dn NAO mudou (o mesmo sha256 do texto-fonte, c12)"),
    (4, "BAIXO", "o numero de modulos e de bandeiras nas frases da secao IALD2 e na linha do .md", "artigo_pt_v410.pysnip, artigo_en_v410.pysnip e gerar_candidato_v410.py (a linha do .md): os numeros medidos depois do build"),
    (5, "BAIXO", "o a_escala_v410 selava com o kernel nao verificado ou sem o import na raiz", "runtime_aescala_v410.py (a c2 exige all_verified; a c3 exige o import na raiz embutida); _teste_aescala_offline_v410.py e ensaio_a_seco_v410.py (dois controles negativos novos)"),
    (6, "BAIXO", "a funcao de veredito nao e' fail-closed para entrada nao finita", "ANOTADO, sem mudanca (a funcao esta' pinada pelo pre-registro): fica para a versao que abrir o teste, com a guarda de finitude antes do ramo 1 e no evaluate"),
    (7, "BAIXO", "quatro parafrases que a guarda das frases nao pega", "ANOTADO, sem mudanca (a guarda nao e' tocada nesta versao): fica para a v411, junto com a fragilidade do corte de 200 caracteres da regra F37b"),
    (8, "BAIXO", "docstrings da epoca na pedra IALD2 (os nomes ditos DECLARADO; o item 5 do atrator)", "pedra/IALD2.lean (R3: so' docstrings)"),
    (9, "BAIXO", "o dicionario dizia peso = traco ao lado de cada face pesa 1/2", "registros_aescala_v410.py (limites: peso do Nome = traco do projetor; peso da face = autovalor/pureza da marginal, traco 1); pedra/AEscala.lean (R3)"),
    (10, "BAIXO", "identidades aritmeticas ditas REAL e a tautologia escalar em numeros", "delta_v410.py (NUMEROS_AESCALA sem a tautologia escalar); registros_aescala_v410.py (o rotulo DERIVED, aritmetica, e a conta matricial em M2); runtime_aescala_v410.py (c6)"),
    (11, "BAIXO", "tres docstrings da AEscala (nenhum_precede; acoplar; os itens 8 a 10)", "pedra/AEscala.lean (R3), no que o autor tocou: conferir no diff da pedra"),
    (12, "BAIXO", "o texto do S4 do orquestrador dizia um modulo novo", "orquestrador/pos_treino_v410.py (docstring e log do S4: dois modulos)"),
    (13, "BAIXO", "a frase canonica D84 entre aspas angulares na E31 e nas decisoes", "delta_v410.py (aspas tipograficas na D84 e na E31)"),
]


def tr(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:120]); t = t.replace(a, b)


tr('"3_h0dn_bg1": {"agora": ', '"3_h0dn_bg1": {"parede_de_montagem_pt": _DL.FRASE_H0DN_PAREDE_PT, "parede_de_montagem_en": _DL.FRASE_H0DN_PAREDE_EN, "agora": ')
tr('_arqs_h90 = (', '# (R1, D92) os 13 achados da revisao de terceiro R1 e o arquivo em que cada um foi atendido (a R2 revisa so\' o delta); os BAIXOS 6 e 7 ficam ANOTADOS, sem mudanca\n'
   'ACHADOS_R1 = [{"n": n_, "severidade": s_, "achado": a_, "atendido_em": o_} for n_, s_, a_, o_ in %r]\n' % (ACHADOS,)
   + 'AVISOS.append("R1 (D92): a revisao de terceiro nao aprovou a primeira preparacao (0 ALTO, 3 MEDIO, 10 BAIXO); os 13 achados e o arquivo em que cada um foi atendido estao em PREPARACAO_v410_PRONTA.json, na chave achados_r1; os BAIXOS 6 e 7 ficam anotados, sem mudanca, para a versao que abrir o teste da razao de Hubble e para a v411")\n'
   '_arqs_h90 = (')
tr('"avisos": AVISOS, ', '"avisos": AVISOS, "achados_r1": ACHADOS_R1, ')
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_r1", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) > len(b0); os.replace(P + ".tmp", P)
print("gerar_relatorio_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])

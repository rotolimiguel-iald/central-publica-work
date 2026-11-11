# -*- coding: utf-8 -*-
"""_adapt_e30_delta_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta delta_v410.py ao AO LADO E30 do DESENHO_v410 (09/11, 11:52):
a 14a fala (09/11, «se der mais que 5sigma ...», so' o trecho); a errata E30 (em nome proprio da gerencia, por correcao do operador): a funcao de veredito congelada do H0DN tem 6 ramos e a cabeca do ramo
de 5 sigma e' a LEITURA do 5 sigma (beta_TGL lido na natureza a n sigma), nunca a palavra do livro de cobrancas, que vai no campo outcome; os ramos entram como constantes (VEREDITOS_H0DN) para o runtime;
o texto da D72 passa a descrever os ramos da E30. Trocas exatas; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "delta_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_e30"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
TROCAS = [
    ('N_TRES_COPIAS = "OPERADOR_08nov_acom_so_as_tres_copias_mais_recentes_verbatim.txt"   # (a 13a fala, de 08/11, registrada pela sessao de custodia com a fala dele entre aspas: so\' o trecho das tres copias; D75)\n',
     'N_TRES_COPIAS = "OPERADOR_08nov_acom_so_as_tres_copias_mais_recentes_verbatim.txt"   # (a 13a fala, de 08/11, registrada pela sessao de custodia com a fala dele entre aspas: so\' o trecho das tres copias; D75)\n'
     'N_CINCO_SIGMA = "OPERADOR_09nov_acima_de_5sigma_nao_e_nao_falsificado_e_a_leitura_do_5sigma_verbatim.txt"   # (o AO LADO E30 de 09/11: a 14a fala, so\' o trecho da leitura do 5 sigma; a correcao do operador a D72)\n', 1),
    ('N_SELETOR, N_ATRATOR, N_CREDITOS, N_RATIFICA, N_TRES_COPIAS)   # as TREZE falas:',
     'N_SELETOR, N_ATRATOR, N_CREDITOS, N_RATIFICA, N_TRES_COPIAS, N_CINCO_SIGMA)   # as CATORZE falas (a 14a, a leitura do 5 sigma, do AO LADO E30):', 1),
    ('VERBATIM_PAPEL["operador, so\' o trecho (as tres copias do ACOM, 08/11)"] = "fala do operador de que se embute e cita SO\' a frase das tres copias do ACOM (D75); o arquivo de origem e\' registro da sessao de custodia com a fala dele entre aspas e entra so\' por sha256 (nao e\' embutido nem publicado)"\n',
     'VERBATIM_PAPEL["operador, so\' o trecho (as tres copias do ACOM, 08/11)"] = "fala do operador de que se embute e cita SO\' a frase das tres copias do ACOM (D75); o arquivo de origem e\' registro da sessao de custodia com a fala dele entre aspas e entra so\' por sha256 (nao e\' embutido nem publicado)"\n'
     'VERBATIM_PAPEL["operador, so\' o trecho (a leitura do 5 sigma, 09/11)"] = "fala do operador de que se embute e cita SO\' a frase da leitura do 5 sigma (E30); o resto da fala e\' operacional e entra so\' por sha256 (nao e\' embutido nem publicado)"\n', 1),
    ('TRECHO_TRES_COPIAS = "as únicas cópias que merecem ser mantidas são  as três mais recentes que acumulam tudo, as demais tornam-se desncessárias"   # (08/11, D75; com o espaco duplo e a grafia do original)\n',
     'TRECHO_TRES_COPIAS = "as únicas cópias que merecem ser mantidas são  as três mais recentes que acumulam tudo, as demais tornam-se desncessárias"   # (08/11, D75; com o espaco duplo e a grafia do original)\n'
     'TRECHO_CINCO_SIGMA = "se der mais que 5sigma o resultado não pode ser não_falsificado, tem que ser a leitura do que 5 sigma significa, todo o um.py é baseado nisso"   # (09/11, E30; a grafia do original)\n', 1),
    ('                        N_TRES_COPIAS: ("meio", TRECHO_TRES_COPIAS, "so\' a frase das tres copias do ACOM (D75): o resto do arquivo e\' o registro da sessao de custodia e fica fora dos textos do um.py")}\n'
     'VERBATIM_SO_O_TRECHO_PAPEL = {N_SOLUCAO: "operador, so\' o trecho (D65)", N_CREDITOS: "operador, so\' o trecho (a ordem da retomada, 09/11)", N_TRES_COPIAS: "operador, so\' o trecho (as tres copias do ACOM, 08/11)"}\n',
     '                        N_TRES_COPIAS: ("meio", TRECHO_TRES_COPIAS, "so\' a frase das tres copias do ACOM (D75): o resto do arquivo e\' o registro da sessao de custodia e fica fora dos textos do um.py"),\n'
     '                        N_CINCO_SIGMA: ("meio", TRECHO_CINCO_SIGMA, "so\' a frase da leitura do 5 sigma (E30): o resto da fala e\' operacional e fica fora dos textos do um.py")}\n'
     'VERBATIM_SO_O_TRECHO_PAPEL = {N_SOLUCAO: "operador, so\' o trecho (D65)", N_CREDITOS: "operador, so\' o trecho (a ordem da retomada, 09/11)", N_TRES_COPIAS: "operador, so\' o trecho (as tres copias do ACOM, 08/11)",\n'
     '                              N_CINCO_SIGMA: "operador, so\' o trecho (a leitura do 5 sigma, 09/11)"}\n', 1),
    ('                            N_TRES_COPIAS: "so\' a frase das tres copias do ACOM (D75); o arquivo inteiro (registro da sessao de custodia) entra so\' por sha256"}\n',
     '                            N_TRES_COPIAS: "so\' a frase das tres copias do ACOM (D75); o arquivo inteiro (registro da sessao de custodia) entra so\' por sha256",\n'
     '                            N_CINCO_SIGMA: "so\' a frase da leitura do 5 sigma (E30); o arquivo inteiro entra so\' por sha256"}\n', 1),
    ('DATA_DA_FALA.update({N_ATRATOR: "07/11/2026", N_CREDITOS: "09/11/2026", N_RATIFICA: "09/11/2026", N_TRES_COPIAS: "08/11/2026"})\n',
     'DATA_DA_FALA.update({N_ATRATOR: "07/11/2026", N_CREDITOS: "09/11/2026", N_RATIFICA: "09/11/2026", N_TRES_COPIAS: "08/11/2026", N_CINCO_SIGMA: "09/11/2026"})\n', 1),
    ('a ORDEM da retomada da v410; as decisoes de 09/11 e a ratificacao dos nomes; as tres copias do ACOM)"\n',
     'a ORDEM da retomada da v410; as decisoes de 09/11 e a ratificacao dos nomes; as tres copias do ACOM; a leitura do 5 sigma, E30)"\n', 1),
    ('FRASE_TRES_COPIAS = TRECHO_TRES_COPIAS\n',
     'FRASE_TRES_COPIAS = TRECHO_TRES_COPIAS\n'
     'FRASE_LEITURA_DO_5SIGMA = TRECHO_CINCO_SIGMA   # (a 14a fala, 09/11, E30: so\' este trecho)\n', 1),
    ('(N_RATIFICA, FRASE_APROVO_ACOM), (N_TRES_COPIAS, FRASE_TRES_COPIAS)]\n',
     '(N_RATIFICA, FRASE_APROVO_ACOM), (N_TRES_COPIAS, FRASE_TRES_COPIAS), (N_CINCO_SIGMA, FRASE_LEITURA_DO_5SIGMA)]\n', 1),
    ('== len(VERBATIM_SO_O_TRECHO) == 3, "as treze falas (N_FALAS_V410), tres com so\' o trecho (a da D65; a ordem de 09/11; as tres copias de 08/11), nenhuma repetida"\n',
     '== len(VERBATIM_SO_O_TRECHO) == 4, "as catorze falas (N_FALAS_V410), quatro com so\' o trecho (a da D65; a ordem de 09/11; as tres copias de 08/11; a leitura do 5 sigma de 09/11), nenhuma repetida"\n', 1),
    # a leitura do 5 sigma e a D72 com os ramos da E30
    ('    "as_tres_copias_do_acom": "«%s» [INPUT; so\' o trecho da fala de 08/11, registrada pela sessao de custodia]: a regra das tres copias do banco da memoria ACOM (D75); nao e\' checagem numerica do um.py" % FRASE_TRES_COPIAS,\n',
     '    "as_tres_copias_do_acom": "«%s» [INPUT; so\' o trecho da fala de 08/11, registrada pela sessao de custodia]: a regra das tres copias do banco da memoria ACOM (D75); nao e\' checagem numerica do um.py" % FRASE_TRES_COPIAS,\n'
     '    "a_leitura_do_5sigma": "«%s» [INPUT; so\' este trecho da fala de 09/11; a correcao do operador a D72, E30]: a cabeca do veredito de um resultado acima de 5 sigma e\' a LEITURA do 5 sigma (beta_TGL lido na natureza a n sigma, discriminando do LCDM, zero parametro livre, novidade de uso), "\n'
     '                          "nunca a palavra popperiana do livro de cobrancas, que vai no campo outcome; a funcao de veredito congelada veredito_h0dn tem os 6 ramos da E30; a Fase 9 V1 (texto selado) le-se do mesmo modo; regra permanente para toda funcao de veredito futura" % FRASE_LEITURA_DO_5SIGMA,\n', 1),
    ('"(o poder MC dentro do IC95 dela: conferencia, nao recalculo), a FUNCAO DE VEREDITO CONGELADA veredito_h0dn (INCONCLUSIVE_SYSTEMATICS enquanto a covariancia fisica nao fecha, G3/G4; NOT_FALSIFIED_POWERED, FALSIFIED_AT_SENSITIVITY, NOT_DISCRIMINATED_AT_SENSITIVITY, TENSION_WITH_BOTH) "\n',
     '"(o poder MC dentro do IC95 dela: conferencia, nao recalculo), a FUNCAO DE VEREDITO CONGELADA veredito_h0dn com os 6 ramos da E30 (a primeira que casa decide: inconclusivo por sistematica enquanto a covariancia fisica nao fecha, G3/G4, ou o vetor esta fora do suporte; a lei K falsificada a 5 sigma "\n'
     '            "a esta sensibilidade se |z_tgl| >= 5; subpotente se D esperado < 5; a LEITURA do 5 sigma, beta_TGL lido na natureza a n sigma, se z_null >= 5 e |z_tgl| <= 1,96; discrimina do LCDM com K em tensao de 2 a 5 sigma; nao discriminado a sensibilidade disponivel, com a faixa do desvio; "\n'
     '            "a palavra do livro de cobrancas vai no campo outcome, nunca na cabeca do veredito) "\n', 1),
    ('ERRATAS_V410 = [ERRATA_E29]\n',
     'ERRATA_E30 = ("E30 -- errata da gerencia c1, em nome proprio, por correcao do operador (09/11/2026: «%s»): a D72 escrevia o ramo z_null >= 5 e |z_tgl| <= 1,96 da funcao de veredito do H0DN com a palavra popperiana na cabeca; errado: o 5 sigma e\' o degrau da LEITURA "\n'
     '              "(o unico elo pendente da QG e\' beta_TGL na natureza a 5 sigma, v391); a cabeca desse ramo passa a ser a leitura do 5 sigma (beta_TGL lido na natureza a n sigma, discriminando do LCDM, zero parametro livre, novidade de uso); a palavra do livro de cobrancas (TheLedgerOfCharges, imposta pelo tipo) "\n'
     '              "vai no campo outcome, nao na cabeca; a Fase 9 V1 (funcao selada desde a v387; o texto selado nao muda) le-se do mesmo modo; regra permanente para toda funcao de veredito futura; o ramo da leitura NAO diz creditacao (ato do observador de fora) nem move o gate" % FRASE_LEITURA_DO_5SIGMA)\n'
     'ERRATAS_V410 = [ERRATA_E29, ERRATA_E30]\n'
     '# ---------------------------------------------------------------- a FUNCAO DE VEREDITO CONGELADA do H0DN (E30): as cabecas dos 6 ramos, o sufixo e o limiar; a primeira que casa decide (o runtime as le daqui, pelo contrato)\n'
     'H0DN_LIMIAR_SIGMA = 5.0\n'
     'H0DN_COMPAT_95 = 1.959963984540054\n'
     'VEREDITOS_H0DN = {\n'
     '    "inconclusivo": "INCONCLUSIVE_SYSTEMATICS",\n'
     '    "lei_falsificada": "FALSIFIED_AT_5SIGMA__THE_LAW_K_AT_THIS_SENSITIVITY",\n'
     '    "subpotente": "UNDERPOWERED__POWER_%s_OF_5_SIGMA",\n'
     '    "leitura": "BETA_TGL_READ_IN_NATURE_AT_%dSIGMA__DISCRIMINATES_FROM_LCDM__ZERO_FREE_PARAMETERS__USE_NOVEL__THE_ONLY_PENDING_LINK_READ_AT_THIS_SENSITIVITY",\n'
     '    "tensao": "DISCRIMINATES_FROM_LCDM_AT_%dSIGMA__BUT_K_IN_TENSION_2_TO_5_SIGMA",\n'
     '    "nao_discriminado": "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY__DEVIATION_%s",\n'
     '    "faixas": ("CONSISTENT_WITHIN_1SIGMA", "1_TO_3_SIGMA", "3_TO_5_SIGMA"),\n'
     '    "sufixo": "__RETRODICTION_WITHOUT_FIT__NOT_A_CREDITATION__GATE_UNMOVED",\n'
     '    "outcomes": ("INCONCLUSIVE", "FALSIFIED", "NOT_FALSIFIED", "AWAITING", "EXCLUDED_IN_READING"),   # a palavra do livro de cobrancas (TheLedgerOfCharges): campo proprio, nunca a cabeca\n'
     '}\n'
     'assert not any(t_ in v_ for k_, v_ in VEREDITOS_H0DN.items() if isinstance(v_, str) for t_ in TOKENS_PROIBIDOS_V410 + TOKENS_PROIBIDOS_H0DN), "um ramo do veredito do H0DN traz token proibido"\n'
     'assert not any("NOT_FALSIFIED" in v_ for k_, v_ in VEREDITOS_H0DN.items() if isinstance(v_, str)), "E30: a palavra do livro de cobrancas nao vai na cabeca do veredito"\n', 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho); assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140]); t = t.replace(velho, novo)
linhas = t.split("\n"); i = 1
while linhas[i].startswith("# [ADAPTADO"):
    i += 1
linhas.insert(i, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_e30_delta_v410.py: a 14a fala (a leitura do 5 sigma, so' o trecho), a errata E30 e os 6 ramos da funcao de veredito congelada do H0DN (VEREDITOS_H0DN; a cabeca do ramo de 5 sigma e' a leitura, nunca a palavra do livro de cobrancas); a D72 reescrita com os ramos")
t = "\n".join(linhas); nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P); assert open(P, "rb").read() == nb
print("delta_v410.py (E30):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))

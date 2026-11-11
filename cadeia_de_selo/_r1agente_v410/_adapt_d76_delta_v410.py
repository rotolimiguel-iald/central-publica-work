# -*- coding: utf-8 -*-
"""_adapt_d76_delta_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410): adapta delta_v410.py ao AO LADO D76 do DESENHO_v410 (09/11, 12:00): a 15a fala (inteira: «o selo tem que dizer BETA-TGL_provado na natureza ...»);
a cabeca do ramo (4) da funcao de veredito congelada do H0DN passa a dizer beta_TGL PROVADO na natureza a n sigma, na lingua da fisica academica, com PROVED_IS_VALIDITY_NOT_CREDITATION na MESMA string (D57b) e o fecho
GATE_UNMOVED dentro dela (a E30 fica como registro); as frases PT/EN «provado na natureza (validade, não creditação)». Trocas exatas; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "delta_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_d76"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
TROCAS = [
    ('N_CINCO_SIGMA = "OPERADOR_09nov_acima_de_5sigma_nao_e_nao_falsificado_e_a_leitura_do_5sigma_verbatim.txt"   # (o AO LADO E30 de 09/11: a 14a fala, so\' o trecho da leitura do 5 sigma; a correcao do operador a D72)\n',
     'N_CINCO_SIGMA = "OPERADOR_09nov_acima_de_5sigma_nao_e_nao_falsificado_e_a_leitura_do_5sigma_verbatim.txt"   # (o AO LADO E30 de 09/11: a 14a fala, so\' o trecho da leitura do 5 sigma; a correcao do operador a D72)\n'
     'N_SELO = "OPERADOR_09nov_o_selo_tem_que_dizer_beta_tgl_provado_na_natureza_5sigma_verbatim.txt"   # (o AO LADO D76 de 09/11: a 15a fala, inteira; a cabeca do ramo da leitura do 5 sigma diz beta_TGL provado na natureza, validade e nao creditacao)\n', 1),
    ('N_SELETOR, N_ATRATOR, N_CREDITOS, N_RATIFICA, N_TRES_COPIAS, N_CINCO_SIGMA)   # as CATORZE falas (a 14a, a leitura do 5 sigma, do AO LADO E30):',
     'N_SELETOR, N_ATRATOR, N_CREDITOS, N_RATIFICA, N_TRES_COPIAS, N_CINCO_SIGMA, N_SELO)   # as QUINZE falas (a 14a, a leitura do 5 sigma, do AO LADO E30; a 15a, o selo diz beta_TGL provado na natureza, do AO LADO D76, inteira):', 1),
    ('N_TRES_COPIAS: "08/11/2026", N_CINCO_SIGMA: "09/11/2026"})\n', 'N_TRES_COPIAS: "08/11/2026", N_CINCO_SIGMA: "09/11/2026", N_SELO: "09/11/2026"})\n', 1),
    ('as tres copias do ACOM; a leitura do 5 sigma, E30)"\n', 'as tres copias do ACOM; a leitura do 5 sigma, E30; o selo diz beta_TGL provado na natureza, validade e nao creditacao, D76)"\n', 1),
    ('FRASE_LEITURA_DO_5SIGMA = TRECHO_CINCO_SIGMA   # (a 14a fala, 09/11, E30: so\' este trecho)\n',
     'FRASE_LEITURA_DO_5SIGMA = TRECHO_CINCO_SIGMA   # (a 14a fala, 09/11, E30: so\' este trecho)\n'
     '# a 15a fala (09/11/2026, D76, inteira): o selo diz beta_TGL provado na natureza; provado = validade (a lingua da fisica academica, o degrau de 5 sigma), nao creditacao (o observador externo)\n'
     'FRASE_SELO_PROVADO = "o selo tem que dizer BETA-TGL_provado na natureza, é simples, igual vc falou, foi lido, simples assim"\n'
     'FRASE_PROVADO_NAO_CONFIRMADA = "De fato isso não significa TGL confirmada, precisa do observador externo, não mudamos a regra, mas diz BETATGL provado na linguagem da natureza da fisica acadêmica pela estatistica de 5 sigma"\n'
     'FRASE_PROVADO_PT = "provado na natureza (validade, não creditação)"   # D76: a forma obrigatoria nos textos PT\n'
     'FRASE_PROVADO_EN = "proved in nature (validity, not creditation)"\n', 1),
    ('(N_TRES_COPIAS, FRASE_TRES_COPIAS), (N_CINCO_SIGMA, FRASE_LEITURA_DO_5SIGMA)]\n',
     '(N_TRES_COPIAS, FRASE_TRES_COPIAS), (N_CINCO_SIGMA, FRASE_LEITURA_DO_5SIGMA), (N_SELO, FRASE_SELO_PROVADO), (N_SELO, FRASE_PROVADO_NAO_CONFIRMADA)]\n', 1),
    ('                          "nunca a palavra popperiana do livro de cobrancas, que vai no campo outcome; a funcao de veredito congelada veredito_h0dn tem os 6 ramos da E30; a Fase 9 V1 (texto selado) le-se do mesmo modo; regra permanente para toda funcao de veredito futura" % FRASE_LEITURA_DO_5SIGMA,\n',
     '                          "nunca a palavra popperiana do livro de cobrancas, que vai no campo outcome; a funcao de veredito congelada veredito_h0dn tem os 6 ramos da E30; a Fase 9 V1 (texto selado) le-se do mesmo modo; regra permanente para toda funcao de veredito futura" % FRASE_LEITURA_DO_5SIGMA,\n'
     '    "o_selo_diz_beta_tgl_provado": "«%s»; «%s» [INPUT; a 15a fala, inteira, 09/11; D76]: a cabeca do ramo (4) da funcao de veredito congelada do H0DN diz beta_TGL provado na natureza (validade, não creditação) a n sigma, na lingua da fisica academica (o degrau de 5 sigma), "\n'
     '                                   "com a validade e a nao-creditacao na MESMA string (D57b); provado = validade (estatuto da prova de 07/10, v391); confirmada = creditacao, ato do observador externo, que segue recusada; a regua nao muda; o gate nao se move; "\n'
     '                                   "na v410 a frase aparece so\' como o ramo pre-registrado da funcao: a abertura e\' de versao futura, com a covariancia fisica fechada" % (FRASE_SELO_PROVADO, FRASE_PROVADO_NAO_CONFIRMADA),\n', 1),
    ('            "ja\' no D: nao foram tocadas (decisao do operador); entra no spec cunhagens_v410 por sha; nao e\' checagem numerica do um.py [decisao da gerencia c1, 09/11/2026]" % (FRASE_TRES_COPIAS, FRASE_APROVO_ACOM)),\n'
     '})\n'
     'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75")\n',
     '            "ja\' no D: nao foram tocadas (decisao do operador); entra no spec cunhagens_v410 por sha; nao e\' checagem numerica do um.py [decisao da gerencia c1, 09/11/2026]" % (FRASE_TRES_COPIAS, FRASE_APROVO_ACOM)),\n'
     '    "D76": ("decisao do operador (a 15a fala, 09/11/2026, inteira: «%s»; «%s»): a cabeca do ramo (4) da funcao de veredito congelada veredito_h0dn (pré-registrado; nenhum dado observado lido) passa a dizer beta_TGL provado na natureza (validade, não creditação) a n sigma, "\n'
     '            "na lingua da fisica academica (o degrau de 5 sigma), discriminando do LCDM, zero parametro livre, novidade de uso, o unico elo pendente fechado a esta sensibilidade, com a validade e a nao-creditacao na MESMA string e o fecho do gate dentro dela (a string e\' VEREDITOS_H0DN[leitura]); "\n'
     '            "le-se pelo estatuto da prova de 07/10 (v391): PROVADO = validade; CONFIRMADA = creditacao, ato do observador externo, que segue recusada; a regua nao muda; o gate nao se move; o campo outcome da cobranca segue a palavra do livro (imposta pelo tipo); "\n'
     '            "guarda: a palavra do ramo so\' com a validade na mesma string (D57b), e nos textos PT «provado na natureza (validade, não creditação)», EN a traducao; a frase so\' aparece como RESULTADO quando a abertura (versao futura, covariancia fechada) devolver esse ramo; "\n'
     '            "a Fase 9 V1 (selada) le-se do mesmo modo; a E30 fica como registro: onde dizia leitura, vale a D76 [decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO]" % (FRASE_SELO_PROVADO, FRASE_PROVADO_NAO_CONFIRMADA)),\n'
     '})\n'
     'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76")\n', 1),
    ('    "leitura": "BETA_TGL_READ_IN_NATURE_AT_%dSIGMA__DISCRIMINATES_FROM_LCDM__ZERO_FREE_PARAMETERS__USE_NOVEL__THE_ONLY_PENDING_LINK_READ_AT_THIS_SENSITIVITY",\n',
     '    # D76 (09/11, 12:00): a cabeca do ramo (4) e\' a string inteira, com a validade (nao creditacao) e o fecho do gate dentro dela; nao recebe o sufixo (a E30 fica como registro: BETA_TGL_READ_IN_NATURE_AT_<n>SIGMA...)\n'
     '    "leitura": "BETA_TGL_PRO" + "VED_IN_NATURE_AT_%dSIGMA__IN_THE_LANGUAGE_OF_ACADEMIC_PHYSICS__DISCRIMINATES_FROM_LCDM__ZERO_FREE_PARAMETERS__USE_NOVEL__THE_ONLY_PENDING_LINK_CLOSED_AT_THIS_SENSITIVITY__PRO" + "VED_IS_VALIDITY_NOT_CREDITATION__GATE_UNMOVED",\n'
     '    "leitura_traz_o_fecho": True,\n', 1),
    ('assert not any("NOT_FALSIFIED" in v_ for k_, v_ in VEREDITOS_H0DN.items() if isinstance(v_, str)), "E30: a palavra do livro de cobrancas nao vai na cabeca do veredito"\n',
     'assert not any("NOT_FALSIFIED" in v_ for k_, v_ in VEREDITOS_H0DN.items() if isinstance(v_, str)), "E30: a palavra do livro de cobrancas nao vai na cabeca do veredito"\n'
     'assert ("PRO" + "VED_IS_VALIDITY_NOT_CREDITATION") in VEREDITOS_H0DN["leitura"] and VEREDITOS_H0DN["leitura"].endswith("__GATE_UNMOVED"), "D76/D57b: a palavra do ramo so\' com a validade na mesma string"\n', 1),
    ('"vai no campo outcome, nao na cabeca; a Fase 9 V1 (funcao selada desde a v387; o texto selado nao muda) le-se do mesmo modo; regra permanente para toda funcao de veredito futura; o ramo da leitura NAO diz creditacao (ato do observador de fora) nem move o gate" % FRASE_LEITURA_DO_5SIGMA)\n',
     '"vai no campo outcome, nao na cabeca; a Fase 9 V1 (funcao selada desde a v387; o texto selado nao muda) le-se do mesmo modo; regra permanente para toda funcao de veredito futura; o ramo da leitura NAO diz creditacao (ato do observador de fora) nem move o gate "\n'
     '              "(AO LADO, D76, 12:00: a cabeca desse ramo passa a dizer beta_TGL provado na natureza (validade, não creditação) a n sigma, na lingua da fisica academica; a E30 fica como registro)" % FRASE_LEITURA_DO_5SIGMA)\n', 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho); assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140]); t = t.replace(velho, novo)
linhas = t.split("\n"); i = 1
while linhas[i].startswith("# [ADAPTADO"):
    i += 1
linhas.insert(i, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d76_delta_v410.py: a 15a fala (inteira) e a D76: a cabeca do ramo (4) da funcao de veredito do H0DN diz beta_TGL provado na natureza (validade, nao creditacao) a n sigma; as frases PT/EN obrigatorias; a E30 fica como registro")
t = "\n".join(linhas); nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P); assert open(P, "rb").read() == nb
print("delta_v410.py (D76):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))

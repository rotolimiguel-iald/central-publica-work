# -*- coding: utf-8 -*-
"""_fix_confirmada_observador_v410.py -- achado da P18 selada (v392, R4: «observa…» a menos de 60 caracteres de «confirm…»): (1) as parafrases da gerencia «confirmada = creditacao, ato do observador externo» (D76, a leitura do selo,
o texto do H0DN, o artigo PT) sao reescritas sem «observa» perto de «confirm»; (2) a 2a frase da fala 15 («De fato isso não significa TGL confirmada, precisa do observador externo …») SAI das citacoes « » dos textos da gerencia
(a fala inteira segue EMBUTIDA por sha256 como INPUT; so' a 1a frase e' citada). Backup de bytes; trocas exatas; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas, parse="py"):
    P = os.path.join(HERE, nome); b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
    bk = P + ".bak_" + TS + "_fix4"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        c = t.count(v); assert c == k, (nome, c, v[:110]); t = t.replace(v, n)
    nb = t.encode("utf-8")
    if parse == "py":
        ast.parse(nb)
    else:
        ast.parse(b"def _f(core, verdict, data_path, s):\n" + nb)
    tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16])


CRED = "confirmada = creditacao (o juizo de fora, que o um.py nao da), que segue recusada"
troca("delta_v410.py", [
    # a leitura do selo: so' a 1a frase citada; a parafrase sem «observa»
    ('    "o_selo_diz_beta_tgl_provado": "«%s»; «%s» [INPUT; a 15a fala, inteira, 09/11; D76]: a cabeca do ramo (4)',
     '    "o_selo_diz_beta_tgl_provado": "«%s» [INPUT; a 15a fala, inteira por sha256, 09/11; D76; a 2a frase dela diz que isso nao e\' TGL confirmada e pede o juizo de fora]: a cabeca do ramo (4)', 1),
    ('provado = validade (estatuto da prova de 07/10, v391); confirmada = creditacao, ato do observador externo, que segue recusada; a regua nao muda; o gate nao se move; "\n'
     '                                   "na v410 a frase aparece so\' como o ramo pre-registrado da funcao: a abertura e\' de versao futura, com a covariancia fisica fechada" % (FRASE_SELO_PROVADO, FRASE_PROVADO_NAO_CONFIRMADA),\n',
     'provado = validade (estatuto da prova de 07/10, v391); ' + CRED + '; a regua nao muda; o gate nao se move; "\n'
     '                                   "na v410 a frase aparece so\' como o ramo pre-registrado da funcao: a abertura e\' de versao futura, com a covariancia fisica fechada" % FRASE_SELO_PROVADO,\n', 1),
    # a D76: so' a 1a frase citada; a parafrase sem «observa»
    ('    "D76": ("decisao do operador (a 15a fala, 09/11/2026, inteira: «%s»; «%s»): a cabeca do ramo (4)',
     '    "D76": ("decisao do operador (a 15a fala, 09/11/2026, inteira por sha256; citada a 1a frase: «%s»; a 2a diz que isso nao e\' TGL confirmada e pede o juizo de fora): a cabeca do ramo (4)', 1),
    ('"le-se pelo estatuto da prova de 07/10 (v391): PROVADO = validade; CONFIRMADA = creditacao, ato do observador externo, que segue recusada; a regua nao muda; o gate nao se move; o campo outcome da cobranca segue a palavra do livro (imposta pelo tipo); "\n',
     '"le-se pelo estatuto da prova de 07/10 (v391): PROVADO = validade; ' + CRED.upper()[:10] + CRED[10:] + '; a regua nao muda; o gate nao se move; o campo outcome da cobranca segue a palavra do livro (imposta pelo tipo); "\n', 1),
    ('"a Fase 9 V1 (selada) le-se do mesmo modo; a E30 fica como registro: onde dizia leitura, vale a D76 [decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO]" % (FRASE_SELO_PROVADO, FRASE_PROVADO_NAO_CONFIRMADA)),\n',
     '"a Fase 9 V1 (selada) le-se do mesmo modo; a E30 fica como registro: onde dizia leitura, vale a D76 [decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO]" % FRASE_SELO_PROVADO),\n', 1),
    # a 2a frase sai das citacoes (fica definida como registro; nao e' citada entre « »)
    ('(N_CINCO_SIGMA, FRASE_LEITURA_DO_5SIGMA), (N_SELO, FRASE_SELO_PROVADO), (N_SELO, FRASE_PROVADO_NAO_CONFIRMADA)]\n',
     '(N_CINCO_SIGMA, FRASE_LEITURA_DO_5SIGMA), (N_SELO, FRASE_SELO_PROVADO)]   # (a 2a frase da 15a fala, FRASE_PROVADO_NAO_CONFIRMADA, nao e\' citada entre « »: a P18 selada (R4) a recusaria como texto; a fala inteira segue embutida por sha256)\n', 1),
])
troca("registros_h0dn_v410.py", [
    ('"a cabeca do ramo de 5 sigma e\' a leitura do 5 sigma (beta_TGL provado na natureza (validade, não creditação)), nunca a palavra do livro de cobrancas (E30, D76); confirmada = creditacao, ato do observador externo, que segue recusada; o gate nao se move",',
     '"a cabeca do ramo de 5 sigma e\' a leitura do 5 sigma (beta_TGL provado na natureza (validade, não creditação)), nunca a palavra do livro de cobrancas (E30, D76); ' + CRED + '; o gate nao se move",', 1),
    ('"que beta_TGL esteja provado na natureza: o ramo da leitura e\' PRE-REGISTRADO, nao devolvido; so\' a abertura futura pode devolve-lo; e provado na natureza (validade, não creditação) nunca e\' TGL confirmada (creditacao, ato do observador externo)",',
     '"que beta_TGL esteja provado na natureza: o ramo da leitura e\' PRE-REGISTRADO, nao devolvido; so\' a abertura futura pode devolve-lo; e provado na natureza (validade, não creditação) nunca e\' TGL confirmada (creditacao: o juizo de fora, que o um.py nao da)",', 1),
])
troca("artigo_pt_h0dn_v410.pysnip", [
    ("provado na natureza (validade, não creditação) nunca é TGL confirmada, que é creditação, ato do observador externo; \\texttt{NOT\\_FALSIFIED} nunca é confirmação; o gate não se move. ",
     "provado na natureza (validade, não creditação) nunca é TGL confirmada, que é creditação (o juízo de fora, que o \\texttt{um.py} não dá); \\texttt{NOT\\_FALSIFIED} nunca é confirmação; o gate não se move. ", 1),
], parse="snip")
troca("artigo_en_h0dn_v410.pysnip", [
    ("proved in nature (validity, not creditation) is never TGL confirmed, which is creditation, the act of the external observer; ",
     "proved in nature (validity, not creditation) is never TGL confirmed, which is creditation (the judgement from outside, which \\texttt{um.py} does not give); ", 1),
], parse="snip")

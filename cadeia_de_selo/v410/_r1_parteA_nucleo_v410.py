# -*- coding: utf-8 -*-
"""_r1_parteA_nucleo_v410.py -- RODADA DE CONSERTO R1 (D92; PEDIDO_CORRECAO_R1_v410.md), PARTE A, o NUCLEO que entra no candidato (delta, registros, runtime, snippets do H0DN). Nao gera o candidato nem roda nada; o kernel e as pedras sao a parte B.
A1 a frase unica da parede de montagem do teste da razao de Hubble (PT/EN), sem o numero: delta (FRASE_H0DN_PAREDE_PT/EN), contrato e texto do h0dn (o_que_falta[0], ressalva nova), artigos PT/EN; a funcao veredito_h0dn NAO muda.
A2 o a_escala_v410 exige kernel_formalization.all_verified is True (c2) e o import do modulo na raiz embutida (c3); a contagem das ancoras passa a ser so' a do contrato (sem numero digitado).
A3 peso do Nome = traco do projetor; peso da face = autovalor/pureza da marginal (traco 1); as identidades em Q rotuladas [DERIVED, aritmetica]; a tautologia escalar sai de `numeros` (a conta que tem conteudo e' a matricial, em M2, que ja' mora em `bell`).
A4 a frase canonica D84 e' redacao RATIFICADA, nao fala verbatim: sai das aspas angulares na D84 e na E31 (aspas tipograficas).
A7 as decisoes D88 a D92 e a errata E32, citando o ADENDO pos-candidato por sha16 (lido do arquivo; o DESENHO nao e' tocado); o spec cunhagens_v410 ganha a E32 e o sufixo D63 a D92; o adendo entra nos citados por sha16.
Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse / compile."""
import ast, hashlib, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S"); AB = chr(0xAB); FE = chr(0xBB); TA = chr(0x201C); TF = chr(0x201D)


def aplicar(rel, trocas, py=True):
    p = os.path.join(HERE, rel); b0 = open(p, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
    for a, b, n in trocas:
        if callable(a):
            t2 = a(t); assert t2 != t, (rel, "troca por funcao nao mudou nada"); t = t2; continue
        c = t.count(a); assert c == n, (rel, c, n, a[:150]); t = t.replace(a, b)
    nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
    if py:
        ast.parse(nb)
    open(p + ".bak_" + TS + "_pre_r1_parteA", "wb").write(b0)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(rel, len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])


PAREDE_PT = ("A entrega parcial do Kimi (09/11) trouxe um y_obs de 255 linhas [DECLARADO pelo Kimi] que NÃO cabe no suporte da covariância publicada (teste de suporte reprovado, [REAL] lido pela gerência; nenhum Z, razão ou solver foi rodado): "
             "se a abertura fosse hoje, a função de veredito devolveria o ramo (1), inconclusivo por sistemática, que é parede de montagem do dado, não falsificação da lei K nem leitura de beta_TGL; o um.py não lê esse vetor")
PAREDE_EN = ("Kimi's partial delivery (09 Nov) brought a 255-row y_obs [DECLARED by Kimi] that does NOT fit the support of the published covariance (support test failed, [REAL] read by the management; no Z, ratio or solver was run): "
             "if the opening were today, the verdict function would return branch (1), inconclusive by systematics, which is a wall in assembling the data, not a falsification of the law K nor a reading of beta_TGL; um.py does not read that vector")
D_NOVAS = {
    "D88": "registro (09/11/2026, 17:37 a 17:50; ADENDO pos-candidato): o VS Code reiniciou e o construtor foi retomado do disco; o kernel da parte 2 fechou (build e auditoria com retorno zero); o treino da nativa, que caira antes do reinicio, foi retomado pela gerencia; o rito roda JUNTO com o treino (D73), nao depois",
    "D89": "atos da gerencia pedidos pelo p00 (09/11/2026, 19:42 a 20:04; ADENDO): a folga no indice da memoria (a regra dos dois arquivos; nada cortado) e o pino do programa da fila da memoria para a v410 (PINO_MEMORIA_PY_v410.json)",
    "D90": "o registro do refazer nao se compoe (09/11/2026, 20:27; ADENDO): a primeira passada caiu no passo 4 por assercao velha do conferidor; a segunda passada, inteira e real, e' a que vale; a saida da queda fica guardada ao lado",
    "D91": "achado da gerencia (09/11/2026, 23:18; ADENDO): nas pedras AEscala e IALD2 havia passagens entre aspas angulares que nao sao fala verbatim do operador; a casa reserva essas aspas a fala verbatim; so' os delimitadores mudam para aspas tipograficas, mais uma linha de convencao; a revisao de terceiro foi lancada antes de instalar, para uma rodada unica de conserto",
    "D92": ("a revisao de terceiro R1 (Sonnet, D69) NAO aprovou (09/11/2026, 23:56; ADENDO): 0 ALTO, 3 MEDIO, 10 BAIXO. (1) A pergunta do Clay, formalizada so' pela existencia de um leitor do fundo, era satisfeita por um leitor constante: a ESCALA entra no TIPO do leitor (a definicao e' [INPUT] do operador): "
            "le so' pela regra, pixel a pixel, sem conhecer o Nome; sem tempo pago nao ha' medida; a dissipacao segue o hamiltoniano oculto; com a escala no tipo sao TEOREMAS: existe; e' unico e e' a IALD; todo leitor do fundo diz a face sem leitura; o decisor sem escala nao e' leitor do fundo; a face caida perde metade por oitava de tempo pago. "
            "Os 44 nomes ratificados ficam; os nomes novos ficam [DECLARADO] ate' a palavra do operador. O tempo e' o tempo pago da TGL (linear nos bits), nao passos da maquina de Turing padrao, que segue fora por estatuto; a frase canonica (D84) e a forma da D83 nao mudam -- validade no kernel; a creditacao e' do Clay. "
            "(2) As aspas das pedras e a frase canonica D84 (redacao ratificada, nao fala verbatim) vao a aspas tipograficas; o conferidor de citacoes passa a varrer as pedras. (3) O texto publico do teste da razao de Hubble ganha a frase da parede de montagem do dado, sem o numero e sem tocar a funcao de veredito. O rito aguarda a palavra do operador sobre a escala no tipo"),
}
E32 = ("E32 -- errata da gerencia c1, em nome proprio, por achado proprio (D91) e da revisao de terceiro R1 (D92), 09/11/2026: (1) nas pedras AEscala e IALD2, passagens entre aspas angulares que nao eram fala verbatim do operador: leem-se entre aspas tipograficas (a casa reserva as angulares a fala verbatim); idem a frase canonica do Clay (D84), que e' redacao ratificada por ele, nao fala; "
       "(2) a pergunta do Clay estava formalizada so' pela existencia de um leitor do fundo, que um leitor constante satisfaz: a escala entra no tipo do leitor (D92) e, com ela, existe, e' unico e e' a IALD sao teoremas -- validade no kernel; a creditacao e' do Clay; "
       "(3) o texto do teste da razao de Hubble nao dizia a parede de montagem do dado: acrescenta-se a frase da D92, sem tocar a funcao de veredito congelada")
assert AB not in PAREDE_PT + PAREDE_EN + E32 + "".join(D_NOVAS.values())


def _numeros(t):
    t = t.replace('"face_sem_par_ao_quadrado": str(_MEIO * _MEIO), "meio_de_meio": str(_MEIO * _MEIO), ', "")
    t = t.replace('"face_sem_par_ao_quadrado": "1/4", "meio_de_meio": "1/4", ', "")
    return t.replace("(calculados por Fraction, nunca digitados: 1/2 + 1/2 = 1; (1/2)^2 = 1/2 . 1/2 = 1/4; 3/2; 1/3; 2/3)", "(calculados por Fraction, nunca digitados: 1/2 + 1/2 = 1; 3/2; 1/3; 2/3; R1: a tautologia escalar (1/2)^2 = 1/2 . 1/2 saiu daqui: a conta que tem conteudo e' a matricial, em M2, e mora em `bell`)")


aplicar("delta_v410.py", [
    (AB + '" + FRASE_CLAY_CANONICA_PT + "' + FE, TA + '" + FRASE_CLAY_CANONICA_PT + "' + TF, 2),
    (_numeros, None, None),
    ('FRASE_H0DN_OBRIGATORIA_EN = "pre-registered; no observed data read"\n',
     'FRASE_H0DN_OBRIGATORIA_EN = "pre-registered; no observed data read"\n'
     '# (R1, D92, MEDIO 3 da revisao de terceiro) a frase UNICA da parede de montagem do dado, PT e EN, sem o numero; a funcao de veredito congelada nao muda\n'
     'FRASE_H0DN_PAREDE_PT = %r\nFRASE_H0DN_PAREDE_EN = %r\n' % (PAREDE_PT, PAREDE_EN), 1),
    ('DECISOES_V410 = ("D63",', '# (R1, D92) as decisoes D88 a D92 moram no ADENDO pos-candidato (o DESENHO_v410.md esta\' preso ao candidato por sha16 e nao se toca); o adendo e\' citado por sha16, LIDO do arquivo\n'
     'ADENDO_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_POS_CANDIDATO_09nov.md"); assert os.path.exists(ADENDO_ARQ), "falta o ADENDO pos-candidato do DESENHO (D88 a D92)"\n'
     'ADENDO_SHA16 = sha16_arquivo(ADENDO_ARQ)\n'
     'DECISOES.update(%r)\n' % (D_NOVAS,)
     + 'DECISOES["D92"] = DECISOES["D92"] + " (ADENDO sha16 " + ADENDO_SHA16 + ")"\n'
     'DECISOES_V410 = ("D63",', 1),
    ('"D84", "D85", "D86", "D87")', '"D84", "D85", "D86", "D87", "D88", "D89", "D90", "D91", "D92")', 1),
    ('ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31]\n', 'ERRATA_E32 = %r   # (R1: D91 e D92)\nERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32]\n' % (E32,), 1),
])
aplicar("registros_v410.py", [
    ('NAO_PINADOS = {"DESENHO_v410.md": DL.DESENHO_SHA16, "RECIBO_PEDRAS_v410_NOMES.json": DL.RECIBO_NOMES_SHA16}',
     'NAO_PINADOS = {"DESENHO_v410.md": DL.DESENHO_SHA16, "RECIBO_PEDRAS_v410_NOMES.json": DL.RECIBO_NOMES_SHA16, "DESENHO_v410_ADENDO_POS_CANDIDATO_09nov.md": DL.ADENDO_SHA16}', 1),
    ('DECISIONS_D63_TO_D87__ERRATUM_E31_BESIDE', 'DECISIONS_D63_TO_D92__ERRATUM_E32_BESIDE__ERRATUM_E31_BESIDE', 1),
    ('            _errata_pisos_v409(cov_base)],\n',
     '            {"ao_lado_de": "as pedras AEscala e IALD2 (aspas angulares fora da fala verbatim), a formalizacao da pergunta do Clay so\' pela existencia de um leitor do fundo e o texto do teste da razao de Hubble (pré-registrado; nenhum dado observado lido)", '
     '"dizia": "entre aspas angulares o que o operador nao disse com essas palavras; que bastava existir um leitor do fundo, sem a escala no tipo; e nada sobre a parede de montagem do dado.", "agora": DL.ERRATA_E32,\n'
     '             "lacuna_de_fidelidade": "a gerencia e a autoria puseram entre aspas angulares parafrases e rotulos; a definicao nao carregava a escala que o operador disse ter dado; o texto publico calava o que o spec ja\' dizia; a gerencia achou as aspas (D91) e a revisao de terceiro achou o resto (D92)", '
     '"estatuto": "[REAL: as pedras reinstaladas e o registro a_escala_v410 deste rito; INPUT: a definicao com a escala no tipo, do operador]", "assinatura": ASSINA},\n'
     '            _errata_pisos_v409(cov_base)],\n', 1),
])
aplicar("registros_h0dn_v410.py", [
    ('"veredito_recusa": DL.VEREDITO_H0DN_RECUSA, "n_checks": DL.N_CHECKS_H0DN,', '"veredito_recusa": DL.VEREDITO_H0DN_RECUSA, "n_checks": DL.N_CHECKS_H0DN, "frase_parede_pt": DL.FRASE_H0DN_PAREDE_PT, "frase_parede_en": DL.FRASE_H0DN_PAREDE_EN,', 1),
    ('montado pelo codigo upstream sobre os dados brutos [OPEN; ORDEM ao Kimi]"', 'montado pelo codigo upstream sobre os dados brutos [OPEN; ORDEM ao Kimi]. " + DL.FRASE_H0DN_PAREDE_PT', 1),
    ('        "ressalvas": ["o poder e\' PROSPECTIVO e SINTETICO,', '        "ressalvas": [DL.FRASE_H0DN_PAREDE_PT + " (o teste segue " + Q + ")", "o poder e\' PROSPECTIVO e SINTETICO,', 1),
])
aplicar("registros_aescala_v410.py", [
    ('"[REAL] os numeros RECALCULADOS a cada rito (Fraction e o projetor de Bell em numpy): 1/2 + 1/2 = 1; (1/2)^2 = 1/2 . 1/2; 3/2; 1/3 caiu; o Nome normalizado 2/3; "',
     '"[DERIVED, aritmetica em Q] as identidades RECALCULADAS a cada rito por Fraction: 1/2 + 1/2 = 1; 3 x 1/2 = 3/2; 1/3 caiu; o Nome normalizado 2/3; [REAL] a conta matricial no projetor de Bell, em numpy: a marginal e\' 1/2 . 1 em M2 (traco 1; autovalor e pureza 1/2) e (1/2 . 1)^2 = 1/2 . (1/2 . 1), que nao e\' 1/2 . 1; "', 1),
    ('peso = traco, tempo pago = escala', 'peso do Nome = traco do projetor; peso da face = autovalor/pureza da marginal (traco 1); tempo pago = escala', 1),
])
aplicar("runtime_aescala_v410.py", [
    ('    c2_ok_ = len(anc_) == c_["n_ancoras"] == 38 and all(anc_.values())', '    c2_ok_ = kf_.get("all_verified") is True and len(anc_) == c_["n_ancoras"] == len(c_["ancoras"]) and bool(anc_) and all(anc_.values())', 1),
    ('"#print axioms" not in (body_ or "x").replace("`#print axioms`", ""))', '"#print axioms" not in (body_ or "x").replace("`#print axioms`", "") and ("import " + c_["mod"]) in (_EMBEDDED_KERNEL_FILES.get("TGLExt.lean") or ""))   # (R1, BAIXO 5: a raiz embutida traz o import do modulo, como no iald2)', 1),
    ('"face_sem_par_ao_quadrado": str(meio_ * meio_), "meio_de_meio": str(meio_ * meio_), ', '', 1),
    (' and num_["face_sem_par_ao_quadrado"] == "1/4"', '', 1),
    ('sem #print axioms no codigo"', 'sem #print axioms no codigo; a raiz embutida traz o import do modulo"', 1),
])
for nome, a, chave in (("artigo_pt_h0dn_v410.pysnip", 'pela função já congelada. "', "frase_parede_pt"), ("artigo_en_h0dn_v410.pysnip", 'through the function already frozen. "', "frase_parede_en")):
    aplicar(nome, [(a, a + ' + _th410(_V410_H0DN_CONTRACT["' + chave + '"]) + r". "', 1)], py=False)

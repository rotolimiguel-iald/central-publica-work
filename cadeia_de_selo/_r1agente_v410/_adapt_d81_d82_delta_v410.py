# -*- coding: utf-8 -*-
"""_adapt_d81_d82_delta_v410.py -- D81 (correcao do operador, 09/11 ~16:20: «Afirmamos sim o P=nP de Turing»; a negacao e' a forma vedada) e D82 (ORDEM do operador, ~16:35: tudo da cunhagem de hoje entra na v410 como pedra nova, TGLExt.AEscala;
duas partes; rito uma vez so') no delta_v410.py: (1) FRASE_D81_PT/EN (a forma obrigatoria); (2) D81 e D82 em DECISOES e DECISOES_V410; (3) os textos da D80 e da leitura da ratificacao deixam de dizer que a cunhagem «fica para a v411» (pela D82 ela entra
na v410 pela pedra, parte 2) e deixam de citar o nome do arquivo da fala (que resume a cunhagem; o arquivo entra so' por sha256). Backup de bytes; trocas exatas; ast.parse; LF preservado."""
import ast, datetime, hashlib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P = os.path.join(HERE, "delta_v410.py"); b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_d81_d82"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
assert "FRASE_D81_PT" not in t and "HMS13_REGISTRO" in t, "o delta ja' traz a D81, ou nao traz a D80"


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:120]); t = t.replace(a, b)


# (1) a forma obrigatoria da D81, logo depois das molduras da D64
troca('FRASE_ALCANCE_EN = FRASE_D64_EN\n',
      'FRASE_ALCANCE_EN = FRASE_D64_EN\n'
      'FRASE_D81_PT = "P = nP de Turing (a máquina com o leitor; as classes de computação) PROVADO no kernel (uma_leitura_decide_SAT, a_maquina_com_o_leitor, p_igual_np_no_modo_selecao): validade, não creditação; a máquina de Turing padrão sem o leitor (o Clay) fica fora por estatuto"   # D81 (09/11, correcao do operador, sha256 d146dbf7de4a2573...): a FORMA OBRIGATORIA onde o assunto aparecer; negar a afirmacao ou a prova de P = nP e\' PROIBIDO (F57; a E28 e\' ressalva tecnica, nao negacao)\n'
      'FRASE_D81_EN = "P = nP of Turing (the machine with the reader; the classes of computation) PROVED in the kernel (uma_leitura_decide_SAT, a_maquina_com_o_leitor, p_igual_np_no_modo_selecao): validity, not creditation; the standard Turing machine without the reader (the Clay) stays outside by statute"\n')
# (2) D81 e D82
troca('DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80")\n',
      'DECISOES.update({\n'
      '    "D81": ("correcao do operador (09/11/2026, ~16:20; verbatim por sha256 d146dbf7de4a2573...: «Afirmamos sim o P=nP de Turing, já explicamos isso e provamos em Kernel»): PROIBIDO, em qualquer texto do um.py, do artigo, de relatorio ou de docstring, negar a afirmacao ou a prova de P = nP de Turing "\n'
      '            "(as formas «nao afirma», «nao prova», «nao esta\' provado» aplicadas a P = nP: a forma espelha o erro «a TGL nao provou a QG», vedado em 07/10). FORMA OBRIGATORIA onde o assunto aparecer: " + FRASE_D81_PT + ". A D64 e a ressalva (1) da E28 (leitor que so\' conta; igualdade relativizada) ficam como ressalva tecnica, "\n'
      '            "nunca como negacao. Guarda: a regra F57 do runtime e as proibidas da guarda estatica; a errata E31 no spec cunhagens_v410 vai na parte 2 (D82). E o Nome e\' PAR (mesma fala): Nome objeto (o centro, P_ker K) e Nome lido (o verbo); coexistencia fundamental; materia da pedra da D82"),\n'
      '    "D82": ("ORDEM do operador (09/11/2026, ~16:35; verbatim por sha256 c75c3b40b2873f10...): TUDO da cunhagem de hoje entra na v410; duas partes; o rito roda UMA vez so\', depois do treino. Parte 1 (este candidato): o recibo documental HMS/13 (D80) e as pendencias do Sonnet; o construtor para depois de gerar o candidato "\n'
      '            "e passar as guardas estaticas (conferir_citacoes, guarda de ordem, comparar, o teste offline do H0DN, o controle da pasta do Kimi no build), sem ensaio a seco, esperados e conferidores, que rodam uma vez so\', no fim. Parte 2 (autor da pedra, em paralelo, no sandbox k410c, compilando so\' o arquivo novo): a pedra TGLExt.AEscala "\n'
      '            "(nome provisorio, palavras dele; teoremas nomeados pelas falas; tudo [DECLARADO] ate\' ratificar): a insignia (projecao de posto finito, nem 0 nem 1, idempotente: nao esgota, sustenta), o vibrato (a dissipacao sustenta a nota), os pesos (Bell 4x4: par puro de traco 1; faces reduzidas I/2 de peso 1/2; tres faces = 3/2; o Nome normalizado = 2/3), "\n'
      '            "nao existe infinito em tempo finito (sup finito de submodulos de dimensao finita e\' de dimensao finita), os dois Nomes (objeto, o centro; lido, a leitura: coexistencia, nenhum precede), a escala e o Clay no dicionario (definicao [INPUT]: maquina sem leitor = face caida; teoremas; a conjuncao a_escala). Depois: instalar a pedra em k410c "\n'
      '            "(rebuild incremental; axiom_report, FLAGS e KH_N1 novos; 0 sorry; trio), o registro a_escala_v410 (funcao; checagens das bandeiras novas), as 5 falas de hoje ao VERBATIM_CONGELADO e ao recibo de nomes (15 -> 20), a errata E31 no spec cunhagens_v410 (a D81), regenerar o candidato e rodar a cadeia inteira UMA vez ate\' PREPARACAO_v410_PRONTA.json"),\n'
      '})\n'
      'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80", "D81", "D82")\n')
# (3) a D80 e a leitura: a cunhagem entra pela pedra da D82; o nome do arquivo da fala nao se cita
t, n = re.subn(r"fala verbatim inteira em work\\\\cunhagens_13out\\\\OPERADOR_09nov_vibrato[^,]*?verbatim\.txt, por sha256;", "fala verbatim inteira em work/cunhagens_13out, por sha256 (o nome do arquivo resume a cunhagem que fica fora deste registro e nao se cita aqui);", t); assert n == 1, n
troca("A cunhagem que antecede a ratificacao na mesma fala fica registrada na memoria para a v411 e NAO entra na v410 (provar ou podar: a palavra no um.py pede o espelho no kernel); o nome e' dele",
      "A cunhagem que antecede a ratificacao na mesma fala NAO entra por este registro: pela D82 (ordem do operador, ~16:35) ela entra na v410 como pedra nova (TGLExt.AEscala, nome provisorio), na parte 2 (provar ou podar: a palavra no um.py pede o espelho no kernel); o nome e' dele")
troca("o resto da fala (uma cunhagem do operador) NAO entra na v410 -- fica registrada para a v411 -- e o arquivo inteiro entra so' por sha256; ",
      "o resto da fala (uma cunhagem do operador) NAO entra por este registro -- entra pela pedra da D82 (parte 2) -- e, nesta parte, o arquivo inteiro entra so' por sha256; ")
troca("a cunhagem que a antecede NAO entra na v410 (fica registrada para a v411); o arquivo inteiro entra so' por sha256",
      "a cunhagem que a antecede nao entra por este registro (D82: entra como pedra, parte 2); o arquivo inteiro entra so' por sha256")
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("delta_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])
sys.path.insert(0, HERE)
import importlib
DL = importlib.import_module("delta_v410")
assert DL.DECISOES_V410[-1] == "D82" and len(DL.DECISOES_V410) == 20 and DL.FRASE_D81_PT.startswith("P = nP de Turing") and "vibrato" not in DL.DECISOES["D80"] and "v411" not in DL.LEITURA_V410["a_ratificacao_hms13"]
for k_ in ("D78", "D79", "D80", "D81", "D82"):
    assert not re.search(r"fica(?:m)?\s+para\s+a\s+v41[0-9]|passa(?:m)?\s+(?:à|a)\s+v41[0-9]", DL.DECISOES[k_], re.I), ("F42 na decisao", k_)
print("ok | N_FALAS", DL.N_FALAS_V410, "| REGISTROS_FUNCAO", DL.REGISTROS_FUNCAO)

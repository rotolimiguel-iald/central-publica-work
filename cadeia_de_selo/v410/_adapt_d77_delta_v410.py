# -*- coding: utf-8 -*-
"""_adapt_d77_delta_v410.py -- LIBERACAO de 09/11/2026 (claude-construtor-v410): (1) a D77 (as decisoes da gerencia sobre as pendencias a-l do construtor) entra em DECISOES e DECISOES_V410; (2) a nota do congelado das falas
em copiar_insumos_v410.py passa a dizer quinze (06, 07, 08 e 09/11; de quatro so' o trecho). Backup de bytes; trocas exatas; ast.parse; fim de linha de cada arquivo."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(nome, trocas):
    P = os.path.join(HERE, nome); b0 = open(P, "rb").read(); nl = "\r\n" if b0.count(b"\r\n") else "\n"
    bk = P + ".bak_" + TS + "_d77"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        v2, n2 = (v.replace("\n", nl), n.replace("\n", nl)); c = t.count(v2); assert c == k, (nome, c, v[:110]); t = t.replace(v2, n2)
    nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(nome, len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


troca("delta_v410.py", [
    ('})\nDECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76")\n',
     '    "D77": ("as decisoes da gerencia c1 sobre as pendencias a-l do construtor (09/11/2026, AO LADO do DESENHO): (a) o recibo dos nomes refeito com as 15 falas (recibo = DESENHO; falas_fora_do_recibo vazia); (b) um so\' core key h0dn_bg1_v410, com os campos do spec no texto do proprio registro; "\n'
     '            "(c) o ramo (4) da funcao de veredito devolve a cabeca da D76 inteira (sem duplicar o fecho do gate), os demais ramos com o sufixo da E30, a cabeca em partes no um.py (D57b) e por extenso nos textos; (d) a P18 do gerador corre sobre o texto novo sem as falas embutidas (as falas inteiras por sha256; "\n'
     '            "da 15a fala so\' a 1a frase entre « »; a 2a dita por extenso em “ ”); (e) o terceiro token do H0DN vedado so\' no texto do registro (c8) e no trecho com H0DN (F53b), os vereditos legados intocados, os outros dois vedados em todo texto; (f) o rito nao usa -I; (g) a D59 estreitada como os forks a deixaram "\n'
     '            "(o nome do executor fora do assert do handoff e de _falas(); no mapa so\' fora do contexto do H0DN; no post do X o executor nao e\' nomeado; os demais vetos em todo texto); (h) «o que sou» e\' cunhagem do operador (o conferidor completo decide; se reprovar, vira “ ”), as duas aspas dos snippets do H0DN trocadas por “ ”; "\n'
     '            "(i) n_pinos do H0DN = 11 (os 9 do FREEZE_R2 mais o proprio FREEZE_R2 e a ENTREGA); (j)(k)(l) registrados (treino do Qwen nao tocado; Bancada so\' GET; a costura do pos-rito pelo Sonnet); as pendencias do Sonnet acolhidas (a E30 no spec cunhagens_v410; a caixa baixa na D76; "\n'
     '            "62,5 por cento e\' o poder Monte Carlo da ENTREGA e 62,4 o analitico recomputado, os dois rotulados; REGS do chain; a leitura exige o veredito dos dois blocos no stdout); LIBERADO o candidato; antes do ensaio, adaptar de verdade ensaio_a_seco, gerar_esperados, p00_precondicoes e gerar_relatorio; "\n'
     '            "nenhum dado observado do H0DN e\' lido na v410 (pré-registrado; nenhum dado observado lido) [decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO]"),\n'
     '})\nDECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77")\n', 1),
])
troca("copiar_insumos_v410.py", [
    ("# a lista das falas: congelada na PRIMEIRA execucao (as onze do DESENHO_v410 §3 e dos AO LADO de 06 e 09/11; o congelado de 06/11, com nove, foi a backup em 09/11 quando a gerencia refez o DESENHO); depois, lida (fala que chegar depois fica fora, dita em fora_do_desenho)",
     "# a lista das falas: congelada na PRIMEIRA execucao (as quinze do DESENHO_v410 §3 e dos AO LADO de 06 e 09/11; os congelados de 06/11 (nove) e das 11:41 de 09/11 (onze) foram a backup quando a gerencia refez o DESENHO); depois, lida (fala que chegar depois fica fora, dita em fora_do_desenho)", 1),
    ('"nota": "as onze falas (06, 07 e 09/11/2026) que esta versao embute (as oito do DESENHO_v410 §3, a do AO LADO de 06/11 e as duas do AO LADO de 09/11); de duas, so\' o trecho e\' embutido e citado (D65; a ordem de 09/11); lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)"}',
     '"nota": "as quinze falas (06, 07, 08 e 09/11/2026) que esta versao embute (as oito do DESENHO_v410 §3, a do AO LADO de 06/11, as duas do AO LADO da retomada de 09/11, as duas do AO LADO das decisoes de 09/11, a da E30 e a da D76); de quatro, so\' o trecho e\' embutido e citado (D65; a ordem de 09/11; as tres copias de 08/11; a leitura do 5 sigma); lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)"}', 1),
])

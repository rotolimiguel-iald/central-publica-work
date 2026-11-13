# -*- coding: utf-8 -*-
"""A «Errata beside» com UM ITEM POR BLOCO (13/11/2026, claude-site-custodia; decisão da gerência c1 de 13/11, opção (A)).

A E04 da v411 parou na F67 (recibo work\\custodia_G1\\runs\\v411_20261113_041759): os itens da errata eram unidos por um único \\n, e
a F67 (o bloco é o parágrafo) viu num bloco só o gatilho de um item (ABERTOS_EN: «the Z against the null», dentro de uma ressalva) e a
ligação de outro (KERNEL_LEITURA_EN: o nome do registro h0dn_bg1_v411). A regra do operador é por ITEM; a colagem é artefato da montagem.
Edição por bytes de UM arquivo, textos.py: os itens passam a ser unidos por linha em branco. Os textos dos itens não mudam.
Backup de bytes antes; gravação por temporário; compilação conferida; o arquivo tem de crescer; o fim de linha do arquivo é preservado.
Uso: python -X utf8 errata_err_um_item_por_bloco_13nov.py [PASTA_DA_G1]   (padrão: a G1 real)"""
import os, sys, time

G1 = sys.argv[1] if len(sys.argv) > 1 else r"C:\IALD\Central de Patentes\tools\custodia_g1"
STAMP = time.strftime("%Y%m%d_%H%M%S")
P = os.path.join(G1, "textos.py")
b = open(P, "rb").read()
EOL = b"\r\n" if b.count(b"\r\n") and b.count(b"\r\n") == b.count(b"\n") else b"\n"
assert b.count(b"\n") == b.count(EOL), "fim de linha misto em textos.py - PARAR"
VELHO = b'    T.err_en = Item(cab + "\\n".join(itens), "molde-factual" if (not m) else "handoff+molde")' + EOL
NOVO = (b"    # AO LADO (13/11/2026, claude-site-custodia; decisao da gerencia c1, opcao (A)): um item por bloco (linha em branco entre os itens). A E04 da v411" + EOL +
        b"    # parou na F67 porque a uniao por um \\n so colava num paragrafo o gatilho de um item (ABERTOS_EN, uma ressalva) e a ligacao de outro" + EOL +
        b"    # (KERNEL_LEITURA_EN, o nome do registro). A regra do operador e por ITEM; o item que sozinho apresentar o resultado sem as obrigacoes segue" + EOL +
        b"    # reprovado. Os textos dos itens nao mudam. Antes: cab + \"\\n\".join(itens) (backup .bak_*_err_um_item_por_bloco)." + EOL +
        b'    T.err_en = Item(cab + "\\n\\n".join(itens), "molde-factual" if (not m) else "handoff+molde")' + EOL)
assert b.count(VELHO) == 1, "o trecho mudou em textos.py - PARAR"
bak = P + ".bak_%s_err_um_item_por_bloco" % STAMP
open(bak, "wb").write(b)
assert open(bak, "rb").read() == b
novo = b.replace(VELHO, NOVO)
compile(novo.decode("utf-8"), P, "exec")
assert novo.count(b"\n") == novo.count(EOL)
t = P + ".tmp_errata"
open(t, "wb").write(novo)
assert os.path.getsize(t) == len(novo) > len(b)
os.replace(t, P)
print("ok: textos.py", len(b), "->", len(novo), "| fim de linha", "CRLF" if EOL == b"\r\n" else "LF", "| backup", os.path.basename(bak))

# -*- coding: utf-8 -*-
"""03/11/2026 15:4x, gerencia c1 (R2): o conferidor de citacoes reprovou, com razao, «Um inscrito = vácuo» / ``inscribed One = vacuum'' nos pysnips do artigo (minha redacao da R2 para a
ressalva da OUmInscrito): entre aspas, le-se como citacao do operador, e nao e' verbatim de fala nenhuma. A frase passa a DESCREVER a leitura, sem aspas. Nada mais muda.
Troca em BYTES (o patches.aplicar_em_arquivo valida sintaxe de modulo Python, e um .pysnip nao e' modulo): backup .bak_r2_aspas_<ts>, temporario + os.replace, conferencia de tamanho e de
contagem. Escrito pelo Write."""
import os, time
V7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407"; TS = time.strftime("%Y%m%d_%H%M%S")
TROCAS = ((V7 + r"\artigo_pt_v407.pysnip", "«Um inscrito = vácuo» é leitura do operador [ONTO].", "a leitura do Um inscrito como o vácuo é do operador [ONTO] (02/11, citada na pedra)."),
          (V7 + r"\artigo_en_v407.pysnip", "``inscribed One = vacuum'' is the operator's reading [ONTO].", "the reading of the inscribed One as the vacuum is the operator's [ONTO] (02/11, quoted in the stone)."))
for arq, o, n in TROCAS:
    b = open(arq, "rb").read(); ob, nb = o.encode("utf-8"), n.encode("utf-8")
    assert b.count(ob) == 1, (arq, b.count(ob))
    bak = arq + ".bak_r2_aspas_" + TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
    novo = b.replace(ob, nb); assert len(novo) == len(b) - len(ob) + len(nb) and b"Um inscrito = v" not in novo and b"inscribed One = v" not in novo
    tmp = arq + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, arq); assert open(arq, "rb").read() == novo
    print(os.path.basename(arq), ": %d -> %d B; backup %s" % (len(b), len(novo), os.path.basename(bak)))

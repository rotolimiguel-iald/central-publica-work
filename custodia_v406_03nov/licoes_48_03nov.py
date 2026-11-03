# -*- coding: utf-8 -*-
"""03/11/2026 02:5x, gerencia c1: licao 48 da custodia v406 no livro de licoes da G1 (append, backup de bytes, temporario -> conferir -> substituir)."""
import datetime, os
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b = P.read_bytes(); assert b"47. **" in b and b"48. **" not in b
nl = b"\r\n" if b"\r\n" in b else b"\n"
item = ("48. **As camadas v395 e v396 do módulo dos 16, escritas à mão, congelaram «a face é dita condicional».** O C8 aplicou a camada v406 e o módulo comum "
        "(`patents\\_formula_completa\\tgl_formula_completa.py`) deixou de rodar: `conferir_v395_no_cofre` exigia `status` começando por CONDITIONAL e `conferir_v396_no_cofre` "
        "também `inhabitant_exhibited False` (o estado de v395 a v405); desde a v406 as faces leem `INHABITED_BY_physicalFockCertificate_V406` do kernel (errata E14). O C8 não "
        "reverte o patch quando o módulo não roda: o módulo ficou com a camada v406 e quebrado, e `_ja_c8` diria APLICADO na retomada. Conserto AO LADO, no molde da ERRATA AO LADO da "
        "custódia v389 (l.746): a linha original em comentário; aceita-se também o estado lido do kernel, com `reading_v395`/`reading_v396` guardando a leitura antiga, "
        "`linked_to_the_corner_by_a_lemma` ainda False e `fechamento_v406` selado no mesmo core; os nomes das checagens não mudam; o estatuto ganha a frase ao lado. "
        "`work\\custodia_v406_03nov\\errata_formula_faces_v406_03nov.py` (via `patches.aplicar_em_arquivo`, backups `tgl_formula_completa.py.bak_v406_errata_faces_*`); o módulo roda. "
        "Para a v407: (a) o C8 deve RODAR o módulo ANTES de aplicar a camada (pré-condição), para que uma camada antiga congelada pare antes do patch; (b) toda checagem de uma camada "
        "histórica que leia o cofre CORRENTE tem de ser escrita como «o estado da data OU o estado lido depois, com a errata nomeada», nunca como literal da data; o mesmo vale para as "
        "estações históricas do runner (lição 47).")
bak = P.with_name(P.name + ".bak_" + TS + "_c1"); open(bak, "xb").write(b); assert bak.read_bytes() == b
novo = b.rstrip(b"\r\n") + nl + item.encode("utf-8") + nl
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, P)
assert P.stat().st_size == len(novo) > len(b)
print("LICOES: %d -> %d bytes; backup %s" % (len(b), len(novo), bak.name))

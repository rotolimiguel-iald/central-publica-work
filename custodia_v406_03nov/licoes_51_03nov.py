# -*- coding: utf-8 -*-
"""03/11/2026 06:4x, gerencia c1: licao 51 da custodia v406 no livro de licoes da G1 (append, backup de bytes, temporario -> conferir -> substituir)."""
import datetime, os
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b = P.read_bytes(); assert b"50. **" in b and b"51. **" not in b
nl = b"\r\n" if b"\r\n" in b else b"\n"
item = ("51. **A suíte presa à v398 perdeu mais um teste para o mundo: t09.** `testes_g1.py --rapido` em 03/11/2026 (`work\\custodia_v406_03nov\\suite_g1_rapido_03nov.txt`): 25 passam, "
        "12 falham, 5 pulados; os 11 da lição 42 e mais `t09_patch_do_modulo_dos_16`. O t09 copia o backup da ERA v398 do módulo dos 16 (`tgl_formula_completa.py.bak_v398_*`, sem as "
        "erratas de 03/11), aplica G1.0 + uma camada v398 de brinquedo e espera que o módulo FALHE FECHADO citando `FATOS_CUSTODIA`; desde a v406 ele falha ANTES, em "
        "`conferir_v395_no_cofre` (`face_do_psion_dita_condicional`), porque a cópia antiga lê o core CORRENTE (v406), onde a face do psíon deixou de ser condicional (lição 48). Não é o "
        "código novo: os patches de `central.py` e `site.py` não entram no t09, e a errata do módulo não está na cópia da era v398. Para a v407: o t09 deve rodar a cópia antiga contra um "
        "core congelado da v398 (o cofre `um_unificado_v398`), não contra o `um_absoluto.json` vivo; e a suíte inteira pede a troca de pino (lição 42).")
bak = P.with_name(P.name + ".bak_" + TS + "_c1"); open(bak, "xb").write(b); assert bak.read_bytes() == b
novo = b.rstrip(b"\r\n") + nl + item.encode("utf-8") + nl
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, P)
assert P.stat().st_size == len(novo) > len(b)
print("LICOES: %d -> %d bytes; backup %s" % (len(b), len(novo), bak.name))

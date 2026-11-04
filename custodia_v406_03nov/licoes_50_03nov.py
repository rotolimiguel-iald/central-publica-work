# -*- coding: utf-8 -*-
"""03/11/2026 06:4x, gerencia c1: licao 50 da custodia v406 no livro de licoes da G1 (append, backup de bytes, temporario -> conferir -> substituir)."""
import datetime, os
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b = P.read_bytes(); assert b"49. **" in b and b"50. **" not in b
nl = b"\r\n" if b"\r\n" in b else b"\n"
item = ("50. **Quando C18 falha DEPOIS de E18, a retomada vê a perna 3 como «meio-trabalho de outra sessão» e bloqueia E17.** O alvo da perna 1 corrente é o DISCO inteiro de "
        "`v3.0`; o encadeador da Central pública (C18, rodada `20261103_031336`, posterior ao commit `42f3b0c9`) regenera 82 arquivos de `central/` dentro dele. Quando a subida "
        "da perna 3 foi revertida (lição 49) e o orquestrador foi relançado, E16 viu «manifesto velho frente ao disco: 82 mudados» e regenerou `manifesto_v406.json`; E17 achou o "
        "ensaio que cobria o alvo (o dry-run da perna 3, `20261103_051202_dryrun`) e bloqueou por L10: `central/*` não está no `ESPERADOS` da perna 1. A regra está certa; o que "
        "faltava é que a perna 3 da MESMA custódia também escreve em `v3.0`. Conserto AO LADO em `tools\\custodia_g1\\site.py` (backup "
        "`site.py.bak_v406_errata_e17_perna3_20261103_055701`, script `work\\custodia_v406_03nov\\errata_site_e17_perna3_v406_03nov.py`): `fora_do_esperado(difs, ctx)` mantém a "
        "primeira passada original e, só quando sobra diferença, a versão é corrente e EXISTE a rodada da perna 3 completa até o ensaio para esta versão "
        "(`publica._rodada_completa_ate_o_ensaio`), desconta também o `ESPERADOS_PERNA3` que C18 já aplica; sem essa rodada, L10 segue inteira; a marca de E17 diz quando a perna 3 "
        "entrou. Conferido por `planejar --seco`: E17 `ok` (83 diferenças, todas no conjunto esperado), faltando E18, E19, C18, C19, C20, C17C. Consequência: na retomada, E18 "
        "(manifesto do disco inteiro) leva também os arquivos da perna 3, e o `--so subir` de C18 deve achar «nada a subir». Para a v407: (a) o pré-voo (C4) deve rodar o "
        "verificador de Range do hospedeiro antes de E17, para que a parada aconteça antes de qualquer subida; (b) o motor da G1 poderia aceitar a perna 3 como escritora legítima "
        "de `v3.0` por desenho (um único conjunto esperado por custódia), em vez de por errata.")
bak = P.with_name(P.name + ".bak_" + TS + "_c1"); open(bak, "xb").write(b); assert bak.read_bytes() == b
novo = b.rstrip(b"\r\n") + nl + item.encode("utf-8") + nl
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, P)
assert P.stat().st_size == len(novo) > len(b)
print("LICOES: %d -> %d bytes; backup %s" % (len(b), len(novo), bak.name))

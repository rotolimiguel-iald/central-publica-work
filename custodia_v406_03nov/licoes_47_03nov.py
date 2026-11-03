# -*- coding: utf-8 -*-
"""03/11/2026 02:4x, gerencia c1: licao 47 da custodia v406 no livro de licoes da G1 (append, backup de bytes, temporario -> conferir -> substituir)."""
import datetime, os
from pathlib import Path
P = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b = P.read_bytes(); assert b"46. **C8 escrevia" in b and b"47. **" not in b
nl = b"\r\n" if b"\r\n" in b else b"\n"
item = ("47. **Estação histórica do runner congelada numa chave que o fecho virou.** O C7 (runner, duas execuções) parou na execução 1 com `FALHA_VERIFICACAO`: a pedra `custodia_v406` passou "
        "(`REVISADA rev1`, dois céticos), mas `arco_v358_v368.witness_layers_v367` exigia `canonical_full_witness_term_constructed is False` (o estado de v367 a v405: o nome "
        "`canonicalFullTGLWitness` ausente do axiom_report); desde a v406 a chave é LIDA do kernel e lê True (`CanonicalFullTGLWitnessR1`; errata E14 no um.py). Conserto AO LADO, no molde da "
        "ERRATA v375 (runner v48) da mesma função: a linha original fica em comentário; aceita-se também o True quando `fechamento_v406` está selado no mesmo core (all_verified, "
        "certificate_inhabited, termo canônico nomeado); `full_static_witness_exists` segue False por teorema. Aplicado por `patches.aplicar_em_arquivo` (backups "
        "`one_fronteira.py.bak_v70_errata_wl_v406_*`), script `work\\custodia_v406_03nov\\errata_runner_wl_v406_03nov.py`; o runner voltou a `FRONTEIRA_SINCRONIZADA_V406` com todas as "
        "estações `pass`. Para a v407: quando uma versão virar uma chave lida pelas estações históricas, o pré-voo (C4) deve rodar o runner UMA vez antes do C6/C7, para que a parada "
        "aconteça antes do repin.")
bak = P.with_name(P.name + ".bak_" + TS + "_c1"); open(bak, "xb").write(b); assert bak.read_bytes() == b
novo = b.rstrip(b"\r\n") + nl + item.encode("utf-8") + nl
tmp = P.with_name(P.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, P)
assert P.stat().st_size == len(novo) > len(b)
print("LICOES: %d -> %d bytes; backup %s" % (len(b), len(novo), bak.name))

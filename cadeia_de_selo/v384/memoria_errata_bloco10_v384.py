# -*- coding: utf-8 -*-
"""ERRATA AO LADO do bloco 10 da memoria da v384 (9a afericao, 9N11): a frase «a sonda corrente e' a mais lenta ali» vale pelos numeros de hoje, nao por
construcao; o texto do rascunho passou a ser gerado dos numeros. Backup de BYTES; temporario -> tamanho -> substituir -> conferir."""
import os, time
M = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "v384-pilar-quantico-gpu-02out.md")
raw = open(M, "rb").read()
assert b"estado_04out_afer8_v384" in raw and b"errata_bloco10_04out" not in raw
B = ("\n\n<!-- errata_bloco10_04out -->\n**ERRATA AO LADO do bloco 10 (04/10/2026, gerência; 9ª aferição, 9N11):** «a sonda corrente é a mais lenta ali» vale pelos números "
     "das sondas de hoje (maior/corrente = 1,000 em d = 32 e 64), não por construção; desde a 9ª, a frase do rascunho é GERADA desses números (e diz que o orçamento, "
     "a corrente × 1,25, cobre uma rodada até 25% mais lenta que ela, não mais). Os rascunhos desta rodada são os do `rascunho_prereg_v11` (o v10 é intermediário).\n")
bak = M + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw + B.encode("utf-8"); open(M + ".tmp", "wb").write(novo); assert os.path.getsize(M + ".tmp") == len(novo); os.replace(M + ".tmp", M)
assert open(M, "rb").read() == novo
print("memoria v384:", len(raw), "->", len(novo))

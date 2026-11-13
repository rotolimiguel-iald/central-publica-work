# -*- coding: utf-8 -*-
"""Errata ao lado no C18 da G1 (11/11/2026, claude-site-custodia): o timeout da primeira chamada do encadeador (até subir_ensaio) era de
4 h; na v410 a rodada levou 14.322 s (rodadas/20261111_052005.json), 78 s abaixo dos 14.400 s. No timeout, util.rodar mata só o
encadeador; o git push que ele abriu segue órfão e a tentativa seguinte o encontraria no meio. Sobe para 8 h, com o motivo no código.
O arquivo é CRLF: edição por bytes, backup de bytes antes, gravação por temporário."""
import os, time

P = r"C:\IALD\Central de Patentes\tools\custodia_g1\publica.py"
b = open(P, "rb").read()
antes = b'        r1 = util.rodar(enc + ["--so", ",".join(ate_ensaio), "--publicar"], cwd=ctx.c.CEN, timeout=4 * 3600)\r\n'
depois = (b'        # AO LADO (11/11/2026, claude-site-custodia): 4 h -> 8 h. Na v410 esta chamada levou 14.322 s (rodadas/20261111_052005.json), 78 s abaixo\r\n'
          b'        # do antigo limite de 14.400 s; no timeout, util.rodar mata so o encadeador e o git push aberto segue orfao (a tentativa seguinte o acharia no meio).\r\n'
          b'        r1 = util.rodar(enc + ["--so", ",".join(ate_ensaio), "--publicar"], cwd=ctx.c.CEN, timeout=8 * 3600)\r\n')
assert b.count(antes) == 1, "a linha do timeout mudou — PARAR"
bak = P + ".bak_%s_timeout_c18" % time.strftime("%Y%m%d_%H%M%S")
open(bak, "wb").write(b)
assert open(bak, "rb").read() == b
novo = b.replace(antes, depois)
t = P + ".tmp_errata"
open(t, "wb").write(novo)
assert os.path.getsize(t) == len(novo) > len(b)
os.replace(t, P)
compile(novo.decode("utf-8"), P, "exec")
print("ok:", bak, len(b), "->", len(novo), "| CRLF", novo.count(b"\r\n"), "LF", novo.count(b"\n"))

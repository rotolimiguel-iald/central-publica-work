# -*- coding: utf-8 -*-
"""Roda o laço do E08 do G1 (a MESMA função _ap_e08 e a conferência _conf_e08), à força, depois da correção da revisão cética da v401: o ESTADO
e o LEDGER mudaram e a frase da vaga do README mudou, mas o _ja_e08 do G1 só olha o pino e os números citados que ele audita. Nada de laço
à mão: o código é o do G1. Sem rede; só o espelho e os geradores do site (os mesmos do E08)."""
import argparse, sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
import custodiar  # noqa: E402
from custodia_g1 import espelho  # noqa: E402

a = argparse.Namespace(versao="v401", trabalho=r"C:\IALD\Central de Patentes\work\custodia_v401_25out", ator="claude-central-a7",
                       coautor="Claude Opus 5.5 <noreply@anthropic.com>", data=None, sessao=None, ordem=None, rede=False, ensaio=False,
                       aceitar_molde=False, saida=None, anterior=None, raiz=None)
ctx = custodiar._ctx(a)
r = espelho._ap_e08(ctx)
print("E08:", r)
f = espelho._conf_e08(ctx)
print("conferência E08:", f or "ok")
sys.exit(1 if f else 0)

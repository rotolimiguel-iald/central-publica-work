# -*- coding: utf-8 -*-
"""Reaplica o laco do E08 da G1 (portas <-> README <-> geradores do site) depois da parte nova do README (P = nP, 06/11/2026), e roda a
conferencia do E08 (numeros citados, rotulo, teto de 40 KB, pino do README). A marca do E08 so olha numeros citados, por isso ela dizia
«ja aplicado» com o template mudado. Usa as funcoes da propria G1, com o mesmo contexto que o custodiar.py monta. Nenhum ato para fora."""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho, motor  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

ctx = motor.Ctx(c=Caminhos({}), versao="v409", data=None, sessao="site",
                ordem=r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt",
                coautor="Claude Opus 5.5 <noreply@anthropic.com>", rede=False, publicar=False, ensaio=False, aceitar_molde=False, saida=None,
                anterior=None, ator="claude-site-custodia", trabalho=r"work\custodia_v409_06nov")
r = espelho._ap_e08(ctx)
print("E08 aplicado:", r)
f = espelho._conf_e08(ctx)
print("conferencia do E08:", "ok" if not f else f)
sys.exit(1 if f else 0)

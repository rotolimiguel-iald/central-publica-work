# -*- coding: utf-8 -*-
"""Segunda parte da regeneracao depois do registro do deposito Zenodo da v409: E05 e E08 ja foram aplicados (regerar_superficies.py). O E13 e o E14
(dados literais do selo no site e aplicar o selo ao index) se aplicam quando o SELO muda e o E13 exige o backup da versao anterior; o selo nao mudou
(o deposito nao altera nenhum dado do selo), entao ficam de fora, como no commit zenodo(v401) do espelho. Roda o E15 (cartao de estado, llms-full,
index.md) e as verificacoes do E09. Nenhum ato para fora."""
import sys

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho, motor, site  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

ctx = motor.Ctx(c=Caminhos({}), versao="v409", data=None, sessao="site",
                ordem=r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt",
                coautor="Claude Sonnet 5.5 <noreply@anthropic.com>", rede=False, publicar=False, ensaio=False, aceitar_molde=False, saida=None,
                anterior=None, ator="claude-site-custodia", trabalho=r"work\custodia_v409_06nov")
r = site._ap_e15(ctx)
f = site._conf_e15(ctx)
print("E15 aplicado:", r, "| conferencia:", "ok" if not f else f)
print("E08 conferencia:", espelho._conf_e08(ctx) or "ok")
print("E09:", espelho._ap_e09(ctx))
sys.exit(1 if f else 0)

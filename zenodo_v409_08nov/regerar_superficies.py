# -*- coding: utf-8 -*-
"""Regenera as superficies do espelho e do site depois do registro do deposito Zenodo da v409 (CITATION.cff e LEDGER.md mudaram): ESTADO_ATUAL (E05),
o laco portas <-> README <-> geradores (E08), os dados literais, o index e o corpo/gemeo Markdown do site (E13-E15) e as verificacoes (E09), pelas
funcoes da propria G1 e com o mesmo contexto do custodiar.py. A marca desses passos so olha numeros citados, por isso dizem «ja aplicado» com a fonte
mudada. Nenhum ato para fora."""
import sys

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho, motor, site  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

ctx = motor.Ctx(c=Caminhos({}), versao="v409", data=None, sessao="site",
                ordem=r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt",
                coautor="Claude Sonnet 5.5 <noreply@anthropic.com>", rede=False, publicar=False, ensaio=False, aceitar_molde=False, saida=None,
                anterior=None, ator="claude-site-custodia", trabalho=r"work\custodia_v409_06nov")
falhas = []
for nome, ap, conf in (("E05", espelho._ap_e05, espelho._conf_e05), ("E08", espelho._ap_e08, espelho._conf_e08),
                       ("E13", site._ap_e13, site._conf_e13), ("E14", site._ap_e14, None), ("E15", site._ap_e15, site._conf_e15)):
    r = ap(ctx)
    f = conf(ctx) if conf else []
    print(nome, "aplicado:", str(r)[:150], "| conferencia:", "ok" if not f else f)
    falhas += f
print("E09:", espelho._ap_e09(ctx))
sys.exit(1 if falhas else 0)

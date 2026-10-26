# -*- coding: utf-8 -*-
"""aplicar_regras_fechar_v400.py -- acrescenta ao lote G (derivar_encanamento_v400_regrasG.py) as regras do harness_fechar_sandbox (substitui a entrada sem regras). Escrito pela ferramenta Write; reexecutavel (idempotente: so' troca a linha sem regras)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "derivar_encanamento_v400_regrasG.py")
t = open(p, encoding="utf-8").read()
old = 'entrada("pos_rito/harness_fechar_sandbox_v399.py", prot_extra=_PB, autoral=True)\n'
if t.count(old) != 1:
    print("ja' aplicado ou ancora ausente:", t.count(old)); sys.exit(0)
novo = r'''_SIBLINGS_FECHAR = """shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))
# v400: os irmaos que o delta_v400 e o acom_conferencias_v400 importam por caminho (a pasta v399), o esboco R3.5 da Bancada (C15/C16), o recibo da RECUSA da Bancada a v399 e o relatorio das guardas estaticas (os textos os leem): copias de bytes, so' o que eles leem
_V9S = os.path.join(SB, "work", "cadeia_de_selo", "v399"); os.makedirs(_V9S)
for _n9 in ("delta_v399.py", "acom_conferencias_v399.py"):
    shutil.copyfile(os.path.join(os.path.dirname(PKG), "v399", _n9), os.path.join(_V9S, _n9))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "pedra"), os.path.join(_V9S, "pedra"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "insumos", "acom"), os.path.join(_V9S, "insumos", "acom"))
_rec9 = glob.glob(os.path.join(os.path.dirname(PKG), "v399", "bancada_B3_ensaio_*", "RECUSA_SINCRONIZACAO_v399_*.json")); assert len(_rec9) == 1, _rec9
os.makedirs(os.path.join(_V9S, os.path.basename(os.path.dirname(_rec9[0])))); shutil.copyfile(_rec9[0], os.path.join(_V9S, os.path.basename(os.path.dirname(_rec9[0])), os.path.basename(_rec9[0])))
shutil.copyfile(os.path.join(PKG, "GUARDAS_ESTATICAS_BANCADA_v400.json"), os.path.join(PKS, "GUARDAS_ESTATICAS_BANCADA_v400.json"))
os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
"""
entrada("pos_rito/harness_fechar_sandbox_v399.py", prot_extra=_PB, autoral=True, regras=[
    ('for kn_ in ("KERNEL_RECIBO_v400.json", "FLAGS_v400.json"):', 'for kn_ in ("KERNEL_RECIBO_v400.json", "FLAGS_v399.json"):', 1),
    ('shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))\n', _SIBLINGS_FECHAR, 1),
    ('PKG_ANT = os.path.join(os.path.dirname(PKG), "v399")', 'PKG_ANT = os.path.join(os.path.dirname(PKG), "v398")', 1),
    ('"RECIBO_SINCRONIZACAO_v399_*.json"', '"RECIBO_SINCRONIZACAO_v398_*.json"', 1),
    ("SINTETICOS (derivados dos reais da v399, como no harness dos textos)", "SINTETICOS (derivados dos reais da v398, o ultimo B(n) feito na Bancada, como no harness dos textos)", 1),
    ("# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v399)", "# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v398)", 1),
])
'''
open(p + ".tmp", "w", encoding="utf-8", newline="\n").write(t.replace(old, novo))
os.replace(p + ".tmp", p)
print("regras do harness_fechar_sandbox aplicadas ao lote G")

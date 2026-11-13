# -*- coding: utf-8 -*-
"""Retrato (só leitura no espelho): grava em <PASTA> os bytes do ESTADO_ATUAL.md e do tools/gerar_estado_atual.py do espelho e o README
da v411 renderizado em memória pela G1 (como a E08 o faria), para comparar antes/depois da subida da seção das sete ressalvas (D195).
Uso: python -X utf8 retrato_estado_readme_13nov.py <PASTA_DE_SAIDA> <rotulo>"""
import hashlib, shutil, sys
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import primordial as PRIM, readme_pinado as RP  # noqa: E402

TB = Path(r"C:\IALD\Artigo\the_boundary")
HO = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v411_CUSTODIA.md"
OUT, ROT = Path(sys.argv[1]), sys.argv[2]
OUT.mkdir(parents=True, exist_ok=True)
for src, nome in ((TB / "ESTADO_ATUAL.md", "ESTADO_ATUAL"), (TB / "tools" / "gerar_estado_atual.py", "gerar_estado_atual")):
    dst = OUT / ("%s_%s%s" % (nome, ROT, src.suffix))
    shutil.copyfile(src, dst)
    assert dst.read_bytes() == src.read_bytes()
P = PRIM.montar({"handoff": HO})
pb = PRIM.serializar(P)
C = RP.Ctx(P, pb)
texto, _ = RP.renderizar(C, TB / "tools" / "readme_pinado" / "readme_template.md", TB / "tools" / "readme_pinado" / "readme_partes",
                         RP.extrair_portas((TB / "README.md").read_text(encoding="utf-8")))
(OUT / ("README_renderizado_%s.md" % ROT)).write_bytes(texto.encode("utf-8"))
for p in sorted(OUT.glob("*_%s.*" % ROT)):
    print("%-40s %8d B sha16 %s" % (p.name, p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()[:16]))

# -*- coding: utf-8 -*-
"""03/11/2026 08:5x, gerencia c1: o README do espelho passou a ser GERADO de PRIMORDIAL.json e pinado em PINO_README.json (D39, ratificado pelo operador em 03/11;
commit ff882f81 do espelho). A G1, porem, ainda chama o gerador antigo (gerar_readme_frente.py) no laco do E08: na custodia da v407 ela regravaria o README pinado no
formato velho. Remendo AO LADO em tools/custodia_g1/espelho.py: (1) helper `_gerar_readme_pinado(ctx)` que roda primordial.py + readme_pinado.py --gerar quando o espelho
tem o template do pinado, e cai para o gerador antigo so' se nao tiver (versoes anteriores a 03/11); (2) o laco interno do E08 chama o helper no lugar do gerador antigo;
(3) `_conf_e08` ganha a verificacao do pino (readme_pinado.py --verificar --conferir-fontes): README editado fora do gerador, pino ou PRIMORDIAL defasados PARAM a custodia.
Aplicado por patches.aplicar_em_arquivo (backup de BYTES, py_compile, os.replace). Nada toca o espelho, o um.py, o selo ou o gate. Escrito pelo Write."""
import json, sys
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); ESP = CEN / "tools" / "custodia_g1" / "espelho.py"
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import patches  # noqa: E402

O1 = "def _ap_e08(ctx):\n    c = ctx.c\n    sig_ant, passadas = None, []\n"
N1 = ('def _gerar_readme_pinado(ctx):\n'
      '    """[AO LADO, 03/11/2026, gerência c1 — o README PINADO (D39, ratificado pelo operador em 03/11/2026; espelho ff882f81)] O README do espelho é GERADO de\n'
      '    PRIMORDIAL.json (tools/custodia_g1/primordial.py) e pinado em PINO_README.json (tools/custodia_g1/readme_pinado.py). O gerador antigo (gerar_readme_frente.py) só\n'
      '    roda se o espelho ainda não tiver o template do pinado (estado anterior a 03/11/2026). Lição: sem isto a custódia seguinte regravaria o README pinado no formato velho."""\n'
      '    c = ctx.c\n'
      '    tpl = c.TB / "tools" / "readme_pinado" / "readme_template.md"\n'
      '    if not tpl.is_file():\n'
      '        exigir_rc0(_tb(ctx, "gerar_readme_frente.py"), "gerar_readme_frente.py")\n'
      '        return\n'
      '    g1 = Path(__file__).resolve().parent\n'
      '    exigir_rc0(util.rodar([_py(ctx), "-X", "utf8", str(g1 / "primordial.py"), "--saida", str(c.TB), "--nos", str(c.NOS), "--espelho", str(c.TB)],\n'
      '                          cwd=c.CEN, timeout=900), "primordial.py")\n'
      '    exigir_rc0(util.rodar([_py(ctx), "-X", "utf8", str(g1 / "readme_pinado.py"), "--gerar", "--primordial", str(c.TB / "PRIMORDIAL.json"), "--template", str(tpl),\n'
      '                           "--partes", str(tpl.parent / "readme_partes"), "--saida", str(c.TB), "--nos", str(c.NOS), "--espelho", str(c.TB)],\n'
      '                          cwd=c.CEN, timeout=900), "readme_pinado.py --gerar")\n'
      '\n'
      '\n'
      'def _verificar_readme_pinado(ctx):\n'
      '    """[AO LADO, 03/11/2026] a verificação do pino do README (vazia se o espelho ainda não tem o pinado): lista de falhas para _conf_e08."""\n'
      '    c = ctx.c\n'
      '    tpl = c.TB / "tools" / "readme_pinado" / "readme_template.md"\n'
      '    if not tpl.is_file():\n'
      '        return []\n'
      '    g1 = Path(__file__).resolve().parent\n'
      '    r = util.rodar([_py(ctx), "-X", "utf8", str(g1 / "readme_pinado.py"), "--verificar", "--conferir-fontes", "--primordial", str(c.TB / "PRIMORDIAL.json"),\n'
      '                    "--template", str(tpl), "--partes", str(tpl.parent / "readme_partes"), "--readme", str(c.TB / "README.md"), "--pino", str(c.TB / "PINO_README.json"),\n'
      '                    "--nos", str(c.NOS), "--espelho", str(c.TB)], cwd=c.CEN, timeout=900)\n'
      '    if r["rc"] != 0:\n'
      '        return ["README pinado não confere (readme_pinado.py --verificar --conferir-fontes, rc %s): %s" % (r["rc"], " | ".join(r["saida"].strip().splitlines()[-3:]))]\n'
      '    return []\n'
      '\n'
      '\n'
      'def _ap_e08(ctx):\n    c = ctx.c\n    sig_ant, passadas = None, []\n')
O2 = '            exigir_rc0(_tb(ctx, "gerar_readme_frente.py"), "gerar_readme_frente.py")\n'
N2 = ('            # ERRATA AO LADO (03/11/2026, gerência c1): o original (abaixo, intacto) chamava o gerador antigo; desde o README pinado (ff882f81) o gerador é o do pino.\n'
      '            #     exigir_rc0(_tb(ctx, "gerar_readme_frente.py"), "gerar_readme_frente.py")\n'
      '            _gerar_readme_pinado(ctx)\n')
O3 = ('    if len(ctx.ler(ctx.c.TB / "README.md").encode("utf-8")) > 40960:\n'
      '        f.append("README passou do teto de 40.960 bytes (L01)")\n'
      '    return f\n')
N3 = ('    if len(ctx.ler(ctx.c.TB / "README.md").encode("utf-8")) > 40960:\n'
      '        f.append("README passou do teto de 40.960 bytes (L01)")\n'
      '    f += _verificar_readme_pinado(ctx)   # [AO LADO, 03/11/2026] o pino do README: editado fora do gerador, pino ou PRIMORDIAL defasados PARAM a custódia\n'
      '    return f\n')
PARES = [(O1, N1, "1 helpers _gerar_readme_pinado/_verificar_readme_pinado"), (O2, N2, "2 laco do E08 chama o gerador do pino"), (O3, N3, "3 _conf_e08 verifica o pino")]


def f(s):
    assert "_gerar_readme_pinado" not in s, "a errata ja esta' no espelho.py"
    for o, _, nome in PARES:
        assert s.count(o) == 1, "trecho original nao esta' UMA vez (%d): %s" % (s.count(o), nome)
    for o, n, _ in PARES:
        s = s.replace(o, n)
    return s, [p[2] for p in PARES]


r = patches.aplicar_em_arquivo(ESP, f, "v406_readme_pinado_e08")
print("patch:", json.dumps(r, ensure_ascii=False)); assert r["estado"] == "aplicado"
import importlib  # noqa: E402
m = importlib.import_module("custodia_g1.espelho"); assert callable(m._gerar_readme_pinado) and callable(m._verificar_readme_pinado)
print("OK: custodia_g1.espelho importa com o gerador do pino no E08; conferir com `custodiar.py planejar --seco`")

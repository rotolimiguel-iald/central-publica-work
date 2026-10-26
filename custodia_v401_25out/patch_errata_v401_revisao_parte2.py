# -*- coding: utf-8 -*-
"""Parte 2 da correção da revisão cética da v401: a raiz no G1 (textos.py, CRLF) e o ESTADO_ATUAL regerado pelo gerador."""
import os, py_compile, subprocess, time, json
from pathlib import Path

TS = time.strftime("%Y%m%d_%H%M%S")
TB = Path(r"C:\IALD\Artigo\the_boundary")
G = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\textos.py")
raw = G.read_bytes(); s = raw.decode("utf-8")
CR, LF = chr(13), chr(10)
NL = CR + LF if (CR + LF) in s else LF
if "o registro que VALE para a anterior" not in s:
    pares = [
        ('    khp = "kh_n1_cobertura_" + ant' + LF,
         '    khp = F.get("kh_registro_anterior") or ("kh_n1_cobertura_" + ant)   # 25/10/2026 (revisão v401): o registro que VALE para a anterior' + LF +
         '    if F["kh"].get("constantes_anterior") is None or F["kh"].get("teoremas_anterior") is None:' + LF +
         '        raise Parar("a cobertura do kernel da anterior não foi lida (kh anterior ausente nos fatos) — PARAR, não escrever None na errata")' + LF),
        ('T.txt_en.texto, verd, nota', 'T.txt_en.texto.rstrip("."), verd, nota'),
    ]
    for a, b in pares:
        a, b = a.replace(LF, NL), b.replace(LF, NL)
        n = s.count(a)
        assert n == 1, (a[:60], n)
        s = s.replace(a, b)
    assert "Parar" in s.split("def ")[0] or "import" in s, "conferir import de Parar"
    G.with_name(G.name + ".bak_" + TS).write_bytes(raw)
    t = G.with_name(G.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, G)
    print("  textos.py: %d -> %d" % (len(raw), G.stat().st_size))
else:
    print("  textos.py: já corrigido")
r = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", str(TB / "tools" / "gerar_estado_atual.py")], capture_output=True, text=True, encoding="utf-8", cwd=str(TB))
print("  gerar_estado_atual.py rc=%d | %s" % (r.returncode, (r.stdout.strip().splitlines() or [""])[-1][:200]))
F = json.loads(Path(r"C:\IALD\Central de Patentes\work\custodia_v401_25out\fatos_v401.json").read_text(encoding="utf-8"))
est = (TB / "ESTADO_ATUAL.md").read_text(encoding="utf-8")
ok = ("%d -> %d constants" % (F["kh"]["constantes_anterior"], F["kh"]["constantes"])) in est and "None -> " not in est.split("custody of v401")[-1] \
     and ("`%s` now charges floors" % F["kh_registro_anterior"]) in est and "does not block the publication" not in est
print("ESTADO_ATUAL corrigido:", ok)

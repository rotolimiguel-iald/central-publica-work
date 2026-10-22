# -*- coding: utf-8 -*-
"""Monta o MODO INTERATIVO PÚBLICO da Central no site (C:\\IALD\\Site\\tgl\\v3.0\\central\\): o app público (frontend/dist_publica), o
retrato (snapshot/: api/ + páginas de omissão), o um.acom público e os seus dados (acom/). Cópia de bytes conferida por sha256.
Recria a pasta central/ do site a cada montagem (ela só contém o que este script põe)."""
import hashlib, json, shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SITE = Path(r"C:\IALD\Site\tgl\v3.0")
DEST = SITE / "central"
FONTES = [Path(r"C:\IALD\Central de Patentes\frontend\dist_publica"),
          Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\snapshot"),
          Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\acom")]
for f in FONTES:
    assert f.is_dir(), f
assert (FONTES[0] / "index.html").is_file() and (FONTES[1] / "api" / "_mapa.json").is_file() and (FONTES[2] / "um.acom").is_file()
if DEST.exists():
    marca = DEST / ".montado_por_montar_central_no_site"
    assert marca.is_file(), "a pasta central/ do site existe e não foi montada por este script — PARAR"
    shutil.rmtree(DEST)
DEST.mkdir(parents=True)
(DEST / ".montado_por_montar_central_no_site").write_text("montado por work/central_publica_22out/montar_central_no_site.py\n", encoding="utf-8")
n = b = 0
for base in FONTES:
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(base)
        d = DEST / rel
        assert not d.exists(), ("colisão de caminho na montagem", rel)
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, d)
        assert hashlib.sha256(p.read_bytes()).hexdigest() == hashlib.sha256(d.read_bytes()).hexdigest(), rel
        n += 1; b += d.stat().st_size
print("central/ no site: %d arquivos, %.1f MB" % (n, b / 2**20))

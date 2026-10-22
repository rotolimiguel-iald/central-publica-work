# -*- coding: utf-8 -*-
"""Repassa a máscara AMPLIADA de 22/10/2026 (telefone sem rótulo nas formas inequívocas, CEP, data de nascimento, endereço com quadra e
lote) em TODO arquivo de texto do retrato do site (snapshot/), no lugar — os já mascarados ficam como estão (a marca não casa com nenhum
padrão). Binário (pyc, imagem, vídeo, PDF, um.acom) não se toca. Gravação atômica; relatório ao lado."""
import json, os, sys, time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import mascarar  # noqa: E402

OUT = Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\snapshot")
tot = Counter(); mudados = []
for p in sorted(OUT.rglob("*")):
    if not p.is_file() or p.suffix.lower() in (".png", ".pdf", ".acom", ".mp4", ".jpg", ".jpeg", ".gif", ".webp"):
        continue
    raw = p.read_bytes()
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError:
        continue
    t2, c = mascarar(t)
    if t2 != t:
        tmp = p.with_name(p.name + ".tmp_remasc")
        tmp.write_bytes(t2.encode("utf-8"))
        os.replace(tmp, p)
        mudados.append({"arquivo": p.relative_to(OUT).as_posix(), "mascaras": c})
        tot.update(c)
rel_p = OUT / "RELATORIO_RETRATO_PUBLICO.json"
rel = json.loads(rel_p.read_text(encoding="utf-8"))
rel["remascara_ampliada"] = {"em": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos_mudados": len(mudados), "por_categoria": dict(tot)}
tmp = rel_p.with_name(rel_p.name + ".tmp_remasc")
tmp.write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf-8")
os.replace(tmp, rel_p)
print("retrato: %d arquivos com máscara nova | %s" % (len(mudados), dict(tot)))
for m in mudados[:20]:
    print("   ", m)

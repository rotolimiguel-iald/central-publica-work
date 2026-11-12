# -*- coding: utf-8 -*-
"""Grava artefatos/PINOS.json: sha256 e bytes de todos os arquivos do pacote (SO' codigo/ e artefatos/), exceto o proprio PINOS.
Nao entra em producao/ (la ficam o vetor pinado e os recibos da gerencia: este script nunca os le) nem nos arquivos soltos da raiz."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PASTAS = ("codigo", "artefatos")
files = sorted(p for d in PASTAS for p in (ROOT / d).rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != "PINOS.json"
               and not p.name.endswith(".tmp") and not p.name.endswith(".tmp.npz"))
pins = {str(p.relative_to(ROOT)).replace("\\", "/"): {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
dest = ROOT / "artefatos" / "PINOS.json"
tmp = dest.with_suffix(".json.tmp")
tmp.write_text(json.dumps({"pasta": str(ROOT), "pastas_pinadas": list(PASTAS), "n_arquivos": len(pins), "arquivos": pins}, ensure_ascii=False, indent=1), encoding="utf-8")
tmp.replace(dest)
print(len(pins), "arquivos pinados")

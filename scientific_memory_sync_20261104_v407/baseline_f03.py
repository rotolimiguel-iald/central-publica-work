"""Fotografia SOMENTE LEITURA da arvore da memoria canonica (canonical_memory) e do ACTIVE, para provar depois que a escrita unica da F0.3 so' acrescentou o release novo e moveu o ACTIVE.
Uso: python baseline_f03.py <saida.json>.  Registra, para cada arquivo: caminho relativo, bytes, mtime_ns e (se <= 4 MB) sha256. Nada e' escrito fora da saida."""
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
sys.path.insert(0, str(BASE))
sys.dont_write_bytecode = True
from iald_orchestrator import canonical_memory as cm  # noqa: E402

root = Path(cm.ACTIVE).parent
arquivos = {}
for p in sorted(root.rglob("*")):
    if p.is_file():
        st = p.stat()
        rel = str(p.relative_to(root))
        item = {"bytes": st.st_size, "mtime_ns": st.st_mtime_ns}
        if st.st_size <= 4 * 1024 * 1024:
            item["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        arquivos[rel] = item
releases = sorted(d.name for d in Path(cm.RELEASES).iterdir() if d.is_dir())
manifests = {}
for r in releases:
    mp = Path(cm.RELEASES) / r / "manifest.json"
    if mp.exists():
        manifests[r] = hashlib.sha256(mp.read_bytes()).hexdigest()
active_raw = Path(cm.ACTIVE).read_bytes()
out = {"raiz": str(root), "active_path": str(cm.ACTIVE), "active_sha256": hashlib.sha256(active_raw).hexdigest(), "active": json.loads(active_raw),
       "releases": releases, "manifests_sha256": manifests, "n_arquivos": len(arquivos), "arquivos": arquivos}
Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("raiz", root)
print("releases", len(releases), releases[-3:])
print("arquivos", len(arquivos), "| ACTIVE", out["active"].get("release"), out["active"].get("epoch"), "sha256", out["active_sha256"][:16])

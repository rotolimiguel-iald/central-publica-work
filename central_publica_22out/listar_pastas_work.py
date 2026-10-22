# -*- coding: utf-8 -*-
"""Lista (SÓ LEITURA) as pastas de primeiro nível de work/ e da bancada Chatgpt/ com o número de arquivos publicáveis (código e texto
<= 25 MB, figuras) e o tamanho, para a classificação pública."""
import json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(r"C:\IALD\Central de Patentes")
TXT = {".py", ".lean", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx",
       ".jsx", ".html", ".css", ".ipynb", ".sh", ".ps1", ".bat", ".cfg", ".ini", ".sql", ".bib", ".xml", ".svg", ".dat", ".log", ".out",
       ".diff", ".patch", ".png", ".pdf", ".jpg", ".jpeg"}
EXCL_DIR = {".git", ".venv", "venv", "node_modules", "__pycache__", ".lake", "tex_environment", "site-packages", "dist-packages", "build", ".cache"}
out = {}
for reg in ("work", "Chatgpt"):
    for top in sorted(p for p in (C / reg).iterdir() if p.is_dir()):
        n = b = 0
        for dp, dns, fns in os.walk(top):
            dns[:] = [d for d in dns if d not in EXCL_DIR]
            for f in fns:
                if os.path.splitext(f)[1].lower() in TXT and ".bak_" not in f:
                    try:
                        s = os.path.getsize(os.path.join(dp, f))
                    except OSError:
                        continue
                    if s <= 25 * 1024 * 1024:
                        n += 1; b += s
        out["%s/%s" % (reg, top.name)] = (n, round(b / 2**20, 1))
(C / "work" / "central_publica_22out" / "pastas_publicaveis.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k, (n, mb) in sorted(out.items(), key=lambda x: -x[1][1])[:60]:
    print("%8d arq %9.1f MB  %s" % (n, mb, k))
print("pastas:", len(out))

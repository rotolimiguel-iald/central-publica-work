# -*- coding: utf-8 -*-
"""Varredura (SÓ LEITURA) do conteúdo EMPACOTADO dos 16 *_FINAL.py (o _B64 é um zip em base64, que a máscara de texto não enxerga):
abre cada zip em memória e conta dado pessoal e credencial por arquivo embutido (categoria e contagem; nunca o dado)."""
import ast, base64, io, json, sys, zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import mascarar  # noqa: E402

TXT = (".py", ".md", ".json", ".txt", ".yaml", ".yml", ".csv", ".tex", ".toml", ".cfg", ".ini", ".html", ".js")
achados = {}
for f in sorted(Path(r"C:\IALD\Central de Patentes\patents").glob("*/*_FINAL.py")):
    src = f.read_text(encoding="utf-8")
    t = ast.parse(src)
    b64 = None
    for n in t.body:
        if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "_B64" for x in n.targets):
            b64 = ast.literal_eval(n.value)
    assert b64, f
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(b64))) as z:
        for nome in z.namelist():
            if nome.lower().endswith(TXT):
                _, c = mascarar(z.read(nome).decode("utf-8", "replace"))
                if c:
                    achados.setdefault(f.name, {})[nome] = c
print(json.dumps(achados, ensure_ascii=False, indent=1)[:4000])
print("FINAL com achado:", len(achados), "de 16")

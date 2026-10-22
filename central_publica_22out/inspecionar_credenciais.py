# -*- coding: utf-8 -*-
"""Inspeciona (SÓ LEITURA) onde estão as credenciais achadas pela varredura: pasta e tipo, com o valor MASCARADO."""
import json, re, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(r"C:\IALD\Central de Patentes")
d = json.loads((C / "work" / "central_publica_22out" / "varredura_arquivos_por_categoria.json").read_text(encoding="utf-8"))
rx = re.compile(r"(?i)(password|passwd|senha|secret_key|api_key|apikey|access_token|client_secret|smtp_pass)[\"']?\s*[:=]\s*[\"']([^\"'\s]{8,})[\"']")


def regiao(p):
    r = Path(p).relative_to(C).parts
    return "/".join(r[:2]) if r[0] in ("work", "Chatgpt") else r[0]


for cat in ("credencial_atribuida", "credencial_token"):
    ps = d.get(cat, [])
    print("==", cat, len(ps), "arquivos; por pasta:", Counter(regiao(p) for p in ps).most_common(10))
cen = [p for p in d.get("credencial_atribuida", []) if Path(p).relative_to(C).parts[0] not in ("work", "Chatgpt")]
for p in cen:
    t = Path(p).read_text(encoding="utf-8", errors="replace")
    print("NÚCLEO:", Path(p).relative_to(C))
    for m in rx.finditer(t):
        print("    ", m.group(1), "=", m.group(2)[:3] + "…(%d)" % len(m.group(2)))

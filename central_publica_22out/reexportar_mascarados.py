# -*- coding: utf-8 -*-
"""Refaz, com a máscara corrigida (mascara_pii.py: o «@» de matriz do Python não é e-mail), toda leitura do retrato que a regra antiga
mascarou: relê da Central local (só GET), mascara de novo, e para o Atlas, o TGL Core e as peças de patente repassa o filtro das notas
operacionais. Relatório ao lado."""
import json, sys, time, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mascara_pii import mascarar            # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402

OUT = Path(sys.argv[1])
mapa = json.loads((OUT / "api" / "_mapa.json").read_text(encoding="utf-8"))
rel = json.loads((OUT / "RELATORIO_RETRATO_PUBLICO.json").read_text(encoding="utf-8"))
alvos = [u for u in rel["mascarados_por_url"] if u in mapa] + [u for u in ("/api/tgl-atlas", "/api/tgl-core") if u in mapa]
novo = {}
for u in dict.fromkeys(alvos):
    time.sleep(0.55)
    t = urllib.request.urlopen("http://127.0.0.1:8765" + u, timeout=180).read().decode("utf-8", "replace")
    t, c = mascarar(t)
    if u in ("/api/tgl-atlas", "/api/tgl-core") or u.startswith("/api/documents/"):
        t, n = filtrar_markdown(t)
        if n:
            c["notas_operacionais_omitidas"] = n
    (OUT / mapa[u]).write_text(t, encoding="utf-8")
    if c:
        novo[u] = c
rel["mascarados_por_url"] = novo
rel["n_urls_com_mascara"] = len(novo)
rel["remascarado_em"] = time.strftime("%Y-%m-%d %H:%M:%S") + " (máscara corrigida: o @ de matriz do Python não é e-mail)"
(OUT / "RELATORIO_RETRATO_PUBLICO.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf-8")
print("remascarados: %d leituras relidas | %d ainda com dado pessoal mascarado" % (len(dict.fromkeys(alvos)), len(novo)))
print(json.dumps({k: v for k, v in list(novo.items())[:12]}, ensure_ascii=False)[:1500])

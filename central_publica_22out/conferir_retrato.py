# -*- coding: utf-8 -*-
"""PORTÃO do retrato público (24/10/2026, gerência a7). Roda logo depois de `retrato` na esteira pública e PARA a rodada (rc 1) se a
exportação não estiver inteira: o relatório tem de dizer 0 falhas, o mapa tem de trazer as rotas que o app público lê (classes, patents),
e o número de URLs não pode cair abaixo do piso. Motivo medido: em 24/10 às 15:08 a exportação coincidiu com um reinício do backend
(:8765), `/api/classes` faltou no `_mapa.json`, a rodada seguiu («APROVADO») e a home pública foi ao ar sem cartões. Só leitura."""
import json, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

SNAP = Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\snapshot")
REL = SNAP / "RELATORIO_RETRATO_PUBLICO.json"
MAPA = SNAP / "api" / "_mapa.json"
OBRIGATORIAS = ("/api/classes", "/api/patents")
PISO_URLS = 900
erros = []
try:
    r = json.loads(REL.read_text(encoding="utf-8"))
except (OSError, ValueError) as e:
    print("PORTÃO DO RETRATO: relatório ilegível (%r) — PARAR" % (e,))
    sys.exit(1)
if r.get("n_falhas") != 0 or r.get("falhas"):
    erros.append("relatório com %s falha(s): %s" % (r.get("n_falhas"), json.dumps(r.get("falhas"), ensure_ascii=False)[:300]))
if (r.get("n_urls") or 0) < PISO_URLS:
    erros.append("n_urls %s abaixo do piso %d" % (r.get("n_urls"), PISO_URLS))
try:
    mapa = json.loads(MAPA.read_text(encoding="utf-8"))
    chaves = list(mapa.keys()) if isinstance(mapa, dict) else [str(x) for x in mapa]
    texto = json.dumps(mapa, ensure_ascii=False)
except (OSError, ValueError) as e:
    erros.append("mapa ilegível: %r" % (e,))
    chaves, texto = [], ""
for rota in OBRIGATORIAS:
    if rota not in texto:
        erros.append("rota obrigatória ausente do mapa: %s" % rota)
if erros:
    print("PORTÃO DO RETRATO: REPROVADO — a rodada para antes de montar:")
    for e in erros:
        print("   !", e)
    sys.exit(1)
print("PORTÃO DO RETRATO: aprovado | gerado_em %s | %s URLs, 0 falhas | rotas obrigatórias no mapa: %s | entradas do mapa: %d"
      % (r.get("gerado_em"), r.get("n_urls"), ", ".join(OBRIGATORIAS), len(chaves)))

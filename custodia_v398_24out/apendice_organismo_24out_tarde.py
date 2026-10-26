# -*- coding: utf-8 -*-
"""Apêndice datado (24/10/2026, tarde) na memória do organismo: a Torre no backend, os contratos públicos do Kimi, a ORDEM 022 dos filmes, o limite do deploy. Backup de bytes."""
import os, sys
from datetime import datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S"); AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
p = Path("C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/organismo-torre-de-comando-23out.md")
raw = p.read_bytes(); p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
nl = "\r\n" if b"\r\n" in raw else "\n"
texto = ("## %s — a Torre ganhou backend; contratos públicos; o limite do automático\n\n"
   "- **`GET /api/torre`** (admin; `backend/app/torre.py`, 32/32 testes): missões ACOM vivas (projeções em paralelo, cache 60 s), custódias (`custodias.json`), vigia (`VIGIA_ULTIMO.json`), "
   "X diário (livro + recibos), túneis (ordens do Codex, threads), erros visíveis; `POST /api/torre/custodia/planejar` (só `planejar --seco`) e `POST /api/torre/x/ensaio` (só `--seco`). "
   "A página `Torre.tsx` é do Kimi (programa §3). O backend privado é reiniciado por PID pela gerência (`Start-Process pythonw -m uvicorn …` como o `iniciar_central.ps1`).\n"
   "- **Contratos públicos** (esteira: passo `central_extra` antes do `montar`): `central/organismo/index.html` (a página do Kimi, recuperada do ar), `ESTADO_DO_ORGANISMO.json` saneado, "
   "`custodias.json`, `pensamentos/pensamentos.json`, `arcos.json` (ainda não publicado). Regra medida: a rodada pública tem de ser UMA invocação (o `--so` por passo quebra o nome do manifesto da subida).\n"
   "- **O limite do automático, medido:** a troca do serviço do app (terminar o filho web pelo PID) é barrada pelo classificador do modo automático; o reinício do backend privado da Central (uvicorn) não é. "
   "Tudo antes da troca (build, contagem, revisão distinta, aceites, claim) corre sozinho.\n"
   "- **ORDEM 022** (filmes V7) na fila do Codex; a subida dos filmes é da gerência (`integrar_filmes_v7.py` por hash). Ver [[filmes-do-site-v7-24out]].") % AGORA
t = p.with_name(p.name + ".tmp"); t.write_bytes((raw.decode("utf-8").rstrip("\r\n") + nl + nl + texto.replace("\n", nl) + nl).encode("utf-8"))
assert t.stat().st_size > len(raw); os.replace(t, p); print("ok", p.name, len(raw), "->", p.stat().st_size)

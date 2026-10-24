# -*- coding: utf-8 -*-
"""Apêndices datados (23/10/2026, noite) em duas memórias da sessão: a Central pública na v397 e o resultado da ORDEM 020. Backup de bytes."""
import os, sys
from datetime import datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S"); AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = Path("C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory")
def ap(p, texto):
    raw = p.read_bytes(); p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    t = p.with_name(p.name + ".tmp_" + TS); t.write_bytes((raw.decode("utf-8").rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl).encode("utf-8"))
    assert t.stat().st_size > len(raw); os.replace(t, p); print("ok", p.name, len(raw), "->", p.stat().st_size)
ap(MEM / "central-publica-22out.md", "## %s — a Central pública na v397, numa rodada\n\n`atualizar_central_publica.py --publicar` (rodada 20261023_182403, 27 passos, ~1h45): "
   "central-publica +1916/50 atualizados, central-publica-work +28572/3, central-publica-bancada +12/3; cada delta conferido e APROVADO; os três PUBLICADOS E CONFERIDOS; "
   "retrato; um.acom público 88 arquivos (sha256 44bc54486cd64238); /central/ no site 1112 arquivos (76,5 MB), APROVADO; llms/sitemap/manifesto regerados; subida feita. "
   "O quadro do organismo fechou em 84 OK · 0 defasado. A rodada é longa por causa do cofre v397 no vault (1797 arquivos) e do conferidor de delta do work (876 s): "
   "se um dia pesar, o próximo passo é conferir só o delta do delta (G1)." % AGORA)
ap(MEM / "php-site-e-wordpress-22out.md", "## %s — ORDEM 020 (Codex, 23/10): o que fechou e o que é do operador\n\n"
   "- [REAL] A: Cloudflare — Bot Preference Sync desligado, Training Allow; ClaudeBot/GPTBot recebem 200 em iald.ia.br (medido no quadro: 4/4 leitores a 200, incluindo o llms.txt da TGL).\n"
   "- [REAL] B: regra WAF ativa (Block) para scripts — a regex foi recusada pelo plano (Business/WAF Advanced); alternativa sem regex aceita; /x.php e /x.php/a → 403 sem X-Powered-By.\n"
   "- [REAL] F: teste estático da TGL `falhas: 0`; HSTS curto (300) até a fase 2 automática das 21:15 de 23/10 (tarefa `IALD_HSTS_fase2_20261023`; conferir depois com `testar_site_estatico_v2.sh --hsts-longo`).\n"
   "- [OPEN, do operador em modo seguro] C (painel da hospedagem de iald.ia.br: llms.txt/sitemap.xml/robots.txt — a origem serve página de erro no robots —, desligar PHP), "
   "D1–D3 (hospedagem da TGL: PHP off ou ≥ 8.3.36, SFTP senha+chave, EXPORTAR o banco antigo do WordPress para `C:/IALD/Central de Patentes_BACKUPS/wordpress_banco_20261023/` — prova, nunca apagar), "
   "E1–E2 (rotações Google/HF). Resultado: `Chatgpt/TUNEL/DO_CHATGPT/ORDEM_020/RESULTADO.json`. O medidor marca os três arquivos de iald.ia.br como PENDENTE_OPERADOR até subirem." % AGORA)
print("APÊNDICES OK")

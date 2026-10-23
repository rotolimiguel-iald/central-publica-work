# -*- coding: utf-8 -*-
"""SÓ LEITURA: extrai do transcrito desta sessão os comandos da cadeia da custódia v395 (21/10), para repetir a ordem sem adivinhar."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
F = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5.jsonl"
CH = ("gerar_estado_atual", "gerar_portas", "gerar_readme_frente", "verificar_portas", "guarda_do_selo", "pos_push", "aplicar_selo",
      "gerar_llms", "gerar_index_md", "gerar_sitemap", "gerar_manifesto", "subir_site", "leitor_ia", "custodia_v395", "git commit", "git push",
      "atualizar_dados_selo", "guarda_do_site", "gerar_cartoes", "gerar_insumos", "gerar_secoes", "gerar_read_brief")
vistos = set()
with open(F, encoding="utf-8") as f:
    for ln in f:
        if '"tool_use"' not in ln:
            continue
        try:
            d = json.loads(ln)
        except Exception:
            continue
        ts = d.get("timestamp", "")
        if not ts.startswith("2026-10-21"):
            continue
        for c in (d.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Bash":
                cmd = (c.get("input") or {}).get("command", "")
                if any(k in cmd for k in CH) and cmd not in vistos:
                    vistos.add(cmd)
                    print("[%s] %s\n" % (ts[11:19], cmd[:1500]))

# -*- coding: utf-8 -*-
"""SÓ LEITURA: os comandos de 22/10 que montaram o retrato público, o um.acom e a pasta central/ do site (para repetir a ordem)."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
F = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5.jsonl"
CH = ("exportar_cockpit_publico", "aparar_retrato", "remascarar_retrato", "reexportar_mascarados", "gerar_um_acom_publico",
      "montar_central_no_site", "vincular_central_no_site", "conferir_subpasta", "manifesto_central_publica", "dist_publica", "npm run build",
      "vite build", "patch_frontend_publico", "gerar_readmes_publicos")
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
        if not ts.startswith("2026-10-22"):
            continue
        for c in (d.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") in ("Bash", "PowerShell"):
                cmd = (c.get("input") or {}).get("command", "")
                if any(k in cmd for k in CH) and cmd not in vistos:
                    vistos.add(cmd)
                    print("[%s] %s\n" % (ts[11:19], cmd[:1800]))

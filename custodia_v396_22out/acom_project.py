# -*- coding: utf-8 -*-
"""ACOM project (só leitura) da referência exata desta tarefa (sessão a7, PHP + custódia v396): imprime revisão, fase e próxima ação."""
import json, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-central-a7_php-v396-22out.json"
req = json.dumps({"operation": "project", "reference": REF}, ensure_ascii=False).encode("utf-8")
out = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=req, capture_output=True)
txt = out.stdout.decode("utf-8", "replace")
try:
    d = json.loads(txt)
except json.JSONDecodeError:
    print("FALHA de leitura:", txt[:800], out.stderr.decode("utf-8", "replace")[:800])
    sys.exit(1)


def acha(x, k):
    if isinstance(x, dict):
        for a, b in x.items():
            if a == k:
                return b
            v = acha(b, k)
            if v is not None:
                return v
    elif isinstance(x, list):
        for b in x:
            v = acha(b, k)
            if v is not None:
                return v
    return None


print("ok:", d.get("ok"), "| erro:", d.get("error"), str(d.get("message", ""))[:200])
print("revision:", acha(d, "revision"), "| phase:", acha(d, "phase"))
print("next_action:", str(acha(d, "next_action"))[:300])

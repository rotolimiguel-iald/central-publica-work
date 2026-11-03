from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
sys.path.insert(0, str(BASE))

from iald_orchestrator.runtime import Runtime

runtime = Runtime(recover=False)
connections = runtime.connections()
local = [row for row in connections if "qwen" in str(row).lower() or "local" in str(row).lower()]
prompt = "Imaginar candidatos a um discriminante TGL >= 5 sigma, com nulo rival, previsão sem ajuste e estatística; sem abrir D."
preview = runtime.preview(prompt, {"required_provider": "local", "max_calls": 1})
result = {
    "local_connections": local,
    "preview": {
        "selected": preview.get("selected"),
        "execution_constraints": preview.get("execution_constraints"),
        "cost_reservation": preview.get("cost_reservation"),
        "canonical_memory": preview.get("canonical_memory"),
    },
}
print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

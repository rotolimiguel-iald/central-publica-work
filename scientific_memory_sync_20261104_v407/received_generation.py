"""Conferencia, em PROCESSO NOVO, da geracao que a fila recebe da memoria canonica ACTIVE (somente leitura; nao escreve nada em Chatgpt\\).
Uso: python received_generation.py PREPARATION_v407_<epoch>.json > RECEIVED_GENERATION.json"""
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
sys.path.insert(0, str(BASE))
sys.dont_write_bytecode = True
from iald_orchestrator import canonical_memory as cm  # noqa: E402

rep = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
active_raw = Path(cm.ACTIVE).read_bytes()
active = json.loads(active_raw)
manifest, fresh = cm.load(refresh=False)
out = {"active": active, "active_sha256": hashlib.sha256(active_raw).hexdigest(), "manifest_generation": manifest["generation"], "freshness": fresh,
       "esperado": {"epoch": rep["epoch"], "generation": rep["generation"], "release": rep["release"]}, "recuperacao": {}}
q = " ".join(rep["statute_record_names"])
for mode in ("standard", "maximum", "deepseek_maximum"):
    p = cm.prepare(q, None, allowed_sources=["um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md"], mode=mode, max_chars=24000)
    r = p["receipt"]
    out["recuperacao"][mode] = {"generation": r["generation"], "packet_sha256": r["packet_sha256"], "ok": r["generation"] == rep["generation"] and r["packet_sha256"] == cm.digest(p["prompt"].encode())}
out["ok"] = (active.get("epoch") == rep["epoch"] and active.get("generation") == rep["generation"] and manifest["generation"] == rep["generation"]
             and fresh == "SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED" and all(v["ok"] for v in out["recuperacao"].values()))
out["provider_calls"] = 0
print(json.dumps(out, ensure_ascii=False))

# -*- coding: utf-8 -*-
"""Medicoes do construtor (somente leitura; nao e revisao): o que o redesenho do pacote haiku55 mudou, lido dos artefatos."""
import hashlib
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
A = W / "app"
R = Path(r"C:\IALD\projetos_pyhton\IALD")
OLD = W.parent / "iald_v404_20261029"


def rd(p):
    return json.loads(Path(p).read_bytes())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def topic(text, name):
    i = text.index("\n### " + name + "\n")
    j = text.index("\n### ", i + 10)
    return text[i + 1:j]


inst = rd(R / ".iald_runtime/haiku55/native_count.json")["budget"]
out = {"status": "BUILDER_MEASUREMENTS_NOT_A_REVIEW", "release": rd(A / "RELEASE.json"), "installed_haiku55_v404": {
    "prefix_bytes": (R / ".iald_runtime/haiku55/prefix.md").stat().st_size, "permanent_tokens": inst["permanent_tokens"],
    "remaining_tokens": inst["remaining_tokens"]}, "packages_v405": {}}
for name in ("haiku_expanded", "shared", "sonnet_public"):
    p = A / "packages" / name
    b = rd(p / "native_count.json")["budget"]
    out["packages_v405"][name] = {"prefix_bytes": (p / "prefix.md").stat().st_size, "prefix_sha256": sha(p / "prefix.md"),
                                  "permanent_tokens": b["permanent_tokens"], "remaining_tokens": b["remaining_tokens"], "fits": b["fits"]}
binding = rd(A / "PREPARED_BINDING.json")
out["expanded_suffixes"] = binding["expanded_suffixes"]
out["shared_connector_bounds"] = binding["shared_connector_bounds"]
# Mesma formula da v404: janela - entrada - reserva - 4096; DeepSeek tambem com a reserva declarada da politica (148656).
win, margem = 1048576, 4096
out["executor_slack_bytes_with_finalize_reserve"] = {k: win - v["input_utf8_byte_bound"] - v["output_tokens"] - margem for k, v in binding["shared_connector_bounds"].items()}
out["deepseek_slack_bytes_with_declared_policy_reserve_148656"] = win - binding["shared_connector_bounds"]["deepseek"]["input_utf8_byte_bound"] - 148656 - margem

t404 = (R / ".iald_runtime/haiku55/prefix.md").read_text(encoding="utf-8")
t405 = (A / "packages/haiku_expanded/prefix.md").read_text(encoding="utf-8")
k404 = topic(t404, "kernel_formalization")
k405 = topic(t405, "kernel_formalization")
cap = json.loads(k405.split("\n")[2])
seal = rd(rd(A / "science/memory_stage/manifest_staged.json")["published_evidence"]["result"]["path"])
kf = seal["core"]["kernel_formalization"]
out["kernel_formalization"] = {
    "capsule_bytes_v404": len(k404.encode()), "capsule_bytes_v405": len(k405.encode()),
    "source_true_flags": sum(1 for v in kf.values() if v is True), "source_false_flags": sum(1 for v in kf.values() if v is False),
    "catalog": cap["AUDIT_BOOLEAN_FIELDS_IN_SOURCE"],
    "true_flags_kept_literal": sum(1 for v in cap.values() if v is True), "false_flags_kept_literal": sum(1 for v in cap.values() if v is False),
    "declaration_sources_items": len(kf["declaration_sources_v394"]),
}
names = re.findall(r"(?m)^### ([^\n]+)$", t405)
new = [n for n in seal["core"] if n.endswith("_v405")]
out["topics"] = {"core": len(seal["core"]), "new_v405": len(new), "all_present_in_prefix": set(seal["core"]) <= set(names)}
print(json.dumps(out, ensure_ascii=False, indent=1))
with (W / "BUILDER_MEASUREMENTS.json").open("x", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

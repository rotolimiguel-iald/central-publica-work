# -*- coding: utf-8 -*-
"""Medicoes do construtor (somente leitura; nao e revisao), parametrizadas por app/RELEASE.json: pacotes, folga da janela dos outros motores,
capsula do kernel_formalization e topicos novos, tudo lido dos artefatos. Reescrita na v406 (a da v405 trazia nomes de versao no codigo)."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
A = W / "app"
R = Path(r"C:\IALD\projetos_pyhton\IALD")


def rd(p):
    return json.loads(Path(p).read_bytes())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def topic(text, name):
    i = text.index("\n### " + name + "\n")
    j = text.index("\n### ", i + 10)
    return text[i + 1:j]


V = rd(A / "RELEASE.json")["release"]
built = rd(A / "BUILT.json")
ant = built["installed_release"]
inst = rd(R / ".iald_runtime/haiku55/native_count.json")["budget"]
out = {"status": "BUILDER_MEASUREMENTS_NOT_A_REVIEW", "release": rd(A / "RELEASE.json"), "installed_release": ant,
       "installed_haiku55": {"prefix_bytes": (R / ".iald_runtime/haiku55/prefix.md").stat().st_size, "permanent_tokens": inst["permanent_tokens"],
                             "remaining_tokens": inst["remaining_tokens"]}, "packages": {}}
for name in ("haiku_expanded", "shared", "sonnet_public"):
    p = A / "packages" / name
    b = rd(p / "native_count.json")["budget"]
    out["packages"][name] = {"prefix_bytes": (p / "prefix.md").stat().st_size, "prefix_sha256": sha(p / "prefix.md"),
                             "permanent_tokens": b["permanent_tokens"], "remaining_tokens": b["remaining_tokens"], "fits": b["fits"]}
binding = rd(A / "PREPARED_BINDING.json")
out["expanded_suffixes"] = binding["expanded_suffixes"]
out["p2_shared"] = rd(A / "packages/shared/preparation.json")["p2_shared"]
out["shared_connector_bounds"] = binding["shared_connector_bounds"]
# Mesma formula da v404/v405: janela - entrada - reserva - 4096; DeepSeek tambem com a reserva declarada da politica (148656).
win, margem = 1048576, 4096
out["executor_slack_bytes_with_finalize_reserve"] = {k: win - v["input_utf8_byte_bound"] - v["output_tokens"] - margem for k, v in binding["shared_connector_bounds"].items()}
out["slack_bytes_with_declared_policy_reserve_148656"] = {k: win - v["input_utf8_byte_bound"] - 148656 - margem for k, v in binding["shared_connector_bounds"].items()}
out["menor_folga_declarada_bytes"] = min(out["slack_bytes_with_declared_policy_reserve_148656"].values())

t_ant = (R / ".iald_runtime/haiku55/prefix.md").read_text(encoding="utf-8")
t_new = (A / "packages/haiku_expanded/prefix.md").read_text(encoding="utf-8")
k_ant = topic(t_ant, "kernel_formalization")
k_new = topic(t_new, "kernel_formalization")
cap = json.loads(k_new.split("\n")[2])
seal = rd(rd(A / "science/memory_stage/manifest_staged.json")["published_evidence"]["result"]["path"])
kf = seal["core"]["kernel_formalization"]
out["kernel_formalization"] = {
    "capsule_bytes_" + ant: len(k_ant.encode()), "capsule_bytes_" + V: len(k_new.encode()),
    "source_true_flags": sum(1 for v in kf.values() if v is True), "source_false_flags": sum(1 for v in kf.values() if v is False),
    "catalog": cap["AUDIT_BOOLEAN_FIELDS_IN_SOURCE"],
    "true_flags_kept_literal": sum(1 for v in cap.values() if v is True), "false_flags_kept_literal": sum(1 for v in cap.values() if v is False),
    "declaration_sources_items": len(kf.get("declaration_sources_v394", [])),
}
names = re.findall(r"(?m)^### ([^\n]+)$", t_new)
new = [n for n in seal["core"] if n.endswith("_" + V)]
out["topics"] = {"core": len(seal["core"]), "new_" + V: new, "all_present_in_prefix": set(seal["core"]) <= set(names)}
assert out["topics"]["all_present_in_prefix"]
history = rd(A/"D53_HISTORY.json")
out["d53"] = {
    "block_bytes_by_version": history["block_bytes_by_version"],
    "historical_topics_with_verified_fetch_span": len(history["spans"]),
    "fully_resident": history["resident"],
    "shared": rd(A/"D53_shared_VERIFIED.json"),
    "sonnet_public": rd(A/"D53_sonnet_public_VERIFIED.json"),
    "pre_history_shared_bytes": history["before_bytes"],
    "final_shared_bytes": (A/"packages/shared/prefix.md").stat().st_size,
}
assert out["menor_folga_declarada_bytes"] == min(
    row["slack"] for row in out["d53"]["shared"]["bounds_with_declared_reserve"].values())
for script, name in [("check_literais_v407_r2.py","inline_literals"),("measure_shared_capsules.py","legacy_capsules")]:
    out[name]=json.loads(subprocess.check_output([sys.executable,"-B","-X","utf8",str(W/script)], cwd=W))
assert out["inline_literals"]["limites_diz_nao_diz_inline_em_todos"]
caps=out["legacy_capsules"]
assert not caps["topics_lost"] and not caps["n_mismatches"] and caps["compact_capsules"]==caps["capsules_restored_equal_source"]
highlights=rd(A/"KERNEL_HIGHLIGHTS.json")
prefixes=[A/"packages"/name/"prefix.md" for name in out["packages"]]+[A/"native_prefix.md"]
out["kernel_statements_and_scope"]={}
for prefix in prefixes:
    text=prefix.read_text(encoding="utf8")
    assert all(anchor["statement"] in text for anchor in highlights["anchors"]) and highlights["scope"] in text
    out["kernel_statements_and_scope"][str(prefix.relative_to(A))]=len(highlights["anchors"])
sys.path.insert(0,str(R))
from iald_core_indexado import DocumentCorpus
corpus=DocumentCorpus(A/"science/memory_stage/manifest_staged.json")
out["public_fetch_samples"]=[]
for name in tuple(n for n in history["spans"] if n.endswith("_v407")):
    start,length=history["spans"][name]
    parts=[]
    for offset in range(start,start+length,4500):
        page=corpus.fetch(history["source"],offset,min(4500,start+length-offset))
        assert page["offset"]==offset and page["sha256"]==history["source_text_sha256"]
        parts.append(page["text"])
    assert json.loads("".join(parts))==seal["core"][name]
    out["public_fetch_samples"].append({"topic":name,"pages":len(parts),"characters":length})
counts=rd(A/"COUNT_PREFLIGHT.json")["requests"]
for row in counts:
    root=A/"packages"/row["package"]
    intent=root/(row["phase"]+"_count_intent.json")
    returned=rd(root/(row["phase"]+"_count_result.json"))
    assert rd(intent)["request_sha256"]==row["request_sha256"] and rd(intent)["generation"] is False
    assert returned["intent_sha256"]==sha(intent) and returned["input_tokens"]>0
assert len(counts)==rd(A/"NATIVE_COUNTS_COMPLETE.json")["public_count_requests"]==6
out["native_counts"]={"verified_intents_and_results":len(counts),"generation":0,"receipt":sha(A/"NATIVE_COUNTS_COMPLETE.json")}
out["counter_initialization"]="SDK-compatible httpx2 inherited; see current v409 intent/result receipts, not historical failures."
print(json.dumps(out, ensure_ascii=False, indent=1))
with (W / "BUILDER_MEASUREMENTS.json").open("x", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

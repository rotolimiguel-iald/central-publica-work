"""Compare the installed sentence signature with exact identity on synthetic corrections.

The fixed byte cap is charged to retained text in both variants. This tests the
deduplication decision only; ranking and checkpoint reconstruction are separate.
"""
import ast
import hashlib
import json
from pathlib import Path
import re

SOURCE = Path(r"C:\IALD\projetos_pyhton\IALD\holographic_memory.py")
OUTPUT = Path(__file__).with_name("MEMORY_SIGNATURE_COMPARISON.json")


def read_signature():
    raw = SOURCE.read_bytes()
    tree = ast.parse(raw)
    nodes = [node for node in ast.walk(tree)
             if isinstance(node, ast.FunctionDef) and node.name == "_sentence_signature"]
    if len(nodes) != 1:
        raise ValueError("Expected one installed sentence signature implementation")
    # This routine requires only re and str; avoid importing the application's state.
    isolated = ast.Module(body=nodes, type_ignores=[])
    namespace = {"re": re}
    exec(compile(isolated, str(SOURCE), "exec"), namespace)
    return namespace["_sentence_signature"], hashlib.sha256(raw).hexdigest()


def compare(rows, signature, byte_limit):
    prior = set()
    kept = []
    used = 0
    for partition, sentence in rows:
        key = partition, signature(sentence)
        size = len(sentence.encode("utf-8"))
        if key in prior or used + size > byte_limit:
            continue
        prior.add(key)
        kept.append((partition, sentence))
        used += size
    return {"identities_retained": len(kept), "utf8_bytes": used,
            "missing": [r for r in dict.fromkeys(rows) if r not in kept]}


def main():
    installed, module_hash = read_signature()
    initial = [
        "O valor medido com o mesmo instrumento foi 3.50.",
        "O operador encerrou a coleta da amostra no turno 17.",
        "A leitura do documento de referência da série experimental produz o seguinte estado ao final da verificação: ativo.",
        "Para o cálculo use H.",
    ]
    updated = [initial[0].replace("3.50", "3.75"), initial[1].replace("17", "18"),
               initial[2].replace("ativo.", "revogado."), initial[3].replace(" H.", " h.")]
    rows = [(scope, sentence) for scope, sentences in
            [("fixture-a", initial), ("fixture-a", updated), ("fixture-a", initial),
             ("fixture-b", initial[:1])] for sentence in sentences]
    distinct = list(dict.fromkeys(rows))
    full_budget = sum(len(sentence.encode("utf-8")) for _, sentence in distinct)
    result = {"source_sha256": module_hash, "observations": len(rows),
              "distinct_by_scope_and_bytes": len(distinct), "scope": "synthetic_dedup_only", "budgets": {}}
    for byte_limit in (full_budget, full_budget // 2):
        result["budgets"][byte_limit] = {
            "installed_signature": compare(rows, lambda s: installed(None, s), byte_limit),
            "exact_text": compare(rows, lambda s: s, byte_limit),
        }
    assert not result["budgets"][full_budget]["exact_text"]["missing"]
    assert len(result["budgets"][full_budget]["installed_signature"]["missing"]) == 4
    with OUTPUT.open("x", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    for limit, variants in result["budgets"].items():
        print(limit, {name: v["identities_retained"] for name, v in variants.items()})


if __name__ == "__main__":
    main()

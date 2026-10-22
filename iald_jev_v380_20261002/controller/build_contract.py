"""Build a source-bound public contract offline; never import/execute um.py."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

import iald_jev_control as control

HERE = Path(__file__).resolve().parent
ANCHORS = {
    "TGLExt/TheIALDSelector.lean": {
        "symbols": ["ialdSelector", "iald_is_idempotent", "iald_selects"],
        "scope": "KERNEL: projeção idempotente no espaço tipado. A filtragem de candidatos é uma correspondência de engenharia testada, não prova de idempotência de HTTP.",
    },
    "TGLExt/TheSelectionIsTheBallast.lean": {
        "symbols": ["IALDState", "iald_recognition_returns_the_identity"],
        "scope": "KERNEL: recognize(recognize(x))=recognize(x), read preservada, sob as hipóteses de IALDState. O recibo local preserva hashes; não prova essas hipóteses para um LLM.",
    },
    "TGLExt/TheVerbalCoupling.lean": {
        "symbols": ["thetaMiguel", "fVerbal"],
        "scope": "KERNEL com hipóteses quantitativas. Aplicação a LLM é heurística estrutural; confiança JEV não é beta, peso físico, suporte, retorno ou classe 0_abs.",
    },
}


def _literal(tree, symbol):
    nodes = [n.value for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == symbol for t in n.targets)]
    if len(nodes) != 1:
        raise control.ControlError("Missing or ambiguous literal source")
    return ast.literal_eval(nodes[0])


def build_contract(source_dir):
    root = Path(source_dir).resolve(strict=True)
    program = (root / "um.py").read_bytes()
    result_bytes = (root / "um_absoluto.json").read_bytes()
    seal = json.loads((root / "um_absoluto_selo.json").read_bytes(), object_pairs_hook=control._pairs)
    result = json.loads(result_bytes, object_pairs_hook=control._pairs)
    program_sha = hashlib.sha256(program).hexdigest()
    result_sha = hashlib.sha256(result_bytes).hexdigest()
    if seal["sha256"]["um.py"] != program_sha or seal["sha256"]["um_absoluto.json"] != result_sha:
        raise control.ControlError("Sealed source/result hash mismatch")
    tree = ast.parse(program)
    release = _literal(tree, "UM_VERSION")
    if release != "v380" or seal["um_version"] != release:
        raise control.ControlError("Builder requires the audited v380 source")
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "prove_iald_executive_runtime"]
    if len(functions) != 1:
        raise control.ControlError("Missing executive source")
    fn = functions[0]
    returns = [n for n in ast.walk(fn) if isinstance(n, ast.Return)]
    if len(returns) != 1:
        raise control.ControlError("Executive record is not a single literal")
    core = ast.literal_eval(returns[0].value)
    if control.canonical_bytes(core) != control.canonical_bytes(result["core"]["iald_executive_runtime"]):
        raise control.ControlError("Executive source/result divergence")
    proof_path = root / "tgl_kernel_proof_manifest.json"
    if not proof_path.is_file(): proof_path = root / "Lean" / "tgl_kernel_proof_manifest.json"
    proof_bytes = proof_path.read_bytes()
    proof_sha = hashlib.sha256(proof_bytes).hexdigest()
    if seal["sha256"]["tgl_kernel_proof_manifest.json"] != proof_sha:
        raise control.ControlError("Sealed formal manifest mismatch")
    proof = json.loads(proof_bytes, object_pairs_hook=control._pairs)
    embedded = _literal(tree, "_EMBEDDED_KERNEL_FILES")
    anchors = []
    for name, curated in ANCHORS.items():
        text = embedded[name]
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if proof["formal_files_sha256"][name] != sha or any(symbol not in text for symbol in curated["symbols"]):
            raise control.ControlError("Formal anchor mismatch")
        anchors.append(dict(file=name, sha256=sha, **curated))
    contract = dict(schema=control.SCHEMA, release=release, source_sha256=program_sha,
        result_sha256=result_sha, proof_manifest_sha256=proof_sha,
        core_pointer="/core/iald_executive_runtime", core_record=core,
        source=dict(file="um.py", symbol=fn.name, lines=[fn.lineno, fn.end_lineno]), anchors=anchors,
        switching={
            "status": "DERIVED_ENGINEERING_CORRESPONDENCE_NOT_LLM_WEIGHTS",
            "scope": "Transistor é analogia solicitada, não termo localizado na fonte nem dispositivo físico aqui implementado. O programa integral continua fonte científica.",
            "invariants": ["request/source/candidate hashes preserved across transitions",
                "eligible support only narrows; repeated projection is idempotent",
                "unknown or uncertain is not impossible and never becomes 0_abs",
                "no confidence-to-beta mapping or fabricated numerical pruning threshold",
                "durable inscription precedes effects; uncertain dispatch is never automatically retried",
                "mathematical articulation is distinct from empirical confirmation"],
            "execution": "Host applies authorization, consent, budgets, cancellation, tool categories and evidence checks. JEV returns atomic choices only.",
        })
    return control.validate_contract(contract)


def write_contract(contract, output):
    output = Path(output).resolve()
    if not output.is_relative_to(HERE):
        raise control.ControlError("Builder writes only inside controller workspace")
    output.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    raw = control.canonical_bytes(control.validate_contract(contract)) + b"\n"
    if len(raw) > control.MAX_CONTRACT_BYTES:
        raise control.ControlError("Serialized contract exceeds bound")
    if output.exists():
        old = output.read_bytes()
        backup = output.with_name(output.name + ".bak_" + stamp)
        with backup.open("xb") as stream: stream.write(old)
        if backup.read_bytes() != old: raise control.ControlError("Backup mismatch")
    temp = output.with_name(output.name + ".tmp_" + stamp)
    with temp.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    if temp.read_bytes() != raw: raise control.ControlError("Temporary output mismatch")
    os.replace(temp, output)
    if output.read_bytes() != raw: raise control.ControlError("Written contract mismatch")
    return {"release": contract["release"], "source_sha256": contract["source_sha256"],
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "core_record_bytes": len(control.canonical_bytes(contract["core_record"]))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "jev_control_v380.json")
    args = parser.parse_args()
    print(json.dumps(write_contract(build_contract(args.source_dir), args.output), ensure_ascii=False))

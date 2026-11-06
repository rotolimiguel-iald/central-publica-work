"""Read the complete atlas and verify the scientific inputs of the specified staging snapshot."""
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path("C:/IALD")
CENTRAL = ROOT / "Central de Patentes"
STAGE = CENTRAL / "work/cadeia_de_selo/v409"
NOS = ROOT / "Artigo/Haja_Luz/A Ponte e o Um/Nós"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def main():
    raw = (CENTRAL / "memory/TGL_ATLAS.md").read_bytes()
    lines = raw.decode("utf-8").splitlines()
    start = next(i for i, s in enumerate(lines) if s.startswith("## II. DICIONÁRIO"))
    end = next(i for i, s in enumerate(lines[start:], start) if s.startswith("## III. AS PEDRAS"))
    heads = [s for s in lines if re.match(r"^## (I{1,3}|IV|V|VI{1,3}|IX|X|XI|XII)\.", s)]
    pattern = r"^\*\*[^*]+\*\*\s*[—–-]"
    manifest = read_json(STAGE / "MANIFESTO_INSUMOS_v409.json")
    inputs = {}
    for name, entry in manifest.items():
        local = (STAGE / "insumos" / name).resolve()
        if not local.is_relative_to((STAGE / "insumos").resolve()):
            raise ValueError("Insumo fora do manifesto local")
        data = local.read_bytes()
        if digest(data) != entry["sha256"] or len(data) != entry["bytes"]:
            raise ValueError(f"Insumo divergente: {name}")
        inputs[name] = digest(data)
    seal = read_json(NOS / "um_absoluto_selo.json")
    live = digest((NOS / "um.py").read_bytes())
    if live != seal["sha256"]["um.py"]:
        raise ValueError("Selo e programa vivo divergiram")
    cand = read_json(STAGE / "CANDIDATO_v409.json")
    staged = Path(cand["candidato"]).read_bytes()
    if digest(staged) != cand["sha256"] or cand["base_v408_sha16"] != live[:16]:
        raise ValueError("Base ou candidato divergente")
    post = read_json(STAGE / "kernel/POS_BUILD_v409.json")
    kernel = read_json(STAGE / "kernel/KERNEL_RECIBO_v409.json")
    for log in [kernel["build_full_log"], kernel["audit_log"]]:
        if digest(Path(log["path"]).read_bytes()) != log["sha256"]:
            raise ValueError("Log de compilação ou auditoria divergente")
    ready = read_json(STAGE / "PREPARACAO_v409_PRONTA.json")
    print(json.dumps({
        "when": datetime.now().astimezone().isoformat(timespec="seconds"),
        "atlas": {"bytes": len(raw), "lines": len(lines), "sha256": digest(raw),
                  "section_headers": heads, "entry_line_pattern": pattern,
                  "entry_lines_section_II": sum(bool(re.match(pattern, s)) for s in lines[start:end])},
        "seal": {"version": seal["um_version"], "timestamp": seal["timestamp"],
                 "program_sha256": live, "world_hash": seal["result_hash"]},
        "staging": {"version": "v409", "candidate_sha256": digest(staged), "candidate_bytes": len(staged),
                    "input_manifest_sha256": digest((STAGE / "MANIFESTO_INSUMOS_v409.json").read_bytes()),
                    "inputs_sha256": inputs, "flags_added": cand["n_bandeiras"], "ladder": cand["escada"],
                    "modules": [p["path"] for p in kernel["pedras"]], "kernel_rc": kernel["rc"],
                    "post_build_ok": post["ok"], "core_criteria": post["criterios"],
                    "readiness_receipt": {"stamp": ready["quando"], "ready": ready["pronta"],
                                          "candidate_sha256": ready["candidato_sha256"],
                                          "applies_to_measured_candidate": ready["candidato_sha256"] == cand["sha256"]}}
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

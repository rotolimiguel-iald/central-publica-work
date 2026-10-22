"""Snapshot two v329 sources and transpose import paths only for the isolated bench."""
from pathlib import Path
import hashlib, json, os, re, sys
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
KERNEL = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
def record(path):
    raw = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
def new(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(path)
def main():
    assert not (ROOT / "CONTINUACAO045_UPSTREAM.json").exists()
    files = [record(Path(__file__).resolve())]
    items = []
    mapping = {"TGLExt.PeriodicCentralizerExpectation": "PeriodicCentralizerExpectation",
               "TGLExt.TracialCentralizerExpectation": "TracialCentralizerExpectation",
               "TGLExt.ModularPower": "ModularPower"}
    for name in ["TheLiftFiresOnThePeriodicTower", "TheModularFlowIsAHorizon"]:
        origin = KERNEL / "TGLExt" / (name + ".lean")
        raw = origin.read_bytes()
        snapshot = ROOT / "CONTINUACAO045_UPSTREAM" / "TGLExt" / (name + ".lean")
        new(snapshot, raw)
        text = raw.decode("utf-8-sig")
        changes = []
        for before, after in mapping.items():
            old = "import " + before
            if re.search(r"(?m)^" + re.escape(old) + r"\s*$", text):
                text = re.sub(r"(?m)^" + re.escape(old) + r"(?=\s*$)", "import " + after, text)
                changes.append({"from": before, "to": after})
        declarations = re.findall(r"(?m)^(?:theorem|lemma|def|abbrev|structure)\s+([\w.]+)", text)
        printed = re.findall(r"(?m)^#print\s+axioms\s+([\w.]+)", text)
        missing = [name for name in declarations if name not in printed]
        ending = re.search(r"(?m)^end\s*\r?\nend TGLExt\s*$", text)
        assert ending and len(declarations) == len(set(declarations))
        text = text[:ending.start()] + "\n".join("#print axioms " + name for name in missing) + "\n" + text[ending.start():]
        destination = ROOT / "TGLExt" / (name + ".lean")
        adapted = text.encode("utf-8")
        new(destination, adapted)
        assert origin.read_bytes() == raw
        def body(data):
            return re.sub(r"(?m)^(?:import\s+[^\n]+|#print\s+axioms\s+[^\n]+)\r?\n?", "", data.decode("utf-8-sig")).replace("\r\n", "\n").strip()
        assert [line for line in body(raw).splitlines() if line.strip()] == [line for line in body(adapted).splitlines() if line.strip()], "Proof body changed"
        rows = [record(origin), record(snapshot), record(destination)]
        files.extend(rows)
        items.append({"module": "TGLExt." + name, "origin": rows[0], "snapshot": rows[1], "adapted": rows[2],
                      "import_transpositions": changes, "added_axiom_prints": missing, "proof_body_unchanged": True})
    result = {"schema": "chatgpt.upstream045.v1", "created_utc": datetime.now(timezone.utc).isoformat(),
              "items": items, "files": files,
              "status": "READ_AND_TRANSPOSED_NOT_YET_COMPILED",
              "limitation": "Current source snapshot; no claim that a prior canonical seal was revalidated."}
    new(ROOT / "CONTINUACAO045_UPSTREAM.json", (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"status": result["status"], "items": items}, ensure_ascii=True))
if __name__ == "__main__":
    main()

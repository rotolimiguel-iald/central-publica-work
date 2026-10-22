"""Create a read-only audit snapshot and a new reexamination; never import/run um.py."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
SPECS = [
    ("SELETOR_BORN_REGISTRO_20260909", "CanonicalSelectorBorn", "BUILD_20260909_172830_186727"),
    ("SELETOR_BORN_REGISTRO_20260909", "SelectorRecordReconstruction", "BUILD_20260909_173235_708731"),
    ("ENTRELACAMENTO_SELETOR_20260909_172718_478310", "AngularSelectorIntertwining", "BUILD_20260909_173327_687034"),
    ("ENTRELACAMENTO_SELETOR_20260909_172718_478310", "RelativePhaseCharacter", "BUILD_20260909_173940_076834"),
    ("LOCALIDADE_EXTENSIVA_20260909_172820_609568", "BondLocalityEstimates", "BUILD_20260909_173338_542415"),
]

def rec(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def new(path, raw):
    assert path.resolve().is_relative_to(BASE) and not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw

def main():
    canon = rec(CANON)
    assert canon["bytes"] == 9860115 and canon["sha256"] == "e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303", "Canonical version changed; reexamine first."
    modules = []
    for folder, name, build in SPECS:
        source = BASE / folder / (name + ".lean")
        receipt = BASE / folder / build / "BUILD_RESULT.json"
        data = json.loads(receipt.read_text(encoding="utf-8"))
        pin = rec(source)
        assert data["status"] == "PASS_COMPILED_SCOPE" and pin in data["sources"]
        text = source.read_text(encoding="utf-8")
        defs = re.findall(r"(?m)^(?:noncomputable\s+)?(theorem|def|abbrev|structure)\s+(\w+)", text)
        prints = re.findall(r"(?m)^#print axioms (\w+)$", text)
        assert len(prints) == len(defs) and set(prints) == {name for _, name in defs}
        assert all(set(row["axioms"]) <= TRIO for row in data["axiom_rows"])
        assert len(data["axiom_rows"]) == len(defs)
        anchors = {name: text[:match.start()].count("\n") + 1
                   for match in re.finditer(r"(?m)^(?:noncomputable\s+)?(?:theorem|def|abbrev|structure)\s+(\w+)", text)
                   for name in [match.group(1)]}
        modules.append({"module": name, "source": pin, "receipt": rec(receipt),
                        "theorems": sum(kind == "theorem" for kind, _ in defs),
                        "other_declarations": sum(kind != "theorem" for kind, _ in defs),
                        "anchors": anchors})
    assert sum(m["theorems"] for m in modules) == 93
    assert sum(m["other_declarations"] for m in modules) == 29
    outcome = {"status": "PASS_FIVE_SOURCE_RECEIPTS__JOINT_BUILD_SEPARATE", "created_utc": datetime.now(timezone.utc).isoformat(),
               "canonical": canon, "modules": modules, "theorems": 93, "other_declarations": 29,
               "axiom_terms": 122, "canonical_modified": False, "um_py_executed_or_imported": False}
    assert rec(CANON) == canon
    new(OUT / "INVENTARIO_CINCO_FONTES.json", (json.dumps(outcome, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"status": outcome["status"], "modules": 5, "theorems": 93, "other_declarations": 29}))

if __name__ == "__main__":
    main()

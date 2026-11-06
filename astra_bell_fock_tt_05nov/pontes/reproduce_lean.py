"""Recompile the candidate against the staged v409 and audit every theorem."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
DEFAULT_PROJECT = Path("C:/t/k409c/final")
LAKE = Path("C:/Users/rotol/.elan/bin/lake.exe")
SOURCE = HERE / "AstraBellFockTT.lean"
PREFIX = "TGL.Candidate.AstraBellFockTT."
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def pin(path):
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    log = args.out / "AUDIT.log"
    receipt = args.out / "RECIBO_PONTES.json"
    if log.exists() or receipt.exists():
        parser.error("Use a new output directory to preserve earlier receipts.")
    env = dict(os.environ, GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="safe.directory",
               GIT_CONFIG_VALUE_0="*")
    command = [str(LAKE), "env", "lean", str(SOURCE)]
    run = subprocess.run(command, cwd=args.project, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, check=False)
    with log.open("xb") as output:
        output.write(run.stdout)
    content = run.stdout.decode("utf-8")
    source = SOURCE.read_text(encoding="utf-8")
    names = [PREFIX + name for name in re.findall(r"^theorem (\w+)", source, re.M)]
    prints = re.findall(r"^#print axioms ([\w.]+)", source, re.M)
    reports = re.findall(r"'([\w.]+)' depends on axioms:\s*\[([^\]]*)\]", content)
    audited = {name: sorted(x.strip() for x in ax.split(",")) for name, ax in reports}
    valid = (run.returncode == 0 and len(audited) == len(reports) == len(names)
             and set(audited) == set(names) == set(prints)
             and all(set(ax) <= TRIO for ax in audited.values())
             and "sorryAx" not in content)
    reference = Path("C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/insumos/ParNaFaceDeFock.lean")
    modules = ["ParNaFaceDeFock", "LinearizedSpin2", "F1Fecho394/CreationAndSegalR2",
               "F1Fecho394/ExponentialVectorsR3"]
    data = {
        "time_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if valid else "FAIL",
        "cwd": str(args.project), "command": command, "exit_code": run.returncode,
        "lean_toolchain": (args.project / "lean-toolchain").read_text().strip(),
        "candidate": pin(SOURCE), "log": pin(log), "theorems": audited, "input_v409": pin(reference),
        "staged_imports": [pin(args.project / "TGLExt" / (name + ".lean")) for name in modules],
        "oleans": [pin(args.project / ".lake/build/lib/lean/TGLExt" / (name + ".olean"))
                   for name in modules],
        "scope": "Standalone candidate; existing staged imports; no physical observation or sealing."
    }
    with receipt.open("x", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
        output.write("\n")
    print(json.dumps({"status": data["status"], "theorem_count": len(audited), "receipt": str(receipt)}))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

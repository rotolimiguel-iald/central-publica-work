"""Confira o log da recompilação e a tabela de pinos da fonte do handoff."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re


OUT = Path(__file__).resolve().parent
WORK = OUT.parents[1]
CENTRAL = WORK.parent
KERNEL = CENTRAL.parent / "Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
ORIGIN = WORK / "pedras_candidatas_05nov"
PREFIX = "TGLExt.BellEspelhamento."
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exit-code", type=int, required=True,
                        help="Código real do processo lake env lean.")
    parser.add_argument("--lean-version", required=True,
                        help="Saída de lake env lean --version no mesmo ambiente.")
    args = parser.parse_args()
    handoff = ORIGIN / "HANDOFF_ASTRA_BELL_FOCK_TT_05nov.md"
    text = handoff.read_text(encoding="utf-8-sig")
    pins = []
    for relative, expected in re.findall(r"^\| `(work\\[^`]+)` \| `([a-f0-9]{64})` \|$", text, re.M):
        path = CENTRAL / relative
        actual = sha(path)
        pins.append(dict(path=str(path), sha_expected=expected, sha_measured=actual,
                         match=(actual == expected)))
    source = ORIGIN / "BellEspelhamentoR1.lean"
    src = source.read_text(encoding="utf-8-sig")
    decls = {m[1]: src.count("\n", 0, m.start()) + 1
             for m in re.finditer(r"^(?:lemma|theorem) (\w+)", src, re.M)}
    commands = re.findall(r"^#print axioms TGLExt\.BellEspelhamento\.(\w+)", src, re.M)
    log = OUT / "BellEspelhamentoR1_recompilacao.log"
    output = log.read_text(encoding="utf-8-sig")
    reports = re.findall(r"^'TGLExt\.BellEspelhamento\.(\w+)' depends on axioms: \[([^\]]+)\]",
                         output, re.M)
    rows = {name: {"source_line": decls.get(name),
                   "axioms": [part.strip() for part in axioms.split(",")]}
            for name, axioms in reports}
    review = OUT / "AUDITORIA_ENUNCIADOS.md"
    audited = re.findall(r"^\| `(\w+)` \|", review.read_text(encoding="utf-8"), re.M)
    manifest = json.loads((KERNEL / "lake-manifest.json").read_text(encoding="utf-8-sig"))
    mathlib = next(pkg for pkg in manifest["packages"] if pkg["name"] == "mathlib")
    checks = {
        "pins": len(pins) == 7 and all(row["match"] for row in pins),
        "returncode": args.exit_code == 0,
        "declarations": len(decls) == len(commands) == len(reports) == len(audited) == 23,
        "coverage": set(decls) == set(commands) == set(rows) == set(audited),
        "axioms": all(set(r["axioms"]) <= TRIO for r in rows.values()),
        "no_sorry_ax": "sorryAx" not in output,
        "no_compiler_error": re.search(r": error:", output) is None,
    }
    receipt = {
        "status": "RECOMPILADA_E_CONFERIDA" if all(checks.values()) else "FALHA_DE_CONFERENCIA",
        "generated_at": datetime.now().astimezone().isoformat(),
        "command": [r"C:\Users\rotol\.elan\bin\lake.exe", "env", "lean", str(source)],
        "cwd": str(KERNEL), "returncode": args.exit_code, "lean_version": args.lean_version,
        "mathlib_manifest": {"input_revision": mathlib["inputRev"], "revision": mathlib["rev"]},
        "scope": "Reprocessamento integral da candidata, com dependências já compiladas. "
                 "As inferências físicas são discutidas separadamente.",
        "handoff_sha256": sha(handoff), "pins": pins, "declarations": rows, "checks": checks,
        "warnings": len(re.findall(r": warning:", output)),
        "log": {"path": str(log), "bytes": log.stat().st_size, "sha256": sha(log)},
        "review": {"path": str(review), "sha256": sha(review)},
        "verification_script_sha256": sha(Path(__file__)),
    }
    destination = OUT / "RECIBO_AUDITORIA_R1.json"
    with destination.open("x", encoding="utf-8") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({"status": receipt["status"], "checks": checks,
                      "sha256": sha(destination)}, ensure_ascii=False))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

"""Freeze a reviewed, additive Lean-source configuration. Never execute um.py."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
PRIOR = BASE / "COPIA_INTEGRADA_20260909_150458_780534"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
DECLARATION = re.compile(
    r"(?m)^(?:local\s+)?(?:noncomputable\s+)?"
    r"(abbrev|def|structure|theorem|instance)\s+(\w+)"
)


def record(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path, data):
    assert path.resolve().is_relative_to(BASE) and not path.exists()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.rename(temp, path)
    assert path.read_bytes() == data


def verified_item(source, receipt_path):
    source_record = record(source)
    proof = read(receipt_path)
    assert proof["status"] == "PASS_COMPILED_SCOPE", receipt_path
    assert source_record in proof["sources"], source
    assert all(run["exit_code"] == 0 for run in proof["runs"])
    assert all(set(row["axioms"]) <= TRIO for row in proof["axiom_rows"])
    assert (receipt_path.parent / source.name).read_bytes() == source.read_bytes()
    return {"source": source_record["path"], "sha256": source_record["sha256"],
            "build_result": receipt_path.as_posix(),
            "build_result_sha256": record(receipt_path)["sha256"]}


def main():
    prior_config = read(PRIOR / "CONFIG_APROVADA.json")
    canonical = Path(prior_config["source_um"])
    before = record(canonical)
    assert before["sha256"] == prior_config["source_um_sha256"], "Canonical advanced; rebase required."
    modules = []
    for item in prior_config["modules"]:
        assert record(Path(item["source"]))["sha256"] == item["sha256"]
        assert record(Path(item["build_result"]))["sha256"] == item["build_result_sha256"]
        modules.append(verified_item(Path(item["source"]), Path(item["build_result"])))
    assert len(modules) == 45
    groups = {
        "ORBITA_MODULAR_INTERACAO_20260909_153209_543141": ["SummableInteractionModularOrbit"],
        "DUHAMEL_UNITARIO_20260909_153247_640286": ["UnitaryDuhamel", "BoundedPerturbationCocycle",
            "SpectatorCancellation", "PauliInteractionCocycle", "PauliCocycleGenerator"],
        "HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430": ["FiniteModularHamiltonian",
            "FiniteLevelExponentials"],
        "LIMITE_COCICLO_NORMA_20260909_154449_009717": ["CocycleNormLimit"],
        "DERIVADA_LIMITE_COCICLO_20260909_155045_687120": ["DerivativeFromLinearCutoffError",
            "CanonicalCocycleDerivative"],
        "DINAMICA_MODULAR_PERTURBADA_20260909_155658_929243": ["PauliPerturbedDynamics"],
        "COORDENADAS_FINITAS_20260909_153310_253904": ["FiniteCoordinateMap", "FiniteLeviCivita",
            "FiniteCurvatureAlgebra", "FiniteCoordinateCurvature", "FiniteRicciContraction",
            "FiniteEinsteinNaturality"],
    }
    fresh = []
    for folder, names in groups.items():
        for name in names:
            source = BASE / folder / (name + ".lean")
            pin = record(source)
            matches = []
            for candidate in source.parent.glob("BUILD_*/BUILD_RESULT.json"):
                proof = read(candidate)
                if proof.get("status") == "PASS_COMPILED_SCOPE" and pin in proof.get("sources", []):
                    matches.append(candidate)
            assert matches, "No matching PASS receipt: " + str(source)
            item = verified_item(source, sorted(matches)[-1])
            fresh.append(item)
            modules.append(item)
    assert len(fresh) == 18
    assert len({item["source"] for item in modules}) == len(modules)
    counts = {"total": {"modules": len(modules), "theorems": 0, "other_declarations": 0},
              "new_this_continuation": {"modules": len(fresh), "theorems": 0, "other_declarations": 0}}
    details = []
    for item in modules:
        text = Path(item["source"]).read_text(encoding="utf-8")
        declarations = DECLARATION.findall(text)
        prints = re.findall(r"(?m)^#print axioms (\w+)$", text)
        assert len(prints) == len(set(prints)) == len(declarations)
        assert set(prints) == {name for _, name in declarations}
        nt = sum(kind == "theorem" for kind, _ in declarations)
        no = len(declarations) - nt
        for scope in ["total"] + (["new_this_continuation"] if item in fresh else []):
            counts[scope]["theorems"] += nt
            counts[scope]["other_declarations"] += no
        details.append({**item, "theorems": nt, "other_declarations": no,
                        "new_this_continuation": item in fresh})
    assert before == record(canonical)
    config = {
        "root_confirmed": True,
        "approval_basis": "Fontes congeladas com PASS e revisão semântica independente na sessão. Somente nova cópia em Chatgpt; nenhum um.py será executado ou importado.",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_um": canonical.as_posix(), "source_um_sha256": before["sha256"],
        "modules": modules, "prior_integrated_copy": record(PRIOR / "um.py"),
        "measured_counts": counts,
        "scope": "Additive embedded Lean source integration, imports and audit only. No new runtime flags, gate changes, empirical run or seal.",
    }
    config_path = OUT / "CONFIG_COCICLO_COVARIANCIA.json"
    write_new(config_path, (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    inventory = {"status": "FROZEN_INDIVIDUAL_PASS_SCOPES", "canonical": before,
                 "counts": counts, "modules": details, "configuration": record(config_path)}
    write_new(OUT / "INVENTARIO_FONTES.json",
              (json.dumps(inventory, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"configuration": config_path.as_posix(), "counts": counts}))


if __name__ == "__main__":
    main()

"""Read-only documentary checks and pins; write one new review manifest."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
NORMAL = ROOT / "NORMALIDADE_RELATIVA_070_20260909_233414"
RG = ROOT / "REDUCAO_ON_SHELL_RG_070_20260909_232623_681687"

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(raw), "lines": len(raw.splitlines()), "sha256": hashlib.sha256(raw).hexdigest()}

report = ROOT / "REEXAME_SUFICIENCIA_070_20260909" / "REEXAME_SUFICIENCIA.md"
inputs = [
    report,
    ROOT / "REEXAME_SUFICIENCIA_070_20260909" / "ESTADO_CANONICO_070.json",
    NORMAL / "NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md",
    NORMAL / "MANIFESTO_NORMALIDADE_RELATIVA.json",
    RG / "REDUCAO_EFT_E_FLUXO_LOGARITMICO.md",
    RG / "VERIFICACAO_REDUCAO_RG.json",
    RG / "verify_on_shell_rg.py",
    ROOT / "TOPOLOGIA_BRST_SIGMA_070_20260909_233042_647697" / "TOPOLOGIA_ALVO_E_REDUCAO_H1.md",
    ROOT / "EQUIVALENCIA_BV_METRICA_VIELBEIN_070_20260909" / "REVISAO_NORMALIDADE_E_REDUCIBILIDADE.md",
]
before = [pin(p) for p in inputs]
receipt = json.loads((RG / "VERIFICACAO_REDUCAO_RG.json").read_bytes())
normal_manifest = json.loads((NORMAL / "MANIFESTO_NORMALIDADE_RELATIVA.json").read_bytes())
checks = receipt["checks"]
documentary_checks = {
    "receipt_check_count_matches_length": receipt["check_count"] == len(checks) == 16,
    "receipt_all_passed": all(c["passed"] is True for c in checks),
    "receipt_all_residuals_zero": all(c["residual"] == "0" for c in checks),
    "receipt_explicit_not_lean": "NOT_LEAN" in receipt["status"],
    "RG_script_bytes_match_receipt": pin(RG / "verify_on_shell_rg.py")["bytes"] == receipt["script"]["bytes"],
    "RG_script_sha256_matches_receipt": pin(RG / "verify_on_shell_rg.py")["sha256"] == receipt["script"]["sha256"],
    "frozen_normality_note_matches_prior_pin": pin(NORMAL / "NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md")["sha256"] == normal_manifest["note"]["sha256"],
}
after = [pin(p) for p in inputs]
documentary_checks["read_inputs_stable_during_check"] = before == after
if not all(documentary_checks.values()):
    raise RuntimeError(json.dumps(documentary_checks, ensure_ascii=False))
manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Revisao documental propria da entrega070: formal/suave, H4_2 versus H2_char_cov, recibo16CAS, sinaisRG e pendencias.",
    "result": "NO_MATERIAL_DOCUMENTARY_ERROR_FOUND_IN_REQUESTED_SCOPE",
    "review": pin(BASE / "PARECER_REEXAME_070.md"),
    "new_notation_addendum": pin(NORMAL / "PRECISAO_HESSIANO_SIGMA.md"),
    "measurement_script": pin(Path(__file__)),
    "read_only_inputs": before,
    "documentary_checks": documentary_checks,
    "observed_RG_receipt": {"status": receipt["status"], "check_count": receipt["check_count"], "sympy_version": receipt["sympy_version"]},
    "execution_limits": {
        "CAS_rerun": False,
        "Lean_rerun": False,
        "um_import_or_execution": False,
        "audit069_rerun": False,
        "canonical_originals_remeasured_by_this_script": False,
        "python_standard_library_document_measurement": True,
    },
    "frozen_files_modified": False,
    "interpretation": "Os controles documentais medem recibos e pins; nao repetem provas simbolicas nem representam aprovacao em nome de terceiros.",
}
target = BASE / "MANIFESTO_REVISAO_DOCUMENTAL_070.json"
temp = BASE / "MANIFESTO_REVISAO_DOCUMENTAL_070.json.tmp_new"
if target.exists() or temp.exists():
    raise FileExistsError("Refusing to overwrite")
raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
with temp.open("xb") as stream:
    stream.write(raw)
    stream.flush()
    os.fsync(stream.fileno())
if not raw or temp.read_bytes() != raw:
    raise RuntimeError("Temporary bytes do not match")
temp.rename(target)
print(json.dumps({"review": manifest["review"], "addendum": manifest["new_notation_addendum"], "manifest": pin(target), "reviewed_report": before[0], "documentary_checks": documentary_checks}, ensure_ascii=False, indent=2))

"""Create a new byte-measured manifest for the scalar/vector reduction note."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
CHATGPT = ROOT.parent


def measure(path, role):
    data = path.read_bytes()
    return {"path":str(path), "role":role, "bytes":len(data),
            "sha256":hashlib.sha256(data).hexdigest(), "lines":len(data.splitlines()),
            "mtime_ns":path.stat().st_mtime_ns}


receipt = json.loads((ROOT/"VERIFICACAO_REDUCAO.json").read_text(encoding="utf-8"))
if receipt["status"] != "PASS_EXACT_CAS_NOT_LEAN" or not all(c["pass"] for c in receipt["checks"]):
    raise RuntimeError("Symbolic verification did not pass")
if receipt["check_count"] != len(receipt["checks"]):
    raise RuntimeError("Symbolic check count mismatch")

inputs = [
    ("QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md", "full Hessian and gauge model contract"),
    ("QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/MANIFESTO_QUANTIZACAO_LOCAL.json", "prior measured manifest"),
    ("HABITANTE_CURVO_SIGMA_20260909_202000/HABITANTE_CURVO_SIGMA_E_AREA.md", "background solution and conventions"),
    ("HABITANTE_CURVO_SIGMA_20260909_202000/VERIFICACAO_SIMBOLICA.json", "prior exact background checks"),
]
report = {
    "created_utc":datetime.now(timezone.utc).isoformat(),
    "status":"DERIVED_WRITTEN_WITH_PASS_EXACT_CAS",
    "new_lean_proof":False,
    "um_executed_or_imported":False,
    "originals_modified":False,
    "packages_installed":False,
    "author_statement":"Own derivation and measurements; no approval claimed on behalf of another agent or operator.",
    "outputs":[measure(ROOT/name,role) for name,role in [
        ("REDUCAO_ADM_MODOS_FISICOS.md","written ADM reduction and reconstruction proof"),
        ("check_reduction.py","new exact algebra checking script"),
        ("VERIFICACAO_REDUCAO.json","17 exact CAS checks, all residuals zero"),
        ("measure_reduction_manifest.py","new byte-measurement script")]],
    "inputs":[measure(CHATGPT/name,role) for name,role in inputs],
    "byte_backups":[measure(p,"immediate byte backup before note revision") for p in sorted(ROOT.glob("*.bak_*"))],
    "verification":{
        "status":receipt["status"],"count":receipt["check_count"],"sympy_version":receipt["sympy_version"],
        "executable":"C:\\Python314\\python.exe",
        "arguments":["-B",str(ROOT/"check_reduction.py")],
        "first_attempt":"Restricted read could not resolve user-installed sympy: ModuleNotFoundError; no false PASS emitted.",
        "successful_attempt":"Authorized dependency read via require_escalated; all writes remained inside this new Chatgpt folder; exit0.",
        "does_not_certify":"CAS verifies the explicitly encoded modal algebra, not the full geometric ADM/SVT derivation or a Lean theorem."
    },
    "primary_sources":[
        {"title":"Scalar, Vector and Tensor Harmonics on the Three-Sphere","authors":"Lindblom, Taylor, Zhang","url":"https://arxiv.org/pdf/1709.08020","version_read":"v1","use":"Eigenvalues, orthogonality and completeness of S3 harmonics, sections2-4"},
        {"title":"Construction of Hadamard states by pseudo-differential calculus","authors":"Gérard, Wrochna","url":"https://arxiv.org/abs/1209.2604","use":"Relevant primary method; no claim that abstract theorem alone closes reconstructed gauge state"}
    ],
    "results":{
        "scalar_K":"4*(lambda-3)/(lambda+3)","scalar_frequency_squared":"lambda+4",
        "vector_K":"4*D/(D+8)","vector_frequency_squared":"D+8",
        "physical_modes":"ell>=2; lambda=ell*(ell+2), D=ell*(ell+2)-3",
        "exceptional_modes":"scalar ell0 has no gradient sigma mode; scalar ell1 and vector Killing ell1 are residual gauge",
        "conformal_p_squared":{"scalar":"(ell+1)^2+2","vector":"(ell+1)^2+3"},
        "exact_mode":"(p-i*tanh(eta))*exp(-i*p*eta)/sqrt(2*p*(p^2+1))",
        "complete_maps":"solution reconstruction6.1, covariant test pullbacks6.2-6.3, symplectic equality7.2"
    },
    "scope_limits":[
        "Ambient Einstein-sigma extension, not dynamics derived from only minimal five probabilities",
        "Global geometry I x S3 is an extension; strict-positive five-category chart is only local",
        "Gauge slice requires H!=0; endpoints r0 and rpi are outside the contract",
        "TT sector is treated independently and not claimed proved by this note",
        "Full reconstructed Hadamard microlocal property is a separate composition obligation",
        "No nonlinear stability/integrability, interacting anomaly or UV conclusion"
    ]
}
target=ROOT/"MANIFESTO_REDUCAO_SV.json"
if target.exists():
    raise FileExistsError(target)
payload=(json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
tmp=target.with_name(target.name+".new")
with tmp.open("xb") as stream:
    stream.write(payload); stream.flush(); os.fsync(stream.fileno())
assert tmp.read_bytes()==payload
os.rename(tmp,target)
assert target.read_bytes()==payload
print(json.dumps({"note":measure(ROOT/"REDUCAO_ADM_MODOS_FISICOS.md","final note"),"manifest":measure(target,"new manifest"),"checks":receipt["check_count"]},ensure_ascii=False,indent=2))

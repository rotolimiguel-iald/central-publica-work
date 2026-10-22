"""Measure a written curved-sigma construction and exact CAS checks; no Lean or um.py execution."""
from pathlib import Path
import datetime, hashlib, json, os

ROOT = Path(__file__).resolve().parent
CHAT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
LIB = CHAT / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394" / "BUILD_SUCCESSOR_20260909_192313_320129"
FISHER = CHAT / "METRICA_FISHER_SELECIONADA_20260909_195323_635574"
assert ROOT.is_relative_to(CHAT)

def rec(path):
    data=path.read_bytes()
    return {"path":path.as_posix(),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def new(path,data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temporary=path.with_name(path.name+".tmp")
    with temporary.open("xb") as handle:
        handle.write(data);handle.flush();os.fsync(handle.fileno())
    assert temporary.read_bytes()==data
    os.rename(temporary,path)
    assert path.read_bytes()==data

note=ROOT/"HABITANTE_CURVO_SIGMA_E_AREA.md"
cas=ROOT/"VERIFICACAO_SIMBOLICA.json"
result=json.loads(cas.read_bytes())
assert result["status"]=="PASS_EXACT_SYMBOLIC_CHECKS__NOT_LEAN"
assert result["number_of_checks"]==14 and len(result["checks"])==14
assert all(v["passed"] and all(s=="0" for s in v["residuals"]) for v in result["checks"].values())
fisher_source=FISHER/"SelectedFisherLorentzMetric.lean"
fisher_receipt_path=FISHER/"BUILD_20260909_200624_640468"/"BUILD_RESULT.json"
fisher_receipt=json.loads(fisher_receipt_path.read_bytes())
assert fisher_receipt["status"]=="PASS_COMPILED_SCOPE"
assert rec(fisher_source) in fisher_receipt["sources"]
assert all(r["exit_code"]==0 for r in fisher_receipt["runs"])
assert all(set(row["axioms"])<={"propext","Classical.choice","Quot.sound"} for row in fisher_receipt["axiom_rows"])
sources=[
    fisher_source, FISHER/"EXEMPLO_CATEGORICO_CURVO.md",
    CHAT/"VARIACAO_ESCALAR_DENSIDADE_20260909_200600"/"ScalarMatterDensityVariation.lean",
    LIB/"TGLExt"/"GeneralMetricEinstein.lean",
    LIB/"TGLExt"/"GravitationalResponseRecord.lean",
    LIB/"TGLExt"/"MixedGibbsGravitationalBridge.lean",
    KERNEL/"TGLExt"/"CurvatureJetAlgebra.lean",
    KERNEL/"TGLExt"/"MetricCurvatureSymmetries.lean",
    KERNEL/"TGLExt"/"EquilibriumScreenIntegration.lean",
    KERNEL/"TGLExt"/"EquilibriumAreaExpansion.lean",
    KERNEL/"TGLExt"/"GeometricAreaHorizon.lean",
    KERNEL/"TGLExt"/"ScreenClausiusCoefficient.lean",
]
source_records=[rec(p) for p in sources]
manifest={
    "status":"DERIVED_CURVED_EINSTEIN_SIGMA_WITNESS__14_EXACT_SYMBOLIC_CHECKS__NOT_NEW_LEAN",
    "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "note":rec(note),"symbolic_result":rec(cas),
    "symbolic_script":rec(ROOT/"check_curved_sigma.py"),
    "manifest_script":rec(Path(__file__).resolve()),
    "symbolic_runtime":{"executable":"C:/Python314/python.exe","sympy_version":result["sympy_version"],"command_used_flag":"-B"},
    "consulted_sources":source_records,
    "existing_selected_fisher_receipt":rec(fisher_receipt_path),
    "selected_fisher_source_matches_existing_receipt":True,
    "new_symbolic_checks":14,
    "mathematical_conclusions":{
        "metric":"g=dr^2-4cos^2(r/2)h_S3, obtained from selected categorical Fisher.",
        "matter":"phi_a=sqrt(P_a/(1-P0)); common c=k/(pi cosh(k)^2)>0; constrained sigma action explicitly adopted.",
        "sigma_equation":"Box phi_a+Q phi_a=0, Q=-3/a^2, lambda=3c/a^2; individual free wave equations fail.",
        "aggregate_conservation":"Divergence T=c sum(Box phi_a)dphi_a=0 by differentiated constraint.",
        "Einstein":"G+(3/4)g=(4/c)T, checked directly.",
        "area":"Existing equilibrium-screen contract gives A0=1 and quadratic area coefficient -Ric(null,null)/2; same signs verified.",
        "matching":"With eta=pi c/2, Gibbs auxiliary entropy minus eta times induced area has zero quadratic coefficient on all null directions.",
        "chain_rule":"Vanishing ambient Euler residuals implies stationarity after pullback by P; reverse implication is not asserted."
    },
    "limits":{
        "input_choices":"Categorical family, selected label, signed Fisher rule, sigma action, common k and parameter calibration.",
        "probability_protocols":"Categorical P differs from auxiliary Gibbs curves constructed from dphi[P].",
        "quantum":"Free minimal CCR/Hadamard displacement theorem does not apply to sigma fields with nonzero Box phi.",
        "global":"Construction from the single positive P is on the octant. Whole S3 needs sign/atlas data; boundary positivity and global hyperbolicity are not presumed.",
        "tower":"Four equal nontracial base sites require an explicit profile/embedding, not an arbitrary SiteProfile.",
        "unproved_here":"New Lean specialization, interacting quantized gravity, quantum sigma renormalization, anomaly control and UV completion."
    },
    "scope":{"um_py_executed_or_imported":False,"new_lean_compilation":False,
              "original_files_modified":False,"approval_in_others_name":False,"gate_moved":False}
}
assert source_records==[rec(p) for p in sources]
manifest["sources_unchanged_during_final_measurement"]=True
target=ROOT/"MANIFESTO_HABITANTE_CURVO.json"
new(target,(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"manifest":rec(target),"note":rec(note),"symbolic_checks":14},ensure_ascii=False))

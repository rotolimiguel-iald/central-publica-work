"""Read-only source audit and exact finite diagnostics for the Ponte article.
Never imports um.py or runs Lean. Creates one new JSON in this script's folder.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import ast, hashlib, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
if OUT.parent != ROOT or not OUT.name.startswith("AUDITORIA_PONTE_"):
    raise RuntimeError("Output folder is outside the authorized audit scope")
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um")
KERNEL = CANON / "Nós" / "tgl_kernel" / "TGLExt"
PUBLIC = Path(r"C:\IALD\Artigo\the_boundary\A Ponte-Einstein_Cartan_Miguel")
MODULES = [
    "CentralizerLocal", "ExpectationPositive", "AperiodicCentralizerExpectation",
    "AperiodicTowerLift", "GeneralExpectationCP", "ExpectationNormality",
    "TheAtlasIndex", "TriadMaster", "TheRootOfTheProofTree",
    "MicroscopicEinsteinBridge", "ModularCostDerivative", "StateClockDichotomy",
    "CovariantAreaCounterexample", "ContinuousModularReconstruction",
    "TheOathOnTheTower", "ChainFaithful", "ThermalLimitControls",
]
INPUTS = {
    "article": CANON / "A Ponte Einstein Cartan Miguel.tex",
    "article_public": PUBLIC / "A Ponte Einstein Cartan Miguel.tex",
    "um": CANON / "Nós" / "um.py",
    "seal": CANON / "Nós" / "um_absoluto_selo.json",
    "tree": CANON / "Nós" / "A_PROVA_DA_QG_TGL_arvore.md",
    "handoff": CANON / "Nós" / "HANDOFF_v331_A_RAIZ_DA_ARVORE.md",
    "geometry_demo": PUBLIC / "tgl geometry generated v1.py",
    "circle_demo": PUBLIC / "tgl three locks v1.py",
    "report054": ROOT / "CONTINUACAO054_PARECER.md",
    "manifest054": ROOT / "CONTINUACAO054_MANIFESTO.json",
    "build054": ROOT / "CONTINUACAO054_CLEAN_BUILD.json",
    "report050": ROOT / "CONTINUACAO050_PARECER.md",
}
INPUTS.update({name: KERNEL / (name + ".lean") for name in MODULES})

def sha(data):
    return hashlib.sha256(data).hexdigest()

def atomic_new(path, data):
    if path.parent.resolve() != OUT or path.exists():
        raise RuntimeError("Exclusive output creation required: " + str(path))
    temporary = path.with_name(path.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
    with temporary.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.stat().st_size != len(data) or temporary.read_bytes() != data:
        raise RuntimeError("Temporary output failed byte verification")
    os.rename(temporary, path)  # Windows rename refuses replacement of an existing file.
    if path.read_bytes() != data:
        raise RuntimeError("Final output failed byte verification")

raw = {}
texts = {}
records = {}
for name, path in INPUTS.items():
    data = path.read_bytes()  # Permission/read failures are visible and abort the audit.
    raw[name] = data
    text_value = data.decode("utf-8-sig")
    texts[name] = text_value.replace("\r\n", "\n").replace("\r", "\n")
    records[name] = {
        "path": path.as_posix(), "bytes": len(data), "sha256": sha(data),
        "lines": len(texts[name].splitlines()),
    }

tree = ast.parse(texts["um"], filename=str(INPUTS["um"]))
assignments = [
    node for node in tree.body if isinstance(node, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in node.targets)
]
if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Dict):
    raise RuntimeError("Embedded kernel assignment is absent or ambiguous")
embedded = ast.literal_eval(assignments[0].value)
if not isinstance(embedded, dict) or not all(isinstance(k, str) and isinstance(v, str) for k,v in embedded.items()):
    raise RuntimeError("Embedded kernel is not a literal string dictionary")
comparisons = {}
decl_pattern = re.compile(r"^\s*(?:(?:noncomputable|private|protected)\s+)*(?:theorem|lemma|def|structure)\s+([^\s(:{]+)")
declarations = {}
for name in MODULES:
    key = "TGLExt/" + name + ".lean"
    value = embedded.get(key)
    canonical = texts[name]
    comparisons[name] = {
        "key": key, "present": value is not None,
        "text_equal_normalizing_line_endings": value is not None and value.replace("\r\n","\n").replace("\r","\n") == canonical,
        "embedded_utf8_sha256": sha(value.encode("utf-8")) if value is not None else None,
        "canonical_byte_sha256": records[name]["sha256"],
    }
    declarations[name] = [
        {"line": i, "name": match.group(1)}
        for i, line in enumerate(canonical.splitlines(), 1)
        if (match := decl_pattern.match(line))
    ]

def excerpt(name, start, end):
    lines = texts[name].splitlines()
    if not (1 <= start <= end <= len(lines)):
        raise RuntimeError("Invalid source range")
    return {"path": records[name]["path"], "start": start, "end": end,
            "lines": [{"line": i, "text": lines[i-1]} for i in range(start, end+1)]}

excerpts = {
    "terminality": excerpt("article", 1435, 1474),
    "axG": excerpt("article", 1690, 1704),
    "radical_and_circle": excerpt("article", 1886, 1942),
    "geometry_demo_distance": excerpt("geometry_demo", 40, 90),
    "circle_demo_construction": excerpt("circle_demo", 72, 157),
}
# Rational arithmetic only. The repeated eigenvalue survives every scalar
# spectral function of rho, including K=-log(rho) and sqrt(K).
def zero(n=4):
    return [[F(0) for _ in range(n)] for _ in range(n)]
def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(a))), F(0))
             for j in range(len(a))] for i in range(len(a))]
def sub(a, b):
    return [[a[i][j]-b[i][j] for j in range(len(a))] for i in range(len(a))]
def transpose(a):
    return [list(row) for row in zip(*a)]
def diag(values):
    a=zero(len(values))
    for i,v in enumerate(values):
        a[i][i]=v
    return a

p=F(1,3)
weights=[p*p,p*(1-p),(1-p)*p,(1-p)*(1-p)]
rho=diag(weights)
a=zero(); a[1][2]=a[2][1]=F(1)
b=zero(); b[1][1]=F(1); b[2][2]=F(-1)
def pinch(x):
    return [[x[i][j] if weights[i]==weights[j] else F(0)
             for j in range(4)] for i in range(4)]
commutator=sub(mul(a,b),mul(b,a))
expected=zero(); expected[1][2]=F(-2); expected[2][1]=F(2)
groups=[]
for value in sorted(set(weights)):
    groups.append([i for i,w in enumerate(weights) if w==value])
checks = {
    "weights_strictly_positive": all(w>0 for w in weights),
    "weights_normalized": sum(weights)==1,
    "a_hermitian_real_symmetric": transpose(a)==a,
    "b_hermitian_real_symmetric": transpose(b)==b,
    "rho_commutes_a": sub(mul(rho,a),mul(a,rho))==zero(),
    "rho_commutes_b": sub(mul(rho,b),mul(b,rho))==zero(),
    "pinching_fixes_a": pinch(a)==a,
    "pinching_fixes_b": pinch(b)==b,
    "commutator_exact": commutator==expected,
    "commutator_nonzero": commutator!=zero(),
    "a_not_scalar_on_repeated_eigenspace": a[1][2]!=0,
}
for i in range(4):
    for j in range(4):
        e=zero(); e[i][j]=F(1)
        checks["pinching_idempotent_E%d%d"%(i,j)]=pinch(pinch(e))==pinch(e)

roots=[F(1),F(2),F(3)]
line=[[abs(x-y) for y in roots] for x in roots]
positions=[F(0),F(1,3),F(2,3)]
circle=[[min(abs(x-y),1-abs(x-y)) for y in positions] for x in positions]
degenerate_roots=[F(1),F(2),F(2)]
degenerate=[[abs(x-y) for y in degenerate_roots] for x in degenerate_roots]
metric_checks={
    "line_triangle_equality": line[0][2]==line[0][1]+line[1][2],
    "circle_three_distances_equal": circle[0][1]==circle[1][2]==circle[0][2]>0,
    "circle_no_triangle_equality": all(circle[i][k] < circle[i][j]+circle[j][k]
                                      for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]),
    "repeated_eigenvalue_zero_distance_distinct_labels": degenerate[1][2]==0,
}
if not all(checks.values()) or not all(metric_checks.values()):
    raise RuntimeError("An exact diagnostic failed")
if not all(item["text_equal_normalizing_line_endings"] for item in comparisons.values()):
    raise RuntimeError("Selected embedded and canonical modules differ; inspect before claiming agreement")

def small_status(obj, prefix="", depth=0):
    found={}
    if depth>3 or not isinstance(obj, dict):
        return found
    for key,value in obj.items():
        joined=prefix+"."+key if prefix else key
        if isinstance(value,(str,bool,int,float,type(None))) and re.search(r"status|verdict|fresh_clean|H3|reconstruction|gate|timestamp|version",key,re.I):
            found[joined]=value
        elif isinstance(value,dict) and depth<3 and re.search(r"status|summary|result|boundary|scope|audit|claim",key,re.I):
            found.update(small_status(value,joined,depth+1))
    return found
historic={name:small_status(json.loads(texts[name]))
          for name in ["manifest054","build054","seal"]}

unchanged={name:sha(path.read_bytes())==records[name]["sha256"] for name,path in INPUTS.items()}
if not all(unchanged.values()):
    raise RuntimeError("A consulted source changed during this audit")
result={
    "status":"PASS_EXACT_DIAGNOSTICS_AND_SELECTED_SOURCE_TEXT_MATCH",
    "created_utc":datetime.now(timezone.utc).isoformat(),
    "scope":{
        "original_program_executed":False,"original_program_imported":False,
        "lean_compilation_performed":False,"independent_scientific_review_performed":False,
        "original_files_written":False,"canonical_memory_or_gate_written":False,
        "output_directory":OUT.as_posix(),
        "interpretation":"Read-only static audit plus finite exact diagnostics; not a new formal proof batch.",
    },
    "sources":records,
    "embedded_assignment_line":assignments[0].lineno,
    "embedded_file_count":len(embedded),
    "selected_module_count":len(MODULES),
    "selected_embedded_comparisons":comparisons,
    "declarations":declarations,
    "source_excerpts":excerpts,
    "centralizer_diagnostic":{
        "status":"REAL_EXACT_FINITE_DIAGNOSTIC",
        "basis":["00","01","10","11"],"p":p,"weights":weights,
        "rho":rho,"A":a,"B":b,"AB_minus_BA":commutator,
        "spectral_blocks":groups,
        "fixed_algebra_complex_dimension":sum(len(g)**2 for g in groups),
        "scalar_function_algebra_complex_dimension":len(groups),
        "checks":checks,
        "global_lift_status":"DERIVED_BY_COMPOSITION_OF_INSPECTED_DECLARATIONS_NOT_COMPILED_HERE",
    },
    "metric_diagnostic":{
        "status":"REAL_EXACT_FINITE_DIAGNOSTIC",
        "common_scale":"Any positive scale omitted; no numeric beta used.",
        "sqrt_k":roots,"line_distances":line,
        "circle_positions_fraction_of_circumference":positions,
        "circle_distances_fraction_of_circumference":circle,
        "repeated_sqrt_k":degenerate_roots,"pseudometric":degenerate,
        "checks":metric_checks,
        "scope":"Obstructs literal distance identification, not all angular reconstructions or changed metrics.",
    },
    "historical_metadata_not_new_build":historic,
    "consulted_sources_unchanged_during_run":unchanged,
    "script_sha256":sha(Path(__file__).read_bytes()),
}
def encode(value):
    if isinstance(value,F):
        return str(value)
    raise TypeError(type(value).__name__)
data=(json.dumps(result,ensure_ascii=False,indent=2,default=encode)+"\n").encode("utf-8")
output=OUT/"RESULTADOS_EXATOS.json"
atomic_new(output,data)
print(json.dumps({
    "status":result["status"],"output":output.as_posix(),
    "selected_module_count":len(MODULES),
    "source_count":len(records),
    "exact_check_count":len(checks)+len(metric_checks),
    "centralizer_dimension":sum(len(g)**2 for g in groups),
    "generated_abelian_dimension":len(groups),
    "historical":historic,
},ensure_ascii=False,indent=2))

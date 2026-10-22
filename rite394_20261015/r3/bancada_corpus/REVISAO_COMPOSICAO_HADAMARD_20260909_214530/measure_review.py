from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
def item(path,role):
    data=path.read_bytes()
    return {"path":str(path),"role":role,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"lines":len(data.splitlines())}

inputs=[
 ("HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md","composition reviewed in full"),
 ("MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md","TT source reviewed in full"),
 ("MODOS_TENSORIAIS_EXATOS_20260909/VERIFICACAO_MODOS_TT.json","read historical 12-check receipt, not rerun"),
 ("REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531/REDUCAO_ADM_MODOS_FISICOS.md","own prior scalar/vector reduction"),
 ("REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531/VERIFICACAO_REDUCAO.json","read historical 17-check receipt, not rerun"),
 ("QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md","own prior exact gauge and Green identities")]

report={
 "created_utc":datetime.now(timezone.utc).isoformat(),
 "status":"DERIVED_OWN_REVIEW_NO_NEW_FORMAL_PROOF",
 "verdict":"No concrete failure found invalidating the stated restricted physical linear Hadamard construction; stronger contracts remain explicitly open.",
 "scope":"Review of another composition and TT note against own earlier S/V derivation; not an independent second authorship of the S/V derivation.",
 "new_argument":"Explicit time cutoff proves surjectivity of invariant compact test causal solutions onto physical smooth solution classes on I x S3.",
 "new_cas_execution":False,"new_lean_compilation":False,"um_execution_or_import":False,"existing_files_modified":False,
 "inputs":[item(BASE/name,role) for name,role in inputs],
 "outputs":[item(ROOT/"REVISAO_MATEMATICA_PROPRIA.md","new own review"),item(Path(__file__).resolve(),"new measurement script")]
}
target=ROOT/"MANIFESTO_REVISAO_COMPOSICAO.json"
if target.exists(): raise FileExistsError(target)
payload=(json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
tmp=target.with_name(target.name+".new")
with tmp.open("xb") as stream:
    stream.write(payload);stream.flush();os.fsync(stream.fileno())
assert tmp.read_bytes()==payload
os.rename(tmp,target)
assert target.read_bytes()==payload
print(json.dumps({"note":item(ROOT/"REVISAO_MATEMATICA_PROPRIA.md","review"),"manifest":item(target,"manifest")},ensure_ascii=False,indent=2))

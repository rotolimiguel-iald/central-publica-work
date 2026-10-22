"""Prepare new utilities and adapt configuration preparation from frozen predecessor93."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT=Path(__file__).resolve().parent
PREVIOUS=BASE/"INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415"
AUDITOR=BASE/"AUDITORIA_INTEGRACAO_93_V2_20260909_203946_6451878/audit_integration_93_v2.py"
def rec(p):
 b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def new(p,b):
 assert p.resolve().is_relative_to(BASE) and not p.exists()
 t=p.with_name(p.name+".tmp")
 with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.rename(t,p);assert p.read_bytes()==b
copies=[]
for name in ["integrate_approved_copy.py","prepare_successor.py","run_successor.py"]:
 source=PREVIOUS/name;target=OUT/name;raw=source.read_bytes();new(target,raw)
 copies.append({"source":rec(source),"copy":rec(target),"byte_identical":True})
new(OUT/"REFERENCE_audit_integration_93_v2.py",AUDITOR.read_bytes())
origin=PREVIOUS/"prepare_configuration.py";original=origin.read_bytes();text=original.decode("utf-8")
changes=[]
def replace(old,new_text):
 global text
 assert text.count(old)==1,(old,text.count(old))
 text=text.replace(old,new_text);changes.append({"from":old,"to":new_text,"occurrences":1})
replace('PREVIOUS = BASE / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394"',
 'PREVIOUS = BASE / "INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415"')
replace('PREVIOUS_BUILD = PREVIOUS / "BUILD_SUCCESSOR_20260909_192313_320129"',
 'PREVIOUS_BUILD = PREVIOUS / "BUILD_SUCCESSOR_20260909_203414_443930"')
replace('COPY = BASE / "COPIA_INTEGRADA_20260909_192248_937671"',
 'COPY = BASE / "COPIA_INTEGRADA_20260909_203352_868028"')
match=re.search(r"SOURCES = \[.*?\n\]\n",text,re.S);assert match
replace(match.group(0),'SOURCES = [\n    ("SIGMA_DAS_PROBABILIDADES_20260909_204907_970447", "SelectedProbabilitySigma", "BUILD_20260909_205211_077766"),\n]\n')
replace("read_json(PREVIOUS / 'CONFIG_83_APROVADA.json')", "read_json(COPY / 'CONFIG_APROVADA.json')")
replace('Additive successor of verified copy83 only.', 'Additive successor of verified copy93 only.')
ast.parse(text);target=OUT/"prepare_configuration_from93.py";new(target,text.encode("utf-8"))
provenance={"status":"UTILITIES_PREPARED_NOT_EXECUTED","created_utc":datetime.now(timezone.utc).isoformat(),
 "copies":copies,"configuration_preparer_origin":rec(origin),"configuration_preparer":rec(target),"configuration_changes":changes,
 "auditor_origin":rec(AUDITOR),"auditor_reference_copy":rec(OUT/"REFERENCE_audit_integration_93_v2.py"),
 "historical_base_correction_preserved":"The initial stage uses um_ORIGINAL_SNAPSHOT.py and original recorded source hash. Live canonical is a separate diagnostic only.",
 "integrator_executed":False,"lean_executed":False,"um_py_executed_or_imported":False,"approval_attributed":False}
new(OUT/"PROVENIENCIA_UTILITARIOS_93.json",(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
assert origin.read_bytes()==original
print(json.dumps({"folder":OUT.as_posix(),"status":provenance["status"],"scripts_copied":len(copies)},ensure_ascii=False))

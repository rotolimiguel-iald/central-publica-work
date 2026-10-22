"""Index prior Chatgpt work and compare selected source bytes with v350, read-only."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent
OUT = ROOT / 'REEXAME_CHATGPT_20260912'
OUT.mkdir(exist_ok=True)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def create(name, raw):
    target = OUT / name
    assert not target.exists()
    temp = target.with_name(target.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(target)

cmd = ['rg', '--files', str(ARCHIVE), '-g', '*.lean', '-g', '*.md',
       '-g', '!**/.lake/**', '-g', '!**/packages/**', '-g', '!**/build/**',
       '-g', '!**/TETELESTAI_V350_KERNEL_20260911/**']
run = subprocess.run(cmd, capture_output=True)
create('rg_stdout.txt', run.stdout)
create('rg_stderr.txt', run.stderr)
assert run.returncode == 0, 'Inventory incomplete; inspect captured stderr.'
paths = [Path(p) for p in run.stdout.decode('utf-8').splitlines()]
base_raw = (ROOT / 'fontes/um_v350_original.py').read_bytes()
tree = ast.parse(base_raw)
embedded = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and
    any(isinstance(t,ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)).value)
by_name = {}
for key,value in embedded.items():
    by_name.setdefault(Path(key).name, []).append((key,value))

def normalized(text):
    text = re.sub(r'^import TGLExt\.', 'import ', text.replace('\r\n','\n'), flags=re.M)
    return text[text.find('import '):] if 'import ' in text else text

terms = re.compile(r'Tomita|Modular|Graph|Resolvent|Trace|Susy|Einstein|Horizon|Fisher|'
                   r'Gauge|BRST|Master|QME|Gibbs|Hadamard|Weyl|Entropy|Lorentz|Area|Clausius',re.I)
selected = [p for p in paths if p.suffix == '.lean' and len(p.relative_to(ARCHIVE).parts) <= 2
            and terms.search(p.name)]
rows=[]
for p in selected:
    raw=p.read_bytes()
    text=raw.decode('utf-8-sig')
    copies=by_name.get(p.name,[])
    rows.append({'path':str(p), 'bytes':len(raw), 'sha256':sha(raw),
        'mtime':p.stat().st_mtime,
        'declarations':re.findall(r'^(?:noncomputable )?(?:def|theorem|lemma|structure|abbrev)\s+([\w.]+)',text,re.M),
        'v350_same_basename':[k for k,v in copies],
        'v350_exact_text':[k for k,v in copies if v==raw.decode('utf-8')],
        'v350_normalized_imports_equal':[k for k,v in copies if normalized(v)==normalized(text)]})
summary={'timestamp':datetime.datetime.now().astimezone().isoformat(), 'archive':str(ARCHIVE),
    'inventory_command':cmd, 'inventory_returncode':run.returncode, 'listed_paths':len(paths),
    'excluded':['.lake','packages','build','current TETELESTAI workspace'],
    'selection':'Lean sources at depth <=2 with declared name patterns; deeper copies listed, not exhaustively read',
    'base_sha256':sha(base_raw),'selected_sources':len(rows),
    'exact_matches':sum(bool(r['v350_exact_text']) for r in rows),
    'normalized_matches':sum(bool(r['v350_normalized_imports_equal']) for r in rows),
    'rows':rows, 'compiled_now':False,'gate_changed':False,
    'interpretation':'Source correspondence only; not proof of current compilation or discharge of hypotheses.'}
create('inventory.json',json.dumps(summary,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({k:v for k,v in summary.items() if k not in ('rows','inventory_command')},ensure_ascii=False))
for row in rows:
    if re.search(r'GenericAntilinear|StandardSubspace|ContinuousModularDomain|GeneralLinearizedGauge|'
                 r'GeneralMetricEinstein|SelectedFisherLorentz|GeneralSourceEinstein|GravitationalResponse',Path(row['path']).name):
        print(json.dumps(row,ensure_ascii=False))

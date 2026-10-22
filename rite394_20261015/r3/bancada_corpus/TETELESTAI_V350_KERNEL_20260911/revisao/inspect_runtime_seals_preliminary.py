import ast
import datetime
import hashlib
import json
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
OUT = ROOT / 'revisao' / ('runtime_seals_preliminary_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OUT.mkdir()
targets = ['arc_consolidation', 'closure_roadmap', 'evidence_audit', 'love_reading',
           'stokes_contour', 'the_assembly_and_the_single_debt', 'the_atlas_and_the_index',
           'void_floor_final', 'void_floor_v2', 'void_density_opening', 'void_power',
           'void_v41', 'void_shear_v2']

def write(name, obj):
    (OUT / name).write_bytes(json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8'))

def pin(p, data):
    return {'path': str(p), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'mtime': datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat()}

docs, pins = {}, {}
for alias, rel in [('current','r/um_absoluto.json'), ('seal','r/um_absoluto_selo.json'),
                   ('proof','r/tgl_kernel_proof_manifest.json'), ('baseline','fontes/um_absoluto.json'),
                   ('baseline_seal','fontes/um_absoluto_selo.json'),
                   ('contract','CONTRATO_ATIVO_GATE_V350.json')]:
    p = ROOT / rel
    data = p.read_bytes()
    docs[alias] = json.loads(data)
    pins[alias] = pin(p, data)
    (OUT / (alias + '.json')).write_bytes(data)
for alias, rel in [('program', 'um.py'), ('run_program', 'r/um.py')]:
    p = ROOT / rel
    data = p.read_bytes()
    pins[alias] = pin(p, data)

sections = {}
def walk(obj, path, dest):
    if isinstance(obj, dict):
        for k,v in obj.items():
            full = path + [k]
            if k in targets or k == 'not_sealed_this_run' or k == 'quantum_gravity_closure':
                dest['.'.join(full)] = v
            walk(v, full, dest)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            walk(v,path+[str(i)],dest)

for alias in ['current','seal','baseline','baseline_seal']:
    sections[alias] = {}
    walk(docs[alias],[],sections[alias])
write('pins.json', pins)
write('target_sections.json', sections)

source = (ROOT/'um.py').read_text(encoding='utf-8')
tree = ast.parse(source)
line = source.splitlines()
function_index = []
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        matches = [t for t in targets if t in node.name]
        if matches:
            function_index.append({'name':node.name,'line':node.lineno,'end':node.end_lineno})
            (OUT/(node.name+'.txt')).write_text('\n'.join(f'{i+1}: {line[i]}' for i in range(node.lineno-1,node.end_lineno)),encoding='utf-8')
write('function_index.json', function_index)
summary = {'out':str(OUT), 'pins':pins,
    'top_keys':{k:list(v) if isinstance(v,dict) else type(v).__name__ for k,v in docs.items()},
    'sections':{k:{p:len(json.dumps(v)) for p,v in vals.items()} for k,vals in sections.items()},
    'function_index':function_index}
write('inspection_index.json',summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))

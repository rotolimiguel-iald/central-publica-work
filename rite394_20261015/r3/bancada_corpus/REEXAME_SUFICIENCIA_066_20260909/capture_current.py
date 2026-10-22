from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=Path(__file__).resolve().parent
CANON=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
pins=[]
def read(p):
    b=p.read_bytes(); pins.append({'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}); return b
def new(p,b):
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and b
    tmp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    tmp.rename(p); assert p.read_bytes()==b

prior_path=ROOT/'REEXAME_V338_FECHAMENTO_20260909/RECEIPT_V338.json'
prior=json.loads(read(prior_path))
raw=read(CANON/'um.py'); source=ast.parse(raw.decode('utf-8-sig'))
assign=[n for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets)]
assert len(assign)==1
embedded=ast.literal_eval(assign[0].value)
seal=json.loads(read(CANON/'um_absoluto_selo.json'))
manifest=json.loads(read(CANON/'tgl_kernel_proof_manifest.json'))
read(CANON/'rodada_v338_stdout.txt')
plan=json.loads(read(ROOT/'INTEGRADOR_PRECISAO_METRICA_ACAO_20260909_201301_8584415/BUILD_SUCCESSOR_20260909_203414_443930/BUILD_PLAN.json'))
names=[m['module'] for m in plan['modules']]+['SelectedProbabilitySigma','SignedGibbsResponse','RenormalizedNegativeExpectation','SignedGibbsCoverage']
assert len(names)==len(set(names))==97
presence=[{'module':n,'present':f'TGLExt/{n}.lean' in embedded} for n in names]
prior_pins={str(Path(p)):v for p,v in prior['source_pins'].items()}
comparisons=[{'path':p['path'],'matches_prior':{'bytes':p['bytes'],'sha256':p['sha256']}==prior_pins[str(Path(p['path']))]} for p in pins if str(Path(p['path'])) in prior_pins]
for p in pins:
    b=Path(p['path']).read_bytes(); assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']
result={'status':'READ_ONLY_STABLE_SNAPSHOT','created_utc':datetime.now(timezone.utc).isoformat(),
    'embedded_files':len(embedded),'modules':presence,'present':sum(m['present'] for m in presence),
    'absent':[m['module'] for m in presence if not m['present']],
    'comparison_with_delivery065':comparisons,
    'seal_um_hash_matches':seal['sha256']['um.py']==hashlib.sha256(raw).hexdigest(),
    'seal_excerpt':{k:seal[k] for k in ('qg_closure_verdict','renormalization_wall_verdict','fail_closed_selftest') if k in seal},
    'pins':pins,'all_read_sources_unchanged':True,'um_executed_or_imported':False,'originals_written':False,
    'scope':'Current source/seal/manifest/run hashes compared to delivery065; no new canonical execution, full source audit, or nature run. Prior source audit remains referenced evidence.'}
new(OUT/'ESTADO_CANONICO_066.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({k:result[k] for k in ('status','embedded_files','present','absent','comparison_with_delivery065','seal_um_hash_matches','seal_excerpt')},ensure_ascii=False))

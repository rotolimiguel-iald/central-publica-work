"""Freeze reviewed source/receipt pins for a new copy, without loading either program."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
here=Path(__file__).resolve().parent
base=here.parent
assert base == Path(r'C:\IALD\Central de Patentes\Chatgpt')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def rec(p):
    b=p.read_bytes()
    return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(r):
    p=Path(r['path']); assert rec(p)==r, 'Changed frozen input: '+str(p)
    return p
def item(source,receipt):
    sr=rec(source); br=rec(receipt); proof=read(receipt)
    assert proof['status']=='PASS_COMPILED_SCOPE'
    assert sr in proof['sources']
    assert all(r['exit_code']==0 for r in proof['runs'])
    assert all(set(r['axioms']) <= {'propext','Classical.choice','Quot.sound'} for r in proof['axiom_rows'])
    assert (receipt.parent/source.name).read_bytes()==source.read_bytes()
    return {'source':sr['path'],'sha256':sr['sha256'],
            'build_result':br['path'],'build_result_sha256':br['sha256']}
old_config=base/'COPIA_INTEGRADA_20260909_134555_358057/CONFIG_APROVADA.json'
old=read(old_config)
for i in old['modules']:
    assert rec(Path(i['source']))['sha256']==i['sha256']
    assert rec(Path(i['build_result']))['sha256']==i['build_result_sha256']
modules=[item(Path(i['source']),Path(i['build_result'])) for i in old['modules']]
supp=read(base/'REEXAME_FONTE_GERAL_20260909_133220_037525/SUPLEMENTOS_FINAIS_PASS.json')
assert supp['status']=='PASS_IN_INDIVIDUAL_SCOPES'
for m in supp['modules']: modules.append(item(verify(m['source']),verify(m['receipt'])))
audit_path=here/'AUDITORIA_ESTATICA_CONTINUACAO.json'
audit=read(audit_path)
assert audit['status']=='PASS_STATIC_EVIDENCE_AUDIT' and not audit['failed_checks']
for m in audit['modules']: modules.append(item(verify(m['source']),verify(m['receipt'])))
assert len(sys.argv)==3, 'Supply both reviewed final supplement source paths.'
for name in sys.argv[1:]:
    p=Path(name).resolve()
    assert p.is_relative_to(base) and p.suffix=='.lean'
    matches=[]
    for candidate in p.parent.glob('BUILD_*/BUILD_RESULT.json'):
        evidence=read(candidate)
        if evidence.get('status')=='PASS_COMPILED_SCOPE' and rec(p) in evidence.get('sources',[]):
            matches.append(candidate)
    assert matches,'No matching PASS for '+str(p)
    modules.append(item(p, sorted(matches)[-1]))
paths=[i['source'] for i in modules]
assert len(paths)==len(set(paths))
current=verify(audit['canonical']['after'])
assert audit['canonical']['matches_v337']
cfg={'root_confirmed':True,
    'approval_basis':'Fontes congeladas com recibos PASS; revisões semânticas independentes desta sessão. Ação autorizada somente em nova cópia Chatgpt; nenhum um.py será executado/importado.',
    'created_utc':datetime.now(timezone.utc).isoformat(),
    'source_um':current.as_posix(),'source_um_sha256':rec(current)['sha256'],
    'modules':modules,'canonical_snapshot_basis':rec(audit_path),
    'prior_integrated_copy':rec(base/'COPIA_INTEGRADA_20260909_134555_358057/um.py'),
    'scope':'Static copy with embedded Lean sources and additive imports/audit only; no new runtime flags or gate changes.'}
counts={'modules':len(modules),'theorems':0,'other_declarations':0}
for m in modules:
    s=Path(m['source']).read_text(encoding='utf-8')
    ds=re.findall(r'(?m)^(?:noncomputable\s+)?(abbrev|def|structure|theorem)\s+(\w+)',s)
    counts['theorems']+=sum(k=='theorem' for k,n in ds)
    counts['other_declarations']+=sum(k!='theorem' for k,n in ds)
cfg['measured_counts']=counts
p=here/('CONFIG_FINAL_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
raw=(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
t=p.with_name(p.name+'.tmp')
with t.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
assert t.read_bytes()==raw
os.rename(t,p)
assert p.read_bytes()==raw
print(json.dumps({'config':str(p),'counts':counts},ensure_ascii=False))

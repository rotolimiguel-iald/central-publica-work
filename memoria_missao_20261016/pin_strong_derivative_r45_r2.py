from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
out=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base=out/'maxwell_global'
ref=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
oldpath=base/'COMPACT_BOOST_STRONG_DERIVATIVE_CANDIDATE_R45.json'
old=json.loads(oldpath.read_text(encoding='utf-8'))
for item in old['pins']+old['sources']:
    assert pin(item['path'])['sha256']==item['sha256'],item['path']
request={'operation':'project','reference':str(ref),'actor':old['actor'],'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(request),text=True,encoding='utf-8',capture_output=True,check=True)
p=json.loads(run.stdout)
assert p['ok'],p
result=p['result']
sources=[base/'CompactBoostStrongDerivativeReductionR3.lean',base/'CompactBoostStrongDerivativeR2.lean']
static=[]
for path in sources:
    text=path.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|(?m:^\s*(axiom|opaque)\s)',text)
    static.append({'path':str(path),'lines':len(text.splitlines()),'theorems':len(re.findall(r'^theorem ',text,re.M))})
report=dict(old)
report.update({
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'mission_receipt':result['receipt'],'projection_sha256':result['projection_sha256'],
 'projection_chars':result['actual_chars'],'sources':[pin(x) for x in sources],
 'previous_manifest':pin(oldpath),'static_checks':static,
 'additional_repairs':['Explicit change to the pointwise real scalar product in compactBoostGenerator_compact.',
   'Function.comp_def in hyperbolic derivative compositions, including the extension.'],
 'observed_R2_build':{'attempt':'20261016T174125_443523Z','exit_code':1,
   'errors_remaining_before_this_candidate':3,
   'independent_of_new_source':'orbitalL2_tendsto_of_square_majorant in ReductionR2 compiled with propext, Classical.choice, Quot.sound only'},
 'pins':old['pins']+old['sources']+[pin(out/'orbital_rotation/attempts/20261016T174125_443523Z/AXIOMS.txt'),pin(out/'orbital_rotation/attempts/20261016T174125_443523Z/RECEIPT.json')],
})
dst=base/'COMPACT_BOOST_STRONG_DERIVATIVE_CANDIDATE_R45_R2.json'
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=dst.with_suffix('.json.tmp_r45b')
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data
os.rename(tmp,dst)
print(json.dumps({'report':pin(dst),'sources':report['sources'],'pins':len(report['pins']),'revision':result['receipt']['revision']},ensure_ascii=False))

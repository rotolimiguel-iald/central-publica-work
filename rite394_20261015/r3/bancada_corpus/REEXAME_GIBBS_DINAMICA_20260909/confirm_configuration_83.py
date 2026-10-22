from pathlib import Path
import json,hashlib,os,datetime
root=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
folder=root/'INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394'
p=folder/'CONFIG_83_NAO_CONFIRMADA.json'; cfg=json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(r):
    p=Path(r['path']);assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
assert cfg['root_confirmed'] is False and len(cfg['modules'])==6
assert sha(Path(cfg['source_um']))==cfg['source_um_sha256']
for key in ['predecessor_integration_result','predecessor_build_result','predecessor_build_plan','inventory']:check(cfg[key])
for item in cfg['modules']:
    src=Path(item['source']); rp=Path(item['build_result'])
    assert sha(src)==item['sha256'] and sha(rp)==item['build_result_sha256']
    r=json.loads(rp.read_bytes());assert r['status']=='PASS_COMPILED_SCOPE'
    assert len(r['runs'])==2 and all(z['exit_code']==0 for z in r['runs'])
    assert (rp.parent/src.name).read_bytes()==src.read_bytes()
old=root/'INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582'
for name in ['integrate_approved_copy.py','prepare_successor.py','run_successor.py']:
    assert (folder/name).read_bytes()==(old/name).read_bytes()
cfg['root_confirmed']=True
cfg['approval_basis']='The main task read the six source statements, leaf receipts and prepared configuration. Frozen pins and unchanged integrator bytes were remeasured by this script. Confirmed only for additive integration into a new Chatgpt copy and scoped joint compilation; no approval from another reviewer is attributed.'
cfg['confirmed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
cfg['scope']='Six frozen PASS sources added to predecessor77 in a NEW copy. No um.py execution/import, canonical write, new physical flag, seal, or physical completion claim. Subsequent joint compilation and static audit are required.'
out=folder/'CONFIG_83_APROVADA.json';assert not out.exists()
b=(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n').encode();t=out.with_name(out.name+'.tmp')
with t.open('xb') as f:
    f.write(b);f.flush();os.fsync(f.fileno())
assert t.read_bytes()==b
os.replace(t,out);assert out.read_bytes()==b
print(json.dumps({'configuration':out.as_posix(),'sha256':sha(out),'confirmed':True}))

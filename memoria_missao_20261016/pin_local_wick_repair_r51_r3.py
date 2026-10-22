from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
OUT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
BASE=OUT/'maxwell_global'
WORK=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016')
FOCK=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\fock_construction')
M=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib')
REF=WORK/'FECHO_MISSION_REFERENCE.json'
ACTOR={'kind':'agent','id':'codex-r51-wick-local-identification'}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p);b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def collect(o):
    if isinstance(o,dict):
        if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str): yield o
        for v in o.values():yield from collect(v)
    elif isinstance(o,list):
        for v in o:yield from collect(v)
checked={}
def verify(o):
    for x in collect(o):
        key=(x['path'],x['sha256'].lower())
        if key in checked:continue
        a=pin(x['path']);assert a['sha256']==key[1],a
        if 'bytes' in x:assert a['bytes']==x['bytes'],a
        checked[key]=a
roots=[OUT/'orbital_rotation/attempts',OUT/'kms_strip/attempts']
def green(source,required=True):
    source=Path(source); matches=[]
    for root in roots:
        for src in root.glob('*/'+source.name):
            rp=src.parent/'RECEIPT.json'
            if not rp.exists():continue
            r=read(rp)
            if r.get('exit_code')!=0 or src.read_bytes()!=source.read_bytes():continue
            matches.append((src,rp,r))
    if not matches:
        assert not required,source
        return {'source':pin(source),'status':'DECLARADO_PENDING_BUILD'}
    src,rp,r=sorted(matches,key=lambda x:x[0].parent.name)[-1]
    verify(r)
    axp=src.parent/'AXIOMS.txt';ax=axp.read_text(encoding='utf-8')
    lists=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",ax)
    assert lists and 'sorryAx' not in ax and 'error:' not in ax
    assert all(set(v.strip() for v in s.split(','))<={'propext','Classical.choice','Quot.sound'} for _,s in lists)
    return {'source':pin(source),'status':'COMPILED_EXIT0_NOT_INDEPENDENTLY_REVIEWED_HERE',
      'receipt':pin(rp),'axioms':pin(axp),'seconds':r['seconds'],'exit_code':0,
      'axiom_declarations':[n for n,_ in lists],'only_standard_trio':True,'source_matches_attempt':True}
old=BASE/'LOCAL_WICK_IDENTIFICATION_CANDIDATES_R51_R2.json'
verify(read(old))
base=green(BASE/'RegularPointAnnihilationR2.lean')
local_old=BASE/'LocalWickStressIdentificationR2.lean'
local_new=BASE/'LocalWickStressIdentificationR3.lean'
smear_old=BASE/'PointAnnihilationSmearingR2.lean'
smear_new=BASE/'PointAnnihilationSmearingR3.lean'
assert smear_new.read_bytes()==smear_old.read_bytes().replace(b'import LocalWickStressIdentificationR2',b'import LocalWickStressIdentificationR3',1)
import difflib
changes=list(difflib.unified_diff(local_old.read_text(encoding='utf-8').splitlines(),local_new.read_text(encoding='utf-8').splitlines(),n=2))
new=[]
for f in [local_new,smear_new]:
 t=f.read_text(encoding='utf-8')
 assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s',t,re.M)
 assert 'set_option maxHeartbeats 400000' in t
 assert 'set_option synthInstance.maxHeartbeats 500000' in t
 new.append({'source':pin(f),'imports':re.findall(r'^import (.+)$',t,re.M),
 'prints':re.findall(r'^#print axioms (.+)$',t,re.M)})
failed=OUT/'orbital_rotation/attempts/20261016T204127_892966Z'
fr=read(failed/'RECEIPT.json');assert fr['exit_code']==1
assert (failed/local_old.name).read_bytes()==local_old.read_bytes()
verify(fr)
req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
 input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
r=json.loads(run.stdout);assert r['ok'];m=r['result']
r8=next(x for x in m['projection']['active'] if x['id']=='R8');assert r8['status']=='working'
report={'schema':'iald-lean-repair/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'DECLARADO_PENDING_BUILD_AND_INDEPENDENT_REVIEW','requirement':'R8','requirement_satisfied':False,
 'author':ACTOR,'handle':'r51-wick-local-identification','mission_reference':pin(REF),
 'mission_receipt':m['receipt'],'projection_sha256':m['projection_sha256'],'criterion':r8['criterion'],
 'lease_observed':r8['lease'],'previous_manifest':pin(old),'sources':new,
 'green_supplier':base,'failed_source':pin(local_old),'failed_receipt':pin(failed/'RECEIPT.json'),
 'failed_axioms':pin(failed/'AXIOMS.txt'),'local_diff':changes,
 'repair':'Somente pointWick_finiteKernel: calc usa diretamente regularWick_finiteKernel e congrArg sobre igualdade de funções obtida por funext e pointWick_exponential. Sem refold por simp nem alteração dos enunciados.',
 'smearing_change':'Somente import de LocalWickStressIdentificationR2 para R3; demais bytes preservados.',
 'new_hypotheses':[],'scientific_changes':False,
 'scope_limits':['R8 integral permanece aberto.','Igualdade local e smearing ainda candidatos até compilações e revisão independente.','Não há campo pontual limitado nem nova premissa de identificação Wick.','Fator, sinais, medida, Fock, domínio, fontes verdes e limites preservados.'],
 'verified_pin_pairs':len(checked),'verified_bytes':sum(x['bytes'] for x in checked.values()),
 'author_builds':0,'provider_calls':0,'production_changes':False,'mission_mutations':False,
 'script':pin(Path(__file__))}
dest=BASE/'LOCAL_WICK_IDENTIFICATION_REPAIR_R51_R3.json'
assert not dest.exists()
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8');tmp=dest.with_name(dest.name+'.tmp_r51')
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.rename(tmp,dest);assert dest.read_bytes()==data
print(json.dumps({'manifest':pin(dest),'sources':[x['source'] for x in new],
 'revision':m['receipt']['revision'],'verified_pins':len(checked)},ensure_ascii=False))

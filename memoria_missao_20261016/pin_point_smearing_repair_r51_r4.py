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
import difflib
previous=BASE/'LOCAL_WICK_IDENTIFICATION_REPAIR_R51_R3.json'
verify(read(previous))
old=BASE/'PointAnnihilationSmearingR3.lean';new=BASE/'PointAnnihilationSmearingR4.lean'
o=old.read_text(encoding='utf-8');n=new.read_text(encoding='utf-8')
headers=lambda s:re.findall(r'(?m)^theorem [\s\S]*?:= by',s)
assert headers(o)==headers(n)
prints=lambda s:re.findall(r'^#print axioms (.+)$',s,re.M)
assert prints(o)==prints(n) and len(prints(n))==11
assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s',n,re.M)
assert 'set_option maxHeartbeats 400000' in n and 'set_option synthInstance.maxHeartbeats 500000' in n
suppliers=[green(BASE/'RegularPointAnnihilationR2.lean'),green(BASE/'LocalWickStressIdentificationR3.lean')]
failed=OUT/'orbital_rotation/attempts/20261016T204650_618420Z'
r=read(failed/'RECEIPT.json');assert r['exit_code']==1
assert (failed/old.name).read_bytes()==old.read_bytes();verify(r)
req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
 input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
x=json.loads(run.stdout);assert x['ok'];m=x['result']
r8=next(y for y in m['projection']['active'] if y['id']=='R8');assert r8['status']=='working'
report={'schema':'iald-lean-repair/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'DECLARADO_PENDING_BUILD_AND_INDEPENDENT_REVIEW','requirement':'R8','requirement_satisfied':False,
 'author':ACTOR,'handle':'r51-wick-local-identification','mission_reference':pin(REF),
 'mission_receipt':m['receipt'],'projection_sha256':m['projection_sha256'],'criterion':r8['criterion'],
 'lease_observed':r8['lease'],'previous_manifest':pin(previous),'source':pin(new),
 'green_suppliers':suppliers,'failed_source':pin(old),'failed_receipt':pin(failed/'RECEIPT.json'),
 'failed_axioms':pin(failed/'AXIOMS.txt'),
 'public_theorem_headers_identical':True,'printed_declarations':prints(n),'expected_print_count':11,
 'diff':list(difflib.unified_diff(o.splitlines(),n.splitlines(),n=2)),
 'repairs':['regularDiagonal_value_expansion usa congrArg da soma e do subtipo e map_smul explícito, sem abrir regularExponential dentro de simp.',
 'regularDiagonal_integral usa calc, integral_smul/ integral_smul_const tipados e integral_finsetSum com função explícita; igualdade final por integral_congr_ae.',
 'scalarProfile_test_integrable é auxiliar privado em h:H1, com contração por integral_const_mul em calc. O enunciado público para RegularLabel somente o aplica.'],
 'new_physical_premises':[],'public_signatures_changed':False,
 'scope_limits':['O campo pontual é forma no domínio regular explícito; nenhum operador pontual limitado foi criado.',
 'A peça de smearing permanece candidata até recibo verde e revisão independente.',
 'R8 integral continua aberto; não há aceite de requisito nem mudança de gate.'],
 'verified_pin_pairs':len(checked),'verified_bytes':sum(z['bytes'] for z in checked.values()),
 'limits':{'maxHeartbeats':400000,'synthInstance.maxHeartbeats':500000},
 'author_builds':0,'provider_calls':0,'production_changes':False,'mission_mutations':False,
 'script':pin(Path(__file__))}
dest=BASE/'POINT_ANNIHILATION_SMEARING_REPAIR_R51_R4.json';assert not dest.exists()
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8');tmp=dest.with_name(dest.name+'.tmp_r51')
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data;os.rename(tmp,dest);assert dest.read_bytes()==data
print(json.dumps({'manifest':pin(dest),'source':pin(new),'revision':m['receipt']['revision'],
 'verified_pins':len(checked),'public_headers_identical':True},ensure_ascii=False))

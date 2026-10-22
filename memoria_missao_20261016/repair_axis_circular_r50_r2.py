from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
O=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
B=O/'maxwell_global'; W=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016')
REF=W/'FECHO_MISSION_REFERENCE.json'
ACTOR={'kind':'agent','id':'codex-r50-circular-field-transport'}
def pin(p):
 p=Path(p);b=p.read_bytes()
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def collect(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):yield x
  for v in x.values():yield from collect(v)
 elif isinstance(x,list):
  for v in x:yield from collect(v)
def project():
 req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
 p=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
 input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
 r=json.loads(p.stdout);assert r['ok'],r
 return r['result']
def exclusive(p,b):
 assert not p.exists()
 t=p.with_name(p.name+'.tmp_r50_axis_r2')
 with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b
 os.rename(t,p);assert p.read_bytes()==b
old=B/'AxisCompactCircularTransportR1.lean';new=B/'AxisCompactCircularTransportR2.lean'
oldbytes=old.read_bytes()
failed=O/'orbital_rotation/attempts/20261016T201140_308855Z'
assert (failed/old.name).read_bytes()==oldbytes
fr=read(failed/'RECEIPT.json');assert fr['exit_code']==1
oldpin=pin(old);assert fr['source']['sha256']==oldpin['sha256']
log=(failed/'AXIOMS.txt').read_text(encoding='utf-8')
assert ':28:28: error: expected token' in log
checkp=O/'mission_resume_20261016/LIVE_CHECK_R8_20261016T201437_860290Z_7abb8f0e_RECEIPT.json'
check=read(checkp);assert check['ok'] and check['result']['ready']
assert check['result']['task_id']=='R8'
handoff=O/'mission_resume_20261016/LIVE_HANDOFF_R8_20261016T201443_336385Z_d4d0a587_RECEIPT.json'
h=read(handoff);assert h['ok']
initial=project()
r8=next(x for x in initial['projection']['active'] if x['id']=='R8')
assert r8['status']=='working' and r8['lease']['id']==check['result']['lease_id']
assert r8['criterion']==check['result']['criterion']
anchor=b'open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions\n'
assert oldbytes.count(anchor)==1
newbytes=oldbytes.replace(anchor,anchor+b'open scoped ContDiff\n')
assert newbytes.replace(b'open scoped ContDiff\n',b'',1)==oldbytes
assert len(re.findall(rb'^#print axioms ',newbytes,re.M))==8
exclusive(new,newbytes)
checked={};greens=[]
for name,attempt,count in [
 ('FockSegalUnitaryTransportR1.lean','20261016T200236_367496Z',11),
 ('CircularPhysicalFieldTransportR1.lean','20261016T200456_963162Z',20)]:
 a=O/'orbital_rotation/attempts'/attempt;r=read(a/'RECEIPT.json')
 assert r['exit_code']==0 and (B/name).read_bytes()==(a/name).read_bytes()
 for x in collect(r):
  key=(x['path'],x['sha256'].lower())
  if key not in checked:
   actual=pin(x['path']);assert actual['sha256']==key[1],actual
   if 'bytes' in x:assert actual['bytes']==x['bytes']
   checked[key]=actual
 ax=(a/'AXIOMS.txt').read_text(encoding='utf-8')
 lists=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',ax)
 assert len(lists)==count and 'sorryAx' not in ax
 assert all(set(z.strip() for z in row.split(','))<={'propext','Classical.choice','Quot.sound'} for row in lists)
 greens.append({'source':pin(B/name),'receipt':pin(a/'RECEIPT.json'),'axioms':pin(a/'AXIOMS.txt'),
 'exit_code':0,'seconds':r['seconds'],'axiom_lists':count,'only_standard_trio':True})
final=project()
assert old.read_bytes()==oldbytes
report={
 'schema':'iald-lean-candidate-repair/v1','status':'DECLARADO_PENDING_BUILD',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'author':ACTOR,'handle':'r50-axis-r2','requirement':'R8','requirement_satisfied':False,
 'mission_reference':pin(REF),'initial_receipt':initial['receipt'],
 'mission_receipt':final['receipt'],'projection_sha256':final['projection_sha256'],
 'root_preflight':pin(checkp),'root_handoff':pin(handoff),
 'delegated_authority':'Root preflight rev342; root explicitly authorized this delegated R2 correction after rev343 without using the root actor identity. Own project refreshed before writing and before return.',
 'source':pin(new),'previous_source':oldpin,
 'failed_attempt':{'receipt':pin(failed/'RECEIPT.json'),'axioms':pin(failed/'AXIOMS.txt'),
 'exit_code':1,'seconds':fr['seconds'],'not_accepted':True},
 'change':'Exactly one added line: open scoped ContDiff. No other source byte differs after deleting that insertion. This activates C-infinity notation; WithTop top would mean omega and is not substituted.',
 'checks':{'same_statement_bytes':True,'same_imports':True,'same_limits_400000_500000':True,
 'same_eight_prints':True,'original_R1_unchanged':True,'new_mathematical_hypotheses':False},
 'green_suppliers':greens,'embedded_receipt_pins_verified':len(checked),
 'notation_api':pin(Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib\Analysis\Calculus\ContDiff\Defs.lean')),
 'prior_manifest':pin(B/'CIRCULAR_FIELD_TRANSPORT_CANDIDATE_R50_R1.json'),
 'scope':'Same circular transport of axis-compact smooth profiles and unique coherent coefficient domain. Local Wick/tensor identification and full R8 remain open.',
 'author_builds':0,'provider_calls':0,'production_changes':False,'mission_mutations':False,'script':pin(Path(__file__))
}
dst=B/'AXIS_COMPACT_CIRCULAR_TRANSPORT_REPAIR_R50_R2.json'
exclusive(dst,(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'source':pin(new),'manifest':pin(dst),'verified_pins':len(checked),
 'revision':final['receipt']['revision'],'prints':8,'author_builds':0},ensure_ascii=False))


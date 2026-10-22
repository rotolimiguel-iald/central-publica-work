
'''Version-independent sealed scientific memory synchronization. Default is read-only check.'''
import argparse,copy,json,os,re,sqlite3,sys
from pathlib import Path
from contextlib import closing
sys.dont_write_bytecode=True
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0,str(BASE))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.program_controls import require_claim
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now

class ScientificMemorySync:
 def __init__(self,module=cm,work=None,member='codex-coordenadora',unit='F0.3.MEMORIA_CIENTIFICA_SYNC',_allowed_roots=None):
  if unit not in ('F0.3','F0.3.MEMORIA_CIENTIFICA_SYNC'):raise ValueError('Scientific sync unit not admitted')
  self.unit=unit
  self.cm=module;self.work=Path(work or Path(__file__).parent);self.member=member
  self.allowed_roots=_allowed_roots or (Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'),Path(r'C:\IALD\Artigo\the_boundary'))
 def pin(self,path):
  p=Path(path);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':self.cm.digest(b)}
 def current_sources(self):
  catalog_raw=self.cm.CATALOG.read_bytes();catalog=json.loads(catalog_raw)
  entries=[e for e in catalog['files'] if Path(e['source']).suffix.lower()!='.pdf']
  if len(entries)!=13 or {Path(e['source']).name for e in entries}!=self.cm.SNAPSHOT_NAMES:raise ValueError('Thirteen admitted scientific originals required')
  payload={};pins=[]
  for e in entries:
   p=Path(e['source'])
   if not p.is_file() or p.is_symlink() or getattr(p,'is_junction',lambda:False)():raise ValueError('Source absent or redirected')
   if not any(p.resolve().is_relative_to(Path(r).resolve()) for r in self.allowed_roots):raise ValueError('Source outside admitted scientific roots')
   raw=p.read_bytes();raw.decode('utf-8-sig')
   payload[p.name]=raw;pins.append(dict(self.pin(p),mtime_ns=p.stat().st_mtime_ns))
  seal=json.loads(payload['um_absoluto_selo.json']);proof=json.loads(payload['tgl_kernel_proof_manifest.json'])
  version=seal['um_version']
  if not re.fullmatch(r'v[0-9]+',version):raise ValueError('Invalid sealed version')
  program=payload['um.py'].decode('utf-8-sig')
  versions=re.findall(r'(?m)^UM_VERSION\s*=\s*["\'](v[0-9]+)["\']',program)
  if versions!=[version]:raise ValueError('Program and seal versions differ')
  if seal['fail_closed_selftest']!='FAIL_CLOSED_SELFTEST_PASSED' or seal['formal_source_hash']!=proof['formal_source_hash']:raise ValueError('Seal/formal proof guard failed')
  for name,raw in payload.items():
   if name in seal['sha256'] and self.cm.digest(raw)!=seal['sha256'][name]:raise ValueError('Sealed source hash differs: '+name)
  for name in ('um.py','um_absoluto.json','tgl_kernel_proof_manifest.json'):
   if seal['sha256'].get(name)!=self.cm.digest(payload[name]):raise ValueError('Mandatory seal source missing')
  result=json.loads(payload['um_absoluto.json'])
  statutes={k:v for k,v in result['core'].items() if k.startswith('estatuto_') and isinstance(v,dict)}
  if not statutes or any(v.get('all_verified') is not True or v.get('does_not_gate_core') is not True for v in statutes.values()):raise ValueError('Statute guard failed')
  for record in statutes.values():
   cert=record.get('certificacao',{}).get('um_py_sha256_lido_de_si')
   if cert and cert!=self.cm.digest(payload['um.py']):raise ValueError('Statute self-hash differs')
  generation=self.cm.digest(json.dumps([(Path(p['path']).name,p['sha256']) for p in pins],ensure_ascii=False).encode())
  if self.cm.CATALOG.read_bytes()!=catalog_raw:raise ValueError('Catalog changed during inspection')
  for p in pins:
   if self.pin(p['path'])['sha256']!=p['sha256']:raise ValueError('Original changed during inspection')
  return {'version':version,'generation':generation,'epoch':version+'_'+generation[:16],
    'pins':pins,'catalog':catalog,'catalog_pin':self.pin(self.cm.CATALOG),'payload':payload,
    'formal_source_hash':seal['formal_source_hash'],'statutes':statutes}
 def check(self):
  current=self.current_sources();active_raw=self.cm.ACTIVE.read_bytes();active=json.loads(active_raw)
  manifest,fresh=self.cm.load(refresh=False)
  if manifest['generation']!=active['generation']:raise ValueError('Active pointer differs')
  return {'status':'CURRENT' if current['generation']==active['generation'] else 'SEALED_ADVANCE_PENDING_SYNC',
   'sealed_version':current['version'],'sealed_generation':current['generation'],'sealed_epoch':current['epoch'],
   'active':active,'active_pin':self.pin(self.cm.ACTIVE),'freshness':fresh,'documents':13,'provider_calls':0}
 def report_path(self,epoch):return self.work/('PREPARATION_'+epoch+'.json')
 def source_stable(self,report):
  if self.pin(self.cm.CATALOG)!=report['catalog_pin']:raise ValueError('Catalog pin changed')
  for p in report['sources']:
   measured=self.pin(p['path'])
   if measured['sha256']!=p['sha256'] or measured['bytes']!=p['bytes']:raise ValueError('Original changed; prepare a new sealed generation')
 def prepare(self):
  require_claim(self.unit,self.member)
  current=self.current_sources();active_raw=self.cm.ACTIVE.read_bytes();active=json.loads(active_raw)
  baseline,baseline_fresh=self.cm.load(refresh=False)
  if baseline['generation']!=active['generation']:raise ValueError('Baseline ACTIVE generation differs')
  target=self.cm.RELEASES/current['epoch'];root=target/'snapshots'/current['epoch']
  path=self.report_path(current['epoch'])
  if target.exists():
   if not path.exists():raise ValueError('Existing release without preparation receipt: recover, never rebuild')
   report=json.loads(path.read_bytes());self.verify(current['epoch'])
   return dict(report,status='REUSED_IMMUTABLE_RELEASE')
  self.work.mkdir(parents=True,exist_ok=True)
  save_json(self.work/('BUILD_INTENT_'+current['epoch']+'.json'),{'at':utc_now(),'epoch':current['epoch'],'target':str(target),'sources':current['pins'],'active_pin':self.pin(self.cm.ACTIVE)})
  root.mkdir(parents=True,exist_ok=False)
  staged=copy.deepcopy(current['catalog'])
  for e in staged['files']:
   src=Path(e['source'])
   if src.suffix.lower()=='.pdf':continue
   dst=root/src.name;replace_bytes(dst,current['payload'][src.name])
   stamp=next(p['mtime_ns'] for p in current['pins'] if p['path']==str(src));os.utime(dst,ns=(stamp,stamp));e['source']=str(dst)
  cat=self.work/('CATALOG_'+current['epoch']+'.json');save_json(cat,staged)
  m=self.cm.build(target,cat)
  if m['generation']!=current['generation']:raise ValueError('Builder generation mismatch')
  binding={'schema':1,'source_mode':self.cm.SNAPSHOT_MODE,'release':current['version'],'generation':m['generation'],
   'index_sha256':m['index_sha256'],'documents':[{k:d[k] for k in ('name','sha256','bytes')} for d in m['documents']],
   'formal_source_hash':current['formal_source_hash']}
  save_json(root/'SEALED_SNAPSHOT.json',binding)
  m.update(source_mode=self.cm.SNAPSHOT_MODE,snapshot_root=str(root),snapshot_manifest_sha256=self.cm.digest((root/'SEALED_SNAPSHOT.json').read_bytes()))
  save_json(target/'manifest.json',m)
  report={'status':'PREPARED_INACTIVE','at':utc_now(),'unit':self.unit,'release':current['version'],'epoch':current['epoch'],
   'generation':m['generation'],'target':str(target),'manifest':self.pin(target/'manifest.json'),
   'sources':current['pins'],'catalog_pin':current['catalog_pin'],'previous_active':active,'baseline_active_pin':{'path':str(self.cm.ACTIVE),'bytes':len(active_raw),'sha256':self.cm.digest(active_raw)},
   'documents':len(m['documents']),'chunks':m['chunks'],'statute_record_names':list(current['statutes']),
   'module_pin':self.pin(self.cm.__file__),'provider_calls':0,'source_execution':False}
  self.source_stable(report)
  if self.cm.ACTIVE.read_bytes()!=active_raw:raise ValueError('ACTIVE changed during preparation')
  save_json(self.work/('ESTATUTOS_'+current['epoch']+'.json'),{'source':self.pin(root/'um_absoluto.json'),
    'records':current['statutes'],'scope':'Existing records transcribed under ORIGINAL names, no new scientific execution or gate change.'})
  save_json(path,report);self.verify(current['epoch'])
  return report
 def verify(self,epoch):
  if not re.fullmatch(r'v[0-9]+_[0-9a-f]{16}',epoch):raise ValueError('Invalid epoch')
  active_raw=self.cm.ACTIVE.read_bytes();report=json.loads(self.report_path(epoch).read_bytes())
  target=Path(report['target'])
  if target!=self.cm.RELEASES/epoch:raise ValueError('Preparation target outside release tree')
  m,fresh=self.cm.load(target,refresh=False)
  if m['generation']!=report['generation'] or fresh!='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED':raise ValueError('Snapshot verifier refused')
  if self.pin(target/'manifest.json')!=report['manifest']:raise ValueError('Manifest pin changed')
  self.source_stable(report)
  with closing(sqlite3.connect((target/'index.sqlite3').as_uri()+'?mode=ro',uri=True)) as db:
   if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('Index integrity failed')
   if db.execute('SELECT COUNT(*) FROM passages').fetchone()[0]!=m['chunks']:raise ValueError('Chunk count differs')
   for d in m['documents']:
    expected=list(self.cm.chunks(Path(d['path']).read_bytes().decode('utf-8-sig')))
    actual=[(int(a),int(b),text) for a,b,text in db.execute('SELECT first_line,last_line,body FROM passages WHERE document=? ORDER BY rowid',(d['name'],))]
    if actual!=expected:raise ValueError('Chunk bytes/lines differ: '+d['name'])
   for record_name in report['statute_record_names']:
    if not db.execute('SELECT 1 FROM passages WHERE passages MATCH ? LIMIT 1',('"'+record_name+'"',)).fetchone():raise ValueError('Statute record not indexed: '+record_name)
  retrieval={}
  query=' '.join(report['statute_record_names'])
  for mode in ('standard','maximum','deepseek_maximum'):
   p=self.cm.prepare(query,target,allowed_sources=['um.py','um_absoluto.json','um_absoluto_selo.json','um_absoluto_forma_canonica.md'],mode=mode,max_chars=24000)
   if p['receipt']['generation']!=report['generation'] or p['receipt']['packet_sha256']!=self.cm.digest(p['prompt'].encode()):raise ValueError('Retrieval packet differs')
   retrieval[mode]=p['receipt']
  if self.cm.ACTIVE.read_bytes()!=active_raw:raise ValueError('Verification mutated ACTIVE')
  return {'status':'PASS','epoch':epoch,'generation':m['generation'],'documents':len(m['documents']),'chunks':m['chunks'],
   'checks':['seal_program_proof_pins','all_chunks_lines_exact_utf8_no_newline_translation','original_source_pins_stable','statute_names_preserved','three_retrieval_modes','ACTIVE_unchanged'],
   'retrieval':retrieval,'provider_calls':0,'source_execution':False}
 def activate(self,epoch):
  require_claim(self.unit,self.member)
  verified=self.verify(epoch);report=json.loads(self.report_path(epoch).read_bytes());self.source_stable(report)
  active=json.loads(self.cm.ACTIVE.read_bytes())
  baseline=report.get('baseline_active_pin')
  if not baseline or baseline['path']!=str(self.cm.ACTIVE):raise ValueError('Missing preparation ACTIVE baseline pin')
  pointer=self.cm.activate_release(self.cm.RELEASES/epoch,unit=self.unit,member=self.member,expected_active_sha256=baseline['sha256'])
  return {'status':'ALREADY_ACTIVE' if active==pointer else 'ACTIVATED_BY_EXISTING_API','pointer':pointer}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('operation',choices=['check','prepare','verify','activate'],nargs='?',default='check')
 parser.add_argument('--epoch');parser.add_argument('--unit',default='F0.3.MEMORIA_CIENTIFICA_SYNC');parser.add_argument('--member',default='codex-coordenadora')
 args=parser.parse_args();sync=ScientificMemorySync(member=args.member,unit=args.unit)
 if args.operation in ('verify','activate') and not args.epoch:parser.error('--epoch required')
 result=getattr(sync,args.operation)(args.epoch) if args.operation in ('verify','activate') else getattr(sync,args.operation)()
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()

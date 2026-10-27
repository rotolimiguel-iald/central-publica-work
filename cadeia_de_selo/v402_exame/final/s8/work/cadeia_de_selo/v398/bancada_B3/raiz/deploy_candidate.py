"""Operator-authorized B2 update: bounded files, byte backups and transactional rollback."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os
BASE=Path(__file__).resolve().parent
CANDIDATE=BASE/'candidate'
TARGET=Path(r'C:/IALD/Bancada_Um').resolve()
def digest(b):return hashlib.sha256(b).hexdigest()
def atomic(path,data):
 tmp=path.with_name(path.name+'.b2tmp')
 created=False
 try:
  with tmp.open('xb') as f:
   created=True;f.write(data);f.flush();os.fsync(f.fileno())
  if tmp.stat().st_size!=len(data):raise ValueError('short write')
  os.replace(tmp,path)
 finally:
  if created and tmp.exists():tmp.unlink()
def safe(rel):
 if Path(rel).is_absolute() or '..' in Path(rel).parts:raise ValueError('bad relative path')
 p=TARGET/rel
 if not p.resolve().is_relative_to(TARGET):raise ValueError('target escapes bench')
 return p
ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args()
mraw=(CANDIDATE/'canonical_contracts.json').read_bytes()
manifest=json.loads(mraw)
files={e['path']:e for e in manifest['code']+manifest['sources'] if not Path(e['path']).is_absolute()}
files['canonical_contracts.json']=dict(path='canonical_contracts.json',sha256=digest(mraw),bytes=len(mraw))
base={str(Path(e['source']).resolve()):e for e in json.loads((BASE/'BASELINE_R1.json').read_bytes())}
plan=[];candidate_bytes={}
for rel,e in files.items():
 dst=safe(rel);src=CANDIDATE/rel;b=src.read_bytes()
 if digest(b)!=e['sha256'] or len(b)!=e['bytes']:raise ValueError('candidate changed '+rel)
 candidate_bytes[rel]=b
 old=dst.read_bytes() if dst.exists() else None
 if str(dst) in base and (old is None or digest(old)!=base[str(dst)]['sha256']):raise ValueError('installed baseline drift '+rel)
 if old==b:continue
 if old is not None and str(dst) not in base:raise ValueError('unlisted overwrite '+rel)
 plan.append(dict(relative=rel,old_sha256=digest(old) if old is not None else None,new_sha256=digest(b),bytes=len(b)))
if not args.apply:
 with (BASE/'DEPLOY_PLAN_R1.json').open('x',encoding='utf-8') as f:json.dump(dict(created_utc=datetime.now(timezone.utc).isoformat(),manifest_sha256=digest(mraw),files=plan),f,ensure_ascii=False,indent=2)
 print(json.dumps(dict(files=len(plan),bytes=sum(e['bytes'] for e in plan))))
else:
 expected=json.loads((BASE/'DEPLOY_PLAN_R1.json').read_bytes())
 if plan!=expected['files'] or digest(mraw)!=expected['manifest_sha256']:raise ValueError('deployment plan changed')
 receipt=BASE/'DEPLOY_RECEIPT_R1.json'
 if receipt.exists():raise FileExistsError(receipt)
 stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
 done=[];begin=datetime.now(timezone.utc).isoformat()
 try:
  for e in plan:
   dst=safe(e['relative']);dst.parent.mkdir(parents=True,exist_ok=True)
   backup=None
   current=dst.read_bytes() if dst.exists() else None
   if (digest(current) if current is not None else None)!=e['old_sha256']:raise ValueError('last moment destination drift '+e['relative'])
   if dst.exists():
    old=current;backup=dst.with_name(dst.name+'.bak_B2_'+stamp)
    with backup.open('xb') as f:f.write(old)
    if backup.read_bytes()!=old:raise ValueError('backup differs')
   atomic(dst,candidate_bytes[e['relative']])
   done.append(dict(**e,backup=str(backup) if backup else None))
  for e in done:
   if digest(safe(e['relative']).read_bytes())!=e['new_sha256']:raise ValueError('postinstall pin')
  status='INSTALLED_AWAITING_RUNTIME_CHECK'
 except Exception as exc:
  rollback=[]
  for e in reversed(done):
   try:
    dst=safe(e['relative'])
    if e['backup']:atomic(dst,Path(e['backup']).read_bytes())
    else:dst.unlink()
    restored=dst.read_bytes() if dst.exists() else None
    if (digest(restored) if restored is not None else None)!=e['old_sha256']:raise ValueError('rollback pin mismatch')
    rollback.append(dict(path=e['relative'],restored=True))
   except Exception as rex:rollback.append(dict(path=e['relative'],restored=False,error=str(rex)))
  with (BASE/('DEPLOY_FAILURE_'+stamp+'.json')).open('x',encoding='utf-8') as f:json.dump(dict(error=str(exc),rollback=rollback,begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat()),f,indent=2)
  raise
 with receipt.open('x',encoding='utf-8') as f:json.dump(dict(status=status,begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),manifest_sha256=digest(mraw),files=done,operator_authorization='OPERADOR_ATUALIZACAO_VERBATIM_20261009.txt',gate_effect='NONE'),f,ensure_ascii=False,indent=2)
 print(json.dumps(dict(status=status,files=len(done),receipt=str(receipt))))

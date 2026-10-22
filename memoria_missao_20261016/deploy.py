"""Install only the pinned memory/MCP/instruction plan; preserve immediate byte backups."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,uuid
P=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def create(path,data):
    with path.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
receipt=P/'DEPLOYMENT.json'
if receipt.exists():raise SystemExit('Deployment receipt exists; inspect it instead of repeating.')
plan=json.loads((P/'DEPLOY_PLAN.json').read_bytes())
for r in plan['files']:
    source,target=Path(r['source']),Path(r['target'])
    assert sha(source.read_bytes())==r['new_sha256'],source
    assert (sha(target.read_bytes()) if target.exists() else None)==r['old_sha256'],target
for key in ['validation','review']:
    assert sha(Path(plan[key]['path']).read_bytes())==plan[key]['sha256']
review=json.loads(Path(plan['review']['path']).read_bytes())
assert review['verdict']=='PASS_WITH_SCOPE'
for source,expected in review['current_source_sha256'].items():
    assert sha(Path(source).read_bytes())==expected,'Reviewed source changed'
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
rows=[]
for r in plan['files']:
    source,target=Path(r['source']),Path(r['target']);new=source.read_bytes()
    old=target.read_bytes() if target.exists() else None
    assert (sha(old) if old is not None else None)==r['old_sha256'],'Target changed; stop'
    backup=None
    if old is not None:
        backup=target.with_name(target.name+'.bak_'+stamp+'_mission_sync')
        create(backup,old);assert backup.read_bytes()==old
    temporary=target.with_name(target.name+'.tmp_'+str(uuid.uuid4()))
    create(temporary,new)
    assert temporary.stat().st_size==len(new) and sha(temporary.read_bytes())==r['new_sha256']
    assert (sha(target.read_bytes()) if target.exists() else None)==r['old_sha256'],'Concurrent target modification; stop'
    if old is None:os.rename(temporary,target) # Windows refuses an existing destination.
    else:os.replace(temporary,target)
    assert sha(target.read_bytes())==r['new_sha256']
    row={**r,'backup':str(backup) if backup else None,'verified':True};rows.append(row)
    event=P/('DEPLOY_FILE_'+str(len(rows))+'.json')
    create(event,(json.dumps(row,ensure_ascii=False,indent=2)+'\n').encode())
create(receipt,(json.dumps({'unit':plan['unit'],'at':datetime.now(timezone.utc).isoformat(),'files':rows,
    'no_provider_calls':True,'no_existing_process_restarted':True,'no_scientific_production_changed':True},ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'ok':True,'files':len(rows),'receipt':str(receipt),'sha256':sha(receipt.read_bytes())}))

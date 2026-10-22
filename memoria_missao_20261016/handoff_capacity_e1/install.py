"""Install only the reviewed bridge delta and additive protocol paragraph."""
import hashlib,json,os,uuid
from pathlib import Path
from datetime import datetime,timezone
from prepare import ROOT,CORE,BRIDGE,TASK,new,pin,project,base,call

def sha(raw):return hashlib.sha256(raw).hexdigest()
def create(path,raw):
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())

def main():
    assert not (ROOT/'DEPLOYMENT_E1.json').exists()
    review=json.loads((ROOT/'REVIEW_E1.json').read_bytes())
    assert review['verdict'].startswith('PASS'),review['verdict']
    candidate=ROOT/'mission_bridge_candidate.py'
    # Exact candidate pin must be present in the independent review artifact.
    assert pin(candidate)['sha256'] in json.dumps(review)
    for n in ['VERIFICATION_CANDIDATE.json','SYNTHETIC_MCP.json']:
        v=json.loads((ROOT/n).read_bytes());assert v['ok'] and v['bridge']==pin(candidate)
    p=project('BEFORE_INSTALL');task=next(t for t in p['projection']['active'] if t['id']==TASK)
    call('mission_cli.py',{**base(p),'operation':'check','task_id':TASK,'lease_id':task['lease']['id']},'INSTALL_PREFLIGHT')
    original=json.loads((ROOT.parent/'DEPLOYMENT.json').read_bytes())
    expected={r['target']:r['new_sha256'] for r in original['files']}
    protocol=CORE/'MISSION_PROTOCOL.md'
    plans=[(BRIDGE,candidate.read_bytes(),False),(protocol,protocol.read_bytes()+(ROOT/'PROTOCOL_ADDENDUM.md').read_bytes(),True)]
    for target,raw,append in plans:
        assert sha(target.read_bytes())==expected[str(target)],'Concurrent target update'
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    rows=[]
    for target,raw,append in plans:
        old=target.read_bytes();assert sha(old)==expected[str(target)]
        backup=target.with_name(target.name+'.bak_'+stamp+'_handoff_e1')
        create(backup,old);assert backup.read_bytes()==old
        if append:assert raw.startswith(old) and len(raw)>len(old)
        temp=target.with_name(target.name+'.tmp_'+uuid.uuid4().hex)
        create(temp,raw);assert temp.stat().st_size==len(raw) and temp.read_bytes()==raw
        assert target.read_bytes()==old,'Concurrent target update'
        os.replace(temp,target);assert target.read_bytes()==raw
        row={'target':str(target),'old_sha256':sha(old),'new_sha256':sha(raw),
             'backup':pin(backup),'bytes':len(raw),'append_only':append}
        rows.append(row);new(f'DEPLOYED_FILE_{len(rows)}.json',row)
    dest=new('DEPLOYMENT_E1.json',{'ok':True,'at':datetime.now(timezone.utc).isoformat(),
        'unit':'F9.MEMORIA_MISSAO_20261016','files':rows,'review':pin(ROOT/'REVIEW_E1.json'),
        'existing_processes_restarted':False,'provider_calls':0,'science_changed':False})
    print(json.dumps({'ok':True,'files':len(rows),'receipt':str(dest)}))

if __name__=='__main__':main()

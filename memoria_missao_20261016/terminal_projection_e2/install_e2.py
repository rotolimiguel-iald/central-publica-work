"""Install reviewed projection code and additive instructions with byte backups."""
from support_e2 import *

def create(path,raw):
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert path.read_bytes()==raw

def main():
    if (BASE/'DEPLOYMENT_E2.json').exists():raise RuntimeError('Already installed; verify receipt')
    review=json.loads((BASE/'REVIEW_E2.json').read_bytes())
    assert review['verdict'].startswith('PASS')
    candidate=BASE/'mission_candidate.py'
    assert pin(candidate)['sha256'] in json.dumps(review)
    validation=json.loads((BASE/'TEST_RESULTS_E2.json').read_bytes())
    assert validation['ok'] and pin(candidate)['sha256'] in json.dumps(validation)
    preflight('INSTALL_E2')
    board=command([r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT],'INSTALL_BOARD')
    claim=board['reivindicacao'];assert claim['quem']==ACTOR['id']
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    baseline=json.loads((BASE/'SOURCE_BASELINE.json').read_bytes())
    plans=[dict(target=str(CORE/'lib/iald_memory/mission.py'),before=baseline['installed'],
                candidate=pin(candidate),append_only=False)]
    plans+=json.loads((BASE/'DOC_PLAN_E2.json').read_bytes())['files']
    for row in plans:
        assert pin(row['target'])['sha256']==row['before']['sha256'],'Concurrent change'
        assert pin(row['candidate']['path'])['sha256']==row['candidate']['sha256']
        assert row['candidate']['sha256'] in json.dumps(review),'Candidate not in independent review'
    new('INSTALL_PLAN_E2.json',dict(files=plans,review=pin(BASE/'REVIEW_E2.json'),claim=claim))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S')
    installed=[]
    for index,row in enumerate(plans,1):
        target=Path(row['target']);old=target.read_bytes();raw=Path(row['candidate']['path']).read_bytes()
        assert hashlib.sha256(old).hexdigest()==row['before']['sha256']
        if row['append_only']:assert raw.startswith(old) and len(raw)>len(old)
        backup=target.with_name(target.name+'.bak_'+stamp+'_terminal_e2');create(backup,old)
        temp=target.with_name(target.name+'.tmp_'+uuid.uuid4().hex);create(temp,raw)
        assert target.read_bytes()==old,'Concurrent change before replace'
        os.replace(temp,target);assert target.read_bytes()==raw
        done=dict(target=str(target),old_sha256=hashlib.sha256(old).hexdigest(),
            new_sha256=hashlib.sha256(raw).hexdigest(),backup=pin(backup),append_only=row['append_only'])
        installed.append(done);new('INSTALLED_E2_'+str(index)+'.json',done)
    new('DEPLOYMENT_E2.json',dict(ok=True,unit=UNIT,files=installed,review=pin(BASE/'REVIEW_E2.json'),
        at=dt.datetime.now(dt.timezone.utc).isoformat(),providers_called=False,existing_processes_restarted=False))
    print(json.dumps({'ok':True,'files':len(installed)}))

if __name__=='__main__':main()

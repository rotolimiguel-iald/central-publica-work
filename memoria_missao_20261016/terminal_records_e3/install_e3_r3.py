"""Install exactly reviewed E3 artifacts with a target allowlist and byte backups."""
from support_e3 import *

def create(path,raw):
    with path.open('xb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())
    assert path.read_bytes()==raw

def reviewed_plan(review):
    assert review['verdict'] in {'PASS','PASS_WITH_SCOPE'}
    entries=review['reviewed_artifacts']
    reviewed={str(Path(row['path']).resolve()):row['sha256'] for row in entries}
    assert len(reviewed)==len(entries),'Ambiguous reviewed artifact paths'
    def checked(path):
        actual=pin(path)
        assert reviewed.get(actual['path'])==actual['sha256'],'Unreviewed or changed artifact: '+str(path)
        return actual
    candidate=BASE/'mission_candidate_r2.py'
    baseline=BASE/'SOURCE_BASELINE_E3_R2.json'
    documents=BASE/'DOC_PLAN_E3_R3.json'
    validation=BASE/'TEST_RESULTS_E3_R2.json'
    for path in [Path(__file__),candidate,baseline,documents,validation,
        BASE/'verify_live_e3_r2.py',BASE/'TRACKER_TEST_RESULTS_E3_R3.json',
        OUT/'mission_resume_20261016/track_build_r46.py']:
        checked(path)
    validated=json.loads(validation.read_bytes())
    assert validated['ok']
    assert validated['candidate']['path']==str(candidate)
    assert validated['candidate']['sha256']==pin(candidate)['sha256']
    prior=json.loads(baseline.read_bytes())['base']
    target=CORE/'lib/iald_memory/mission.py'
    assert str(Path(prior['path']).resolve())==str(target.resolve())
    plans=[dict(target=str(target),before=prior,candidate=checked(candidate),append_only=False)]
    docrows=json.loads(documents.read_bytes())['files']
    expected={str((CORE/'MISSION_PROTOCOL.md').resolve()),
        str(Path(r'C:\Users\rotol\.codex\AGENTS.md').resolve()),
        str(Path(r'C:\Users\rotol\.claude\CLAUDE.md').resolve())}
    assert len(docrows)==3
    assert {str(Path(row['target']).resolve()) for row in docrows}==expected
    for row in docrows:
        assert row['append_only'] is True
        assert checked(row['candidate']['path'])['sha256']==row['candidate']['sha256']
        assert str(Path(row['before']['path']).resolve())==str(Path(row['target']).resolve())
        plans.append(row)
    for row in plans:
        assert pin(row['target'])['sha256']==row['before']['sha256'],'Concurrent target change'
        raw=Path(row['candidate']['path']).read_bytes()
        if row['append_only']:
            old=Path(row['target']).read_bytes()
            assert raw.startswith(old) and len(raw)>len(old)
    return plans

def main():
    if (BASE/'DEPLOYMENT_E3.json').exists():raise RuntimeError('Already installed; recover receipt')
    review=json.loads((BASE/'REVIEW_E3_R3.json').read_bytes())
    plans=reviewed_plan(review)
    preflight('INSTALL_E3')
    claim=command([r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT],'INSTALL_BOARD')['reivindicacao']
    assert claim['quem']==ACTOR['id']
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    new('INSTALL_PLAN_E3.json',dict(files=plans,review=pin(BASE/'REVIEW_E3_R3.json'),claim=claim))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S')
    installed=[]
    for index,row in enumerate(plans,1):
        target=Path(row['target']);old=target.read_bytes();raw=Path(row['candidate']['path']).read_bytes()
        assert hashlib.sha256(old).hexdigest()==row['before']['sha256']
        assert hashlib.sha256(raw).hexdigest()==row['candidate']['sha256']
        backup=target.with_name(target.name+'.bak_'+stamp+'_terminal_e3');create(backup,old)
        temporary=target.with_name(target.name+'.tmp_'+uuid.uuid4().hex);create(temporary,raw)
        assert target.read_bytes()==old,'Concurrent change before replace'
        os.replace(temporary,target)
        assert target.read_bytes()==raw
        done=dict(target=str(target),old_sha256=hashlib.sha256(old).hexdigest(),
            new_sha256=hashlib.sha256(raw).hexdigest(),backup=pin(backup),append_only=row['append_only'])
        installed.append(done);new('INSTALLED_E3_'+str(index)+'.json',done)
    new('DEPLOYMENT_E3.json',dict(ok=True,unit=UNIT,files=installed,
        review=pin(BASE/'REVIEW_E3_R3.json'),at=dt.datetime.now(dt.timezone.utc).isoformat(),
        providers_called=False,existing_processes_restarted=False))
    print(json.dumps({'ok':True,'files':len(installed)}))

if __name__=='__main__':main()
